import pandas as pd
import pytest
from financial_intelligence_lab.core import make_ledger,make_budget,pnl,summary_by_month
from financial_intelligence_lab.report import render_html

def test_seed_is_deterministic():
    pd.testing.assert_frame_equal(make_ledger(42),make_ledger(42))

def test_different_seeds():
    assert not make_ledger(1).equals(make_ledger(2))

def test_unique_transactions():
    assert make_ledger().entry_id.is_unique

def test_revenue_minus_cost_equals_gross():
    p=pnl(make_ledger(),make_budget())
    assert (p.actual_revenue-p.actual_cogs-p.actual_gross_profit).abs().max()<.011

def test_operating_profit_identity():
    p=pnl(make_ledger(),make_budget())
    assert (p.actual_gross_profit-p.actual_opex-p.actual_operating_profit).abs().max()<.011

def test_budget_variance_identity():
    p=pnl(make_ledger(),make_budget())
    assert (p.actual_operating_profit-p.budget_operating_profit-p.operating_profit_variance).abs().max()<.011

def test_monthly_rollup_conserves_revenue():
    p=pnl(make_ledger(),make_budget())
    assert summary_by_month(p).actual_revenue.sum()==pytest.approx(p.actual_revenue.sum(),abs=.01)

def test_duplicate_budget_key_is_rejected():
    b=make_budget();b=pd.concat([b,b.iloc[:1]],ignore_index=True)
    with pytest.raises(ValueError,match="duplicate"):pnl(make_ledger(),b)

def test_unknown_account_rejected():
    l=make_ledger();l.loc[0,"account"]="salaries-private"
    with pytest.raises(ValueError,match="unknown"):pnl(l,make_budget())

def test_negative_amount_rejected():
    l=make_ledger();l.loc[0,"amount"]=-5
    with pytest.raises(ValueError,match="nonnegative"):pnl(l,make_budget())

def test_fictional_dashboard(tmp_path):
    dest=tmp_path/"dashboard.html";render_html(summary_by_month(pnl(make_ledger(),make_budget())),dest)
    assert "100% synthetic" in dest.read_text()
