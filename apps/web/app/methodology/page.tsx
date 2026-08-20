import { marked } from 'marked';
import { getRepositoryMarkdown } from '../../lib/content';

export const metadata = {
  title: 'Methodology',
};

export default function MethodologyPage() {
  const html = marked.parse(getRepositoryMarkdown('METHODOLOGY.md')) as string;

  return (
    <article className="container prose">
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </article>
  );
}
