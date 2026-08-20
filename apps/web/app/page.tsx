import Link from 'next/link';

const stats = [
  { label: 'UK public spending 2024–25', value: '£1.26tn' },
  { label: 'scorecards published', value: '1' },
  { label: 'countries', value: '1' },
  { label: 'data pipelines', value: '14' },
];

export default function HomePage() {
  return (
    <>
      <section className="hero">
        <div className="container">
          <h1>Dismantle overreaching, wasteful states.</h1>
          <p>
            nstate audits every public pound against its stated objective. Open data,
            reproducible methods, published for everyone.
          </p>
          <div className="button-row">
            <Link className="button" href="/ask">ask the data →</Link>
            <Link className="button button--secondary" href="/scorecards">UK scorecards</Link>
          </div>
        </div>
      </section>

      <div className="container stats">
        {stats.map((stat) => (
          <div className="stat" key={stat.label}>
            <span className="stat__label">{stat.label}</span>
            <span className="stat__value">{stat.value}</span>
          </div>
        ))}
      </div>

      <section className="section">
        <div className="container">
          <h2>Evidence before argument.</h2>
          <p>
            Every scorecard starts with the government&apos;s own stated objective,
            traces every number to a primary source, and makes its assumptions explicit.
          </p>
        </div>
      </section>
    </>
  );
}
