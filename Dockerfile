FROM python:3.13-slim AS base
COPY --from=ghcr.io/astral-sh/uv:0.12.5 /uv /usr/local/bin/uv
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev
ENV PATH="/app/.venv/bin:$PATH" PYTHONUNBUFFERED=1
COPY reports ./reports
COPY app.py ./
RUN useradd --uid 10001 --create-home app
USER app

FROM postgres:16.6 AS backup
RUN apt-get update && apt-get install -y --no-install-recommends python3 python3-boto3 ca-certificates \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY ops/backup.py /app/backup.py
USER postgres
ENTRYPOINT []
CMD ["python3", "/app/backup.py"]

FROM base AS worker
CMD ["python", "-m", "reports.worker"]

FROM base AS api
EXPOSE 8000
CMD ["sh", "-c", "exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]
