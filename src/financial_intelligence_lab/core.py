"""Fictional bookkeeping events and auditable income-statement calculations."""
from __future__ import annotations
from random import Random
import pandas as pd

CHANNELS=("Retail","Online","Wholesale","Partners")
ACCOUNTS=("revenue","cogs","opex")

def make_ledger(seed: int=2026) -> pd.DataFrame:
    rng=Random(seed)
    rows=[]; counter=1
    for month in range(1,13):
        for channel in CHANNELS:
            for account in ACCOUNTS:
                for _ in range(8):
                    magnitude={"revenue":8000,"cogs":3900,"opex":2100}[account]
                    # Positive magnitudes for all types; reporting signs assigned at aggregation.
                    amount=round(magnitude*rng.uniform(.75,1.27),2)
                    rows.append({"entry_id":f"FI-{counter:06d}","month":f"2026-{month:02d}","channel":channel,"account":account,"amount":amount,"currency":"SYN"})
                    counter+=1
    return pd.DataFrame(rows)


def make_budget(seed: int=2026) -> pd.DataFrame:
    """Deterministic fictional budgets by month/channel/account."""
    rng=Random(seed+73)
    rows=[]
    for month in range(1,13):
        for channel in CHANNELS:
            for account in ACCOUNTS:
                magnitude={"revenue":8000,"cogs":3900,"opex":2100}[account]
                rows.append({"month":f"2026-{month:02d}","channel":channel,"account":account,"budget_amount":round(8*magnitude*rng.uniform(.92,1.08),2)})
    return pd.DataFrame(rows)


def pnl(ledger: pd.DataFrame, budget: pd.DataFrame) -> pd.DataFrame:
    required={"month","channel","account","amount"}
    if not required.issubset(ledger):raise ValueError("ledger missing required columns")
    if not {"month","channel","account","budget_amount"}.issubset(budget):raise ValueError("budget missing required columns")
    if ledger.empty or budget.empty:raise ValueError("empty dataset")
    if not ledger.account.isin(ACCOUNTS).all() or not budget.account.isin(ACCOUNTS).all():raise ValueError("unknown account")
    if (ledger.amount<0).any() or (budget.budget_amount<0).any():raise ValueError("amounts must be nonnegative magnitudes")
    grouping=["month","channel","account"]
    actual=ledger.groupby(grouping,as_index=False,sort=True)["amount"].sum()
    if budget.duplicated(grouping).any():raise ValueError("duplicate budget key")
    merged=actual.merge(budget,on=grouping,how="outer",indicator=True,validate="one_to_one")
    if not merged._merge.eq("both").all():raise ValueError("missing budget or actual account rows")
    long=merged.drop(columns="_merge")
    a=long.pivot(index=["month","channel"],columns="account",values="amount")
    b=long.pivot(index=["month","channel"],columns="account",values="budget_amount")
    for df in (a,b):
        if df.isna().any().any():raise ValueError("incomplete month/channel/account combinations")
    out=pd.DataFrame(index=a.index)
    for name,frame in (("actual",a),("budget",b)):
        out[f"{name}_revenue"]=frame["revenue"]
        out[f"{name}_cogs"]=frame["cogs"]
        out[f"{name}_opex"]=frame["opex"]
        out[f"{name}_gross_profit"]=frame["revenue"]-frame["cogs"]
        out[f"{name}_operating_profit"]=frame["revenue"]-frame["cogs"]-frame["opex"]
    out["operating_profit_variance"]=out["actual_operating_profit"]-out["budget_operating_profit"]
    out["actual_gross_margin_pct"]=(100*out["actual_gross_profit"] / out["actual_revenue"]).where(out["actual_revenue"]!=0).round(2)
    out["actual_operating_margin_pct"]=(100*out["actual_operating_profit"] / out["actual_revenue"]).where(out["actual_revenue"]!=0).round(2)
    return out.reset_index().round(2)


def summary_by_month(report: pd.DataFrame) -> pd.DataFrame:
    if report.empty:raise ValueError("empty report")
    numeric=["actual_revenue","actual_cogs","actual_opex","actual_gross_profit","actual_operating_profit","budget_operating_profit","operating_profit_variance"]
    out=report.groupby("month",as_index=False)[numeric].sum()
    out["gross_margin_pct"]=(100*out["actual_gross_profit"]/out["actual_revenue"]).where(out["actual_revenue"]!=0).round(2)
    out["operating_margin_pct"]=(100*out["actual_operating_profit"]/out["actual_revenue"]).where(out["actual_revenue"]!=0).round(2)
    return out.round(2)
