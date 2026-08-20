import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Developer API — nstate',
  description: 'Public REST API for querying nstate government data. No key required.',
};

const API = 'https://api.nstate.org';

const ENDPOINTS = [
  {
    method: 'POST',
    path: '/query',
    description: 'Ask a plain-English question. Returns a cited, data-backed answer or a gap notice.',
    note: 'Rate limited: 30 requests/hour per IP.',
    example: `curl -X POST ${API}/query \\
  -H 'Content-Type: application/json' \\
  -d '{"question":"How many civil servants work for the UK?","country":"uk"}'`,
  },
  {
    method: 'GET',
    path: '/findings',
    description: 'List published findings. Add ?status=reviewed_finding for curated ones.',
    note: null,
    example: `curl "${API}/findings?country=uk&limit=10"`,
  },
  {
    method: 'GET',
    path: '/findings/{id}',
    description: 'Single finding by ID — includes question, narrative, key stat, SQL.',
    note: null,
    example: `curl "${API}/findings/uk-2026-0001"`,
  },
  {
    method: 'GET',
    path: '/findings/{id}/export.csv',
    description: 'Download finding data as a CSV file. Re-runs stored SQL for fresh rows.',
    note: null,
    example: `curl -O "${API}/findings/uk-2026-0001/export.csv"`,
  },
  {
    method: 'POST',
    path: '/findings/{id}/flag',
    description: 'Flag a finding as incorrect, outdated, misleading, or other.',
    note: null,
    example: `curl -X POST ${API}/findings/uk-2026-0001/flag \\
  -H 'Content-Type: application/json' \\
  -d '{"flag_type":"outdated","note":"ONS updated this in June 2026"}'`,
  },
  {
    method: 'GET',
    path: '/gaps',
    description: 'Top data gaps sorted by vote count — the public roadmap.',
    note: null,
    example: `curl "${API}/gaps?country=uk&limit=20"`,
  },
  {
    method: 'POST',
    path: '/gaps/vote',
    description: 'Vote to prioritise a gap topic.',
    note: null,
    example: `curl -X POST "${API}/gaps/vote?topic=NHS+waiting+times+by+trust&country=uk"`,
  },
  {
    method: 'GET',
    path: '/datasets',
    description: 'List loaded datasets for a country with source URLs and priority.',
    note: null,
    example: `curl "${API}/datasets?country=uk"`,
  },
  {
    method: 'GET',
    path: '/health',
    description: 'Health check — returns current UTC time.',
    note: null,
    example: `curl "${API}/health"`,
  },
];

const METHOD_COLOUR: Record<string, string> = {
  GET: '#22c55e',
  POST: '#facc15',
};

export default function DeveloperPage() {
  return (
    <>
      <div className="container page-header">
        <h1>Developer API</h1>
        <p>
          The nstate API is public and requires no key. Base URL:{' '}
          <code style={{ color: 'var(--amber)' }}>{API}</code>
        </p>
        <div className="button-row" style={{ marginTop: '1rem' }}>
          <a className="button" href={`${API}/docs`} rel="noopener noreferrer" target="_blank">
            interactive docs (OpenAPI) ↗
          </a>
          <a
            className="button button--secondary"
            href="https://github.com/nstate-project/nstate"
            rel="noopener noreferrer"
            target="_blank"
          >
            source on GitHub ↗
          </a>
        </div>
      </div>

      <div className="container">
        <div className="result-block" style={{ marginBottom: '2rem' }}>
          <div className="result-label">licence</div>
          <p style={{ color: 'var(--text-2)', fontSize: '0.9em' }}>
            Data: CC BY 4.0 — free to use, attribute nstate.org. Code: MIT.
            Rate limit: 30 requests/hour per IP for /query. All other endpoints are unlimited.
          </p>
        </div>

        {ENDPOINTS.map((ep) => (
          <div className="card" key={ep.path} style={{ marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.75rem', marginBottom: '0.4rem' }}>
              <span style={{
                color: METHOD_COLOUR[ep.method] ?? 'var(--text-2)',
                fontSize: '0.78em',
                fontWeight: 700,
                letterSpacing: '0.05em',
              }}>
                {ep.method}
              </span>
              <code style={{ color: 'var(--text)', fontSize: '0.95em' }}>{ep.path}</code>
            </div>
            <p style={{ color: 'var(--text-2)', fontSize: '0.88em', marginBottom: ep.note || ep.example ? '0.5rem' : 0 }}>
              {ep.description}
            </p>
            {ep.note && (
              <p style={{ color: 'var(--amber-dim)', fontSize: '0.82em', marginBottom: '0.5rem' }}>
                ⚠ {ep.note}
              </p>
            )}
            {ep.example && (
              <pre style={{
                background: 'var(--surface-2)',
                border: '1px solid var(--border)',
                borderRadius: 4,
                fontSize: '0.78em',
                overflowX: 'auto',
                padding: '0.65rem 0.85rem',
              }}>
                {ep.example}
              </pre>
            )}
          </div>
        ))}
      </div>
    </>
  );
}
