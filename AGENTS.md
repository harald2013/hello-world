# AGENTS.md

Instructions for AI coding agents working in this repository.

## Architecture rules

Read [AGENT_RULES.md](AGENT_RULES.md) before working in this repository.
Read inherited and active-scope rules when working in a module. Load the linked
German ADRs only when you need the rationale or are reviewing a decision.

Before planning or changing infrastructure or architecture, call the
Development Instructor MCP's `server_guide` and then `get_agent_rules`.
Apply the returned rules for the domains used by this project.

## Overview

Portable report example: FastAPI, Temporal workflows and PostgreSQL.

- `app.py` — ASGI entry point; API routes live in `reports/api.py`.
- `reports/` — runtime configuration, models, database, workflow and worker.
- `tests/` — API/configuration tests and a real Temporal test-server integration.
- `Dockerfile` — `api` and `worker` targets, Python 3.13, non-root runtime.
- `compose.yml` — local synthetic-data stack; never deploy it to Coolify.
- `deploy/` — staging and managed-production setup and operating instructions.
- `.github/workflows/` — CI and immutable image publication.
- `scripts/verify` — the verification entry point.
- `scripts/smoke.py` — full-stack check; optional local worker restart.
- `scripts/git_*.py` — workflow git scripts (see below).

## Local Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync --locked
cp .env.example .env
docker compose up --build -d --wait --wait-timeout 240
uv run python scripts/smoke.py
```

See [README.md](README.md) for API usage and [deploy/](deploy/operations.md)
for configuration. Staging uses individual images on workhorse. Production uses
managed application hosting, Temporal Cloud and Neon. Read [COOLIFY.md](COOLIFY.md)
for existing staging resources before using Coolify tools; production resources
have not been provisioned.

## Verification

Run before every commit:

```bash
./scripts/verify
```

It runs `ruff check`, `ruff format --check` and `pytest`. `scripts/` is
excluded from ruff.

The Temporal integration downloads the official SDK test server on first use;
`TEMPORAL_TEST_SERVER` can select an existing binary. After container or database
changes, also run the Compose smoke test. Workflow changes require history replay.

## Workflow

- Tickets are Linear issues with the `TIL-<number>` prefix.
- Work on a branch `feature/<ticket>-<short-feature-name>`, e.g.
  `feature/til-116-change-message`.
- Never push directly to `main`. Changes reach `main` only through a pull
  request against `main`.

The git scripts in `scripts/` implement these steps. They log to
`workflow-logs/<branch>/` inside the checkout (excluded via
`.git/info/exclude`):

```bash
python3 -B scripts/git_start.py  <repository> <ticket> <short-feature-name> [base]
python3 -B scripts/git_commit.py <repository> <message>
python3 -B scripts/git_fetch.py  <repository> [remote] [ref]
python3 -B scripts/git_push.py   <repository> [remote] [base]
```

`scripts/git_*.py` are unmodified development-instructor templates. Do not
edit them in this repository.
