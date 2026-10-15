# Engineering decisions

- A deterministic random seed makes all generated values reproducible.
- Currency label `SYN` signals the data are illustrative, **not actual USD, GTQ, or COP**.
- Source ledger stores transaction rows, not precomputed KPIs; aggregation logic remains verifiable.
- Strict budget join guards against dropped or duplicated month/channel/account entries.
- Tests check accounting identities and rollup conservation.
- The offline preview uses simple HTML/CSS with no tracking calls or external scripts.
- Not implemented: corporate consolidation, tax, accrual accounting, cash flow, FX or regulatory reporting.
