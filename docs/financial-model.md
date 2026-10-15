# Auditable financial model

## Statement scope

A simplified management P&L is built from positive-valued ledger magnitudes classified as `revenue`, `cogs`, or `opex`. Negative numbers are not needed to represent expenses; the sign comes from the account classification at rollup.

- Gross profit = Revenue − Cost of goods sold.
- Operating profit = Gross profit − Operating expenses.
- Gross margin (%) = Gross profit / Revenue × 100; undefined if revenue is zero.
- Operating margin (%) = Operating profit / Revenue × 100; undefined if revenue is zero.
- Operating-profit variance = Actual operating profit − Budget operating profit.

Budgets and actuals must have the same month/channel/account keys. Duplicated budgets and missing account combinations fail fast, instead of quietly filling with zero.

## Deliberate exclusions

This is **not** a GAAP/IFRS income statement or a balance sheet. It does not model tax, depreciation, inventory valuation, currency conversion, rebates, cash flows, liabilities, accruals, or audit controls. All amounts use `SYN`, a fictional currency label. Do not use for financial decisions.
