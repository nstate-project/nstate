'use client';

import { useState } from 'react';

export function CitationCopy({ text }: { text: string }) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  return (
    <button
      className="button button--secondary"
      onClick={copy}
      style={{ fontSize: '0.85em' }}
      type="button"
    >
      {copied ? 'copied ✓' : 'copy citation'}
    </button>
  );
}
