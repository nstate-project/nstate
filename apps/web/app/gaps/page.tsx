import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Data gaps — nstate',
  description: 'The data gaps the public has asked for most. Vote to help shape our roadmap.',
};

const API = 'https://api.nstate.org';

type Gap = {
  topic: string;
  question_example: string;
  votes: number;
  created_at: string;
};

async function getGaps(): Promise<Gap[]> {
  try {
    const res = await fetch(`${API}/gaps?limit=50`, { next: { revalidate: 300 } });
    if (!res.ok) return [];
    const data = (await res.json()) as { gaps: Gap[] };
    return data.gaps;
  } catch {
    return [];
  }
}

export default async function GapsPage() {
  const gaps = await getGaps();

  return (
    <>
      <div className="container page-header">
        <h1>Data gaps</h1>
        <p>
          Questions the public has asked that we can&apos;t yet answer — sorted by votes. This is
          our data roadmap.
        </p>
      </div>
      <div className="container">
        {gaps.length === 0 && (
          <p style={{ color: 'var(--text-2)' }}>No gaps recorded yet. Ask a question to log the first one.</p>
        )}
        {gaps.length > 0 && (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Question asked</th>
                  <th style={{ textAlign: 'right', whiteSpace: 'nowrap' }}>votes</th>
                </tr>
              </thead>
              <tbody>
                {gaps.map((g, i) => (
                  <tr key={i}>
                    <td style={{ maxWidth: 620 }}>{g.question_example || g.topic}</td>
                    <td style={{ textAlign: 'right', fontVariantNumeric: 'tabular-nums' }}>
                      <span className="badge badge--amber">{g.votes}</span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        <div style={{ marginTop: '2rem', display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
          <a className="button" href="/ask">ask a question →</a>
          <a className="button button--secondary" href="https://github.com/nstate-project/nstate/issues/new?title=Dataset+request" rel="noopener noreferrer" target="_blank">
            request a dataset on GitHub ↗
          </a>
        </div>
      </div>
    </>
  );
}
