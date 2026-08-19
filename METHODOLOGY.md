# nstate — Methodology

Every nstate scorecard uses this framework. No exceptions. The methodology is public before any findings are published. If you believe the method is wrong, open an issue — we would rather fix the framework than defend a bad finding.

---

## Principles

1. **Policy, not narrative.** We evaluate discrete, datable policy interventions — not parties, ideologies, or politicians.
2. **Same template for everything.** Every policy gets the identical scorecard. No special treatment in either direction.
3. **Facts, estimates, and opinions are labelled differently.** A fact is a measurement from an official source. An estimate is a modelled figure with stated assumptions. An opinion is our interpretation. All three may appear in a scorecard; none should be confused for the others.
4. **Uncertainty is shown, not hidden.** Ranges, not point estimates. Confidence ratings, not false precision.
5. **"Insufficient evidence" is a valid verdict.** If the data cannot support a conclusion, we say so. We do not reach.
6. **We can exonerate.** If a programme achieves its stated objectives at reasonable cost, we say that too. Our credibility depends on it.

---

## Scorecard template

Every policy scorecard contains these sections, in this order.

### A. Policy definition
- **Name:** official policy name
- **Implementation date:** when it came into force
- **Jurisdiction:** UK-wide / England-only / devolved / mixed
- **Stated government objective:** their words, their framing
- **Target population:** who it is supposed to affect

### B. Observed data
What the official data shows after implementation. No causal claims in this section — only measurements. Time series where available. International comparisons where they exist and are methodologically valid.

### C. Counterfactual
What would likely have happened without this policy. The method used must be stated explicitly:

| Method | When to use |
|---|---|
| Direct accounting | Tax or levy explicitly line-itemised; arithmetic, not modelling |
| Before/after with controls | Discrete policy start date, control variables available |
| Difference-in-differences | Treatment vs. comparable control group |
| Synthetic control | Single treated jurisdiction, multiple valid donor units |
| Scenario / sensitivity | When causal identification is weak — clearly labelled as such |
| Descriptive only | When counterfactual cannot be credibly constructed |

All assumptions behind the counterfactual must be stated. Sensitivity analysis required for any estimate that changes materially under different assumptions.

### D. Impact dimensions

| Dimension | What to measure | Data source |
|---|---|---|
| Exchequer impact | Net receipts minus costs minus admin | HM Treasury, HMRC, OBR |
| Household impact | Annual cost or benefit per affected household | ONS, DWP, HMRC |
| GDP / productivity | Effect on economic output or productivity | ONS, OBR |
| Competitiveness | UK performance vs. comparable international peers | Eurostat, OECD, World Bank |
| Distributional | Who gains, who loses, by income decile / region / age | HMRC distributional data, ONS |
| Delivery / output | Did the stated objective get met? Metric and source | Departmental stats, NAO |
| Implementation cost | Admin, transition, legal, technology costs | Departmental annual reports, NAO |

Not every dimension will be quantifiable for every policy. Where data does not exist, say so.

### E. Evidence quality rating

- **HIGH:** Direct measurement from official administrative data. Clean attribution. Minimal estimation required.
- **MEDIUM:** Partially observable. Some estimation required. Attribution plausible but not certain.
- **LOW:** Heavily assumption-dependent. Causal identification weak. Results sensitive to methodology choices.
- **NOT MEASURABLE:** Insufficient data, policy too recent, or too many confounders to attribute.

### F. Agent benchmark (where applicable)
For administrative processes (not policy decisions), a shadow agent benchmark may be included:
- What human process currently exists, at what estimated cost
- What an open-source agent produced when run in shadow mode
- Comparison: cost, speed, accuracy, error rate
- Code repository for the agent

### G. Verdict

Three separate scores:
1. **Fiscal score:** Did it improve the public finances?
2. **Economic score:** Did it improve economic outcomes (growth, productivity, employment)?
3. **Delivery score:** Did it achieve the government's stated objective?

Separate these. A policy can score well on one and poorly on another. Do not collapse them into a single rating.

Bottom line: "This policy cost approximately £X per year, affected Y people. Its stated objective was [achieved / partially achieved / not achieved]. The evidence quality for this assessment is [HIGH / MEDIUM / LOW]."

---

## Counterfactual rules

### Always state the baseline
Every comparison requires an explicit baseline. What are we comparing to? The same policy without intervention? International peers? Pre-policy trend? The baseline must be stated before results are reported.

### Never present the counterfactual as fact
The counterfactual is always an estimate. Label it as such. Use language like "the estimated cost under a counterfactual scenario of X is approximately £Y, assuming Z."

### Separate fiscal cost from economic cost from transfer
- **Fiscal cost:** what it costs the exchequer
- **Economic cost:** what it costs the economy (including deadweight loss, distortions, second-order effects)
- **Transfer:** money that moves from one group to another without representing a net cost or gain

These are different. Collapsing them is a common error that destroys credibility.

---

## Policy inclusion criteria

A policy qualifies for a nstate scorecard when it meets all of the following:

1. It is a discrete, datable government intervention (a law, a levy, a programme, a structural change)
2. At least two independent public data sources exist for its fiscal impact
3. The stated government objective is measurable, or has been measured, within a reasonable timeframe
4. A counterfactual can be constructed at LOW evidence quality or better
5. The policy is of sufficient scale or salience to be worth the analysis effort

Policies are selected by this criteria — not by their political valence. We will score policies from all parties and ideological traditions.

---

## Data sources

All data must be from primary official sources. Secondary aggregators (Trading Economics, Statista, etc.) are not acceptable as primary citations. Use:

| Domain | Primary sources |
|---|---|
| Public spending | HM Treasury PESA, Whole of Government Accounts |
| Tax receipts | HMRC Statistics |
| GDP / productivity | ONS National Accounts |
| Public sector employment | ONS Public Sector Employment, Cabinet Office Civil Service Statistics |
| Welfare | DWP Stat-Xplore, OBR Welfare Trends |
| Education | DfE School Census, DfE Funding Statistics |
| Energy | Ofgem, DESNZ, National Grid ESO, LCCC |
| Health | NHS England, DHSC |
| Economic freedom (cross-country) | Fraser Institute Economic Freedom of the World |
| GDP per capita (historical) | Maddison Project Database |
| Cross-country social spending | OECD SOCX |
| Procurement / major projects | Contracts Finder, Find a Tender, IPA Annual Report, NAO |

Each data point in a scorecard must include: source name, URL, dataset name, data vintage (date downloaded or data date), and any transformation applied.

---

## What we will not do

- Cite secondary aggregators without tracing to the primary source
- Present correlation as causation
- Report point estimates without uncertainty ranges for modelled figures
- Classify spending as "ideological" as an analytical finding (that is an editorial judgement, clearly labelled)
- Name individual civil servants, benefit recipients, or low-level employees
- Publish a finding we have not been able to reproduce from the stated source

---

## Corrections policy

If a scorecard contains an error:

1. We correct it and publish a correction notice at the top of the scorecard
2. We document the correction in the repo commit history
3. We do not delete or suppress the original; the correction and original remain visible
4. If the error materially changes the verdict, we restate the verdict and note the revision

We welcome challenges. Open an issue, cite the evidence, and we will review it.

---

## Versioning

Each scorecard carries a version number and a data date. When new data arrives that materially changes the findings, the scorecard is updated and the change is noted. The previous version remains accessible in the git history.
