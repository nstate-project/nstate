# nstate

**We audit every pound your government spends. We prove what fails. We build the alternative.**

Governments across the democratic world have expanded relentlessly for decades. Spending up. Taxes up. Bureaucracy up. Public services down. Trust in collapse. And after all of it — the people paying the bills have no clear, honest, reproducible account of what they got in return.

nstate changes that.

We are an open-source, grassroots audit of government spending — starting with the UK, designed to be forked for anywhere. We find the policies that cost the most and deliver the least. We prove it with the government's own published data. And we build the open-source tools that could do the job better, for less.

Then we ask the question governments don't want asked: **if this can be done for a fraction of the cost — why are you still paying for the current version?**

---

## Why now

In the UK alone, multiple prime ministers have cycled through in under a decade. Governments of every party have promised efficiency, delivered expansion, and blamed each other. The state has grown. The tax burden has grown. And the fundamental question — does any of this actually work? — has never been answered systematically, in public, with reproducible evidence.

The institutions that should answer it (the IFS, the NAO, the OBR) do excellent but fragmented work. Nobody runs a continuous, policy-by-policy, publicly queryable scoreboard — where every claim traces back to a source, every number can be rerun, and every "wasteful" verdict has to survive scrutiny.

That is what nstate is.

---

## How it works

Every policy gets the same scorecard:

- **What did it cost?** (official sources, cited)
- **What was it supposed to achieve?** (government's own stated objective)
- **What did it actually achieve?** (measured outcomes vs. stated goals)
- **What is the counterfactual?** (what would likely have happened without it)
- **Who paid, who benefited, who lost?** (distributional impact)
- **Could an open-source agent do this cheaper?** (shadow benchmarking)

All methodology is public. All data pipelines are reproducible. If we're wrong, show us — and we'll correct it.

---

## The AI layer

For each audited process, we build the alternative. Open-source agents that can handle the administrative function — processing applications, routing cases, flagging anomalies, generating decisions for human review. We run them in shadow mode against the current system. We publish the results.

We are not arguing for removing government. We are arguing that a large proportion of what government does is administrative overhead that can be done faster, cheaper, and more consistently — and that the savings belong to taxpayers, not to the bureaucracy.

Governments can use the agents if they want. Most won't. That's the point.

---

## UK first. Then everywhere.

The UK audit is the proof of concept. The methodology, the scorecard template, the agent framework — all of it is designed to be forked. If you want to run this for France, Germany, Australia, Canada, South Africa — take the template, apply it to your country's public data, open a pull request. We review the methodology, not the politics.

One standard. Many audits. Transparent everywhere.

---

## What nstate is not

- Not a political party or campaign
- Not affiliated with any think tank, donor, or government
- Not a news outlet — we publish evidence, not opinion
- Not anti-government in principle — we are pro-accountability, always

Our findings follow the data. If a programme delivers strong outcomes at reasonable cost, we say so. Our credibility depends on being capable of saying that.

---

## Get involved

- **Claim a policy area:** open an issue, pick a UK policy, follow the scorecard template, submit a PR
- **Add a country:** fork the country template, start your national audit
- **Build an agent:** pick an audited process, build the shadow agent, benchmark it against current practice
- **Spread it:** share findings, cite us, challenge us, improve us

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full guide.

---

## Structure

```
nstate/
├── README.md               ← you are here
├── MISSION.md              ← the thesis and framing
├── METHODOLOGY.md          ← scorecard rules, evidence standards, counterfactual framework
├── CONTRIBUTING.md         ← how to add a scorecard, an agent, or a country
├── COUNTRY-TEMPLATE.md     ← fork this to start a national audit
├── uk/
│   ├── README.md           ← UK overview and findings summary
│   ├── scorecards/         ← one .md file per policy
│   └── pipelines/          ← data fetch scripts (Python)
├── agents/
│   └── README.md           ← agent framework and shadow benchmarking guide
└── research/               ← debates, background analysis, historical context
```

---

## Data

All source data is public UK government data (ONS, HMRC, OBR, DfE, DWP, Ofgem, Cabinet Office, NAO and others). Raw data and transformation scripts live in this repository. No source data requires purchase or FOI — if a claim can't be traced to a public source, it doesn't go in a scorecard.

---

## Licence

Code: MIT. Reports and analysis: CC BY 4.0. Source data: original licence (mostly Open Government Licence). You can use, fork, adapt and build on everything here — provided you maintain attribution and publish your methodology.

---

*nstate is built by people who believe the public is owed an honest account of what government does with their money. Join us.*
