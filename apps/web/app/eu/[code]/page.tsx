import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';

const EU27: Record<string, string> = {
  AT: 'Austria', BE: 'Belgium', BG: 'Bulgaria', CY: 'Cyprus',
  CZ: 'Czechia', DE: 'Germany', DK: 'Denmark', EE: 'Estonia',
  EL: 'Greece', ES: 'Spain', FI: 'Finland', FR: 'France',
  HR: 'Croatia', HU: 'Hungary', IE: 'Ireland', IT: 'Italy',
  LT: 'Lithuania', LU: 'Luxembourg', LV: 'Latvia', MT: 'Malta',
  NL: 'Netherlands', PL: 'Poland', PT: 'Portugal', RO: 'Romania',
  SE: 'Sweden', SI: 'Slovenia', SK: 'Slovakia',
};

const API = 'https://api.nstate.org';

export async function generateStaticParams() {
  return Object.keys(EU27).map((code) => ({ code: code.toLowerCase() }));
}

export async function generateMetadata(
  { params }: { params: Promise<{ code: string }> }
): Promise<Metadata> {
  const { code } = await params;
  const name = EU27[code.toUpperCase()] ?? code.toUpperCase();
  return {
    title: `${name} — nstate`,
    description: `${name} government finance data: spending, debt, tax revenue and public employment from Eurostat.`,
  };
}

type LatestStat = { value: number; year: number };
type CountryStats = {
  country: string; name: string;
  latest: {
    expenditure_pct_gdp?: LatestStat;
    debt_pct_gdp?: LatestStat;
    deficit_pct_gdp?: LatestStat;
  };
  eu27_avg: Record<string, number>;
  eu27_comparison_year: number;
  debt_series: { year: number; value: number }[];
  tax_revenue_pct_gdp: number | null; tax_revenue_year: number | null;
  public_employment_thousands: number | null; public_employment_year: number | null;
  tax_breakdown: Record<string, { value: number; year: number }>;
  labour_tax_wedge_pct: number | null; labour_tax_wedge_year: number | null;
  corporate_tax_rate: number | null;
  personal_top_rate: number | null;
  vat_standard_rate: number | null;
  vat_reduced_rate: number | null;
};

type PriceCategory = { pli: number; year: number };
type CountryPrices = {
  country: string; name: string;
  price_levels: Record<string, PriceCategory>;
};

async function getStats(ucode: string): Promise<CountryStats | null> {
  try {
    const res = await fetch(`${API}/country/${ucode}/stats`, { next: { revalidate: 3600 } });
    return res.ok ? (res.json() as Promise<CountryStats>) : null;
  } catch { return null; }
}

async function getPrices(ucode: string): Promise<CountryPrices | null> {
  try {
    const res = await fetch(`${API}/country/${ucode}/prices`, { next: { revalidate: 3600 } });
    return res.ok ? (res.json() as Promise<CountryPrices>) : null;
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
  const debtPeak = stats.debt_series.reduce(
    (m, r) => r.value > m.value ? r : m, { year: 0, value: 0 }
  );
  return (
    <section className="section">
      <div className="container">
        <h2>Headline stats</h2>
        {l.debt_pct_gdp && debtPeak.year > 0 && debtPeak.value > l.debt_pct_gdp.value + 5 && (
          <p style={{ color: 'var(--text-2)', margin: '0.5rem 0 1.25rem' }}>
            Debt peaked at{' '}
            <strong style={{ color: 'var(--amber)' }}>{fmt(debtPeak.value)}% GDP</strong>{' '}
            in {debtPeak.year} — now{' '}
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

function TaxSection({ stats, name }: { stats: CountryStats; name: string }) {
  const { corporate_tax_rate: corp, personal_top_rate: pit, vat_standard_rate: vat,
          labour_tax_wedge_pct: wedge, labour_tax_wedge_year: wedgeYr } = stats;
  if (!corp && !pit && !vat && !wedge) return null;
  return (
    <section className="section">
      <div className="container">
        <h2>Tax rates</h2>
        <p style={{ color: 'var(--text-2)', margin: '0.5rem 0 1.25rem' }}>
          What {name} takes — statutory rates and effective burden on workers.
        </p>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {wedge != null && (
            <StatCard label="Labour tax wedge" value={fmt(wedge)} unit="% of labour cost"
              year={wedgeYr!} direction={wedge < 30 ? 'good' : wedge > 40 ? 'bad' : 'neutral'} />
          )}
          {pit != null && (
            <StatCard label="Top income tax rate" value={fmt(pit, 0)} unit="%" year={2024}
              direction={pit > 50 ? 'bad' : pit < 20 ? 'good' : 'neutral'} />
          )}
          {corp != null && (
            <StatCard label="Corporate tax rate" value={fmt(corp, 1)} unit="%" year={2024}
              direction={corp < 15 ? 'good' : corp > 28 ? 'bad' : 'neutral'} />
          )}
          {vat != null && (
            <StatCard label="Standard VAT rate" value={fmt(vat, 0)} unit="%" year={2024}
              direction={vat > 24 ? 'bad' : vat < 18 ? 'good' : 'neutral'} />
          )}
        </div>
        <p style={{ color: 'var(--text-3)', fontSize: '0.78em', marginTop: '1rem' }}>
          Labour tax wedge: effective % of gross labour cost (salary + employer contributions) going to income tax
          and social contributions for a single person at average wage. Source: Eurostat earn_nt_taxrate.
          Statutory rates: OECD Taxing Wages 2024 / EC Taxation Trends 2024.
        </p>
      </div>
    </section>
  );
}

const PRICE_LABELS: Record<string, string> = {
  GDP: 'Overall price level',
  A0101: 'Food & non-alcoholic drinks',
  A0102: 'Alcohol & tobacco',
  A0103: 'Clothing & footwear',
  A0104: 'Housing, utilities & energy',
  A0105: 'Household furnishings',
  A0106: 'Health',
  A0107: 'Transport',
  A0108: 'Communication',
  A0109: 'Recreation & culture',
  A0110: 'Education',
  A0111: 'Restaurants & hotels',
  A0112: 'Miscellaneous',
};
const PRICE_ORDER = ['GDP','A0101','A0104','A0111','A0107','A0106','A0110','A0103','A0109','A0102','A0105','A0108','A0112'];

function PricesSection({ prices, name }: { prices: CountryPrices; name: string }) {
  const pl = prices.price_levels;
  const gdp = pl['GDP'];
  if (!gdp) return null;
  const cheaper = gdp.pli < 100;
  const diff = Math.abs(100 - gdp.pli).toFixed(1);
  return (
    <section className="section">
      <div className="container">
        <h2>Comparative prices</h2>
        <p style={{ color: 'var(--text-2)', margin: '0.5rem 0 1.25rem' }}>
          {name} is{' '}
          <strong style={{ color: cheaper ? 'var(--green)' : '#f87171' }}>
            {diff}% {cheaper ? 'cheaper' : 'more expensive'}
          </strong>{' '}
          than the EU average overall ({gdp.year}). Index: EU27 = 100.
        </p>
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Category</th>
                <th style={{ textAlign: 'right' }}>Price index</th>
                <th style={{ textAlign: 'right' }}>vs EU avg</th>
              </tr>
            </thead>
            <tbody>
              {PRICE_ORDER.map((cat) => {
                const entry = pl[cat];
                if (!entry) return null;
                const label = PRICE_LABELS[cat] ?? cat;
                const vs = entry.pli - 100;
                const cc = vs < 0 ? 'var(--green)' : vs > 0 ? '#f87171' : 'var(--text-3)';
                return (
                  <tr key={cat}>
                    <td>{label}</td>
                    <td style={{ textAlign: 'right', fontVariantNumeric: 'tabular-nums' }}>
                      {entry.pli.toFixed(1)}
                    </td>
                    <td style={{ textAlign: 'right', fontVariantNumeric: 'tabular-nums', color: cc }}>
                      {vs > 0 ? '+' : ''}{vs.toFixed(1)}%
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <p style={{ color: 'var(--text-3)', fontSize: '0.78em', marginTop: '0.75rem' }}>
          Source: Eurostat prc_ppp_ind. EU27_2020 = 100. Green = cheaper than EU average.
        </p>
      </div>
    </section>
  );
}

function QuestionsSection({ name }: { name: string }) {
  const qs = [
    `How has ${name}'s government debt changed since 2010?`,
    `How does ${name}'s tax burden compare to Germany and France?`,
    `What is ${name}'s government spending as a percentage of GDP?`,
    `How does ${name}'s public sector employment compare to the EU average?`,
  ];
  return (
    <section className="section">
      <div className="container">
        <h2>Ask questions about {name}</h2>
        <p style={{ color: 'var(--text-2)', marginBottom: '1rem' }}>
          The query agent compares {name} against other EU countries using Eurostat data.
        </p>
        <div className="card-list">
          {qs.map((q) => (
            <a className="card" href={`/ask?q=${encodeURIComponent(q)}`} key={q}>
              <p style={{ fontSize: '0.9em' }}>{q}</p>
            </a>
          ))}
        </div>
      </div>
    </section>
  );
}

function DataSources() {
  return (
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
              <tr><td>Tax breakdown (VAT, income, social)</td><td>Eurostat gov_10a_taxag</td><td>2000–2023</td></tr>
              <tr><td>Labour tax wedge</td><td>Eurostat earn_nt_taxrate</td><td>2000–2023</td></tr>
              <tr><td>Statutory tax rates (income, corporate, VAT)</td><td>OECD / EC Taxation Trends 2024</td><td>2024</td></tr>
              <tr><td>Comparative price levels (13 categories)</td><td>Eurostat prc_ppp_ind</td><td>1995–2024</td></tr>
            </tbody>
          </table>
        </div>
        <div style={{ marginTop: '1.5rem' }}>
          <Link className="button button--secondary" href="/eu">← all EU countries</Link>
        </div>
      </div>
    </section>
  );
}

export default async function CountryChapterPage(
  { params }: { params: Promise<{ code: string }> }
) {
  const { code } = await params;
  const ucode = code.toUpperCase();
  const name = EU27[ucode];
  if (!name) notFound();

  const [stats, prices] = await Promise.all([getStats(ucode), getPrices(ucode)]);

  return (
    <>
      <div className="container page-header">
        <h1>{name}</h1>
        <p>
          Government finance and cost-of-living data from{' '}
          <a href="https://ec.europa.eu/eurostat" rel="noopener noreferrer" target="_blank">Eurostat</a>
          {' '}— spending, debt, tax, and comparative prices.
        </p>
        <div className="button-row" style={{ marginTop: '1rem' }}>
          <Link className="button" href={`/ask?q=${encodeURIComponent(`How does ${name}'s government debt compare to the EU average?`)}`}>
            ask about {name} →
          </Link>
          <a className="button button--secondary"
            href={`https://github.com/nstate-project/nstate/blob/main/${code}/README.md`}
            rel="noopener noreferrer" target="_blank">contribute data ↗</a>
        </div>
      </div>
      {stats && <HeadlineStats stats={stats} />}
      {stats && <TaxSection stats={stats} name={name} />}
      {prices && <PricesSection prices={prices} name={name} />}
      {stats && <DebtTable series={stats.debt_series} />}
      <QuestionsSection name={name} />
      <DataSources />
    </>
  );
}
