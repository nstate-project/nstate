import type { Metadata } from 'next';
import Link from 'next/link';
import CountriesClient from '../../components/CountriesClient';

export const metadata: Metadata = {
  title: 'Countries — nstate',
  description: 'Government finance data for countries worldwide. Powered by World Bank WDI.',
};

export const revalidate = 86400;

const API = 'https://api.nstate.org';

export type Country = {
  country: string;
  name: string;
  region: string;
  income_group: string;
};

async function getCountries(): Promise<Country[]> {
  try {
    const res = await fetch(`${API}/countries/list`, { next: { revalidate: 86400 } });
    if (!res.ok) return [];
    const d = (await res.json()) as { countries: Country[] };
    return d.countries ?? [];
  } catch {
    return [];
  }
}

export default async function CountriesPage() {
  const countries = await getCountries();

  return (
    <>
      <div className="container page-header">
        <h1>Countries</h1>
        <p>
          Government finance data for {countries.length} countries from the{' '}
          <a
            href="https://databank.worldbank.org/source/world-development-indicators"
            rel="noopener noreferrer"
            target="_blank"
          >
            World Bank WDI
          </a>
          . Debt, expenditure, revenue, and comparative price levels.
        </p>
        <p style={{ marginTop: '0.5rem', fontSize: '0.88em', color: 'var(--text-2)' }}>
          EU member states: <Link href="/eu">detailed Eurostat data →</Link>
        </p>
      </div>

      <CountriesClient countries={countries} />
    </>
  );
}
