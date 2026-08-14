# Contributing

QueryProof is a focused portfolio project. Small fixes, reproducible bug reports,
and narrowly scoped improvements are welcome.

## Before opening a change

1. Open an issue describing the problem and acceptance criteria.
2. Confirm that all fixtures are synthetic and contain no personal or employer
   data.
3. Keep executable SQL inside the reviewed catalog; never interpolate user text.

## Development

```bash
npm ci
uv sync --frozen --group dev
npm run check
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy api queryproof scripts
```

Regenerate data before changing fixture logic:

```bash
uv run python scripts/generate_data.py
git diff -- data/support_tickets.csv
```

Pull requests should explain the problem, solution, verification, privacy impact,
and known limitations. UI changes should include a screenshot made only from the
synthetic fixture.
