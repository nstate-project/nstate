import { notFound } from 'next/navigation';
import type { Metadata } from 'next';

const API = 'https://api.nstate.org';

type Finding = {
  id: string;
  question: string;
  narrative: string;
  key_stat_value?: number;
  key_stat_unit?: string;
  sql?: string;
  created_at?: string;
};

async function getFinding(id: string): Promise<Finding | null> {
  const res = await fetch(`${API}/findings/${id}`, { cache: 'no-store' });
  if (!res.ok) return null;
  return res.json() as Promise<Finding>;
}

export async function generateMetadata(
  { params }: { params: Promise<{ id: string }> },
): Promise<Metadata> {
  const { id } = await params;
  const f = await getFinding(id);
  if (!f) return { title: 'Not found' };
  return {
    title: f.question.slice(0, 60),
    description: f.narrative.slice(0, 160),
    openGraph: { images: [`/f/${id}/opengraph-image`] },
  };
}

export default async function FindingPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  const f = await getFinding(id);
  if (!f) notFound();

  return (
    <div className="container">
      <div className="page-header">
        <h1 style={{ fontSize: '1.4rem', maxWidth: '55ch', letterSpacing: '-0.02em' }}>
          {f.question}
        </h1>
      </div>

      <div className="results">
        <section className="result-block">
          <div className="result-label">answer</div>
          <p className="narrative">{f.narrative}</p>
          {f.key_stat_value !== undefined && (
            <div className="key-stat">
              <span className="key-stat__value">
                {new Intl.NumberFormat('en-GB', { maximumFractionDigits: 1 }).format(f.key_stat_value)}
              </span>
              <span className="key-stat__unit">{f.key_stat_unit}</span>
            </div>
          )}
        </section>

        {f.sql && (
          <details className="result-block sql-details">
            <summary className="result-label">SQL query</summary>
            <pre>{f.sql}</pre>
          </details>
        )}

        <div className="result-block">
          <a className="button button--secondary" href="/ask">← ask another question</a>
        </div>
      </div>
    </div>
  );
}
