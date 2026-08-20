import { marked } from 'marked';
import Link from 'next/link';
import { getRepositoryMarkdown, getScorecards } from '../../lib/content';

export const metadata = {
  title: 'UK',
};

export default function UKPage() {
  const scorecards = getScorecards();
  const html = marked.parse(getRepositoryMarkdown('uk/README.md')) as string;

  return (
    <div className="container">
      <header className="page-header">
        <h1>United Kingdom</h1>
        <p>National audit — open, reproducible, evidence-backed.</p>
      </header>

      {scorecards.length > 0 && (
        <section style={{ marginBottom: '3rem' }}>
          <h2 style={{ fontSize: '1rem', color: 'var(--text-2)', marginBottom: '1rem' }}>
            published scorecards
          </h2>
          <div className="card-list">
            {scorecards.map((sc) => (
              <Link className="card" href={`/scorecards/${sc.slug}`} key={sc.slug}>
                <div className="card__meta">
                  <span className={`badge ${sc.status.toLowerCase() === 'published' ? 'badge--amber' : ''}`}>
                    {sc.status}
                  </span>
                  <span className={`badge ${sc.evidenceQuality.toLowerCase() === 'high' ? 'badge--green' : ''}`}>
                    evidence: {sc.evidenceQuality}
                  </span>
                </div>
                <h3>{sc.title}</h3>
                <p>Data date: {sc.dataDate}</p>
              </Link>
            ))}
          </div>
        </section>
      )}

      <article className="prose">
        <div dangerouslySetInnerHTML={{ __html: html }} />
      </article>
    </div>
  );
}
