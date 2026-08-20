# SPEC-NSTATE-PLATFORM.md
# nstate — Full Platform Specification v0.1

**Mission:** Dismantle overreaching, wasteful states — through transparency and solutions.

**Status:** Draft · Pre-build
**Last updated:** 2026-08-19

---

## 1. Product Overview

nstate is a public intelligence platform. Anyone, with no account or login, can ask a plain-English question about government spending and policy, receive a data-backed answer with a chart, and share it instantly on social media.

It is also a living data warehouse: government datasets are loaded continuously, agents scan for anomalies in the background, and findings are published into a public feed. When someone asks for data we don't have, the gap is logged and prioritised.

The platform is fully open source. Anyone can contribute data pipelines, challenge findings, or fork the methodology for their own country.

### What it is not
- Not a government-affiliated tool
- Not paywalled or login-gated
- Not a static report or PDF
- Not a general AI chatbot — every answer traces to a specific government data source

---

## 2. Core User Journeys

### Journey 1: The Curious Citizen
1. Lands on nstate.org (from a shared card on X/Bluesky)
2. Sees the search box and live query feed
3. Types a question: *"How much has the civil service cost per taxpayer since 2010?"*
4. Gets: headline stat, chart, plain-English explanation, one caveat, citations
5. Clicks Share → permanent link with OG image card generated → posts to X
6. Done. No account. No friction.

### Journey 2: The Journalist
1. Finds a reviewed finding on nstate.org
2. Reads the plain-English headline
3. Clicks "show working" → sees exact source, SQL query, data release date, pipeline version
4. Downloads CSV or copies citation in academic/journalistic format
5. Publishes their piece citing nstate.org/f/[id]

### Journey 3: The Data Gap Reporter
1. Types a question — agent finds no matching data
2. Sees: *"We don't have this data yet. 23 others have asked. Vote to prioritise."*
3. Clicks vote → gap logged, admin notified if threshold reached
4. Returns later when data is loaded (optional email notification)

### Journey 4: The Country Builder
1. Reads CONTRIBUTING.md and COUNTRY-TEMPLATE.md on GitHub
2. Opens issue: "Country chapter: Germany"
3. Adds `/countries/de/config.yaml` with Destatis (German stats office) sources
4. Submits first scorecard via PR
5. DE chapter appears on nstate.org/de

---

## 3. Technical Architecture

### 3.1 Overview

```
┌─────────────────────────────────────────────────┐
│                 nstate.org                      │
│              (Next.js — Vercel)                 │
│                                                 │
│  Static pages: /, /methodology, /contribute     │
│  Dynamic pages: /[country]/query, /f/[id]       │
│  API routes: /api/query, /api/findings          │
└─────────────────┬───────────────────────────────┘
                  │ HTTP
┌─────────────────▼───────────────────────────────┐
│           Query API (FastAPI)                   │
│              VPS — nstate-vps1                  │
│                                                 │
│  POST /query  → agent → SQL → DuckDB → result  │
│  GET  /findings → curated findings feed         │
│  GET  /gaps    → data gap queue                 │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│          Data Warehouse (DuckDB)                │
│              VPS — nstate-vps1                  │
│                                                 │
│  uk_* tables  — ONS, HMRC, OBR, Cabinet Office │
│  eu_* tables  — Eurostat (Phase 2)             │
│  de_* tables  — Destatis (Phase 2)             │
│  meta_*       — sources, gaps, findings         │
└─────────────────┬───────────────────────────────┘
                  │
┌─────────────────▼───────────────────────────────┐
│         Raw Data Store (Parquet)                │
│     VPS disk + GitHub (small files)             │
│                                                 │
│  /data/uk/ons/[dataset]/[date].parquet          │
│  /data/uk/hmrc/[dataset]/[date].parquet         │
│  manifest.json (hash, source URL, date)         │
└─────────────────────────────────────────────────┘
```

### 3.2 Repository Structure (Monorepo)

```
nstate/
├── apps/
│   └── web/                  ← Next.js app
│       ├── app/
│       │   ├── page.tsx      ← Homepage (search + feed)
│       │   ├── [country]/
│       │   │   └── query/    ← Country query page
│       │   ├── f/[id]/       ← Finding permalink
│       │   ├── findings/     ← Findings feed
│       │   ├── methodology/  ← Static content
│       │   ├── contribute/   ← Static content
│       │   └── api/          ← Next.js API routes (proxy to FastAPI)
│       └── components/
│
├── services/
│   └── api/                  ← FastAPI backend
│       ├── main.py
│       ├── query/            ← Query agent
│       ├── agents/           ← Background anomaly agents
│       ├── gaps/             ← Gap detection
│       └── findings/         ← Findings management
│
├── data/
│   ├── uk/
│   │   ├── pipelines/        ← Python fetch scripts
│   │   └── parquet/          ← Raw data files (gitignored if large)
│   ├── eu/                   ← Phase 2
│   └── de/                   ← Phase 2
│
├── countries/
│   ├── uk/config.yaml        ← UK data sources + schedule
│   ├── eu/config.yaml        ← Phase 2
│   └── TEMPLATE.yaml         ← Fork this for new countries
│
├── METHODOLOGY.md
├── CONTRIBUTING.md
├── COUNTRY-TEMPLATE.md
└── docker-compose.yml        ← Full local stack in one command
```

---

## 4. Data Layer

### 4.1 UK First-Wave Datasets (Priority Order)

| Dataset | Source | Update frequency | Tables |
|---|---|---|---|
| Public sector finances | OBR | Monthly | `uk_psf_*` |
| Government expenditure (PESA) | HM Treasury | Annual | `uk_pesa_*` |
| Civil service statistics | Cabinet Office | Annual | `uk_civil_service_*` |
| Tax receipts | HMRC | Monthly | `uk_tax_receipts_*` |
| ONS national accounts | ONS | Quarterly | `uk_national_accounts_*` |
| Energy bill components | Ofgem | Quarterly | `uk_energy_bills_*` |

### 4.2 Data Pipeline Contract

Every pipeline script must produce:

```
/data/uk/[source]/[dataset]/
  raw/[YYYY-MM-DD].parquet        ← exact bytes from source
  manifest.json                   ← URL, date, SHA-256, licence, adapter version
  clean/[YYYY-MM-DD].parquet      ← normalised, typed, documented columns
```

Manifests are committed to git. Raw Parquet goes to VPS disk. Forks download from source using the manifest.

### 4.3 DuckDB Schema Conventions

```sql
-- Every table follows this pattern
CREATE TABLE uk_civil_service_headcount (
  period        DATE,            -- always a date, not a string
  value         DECIMAL(18,2),   -- never store as text
  unit          VARCHAR,         -- 'headcount', 'GBP', 'GBP_millions'
  price_basis   VARCHAR,         -- 'nominal', 'real_2024'
  geography     VARCHAR,         -- 'UK', 'England', 'Scotland'
  source_id     VARCHAR,         -- FK to meta_sources
  release_date  DATE,            -- when the government published this
  _loaded_at    TIMESTAMP        -- when we ingested it
);
```

No silent overwrites. Each new release adds rows, never replaces. Old vintages remain queryable.

### 4.4 Country Config Format

```yaml
# countries/uk/config.yaml
country: uk
name: United Kingdom
currency: GBP
fiscal_year: April-March
data_licence: OGL v3
attribution: "Contains public sector information licensed under the Open Government Licence v3.0"

sources:
  - id: obr_psf
    name: OBR Public Sector Finances
    url: https://obr.uk/data/
    schedule: "0 9 * * 1"    # Monday 09:00 UTC
    pipeline: data/uk/pipelines/obr_psf.py
    tables: [uk_psf_receipts, uk_psf_expenditure]
    licence: OGL v3

  - id: cabinet_office_civil_service
    name: Cabinet Office Civil Service Statistics
    url: https://www.gov.uk/government/collections/civil-service-statistics
    schedule: "0 9 1 9 *"   # 1 Sep annually
    pipeline: data/uk/pipelines/cabinet_office_civil_service.py
    tables: [uk_civil_service_headcount, uk_civil_service_pay]
    licence: OGL v3
```

---

## 5. Query Agent

### 5.1 Flow

```
User input (plain English)
  ↓
Intent parser (OpenRouter/Haiku)
  → extracts: topic, metric, geography, time range, comparison
  → maps to: available tables in DuckDB
  ↓
Data check
  → tables found? → continue
  → tables NOT found? → gap detection flow
  ↓
SQL generator (OpenRouter/Sonnet)
  → generates read-only SQL against DuckDB
  → validated: read-only, table allowlist, row limit
  ↓
DuckDB execution
  → returns typed result object (no model can alter the numbers)
  ↓
Chart generator
  → Vega-Lite spec from result + chart type selection
  ↓
Narrative generator (OpenRouter/Haiku)
  → receives: {question, result_object, chart_type, caveats}
  → generates: headline (1 sentence), explanation (2-3 sentences)
  → numbers injected from result_object as {{placeholders}}
  → model cannot change or invent numbers
  ↓
Verifier
  → checks every number in narrative matches result_object
  → if mismatch: retry or surface as unverified
  ↓
Result object
  {
    id: "uk-2026-0042",
    question: "How much has the civil service cost since 2010?",
    interpreted_as: "UK civil service total pay bill 2010-2024",
    headline: "The UK civil service pay bill grew from £Xbn to £Ybn between 2010 and 2024",
    chart: { vega_lite_spec },
    key_stat: { value, unit, context },
    caveat: "Figures are nominal; real-terms growth is lower",
    sources: [{ id, name, release_date, url, licence }],
    sql: "SELECT ...",
    pipeline_version: "uk-cs-1.2.0",
    status: "user_analysis",
    created_at: "2026-08-19T16:00:00Z"
  }
```

### 5.2 Agent Rules

- Agents NEVER generate numbers. Numbers come from DuckDB result rows only.
- Agents NEVER post autonomously. All social posts require human approval (initially).
- Agents flag anomalies as `automated_finding` — never as `reviewed_finding`.
- All agent activity is logged: model, prompt, response, timestamp.
- Fail closed: if data freshness > 30 days, surface a staleness warning.

### 5.3 OpenRouter Model Routing

| Task | Model | ~Cost/query |
|---|---|---|
| Intent parsing | claude-haiku-4-5 | $0.0003 |
| SQL generation | claude-sonnet-4-6 | $0.003 |
| Narrative generation | claude-haiku-4-5 | $0.0003 |
| Anomaly detection agents | claude-haiku-4-5 | $0.0003 |
| Finding review summary | claude-sonnet-4-6 | $0.003 |

Typical user query: ~$0.004 all-in.

---

## 6. Frontend (Next.js)

### 6.1 Homepage

```
┌──────────────────────────────────────────────────┐
│  nstate                          UK ▾  [github]  │
│                                                  │
│         Dismantle overreaching,                  │
│         wasteful states.                         │
│                                                  │
│  ┌────────────────────────────────────────────┐  │
│  │  Ask about UK government spending...       │  │
│  └────────────────────────────────────────────┘  │
│                                                  │
│  Try: "HS2 cost overrun"  "NHS agency staff"     │
│       "Civil service headcount since 2010"       │
│                                                  │
├──────────────────────────────────────────────────┤
│  LIVE  ●  3 queries right now                   │
│  "How much does foreign aid cost per taxpayer?"  │
│  "Prison population cost 2024"                   │
│                                                  │
│  POPULAR THIS WEEK                               │
│  1. HS2 total projected cost → 4,203 queries    │
│  2. NHS agency staff spend → 1,847 queries      │
│                                                  │
│  DATA GAPS  (help us prioritise)                │
│  "Local council CEO pay" — 89 people asked      │
│  [vote] [vote] [vote]                           │
└──────────────────────────────────────────────────┘
```

### 6.2 Query Result Page (/f/[id])

```
┌──────────────────────────────────────────────────┐
│  nstate / uk / civil service headcount           │
│                                      [user analysis] │
│                                                  │
│  The UK civil service grew from 492,000          │
│  to 542,000 between 2010 and 2024.               │
│                                                  │
│  +10.2% · +50,000 people · +£Xbn pay bill       │
│                                                  │
│  [CHART — bar/line, labelled, accessible]        │
│                                                  │
│  ⚠ Figures are headcount not FTE.               │
│    Source: Cabinet Office Civil Service          │
│    Statistics, September 2024 release.           │
│                                                  │
│  [Share ↗]  [Download CSV]  [Embed chart]       │
│                                                  │
│  ─────────────────────────────────────────────  │
│  ▼ Show working                                 │
│    Source: Cabinet Office · OGL v3              │
│    Release date: 2024-09-26                     │
│    Query: SELECT ...                            │
│    Pipeline: uk-civil-service-1.2.0             │
│    Reproduce: nstate.org/reproduce/uk-2026-0042 │
└──────────────────────────────────────────────────┘
```

### 6.3 OG Image (auto-generated per result)

Generated server-side via `next/og` on every `/f/[id]` request:

```
┌──────────────────────────────────────┐
│ nstate                               │
│                                      │
│ UK civil service: +10.2% since 2010  │
│                                      │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓ 2024: 542,000     │
│ ▓▓▓▓▓▓▓▓▓▓▓▓▓▓   2010: 492,000     │
│                                      │
│ Source: Cabinet Office · OGL v3      │
│ nstate.org/f/uk-2026-0042            │
└──────────────────────────────────────┘
```

When someone shares `/f/[id]` on X/Bluesky/LinkedIn, this image appears in the preview natively. No screenshot. No friction.

### 6.4 Publication Status Labels

Every result and finding displays one of:

| Status | Label | Meaning |
|---|---|---|
| `user_analysis` | `user query` | User asked, agent answered — not reviewed |
| `automated_finding` | `agent finding` | Background agent detected — needs review |
| `reviewed_finding` | `verified` | Human approved — safe to cite |

### 6.5 Country Selector

Dropdown in nav: UK (active) → EU (coming) → Add your country →

When a country is added, it appears automatically from `countries/*/config.yaml`.

---

## 7. Background Agents

### 7.1 Types

| Agent | Trigger | Output |
|---|---|---|
| Release monitor | Cron: checks each source daily | Flags new data releases for ingestion |
| Anomaly detector | After each pipeline run | Flags values > 2σ from historical trend |
| Budget vs outturn | After PESA/OBR update | Compares plans vs actual spend |
| Benchmark comparator | Weekly | Cross-country comparison findings |
| Government announcement parser | On-demand / news trigger | Analyses official announcements against data |

### 7.2 Finding Lifecycle

```
Agent detects anomaly
  → creates draft finding (status: automated_finding)
  → queued for human review
  → admin reviews: approve / reject / needs-more-context
  → if approved: status → reviewed_finding
  → published to findings feed
  → social card generated
  → posted to X (initially: manual post; later: auto after track record)
```

---

## 8. Gap Detection

When a query returns no matching data:

1. Log: `{ question, interpreted_topic, country, timestamp }`
2. Fuzzy-match against existing gap log — deduplicate similar questions
3. Increment vote count for that gap
4. Show user: *"We don't have this data yet. X others have asked. [Vote to prioritise]"*
5. Notify admin when:
   - New gap first detected → webhook (immediate)
   - Gap reaches 10 votes → email digest
   - Gap reaches 50 votes → priority alert
6. Admin dashboard: gap queue sorted by votes → becomes the data roadmap

---

## 9. Infrastructure

### 9.1 VPS (nstate-vps1 — Hetzner CPX21)

```
Runs:
  - FastAPI query service (port 8000, behind nginx)
  - DuckDB data warehouse (file: /data/nstate.duckdb)
  - Parquet data files (/data/parquet/)
  - Background agent scheduler (cron / systemd)
  - Nginx (reverse proxy + SSL via Let's Encrypt)

Scale triggers:
  CPX21 → CPX31 (8GB): when queries > 100/hour sustained
  CPX31 → CPX41 (16GB): when data warehouse > 50GB
```

### 9.2 API Security

- Rate limiting: 30 queries/hour per IP (no login required)
- Query allowlist: read-only SQL only, table allowlist enforced
- No personal data stored: queries logged without IP after 24h
- CORS: nstate.org origin only
- API key: OpenRouter key stored in VPS env, never in repo

### 9.3 Frontend (Vercel)

- Next.js app deployed to Vercel
- Static pages (methodology, contribute) pre-built at deploy time
- Dynamic pages (query, findings) hit FastAPI on VPS via environment variable
- OG images generated server-side on Vercel edge
- Custom domain: nstate.org

### 9.4 Self-Hosting

Anyone can self-host the full stack:

```bash
git clone https://github.com/nstate-project/nstate
cd nstate
cp .env.example .env   # add OpenRouter key
docker compose up
# → full stack at localhost:3000
```

---

## 10. Multi-Country Expansion

### 10.1 Adding a Country

1. Create `countries/[code]/config.yaml` (fork TEMPLATE.yaml)
2. Write first pipeline in `data/[code]/pipelines/`
3. Add tables to DuckDB with `[code]_*` namespace
4. Submit PR — country appears in nav selector when merged

### 10.2 EU Chapter (Priority Phase 2)

Eurostat has a public REST API with comprehensive EU-wide data:
- Government expenditure by function (COFOG)
- Tax revenue by country
- Public debt and deficit
- Government employment

EU chapter makes every UK finding instantly comparable to 26 countries. High value, relatively low pipeline effort.

### 10.3 Cross-Country Queries (Phase 3)

```
User: "How does UK civil service headcount compare to Germany?"
→ agent queries uk_civil_service_* AND de_civil_service_*
→ normalises to common unit (per 1000 population)
→ comparative chart
→ caveats: definition differences stated explicitly
```

---

## 11. Social Distribution

### 11.1 Sharing Flow

1. Result page `/f/[id]` auto-generates OG image on first load
2. User clicks Share → copies URL (no screenshot needed)
3. Posted to X/Bluesky: preview card appears with chart + headline
4. Link back to full result page with working + citations

### 11.2 nstate Social Accounts

- X/Twitter: @nstate_org
- Bluesky: nstate.bsky.social

Initially: manually post reviewed findings.
Later (after track record proven): auto-post pre-approved finding templates.

### 11.3 Embed Widget (Phase 2)

```html
<iframe src="https://nstate.org/embed/f/uk-2026-0042"
        width="600" height="400" frameborder="0">
</iframe>
```

Journalists and bloggers can embed live charts in their articles. Chart updates if source data is revised.

---

## 12. Build Phases

### Phase 0 — Foundation (now)
- [x] Provision Hetzner VPS (nstate-vps1)
- [x] Scaffold Next.js app (replace Astro)
- [x] Scaffold FastAPI backend
- [x] DuckDB setup + first UK table schema
- [x] First UK pipeline: Cabinet Office civil service data
- [x] Basic query agent (intent parse → SQL → result)

### Phase 1 — Query MVP
- [x] Homepage with search box
- [x] Query result page + OG image generation
- [x] Public query feed (live + popular)
- [x] Gap detection + admin notification
- [x] 6 UK datasets loaded (14 loaded)
- [x] Rate limiting + IP-based abuse prevention

### Phase 2 — Findings + Social
- [ ] Background anomaly agents
- [x] Findings feed on homepage
- [ ] Finding review dashboard (admin)
- [ ] Social posting workflow
- [ ] EU chapter (Eurostat pipelines)
- [ ] Embed widget

### Phase 3 — Community + Scale
- [ ] Gap voting + prioritisation
- [ ] Community review (flag findings, add context)
- [ ] Second country chapter
- [ ] Cross-country comparisons
- [ ] Journalist citation export (academic format)
- [ ] API access (for developers)

---

## 13. Open Questions

1. Which UK datasets are loaded in Phase 0? (Recommended: Cabinet Office civil service as first proof of concept)
2. OpenRouter key — use existing key from api-registry or create nstate-specific?
3. Admin notification channel — email, webhook to phone, or Slack?
4. What is the VPS SSH key to use?
5. When does EU chapter start? (Recommend: alongside Phase 1, easy win)
6. Legal: should "user_analysis" results carry a disclaimer that they are unreviewed?

---

## Appendix: Technology Stack

| Layer | Technology | Why |
|---|---|---|
| Frontend | Next.js 15 (App Router) | SSR + static + API routes + OG images in one |
| Styling | Tailwind + custom CSS (Berkeley Mono) | Utility-first, contributors know it |
| Backend | FastAPI (Python) | Data science ecosystem, async, fast |
| Database | DuckDB | Zero-infra analytics, reads Parquet directly |
| Data format | Parquet | Open, compressed, columnar, DuckDB-native |
| LLM routing | OpenRouter | Multi-model, cost routing, no lock-in |
| Hosting | Vercel (FE) + Hetzner (BE) | Static resilience + cheap VPS |
| Data pipeline | Python scripts + cron | Simple, forkable, no Airflow overhead |
| OG images | next/og (Satori) | Server-rendered, no Puppeteer |
| Charts | Vega-Lite | Declarative, embeddable, accessible |
| Version control | GitHub (nstate-project/nstate) | Open source, PRs, Actions |
| Container | Docker Compose | One command self-host |
| Licence | CC BY 4.0 (data) + MIT (code) | Maximum reuse |
