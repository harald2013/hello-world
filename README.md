# Report example

Portable Python-Vorlage für eine FastAPI-API, einen Temporal-Worker und PostgreSQL.
Die API nimmt Zahlen entgegen; ein langlebiger Workflow berechnet und speichert
einen Bericht. Lokal laufen separate Images mit Compose, Staging verwendet
Einzelimages in Coolify auf workhorse. Produktion nutzt Railway, Temporal Cloud,
Neon und unabhängige Backups in Cloudflare R2.

## Start und Prüfung

```bash
uv sync --locked
cp .env.example .env
docker compose up --build -d --wait --wait-timeout 240
uv run python scripts/smoke.py
./scripts/verify
```

Die Anwendung liegt in `reports/`, Tests in `tests/`, der Backup-Job in `ops/`.
Das Dockerfile enthält getrennte Build-Ziele für API, Worker und Backups.

- [README.extended.md](README.extended.md): für API-Beispiele und lokale Betriebsdetails lesen.
- [Produktion](deploy/production.md): für Railway, Migrationen, Backups und Abnahme lesen.
- [Staging](deploy/staging.md): für den Betrieb der Einzelimages auf workhorse lesen.
- [Infrastruktur](.agents/infra/README.md): vor Zugriffen auf vorhandene Cloud-Ressourcen lesen.
- [Architekturregeln](AGENT_RULES.md): vor Änderungen am Projekt lesen.

Dummy-Zeile für einen Test-PR (kann gelöscht werden).
