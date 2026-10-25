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

Minimal HTTP server that returns a plain-text greeting. It uses only the
Python standard library.

- `app.py` — the whole server. `GET /health` returns `ok`; every other
  `GET` path returns `BODY`. Listens on `0.0.0.0:8000`.
- `tests/test_app.py` — pytest tests that start the server on a free port.
- `Dockerfile` — runs `app.py` on `python:3.13-slim`, exposes port 8000.
- `scripts/verify` — the verification entry point.
- `scripts/git_*.py` — workflow git scripts (see below).

## Local Setup

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
uv sync
uv run python app.py
curl -s http://127.0.0.1:8000/        # greeting
curl -s http://127.0.0.1:8000/health  # ok
```

Container:

```bash
docker build -t hello-world .
docker run --rm -p 8000:8000 hello-world
```

## Verification

Run before every commit:

```bash
./scripts/verify
```

It runs `ruff check`, `ruff format --check` and `pytest`. `scripts/` is
excluded from ruff.

When changing `BODY`, `HEALTH_BODY` or `CONTENT_TYPE`, the tests import the
constants from `app.py`; keep tests and app in sync.

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
