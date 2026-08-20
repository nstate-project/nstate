'use client';

import Link from 'next/link';
import { useMemo, useState } from 'react';
import type { Country } from '../app/countries/page';
import s from './CountriesClient.module.css';

const REGION_ORDER = [
  'Europe & Central Asia',
  'North America',
  'East Asia & Pacific',
  'Latin America & Caribbean',
  'Middle East & North Africa',
  'South Asia',
  'Sub-Saharan Africa',
];

const INCOME_ORDER = [
  'High income',
  'Upper middle income',
  'Lower middle income',
  'Low income',
];

function filterCountries(countries: Country[], search: string, region: string, income: string) {
  const q = search.toLowerCase().trim();
  return countries.filter(
    (c) =>
      (!q || c.name.toLowerCase().includes(q) || c.country.toLowerCase().includes(q)) &&
      (!region || c.region === region) &&
      (!income || c.income_group === income)
  );
}

function groupByRegion(countries: Country[]): Record<string, Country[]> {
  const map: Record<string, Country[]> = {};
  for (const c of countries) (map[c.region || 'Other'] ??= []).push(c);
  return map;
}

function visibleRegionKeys(byRegion: Record<string, Country[]>, active: string): string[] {
  if (active) return byRegion[active] ? [active] : [];
  return REGION_ORDER.filter((r) => byRegion[r]).concat(
    Object.keys(byRegion).filter((r) => !REGION_ORDER.includes(r))
  );
}

function Pills({ label, options, active, onSelect }: {
  label: string; options: string[]; active: string; onSelect: (v: string) => void;
}) {
  return (
    <div className={s.filterPills}>
      <span className={s.filterPillsLabel}>{label}:</span>
      <button className={`${s.pill}${!active ? ` ${s.pillActive}` : ''}`} onClick={() => onSelect('')} type="button">All</button>
      {options.map((o) => (
        <button
          className={`${s.pill}${active === o ? ` ${s.pillActive}` : ''}`}
          key={o}
          onClick={() => onSelect(active === o ? '' : o)}
          type="button"
        >{o}</button>
      ))}
    </div>
  );
}

function CountrySection({ region, items }: { region: string; items: Country[] }) {
  return (
    <section className="section">
      <div className="container">
        <h2>{region}</h2>
        <div className="card-list" style={{ marginTop: '1rem' }}>
          {items.map((c) => (
            <Link className="card" href={`/country/${c.country.toLowerCase()}`} key={c.country}
              style={{ flex: '1 1 160px', minWidth: 0 }}>
              <strong style={{ fontSize: '1em' }}>{c.name}</strong>
              <div style={{ color: 'var(--text-3)', fontSize: '0.78em', marginTop: '0.25rem' }}>{c.income_group}</div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}

export default function CountriesClient({ countries }: { countries: Country[] }) {
  const [search, setSearch] = useState('');
  const [region, setRegion] = useState('');
  const [income, setIncome] = useState('');

  const regions = useMemo(
    () => REGION_ORDER.filter((r) => countries.some((c) => c.region === r)),
    [countries]
  );
  const incomeGroups = useMemo(
    () => INCOME_ORDER.filter((g) => countries.some((c) => c.income_group === g)),
    [countries]
  );
  const filtered = useMemo(() => filterCountries(countries, search, region, income), [countries, search, region, income]);
  const byRegion = useMemo(() => groupByRegion(filtered), [filtered]);
  const regionKeys = useMemo(() => visibleRegionKeys(byRegion, region), [byRegion, region]);
  const anyFilter = !!(search || region || income);

  return (
    <>
      <div className="container">
        <div className={s.filterBar}>
          <input aria-label="Search countries" className={s.filterSearch} type="search"
            placeholder="Search countries…" value={search} onChange={(e) => setSearch(e.target.value)} />
        </div>
        <Pills label="Region" options={regions} active={region} onSelect={setRegion} />
        <div style={{ marginTop: '0.5rem' }}>
          <Pills label="Income" options={incomeGroups} active={income} onSelect={setIncome} />
        </div>
        {anyFilter && (
          <div className={s.filterSummary}>
            {filtered.length} of {countries.length} countries
            <button className={`${s.pill} ${s.pillReset}`} type="button"
              onClick={() => { setSearch(''); setRegion(''); setIncome(''); }}>
              clear ×
            </button>
          </div>
        )}
      </div>

      {regionKeys.map((r) => <CountrySection key={r} region={r} items={byRegion[r] ?? []} />)}

      {filtered.length === 0 && (
        <div className="container" style={{ paddingTop: '2rem', color: 'var(--text-2)' }}>
          No countries match your filters.
        </div>
      )}
    </>
  );
}
