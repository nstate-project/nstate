# Debate - 2026-06-26 12:03

**Question:** UK GOVERNMENT SPENDING ACCOUNTABILITY ENGINE — using public data to fact-check whether government spending decisions are net positive or net negative for the country. The thesis: most UK government decisions are driven by ideology, not evidence. We want to build a system that quantifies the ACTUAL impact of policy decisions using publicly available data. Examples: 1) VAT on independent schools — forced families into state education, so government now pays more per pupil. What's the net fiscal impact? Data exists: HMRC VAT receipts, DfE pupil numbers, per-pupil state funding costs. 2) Net zero energy policy — Ed Miliband's agenda pushing up energy costs, which cascade into ALL costs (manufacturing, food, transport). Data exists: Ofgem price caps, ONS CPI components, BEIS energy statistics. 3) Civil service expansion — number of civil servants has exploded with quangos. Data exists: ONS public sector employment, Cabinet Office headcounts, quango spend reports. 4) Tax burden at all time high — UK tax-to-GDP ratio highest since post-WW2. Data exists: HMRC receipts, OBR forecasts, ONS GDP. Questions to debate: 1) What public UK government data sources are available (APIs, datasets, FOI)? 2) How would we structure a 'policy impact scorecard' that quantifies net fiscal impact? 3) What metrics matter — tax receipts vs spending vs debt vs GDP growth vs productivity vs cost of living? 4) How do we avoid political bias and stick to facts/numbers? 5) What's the MVP — a website? a report? a dataset people can query? 6) Legal considerations — is this just using public data or are there risks? 7) How do we handle the counterfactual problem (what would have happened WITHOUT the policy)? 8) Who has done this before — IFS, TaxPayers Alliance, Full Fact — and what can we learn?

## Research Context (Tavily)

### Tavily (AI search)
Summary: UK government spending increased significantly in the 2020s, with health and social protection as top expenditures. Spending decisions often lack public trust, raising questions about their net impact. Evidence-based assessments are crucial for accountability.
- [Full Fact Report 2026 – Full Fact](https://fullfact.org/policy/reports/full-fact-report-2026): Full Fact’s polling of UK adults points to the lack of a single actor that commands widespread public trust to provide accurate and reliable information.[[39]](https://fullfact.org/policy/reports/full-fact-report-2026#ftnt39) Of the institutions people were asked about, government department website
- [United Kingdom Government Spending - Trading Economics](https://tradingeconomics.com/united-kingdom/government-spending): Government Spending in the United Kingdom increased to 149462 GBP Million in the first quarter of 2026 from 148909 GBP Million in the fourth quarter of 2025
- [UK government spending 2026| Statista](https://www.statista.com/statistics/298465/government-spending-uk): As your partner for data-driven success, we combine expertise in research, strategy, and marketing communications. Strategy and business building for the data-driven economy. See why Statista is the trusted choice for reliable data and insights. ## Total managed expenditure of the government of the 
- [What does the government spend money on? | Institute for Fiscal Studies](https://ifs.org.uk/taxlab/taxlab-key-questions/what-does-government-spend-money): *   [Health spending is growing](https://ifs.org.uk/taxlab/taxlab-key-questions/what-does-government-spend-money#toc-id-2). It is the monetary value of all market production in a particular area (usually a country) in a given period (usually a year).[Read more](https://ifs.org.uk/taxlab/glossary#gro
- [Public spending statistics: February 2026 - GOV.UK](https://www.gov.uk/government/statistics/public-spending-statistics-release-february-2026/public-spending-statistics-february-2026): ## Cookies on GOV.UK. We’d like to set additional cookies to understand how you use GOV.UK, remember your settings and improve government services. # Public spending statistics: February 2026. This publication is available at https://www.gov.uk/government/statistics/public-spending-statistics-releas

### Serper (Google SERP)
- [What does the government spend money on?](https://ifs.org.uk/taxlab/taxlab-key-questions/what-does-government-spend-money): In 2022–23, UK government spending was almost £1,200 billion, or around £17,000 per person. This was equivalent to around 45% of GDPGross domestic product (GDP)
- [The UK government's making huge spending decisions ... - YouTube](https://www.youtube.com/watch?v=dIbYv8CpW8Y): We're looking at what's going on in the Treasury as the final decisions are being made ahead of the government's Spending Review on ...
- [[PDF] Evaluating government spending - National Audit Office](https://www.nao.org.uk/wp-content/uploads/2021/12/Evaluating-government-spending.pdf): Our report considers the provision and use of evaluation evidence in policy-making in the core government departments. government evaluations ...
- [(Why) Is Misinformation a Problem? - PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC10623619/): We examined different disciplines (computer science, economics, history, information science, journalism, law, media, politics, philosophy, psychology, ...
- [Government spending areas: perception vs reality - YouGov](https://yougov.com/en-gb/articles/53415-government-spending-areas-perception-vs-reality): The results suggest that spending on interest on government debt, public order and safety, and overseas aid are overestimated, while spending on ...

---

## Gemini's Response

### Answer
The ultimate UK Government Spending Accountability Engine must be built as an **open-source, interactive causal inference platform** (a dynamic "simulation engine" rather than a static reporting site). Because isolating policy impacts from global macro shocks is highly complex, the engine must allow users to adjust behavioral assumptions and elasticity parameters transparently, using standard econometric models (like Synthetic Control methods) to prevent accusations of partisan bias.

---

### Reasoning

*   **FACT**: Highly detailed and historic UK public sector financial data is scattered across multiple statutory bodies, including the Office for National Statistics (ONS) for employment and CPI, HM Revenue and Customs (HMRC) for tax receipts, the Office for Budget Responsibility (OBR) for economic forecasts, and HM Treasury for departmental spending allocations [[Trading Economics, IFS, NAO, GOV.UK]].
*   **FACT**: The UK National Audit Office (NAO) has explicitly reported that government evaluation of the actual effectiveness of spending policies is staggeringly weak and inconsistent, with many departments failing to conduct robust, post-implementation, evidence-based evaluations of major policy initiatives [[National Audit Office Report, 2021]].
*   **INFERENCE**: Because major macroeconomic shifts (such as global supply chain shocks or energy price volatility) happen concurrently with domestic policy changes, any fixed "net fiscal impact" figure produced by a black-box model will be easily discredited as politically biased unless the underlying econometric assumptions (such as price elasticity of demand or substitution effects) are fully exposed and customizable by the user. 
*   **OPINION**: The thesis that ideological posturing routinely overrides objective data-driven policymaking in Whitehall is highly accurate; however, a platform that claims to find a single, definitive "truth" will be instantly weaponized or dismissed by the opposing political faction. The only way to gain systemic authority and public trust is to act as the "calculator" rather than the "arbiter," allowing the data and transparent formulas to speak for themselves.

---

### Trade-offs

*   **Dynamic Customization vs. User Accessibility**: Giving users the power to alter modeling variables (e.g., dynamic tax-behavior elasticities for the VAT on private schools) makes the tool highly credible to economists and journalists, but risks alienating the general public, who prefer simple, definitive, "bumper-sticker" numbers.
*   **Methodological Rigor vs. Real-Time Tracking**: Establishing absolute causal proof of a policy's impact requires lag-heavy datasets (often published annually or bi-annually by the ONS/HMRC). Opting for real-time tracking means using imperfect proxy data (such as high-frequency sentiment polls or immediate market spot prices), which significantly degrades the scientific credibility of your "net fiscal impact" score.
*   **Bipartisan Reach vs. Viral Engagement**: Highly polarized, direct-attribute headlines (e.g., *"Ed Miliband's Energy Policy Cost Your Household £1,400 This Year"*) generate massive social media traffic and donor interest. However, sticking to academically defensible, range-bound numbers (e.g., *"Net fiscal impact is likely between -£150m and +£50m depending on gas price baselines"*) will limit early viral growth in favor of long-term institutional authority.

---

### What I Don't Know

*   The exact lag-times and API health of the Department for Education’s (DfE) pupil census databases, making it difficult to know if we can track state-school migration patterns in real-time or if we must rely on annual publishing cycles.
*   The terms of service and commercial scraping limitations of energy-sector market databases (such as Elexon or National Grid ESO data hubs) required to bypass incomplete, aggregated government-reported energy statistics.
*   The willingness of the Cabinet Office and Treasury to release granular internal business cases via FOI without hiding behind Section 35 (formulation of government policy) exemptions.

---

### Action Items

*   **Pipeline Setup**: Build robust, automated data scraping pipelines targeting the ONS API, OBR forecast databases, HMRC annual receipts reports, and sector-specific portals (such as Ofgem price cap announcements and the DfE School Census).
*   **Build the "Private School VAT" MVP**: Develop one highly focused, single-issue interactive calculator. Map HMRC VAT intake against DfE state pupil intake changes and local authority per-pupil funding allocations (using standard £7,600+ per-pupil state cost baselines) to establish the net fiscal balance sheet of this specific policy.
*   **Codify the Counterfactual Framework**: Implement standardized open-source econometric libraries (e.g., using Python's `DoWhy` or structural causal models) to construct synthetic historical controls (how the UK economy or sector would have performed without the policy in question).
*   **Establish a Red-Team Advisory Council**: Form an advisory board comprising economists from contrasting ideological leanings (e.g., featuring former IFS or OBR analysts alongside market-focused or public-sector-oriented academics) to audit the platform's formulas before the public code launch.

---

### Risks & Blind Spots

*   **The Confounding Variable Trap (Causation vs. Correlation)**: You run a high risk of attributing broader, global macroeconomic trends to highly localized UK政策. For example, if you blame Ed Miliband's energy strategy for a sudden surge in food production costs, but the underlying driver was actually global fertilizer shortages or international shipping disruptions, the engine’s credibility will be permanently damaged.
*   **Laffer Curve Assumptions**: Models evaluating tax changes are highly sensitive to dynamic behavioral assumptions (how people change behavior when taxed). If your engine hardcodes high or low elasticity of taxpayer migration, the engine will immediately be classified as a partisan tool (libertarian or socialist) by partisan actors.
*   **Goodhart’s Law**: Once policymakers realize their metrics are being aggregated and targeted by an open-access "Accountability Engine," civil servants may alter how they classify and report raw data (e.g., renaming "civil servants" to "outsource contractors" to artificially suppress headcount data in official statistics), rendering historical comparisons inaccurate.

---

## GPT's Response

1. **Answer**:  
Build this as a **transparent policy-evaluation platform**, not a partisan “gotcha engine”: start with **3–5 narrow, high-salience policies** and publish a **replicable scorecard** that separates **observed facts**, **estimated causal effects**, and **value judgements**. The right MVP is a **public website + downloadable methodology + queryable dataset**, with every claim traceable to UK public sources and every counterfactual clearly labeled as an estimate rather than a fact.

2. **Reasoning**:
- **FACT**: The UK already has substantial public spending data and official statistics suitable for a first version. HM Treasury publishes public spending statistics; IFS summarizes UK government spending levels and composition; ONS, HMRC, DfE, Ofgem, DESNZ/BEIS, OBR, and Cabinet Office all publish relevant datasets. The IFS notes UK government spending in 2022–23 was almost **£1.2 trillion**, around **45% of GDP**; HM Treasury publishes the *Public spending statistics* release; Trading Economics reports UK government spending at **149,462 GBP million in Q1 2026** based on official data. Sources: IFS “What does the government spend money on?”, GOV.UK *Public spending statistics: February 2026*, Trading Economics UK government spending series.  
- **FACT**: There is a real accountability gap around how government decisions are assessed and communicated. Full Fact reports low public trust in a single reliable actor for accurate information, which supports the case for a transparent, evidence-led accountability product. Source: Full Fact Report 2026.  
- **FACT + INFERENCE**: The National Audit Office has explicitly highlighted weaknesses in evaluation evidence in government decision-making. That means a system focused on evaluation quality, causal identification, and reproducibility would address a genuine institutional need rather than just a political messaging opportunity. Source: NAO, *Evaluating government spending* (2021).  
- **INFERENCE**: Your strongest differentiator is **not** “proving ideology drives policy” — that thesis is too broad and hard to evidence cleanly — but building a framework that quantifies **fiscal**, **economic**, and **distributional** effects policy-by-policy. If you lead with a pre-committed political conclusion, you will lose credibility and likely reproduce the same trust problem you want to solve.  
- **OPINION**: The right architecture is a **scorecard with multiple lenses**, not a single “net positive/net negative” number. A one-number verdict is seductive but often misleading because fiscal impact, GDP impact, household welfare, productivity, and long-run environmental or health effects can point in different directions.

3. **Trade-offs**:
- A rigorous system will be **slower and less headline-friendly** than political commentary.  
- Public data is often **lagged, revised, incomplete, or aggregated**, which limits precision.  
- Counterfactual estimates will always be contestable; critics will attack assumptions, not just outputs.  
- Some policies have **long-run effects** that are not visible in short-run fiscal data.  
- A multi-metric scorecard is more honest, but less media-friendly than a simple “this policy cost X” claim.

4. **What I don't know**:
- I do **not** know your intended audience: media, voters, MPs, think tanks, campaigners, or investors. That changes the product design.  
- I do **not** know whether you want a **neutral public-interest tool** or an advocacy vehicle with a policy stance. That affects trust, governance, and legal/comms risk.  
- I do **not** know the exact availability and granularity of some specific datasets you’ll need for each case study, especially for quasi-experimental identification.  
- I do **not** know whether you have data science / econometrics capability in-house; that determines whether causal claims are realistic in the MVP.  
- I do **not** know whether you plan to cover **UK-wide** policy only or devolved governments too; that materially complicates attribution.

5. **Action items**:
- **Define the unit of analysis**: evaluate **individual policy changes** (e.g. VAT on private schools, energy levies, civil service expansion) rather than broad ideological agendas.  
- **Build a source map**: catalog datasets from HM Treasury, ONS, HMRC, OBR, DfE, Ofgem, DESNZ, Cabinet Office, Companies House, NAO, ONS Secure Research Service where relevant, plus FOI routes for missing operational data.  
- **Design the scorecard** with separate sections for:  
  1) direct fiscal effect,  
  2) macroeconomic effect,  
  3) household cost-of-living effect,  
  4) distributional effect,  
  5) implementation/administrative cost,  
  6) confidence level / evidence quality.  
- **Pilot 3 case studies** where data is comparatively strong:  
  1) VAT on independent schools,  
  2) civil service headcount growth,  
  3) tax burden / receipts vs GDP.  
  I would leave “net zero” as a later phase because attribution is much harder and more politically combustible.  
- **Publish a methods paper** before launching headline conclusions, including causal strategy, assumptions, confidence bands, and rules for handling uncertainty.

6. **Risks & blind spots**:
- **Counterfactual fragility**: The biggest risk is overstating causality from observational public data. Example: if private-school enrolment falls, isolating how much is due to VAT versus demographics, income shocks, or school fee inflation is difficult.  
- **Metric gaming**: If you optimise for fiscal effects alone, you may wrongly label socially beneficial policies “negative.” For example, some spending raises long-run productivity or health outcomes but worsens near-term borrowing.  
- **Selection bias**: If you only pick policies associated with one party or ideology, the platform will look like advocacy dressed up as data.  
- **False precision**: Publishing single-number impacts without ranges, assumptions, and sensitivity analysis will undermine credibility.  
- **Public trust risk**: Full Fact’s findings imply the environment is already trust-poor. If your methodology is not maximally transparent, you will be seen as another partisan actor.  
- **Legal/comms risk**: Using public data is usually low-risk, but defamatory or misleading claims about named politicians, or misuse of licensed datasets, can create exposure. Check Crown copyright / Open Government Licence terms, API terms, and any restrictions on republishing derived datasets.  
- **Institutional blind spot**: The thesis “most decisions are ideology-driven” may be true in some cases, but you likely cannot prove that from spending data alone. You can prove **whether outcomes matched stated objectives**, which is stronger and more defensible.

---

## More specific recommendations on your 8 questions

### 1) What public UK government data sources are available?
**FACT**: The core public sources are:
- **HM Treasury**: Public spending statistics, PESA, spending reviews, Whole of Government Accounts  
- **ONS**: GDP, productivity, inflation, labour market, public sector employment, public finances  
- **OBR**: forecasts, economic and fiscal outlooks, policy costings where available  
- **HMRC**: tax receipts, tax expenditures, VAT statistics, distributional tax data  
- **DfE**: school census, pupil numbers, school finances, per-pupil funding  
- **Ofgem**: price cap data and retail energy market indicators  
- **DESNZ/BEIS**: energy generation, consumption, prices, policy publications  
- **Cabinet Office / CSHR / GOV.UK**: civil service statistics, public body reviews  
- **NAO**: value-for-money reports and evaluation critiques  
- **Parliament / House of Commons Library**: policy briefings and background analysis  
- **FOI**: useful for implementation costs, internal guidance, contract values, and unpublished management information, though response quality varies.

**INFERENCE**: You should maintain a **data registry** with fields: source owner, frequency, geography, lag, revisions policy, licensing, and whether it supports causal inference or only descriptive analysis.

### 2) How should the policy impact scorecard work?
My recommendation:

**Policy Scorecard Template**
1. **Policy definition**  
   Exact measure, implementation date, target population, intended goal  
2. **Observed facts**  
   What happened in the data after implementation  
3. **Counterfactual estimate**  
   What likely would have happened otherwise  
4. **Impact dimensions**  
   - Direct fiscal impact  
   - Administrative cost  
   - Household impact  
   - Business impact  
   - GDP/productivity effect  
   - Distributional effect  
   - Environmental/social effect if relevant  
5. **Confidence rating**  
   High / Medium / Low based on evidence quality  
6. **Bottom-line verdict**  
   Not one number only — use a dashboard with weighted views

**OPINION**: If you insist on a single headline score, make it a **composite with visible sub-scores** and allow users to change weights.

### 3) What metrics matter?
Use 3 tiers:

**Tier 1: Core required metrics**
- Net Exchequer effect: receipts minus spending minus admin cost  
- Public borrowing / debt impact  
- GDP / GVA effect  
- Productivity effect  
- CPI / household cost-of-living effect

**Tier 2: Distributional metrics**
- Income decile impact  
- Regional impact  
- Sector impact  
- Intergenerational impact

**Tier 3: Policy-specific metrics**
- Education: pupil movement, attainment, local authority capacity  
- Energy: wholesale/retail pass-through, industrial competitiveness, fuel poverty  
- Civil service: output per FTE, service delivery times, regulatory load

**INFERENCE**: For credibility, distinguish **fiscal score** from **national welfare score**. They are not the same thing.

### 4) How do you avoid political bias?
- Pre-register methodology before seeing results where possible  
- Use the same template across left/right policies  
- Publish all assumptions and sensitivity ranges  
- Separate facts from estimates from value judgements  
- Have an external advisory board with mixed viewpoints  
- Include policies that may cut both ways politically

**OPINION**: If you cannot commit to evaluating policies from multiple parties and ideological camps, don’t market it as neutral.

### 5) What’s the MVP?
**Best MVP**:  
A **website** with:
- 3 flagship policy pages  
- downloadable methodology PDF  
- linked datasets / notebooks  
- charts and scorecards  
- “evidence quality” labels

**Why not start with a report only?**  
A report gets attention, but a website creates a reusable accountability engine.

### 6) Legal considerations
**FACT**: Much UK government data is available under the **Open Government Licence**, but not all datasets or APIs are unrestricted; third-party rights and terms can apply.  
**INFERENCE**: Main legal issues are less about using public data and more about:
- licence compliance  
- reproducing non-OGL content  
- defamation risk in attributing motives or misconduct  
- data protection if combining microdata  
- inaccurate financial claims presented as fact

Get a media/data lawyer to review publication standards if you plan to make adversarial claims.

### 7) How do you handle the counterfactual problem?
Use a hierarchy:
1. **Natural experiments / difference-in-differences** where possible  
2. **Synthetic controls** for region/time comparisons  
3. **Pre/post with control variables** if better methods unavailable  
4. **Scenario modelling** when causal identification is weak

And always label which level you are using.

**OPINION**: Do not claim causal certainty where only descriptive correlation exists. That would destroy the project.

### 8) Who has done this before, and what can you learn?
- **IFS**: strongest on tax/spend clarity and methodological seriousness  
- **NAO**: strongest on evaluation discipline and value-for-money framing  
- **Full Fact**: strongest lesson on trust, sourcing, and communication clarity  
- **TaxPayers’ Alliance**: shows there is demand for spending scrutiny, but also demonstrates how easy it is to be dismissed as partisan if methods are not robust  
- **House of Commons Library / OBR**: useful model for factual restraint and transparent caveats

**INFERENCE**: Your white space is combining **public-data infrastructure + causal evaluation + plain-English scorecards** in one place.

## Bottom line
My recommendation is to **do this**, but only if you are willing to be **more rigorous than ideological**. The winning product is not “proof that politicians are wrong”; it is a **credible evidence system** that lets anyone inspect whether a policy achieved its stated aims, at what cost, and with what degree of confidence.

---

## Claude's Response

# UK Government Spending Accountability Engine — Expert Assessment

---

## 1. Answer

This is a viable, high-value project that can be built with publicly available data — the technical and legal barriers are low, but the **counterfactual problem and confirmation bias risk are the two existential threats** that will determine whether this becomes a credible accountability tool or just another ideologically-dressed think-tank. Build the MVP as a **queryable dataset with a methodology-first public documentation layer**, not a website with conclusions — let the numbers speak and let critics attack the methodology, not the framing.

---

## 2. Reasoning

- **FACT**: The UK government publishes extensive machine-readable spending data. Sources include: HMRC tax receipts (monthly, downloadable CSV), ONS public sector finances (monthly), DfE school census pupil numbers, Ofgem price cap datasets, Cabinet Office Civil Service Statistics (annual), OBR Economic and Fiscal Outlook, and HM Treasury PESA (Public Expenditure Statistical Analyses). All are freely available without FOI. The NAO's 2021 report *"Evaluating government spending"* explicitly identifies gaps in how government departments use evaluation evidence, confirming that independent analysis adds genuine value. [Source: NAO, 2021; GOV.UK statistics releases]

- **FACT**: In 2022–23, UK government spending was approximately £1,200 billion, roughly 45% of GDP (£17,000 per person). [Source: IFS TaxLab]. The UK tax-to-GDP ratio is at historically elevated levels per OBR forecasts. This scale means even marginal inefficiencies represent billions of pounds — the stakes justify the analytical effort.

- **INFERENCE**: The VAT on independent schools example is analytically tractable but more complex than it first appears. You need: (a) HMRC VAT receipts specifically attributable to independent schools (not publicly broken out — may require estimation or FOI), (b) DfE data on state school per-pupil funding (published in school funding allocations), (c) actual pupil migration data (DfE school census, January each year), (d) the timing lag between VAT receipts starting and state system absorbing pupils. The net fiscal calculation is *possible* but the inputs require careful sourcing — some are estimates, not direct measurements.

- **INFERENCE**: The most credible precedent is the **IFS (Institute for Fiscal Studies)**, which uses exactly this methodology — public data, explicit assumptions, transparent modelling — and has built 40+ years of credibility by being scrupulously non-partisan in method even when conclusions favour one side politically. The **TaxPayers' Alliance** publishes similar analyses but is perceived as right-leaning, which limits its credibility with half the audience. **Full Fact** focuses on claim verification rather than impact quantification. The gap this project fills is: *systematic, queryable, methodology-transparent impact scoring across multiple policies simultaneously* — which none of these organisations currently do at scale.

- **OPINION**: The thesis that "most UK government decisions are driven by ideology, not evidence" is probably correct as a directional observation but is itself an ideological framing that will undermine the project's credibility if baked into the product. The system should be designed to *produce* that finding as an output if the data supports it, not *assume* it as an input. This distinction is the difference between journalism and propaganda.

---

## 3. Trade-offs

| Dimension | Upside | Downside |
|---|---|---|
| **Counterfactual problem** | You can model scenarios with stated assumptions | Every counterfactual is contestable; opponents will always find alternative assumptions |
| **Public data availability** | Most macro data is free and machine-readable | Granular policy-specific data often requires FOI or estimation; HMRC doesn't publish VAT by sector at fine granularity |
| **Political neutrality** | Methodology-first approach builds credibility | Genuinely neutral analysis will produce findings that anger *both* left and right — be prepared for attacks from all directions |
| **Complexity of attribution** | Some policies have clean data trails | Most spending decisions have confounded causal chains (e.g., energy prices are affected by Ukraine war, not just Net Zero policy — separating these is methodologically hard) |
| **Scale of MVP** | A focused dataset on 4-5 policies is achievable | Scope creep will kill this — resisting the urge to cover everything is a discipline problem, not a technical one |

---

## 4. What I Don't Know

- **HMRC data granularity**: I don't know the precise breakdown available for VAT receipts by sector/institution type. This may require FOI requests and the response timeline (20 working days statutory, often extended) could delay the VAT-on-schools analysis.
- **Current API availability**: GOV.UK and ONS have APIs but their coverage, reliability, and rate limits I cannot fully verify without hands-on testing. The ONS Beta API exists but data coverage is incomplete.
- **Legal status of derived datasets**: Whether publishing a derived analytical dataset that incorporates ONS/HMRC data under the Open Government Licence (OGL) requires attribution only, or whether there are restrictions on commercial use of derived works — I know OGL is generally permissive but edge cases around derived commercial products need a legal check.
- **Existing HMRC microdata access**: Researchers can apply for access to HMRC administrative microdata via the UKDS Secure Research Service — I don't know current wait times or eligibility criteria for non-academic applicants.
- **Full Fact's 2026 report findings**: The search results reference a Full Fact 2026 report but I cannot access its full content to assess what methodologies or data sources they recommend.

---

## 5. Action Items

1. **Data audit first (Week 1-2)**: Map every data source against each of the 4 example policies. For each: identify the exact dataset, URL/API, update frequency, granularity, and gaps that require estimation or FOI. Produce a public "data manifest" — this is itself a credibility asset. Priority sources: ONS Public Sector Finances, DfE School Census, HMRC Tax Receipts, Cabinet Office Civil Service Statistics, Ofgem price cap data, OBR Fiscal Sustainability Reports.

2. **Define the scorecard methodology explicitly and publicly (Week 2-3)**: The "Policy Impact Scorecard" needs at minimum: (a) direct fiscal cost/benefit — measurable from public data; (b) indirect fiscal effects — modelled with stated elasticities and cited sources; (c) GDP/productivity effects — using OBR or IFS multipliers, *cited*; (d) distributional effects — who pays, who benefits; (e) confidence rating — how much of this is hard data vs modelled. Publish the methodology *before* publishing any policy scores. This is the IFS playbook and it works.

3. **Start with the VAT on independent schools case as the proof-of-concept**: It is the most data-rich, time-bounded (policy started September 2024), and politically salient. DfE January 2025 school census data will show pupil migration. Per-pupil state funding is published. VAT receipts are estimable. This is achievable in 4-6 weeks with a small team and will generate media attention that validates the broader project.

4. **Build the MVP as a GitHub repository + methodology PDF + simple data explorer**: Not a full website initially. A public GitHub repo with raw data, transformation scripts, and outputs builds technical credibility and invites peer review. A simple Datasette or Observable notebook gives non-technical users query access. Cost: near zero. Timeline: 6-8 weeks for first policy.

5. **Engage IFS, NAO, and academic reviewers early**: Before publishing, send methodology to IFS for peer comment (they respond to serious analytical work). The NAO's 2021 evaluation framework is the closest thing to an official methodology benchmark — align to it. This inoculates against "ideological hit job" accusations.

---

## 6. Risks & Blind Spots

- **Confirmation bias in policy selection**: The four examples chosen (VAT on schools, Net Zero, civil service expansion, tax burden) all lean toward "government is doing harm." A credible tool must also score policies where evidence shows *positive* net impact — or the selection bias will be immediately apparent and the project dismissed. **This is the single biggest credibility risk.**

- **Attribution vs correlation**: Energy prices rising under Ed Miliband's watch does not mean Net Zero *caused* the rise. Global gas prices (Ukraine war, LNG competition), grid infrastructure investment cycles, and weather all affect energy costs. Isolating the Net Zero policy contribution requires explicit causal modelling, not correlation. Presenting correlation as causation will destroy credibility with any technically literate reviewer.

- **The counterfactual is not optional**: Every "net negative" finding implicitly assumes a counterfactual. For civil service expansion: compared to what? A smaller civil service that fails to deliver public services? You must state the counterfactual explicitly or critics will (correctly) say your analysis is incomplete.

- **Legal risk is low but not zero**: Using public data under OGL is legally safe. Publishing *analysis* that attributes fiscal harm to named politicians is protected as opinion/commentary in the UK under the Defamation Act 2013 (s.3 honest opinion defence) provided it is clearly labelled as analysis, not fact. **However**: if the project is commercially funded or perceived as a political campaign, different rules may apply. Get a one-hour legal review from a media law solicitor before launch — cost ~£300-500, risk mitigation: high.

- **Data lags will frustrate real-time accountability**: Most ONS/HMRC datasets are 3-6 months behind. You cannot do "live" impact scoring — you are always scoring the recent past. Frame the product accordingly.

- **The civil service expansion metric is murkier than it looks**: ONS public sector employment data includes NHS staff, teachers, and other frontline workers — lumping these in with "quango expansion" is analytically misleading. Cabinet Office headcount data separates this, but comparisons over time require careful adjustment for machinery of government changes (departments merged/split). FACT: Civil Service Statistics are published annually by Cabinet Office — but interpreting trends requires accounting for these structural changes.

---

**Bottom line**: This is analytically serious and politically necessary work. The methodology discipline — stating assumptions, separating data from inference, scoring policies that produce inconvenient findings for *any* ideological tribe — is what separates it from the dozens of existing think-tanks that already do this badly. Do that right, and you have something genuinely valuable. Cut corners on it, and you're just another advocacy operation with better spreadsheets.

---

## DeepSeek's Response

**Answer (direct recommendation)**  
Build an open, interactive **Policy Impact Tracker website** that, for a curated set of high-profile policies, computes a **net fiscal impact scorecard** using only published UK government data and transparent, pre-registered counterfactual models. Start with an MVP for one policy—the VAT on independent schools—to demonstrate feasibility before scaling. The tracker must expose all assumptions, show sensitivity ranges, and avoid any ideological commentary; it simply answers, “Did this policy raise or cost the public purse more than the alternative, based on the best available quantitative evidence?”

---

**Reasoning**  

1. **FACT**: Public trust in government spending information is low. Full Fact’s 2026 polling found no single actor commands widespread trust for accurate, reliable information (source: Full Fact Report 2026).  
   *Why this matters*: A transparent, evidence-only tool directly addresses the accountability gap, giving citizens and journalists a neutral reference point.

2. **FACT**: The UK’s core public datasets—ONS, HMRC, DfE, HM Treasury, OBR—are extensive and granular. For example, ONS provides quarterly public spending and employment data; HMRC publishes tax receipts by category; DfE releases pupil numbers and per-pupil funding. Much of this is available via APIs (ONS API, HMRC statistics portal, data.gov.uk).  
   *INFERENCE*: Because the data already exists, the main challenge is not data scarcity but rigorous counterfactual modelling and consistent integration. The project is viable without new primary data collection.

3. **FACT**: The National Audit Office has already stressed the poor use of evaluation evidence in core government departments (NAO, “Evaluating government spending”, 2021). Similarly, the IFS regularly models tax and spending changes but doesn’t run an always-on public scorecard for specific policy net impacts.  
   *OPINION*: Existing bodies either lack an interactive public platform (IFS does ad‑hoc reports) or lean towards advocacy (TaxPayers Alliance). A neutral, continuously updated, open-scorecard fills a genuine gap.

4. **INFERENCE**: A structured “policy impact scorecard” can separate cash-flow impacts from second-order effects if you limit scope. The cash-flow side (tax receipts, direct spending) is straightforward to quantify with official data. Second-order effects (e.g., GDP, productivity, cost of living) can be added as supplementary indicators but not obscured with the net fiscal figure. This keeps the core methodology auditable.

5. **OPINION**: The VAT-on-independent-schools example is the perfect MVP. HMRC can supply or estimate new VAT receipts; DfE data shows any rise in state-school pupils and the associated per‑pupil funding increase. The net fiscal impact is simply: (VAT receipts) – (extra state-school spending + any reduced independent-school tax revenues). You can build a transparent web calculator showing the calculation steps.

---

**Trade‑offs**  
- **Rigid focus on fiscal net impact** undervalues non‑financial goals (e.g., equity, national security, environmental quality). A policy could be fiscally negative but societally essential.  
- **Counterfactual uncertainty** means any single number is contestable. The tracker would need to show a range of estimates under different assumptions, which some users will misinterpret.  
- **Data lag**: Official statistics are published with months of delay, so the tracker cannot offer real‑time accountability.  
- **Scope creep**: Attempting to model every policy dilutes quality. Curating a few high‑interest policies is more trustworthy.

---

**What I don’t know**  
- I do not know the exact queryable APIs that HM Treasury or HMRC offer for granular tax‑by‑policy data; some data may require FOI or custom data‑sharing agreements.  
- I don’t know the legal fine print of using ONS data in a commercial or heavily‑trafficked public tool, although the Open Government Licence is permissive.  
- I don’t know the practical difficulty of obtaining disaggregated pupil‑level movement data for independent‑to‑state transfers post‑VAT policy—DfE may hold it but not publish the precise cross‑sector migration.  
- The exact legal risk of consistently criticising government spending decisions with official data (defamation, political pressure) is unclear; purely factual reporting is protected, but the boundary can be tested.

---

**Action items**  
1. **Select first policy and data scope**: Define the VAT‑on‑schools pilot, list all required datasets (HMRC VAT receipts, DfE pupil numbers, per‑pupil state funding, independent school employment tax effects), and confirm public availability or FOI route.  
2. **Design the scorecard architecture**: Core metric = net fiscal impact (£m, annual), supplemented by confidence intervals from sensitivity analysis. Secondary metrics: change in tax‑to‑GDP ratio segment, effect on specific ONS CPI sub‑components (if relevant). All formulas publicly documented.  
3. **Build a lightweight web MVP**: An interactive dashboard that lets users adjust assumptions (e.g., price elasticity of private school demand) and see re‑calculated net impact. Host on a transparent .org domain with complete methodology notes.  
4. **Engage an advisory panel**: Recruit econometricians from IFS style institutions and data journalists to validate the counterfactual models, ensuring the tool is seen as rigorous, not partisan.  
5. **Pre‑register evaluation criteria**: Before analysing any new policy, publish the exact methodology, data sources, and counterfactual approach on GitHub. This prevents after‑the‑fact cherry‑picking of favourable assumptions.

---

**Risks & blind spots**  
- **Political polarisation**: Even if perfectly factual, the tracker will be weaponised by the side that benefits from the calculated net impact. You must actively refuse to draw normative conclusions (“Therefore this policy is bad”); stick to “net cost to Exchequer: £Xm”.  
- **Selection bias**: Choosing which policies to track itself introduces a bias. The project needs a transparent, criteria‑based selection process (e.g., policies with explicit fiscal‑impact claims by the government).  
- **Counterfactual errors**: Using naive before‑after comparisons without controlling for unrelated trends will produce wrong numbers. The tracker must use robust causal inference methods (synthetic control, difference‑in‑differences with parallel‑trend checks), and many policies simply don’t have suitable comparison groups—leading to an “unmeasurable” verdict, which is unsatisfying but honest.  
- **Legal retaliation**: While data use is likely lawful, persistent, high‑profile factual criticism could invite reputational or bureaucratic pushback. The project should secure legal advice on defamation and on any terms of use for Crown‑copyright materials when building a public service.  
- **Unseen externalities**: The fiscal scorecard will miss costs/benefits that don’t show in government accounts (e.g., reduced societal inequality, long‑term health gains). That’s by design, but the audience must be constantly reminded of the limitation.

---

## Synthesis

Below is a rigorous synthesis of the four independent responses, with conflicts resolved where possible and gaps filled.

---

# 1) Consensus: where they align

## Strong areas of agreement
All four experts broadly agree on these points:

1. **The project is viable using public UK data**
   - This is well-evidenced.
   - Core sources named repeatedly: **ONS, HMRC, HM Treasury, OBR, DfE, Ofgem, DESNZ/BEIS, Cabinet Office, NAO**.
   - Correct in substance: these bodies do publish enough to build a first version.

2. **The biggest methodological challenge is the counterfactual**
   - This is the strongest and most justified consensus.
   - They all correctly identify that the key question is not “what happened after policy X?” but “what would have happened without policy X?”
   - This is analytically true and should dominate system design.

3. **A one-number “good/bad policy” output is risky**
   - Well-reasoned.
   - Most recommend separating:
     - observed data,
     - estimated causal effect,
     - assumptions/value judgments.
   - This is the right approach if credibility matters.

4. **The MVP should start narrow**
   - Broad agreement: start with a few tractable policies, not a universal engine.
   - This is evidence-based in a practical sense: data quality and causal identification vary hugely by policy.

5. **Transparency is essential to avoid looking partisan**
   - Strong agreement.
   - Publish methods, assumptions, sensitivity ranges, and source registry.
   - This is not just PR advice; it is structurally necessary for defensibility.

6. **The VAT-on-independent-schools case is a plausible MVP**
   - Most agree this is among the more tractable examples.
   - But “tractable” does not mean easy; there are important caveats discussed below.

## Agreements that are more assumption than proof
Some consensus points are plausible but not strongly evidenced in the responses:

- **“Public trust is low, so this product is needed.”**
  - Likely true, but the repeated Full Fact reference is vague and not properly evidenced in the responses.
  - Even if trust is low, that does not prove demand for this exact product.

- **“No one has done this in this exact way.”**
  - Plausible, but not fully demonstrated.
  - There are adjacent models: IFS, NAO, OBR, Resolution Foundation, Full Fact, House of Commons Library, Institute for Government, TaxPayers’ Alliance, open data dashboards, and policy microsimulation tools.

---

# 2) Factual conflicts

## Conflict A: what should the MVP be?

### Claims
- **Gemini**: “must be built as an open-source, interactive causal inference platform”
- **GPT**: “best MVP is a website + downloadable methodology + queryable dataset”
- **Claude**: “Build the MVP as a queryable dataset with a methodology-first public documentation layer, not a website with conclusions”
- **DeepSeek**: “Build an open, interactive Policy Impact Tracker website”

### Resolution
This is **not a factual conflict**, it’s an approach conflict.

**Best answer:** Claude/GPT have the stronger reasoning for MVP.  
Why:
- The main risk is methodological credibility, not front-end UX.
- A website with bold claims before the methods are battle-tested creates reputational risk.
- Best first build:
  1. **data pipeline**
  2. **public methodology paper**
  3. **reproducible notebook/repo**
  4. **simple front-end explorer**
- Full polished “interactive causal engine” is a later-stage product, not the MVP.

## Conflict B: availability of HMRC VAT data for independent schools

### Claims
- **Claude**: “HMRC doesn't publish VAT by sector at fine granularity”
- **DeepSeek**: “HMRC can supply or estimate new VAT receipts”
- **Gemini/GPT** imply VAT receipts can be used, but with uncertainty

### Resolution
**Claude is more correct.**

HMRC publishes extensive VAT statistics, but not typically a clean public series for **“VAT receipts from independent schools”** as a standalone policy line item. That likely requires:
- estimation,
- possibly HMRC policy costings,
- possibly FOI,
- or using Treasury/OBR costings from the policy process.

So the VAT-on-schools model is feasible, but not by simply downloading a neat official “VAT from private schools” CSV.

## Conflict C: “civil service expansion has exploded with quangos”

### Claims
- User framing plus some responses imply dramatic quango/civil service expansion.
- **Claude** specifically warns that this is analytically murky and that ONS public sector employment includes many non-civil-service workers.

### Resolution
**Claude is correct to push back.**

Important distinctions:
- **Civil service headcount**
- **Wider public sector employment**
- **Arm’s-length bodies / public bodies / quangos**
- **Contractors / consultants / outsourced service delivery**

These are not interchangeable.  
Any engine that collapses them into a single “bureaucracy exploded” metric will be wrong.

## Conflict D: “Net zero energy policy” as MVP

### Claims
- Some responses treat it as a feasible case.
- **GPT** says leave it for later because attribution is much harder.

### Resolution
**GPT is correct.**

Energy prices are driven by:
- wholesale gas prices,
- international markets,
- capacity margins,
- network charges,
- environmental/social levies,
- VAT,
- weather,
- hedging cycles,
- supplier failures,
- policy interventions.

A claim like “Ed Miliband’s agenda pushed up all costs” is too broad for a credible MVP.  
You can evaluate **specific policy instruments** within energy policy, but not “the agenda” as a clean causal unit.

---

# 3) Unsupported or weakly supported claims

## Gemini
- “The thesis that ideological posturing routinely overrides objective data-driven policymaking in Whitehall is highly accurate”
  - Unsupported opinion.
  - Could be directionally true, but not established by cited evidence.
- “viral headlines” discussion is speculative, not evidence.

## GPT
- “Trading Economics reports UK government spending at 149,462 GBP million in Q1 2026”
  - This is not useful evidence for your product design and relies on a secondary aggregator.
  - Prefer primary official sources.
- “Full Fact Report 2026” is cited vaguely without a clear report title or directly relevant finding.

## Claude
- “Defamation Act 2013 (s.3 honest opinion defence)” point is directionally sensible but oversimplified as legal advice.
  - UK defamation risk depends heavily on publication wording, implied factual allegations, and whether you target identifiable individuals.
  - Legal review is sensible; the statement shouldn’t be treated as sufficient legal guidance.
- “Cost ~£300–500” for legal review is arbitrary.

## DeepSeek
- “HMRC can supply or estimate new VAT receipts”
  - “Estimate” yes; “can supply” is too strong absent proof.
- “The net fiscal impact is simply: VAT receipts – extra state-school spending + any reduced independent-school tax revenues”
  - This is **not simple** if done properly.
  - Missing transitional effects, fee pass-through, pupil mix, existing reliefs, school closures, staffing effects, local capacity costs, and behavior changes.

---

# 4) Disagreements on approach and who reasons better

## A. Single score vs multi-dimensional scorecard
- **Gemini/GPT/Claude** lean against a single black-box number.
- **DeepSeek** is more comfortable with a net fiscal tracker plus supplements.

### Best view
**GPT/Claude have the stronger reasoning.**

Why:
- “Net fiscal impact” is only one lens.
- Many policies are fiscally negative in the short term but welfare-positive overall.
- If you want credibility, you should report at least:
  - **Exchequer effect**
  - **GDP/productivity effect**
  - **household cost effect**
  - **distributional effect**
  - **evidence quality/confidence**

A single score can exist, but only as a user-configurable composite, not as the truth.

## B. MVP format: website first vs methodology/repo first
- **Claude** strongest here.
- **GPT** also sensible.
- **Gemini/DeepSeek** are too product-forward for the risk profile.

### Best view
Build **methodology + reproducible data + light web layer**, not a media-first site.

## C. Policy scope
- **GPT/Claude** are more disciplined: start with tractable cases, avoid broad ideological bundles.
- **Gemini/DeepSeek** are directionally right but less strict on scoping.

### Best view
Evaluate **discrete, dated policy interventions**, not narratives.

---

# 5) Blind spots: what all four missed

This is the most important section.

## 1. They did not distinguish enough between policy evaluation types
You need a taxonomy. Not all policies can be evaluated the same way.

At least four categories:

1. **Direct accounting policies**
   - e.g. a tax change, benefit rate, departmental headcount change
   - mostly arithmetic + behavioral assumptions

2. **Operational efficiency policies**
   - e.g. civil service expansion, quango reform
   - require output measures, not just input cost

3. **Market-shaping policies**
   - e.g. energy regulation
   - much harder causal attribution

4. **Long-horizon investment policies**
   - e.g. infrastructure, decarbonisation, education reform
   - costs now, benefits later; short-run fiscal score can mislead

Without this taxonomy, you risk applying the wrong method to the wrong policy.

## 2. They underplayed revision, comparability, and metadata issues
Public UK data is not just “available”; it is often:
- revised later,
- rebased,
- reclassified,
- changed in methodology,
- broken across departmental restructures,
- inconsistent across UK nations.

Your engine needs a **data governance layer**:
- versioned snapshots,
- revision tracking,
- series break flags,
- methodology notes,
- source hierarchy.

This is essential.

## 3. They missed devolved government complexity
Many policy areas are partly or largely devolved:
- education,
- health,
- transport,
- some economic development,
- implementation differences across England/Scotland/Wales/NI.

If you say “UK government policy” but use England-only operational data, you can mislead badly.

You need to define the jurisdiction of each policy:
- UK-wide
- England-only
- GB-only
- devolved/mixed competence

## 4. They did not stress enough the distinction between stated objective and national welfare
A policy can:
- fail its own stated objective,
- succeed fiscally,
- fail economically,
- succeed distributionally,
- or vice versa.

Your engine should score at least two separate questions:
1. **Did it achieve the government’s stated objective?**
2. **What was its measurable net impact across selected metrics?**

Those are not the same thing.

## 5. They missed implementation and transition costs in enough detail
For policies like VAT on private schools:
- legal/admin setup costs,
- school adaptation,
- local authority placement costs,
- transport/SEND pressure,
- timing mismatch between receipts and expenditure,
- capacity constraints in certain regions.

For civil service cases:
- severance costs,
- consultancy substitution,
- digital transition spending,
- output/service delay impacts.

These are not footnotes; they can dominate short-run effects.

## 6. They did not mention uncertainty communication design enough
It’s not enough to have confidence bands in a methodology PDF.

You need a standard output like:
- **Observed data**
- **Estimated causal effect**
- **Assumption-sensitive range**
- **Evidence quality score**
- **What we cannot observe**
- **Last updated / subject to revision**

This is a product design issue as much as a statistical one.

## 7. They under-discussed licensing and terms of use nuance
Most official UK data is under the **Open Government Licence**, but not all.
You need to check:
- OGL coverage,
- Crown copyright notices,
- API usage terms,
- third-party rights within government publications,
- whether charts/tables are OGL if they embed external data,
- restrictions around secure microdata.

This matters if the product is commercial.

## 8. They missed the need for a policy registry and inclusion rules
Selection bias is one of the biggest threats.

You need published rules for:
- which policies are eligible,
- minimum data requirements,
- minimum measurable scale,
- when a policy is “not measurable”,
- when a score is provisional,
- how updates occur.

Without this, your engine will look hand-picked for narrative value.

## 9. They underplayed “absence of evidence” outputs
A credible engine must often conclude:
- **insufficient evidence**
- **effect not identifiable**
- **policy too early to assess**
- **observed change cannot be attributed**

This should be seen as success, not failure.

## 10. They didn’t mention pre-existing UK micro-simulation infrastructure enough
For tax/benefit analysis, there are established models and precedents:
- **IFS tax-benefit microsimulation**
- **UKMOD / EUROMOD**
- OBR and HMT policy costings
- departmental impact assessments

You do not need to invent everything from scratch.

---

# 6) Final synthesised answer

## Short answer
Yes, this is a real and potentially valuable project — but only if you build it as a **transparent policy evaluation system**, not a politically pre-committed “gotcha engine.” The main challenge is **causal attribution**, not data access. Start with **a small number of discrete policies with strong public datasets**, publish **methods before conclusions**, and separate **fiscal accounting** from **wider economic and welfare effects**.

---

## A. What public UK data sources are available?

### Core official sources
For a first version, the main sources are:

- **ONS**
  - GDP, productivity, CPI, labour market, public sector employment, public finances
  - Good APIs and bulk downloads, but some series are revised and methodology changes matter

- **HM Treasury**
  - PESA, Whole of Government Accounts, spending reviews, departmental spending data

- **OBR**
  - Economic and Fiscal Outlook, forecast assumptions, policy costings where published

- **HMRC**
  - tax receipts, VAT statistics, tax expenditures/reliefs, distributional tax publications
  - strong for aggregate tax series; weaker for very policy-specific micro-breakouts in public form

- **DfE**
  - school census, school capacity, funding allocations, attainment, LA-level data

- **Ofgem**
  - default tariff price cap, retail market data

- **DESNZ** (formerly BEIS)
  - energy generation, fuel mix, prices, demand, policy publications

- **Cabinet Office / Civil Service Statistics**
  - civil service headcount, grades, departmental breakdowns

- **NAO**
  - value-for-money reports, evaluation critiques, implementation analysis

- **House of Commons Library / Institute for Government**
  - excellent contextual briefings, though not primary raw data

- **data.gov.uk**
  - discovery layer, not always the canonical source

- **FOI**
  - useful for implementation detail, internal management information, and missing operational data
  - but slow, uneven, and often refused for policy formulation or burden reasons

### Important correction
Do **not** assume every policy has a neat public dataset.  
Some examples, like “VAT receipts from independent schools,” likely require **estimation**, not direct official reporting.

---

## B. How to structure the policy impact scorecard

Do **not** start with one “net positive/net negative” number.

Use a standard scorecard with these layers:

### 1. Policy definition
- exact measure
- implementation date
- jurisdiction
- target population
- stated government objective

### 2. Observed data
- what changed in official data after implementation
- no causal claims yet

### 3. Counterfactual estimate
- what likely would have happened otherwise
- clearly labelled as modelled estimate
- method stated:
  - accounting model
  - difference-in-differences
  - synthetic control
  - microsimulation
  - scenario modelling

### 4. Impact dimensions
At minimum:

**A. Direct Exchequer impact**
- receipts gained/lost
- spending gained/lost
- admin/implementation cost

**B. Macroeconomic impact**
- GDP/GVA
- productivity
- employment if relevant

**C. Household/business impact**
- CPI or specific cost pass-through
- disposable income effects
- sector competitiveness

**D. Distributional impact**
- income deciles
- region
- age cohort
- business size/sector where relevant

**E. Delivery/output impact**
- only where relevant
- e.g. waiting times, pupil outcomes, service throughput

### 5. Evidence quality
A simple rating such as:
- High: strong identification / direct administrative data
- Medium: partial identification / some estimation
- Low: descriptive or heavily assumption-driven
- Not measurable yet

### 6. Range, not point estimate alone
Each key estimate should show:
- central estimate
- uncertainty range
- key assumptions driving the range

---

## C. What metrics matter?

You asked the right question: tax receipts/spending/debt/GDP/productivity/cost of living all matter, but they should not be collapsed carelessly.

### Minimum core metrics
1. **Net Exchequer effect**
2. **Borrowing/debt effect**
3. **GDP/productivity effect**
4. **Household cost-of-living effect**
5. **Distributional effect**
6. **Implementation/admin cost**
7. **Evidence strength**

### Important principle
Separate:
- **fiscal score**
from
- **national welfare score**

A policy can raise revenue but reduce growth, or increase spending but improve long-run productivity. Those are different judgments.

---

## D. How to avoid political bias

This is mainly about governance and process.

### Non-negotiables
1. **Evaluate discrete policies, not ideological narratives**
2. **Pre-publish the methodology**
3. **Use the same template for all policies**
4. **Score policies associated with different parties and ideologies**
5. **Publish assumptions and sensitivity analysis**
6. **Allow “insufficient evidence” as a valid outcome**
7. **Keep fact, estimate, and judgment separate**
8. **Use external review from mixed ideological backgrounds**

### Biggest trap
If all your launch examples are “government intervention bad,” the tool will be dismissed as advocacy even if some math is good.

So include at least one policy where the evidence may come out positive.

---

## E. What’s the right MVP?

### Best MVP
Not a full “engine.”  
Build this stack:

1. **Policy registry**
   - what you cover, why, and inclusion rules

2. **Reproducible data pipeline**
   - source manifest, scripts, versioning, revision handling

3. **Methods paper**
   - scorecard template
   - causal methods hierarchy
   - confidence rules
   - update policy

4. **One or two case studies**
   - with notebooks and downloadable data

5. **Simple public front end**
   - charts
   - scorecards
   - assumptions toggle
   - source links

### First policy choice
**VAT on independent schools** is a reasonable first case.  
Why:
- discrete policy
- clear implementation timing
- identifiable fiscal channels
- strong public interest
- enough data to produce a bounded estimate

### Second/third policy suggestions
Better than “net zero agenda” as a bundle:
- **civil service headcount by department vs output metrics**
- **specific tax measure and receipts/GDP effect**
- **specific energy levy or scheme**, not the whole decarbonisation agenda

Avoid broad slogans as units of analysis.

---

## F. Legal considerations

### Generally low risk, but not zero
Using official public data is usually lawful, especially under the **Open Government Licence**, but check each source.

### Main legal/compliance risks
- licence compliance
- third-party rights inside official publications
- API terms
- republishing derived datasets commercially
- defamation risk if you overstate claims about named individuals
- data protection if you ever touch microdata or linked records

### Practical advice
Get a solicitor to review:
- publication wording,
- data licensing,
- company/charity/nonprofit structure,
- whether any work could be construed as regulated political campaigning.

That last point was mostly missed by the experts: if this becomes influential during an election period, UK electoral/campaigning rules may matter depending on structure and activity.

---

## G. How to handle the counterfactual

Use a hierarchy. Not every policy gets the same method.

### Method ladder
1. **Direct accounting identity**
   - best for simple fiscal mechanics

2. **Microsimulation**
   - ideal for tax/benefit/distributional analysis
   - use established UK tax-benefit modelling where possible

3. **Difference-in-differences / event study**
   - when clean treatment/control comparisons exist

4. **Synthetic control**
   - useful but not always available; requires careful donor pool choice

5. **Structural/scenario modelling**
   - fallback when identification is weak

6. **Descriptive only**
   - if causal identification is not credible

### Core rule
Every page should explicitly say:
- what is observed,
- what is estimated,
- what assumptions matter most,
- what cannot be known.

---

## H. Who has done this before, and what to learn

### Best precedents
- **IFS**
  - gold standard for transparent fiscal/policy analysis
  - lesson: methodological restraint builds trust

- **NAO**
  - strong on value-for-money and evaluation discipline
  - lesson: implementation and delivery matter, not just headline spending

- **OBR**
  - strong on baseline/forecast logic and policy costings
  - lesson: assumptions should be explicit and institutionalised

- **Full Fact**
  - strong on sourcing and communication discipline
  - lesson: trust depends on traceability and careful wording

- **Institute for Government**
  - useful for machinery-of-government and implementation insight

- **TaxPayers’ Alliance**
  - shows audience demand for spending scrutiny
  - lesson: perceived partisanship can cap influence

### White space
Your gap is not “using public data” alone.  
It is combining:
- official datasets,
- reproducible methods,
- policy-by-policy scorecards,
- public queryability,
- explicit uncertainty.

---

# 7) Confidence level

**Confidence: Medium-High**

Why not High?
- The broad architecture is clear.
- The data ecosystem is real.
- But policy-specific feasibility varies a lot.
- Some flagship claims, especially around energy and policy-specific tax receipts, may be much harder than they first appear.

### What would increase confidence?
- A proper data audit for the first 3 policies
- Confirmation of exact HMRC/DfE/ONS series available
- A prototype causal design for the VAT-on-schools case
- Legal review of licensing and publication structure

### What would reduce confidence?
- If the project insists on broad ideological framing from the outset
- If it tries to score “net zero” or “bureaucracy” as monoliths
- If there is no in-house econometrics capability

---

# 8) Open questions to investigate before acting

1. **What is the exact product goal?**
   - journalism?
   - public-interest watchdog?
   - think tank?
   - campaign tool?
   - commercial data product?

2. **Who is the audience?**
   - voters
   - journalists
   - MPs
   - researchers
   - donors
   - campaigners

3. **What is the policy inclusion rule?**
   - scale threshold?
   - fiscal salience?
   - data quality threshold?
   - explicit government claim to test?

4. **What jurisdiction do you cover?**
   - UK-wide?
   - England-only?
   - devolved comparators?

5. **Do you have econometrics/microsimulation capability?**
   - If not, start with accounting-style scorecards only.

6. **Can you get enough granularity for the VAT-on-schools model?**
   - HMRC receipts
   - DfE migration/capacity data
   - local authority cost pressures
   - timing assumptions

7. **What is your standard for “causal enough”?**
   - Will you publish “insufficient evidence” outcomes?

8. **How will you handle revisions and methodology changes in official series?**
   - versioning and audit trail are essential

9. **Will you assess positive policies too?**
   - if not, don’t claim neutrality

10. **What legal/entity structure will you use?**
   - nonprofit, company, media outlet, think tank
   - this affects governance, trust, and legal exposure

---

## Bottom line
The best version of this idea is **not** “prove ideology beats evidence.”  
It is: **build a transparent UK policy impact scorecard system that measures what happened, estimates what likely would have happened otherwise, and shows the fiscal/economic/distributional consequences with explicit uncertainty.**

If you do that, it could be genuinely useful.  
If you launch as a conclusion-first political engine, it will be dismissed quickly and probably deserve to be.
