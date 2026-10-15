# Business Intelligence implementation

Load the generated `synthetic_ledger.csv` and `synthetic_budget.csv` into Power BI. Build Date, Account and Channel dimensions, and connect each dimension to both fact tables. Do not create an ambiguous fact-to-fact relationship.

## Core DAX

```DAX
Actual Revenue = CALCULATE(SUM(Ledger[amount]), Accounts[account] = "revenue")
Actual COGS = CALCULATE(SUM(Ledger[amount]), Accounts[account] = "cogs")
Actual Opex = CALCULATE(SUM(Ledger[amount]), Accounts[account] = "opex")
Gross Profit = [Actual Revenue] - [Actual COGS]
Operating Profit = [Gross Profit] - [Actual Opex]
Operating Margin % = DIVIDE([Operating Profit], [Actual Revenue])
Budget Revenue = CALCULATE(SUM(Budget[budget_amount]), Accounts[account] = "revenue")
Budget COGS = CALCULATE(SUM(Budget[budget_amount]), Accounts[account] = "cogs")
Budget Opex = CALCULATE(SUM(Budget[budget_amount]), Accounts[account] = "opex")
Budget Operating Profit = [Budget Revenue] - [Budget COGS] - [Budget Opex]
Operating Profit Variance = [Operating Profit] - [Budget Operating Profit]
```

Measures assume a shared Accounts dimension filters both tables; budget filtering does **not** work correctly without proper relationships. Use percentage formatting in Power BI for the ratio measures, not a separate ×100.

## Report pages

1. Executive snapshot — revenue, gross margin, operating profit, variance.
2. Variance waterfall — monthly and channel breakdown, favorable/unfavorable labeling.
3. Profitability — channel and period contribution; explicitly distinguish revenue mix from profitability.
4. Controls — source totals, duplicate budget keys, missing months, reconciliation checks.

No PBIX is bundled: this is a transparent, independently reproducible blueprint.
