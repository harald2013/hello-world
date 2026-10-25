# Produktion: Railway, Temporal Cloud, Neon und R2

[ADR 0006](../docs/adr/0006-railway-production.md) legt das aktuelle Zielbild fest.
Render entfällt vollständig. Railway betreibt drei getrennte vorgebaute Images:
API, Worker und einen beendenden Backup-Job. Staging bleibt auf workhorse.

## Gewählte Betriebsparameter

- Railway Hobby; Monatsbudget insgesamt 50 Euro, Verbrauch zusätzlich zum
  enthaltenen Guthaben beobachten. Keine garantierte Kostenobergrenze.
- Railway Amsterdam; Neon Free AWS Frankfurt, Compute zunächst 0.25 CU.
- Temporal-Namespace `default-namespace.rq4it`, Endpoint
  `default-namespace.rq4it.tmprl.cloud:7233` (Benutzerangabe).
- API-Domain `api.report-example.ratzberger.net`, DNS bei World4You.
- RPO und RTO jeweils 24 Stunden. Höchstens 100 Demo-Berichte täglich.
- Backups alle zwölf Stunden (`0 */12 * * *`, UTC), sieben Tage Aufbewahrung.
- R2: privater EU-Bucket `default-bucket`, Präfix `report-example/production/`.
  Endpoint: `https://960c285a06dcb6cb9a4f8212c9b5ae46.eu.r2.cloudflarestorage.com`.

Konkreter Aufbau und offene Nachweise: [production-setup.md](production-setup.md).

Bestehende IDs: [.agents/infra](../.agents/infra/README.md). Darin stehen keine
laufenden Image-Versionen oder Secrets. Tatsächliche Deploymentnachweise werden
separat erfasst. Ein angelegter Dienst ist noch kein erfolgreiches Deployment.

## Einrichtung und Reihenfolge

1. Neon-Datenbank und Temporal-Zugang vorbereiten. `DATABASE_URL` verwendet
   `sslmode=verify-full`; `PGSSLROOTCERT=/etc/ssl/certs/ca-certificates.crt`.
2. API und Worker erhalten die Runtime-Werte aus `production.env.example`.
   `TEMPORAL_API_KEY` und `API_TOKEN` sind Secrets; Produktions-TLS einschalten.
3. API: geprüften Staging-Digest verwenden, PORT=8000; native Pre-Deploy-Phase
   `/app/.venv/bin/python -m reports.store`; Healthcheck `/ready`.
4. Erst nach erfolgreicher Migration und API-Readiness das passende Workerimage
   ausrollen. Kein Worker-Pre-Deploy, keine öffentliche Domain, kein Serverless-
   Sleep für API oder Worker. Keine Repository-Builds auf Railway.
5. Backup-Service: geprüftes Backupimage, kein HTTP-Port, Cron `0 */12 * * *`,
   Restart-Policy NEVER. Prozess endet nach Dump, Uploadprüfung und Bereinigung.
   `DATABASE_URL`, `PGSSLROOTCERT`, `BACKUP_ENDPOINT`, `BACKUP_BUCKET`,
   `BACKUP_PREFIX`, `BACKUP_RETENTION_DAYS=7`, `AWS_DEFAULT_REGION=auto` setzen.
   `AWS_ACCESS_KEY_ID` und `AWS_SECRET_ACCESS_KEY` direkt als Secrets hinterlegen.
6. Nur API öffentlich routen; die von Railway gelieferten CNAME- und
   Ownership-TXT-Einträge bei World4You setzen und TLS-Status prüfen.

`/ready` prüft Neon und Temporal; Railway fragt ihn nur beim Deployment ab.
Für häufige externe Prozessüberwachung `/health` verwenden. Das Suspend-Verhalten
und die Compute-Auslastung in Neon vor Freigabe prüfen: ein dauerhaft aktiver
0.25-CU-Endpoint überschreitet im vollen Monat das kostenlose Kontingent.

## Backup und Wiederherstellung

Das Backupimage enthält PostgreSQL-16-Clients und boto3. Secrets stehen in
Umgebungsvariablen, nicht in Prozessargumenten oder Logs. Der Dump wird vor dem
Upload mit pg_restore gelesen; anschließend werden Größe und SHA256-Metadaten
am Objekt geprüft. Dies ersetzt keine echte Restore-Probe. Alte Dumps werden
nur unter dem reservierten Projektpräfix nach erfolgreichem Upload entfernt.
Andere Bucket-Inhalte und dessen allgemeine Lifecycle-Regeln bleiben unberührt.

Für die Restore-Probe aus einer berechtigten Cloud-Umgebung einen Dump laden,
dessen SHA256 prüfen und mit `pg_restore --no-owner --no-acl` in eine isolierte
Testdatenbank einspielen. Gespeicherte Berichte mit dem Ausgangsbestand vergleichen.
Nicht auf Entwicklerrechner herunterladen und nicht die Produktionsdatenbank
überschreiben. Wiederherstellungsdauer dokumentieren und Testdatenbank kontrolliert
entfernen. Anschließend einen neuen Report vollständig verarbeiten.

## Abnahme und Benachrichtigungen

- Authentifizierten Report vollständig ausführen; ohne Token muss POST 401 liefern.
- Migrationsfehler in separater Testumgebung muss das neue Release stoppen und
  die bisherige API erhalten. Siehe [migrations.md](migrations.md).
- Ersten echten R2-Upload und Restore nachweisen.
- Railway-Fehlerbenachrichtigungen an die vom Benutzer bestätigte Kontoadresse
  einrichten und testen. Die frühere Render-Zustimmung allein konfiguriert Railway
  nicht. Zusätzlich ausbleibende Backups erkennen, bevor das jüngste Backup
  24 Stunden alt ist. Fehler-Exitcodes allein erkennen keinen ausgefallenen Cron.
- Erst danach gilt die Produktion als abgenommen; kostenpflichtige Zusatzdienste
  für Überwachung nur innerhalb des vereinbarten Budgets auswählen.

Quellen: [Railway Pre-Deploy](https://docs.railway.com/deployments/pre-deploy-command),
[Healthchecks](https://docs.railway.com/deployments/healthchecks),
[Cron Jobs](https://docs.railway.com/cron-jobs),
[Regionen](https://docs.railway.com/deployments/regions).
