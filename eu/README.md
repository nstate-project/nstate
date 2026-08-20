# nstate — European Union

> nstate audits EU member state government finances against stated objectives using Eurostat's open data. All 27 countries. Reproducible methods. No spin.

**Data source:** [Eurostat](https://ec.europa.eu/eurostat) — the EU's official statistics office. Free to reuse under the [Eurostat reuse policy](https://ec.europa.eu/eurostat/about-us/policies/copyright).

---

## Datasets loaded

| Dataset | Eurostat code | Coverage | Update |
|---|---|---|---|
| Government expenditure (% GDP) | `gov_10a_exp` | EU27 + aggregates, 1995–2024 | Annual |
| Government deficit (% GDP) | `gov_10dd_edpt1` (B9) | EU27, 1995–2024 | Annual |
| Government debt (% GDP) | `gov_10dd_edpt1` (GD) | EU27, 1995–2024 | Annual |
| Tax revenue (% GDP) | `gov_10a_taxag` | EU27, 1995–2024 | Annual |
| Public sector employment | `nama_10_a64_e` (NACE O-Q) | EU27, 1995–2024 | Annual |

---

## Country chapters

Each country chapter audits national government spending against stated objectives. Contribute a chapter by following [CONTRIBUTING.md](../CONTRIBUTING.md).

| Country | Code | Status | Chapter |
|---|---|---|---|
| Germany | DE | Seeking contributors | [de/](../de/) |
| France | FR | Seeking contributors | [fr/](../fr/) |
| Italy | IT | Seeking contributors | [it/](../it/) |
| Spain | ES | Seeking contributors | [es/](../es/) |
| Poland | PL | Seeking contributors | [pl/](../pl/) |
| Netherlands | NL | Seeking contributors | [nl/](../nl/) |
| Belgium | BE | Seeking contributors | [be/](../be/) |
| Sweden | SE | Seeking contributors | [se/](../se/) |
| Austria | AT | Seeking contributors | [at/](../at/) |
| Denmark | DK | Seeking contributors | [dk/](../dk/) |
| Finland | FI | Seeking contributors | [fi/](../fi/) |
| Ireland | IE | Seeking contributors | [ie/](../ie/) |
| Portugal | PT | Seeking contributors | [pt/](../pt/) |
| Czech Republic | CZ | Seeking contributors | [cz/](../cz/) |
| Romania | RO | Seeking contributors | [ro/](../ro/) |
| Hungary | HU | Seeking contributors | [hu/](../hu/) |
| Slovakia | SK | Seeking contributors | [sk/](../sk/) |
| Bulgaria | BG | Seeking contributors | [bg/](../bg/) |
| Croatia | HR | Seeking contributors | [hr/](../hr/) |
| Lithuania | LT | Seeking contributors | [lt/](../lt/) |
| Latvia | LV | Seeking contributors | [lv/](../lv/) |
| Slovenia | SI | Seeking contributors | [si/](../si/) |
| Estonia | EE | Seeking contributors | [ee/](../ee/) |
| Cyprus | CY | Seeking contributors | [cy/](../cy/) |
| Luxembourg | LU | Seeking contributors | [lu/](../lu/) |
| Malta | MT | Seeking contributors | [mt/](../mt/) |
| Greece | EL | Seeking contributors | [el/](../el/) |

---

## How to start a country chapter

1. Read [COUNTRY-TEMPLATE.md](../COUNTRY-TEMPLATE.md)
2. Copy it to `{country-code}/README.md` (e.g. `de/README.md`)
3. Map your country's key data sources
4. Open a PR — your chapter appears on nstate.org automatically

Priority first-wave datasets for any EU country:
- National statistics office (e.g. Destatis for Germany, INSEE for France)
- Tax authority data
- Public expenditure statistics
- Social welfare spending
- Public sector wage data

The Eurostat EU-wide data is already loaded — country chapters add national detail and scorecards that go deeper than EU aggregates.
