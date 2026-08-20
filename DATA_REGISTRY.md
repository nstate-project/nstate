# nstate Data Registry

Every table in the nstate DuckDB must be registered here before any pipeline runs.
This file is the single source of truth for schema conventions, coverage, and data quality.

---

## Naming conventions

| Prefix | Geography | Examples |
|--------|-----------|---------|
| `uk_` | United Kingdom | `uk_hmrc_tax_receipts`, `uk_ons_gdp` |
| `eu_` | EU member states (Eurostat) | `eu_government_finance`, `eu_vat_rates` |
| `meta_` | Platform metadata | `meta_findings`, `meta_datasets` |

**Column unit suffixes** (use consistently):
- `_pct_gdp` — percentage of GDP
- `_thousands` — headcount in thousands
- `_gbpm` — GBP millions
- `_rate` — a rate/ratio/percentage
- `_pct` — a plain percentage

**Format conventions:**
- Long/narrow tables preferred over wide (add `indicator VARCHAR` column rather than multiple value columns)
- `PRIMARY KEY (country, year, indicator)` for time-series EU tables
- `loaded_at VARCHAR` on every table (ISO 8601 timestamp string)
- Country codes: 2-letter ISO (EU Eurostat convention: `EL`=Greece, `EU27_2020`=EU average)

---

## EU tables

### eu_government_finance
| Property | Value |
|----------|-------|
| **Pipeline** | `eu/pipelines/eu_government_finance.py` |
| **Source** | Eurostat `gov_10a_exp`, `gov_10dd_edpt1` |
| **Coverage** | 27 EU countries + EU27_2020 aggregate · 1990–2025 · annual |
| **Rows** | ~2,538 |
| **Update** | Annual (Eurostat September release) |
| **Licence** | Eurostat reuse policy (free, attribution required) |

Indicators (`indicator` column exact values):
- `expenditure_pct_gdp` — total government expenditure % GDP
- `deficit_pct_gdp` — EDP deficit % GDP (positive = surplus)
- `debt_pct_gdp` — gross government debt % GDP

> **Note:** Finland has data from 1990 (banking crisis era). All other countries start 1995.

---

### eu_tax_revenue
| Property | Value |
|----------|-------|
| **Pipeline** | `eu/pipelines/eu_tax_revenue.py` |
| **Source** | Eurostat `gov_10a_taxag` (D2_D5_D91_D61) |
| **Coverage** | 27 EU countries + EU27_2020 · 1995–2025 · annual |
| **Rows** | ~848 |
| **Update** | Annual |
| **Licence** | Eurostat reuse policy |

Columns: `country`, `year`, `value_pct_gdp` (total tax + social contributions as % GDP), `loaded_at`.

---

### eu_tax_breakdown
| Property | Value |
|----------|-------|
| **Pipeline** | `eu/pipelines/eu_tax_breakdown.py` |
| **Source** | Eurostat `gov_10a_taxag` (6 na_item codes) |
| **Coverage** | 27 EU countries + EU27_2020 · 1995–2025 · annual |
| **Rows** | ~4,736 |
| **Update** | Annual |
| **Licence** | Eurostat reuse policy |

Indicators (`indicator` column exact values):
- `vat_pct_gdp` — VAT (D211) as % GDP · all 27 countries
- `employee_social_contrib_pct_gdp` — employee social contributions (D613CE) · all 27
- `employer_social_contrib_pct_gdp` — employer social contributions (D611C) · all 27
- `excise_duties_pct_gdp` — excise duties (D214A) · all 27
- `corporate_tax_pct_gdp` — corporate income tax (D51B) · **24/27 countries** (EE, LV, LT not separately reported)
- `personal_income_tax_pct_gdp` — personal income tax (D51A) · **23/27 countries** (some countries bundle personal + corporate)

> **Coverage note:** Corporate and personal income tax breakdown is unavailable for countries using distribution-based corporate tax systems (Estonia, Latvia) and some bundled-reporting countries. This is a Eurostat data limitation, not a pipeline error.

---

### eu_labour_tax_wedge
| Property | Value |
|----------|-------|
| **Pipeline** | `eu/pipelines/eu_labour_tax_wedge.py` |
| **Source** | Eurostat `earn_nt_taxrate` |
| **Coverage** | 27 EU countries (no EU27 aggregate) · 2000–2025 · annual |
| **Rows** | ~1,965 |
| **Update** | Annual |
| **Licence** | Eurostat reuse policy |

Definition: effective percentage of **gross labour cost** (salary + employer social contributions) going to income tax and social contributions. Single person, no children.

Income levels (`income_level` column exact values):
- `AW67` — 67% of national average wage
- `AW100` — 100% of average wage
- `AW125` — 125% of average wage

> **Interpretation:** If `tax_wedge_pct = 38.0` for DE at AW100, then of every €100 an employer spends on a worker, €38 goes to the government before the worker sees any money.

---

### eu_tax_rates
| Property | Value |
|----------|-------|
| **Pipeline** | `eu/pipelines/eu_tax_rates.py` |
| **Source** | OECD Taxing Wages 2024; EC Taxation Trends in the European Union 2024 |
| **Coverage** | 27 EU countries · static 2024 |
| **Rows** | 54 (27 × 2 rate types) |
| **Update** | Manual — refresh when EC publishes annual Taxation Trends report (usually October) |
| **Licence** | OECD/EC open data |

Rate types (`tax_type` column exact values):
- `personal_top_rate` — top marginal statutory personal income tax rate %
- `corporate_rate` — headline statutory corporate income tax rate %

> **Note on corporate rates:** DE includes trade tax (~15% federal + ~15% local), IE is 12.5% (15% from 2024 for multinationals >€750m turnover), EE/LV tax only distributed profits (22%/20% shown are on-distribution rates).

---

### eu_vat_rates
| Property | Value |
|----------|-------|
| **Pipeline** | `eu/pipelines/eu_vat_rates.py` |
| **Source** | EC "VAT Rates Applied in the Member States" 2024 |
| **Coverage** | 27 EU countries · static 2024 |
| **Rows** | 27 |
| **Update** | Manual — check EC document annually. DK has no reduced rate (NULL). |
| **Licence** | EC open data |

Columns: `standard_rate`, `reduced_rate` (NULL where no reduced rate), `year`, `source`.

Range: LU 17% (lowest) → HU 27% (highest standard rate in EU).

---

### eu_public_employment
| Property | Value |
|----------|-------|
| **Pipeline** | `eu/pipelines/eu_public_employment.py` |
| **Source** | Eurostat `nama_10_a64_e` (NACE O-Q sectors) |
| **Coverage** | 27 EU countries + EU27_2020 · 1975–2025 · annual |
| **Rows** | ~871 |
| **Update** | Annual |
| **Licence** | Eurostat reuse policy |

Column: `employment_thousands` — persons employed in public administration, education, and health (NACE sectors O, P, Q combined).

---

## UK tables

### uk_civil_service_headcount
| Property | Value |
|----------|-------|
| **Pipeline** | `data/uk/pipelines/civil_service.py` |
| **Source** | Cabinet Office Civil Service Statistics (annual, March census) |
| **Coverage** | 2010–2024 · annual |
| **Rows** | 15 (UK total only — department breakdown not yet loaded) |
| **Update** | Annual (September release) |
| **Licence** | OGL v3 |

---

### uk_ons_cpih
| Property | Value |
|----------|-------|
| **Source** | ONS Consumer Prices Index including owner-occupiers' housing costs |
| **Coverage** | Apr 2000 – present · monthly |
| **Rows** | ~55,754 |
| **Update** | Monthly |
| **Licence** | OGL v3 |

`aggregate_code = 'CP00'` for headline CPIH. Year-on-year % must be calculated by joining to the same month previous year.

---

### uk_ons_gdp
| Property | Value |
|----------|-------|
| **Source** | ONS GDP monthly index |
| **Coverage** | Monthly · 2019=100 base |
| **Rows** | ~9,477 |
| **Licence** | OGL v3 |

---

### uk_ons_labour_market
| Property | Value |
|----------|-------|
| **Source** | ONS Labour Market Statistics |
| **Coverage** | Monthly rolling quarters |
| **Rows** | ~31,968 |
| **Licence** | OGL v3 |

---

### uk_ons_house_prices
| Property | Value |
|----------|-------|
| **Source** | ONS UK House Price Index by local authority |
| **Coverage** | 2012–2022 · by local authority (331 LAs) |
| **Rows** | ~695,897 |
| **Licence** | OGL v3 |

> **Latest data: 2022.** Do not query `year > '2022'` — no data exists.

---

### uk_ons_wages
| Property | Value |
|----------|-------|
| **Source** | ONS Annual Survey of Hours and Earnings (ASHE) |
| **Coverage** | Regional · public/private sector · annual |
| **Rows** | ~380,140 |
| **Licence** | OGL v3 |

---

### uk_hmrc_tax_receipts
| Property | Value |
|----------|-------|
| **Source** | HMRC Tax Receipts and National Insurance Contributions |
| **Coverage** | Fiscal years 1999–2026 |
| **Rows** | ~693 |
| **Licence** | OGL v3 |

`year` = fiscal year end (2026 = April 2025 – March 2026).

---

### uk_pesa_functional
| Property | Value |
|----------|-------|
| **Source** | HM Treasury Public Expenditure Statistical Analyses (PESA 2025) |
| **Coverage** | By function · 2019–2029 (2026+ are plans, not outturn) |
| **Rows** | ~4,124 |
| **Licence** | OGL v3 |

> **ALWAYS filter `year <= 2025`** for real outturn. 2026–2029 are forward spending plans.

---

### uk_pesa_departmental
| Property | Value |
|----------|-------|
| **Source** | HM Treasury PESA 2025 (departmental tables) |
| **Coverage** | By department · annual |
| **Rows** | ~990 |
| **Licence** | OGL v3 |

---

### uk_dwp_benefits
| Property | Value |
|----------|-------|
| **Source** | DWP Stat-Xplore |
| **Coverage** | Quarterly · 4 major benefits |
| **Rows** | 28 |
| **Licence** | OGL v3 |

Benefits loaded: Universal Credit, Personal Independence Payment, State Pension, Housing Benefit.

---

### uk_spend_25k
| Property | Value |
|----------|-------|
| **Source** | HM Treasury government spending over £25,000 |
| **Coverage** | Rolling — 1,794 transactions loaded |
| **Rows** | 1,794 |
| **Licence** | OGL v3 |

---

### uk_contracts
| Property | Value |
|----------|-------|
| **Source** | Find a Tender (UK government procurement) |
| **Coverage** | 500 most recent contracts |
| **Rows** | 500 |
| **Licence** | OGL v3 |

---

## Adding a new table (checklist)

1. **Register here first** — add an entry to this file before writing any code
2. **Name the table** — follow `{geography}_{source}_{topic}` pattern
3. **Choose format** — long/narrow (with `indicator` column) for multi-metric time series; wide only for single-metric tables
4. **Write pipeline** — `eu/pipelines/` or `data/uk/pipelines/` following existing patterns
5. **Update schema_eu.py / schema_uk.py** — add `CREATE TABLE IF NOT EXISTS` DDL
6. **Update agent.py SCHEMA_SUMMARY** — add table description with EXACT column values and working SQL examples
7. **Run on VPS** — `scp` then execute; verify with `SELECT COUNT(*) FROM {table}`
8. **Update /country/{code}/stats if needed** — for country chapter page stat cards

---

## Data coverage gaps (open for contribution)

| Gap | What's needed | Source |
|-----|--------------|--------|
| UK tax rates (income tax bands, NI rates) | Statutory rates by year | HMRC |
| EU housing prices by country | Annual index or median price | Eurostat `prc_hpi_a` |
| EU comparative price levels | PPP-adjusted price levels by category (food, housing, transport) | Eurostat `prc_ppp_ind` |
| UK local authority spend | Per-LA spending by service | MHCLG Section 251 |
| EU PISA education scores | Reading/maths/science by country | OECD PISA |
| EU healthcare outcomes | Life expectancy, infant mortality | Eurostat `demo_mlexpec` |
| EU broadband / infrastructure | Connectivity %, speed | Eurostat DESI |

The PPP price levels and healthcare outcomes datasets are the highest-priority for the "capital efficiency index" use case.
