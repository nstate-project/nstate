'use client';

import { useState } from 'react';

const API = 'https://api.nstate.org';
const ADMIN_KEY = process.env.NEXT_PUBLIC_ADMIN_KEY ?? 'nstate-admin-2026';

type Finding = {
  id: string;
  country: string;
  question: string;
  headline: string;
  key_stat_value?: number;
  key_stat_unit?: string;
  status: string;
  created_at?: string;
};

function FindingRow({
  f,
  onAction,
}: {
  f: Finding;
  onAction: (id: string, action: 'approve' | 'reject') => void;
}) {
  return (
    <tr>
      <td style={{ maxWidth: 320 }}>
        <div style={{ marginBottom: '0.25rem', color: 'var(--text)' }}>{f.question}</div>
        <div style={{ color: 'var(--text-2)', fontSize: '0.85em' }}>{f.headline}</div>
      </td>
      <td>
        {f.key_stat_value !== undefined && (
          <span className="badge badge--amber">
            {new Intl.NumberFormat('en-GB', { maximumFractionDigits: 1 }).format(f.key_stat_value)}
            {f.key_stat_unit ? ` ${f.key_stat_unit}` : ''}
          </span>
        )}
      </td>
      <td style={{ color: 'var(--text-2)', fontSize: '0.85em' }}>{f.status}</td>
      <td>
        <div className="button-row" style={{ gap: '0.5rem' }}>
          <button
            className="button"
            onClick={() => onAction(f.id, 'approve')}
            style={{ padding: '0.25rem 0.75rem', fontSize: '0.85em' }}
            type="button"
          >
            approve
          </button>
          <button
            className="button button--secondary"
            onClick={() => onAction(f.id, 'reject')}
            style={{ padding: '0.25rem 0.75rem', fontSize: '0.85em' }}
            type="button"
          >
            reject
          </button>
        </div>
      </td>
    </tr>
  );
}

export default function AdminPage() {
  const [findings, setFindings] = useState<Finding[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('automated_finding');

  async function load() {
    setLoading(true);
    setError('');
    try {
      const res = await fetch(`${API}/admin/findings?key=${ADMIN_KEY}&status=${filter}`);
      if (!res.ok) throw new Error(`${res.status}`);
      const data = await res.json() as { findings: Finding[] };
      setFindings(data.findings);
    } catch {
      setError('Could not load findings. Check the admin key.');
    } finally {
      setLoading(false);
    }
  }

  async function handleAction(id: string, action: 'approve' | 'reject') {
    await fetch(`${API}/findings/${id}/review?key=${ADMIN_KEY}&action=${action}`, {
      method: 'PATCH',
    });
    setFindings((prev) => prev?.filter((f) => f.id !== id) ?? null);
  }

  return (
    <>
      <div className="container page-header">
        <h1>Admin — findings review</h1>
        <p>Review and approve automated findings before they enter the public feed.</p>
        <div className="button-row" style={{ marginTop: '1rem' }}>
          <a className="button button--secondary" href="/admin/social">social posting queue →</a>
        </div>
      </div>
      <div className="container">
        <div className="button-row" style={{ marginBottom: '1.5rem', gap: '0.75rem' }}>
          {(['automated_finding', 'reviewed_finding', 'rejected'] as const).map((s) => (
            <button
              className={`button ${filter === s ? '' : 'button--secondary'}`}
              key={s}
              onClick={() => setFilter(s)}
              type="button"
            >
              {s.replace('_', ' ')}
            </button>
          ))}
          <button className="button" onClick={load} type="button">
            {loading ? 'loading…' : 'load →'}
          </button>
        </div>
        {error && <div className="error-state">{error}</div>}
        {findings !== null && findings.length === 0 && (
          <p style={{ color: 'var(--text-2)' }}>No findings with status &quot;{filter}&quot;.</p>
        )}
        {findings && findings.length > 0 && (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>Question / headline</th>
                  <th>Key stat</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {findings.map((f) => (
                  <FindingRow f={f} key={f.id} onAction={handleAction} />
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </>
  );
}
