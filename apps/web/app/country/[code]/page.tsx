import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';

const API = 'https://api.nstate.org';

export async function generateMetadata(
  { params }: { params: Promise<{ code: string }> }
): Promise<Metadata> {
  const { code } = await params;
  const ucode = code.toUpperCase();
  const data = await getGlobalStats(ucode);
  const name = data?.name ?? ucode;
  return {
    title: `${name} — nstate`,
    description: `${name} government finances and price levels from World Bank data.`,
  };
}

type FiscalStat = { value: number; year: number };
type GlobalStats = {
  country: string; name: string;
  fiscal: Record<string, FiscalStat>;
  debt_series: { year: number; value: number }[];
  price_level_pli: number | null; price_level_year: number | null; price_level_base: string;
  labour_tax_wedge_pct: number | null; labour_tax_wedge_year: number | null;
  corporate_tax_rate: number | null;
  personal_top_rate: number | null;
  vat_standard_rate: number | null;
  vat_reduced_rate: number | null;
};

async function getGlobalStats(ucode: string): Promise<GlobalStats | null> {
  try {
    const res = await fetch(`${API}/country/${ucode}/global-stats`, { next: { revalidate: 86400 } });
    return res.ok ? (res.json() as Promise<GlobalStats>) : null;
  } catch { return null; }
}

function fmt(n: number | undefined | null, decimals = 1): string {
  if (n == null) return '—';
  return new Intl.NumberFormat('en-GB', { maximumFractionDigits: decimals }).format(n);
}

function StatCard({ label, value, unit, year, direction }: {
  label: string; value: string; unit: string; year: number | null;
  direction?: 'good' | 'bad' | 'neutral';
}) {
  const colour = direction === 'good' ? 'var(--green)' : direction === 'bad' ? '#f87171' : 'var(--amber)';
  return (
    <div className="card" style={{ flex: '1 1 200px', minWidth: 0 }}>
      <div className="result-label" style={{ marginBottom: '0.5rem' }}>{label}</div>
      <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.4rem', marginBottom: '0.25rem' }}>
        <span style={{ fontSize: '2rem', fontWeight: 700, color: colour }}>{value}</span>
        <span style={{ color: 'var(--text-2)', fontSize: '0.9em' }}>{unit}</span>
      </div>
      {year && <div style={{ color: 'var(--text-3)', fontSize: '0.78em' }}>{year}</div>}
    </div>
  );
}

function FiscalSection({ stats }: { stats: GlobalStats }) {
  const f = stats.fiscal;
  const debt = f['debt_pct_gdp'];
  const exp = f['expenditure_pct_gdp'];
  const rev = f['revenue_pct_gdp'];
  const sur = f['surplus_pct_gdp'];
  if (!debt && !exp && !rev) return null;
  return (
    <section className="section">
      <div className="container">
        <h2>Government finances</h2>
        <p style={{ color: 'var(--text-2)', margin: '0.5rem 0 1.25rem', fontSize: '0.88em' }}>
          Central government data (World Bank WDI). Not directly comparable with EU Maastricht figures which use general government.
        </p>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {debt && (
            <StatCard label="Government debt" value={fmt(debt.value)} unit="% GDP" year={debt.year}
              direction={debt.value < 60 ? 'good' : debt.value > 100 ? 'bad' : 'neutral'} />
          )}
          {exp && (
            <StatCard label="Govt expenditure" value={fmt(exp.value)} unit="% GDP" year={exp.year} direction="neutral" />
          )}
          {rev && (
            <StatCard label="Govt revenue" value={fmt(rev.value)} unit="% GDP" year={rev.year} direction="neutral" />
          )}
          {sur && (
            <StatCard
              label={sur.value >= 0 ? 'Budget surplus' : 'Budget deficit'}
              value={fmt(Math.abs(sur.value))} unit="% GDP" year={sur.year}
              direction={sur.value >= 0 ? 'good' : 'neutral'} />
          )}
        </div>
      </div>
    </section>
  );
}

function PriceLevelSection({ stats }: { stats: GlobalStats }) {
  const pli = stats.price_level_pli;
  if (pli == null) return null;
  const cheaper = pli < 100;
  const diff = Math.abs(100 - pli).toFixed(1);
  return (
    <section className="section">
      <div className="container">
        <h2>Price level</h2>
        <p style={{ color: 'var(--text-2)', margin: '0.5rem 0 1.25rem' }}>
          {stats.name} is{' '}
          <strong style={{ color: cheaper ? 'var(--green)' : '#f87171' }}>
            {diff}% {cheaper ? 'cheaper' : 'more expensive'}
          </strong>{' '}
          than the USA overall ({stats.price_level_year}). Index: USA = 100.
        </p>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <StatCard label="Overall price level" value={pli.toFixed(1)} unit="(USA=100)"
            year={stats.price_level_year}
            direction={pli < 70 ? 'good' : pli > 130 ? 'bad' : 'neutral'} />
        </div>
        <p style={{ color: 'var(--text-3)', fontSize: '0.78em', marginTop: '0.75rem' }}>
          Source: World Bank WDI (PA.NUS.PPP / PA.NUS.FCRF × 100). GDP price level only.{' '}
          {stats.country && ['AT','BE','BG','CY','CZ','DE','DK','EE','EL','ES','FI','FR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','PT','RO','SE','SI','SK','NO','IS','CH','LI'].includes(stats.country) && (
            <>Detailed category-level price data (EU27=100) available on the <Link href={`/eu/${stats.country.toLowerCase()}`}>EU country page</Link>.</>
          )}
        </p>
      </div>
    </section>
  );
}

function TaxSection({ stats }: { stats: GlobalStats }) {
  const { corporate_tax_rate: corp, personal_top_rate: pit, vat_standard_rate: vat, labour_tax_wedge_pct: wedge, labour_tax_wedge_year: wedgeYr } = stats;
  if (!corp && !pit && !vat && !wedge) return null;
  return (
    <section className="section">
      <div className="container">
        <h2>Tax rates</h2>
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          {wedge != null && (
            <StatCard label="Labour tax wedge" value={fmt(wedge)} unit="% of labour cost"
              year={wedgeYr} direction={wedge < 30 ? 'good' : wedge > 40 ? 'bad' : 'neutral'} />
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
          Statutory rates 2024: OECD Taxing Wages / EC Taxation Trends. Labour wedge: Eurostat earn_nt_taxrate (EEA/EU countries only).
        </p>
      </div>
    </section>
  );
}

function DebtTable({ series, name }: { series: GlobalStats['debt_series']; name: string }) {
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

export default async function CountryPage(
  { params }: { params: Promise<{ code: string }> }
) {
  const { code } = await params;
  const ucode = code.toUpperCase();
  const stats = await getGlobalStats(ucode);
  if (!stats) notFound();

  const { name } = stats;
  const isEU27 = ['AT','BE','BG','CY','CZ','DE','DK','EE','EL','ES','FI','FR','HR','HU','IE','IT','LT','LU','LV','MT','NL','PL','PT','RO','SE','SI','SK'].includes(ucode);

  return (
    <>
      <div className="container page-header">
        <h1>{name}</h1>
        <p>
          Government finance and price level data from the{' '}
          <a href="https://databank.worldbank.org/source/world-development-indicators" rel="noopener noreferrer" target="_blank">
            World Bank WDI
          </a>.
        </p>
        {isEU27 && (
          <p style={{ marginTop: '0.5rem', fontSize: '0.88em', color: 'var(--text-2)' }}>
            EU member state — <Link href={`/eu/${code.toLowerCase()}`}>view detailed Eurostat data →</Link>
          </p>
        )}
        <div className="button-row" style={{ marginTop: '1rem' }}>
          <Link className="button" href={`/ask?q=${encodeURIComponent(`How does ${name}'s government debt compare to the G7 average?`)}`}>
            ask about {name} →
          </Link>
          <Link className="button button--secondary" href="/countries">← all countries</Link>
        </div>
      </div>
      <FiscalSection stats={stats} />
      <PriceLevelSection stats={stats} />
      <TaxSection stats={stats} />
      {stats.debt_series.length > 1 && <DebtTable series={stats.debt_series} name={name} />}
      <section className="section">
        <div className="container">
          <h2>Data sources</h2>
          <div className="table-wrap">
            <table>
              <thead><tr><th>Dataset</th><th>Source</th><th>Coverage</th></tr></thead>
              <tbody>
                <tr><td>Govt debt / expenditure / revenue / surplus</td><td>World Bank WDI (GC.* indicators)</td><td>2000–2024</td></tr>
                <tr><td>Price level index (USA=100)</td><td>World Bank WDI PPP/XR ratio</td><td>1990–2023</td></tr>
                <tr><td>Labour tax wedge</td><td>Eurostat earn_nt_taxrate</td><td>EEA/EU only</td></tr>
                <tr><td>Statutory tax rates</td><td>OECD / EC Taxation Trends 2024</td><td>EU+EFTA only</td></tr>
              </tbody>
            </table>
          </div>
        </div>
      </section>
    </>
  );
}
