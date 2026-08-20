import { marked } from 'marked';
import { notFound } from 'next/navigation';
import { getScorecard, getScorecardSlugs } from '../../../lib/content';

type ScorecardPageProps = {
  params: Promise<{ slug: string }>;
};

export function generateStaticParams() {
  return getScorecardSlugs().map((slug) => ({ slug }));
}

export default async function ScorecardPage({ params }: ScorecardPageProps) {
  const { slug } = await params;
  const scorecard = getScorecard(slug);

  if (!scorecard) {
    notFound();
  }

  const html = marked.parse(scorecard.content) as string;

  return (
    <article className="container prose">
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </article>
  );
}
