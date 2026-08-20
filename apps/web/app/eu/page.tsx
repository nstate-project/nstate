import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = { title: 'EU chapter' };

const DATASETS = [
  { label: 'Government expenditure (% GDP)', code: 'gov_10a_exp', table: 'eu_government_finance' },
  { label: 'Government deficit (% GDP)', code: 'gov_10dd_edpt1 (B9)', table: 'eu_government_finance' },
  { label: 'Government debt (% GDP)', code: 'gov_10dd_edpt1 (GD)', table: 'eu_government_finance' },
  { label: 'Tax revenue (% GDP)', code: 'gov_10a_taxag', table: 'eu_tax_revenue' },
  { label: 'Public sector employment', code: 'nama_10_a64_e (O-Q)', table: 'eu_public_employment' },
];

const COUNTRIES = [
  { code: 'de', name: 'Germany' }, { code: 'fr', name: 'France' },
  { code: 'it', name: 'Italy' }, { code: 'es', name: 'Spain' },
  { code: 'pl', name: 'Poland' }, { code: 'nl', name: 'Netherlands' },
  { code: 'be', name: 'Belgium' }, { code: 'se', name: 'Sweden' },
  { code: 'at', name: 'Austria' }, { code: 'dk', name: 'Denmark' },
  { code: 'fi', name: 'Finland' }, { code: 'ie', name: 'Ireland' },
  { code: 'pt', name: 'Portugal' }, { code: 'cz', name: 'Czech Republic' },
  { code: 'ro', name: 'Romania' }, { code: 'hu', name: 'Hungary' },
  { code: 'sk', name: 'Slovakia' }, { code: 'bg', name: 'Bulgaria' },
  { code: 'hr', name: 'Croatia' }, { code: 'lt', name: 'Lithuania' },
  { code: 'lv', name: 'Latvia' }, { code: 'si', name: 'Slovenia' },
  { code: 'ee', name: 'Estonia' }, { code: 'cy', name: 'Cyprus' },
  { code: 'lu', name: 'Luxembourg' }, { code: 'mt', name: 'Malta' },
  { code: 'el', name: 'Greece' },
];

export default function EuPage() {
  return (
    <>
      <div className="container page-header">
        <h1>EU chapter</h1>
        <p>
          EU-wide government finance data for all 27 member states, sourced from{' '}
          <a href="https://ec.europa.eu/eurostat" rel="noopener noreferrer" target="_blank">
            Eurostat
          </a>
          . Ask the data or contribute a country chapter.
        </p>
        <div className="button-row" style={{ marginTop: '1rem' }}>
          <Link className="button" href="/ask">ask the EU data →</Link>
          <a
            className="button button--secondary"
            href="https://github.com/nstate-project/nstate/blob/main/eu/README.md"
            rel="noopener noreferrer"
            target="_blank"
          >
            contribute a chapter ↗
          </a>
        </div>
      </div>

      <section className="section">
        <div className="container">
          <h2>Datasets loaded</h2>
          <div className="table-wrap" style={{ marginTop: '1rem' }}>
            <table>
              <thead>
                <tr><th>Dataset</th><th>Eurostat code</th><th>Coverage</th></tr>
              </thead>
              <tbody>
                {DATASETS.map((d) => (
                  <tr key={d.code}>
                    <td>{d.label}</td>
                    <td><code>{d.code}</code></td>
                    <td>EU27 · 1995–2024 · annual</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </section>

      <section className="section">
        <div className="container">
          <h2>Country chapters</h2>
          <p style={{ color: 'var(--text-2)', marginBottom: '1rem' }}>
            All 27 chapters are open for contribution. EU-wide Eurostat data is loaded for every country — chapters add national detail and scorecards.
          </p>
          <div className="card-list">
            {COUNTRIES.map((c) => (
              <a
                className="card"
                href={`https://github.com/nstate-project/nstate/blob/main/${c.code}/README.md`}
                key={c.code}
                rel="noopener noreferrer"
                target="_blank"
              >
                <p style={{ marginBottom: '0.25rem' }}>{c.name}</p>
                <div className="card__meta">
                  <span className="badge">{c.code.toUpperCase()}</span>
                  <span className="badge" style={{ color: 'var(--amber)' }}>seeking contributors</span>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>
    </>
  );
}
