# Contributing to nstate

nstate is open source and community-driven. The more people who contribute, the more comprehensive and credible the evidence base becomes. This guide explains exactly how to get involved — whether you want to add a policy scorecard, build a shadow agent, or start a national chapter for your own country.

---

## Ways to contribute

| Contribution type | What it involves | Skills needed |
|---|---|---|
| **Policy scorecard** | Research and document a UK government policy | Data literacy, access to public datasets |
| **Data pipeline** | Automate fetching of a source dataset | Python, basic ETL |
| **Shadow agent** | Build an AI agent that benchmarks against a current administrative process | Python, LLMs |
| **Country chapter** | Fork the methodology and start a national audit | Same as scorecard, local knowledge |
| **Methodology improvement** | Propose changes to the scoring framework | Econometrics / policy analysis background helpful |
| **Translation / accessibility** | Make findings accessible to non-technical audiences | Writing, communication |

---

## Before you start

1. **Read [METHODOLOGY.md](METHODOLOGY.md).** Every scorecard follows the same framework. If you don't follow it, the PR will not be merged.
2. **Check open issues.** Someone may already be working on the policy you have in mind. Claim it with a comment before you start.
3. **Check the inclusion criteria.** Not every policy qualifies. The criteria are in METHODOLOGY.md. If unsure, open a discussion issue first.

---

## Adding a policy scorecard

### Step 1: Claim it
Open an issue titled `[Scorecard] Policy name` and say you're working on it. This prevents duplication.

### Step 2: Find the data
Every claim must trace to a primary official source. See the data sources table in METHODOLOGY.md. Before you write anything, confirm the data exists and is in a form you can cite.

### Step 3: Write the scorecard
Copy `uk/scorecards/TEMPLATE.md` and fill in every section. Do not skip sections. If data is unavailable for a section, write "Data not available: [reason]." If the counterfactual cannot be constructed, write "Counterfactual: not constructible — insufficient data."

Your scorecard must include:
- Every data point cited with source, URL, and data date
- Uncertainty ranges on all estimated figures (not just point estimates)
- An evidence quality rating for each impact dimension
- A clear separation between observed facts, modelled estimates, and editorial judgements

### Step 4: Submit a PR
Branch name: `scorecard/policy-name`
PR title: `Add scorecard: [Policy name]`
PR description: summarise what the policy is, what the key findings are, and flag any areas of uncertainty you are aware of.

### Step 5: Review
A maintainer will review for:
- Methodology compliance (same template, sources cited, uncertainty shown)
- Factual accuracy (can the numbers be reproduced from the cited sources)
- Scope (does the policy meet inclusion criteria)
- Framing (are facts, estimates and editorial separated correctly)

We do not review for political conclusions. If the data shows a policy works, the scorecard says it works.

---

## Adding a data pipeline

Data pipelines live in `uk/pipelines/`. Each pipeline is a Python script that fetches, transforms, and saves a dataset used by one or more scorecards.

Requirements:
- Fetches from primary official source only
- Saves output as CSV or Parquet in `uk/data/`
- Includes a `--help` flag with description, source URL, and output schema
- Runs without paid API keys (all sources must be freely available)
- Includes a `requirements.txt` or is part of the top-level project dependencies

Branch name: `pipeline/source-name`

---

## Building a shadow agent

Shadow agents live in `agents/`. Each agent is benchmarked against a specific administrative process identified in a scorecard.

A shadow agent submission must include:
- A description of the administrative process being modelled
- The current estimated cost of the human process (with source)
- The agent code (Python, documented)
- A test harness with sample inputs and expected outputs
- A benchmark report comparing the agent to the human baseline on: cost per decision, processing time, error rate on test cases, and any identified failure modes
- A clear statement of what the agent does NOT handle and why

We do not accept agents that make autonomous decisions on real cases. Shadow mode only — agents recommend, humans decide, until the agent is separately approved for bounded deployment.

---

## Starting a country chapter

Fork the repo. Create a top-level directory named with your country code (`fr/`, `de/`, `au/`, etc.). Copy `COUNTRY-TEMPLATE.md` and complete it for your country. Start with the equivalent of the UK's first three scorecard areas — the ones with the strongest data availability.

A country chapter PR must include:
- `{country}/README.md` — overview of the national audit, key data sources, and status
- At least one completed scorecard following the standard template
- A data sources table equivalent to the UK version, mapping to your country's official statistics bodies

Country chapters use the same scorecard template and methodology. Local data sources replace UK ones, but the evidence standards are identical.

Open a discussion issue first with the title `[Country] {country name}` so we can flag any existing forks or collaborators.

---

## Methodology contributions

If you want to propose a change to the scorecard template or methodology:

1. Open an issue explaining the proposed change, why the current approach is insufficient, and what you would replace it with
2. Reference any academic literature or official evaluation frameworks that support the change
3. Show how the change would affect at least one existing scorecard
4. Be prepared for a longer review process — methodology changes affect every scorecard

We maintain backward compatibility where possible. If a methodology change would change the verdict on an existing scorecard, we reversion that scorecard and note the reason.

---

## Standards for all contributions

**No numbers without sources.** Every quantitative claim needs: source name, URL, dataset name, and data date. If you cannot provide this, the number does not go in the scorecard.

**No editorialising in scorecard fields.** Use the "Editor's note" field clearly labelled for any interpretive remarks. The scored fields contain facts, estimates, and confidence ratings only.

**No targeting individuals.** We do not name civil servants, benefit recipients, low-level employees, or contractors in our findings. We measure systems and programmes.

**No speculation about motives.** We measure outcomes, not intentions. A programme that fails may have failed due to poor design, bad implementation, unforeseeable circumstances, or deliberate obstruction. Our scorecards record what happened, not why ministers decided it.

---

## Review timeline

We aim to respond to all PRs within two weeks. Scorecards require review from at least two maintainers before merge. Data pipelines require one maintainer plus one independent reproducibility check. Country chapters require review from someone with knowledge of the relevant country's data infrastructure where possible.

---

## Code of conduct

We are building an evidence base, not a political movement. Disagreements about findings should be resolved by pointing to better data or stronger methodology — not by argument about intentions.

Contributors who submit scorecards designed to reach a predetermined conclusion (cherry-picked data, excluded contradicting evidence, inflated estimates) will be removed.

Contributors who target individuals, harass other contributors, or attempt to politicise the review process will be removed.

We welcome people from all political backgrounds. Our only commitment is to the evidence.

---

## Questions

Open a GitHub Discussion. Do not open an issue for general questions — issues are for specific scorecard claims, data pipeline bugs, or methodology proposals.
