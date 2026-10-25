# Staging auf workhorse

Diese Anleitung beschreibt das einzurichtende Setup. Dieses Repository enthält
noch keine angelegten Coolify-Ressourcen. Bestehende IDP-Ressourcen werden nicht
wiederverwendet oder geändert. Staging enthält ausschließlich synthetische Daten.

Vor Coolify-Änderungen die aktuelle Instanzkonfiguration lesen. Beim Anlegen der
ersten Ressourcen `/COOLIFY.md` aus der Development-MCP-Vorlage erstellen, reale
UUIDs und stabile Imagequellen eintragen und mit `validate_coolify_md` prüfen.
Keine UUIDs aus einem anderen Projekt als eigene Ressourcen übernehmen.

## Einzelne Ressourcen

In Coolify auf workhorse ein eigenes Projekt `report-example` mit Umgebung
`staging` anlegen. Jede der folgenden Rollen wird eine eigenständige
Docker-Image-Anwendung. Compose wird hier nicht verwendet.

| Rolle | Imagequelle | Interner Alias | Port / Daten |
| --- | --- | --- | --- |
| PostgreSQL | `postgres:16.6` | `report-postgres` | 5432 intern; Volume `/var/lib/postgresql/data` |
| Temporal | `temporalio/auto-setup:1.29.7` | `report-temporal` | 7233 intern |
| Temporal UI | `temporalio/ui:2.51.0` | `report-temporal-ui` | 8080; nur privater Zugriff |
| API | `ghcr.io/harald2013/hello-world-api:sha-<commit>` | `report-api` | 8000; HTTPS am Proxy |
| Worker | `ghcr.io/harald2013/hello-world-worker:sha-<commit>` | `report-worker` | Kein eingehender Port |

`<commit>` ist der volle Commit des erfolgreich geprüften Image-Builds.
Für API und Worker dieselbe Revision verwenden. Die unveränderlichen Image-Digests
nach dem Build festhalten und für die Übernahme nach Produktion verwenden.
Alle Rollen erhalten ein gemeinsames, nur für Staging vorgesehenes Netz und
die oben genannten Aliase. Datenbank, Temporal und Worker nicht öffentlich
veröffentlichen. Der PostgreSQL-Container hält hier auch die separaten Datenbanken
für Temporals Ausführungshistorie; das ist ausschließlich ein Demo-/Staging-Aufbau.

## Konfiguration und Reihenfolge

1. PostgreSQL: `POSTGRES_USER=reports`, `POSTGRES_DB=reports`, eigenes zufälliges
   `POSTGRES_PASSWORD`. Healthcheck `pg_isready -U reports -d reports`.
2. Temporal nach gesundem PostgreSQL starten: `DB=postgres12`, `DB_PORT=5432`,
   `POSTGRES_USER=reports`, `POSTGRES_PWD` aus dem Secret,
   `POSTGRES_SEEDS=report-postgres`, `BIND_ON_IP=0.0.0.0`,
   `DEFAULT_NAMESPACE=default`. Mit dem Admin-Tools-Image aus Compose die
   Bereitschaft des Namespace prüfen; bis dahin API/Worker nicht starten.
3. Temporal UI mit `TEMPORAL_ADDRESS=report-temporal:7233` starten. Die UI
   ausschließlich privat zugänglich machen.
4. API-/Worker-Konfiguration anhand `staging.env.example` als Coolify-Secrets
   und normale Variablen setzen. Zugangsdaten im Datenbank-URI URL-kodieren.
5. Als einmaligen Job das geprüfte API-Image mit `python -m reports.store`
   im selben Netz und mit denselben Variablen starten. Exitcode 0 abwarten.
   Der Job initialisiert das Schema und ist keine dauerhaft laufende Anwendung.
6. Worker und API starten. API-Healthcheck `GET /ready` auf Port 8000,
   Timeout mindestens 10 Sekunden. Für den Worker keinen HTTP-Healthcheck
   konfigurieren; Prozessüberwachung und erfolgreich verarbeitete Aufträge prüfen.
7. Authentifizierten Smoke-Test gegen die Staging-API ausführen:

```bash
API_BASE_URL=https://STAGING-API API_TOKEN="$STAGING_API_TOKEN" \
  uv run python scripts/smoke.py
```

Für einen Wiederanlauftest einen Auftrag mit 120 Sekunden Verzögerung anlegen,
auf den Datenbankeintrag warten und nur die Worker-Anwendung in Coolify neu
starten. Derselbe Auftrag muss anschließend fertig werden. Den lokalen
`--restart-worker`-Schalter nicht gegen Staging verwenden.

Die tatsächlich eingerichteten URLs, UUIDs, Aliase und Volumes gehören nach
`COOLIFY.md`. Aktuelle Versionen und Deployment-Ergebnisse live prüfen; sie
gehören nicht in diese stabile Ressourcenübersicht.
