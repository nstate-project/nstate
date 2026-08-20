'use client';

import { useRouter } from 'next/navigation';
import { useState } from 'react';

export default function HomeAsk() {
  const [q, setQ] = useState('');
  const router = useRouter();

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const question = q.trim();
    if (question) router.push(`/ask?q=${encodeURIComponent(question)}`);
  }

  return (
    <form className="ask-form" onSubmit={handleSubmit} style={{ marginTop: '1.5rem' }}>
      <input
        aria-label="Ask about government data"
        onChange={(e) => setQ(e.target.value)}
        placeholder="Which country has the highest debt? How much does the UK spend on the NHS?"
        value={q}
      />
      <button className="button" type="submit">ask →</button>
    </form>
  );
}
