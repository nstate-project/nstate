import Link from 'next/link';

const API = 'https://api.nstate.org';

const stats = [
  { label: 'UK public spending 2024–25', value: '£1.26tn' },
  { label: 'scorecards published', value: '3' },
  { label: 'countries', value: '1' },
  { label: 'data pipelines', value: '14' },
];

type RecentFinding = {
  id: string;
  question: string;
  key_stat_value?: number;
  key_stat_unit?: string;
  created_at?: string;
};

async function getRecentFindings(): Promise<RecentFinding[]> {
  try {
    const res = await fetch(`${API}/findings/recent?limit=5`, { next: { revalidate: 60 } });
    if (!res.ok) return [];
    const data = await res.json() as { findings: RecentFinding[] };
    return data.findings ?? [];
  } catch {
    return [];
  }
}

function timeAgo(iso?: string) {
  if (!iso) return '';
  const diff = Date.now() - new Date(iso).getTime();
  const h = Math.floor(diff / 3600000);
  if (h < 1) return 'just now';
  if (h < 24) return `${h}h ago`;
  return `${Math.floor(h / 24)}d ago`;
}

export default async function HomePage() {
  const findings = await getRecentFindings();

  return (
    <>
      <section className="hero">
        <div className="container">
          <h1>Dismantle overreaching, wasteful states.</h1>
          <p>
            nstate audits every public pound against its stated objective. Open data,
            reproducible methods, published for everyone.
          </p>
          <div className="button-row">
            <Link className="button" href="/ask">ask the data →</Link>
            <Link className="button button--secondary" href="/scorecards">UK scorecards</Link>
          </div>
        </div>
      </section>

      <div className="container stats">
        {stats.map((stat) => (
          <div className="stat" key={stat.label}>
            <span className="stat__label">{stat.label}</span>
            <span className="stat__value">{stat.value}</span>
          </div>
        ))}
      </div>

      {findings.length > 0 && (
        <section className="section">
          <div className="container">
            <h2>Recent queries</h2>
            <div className="card-list" style={{ marginTop: '1rem' }}>
              {findings.map((f) => (
                <Link className="card" href={`/f/${f.id}`} key={f.id}>
                  <p style={{ marginBottom: '0.4rem' }}>{f.question}</p>
                  <div className="card__meta">
                    {f.key_stat_value !== undefined && (
                      <span className="badge badge--amber">
                        {new Intl.NumberFormat('en-GB', { maximumFractionDigits: 1 }).format(f.key_stat_value)}
                        {f.key_stat_unit ? ` ${f.key_stat_unit}` : ''}
                      </span>
                    )}
                    <span className="badge">{timeAgo(f.created_at)}</span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>
      )}

      <section className="section">
        <div className="container">
          <h2>Evidence before argument.</h2>
          <p>
            Every scorecard starts with the government&apos;s own stated objective,
            traces every number to a primary source, and makes its assumptions explicit.
          </p>
        </div>
      </section>
    </>
  );
}
