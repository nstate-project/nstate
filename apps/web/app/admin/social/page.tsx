'use client';

import { useState } from 'react';

const API = 'https://api.nstate.org';
const ADMIN_KEY = process.env.NEXT_PUBLIC_ADMIN_KEY ?? 'nstate-admin-2026';
const SITE = 'https://nstate.org';
const X_MAX = 280;
const BSKY_MAX = 300;
const HASHTAGS = '#OpenData #UKGov';

type Finding = {
  id: string;
  question: string;
  headline: string;
  key_stat_value?: number;
  key_stat_unit?: string;
  status: string;
};

function formatStat(f: Finding): string {
  if (f.key_stat_value === undefined) return '';
  const n = new Intl.NumberFormat('en-GB', { maximumFractionDigits: 1 }).format(f.key_stat_value);
  return f.key_stat_unit ? `${n} ${f.key_stat_unit}` : n;
}

function draftPost(f: Finding, platform: 'x' | 'bsky'): string {
  const max = platform === 'x' ? X_MAX : BSKY_MAX;
  const utm = `?utm_source=${platform === 'x' ? 'x' : 'bluesky'}&utm_medium=social`;
  const url = `${SITE}/f/${f.id}${utm}`;
  const stat = formatStat(f);
  const footer = `\n\n${url}\n\n${HASHTAGS}`;
  const budget = max - footer.length;
  const intro = stat ? `${stat}\n\n` : '';
  const body = `${intro}${f.headline}`;
  const trimmed = body.length > budget
    ? `${intro}${f.headline.slice(0, budget - intro.length - 1)}…`
    : body;
  return `${trimmed}${footer}`;
}

function PostDraft({ f, onPosted }: { f: Finding; onPosted: (id: string) => void }) {
  const [copied, setCopied] = useState<'x' | 'bsky' | null>(null);
  const [posting, setPosting] = useState(false);

  async function copy(platform: 'x' | 'bsky') {
    await navigator.clipboard.writeText(draftPost(f, platform));
    setCopied(platform);
    setTimeout(() => setCopied(null), 2000);
  }

  function openIntent(platform: 'x' | 'bsky') {
    const text = encodeURIComponent(draftPost(f, platform));
    const url = platform === 'x'
      ? `https://x.com/intent/tweet?text=${text}`
      : `https://bsky.app/intent/compose?text=${text}`;
    window.open(url, '_blank', 'noopener,noreferrer');
  }

  async function markPosted() {
    setPosting(true);
    await fetch(`${API}/findings/${f.id}/review?key=${ADMIN_KEY}&action=mark_posted`, {
      method: 'PATCH',
    });
    onPosted(f.id);
  }

  return (
    <div className="card" style={{ marginBottom: '1.5rem' }}>
      <p style={{ marginBottom: '0.5rem', fontWeight: 600 }}>{f.question}</p>
      {formatStat(f) && (
        <span className="badge badge--amber" style={{ marginBottom: '0.75rem', display: 'inline-block' }}>
          {formatStat(f)}
        </span>
      )}
      {(['x', 'bsky'] as const).map((platform) => {
        const draft = draftPost(f, platform);
        const label = platform === 'x' ? 'X / Twitter' : 'Bluesky';
        const max = platform === 'x' ? X_MAX : BSKY_MAX;
        return (
          <div key={platform} style={{ marginBottom: '1rem' }}>
            <div className="result-label" style={{ marginBottom: '0.35rem' }}>
              {label} · {draft.length}/{max} chars
            </div>
            <pre style={{ background: 'var(--surface-2)', padding: '0.75rem', borderRadius: '4px',
              fontSize: '0.85em', whiteSpace: 'pre-wrap', border: '1px solid var(--border)',
              marginBottom: '0.5rem' }}>
              {draft}
            </pre>
            <div className="button-row" style={{ gap: '0.5rem' }}>
              <button className="button button--secondary"
                onClick={() => copy(platform)} type="button"
                style={{ fontSize: '0.8em', padding: '0.25rem 0.6rem' }}>
                {copied === platform ? 'copied ✓' : 'copy'}
              </button>
              <button className="button" onClick={() => openIntent(platform)} type="button"
                style={{ fontSize: '0.8em', padding: '0.25rem 0.6rem' }}>
                open in {label} ↗
              </button>
            </div>
          </div>
        );
      })}
      <button className="button button--secondary" disabled={posting}
        onClick={markPosted} type="button"
        style={{ fontSize: '0.85em', marginTop: '0.25rem', opacity: posting ? 0.5 : 1 }}>
        {posting ? 'marking…' : 'mark as posted →'}
      </button>
    </div>
  );
}

export default function SocialPage() {
  const [findings, setFindings] = useState<Finding[] | null>(null);
  const [loading, setLoading] = useState(false);

  async function load() {
    setLoading(true);
    try {
      const res = await fetch(`${API}/admin/findings?key=${ADMIN_KEY}&status=reviewed_finding&limit=20`);
      const data = await res.json() as { findings: Finding[] };
      setFindings(data.findings);
    } finally {
      setLoading(false);
    }
  }

  function onPosted(id: string) {
    setFindings((prev) => prev?.filter((f) => f.id !== id) ?? null);
  }

  return (
    <>
      <div className="container page-header">
        <h1>Social posting queue</h1>
        <p>Draft and post reviewed findings to X and Bluesky. Posts are manual — copy the text, open the platform, paste.</p>
        <div className="button-row" style={{ marginTop: '1rem' }}>
          <button className="button" onClick={load} type="button">
            {loading ? 'loading…' : 'load queue →'}
          </button>
          <a className="button button--secondary" href="/admin">← back to review</a>
        </div>
      </div>
      <div className="container">
        {findings !== null && findings.length === 0 && (
          <p style={{ color: 'var(--text-2)' }}>No reviewed findings waiting to post.</p>
        )}
        {findings?.map((f) => (
          <PostDraft f={f} key={f.id} onPosted={onPosted} />
        ))}
      </div>
    </>
  );
}
