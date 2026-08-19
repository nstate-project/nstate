# SPEC: State Impact Engine

**Date:** 2026-06-26
**Status:** Draft — Phase 1 infrastructure BUILT, data loaded, scorecards in progress
**Author:** Claude Opus 4.6 + Charl
**Debates:**
- DEBATE-UK-GOVERNMENT-SPENDING-ACCOUNTABILITY.md — 4 models on UK spending accountability
- DEBATE-STATE-INTERVENTION-EVIDENCE-BASE.md — 4 models on systematic state intervention harm
**Research:** Watt-Logic (Kathryn Porter), ISC Census 2026, Oxford Economics, OBR, Eurostat
**Infrastructure:** VPS 3 (95.216.158.172), database `policy_impact`, 51 data points loaded

---

## 0. Mission & Thesis

### Mission

> **Shrink the state through transparency and evidence.**
>
> Governments grow by default. Each intervention justifies the next. Nobody systematically
> measures the damage. We build the evidence base that makes excess state intervention
> indefensible — not through ideology, but through data so clear it speaks for itself.

The objective is not academic analysis. It is to create an engine of accountability so rigorous and transparent that it shifts the Overton window toward smaller government, lower taxes, and greater individual freedom — because the evidence demands it.

### Thesis

> Less state control = better prosperity. The evidence across countries and decades shows that
> price controls, poorly designed transfers, labour-market rigidities, and discretionary industrial
> policy generate measurable distortions and consistently underperform their stated goals.

This is NOT "all government is bad." Property rights, contract law, basic infrastructure, and public health are necessary state functions. The thesis is about EXCESS intervention — the point at which government activity shifts from enabling markets to strangling them.

### The gap

The IFS does ad-hoc reports. The NAO does audits. Full Fact checks claims. The TaxPayers' Alliance advocates. Nobody runs a **systematic, queryable, continuously-updated policy impact scorecard** with transparent methodology and explicit uncertainty. We fill that gap.

---

## 1. Build Plan (phased like AvB Capital)

Start small, learn, build out — the same approach that found G3+V1+Q4 works across every equity market.

### Phase 1: UK Policy Scorecards (Month 1-2) — IN PROGRESS

**Week 1-2: Infrastructure + data pipeline — DONE**
1. `policy_impact` database on VPS 3 (95.216.158.172) — DONE
2. Schema: 5 tables (policies, data_sources, observations, scorecards, methodology_log) — DONE
3. 3 MVP policies registered — DONE
4. 51 data points loaded (education, energy, civil service) — DONE
5. Draft methodology paper (scorecard template, counterfactual rules, evidence quality criteria)

**Week 3-4: Energy + Education scorecards**
1. Automated data fetchers (Ofgem price cap, LCCC CfD payments, Eurostat prices)
2. Energy bill decomposition chart (wholesale vs policy vs network)
3. Education: VAT revenue vs state cost trajectory chart
4. Education: OBR forecast vs actual pupil migration comparison
5. Counterfactual calculations with sensitivity ranges
6. Publish both scorecards

**Week 5-6: Civil service + tax burden**
1. Cabinet Office civil service statistics (full time series)
2. Output metrics (HMRC wait times, passport processing, planning backlogs)
3. Tax-to-GDP ratio trajectory (HMRC + ONS)
4. Publish scorecards

### Phase 2: UK Welfare State Deep Dive (Month 2-3)

1. Download DWP Stat-Xplore benefit caseload data (1999-present)
2. Download OBR welfare spending trends (1948-2074 forecast)
3. Build welfare spend as % GDP time series (1948-present)
4. Map Universal Credit taper rates to effective marginal tax rates by income
5. Correlate benefit generosity with ONS economic inactivity data
6. Employer NI impact: HMRC PAYE data before/after April 2025
7. Scorecard: "The Welfare Trap" — quantified cost of dependency

### Phase 3: Cross-Country Evidence (Month 3-4)

1. Download Fraser Economic Freedom of the World (165 countries, 50 years)
2. Download Maddison Project GDP per capita (150+ countries, 200 years)
3. Build: Economic Freedom vs GDP Growth scatter (the core chart)
4. Argentina century dataset: GDP per capita vs intervention events
5. Reform event studies: NZ 1984, Estonia 1992, Ireland 1988, Chile 1975
6. Synthetic control analysis where possible
7. Report: "What Happens When Countries Reduce State Intervention"

### Phase 4: Rent Controls Evidence (Month 4-5)

1. Compile city-level evidence matrix from peer-reviewed studies
2. San Francisco, Stockholm, Berlin, New York, Barcelona
3. Housing starts, rent indices, vacancy rates, queue lengths, quality metrics
4. Report: "Every City That Tried Rent Controls" — the systematic evidence

### Phase 5: Website + Public Launch (Month 5-6)

1. Static site with scorecard pages (all policies same template)
2. Cross-country comparison tool (Fraser EFW explorer)
3. Downloadable data and methodology for every claim
4. GitHub public repo with all scripts (transparency)
5. Interactive charts (Observable notebooks or similar)
6. Methodology paper published prominently

### Phase 6: Continuous Updates + Expansion (ongoing)

1. Automated data collection crons (quarterly for most UK sources)
2. Scorecard updates when new data arrives
3. New policy additions as they occur
4. International expansion (EU policy comparisons)
5. The database becomes the evidence base that grows over time

---

## 2. The Evidence Domains

### Domain 1 — UK Policy Scorecards (Phase 1)

| Policy | Data quality | Evidence strength | Status |
|---|---|---|---|
| Net Zero Energy Levies | HIGH | HIGH (itemised in bills) | Data loaded |
| VAT on Independent Schools | HIGH | HIGH (pupil numbers measured) | Data loaded |
| Civil Service Expansion | MEDIUM | MEDIUM (output attribution hard) | Data loaded |

### Domain 2 — UK Welfare State & Labour Market (Phase 2)

| Policy | Data quality | Evidence strength | Key data source |
|---|---|---|---|
| Welfare dependency trajectory | HIGH | HIGH | DWP Stat-Xplore, OBR welfare trends |
| Welfare trap (effective marginal tax rates) | HIGH | HIGH | UC taper rates, IFS microsimulation |
| Employer NI increase impact on hiring | MEDIUM | MEDIUM (too recent) | HMRC PAYE real-time data |
| Employment Rights Bill cost | MEDIUM | MEDIUM (too recent) | BCC surveys, ONS vacancies |
| Tax burden trajectory (tax-to-GDP) | HIGH | HIGH | HMRC receipts, ONS GDP |
| Economic inactivity crisis | HIGH | MEDIUM | ONS labour market, 9M inactive |

### Domain 3 — Cross-Country Evidence (Phase 3)

| Case study | What it proves | Key data source |
|---|---|---|
| **Argentina (1900-2025)** | 100-year decline from top-10 to basket case under Peronist intervention | Maddison Project GDP per capita |
| **New Zealand (1984-2000)** | Rogernomics reforms led to GDP convergence with Australia | Fraser Economic Freedom Index |
| **Estonia (1992-2010)** | Flat tax + privatisation led to fastest post-Soviet growth | World Bank WDI |
| **Ireland (1988-2007)** | Corporate tax cut 50% to 12.5% led to Celtic Tiger | OECD tax database |
| **Chile (1975-2000)** | Market reforms led to strongest LatAm growth | Fraser EFW + Maddison |
| **Singapore vs UK** | Minimal regulation, GDP per capita overtook UK | World Bank, Fraser |
| **Hong Kong vs EU** | Economic freedom led to prosperity despite no resources | Fraser EFW |
| **Nordic paradox** | High redistribution BUT strong property rights + open trade + flexible labour | Fraser EFW (high scores on 4/5 dimensions) |

### Domain 4 — Rent Controls (Phase 4)

| City | What happened | Key evidence |
|---|---|---|
| **San Francisco** | 15% supply reduction, higher citywide rents | Diamond, McQuade, Qian (2019) AER |
| **Stockholm** | 20+ year queue for rental apartments | Swedish Housing Agency |
| **Berlin** | 25% fewer listings under Mietendeckel (struck down 2021) | DIW Berlin |
| **New York** | Chronic underinvestment, housing court backlogs | Multiple studies |
| **Barcelona** | Rent cap 2020 led to supply contraction | Idealista/Fotocasa data |

### Domain 5 — Systematic Patterns (Phase 5)

| Analysis | What it shows | Dataset |
|---|---|---|
| Fraser EFW vs GDP growth (165 countries, 50 years) | More economic freedom = more prosperity | Fraser Institute (free) |
| Government spending % GDP vs GDP growth | Diminishing/negative returns above ~25% threshold | OECD, World Bank |
| Regulation burden vs business formation | More regulation = fewer new businesses | World Bank Doing Business archive |
| Welfare spend vs economic inactivity | Correlation between benefit generosity and workforce exit | DWP + ONS |

### The risk-shifting argument (framework across all domains)

Governments don't eliminate risk — they shift it between groups while adding administrative overhead:
- **VAT on schools:** Shifted cost from parents (voluntary) to taxpayers (involuntary)
- **Energy levies:** Shifted cost of decarbonisation from investors to bill-payers
- **Rent controls:** Shifted cost from tenants to landlords, landlords exit, tenants worse off
- **Welfare expansion:** Shifted cost from individuals to taxpayers, created dependency trap
- **Employer NI:** Shifted cost from government to employers, employers cut hiring

Each intervention creates new distortions and unintended consequences. The database documents these systematically.

---

## 3. Scorecard Template

Every policy gets the same template. This is how we maintain credibility.

### A. Policy Definition
- **Name:** [official name]
- **Implementation date:** [when it started]
- **Jurisdiction:** UK-wide / England-only / devolved
- **Stated government objective:** [in their words]
- **Target population:** [who it affects]

### B. Observed Data (facts only, no causal claims)
- What changed in official data after implementation
- Time series: before vs after
- International comparison where relevant

### C. Counterfactual Estimate
- What would likely have happened without this policy
- Method used: accounting / diff-in-diff / synthetic control / scenario
- Key assumptions stated explicitly
- Sensitivity range (best case / central / worst case)

### D. Impact Dimensions

| Dimension | Metric | Value | Confidence |
|---|---|---|---|
| **Exchequer impact** | Net receipts - costs - admin | Xm/year | H/M/L |
| **Household impact** | Cost per household/year | X/year | H/M/L |
| **GDP/productivity** | Effect on growth | X% | H/M/L |
| **Industrial competitiveness** | UK vs international comparison | X vs Y | H/M/L |
| **Distributional** | Who gains, who loses | Description | H/M/L |
| **Delivery/output** | Did the stated objective get met? | Yes/No/Partial | H/M/L |
| **Implementation cost** | Admin, transition, setup | Xm | H/M/L |

### E. Evidence Quality Rating
- **HIGH:** Direct measurement from official statistics, clean attribution
- **MEDIUM:** Partially observable, some estimation required
- **LOW:** Heavily assumption-dependent, weak causal identification
- **NOT MEASURABLE:** Insufficient data or too early to assess

### F. Bottom Line
- Separate: fiscal score, economic score, welfare score
- State what is known, what is estimated, what is unknown
- "This policy cost the Exchequer Xm and households Y/year. The stated objective was [partially/fully/not] achieved."

---

## 4. Counterfactual Framework

### Method hierarchy (use the strongest available):

| Method | When to use | Example |
|---|---|---|
| **Direct accounting** | Tax/levy that's itemised in bills | Energy: remove levies from bills |
| **Before/after with controls** | Discrete policy with clean start date | School VAT: pupil numbers before/after Jan 2025 |
| **Difference-in-differences** | Treatment vs control group exists | UK energy prices vs comparable countries |
| **Synthetic control** | One treated unit, multiple controls | UK industrial competitiveness vs EU peers |
| **Scenario modelling** | When ID is weak | Civil service: what output would fewer staff deliver? |
| **Not attributable** | Too many confounders | "Net zero caused inflation" — too broad |

### For each MVP policy:

**Energy:** Direct accounting (levies are itemised) + diff-in-diff (UK vs EU prices). Evidence quality: HIGH.

**School VAT:** Before/after with controls (pupil migration data) + accounting (VAT revenue vs state education cost). Evidence quality: HIGH.

**Civil service:** Descriptive (headcount trends) + output metrics where available. Evidence quality: MEDIUM.

---

## 5. MVP Policy Detail: Energy — Net Zero Costs on Bills

The net zero costs are NOT hidden in global gas prices. They are **explicitly line-itemised** in energy bills as environmental levies, CfD payments, capacity market charges, and constraint costs. Watt-Logic (Kathryn Porter, physicist + energy consultant) has already decomposed these.

**Hard numbers:**

| Metric | Value | Source |
|---|---|---|
| Environmental levies on bills (2023-24) | 17.2 billion/year | Watt-Logic / Ofgem |
| Projected levies (2029-30) | 20+ billion/year | Watt-Logic |
| Policy costs as % of bill | 14% (after reclassifying CfDs to policy) | Watt-Logic |
| Counterfactual saving since 2006 | 218 billion (2025 money) | Watt-Logic |
| Constraint costs (paying wind NOT to generate) | 2.3 billion (2024-25) | National Grid ESO |
| Capacity Market cost | 1.3bn now, 4bn by 2030 | Watt-Logic |
| UK industrial electricity vs EU | 27.91 vs 10.80 p/kWh (2.6x) | Eurostat June 2024 |
| UK electricity prices vs EU average | 23% above | H1 2025 |
| UK gas prices vs EU average | 28% below | H1 2025 |

**The counterfactual is arithmetic, not modelling:** Had the UK stuck with gas generation since 2006, consumers would be 218 billion better off in 2025 money, even including the gas crisis.

**Bill breakdown (post-reclassification):**
- Wholesale energy: ~42%
- Network costs: ~24%
- Policy costs: ~14%
- Operating costs: ~10%
- VAT: ~5%
- Supplier margin: ~5%

**Policy cost components:** CfD subsidies, Renewables Obligation, Capacity Market, Feed-in Tariffs, Warm Homes Discount, Green Gas Levy, constraint payments (paying wind farms to switch off).

**Data sources:** Ofgem Price Cap model (quarterly), LCCC CfD payments (monthly), National Grid ESO constraints (daily/monthly), Elexon/BMRS wholesale prices (real-time), DESNZ energy statistics (quarterly), Eurostat international comparisons (biannual), OBR policy costings (per fiscal event).

**Scorecard summary:** 17.2bn/year in levies, ~220/household/year, UK 2.6x EU industrial prices, 218bn cumulative cost since 2006. Evidence quality: HIGH.

---

## 6. MVP Policy Detail: VAT on Independent School Education

**Implementation:** January 2025 (20% VAT on independent school fees)

**The fundamental fiscal argument: independent schools SAVE the government money.** Independent schools educate ~530,000 pupils (pre-VAT) at NO cost to the taxpayer. Oxford Economics calculated this saves the exchequer **4.4 billion per year** (2022). Every pupil that leaves independent for state costs the government 8,580/year (DfE 2026-27).

The policy taxes parents who are SAVING the government money, driving them into a system that COSTS the government money. Net negative by design.

**The case for subsidies (not taxes):** Subsidise means-tested independent places for ~2bn/year, net saving 2.4bn/year + better outcomes + reduced state school pressure.

**The exodus (ISC Census 2026 + latest data):**

| Metric | Value | Source |
|---|---|---|
| Pupils lost since VAT (total) | 43,000 | ISC / latest data |
| ISC Census 2026 drop | 20,000 in one year (-3.5%) | ISC Census 2026 |
| New pupil intake | -5.6% | ISC Census 2026 |
| Boarding pupils | -8.2% | ISC Census 2026 |
| International pupils | -4.7% | ISC Census 2026 |
| Primary/prep | -5.0% | ISC Census 2026 |
| Year 12 sixth form entry | -6.6% (biggest drop) | ISC Census 2026 |

**The OBR got it wrong:** Forecast 35,000 pupils leaving (steady state, several years). Actual: 43,000 in ~18 months — already exceeded.

**Crossover point:** At ~175,000 pupils lost (33% of sector), state cost EQUALS VAT revenue. Policy becomes net negative.

**Data sources:** ISC Census (annual), DfE School Census (annual), DfE Funding Statistics, HMRC VAT statistics, OBR Policy Costings, Oxford Economics, IFS, House of Commons Library (CBP-10125).

**Evidence quality:** HIGH.

---

## 7. MVP Policy Detail: Civil Service Expansion

**Key numbers:** 418,000 (2016, post-austerity low) to 513,000 (2024) = +23%, +95,000 staff. 300+ public bodies (quangos).

**The question:** What did we get for the extra ~95,000 staff?

**Honest complexity:** Must separate civil servants from NHS/teachers/police. Machinery of government changes break time series. Some growth was Brexit-related, some COVID. Need OUTPUT metrics alongside INPUT (headcount).

**Data sources:** Cabinet Office Civil Service Statistics (annual), ONS Public Sector Employment (quarterly), Cabinet Office Public Bodies Register, NAO reports, departmental annual reports.

**Evidence quality:** MEDIUM.

---

## 8. Credibility & Bias Rules

### Rules (from 4-model debate consensus):

1. **Evaluate discrete policies, not ideological narratives** — "Environmental levies in energy bills" not "Net zero is destroying Britain"
2. **Same template for every policy** — no special treatment
3. **Score policies from BOTH sides** — include policies where evidence shows positive impact (furlough, auto-enrolment pensions)
4. **Pre-publish methodology** before publishing conclusions
5. **Separate facts from estimates from opinions** — opinions NOT included in scorecards
6. **Allow "insufficient evidence"** as a valid outcome
7. **Show ranges, not point estimates**
8. **Published inclusion criteria** for which policies get scored

### The name matters:
- NOT: "Government Waste Tracker" (advocacy)
- CONSIDER: "State Impact Engine" / "PolicyCheck" / "FiscalWatch"
- Should sound like the IFS, not the TaxPayers' Alliance

### Selection criteria for policy inclusion:
1. Discrete, datable policy intervention
2. At least 2 public data sources for fiscal impact
3. Measurable outcome within 2 years
4. Counterfactual is constructible
5. Politically salient enough that people care

---

## 9. Existing Landscape

| Organisation | Strength | Weakness | What we take |
|---|---|---|---|
| **IFS** | Methodological gold standard | Ad-hoc reports, not always-on | Rigour, assumption transparency |
| **NAO** | Evaluation discipline, VFM | Only covers audited departments | Output metrics alongside input costs |
| **OBR** | Forecast logic, baseline discipline | Doesn't evaluate retrospectively | Forecast vs actual comparison |
| **Full Fact** | Trust, sourcing, communication | Checks claims, no impact analysis | Plain-English, source-linked |
| **TaxPayers' Alliance** | Shows demand for scrutiny | Perceived as partisan | What NOT to do |
| **Watt-Logic** | Deep energy cost decomposition | Energy only | Bill breakdown methodology |
| **Institute for Government** | Implementation insight | Descriptive, not evaluative | Civil service output metrics |

**Our gap:** Official datasets + reproducible methods + policy-by-policy scorecards + public queryability + explicit uncertainty + cross-country patterns — in one always-on system, with a clear mission to shrink the state.

---

## 10. Infrastructure & Technology

### Where it runs
VPS 3 (95.216.158.172) — same box as Business Alpha, separate database. Cost: included in 8.49/mo.

### Tech stack

| Component | Technology |
|---|---|
| Database | PostgreSQL 18, database `policy_impact` |
| Data collection | Python scripts (requests, pandas, openpyxl) |
| Analysis | Python (pandas, numpy, scipy) |
| Visualisation | Observable notebooks or static site |
| Methodology docs | Markdown / PDF |
| Code | GitHub public repo (transparency) |
| LLM usage | Minimal — PDF extraction and summaries only, NOT for analysis |

### Schema (BUILT)

5 tables: `pie_policies`, `pie_data_sources`, `pie_observations`, `pie_scorecards`, `pie_methodology_log`. See database for full schema.

### Data collection crons (to build)

| Cron | Frequency | Source | What it fetches |
|---|---|---|---|
| `fetch_ofgem_price_cap.py` | Quarterly | Ofgem | Bill breakdown, levy rates |
| `fetch_lccc_cfd.py` | Monthly | LCCC | CfD payments by technology |
| `fetch_ngeso_constraints.py` | Monthly | National Grid ESO | Constraint costs |
| `fetch_eurostat_energy.py` | Biannual | Eurostat | International price comparisons |
| `fetch_hmrc_receipts.py` | Monthly | HMRC | Tax receipts by category |
| `fetch_ons_employment.py` | Quarterly | ONS | Public sector employment |
| `fetch_dfe_census.py` | Annual | DfE | School pupil numbers |
| `fetch_obr_forecasts.py` | Per fiscal event | OBR | Policy costings, forecasts |
| `fetch_fraser_efw.py` | Annual | Fraser Institute | Economic Freedom Index |
| `fetch_dwp_statxplore.py` | Quarterly | DWP | Benefit caseloads |

### Key datasets (all free/public)

| Dataset | Source | Coverage |
|---|---|---|
| Fraser Economic Freedom of the World | fraserinstitute.org | 165 countries, 1970-2024 |
| Maddison Project GDP per capita | Groningen University | 150+ countries, 1820-2023 |
| OECD Social Expenditure (SOCX) | OECD.Stat | 38 countries, 1980-2023 |
| World Bank Doing Business (archived) | World Bank | 190 economies, 2003-2020 |
| DWP Stat-Xplore | DWP | UK benefit caseloads, 1999-present |
| ONS Labour Market | ONS | UK employment/inactivity, 1971-present |
| HM Treasury PESA | gov.uk | UK public spending breakdown |
| HMRC Tax Receipts | gov.uk | UK tax receipts by type, monthly |
| OBR Welfare Trends | OBR | UK welfare spending 1948-2074 |
| Penn World Tables | Groningen | 183 countries, 1950-2019 |

---

## 11. Legal Considerations

**Low risk overall.** All data sources public, mostly under Open Government Licence. Analysis protected as commentary under UK law. Watt-Logic has published critical energy policy analysis since 2016 without legal issues.

**Checks needed:** OGL compliance for derived datasets. Avoid implying personal corruption of named politicians. If influential near elections, check Electoral Commission rules on regulated campaigning. Consider legal structure: nonprofit/CIC for credibility.

---

## 12. Risks & Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| **Dismissed as partisan** | HIGH | Same template for all policies. Include positive-impact policies. Methodology-first. |
| **Counterfactual contested** | HIGH | Show ranges, state assumptions, label evidence quality. |
| **Data gaps** | MEDIUM | Flag gaps explicitly. "Insufficient evidence" is a valid finding. |
| **Selection bias in policies** | MEDIUM | Published inclusion criteria. Score policies from both sides. |
| **Government pushback** | LOW | All public data. Protected commentary. Legal review before launch. |
| **Scope creep** | MEDIUM | 3 policies for MVP. Strict inclusion criteria for additions. |
| **False precision** | HIGH | Always show ranges. Never present estimates as facts. |
| **Nordic paradox** | MEDIUM | Address head-on: high redistribution + strong property rights + open trade. Not a counter-example when decomposed. |
| **Reverse causality** | MEDIUM | Weak economies cause intervention, not just the reverse. Use causal methods where possible. |

---

## 13. Open Questions

1. **Product name** — "State Impact Engine" / "PolicyCheck" / "FiscalWatch"?
2. **Legal structure** — CIC / nonprofit / personal project?
3. **Advisory board** — economists from different leanings to review methodology?
4. **Watt-Logic engagement** — collaborate or cite?
5. **Target audience** — journalists? voters? MPs? think tanks? all of the above?
6. **Funding model** — donations? grants? pro bono?
7. **IFS/NAO peer review** before launch?
8. **Timing** — political moment for maximum impact?
9. **Should cross-country evidence (Phase 3) be a separate product** or integrated?

---

## 14. What Success Looks Like

**Month 1:** Energy + education scorecards published. Journalists cite: "Environmental levies cost UK households 220/year" and "43,000 pupils forced into state education costing 369m/year."

**Month 3:** 5+ policies scored. Welfare trap quantified. Template established.

**Month 6:** Cross-country evidence published. Fraser EFW scatter chart shows the pattern across 165 countries. Argentina case study live. Rent controls evidence compiled.

**Year 1:** 15+ policies scored. Continuous updates. Cross-country database. Cited by journalists, MPs, and think tanks. Track record of rigorous, transparent analysis.

**The north star:** When a government proposes a new intervention, people check the State Impact Engine first — and the data consistently shows that less state control delivers better outcomes.

### Additional UK Policy Candidates (as data allows):

| Policy | Data quality | Attribution | Salience |
|---|---|---|---|
| HS2 cost escalation | HIGH | MEDIUM | HIGH |
| COVID spending waste (PPE, Test & Trace) | HIGH | LOW | HIGH |
| Immigration fiscal impact | MEDIUM | HIGH | VERY HIGH |
| NHS spending vs outcomes | MEDIUM | HIGH | HIGH |
| Housing benefit cost trajectory | HIGH | MEDIUM | MEDIUM |
| Green Belt restrictions on housing supply | LOW | HIGH | MEDIUM |
