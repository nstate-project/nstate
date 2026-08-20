import { ImageResponse } from 'next/og';

export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';

const API = 'https://api.nstate.org';

export default async function OgImage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;

  let question = 'UK government data, open and cited.';
  let stat = '';

  try {
    const res = await fetch(`${API}/findings/${id}`, { cache: 'no-store' });
    if (res.ok) {
      const f = await res.json() as { question?: string; key_stat_value?: number; key_stat_unit?: string };
      if (f.question) question = f.question;
      if (f.key_stat_value !== undefined) {
        const n = new Intl.NumberFormat('en-GB', { maximumFractionDigits: 1 }).format(f.key_stat_value);
        stat = `${n}${f.key_stat_unit ? ` ${f.key_stat_unit}` : ''}`;
      }
    }
  } catch {
    // fall through to defaults
  }

  const q = question.length > 90 ? `${question.slice(0, 90)}…` : question;

  return new ImageResponse(
    (
      <div style={{
        width: '100%', height: '100%', background: '#0a0a0a',
        display: 'flex', flexDirection: 'column', justifyContent: 'space-between',
        padding: '64px', fontFamily: 'monospace',
      }}>
        <span style={{ color: '#facc15', fontSize: 28, fontWeight: 700 }}>nstate</span>
        <div>
          <div style={{ color: '#f5f5f5', fontSize: 42, fontWeight: 700, lineHeight: 1.25, maxWidth: 1000 }}>
            {q}
          </div>
          {stat && (
            <div style={{ color: '#facc15', fontSize: 72, fontWeight: 700, marginTop: 32 }}>
              {stat}
            </div>
          )}
        </div>
        <span style={{ color: '#4b5563', fontSize: 22 }}>nstate.org · open data · no spin</span>
      </div>
    ),
    { ...size },
  );
}
