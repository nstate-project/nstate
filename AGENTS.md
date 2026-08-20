## Development

### Frontend (apps/web — Next.js 15 App Router)

```bash
cd apps/web
npm install
npm run dev       # → localhost:3000
npm run build     # verify before PR
```

### Backend (services/api — FastAPI)

```bash
cd services/api
python -m uvicorn main:app --reload  # → localhost:8000
```

Or run the full stack:

```bash
docker compose up
```

## Architecture

See `research/SPEC-NSTATE-PLATFORM.md` for the authoritative platform spec.

- Frontend: Next.js 15 (App Router) → `apps/web/`
- Backend: FastAPI → `services/api/` (deployed to VPS 95.217.212.173)
- Database: DuckDB at `/opt/nstate/data/nstate.duckdb` on VPS
- Data pipelines: Python scripts → `data/uk/pipelines/`

## Documentation

- [Next.js App Router](https://nextjs.org/docs/app)
- [next/og — OG image generation](https://nextjs.org/docs/app/api-reference/file-conventions/metadata/opengraph-image)
- [Vega-Lite — charts](https://vega.github.io/vega-lite/)
