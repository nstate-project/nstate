'use client';

import { useState } from 'react';

const API = 'https://api.nstate.org';

const FLAG_TYPES = [
  { value: 'incorrect', label: 'Incorrect — the numbers are wrong' },
  { value: 'outdated', label: 'Outdated — newer data exists' },
  { value: 'misleading', label: 'Misleading — technically right but missing context' },
  { value: 'other', label: 'Other' },
];

export function FlagFinding({ id }: { id: string }) {
  const [open, setOpen] = useState(false);
  const [flagType, setFlagType] = useState('incorrect');
  const [note, setNote] = useState('');
  const [state, setState] = useState<'idle' | 'sending' | 'done'>('idle');

  async function submit() {
    setState('sending');
    await fetch(`${API}/findings/${id}/flag`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ flag_type: flagType, note }),
    });
    setState('done');
  }

  if (!open) {
    return (
      <button
        className="button button--secondary"
        onClick={() => setOpen(true)}
        style={{ fontSize: '0.8em', opacity: 0.6 }}
        type="button"
      >
        flag this finding
      </button>
    );
  }

  if (state === 'done') {
    return (
      <div style={{ color: 'var(--green)', fontSize: '0.9em' }}>
        ✓ Flagged. Thank you — we&apos;ll review it.
      </div>
    );
  }

  return (
    <div className="card" style={{ marginTop: '0.5rem' }}>
      <div className="result-label" style={{ marginBottom: '0.75rem' }}>flag this finding</div>
      <select
        onChange={(e) => setFlagType(e.target.value)}
        style={{
          background: 'var(--surface-2)',
          border: '1px solid var(--border-2)',
          borderRadius: 4,
          color: 'var(--text)',
          font: 'inherit',
          fontSize: '0.85em',
          marginBottom: '0.75rem',
          padding: '0.4rem 0.6rem',
          width: '100%',
        }}
        value={flagType}
      >
        {FLAG_TYPES.map((t) => (
          <option key={t.value} value={t.value}>{t.label}</option>
        ))}
      </select>
      <textarea
        onChange={(e) => setNote(e.target.value)}
        placeholder="Additional context (optional)"
        rows={3}
        style={{
          background: 'var(--surface-2)',
          border: '1px solid var(--border-2)',
          borderRadius: 4,
          color: 'var(--text)',
          font: 'inherit',
          fontSize: '0.85em',
          marginBottom: '0.75rem',
          padding: '0.4rem 0.6rem',
          resize: 'vertical',
          width: '100%',
        }}
        value={note}
      />
      <div className="button-row" style={{ gap: '0.5rem' }}>
        <button
          className="button"
          disabled={state === 'sending'}
          onClick={submit}
          style={{ fontSize: '0.85em' }}
          type="button"
        >
          {state === 'sending' ? 'sending…' : 'submit flag'}
        </button>
        <button
          className="button button--secondary"
          onClick={() => setOpen(false)}
          style={{ fontSize: '0.85em' }}
          type="button"
        >
          cancel
        </button>
      </div>
    </div>
  );
}
