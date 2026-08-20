import type { Metadata } from 'next';

const API = 'https://api.nstate.org';

type Finding = {
  id: string;
  question: string;
  narrative: string;
  key_stat_value?: number;
  key_stat_unit?: string;
  source?: string;
};

async function getFinding(id: string): Promise<Finding | null> {
  const res = await fetch(`${API}/findings/${id}`, { cache: 'no-store' });
  if (!res.ok) return null;
  return res.json() as Promise<Finding>;
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ id: string }>;
}): Promise<Metadata> {
  const { id } = await params;
  const f = await getFinding(id);
  return f
    ? { title: f.question.slice(0, 60), description: f.narrative.slice(0, 160) }
    : { title: 'nstate embed' };
}

export default async function EmbedPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  const f = await getFinding(id);

  if (!f) {
    return (
      <div style={{ padding: '1rem', fontFamily: 'monospace', color: '#9ca3af' }}>
        Finding not found.
      </div>
    );
  }

  const stat =
    f.key_stat_value !== undefined
      ? `${new Intl.NumberFormat('en-GB', { maximumFractionDigits: 1 }).format(f.key_stat_value)}${f.key_stat_unit ? ` ${f.key_stat_unit}` : ''}`
      : null;

  return (
    <div
      style={{
        background: '#0a0a0a',
        color: '#f5f5f5',
        fontFamily: "'Courier New', monospace",
        padding: '1.25rem 1.5rem',
        border: '1px solid #1a1a1a',
        borderRadius: '4px',
        minHeight: '100vh',
      }}
    >
      <p style={{ color: '#9ca3af', fontSize: '0.8em', marginBottom: '0.75rem' }}>
        nstate · UK public data
      </p>
      <p style={{ fontSize: '0.95em', marginBottom: '0.75rem', color: '#f5f5f5' }}>
        {f.question}
      </p>
      {stat && (
        <div style={{ color: '#facc15', fontSize: '2rem', fontWeight: 700, margin: '0.5rem 0' }}>
          {stat}
        </div>
      )}
      <p style={{ color: '#d1d5db', fontSize: '0.88em', margin: '0.75rem 0' }}>{f.narrative}</p>
      {f.source && (
        <p style={{ color: '#4b5563', fontSize: '0.78em' }}>Source: {f.source}</p>
      )}
      <a
        href={`https://nstate.org/f/${id}`}
        rel="noopener noreferrer"
        style={{ color: '#facc15', fontSize: '0.8em', textDecoration: 'none' }}
        target="_blank"
      >
        nstate.org →
      </a>
    </div>
  );
}
