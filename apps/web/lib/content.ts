import fs from 'node:fs';
import path from 'node:path';
import matter from 'gray-matter';

const repositoryRoot = path.resolve(process.cwd(), '../..');

export type Scorecard = {
  dataDate: string;
  evidenceQuality: string;
  slug: string;
  status: string;
  title: string;
};

function getField(content: string, label: string) {
  const match = content.match(new RegExp(`\\*\\*${label}:\\*\\*\\s*([^\\n]+)`, 'i'));
  return match?.[1]?.trim() ?? 'Not stated';
}

export function getRepositoryMarkdown(filename: string) {
  return fs.readFileSync(path.join(repositoryRoot, filename), 'utf8');
}

function getScorecardsDirectory() {
  return path.join(repositoryRoot, 'uk/scorecards');
}

export function getScorecardSlugs() {
  return fs
    .readdirSync(getScorecardsDirectory())
    .filter((filename) => filename.endsWith('.md') && filename !== 'TEMPLATE.md')
    .map((filename) => filename.replace(/\.md$/, ''));
}

export function getScorecard(slug: string): (Scorecard & { content: string }) | null {
  if (!getScorecardSlugs().includes(slug)) {
    return null;
  }

  const filePath = path.join(getScorecardsDirectory(), `${slug}.md`);
  const parsed = matter(fs.readFileSync(filePath, 'utf8'));
  const title = parsed.content.match(/^#\s+(.+)$/m)?.[1] ?? slug;

  return {
    content: parsed.content,
    dataDate: getField(parsed.content, 'Data date'),
    evidenceQuality: getField(parsed.content, 'Evidence quality \\(overall\\)'),
    slug,
    status: getField(parsed.content, 'Status'),
    title,
  };
}

export function getScorecards(): Scorecard[] {
  return getScorecardSlugs()
    .map((slug) => getScorecard(slug))
    .filter((scorecard): scorecard is Scorecard & { content: string } => scorecard !== null)
    .map(({ content: _, ...scorecard }) => scorecard);
}
