# AI Customer Support

Python 3.13 application built with FastAPI and managed with `uv`.

## Setup

From this directory, install the project dependencies and create your local
environment file:

```powershell
uv sync --dev
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Fill in the credentials in `.env`, then start the development server:

```powershell
uv run fastapi dev app/main.py
```

The health check is available at <http://127.0.0.1:8000/health>.

For AI features through the FreeLLMAPI desktop app, configure eligible
provider keys and routes in its dashboard. Copy its unified API key into
`OPENAI_API_KEY` in `.env`. Both the classifier and support agent use the
explicit `gpt-oss-120b` model through the OpenAI-compatible endpoint at
`http://127.0.0.1:31415/v1`. The support agent loads relevant knowledge-base
entries into the prompt, avoiding fragile provider-side function calls.
Explicit model selection avoids the router's `auto` selection, which may
choose rate-limited or tool-incompatible routes. Confirm the model is
available in the FreeLLMAPI dashboard; provider quotas and availability still
apply. A self-hosted Docker instance uses port 3001 instead.

## Knowledge base

Each `##` heading in `knowledge_base/*.md` becomes one knowledge-base entry.
Validate the Markdown without connecting to or changing the database:

```powershell
uv run python -m scripts.load_knowledge_base
```

After reviewing the content and confirming `.env` points to the intended
database, seed or update the entries:

```powershell
uv run python -m scripts.seed_knowledge_base
```

Seeding upserts by section and title. Re-running it updates matching database
entries with the Markdown content; it does not delete entries removed from the
files.

---
