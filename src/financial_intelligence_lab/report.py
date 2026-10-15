"""Build a self-contained management dashboard for fictional finance data."""
from html import escape
from pathlib import Path
import pandas as pd


def render_html(months:pd.DataFrame,out: str|Path) ->None:
    if months.empty:raise ValueError("Empty monthly report")
    revenue=float(months.actual_revenue.sum())
    op=float(months.actual_operating_profit.sum())
    margin=100*op/revenue if revenue else 0
    variance=float(months.operating_profit_variance.sum())
    cards=[("TOTAL REVENUE",f"SYN {revenue:,.0f}"),("OPERATING PROFIT",f"SYN {op:,.0f}"),("OPERATING MARGIN",f"{margin:.1f}%"),("VS. BUDGET",f"SYN {variance:+,.0f}")]
    elements="".join(f'<div class="stat"><small>{escape(k)}</small><strong>{escape(v)}</strong></div>' for k,v in cards)
    maxvalue=max(float(x) for x in months.actual_revenue)
    bars="".join(f'<div class="row"><span>{escape(str(x.month))}</span><div class="track"><div class="fill" style="width:{max(0,100*float(x.actual_revenue)/maxvalue):.2f}%"></div></div><span>{float(x.actual_revenue):,.0f}</span></div>' for x in months.itertuples())
    html=f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Financial Intelligence Lab | Synthetic P&amp;L</title><style>:root{{--bg:#0a1023;--fg:#e9f2ff;--cyan:#51dfff;--purple:#ae93ff}}*{{box-sizing:border-box}}body{{margin:0;background:linear-gradient(140deg,#0a1023,#201534);color:var(--fg);font:16px system-ui,Arial}}main{{max-width:1100px;margin:auto;padding:42px 22px}}h1{{font-size:clamp(30px,5vw,56px)}}h1 span{{color:var(--cyan)}}.muted,small{{color:#b4c5df}}.micro{{color:var(--purple);letter-spacing:3px;font-size:12px}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:30px 0}}.stat,.panel{{background:#15213be8;border:1px solid #344565;padding:21px;border-radius:14px}}strong{{display:block;margin:12px 0 0;color:var(--cyan);font-size:27px}}.row{{display:grid;grid-template-columns:75px 1fr 100px;align-items:center;gap:14px;margin:13px 0}}.track{{height:13px;background:#303957;border-radius:12px;overflow:hidden}}.fill{{height:100%;background:linear-gradient(90deg,var(--cyan),var(--purple))}}.caption{{font-size:13px;color:#bdcae3;margin:20px 0}}</style></head><body><main><div class="micro">MELISSA CASTRO // FINANCIAL ANALYTICS</div><h1>Financial <span>Intelligence Lab</span></h1><p class="muted">Auditable fictional income statement and budget variance analysis</p><div class="cards">{elements}</div><div class="panel"><h2>Monthly revenue</h2><p class="muted">Units: SYN (a fictitious currency label)</p>{bars}</div><p class="caption">100% synthetic. Gross profit = revenue − cost of goods. Operating profit = gross profit − operating expenses. Budget variance = actual − budget. No real financial records or financial advice.</p></main></body></html>"""
    dest=Path(out);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(html,encoding="utf-8")
