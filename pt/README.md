# nstate — Portugal (PT)

**Status:** Live — Eurostat data loaded. INE national detail open for contribution.  
**Chapter lead:** open  
**Live page:** [nstate.org/pt](https://nstate.org/pt)

---

## Data loaded

All data from Eurostat. Updated annually when Eurostat publishes.

| Dataset | Eurostat code | Coverage |
|---|---|---|
| Govt expenditure / debt / deficit | gov_10dd_edpt1, gov_10a_exp | 1995–2025 |
| Tax revenue | gov_10a_taxag | 1995–2025 |
| Public employment (NACE O-Q) | nama_10_a64_e | 1995–2024 |

## National data (open for contribution)

Portugal's national statistics office is **INE** (Instituto Nacional de Estatística):
- API: https://www.ine.pt/ine/statistic_information.jsp
- Key datasets to add:
  - Employment by sector (LFS microdata equivalent)
  - Regional GDP (NUT II/III)
  - Housing prices by municipality (Confidencial Imobiliário / INE)
  - Government revenue breakdown (DGO — Direção-Geral do Orçamento)

## Key narratives

Portugal had one of the biggest fiscal crises in the EU (2010–2014 IMF bailout, debt peaked ~132% GDP) followed by one of the strongest fiscal recoveries. As of 2025 debt is at ~90% and Portugal is running a budget surplus.

## Contributing

1. Fork the repo and create `pt/pipelines/`
2. Write a pipeline that fetches from INE or another authoritative Portuguese source
3. Write to a `pt_<dataset>` table in DuckDB following the naming convention
4. Submit a PR — the data appears in the agent immediately on merge

## Questions?

Open an issue tagged `[pt]` in the [nstate repository](https://github.com/nstate-project/nstate).
