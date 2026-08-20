import Link from 'next/link';
import { getScorecards } from '../../lib/content';

export const metadata = {
  title: 'Scorecards',
};

export default function ScorecardsPage() {
  const scorecards = getScorecards();

  return (
    <div className="container">
      <header className="page-header">
        <h1>UK scorecards</h1>
        <p>
          Reproducible policy audits using public data, stated assumptions, and a clear
          separation between observation and estimate.
        </p>
      </header>

      <div className="card-list">
        {scorecards.map((scorecard) => (
          <Link className="card" href={`/scorecards/${scorecard.slug}`} key={scorecard.slug}>
            <div className="card__meta">
              <span className={`badge ${scorecard.status.toLowerCase() === 'published' ? 'badge--amber' : ''}`}>
                {scorecard.status}
              </span>
              <span className={`badge ${scorecard.evidenceQuality.toLowerCase() === 'high' ? 'badge--green' : ''}`}>
                evidence: {scorecard.evidenceQuality}
              </span>
            </div>
            <h2>{scorecard.title}</h2>
            <p>Data date: {scorecard.dataDate}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
