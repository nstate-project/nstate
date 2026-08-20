import { marked } from 'marked';
import { getRepositoryMarkdown } from '../../lib/content';

export const metadata = {
  title: 'Contribute',
};

export default function ContributePage() {
  const html = marked.parse(getRepositoryMarkdown('CONTRIBUTING.md')) as string;

  return (
    <article className="container prose">
      <div dangerouslySetInnerHTML={{ __html: html }} />
    </article>
  );
}
