# Staging auf wh-coolify

Das Projekt `report-example` mit der Umgebung `staging` ist auf der
Coolify-Instanz wh-coolify angelegt ([ADR 0008](../docs/adr/0008-staging-on-wh-coolify.md)).
Die tatsächlichen Ressourcen, UUIDs, Netzwerk-Aliase, festen Adressen und
privaten HTTPS-Adressen stehen in [.agents/infra/staging/coolify.md](../.agents/infra/staging/coolify.md).
Staging enthält ausschließlich synthetische Daten.

Die fünf Anwendungen liegen im eigenen Docker-Netz `report-example-staging`
mit festem Subnetz. Das Netz ist von den Netzen anderer Projekte getrennt.
PostgreSQL erhält ein eigenes persistentes Volume.

API: https://wh-coolify.tail8fba42.ts.net:15100/docs  
Temporal UI: https://wh-coolify.tail8fba42.ts.net:15101/

Beide Adressen sind nur im Tailnet erreichbar. Keine Anwendung bindet einen
Host-Port. Tailscale Serve auf wh-coolify leitet direkt an die festen Adressen
von API und Temporal UI im Projektnetz weiter. PostgreSQL, Temporal und Worker
haben weder Serve-Route noch öffentliche Domain. Der API-Schlüssel liegt als
Shared Variable `API_TOKEN` an der Umgebung; Prüfungen verwenden ihn im
API-Container, statt ihn aus Coolify auszulesen.

Der [Abnahmenachweis](staging-acceptance.md) enthält die Ergebnisse der
Einrichtung, Verarbeitungs- und Wiederanlauftests.

## Einzelne Ressourcen

Jede der folgenden Rollen ist eine eigenständige Docker-Image-Anwendung.
Compose wird hier nicht verwendet.

| Rolle | Imagequelle | Interner Alias | Port / Daten |
| --- | --- | --- | --- |
| PostgreSQL | `postgres:16.6` | `report-postgres` | 5432 intern; Volume `/var/lib/postgresql/data` |
| Temporal | `temporalio/auto-setup:1.29.7` | `report-temporal` | 7233 intern |
| Temporal UI | `temporalio/ui:2.51.0` | `report-temporal-ui` | 8080; feste Adresse, nur über Tailscale Serve |
| API | `ghcr.io/harald2013/report-example-api:sha-<commit>` | `report-api` | 8000; feste Adresse, nur über Tailscale Serve |
| Worker | `ghcr.io/harald2013/report-example-worker:sha-<commit>` | `report-worker` | Kein eingehender Port |

`<commit>` ist der volle Commit des erfolgreich geprüften Image-Builds.
Für API und Worker dieselbe Revision verwenden. Der Image-Workflow veröffentlicht
auch Feature-Branch-Revisionen, damit Staging keinen Merge voraussetzt. Die
unveränderlichen Image-Digests nach dem Build festhalten und für die Übernahme
nach Produktion verwenden. Der PostgreSQL-Container hält auch die separaten
Datenbanken für Temporals Ausführungshistorie; das ist ausschließlich ein
Demo-/Staging-Aufbau.

## Einrichtung

Schritte am Host von wh-coolify führt der Benutzer aus; Agenten haben dort
keinen SSH-Zugang.

1. Am Host das Netz mit festem Subnetz anlegen, nachdem geprüft wurde, dass
   das Subnetz frei ist:
   `docker network create --attachable --subnet 172.30.0.0/24 report-example-staging`.
   In Coolify unter dem Server eine Destination für dieses Netz hinzufügen.
2. In der Umgebung `staging` die Shared Variables anlegen: `APP_ENV=staging`,
   `TEMPORAL_ADDRESS=report-temporal:7233`, `TEMPORAL_NAMESPACE=default`,
   `TEMPORAL_TASK_QUEUE=reports-v1`, `TEMPORAL_TLS=false` sowie die Secrets
   `POSTGRES_PASSWORD`, `DATABASE_URL` und `API_TOKEN`. Das Passwort
   hexadezimal erzeugen, damit es im `DATABASE_URL` nicht URL-kodiert werden
   muss. Keine Variable als „shown once“ sperren.
3. Die fünf Anwendungen in dieser Destination anlegen. Die automatisch
   vergebene sslip.io-Domain sofort entfernen. Aliase setzen, API und Temporal
   UI erhalten `--ip` mit ihrer festen Adresse in den Docker-Optionen.
   Anwendungsvariablen verweisen auf die Shared Variables; PostgreSQL erhält
   zusätzlich `POSTGRES_USER=reports` und `POSTGRES_DB=reports`, Temporal
   `DB=postgres12`, `DB_PORT=5432`, `POSTGRES_USER=reports`,
   `POSTGRES_SEEDS=report-postgres`, `BIND_ON_IP=0.0.0.0` und
   `DEFAULT_NAMESPACE=default`. Die Temporal UI erhält `TEMPORAL_ADDRESS`.
4. In der Coolify-Oberfläche für PostgreSQL den Healthcheck
   `pg_isready -U reports -d reports` als Kommando und konsistente
   Containernamen einschalten, für die API den Kommando-Healthcheck
   `python -m reports.healthcheck`. Werte danach über die API zurücklesen.
   Für Temporal und Worker keinen HTTP-Healthcheck konfigurieren.
5. PostgreSQL deployen und gesund abwarten, danach Temporal; im Log muss der
   Namespace `default` angelegt sein. Danach Temporal UI, Worker und API.
6. Als einmalige Coolify-Aufgabe im API-Container `python -m reports.store`
   ausführen und `Migration completed` abwarten. Ein Worker, der vor dem
   Schema gestartet ist, wird danach neu gestartet.
7. Am Host von wh-coolify Tailscale Serve einrichten:
   `tailscale serve --bg --https=15100 http://172.30.0.13:8000` und
   `tailscale serve --bg --https=15101 http://172.30.0.12:8080`.

## Prüfung

Über das Tailnet müssen `/ready`, `/ui/` und die Temporal UI HTTP 200 liefern;
ein `POST /reports` ohne gültigen Schlüssel muss 401 liefern.

Authentifizierte Prüfungen laufen als einmalige Coolify-Aufgabe im
API-Container und lesen `API_TOKEN` aus dessen Umgebung, zum Beispiel ein
`POST /reports` an `http://127.0.0.1:8000` und danach `GET /reports/<id>`.
Für einen Wiederanlauftest einen Auftrag mit 60 Sekunden Verzögerung anlegen,
die Worker-Anwendung in Coolify neu starten und prüfen, dass derselbe Auftrag
fertig wird. Den lokalen `--restart-worker`-Schalter nicht gegen Staging
verwenden.

Nach jedem Deployment von API oder Temporal UI prüfen, dass der Container
seine feste Adresse behalten hat und die Serve-Route antwortet.

Die tatsächlich eingerichteten URLs, UUIDs, Aliase und Volumes gehören nach
`.agents/infra/staging/coolify.md`. Aktuelle Versionen und Deployment-Ergebnisse
live prüfen; sie gehören nicht in diese stabile Ressourcenübersicht.

## Abweichung von den aktuellen Deployment-Regeln

Der Aufbau verwendet weiterhin einen separaten Schemajob. Die aktuellen
`development-mcp`-Regeln verlangen für Coolify stattdessen eine Migration aus
dem neuen Image im Entrypoint, vor dem API-Prozess und durch einen
Datenbank-Lock geschützt. Coolifys Pre-Deploy-Befehl läuft im alten Container;
ein fehlgeschlagener Post-Deploy-Befehl verhindert den Rollout nicht. Beide
Phasen eignen sich deshalb nicht als Ersatz.

Das aktuelle API-Image startet noch ohne Migration. Die Entrypoint-Umstellung
und ihr Fehlerfall müssen implementiert und auf Staging geprüft werden, bevor
der Aufbau als regelkonform bezeichnet werden kann. Dazu sind auch die
bisherigen projektweiten Migrationsregeln und ihr ADR gemeinsam anzupassen.
Railways Migration aus dem neuen Image in der nativen Pre-Deploy-Phase bleibt
der vorgesehene Produktionsablauf.

Die Bindung an feste Containeradressen statt an Loopback-Ports ist in
[ADR 0008](../docs/adr/0008-staging-on-wh-coolify.md) begründet.

Für Updates des selbst betriebenen PostgreSQL sind außerdem ein getesteter
Updateplan und ein vom Benutzer genehmigtes Wartungsfenster erforderlich.
Automatische und Rolling-Updates ausschalten; ein explizites Image-Release
verwenden. Die bestehende Stop-vor-Start-Vorgabe gilt weiterhin
([ADR 0005](../docs/adr/0005-stateful-staging-updates.md)).
