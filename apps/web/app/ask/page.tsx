'use client';

import { FormEvent, RefObject, useEffect, useRef, useState } from 'react';

const API_URL = 'https://api.nstate.org/query';

const EXAMPLES = [
  'How many civil servants work for the UK government?',
  'What are the biggest categories of UK government spending?',
  'How much did HMRC collect in income tax last year?',
  'What is the average UK private sector salary?',
  'How many people claim Universal Credit?',
];

type QueryResponse = {
  chart_spec?: Record<string, unknown>;
  columns?: string[];
  id?: string;
  key_stat_unit?: string;
  key_stat_value?: number;
  narrative?: string;
  reason?: string;
  rows?: Record<string, unknown>[];
  source?: string;
  sql?: string;
  status?: 'ok' | 'gap';
  topic?: string;
  votes?: number;
};

declare global {
  interface Window {
    vegaEmbed?: (el: Element, spec: Record<string, unknown>, opts: Record<string, unknown>) => Promise<unknown>;
  }
}

function loadScript(src: string) {
  return new Promise<void>((resolve, reject) => {
    const s = document.createElement('script');
    s.src = src; s.async = true;
    s.onload = () => resolve();
    s.onerror = () => reject(new Error(`Failed to load ${src}`));
    document.head.appendChild(s);
  });
}

function DataTable({ rows, columns }: { rows: Record<string, unknown>[]; columns: string[] }) {
  return (
    <section className="result-block">
      <div className="result-label">data</div>
      <div className="table-wrap">
        <table>
          <thead><tr>{columns.map((c) => <th key={c}>{c.replaceAll('_', ' ')}</th>)}</tr></thead>
          <tbody>
            {rows.map((row, i) => (
              <tr key={i}>{columns.map((c) => <td key={c}>{String(row[c] ?? '')}</td>)}</tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}

function GapState({ result }: { result: QueryResponse }) {
  const [votes, setVotes] = useState(result.votes ?? 0);
  const [voted, setVoted] = useState(false);

  async function vote() {
    if (voted || !result.topic) return;
    setVoted(true);
    setVotes((v) => v + 1);
    await fetch(
      `https://api.nstate.org/gaps/vote?topic=${encodeURIComponent(result.topic)}`,
      { method: 'POST' },
    );
  }

  return (
    <div className="gap-state">
      <div className="gap-state__circle">○</div>
      <p>{result.reason ?? "We don't have this data yet."}</p>
      <p style={{ color: 'var(--text-2)', fontSize: '0.9em', marginTop: '0.5rem' }}>
        {votes > 1 && <span>{votes} others have asked.{' '}</span>}
        {!voted ? (
          <button
            className="button button--secondary"
            disabled={!result.topic}
            onClick={vote}
            style={{ fontSize: '0.82em', padding: '0.2rem 0.55rem' }}
            type="button"
          >
            vote to prioritise
          </button>
        ) : (
          <span style={{ color: 'var(--green)' }}>✓ voted</span>
        )}
      </p>
      <p style={{ color: 'var(--text-3)', fontSize: '0.82em', marginTop: '0.25rem' }}>
        <a href="/gaps">see all data gaps →</a>
      </p>
    </div>
  );
}

function Results({ result, chartRef }: { result: QueryResponse; chartRef: RefObject<HTMLDivElement | null> }) {
  const columns = result.columns ?? [];
  const rows = result.rows ?? [];
  return (
    <div className="results">
      <section className="result-block">
        <div className="result-label">answer</div>
        <p className="narrative">{result.narrative}</p>
        {result.key_stat_value !== undefined && (
          <div className="key-stat">
            <span className="key-stat__value">
              {new Intl.NumberFormat('en-GB', { maximumFractionDigits: 1 }).format(result.key_stat_value)}
            </span>
            <span className="key-stat__unit">{result.key_stat_unit}</span>
          </div>
        )}
      </section>
      {result.chart_spec && <div className="result-block" ref={chartRef} />}
      {rows.length > 0 && columns.length > 0 && <DataTable rows={rows} columns={columns} />}
      {result.sql && (
        <details className="result-block sql-details">
          <summary className="result-label">SQL query</summary>
          <pre>{result.sql}</pre>
        </details>
      )}
      {result.source && (
        <div className="result-block"><div className="result-label">source</div><p>{result.source}</p></div>
      )}
      {result.id && (
        <div className="result-block">
          <a className="button button--secondary" href={`/f/${result.id}`}>share this result →</a>
        </div>
      )}
    </div>
  );
}

function useVegaChart(chartRef: RefObject<HTMLDivElement | null>, result: QueryResponse | null) {
  const [chartReady, setChartReady] = useState(false);

  useEffect(() => {
    let active = true;
    async function load() {
      try {
        await loadScript('https://cdn.jsdelivr.net/npm/vega@5/build/vega.min.js');
        await loadScript('https://cdn.jsdelivr.net/npm/vega-lite@5/build/vega-lite.min.js');
        await loadScript('https://cdn.jsdelivr.net/npm/vega-embed@6/build/vega-embed.min.js');
        if (active) setChartReady(true);
      } catch { /* chart optional */ }
    }
    void load();
    return () => { active = false; };
  }, []);

  useEffect(() => {
    if (!chartReady || !chartRef.current || !result?.chart_spec || !window.vegaEmbed) return;
    chartRef.current.replaceChildren();
    void window.vegaEmbed(chartRef.current, {
      ...result.chart_spec,
      background: '#0a0a0a',
      config: {
        view: { stroke: '#1a1a1a' },
        axis: { domainColor: '#242424', gridColor: '#1a1a1a', labelColor: '#9ca3af', titleColor: '#9ca3af' },
        mark: { color: '#facc15' },
      },
    }, { actions: false, renderer: 'svg' });
  }, [chartReady, result, chartRef]);
}

export default function AskPage() {
  const chartRef = useRef<HTMLDivElement | null>(null);
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState<QueryResponse | null>(null);
  const [state, setState] = useState<'idle' | 'loading' | 'error'>('idle');

  useVegaChart(chartRef, result);

  async function submitQuery(q: string) {
    setQuestion(q); setResult(null); setState('loading');
    try {
      const res = await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: q }),
      });
      if (!res.ok) throw new Error(`${res.status}`);
      setResult((await res.json()) as QueryResponse);
      setState('idle');
    } catch { setState('error'); }
  }

  function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const q = question.trim();
    if (q) void submitQuery(q);
  }

  return (
    <>
      <div className="container page-header">
        <h1>Ask the data</h1>
        <p>Query UK government data in plain English. Every answer is backed by official data.</p>
      </div>
      <div className="ask-bar">
        <div className="container">
          <form className="ask-form" onSubmit={handleSubmit}>
            <input
              aria-label="Question about UK government data"
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="How much does the UK government spend on the NHS per year?"
              value={question}
            />
            <button className="button" type="submit">ask →</button>
          </form>
        </div>
      </div>
      <div className="container">
        <div className="examples">
          {EXAMPLES.map((ex) => (
            <button className="example-pill" key={ex} onClick={() => void submitQuery(ex)} type="button">{ex}</button>
          ))}
        </div>
        {state === 'loading' && <div className="loading">querying...</div>}
        {state === 'error' && <div className="error-state">Could not reach the API. Check your connection.</div>}
        {result?.status === 'gap' && <GapState result={result} />}
        {result?.status !== 'gap' && result && <Results result={result} chartRef={chartRef} />}
      </div>
    </>
  );
}
