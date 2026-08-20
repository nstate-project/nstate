import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Portugal — nstate',
  description: 'Portugal government finance: spending, debt, tax revenue and public employment from Eurostat.',
};

const API = 'https://api.nstate.org';

type LatestStat = { value: number; year: number };
type CountryStats = {
  country: string;
  name: string;
  latest: {
    expenditure_pct_gdp?: LatestStat;
    debt_pct_gdp?: LatestStat;
    deficit_pct_gdp?: LatestStat;
  };
  eu27_avg: Record<string, number>;
  eu27_comparison_year: number;
  debt_series: { year: number; value: number }[];
  tax_revenue_pct_gdp: number | null;
  tax_revenue_year: number | null;
  public_employment_thousands: number | null;
  public_employment_year: number | null;
};

async function getStats(): Promise<CountryStats | null> {
  try {
    const res = await fetch(`${API}/country/PT/stats`, { next: { revalidate: 3600 } });
    return res.ok ? (res.json() as Promise<CountryStats>) : null;
  } catch { return null; }
}

function fmt(n: number | undefined | null, decimals = 1): string {
  if (n == null) return '—';
  return new Intl.NumberFormat('en-GB', { maximumFractionDigits: decimals }).format(n);
}

type StatCardProps = {
  label: string; value: string; unit: string; year: number;
  vs?: string; vsLabel?: string; direction?: 'good' | 'bad' | 'neutral';
};
function StatCard({ label, value, unit, year, vs, vsLabel, direction }: StatCardProps) {
  const colour = direction === 'good' ? 'var(--green)' : direction === 'bad' ? '#f87171' : 'var(--amber)';
  return (
    <div className="card" style={{ flex: '1 1 200px', minWidth: 0 }}>
      <div className="result-label" style={{ marginBottom: '0.5rem' }}>{label}</div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.4rem', marginBottom: '0.25rem' }}>
        <span style={{ fontSize: '2rem', fontWeight: 700, color: colour }}>{value}</span>
        <span style={{ color: 'var(--text-2)', fontSize: '0.9em' }}>{unit}</span>
      </div>
      <div style={{ color: 'var(--text-3)', fontSize: '0.78em' }}>{year}</div>
      {vs && (
        <div style={{ color: 'var(--text-2)', fontSize: '0.8em', marginTop: '0.4rem' }}>
          EU27 avg: {vs}{unit}{vsLabel && <span style={{ color: 'var(--text-3)' }}> ({vsLabel})</span>}
        </div>
      )}
    </div>
  );
}

function HeadlineStats({ stats }: { stats: CountryStats }) {
  const { latest: l, eu27_avg: eu, eu27_comparison_year: yr } = stats;
  const cmpYr = yr ? String(yr) : undefined;
  const debtPeak = stats.debt_series.reduce((m, r) => r.value > m.value ? r : m, { year: 0, value: 0 });
  return (
    <section className="section">
      <div className="container">
        <h2>Headline stats</h2>
        {l.debt_pct_gdp && debtPeak.year > 0 && (
          <p style={{ color: 'var(--text-2)', margin: '0.5rem 0 1.25rem' }}>
            Debt peaked at{' '}
            <strong style={{ color: 'var(--amber)' }}>{fmt(debtPeak.value)}% GDP</strong>{' '}
            in {debtPeak.year} during the IMF bailout era — now{' '}
            <strong style={{ color: 'var(--green)' }}>{fmt(l.debt_pct_gdp.value)}%</strong>.
          </p>
        )}
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {l.debt_pct_gdp && (
            <StatCard label="Government debt" value={fmt(l.debt_pct_gdp.value)} unit="% GDP"
              year={l.debt_pct_gdp.year} vs={eu.debt_pct_gdp != null ? fmt(eu.debt_pct_gdp) : undefined}
              vsLabel={cmpYr} direction={l.debt_pct_gdp.value < (eu.debt_pct_gdp ?? 100) ? 'good' : 'bad'} />
          )}
          {l.expenditure_pct_gdp && (
            <StatCard label="Govt expenditure" value={fmt(l.expenditure_pct_gdp.value)} unit="% GDP"
              year={l.expenditure_pct_gdp.year}
              vs={eu.expenditure_pct_gdp != null ? fmt(eu.expenditure_pct_gdp) : undefined}
              vsLabel={cmpYr} direction="neutral" />
          )}
          {l.deficit_pct_gdp && (
            <StatCard
              label={l.deficit_pct_gdp.value >= 0 ? 'Budget surplus' : 'Budget deficit'}
              value={fmt(Math.abs(l.deficit_pct_gdp.value))} unit="% GDP"
              year={l.deficit_pct_gdp.year}
              vs={eu.deficit_pct_gdp != null ? fmt(Math.abs(eu.deficit_pct_gdp)) : undefined}
              vsLabel={cmpYr} direction={l.deficit_pct_gdp.value >= 0 ? 'good' : 'neutral'} />
          )}
          {stats.tax_revenue_pct_gdp != null && (
            <StatCard label="Tax revenue" value={fmt(stats.tax_revenue_pct_gdp)} unit="% GDP"
              year={stats.tax_revenue_year!} direction="neutral" />
          )}
          {stats.public_employment_thousands != null && (
            <StatCard label="Public sector jobs" value={fmt(stats.public_employment_thousands, 0)}
              unit="k" year={stats.public_employment_year!} direction="neutral" />
          )}
        </div>
      </div>
    </section>
  );
}

function DebtTable({ series }: { series: CountryStats['debt_series'] }) {
  if (series.length < 2) return null;
  const rows = series.slice(-15);
  return (
    <section className="section">
      <div className="container">
        <h2>Government debt since {rows[0].year}</h2>
        <div className="table-wrap" style={{ marginTop: '1rem' }}>
          <table>
            <thead>
              <tr>
                <th>Year</th>
                <th style={{ textAlign: 'right' }}>Debt (% GDP)</th>
                <th style={{ textAlign: 'right' }}>Change</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r, i) => {
                const change = i > 0 ? r.value - rows[i - 1].value : null;
                const cc = change == null ? 'var(--text-3)' : change < 0 ? 'var(--green)' : '#f87171';
                return (
                  <tr key={r.year}>
                    <td>{r.year}</td>
                    <td style={{ textAlign: 'right', fontVariantNumeric: 'tabular-nums' }}>{fmt(r.value)}</td>
                    <td style={{ textAlign: 'right', fontVariantNumeric: 'tabular-nums', color: cc }}>
                      {change == null ? '—' : `${change > 0 ? '+' : ''}${fmt(change)}`}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </section>
  );
}

const QUESTIONS = [
  "How has Portugal's government debt changed since 2011?",
  "How does Portugal's tax burden compare to Germany and France?",
  "What is Portugal's public sector employment compared to the EU average?",
  "How does Portugal's government spending compare to Spain?",
];

function QuestionsAndSources() {
  return (
    <>
      <section className="section">
        <div className="container">
          <h2>Ask questions about Portugal</h2>
          <p style={{ color: 'var(--text-2)', marginBottom: '1rem' }}>
            The query agent compares Portugal against other EU countries using Eurostat data.
          </p>
          <div className="card-list">
            {QUESTIONS.map((q) => (
              <a className="card" href={`/ask?q=${encodeURIComponent(q)}`} key={q}>
                <p style={{ fontSize: '0.9em' }}>{q}</p>
              </a>
            ))}
          </div>
        </div>
      </section>
      <section className="section">
        <div className="container">
          <h2>Data sources</h2>
          <div className="table-wrap">
            <table>
              <thead><tr><th>Dataset</th><th>Source</th><th>Coverage</th></tr></thead>
              <tbody>
                <tr><td>Govt expenditure / debt / deficit</td><td>Eurostat gov_10dd_edpt1</td><td>1995–2025</td></tr>
                <tr><td>Tax revenue</td><td>Eurostat gov_10a_taxag</td><td>1995–2025</td></tr>
                <tr><td>Public employment (NACE O-Q)</td><td>Eurostat nama_10_a64_e</td><td>1995–2024</td></tr>
                <tr>
                  <td>National detail (labour, housing, industry)</td>
                  <td><a href="https://www.ine.pt" rel="noopener noreferrer" target="_blank">INE ↗</a></td>
                  <td><span style={{ color: 'var(--amber)' }}>open for contribution</span></td>
                </tr>
              </tbody>
            </table>
          </div>
          <div style={{ marginTop: '1.5rem' }}>
            <Link className="button button--secondary" href="/eu">← all EU countries</Link>
          </div>
        </div>
      </section>
    </>
  );
}

export default async function PortugalPage() {
  const stats = await getStats();
  return (
    <>
      <div className="container page-header">
        <h1>Portugal</h1>
        <p>
          Government finance data from{' '}
          <a href="https://ec.europa.eu/eurostat" rel="noopener noreferrer" target="_blank">Eurostat</a>
          {' '}— spending, debt, tax revenue, and public employment.{' '}
          <a href="https://www.ine.pt" rel="noopener noreferrer" target="_blank">INE</a>{' '}
          national-detail pipelines are open for contribution.
        </p>
        <div className="button-row" style={{ marginTop: '1rem' }}>
          <Link className="button" href="/ask">ask about Portugal →</Link>
          <a className="button button--secondary"
            href="https://github.com/nstate-project/nstate/blob/main/pt/README.md"
            rel="noopener noreferrer" target="_blank">contribute data ↗</a>
        </div>
      </div>
      {stats && <HeadlineStats stats={stats} />}
      {stats && <DebtTable series={stats.debt_series} />}
      <QuestionsAndSources />
    </>
  );
}
