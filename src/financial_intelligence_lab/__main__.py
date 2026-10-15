import argparse
from pathlib import Path
from .core import make_ledger, make_budget, pnl, summary_by_month
from .report import render_html

def main(argv=None):
    p=argparse.ArgumentParser(description="Fictional, auditable P&L lab")
    p.add_argument("command",choices=["demo"])
    p.add_argument("--seed",type=int,default=2026)
    p.add_argument("--out-dir",default="build/demo")
    args=p.parse_args(argv);dest=Path(args.out_dir);dest.mkdir(parents=True,exist_ok=True)
    ledger=make_ledger(args.seed);budget=make_budget(args.seed)
    report=pnl(ledger,budget);months=summary_by_month(report)
    for filename,df in (("synthetic_ledger.csv",ledger),("synthetic_budget.csv",budget),("channel_pnl.csv",report),("monthly_pnl.csv",months)):
        df.to_csv(dest/filename,index=False,float_format="%.2f")
    render_html(months,dest/"dashboard.html")
    print(f"Built fictional P&L for {len(months)} months in {dest}")

if __name__=="__main__":main()
