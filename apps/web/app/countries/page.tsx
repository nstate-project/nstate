import type { Metadata } from 'next';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Countries — nstate',
  description: 'Government finance data for countries worldwide. Powered by World Bank WDI.',
};

export const revalidate = 86400;

const API = 'https://api.nstate.org';

type Country = { country: string; name: string; region: string; income_group: string };

const REGION_ORDER = [
  'Europe & Central Asia',
  'North America',
  'East Asia & Pacific',
  'Latin America & Caribbean',
  'Middle East & North Africa',
  'South Asia',
  'Sub-Saharan Africa',
];

async function getCountries(): Promise<Country[]> {
  try {
    const res = await fetch(`${API}/countries/list`, { next: { revalidate: 86400 } });
    if (!res.ok) return [];
    const d = (await res.json()) as { countries: Country[] };
    return d.countries ?? [];
  } catch { return []; }
}

export default async function CountriesPage() {
  const countries = await getCountries();
  const byRegion: Record<string, Country[]> = {};
  for (const c of countries) {
    const region = c.region || 'Other';
    (byRegion[region] ??= []).push(c);
  }
  const regions = REGION_ORDER.filter((r) => byRegion[r]).concat(
    Object.keys(byRegion).filter((r) => !REGION_ORDER.includes(r))
  );

  return (
    <>
      <div className="container page-header">
        <h1>Countries</h1>
        <p>
          Government finance data for {countries.length} countries from the{' '}
          <a href="https://databank.worldbank.org/source/world-development-indicators"
            rel="noopener noreferrer" target="_blank">World Bank WDI</a>.
          Debt, expenditure, revenue, and comparative price levels.
        </p>
        <p style={{ marginTop: '0.5rem', fontSize: '0.88em', color: 'var(--text-2)' }}>
          EU member states: <Link href="/eu">detailed Eurostat data →</Link>
        </p>
      </div>

      {regions.map((region) => (
        <section className="section" key={region}>
          <div className="container">
            <h2>{region}</h2>
            <div className="card-list" style={{ marginTop: '1rem' }}>
              {(byRegion[region] ?? []).map((c) => (
                <Link
                  key={c.country}
                  href={`/country/${c.country.toLowerCase()}`}
                  className="card"
                  style={{ flex: '1 1 160px', minWidth: 0 }}
                >
                  <strong style={{ fontSize: '1em' }}>{c.name}</strong>
                  <div style={{ color: 'var(--text-3)', fontSize: '0.78em', marginTop: '0.25rem' }}>
                    {c.income_group}
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      ))}

      {countries.length === 0 && (
        <div className="container">
          <p style={{ color: 'var(--text-2)' }}>Loading country data…</p>
        </div>
      )}
    </>
  );
}
