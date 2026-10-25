# Gemanagte Produktion

Ziel ist der Betrieb eigener Anwendungscode-Images ohne selbst administrierte
Produktionsserver. API und Worker laufen im gewählten Beispiel auf Render (Railway bleibt Alternative),
Prozesssteuerung in Temporal Cloud, Anwendungsdaten in Neon. workhorse ist für
Laufzeit und Wiederherstellung der Produktion keine Abhängigkeit.

Diese Anleitung legt keine kostenpflichtigen Ressourcen an. Die Verteilung ist
in [ADR 0006](../docs/adr/0006-managed-cloud-placement.md) beschlossen.
Tarife, Verfügbarkeitszusagen und Wiederherstellungsziele bleiben vor dem echten
Setup festzulegen. Die Bezeichnungen der Dienste garantieren diese Eigenschaften
nicht.

## Abgestimmter Deploymentplan

| Baustein | Lokal | Staging: Coolify auf workhorse | Produktion |
| --- | --- | --- | --- |
| FastAPI API | Compose | Einzelnes API-Image | Render Web Service |
| Python-Worker | Compose | Einzelnes Worker-Image | Render Background Worker |
| Temporal-Server | Compose | Einzelnes Temporal-Image | Temporal Cloud |
| Anwendungsdatenbank | Compose | PostgreSQL-Image mit Volume | Neon |
| Temporal-Oberfläche | Compose | Einzelnes UI-Image | Temporal Cloud Console |
| Migration | Einmaliger Compose-Job | Temporärer Container | Render Pre-Deploy |

Zielregion ist **Frankfurt**: Render Frankfurt, Temporal Cloud AWS
`eu-central-1` und Neon AWS Frankfurt. Verfügbarkeit beim Anlegen prüfen:
[Render](https://render.com/docs/regions),
[Temporal Cloud](https://docs.temporal.io/evaluate/cloud/regions),
[Neon](https://neon.com/docs/introduction/regions).
Anbieterübergreifende Verbindungen verwenden TLS; ein gemeinsames privates
Netzwerk wird nicht vorausgesetzt.

Vor der kostenpflichtigen Einrichtung sind diese Punkte offen:

- Monatliches Budget und konkrete Tarife für alle drei Anbieter.
- Domain beziehungsweise bewusste Verwendung der Render-Domain.
- Maximal tolerierbarer Datenverlust (RPO) und Wiederherstellungszeit (RTO),
  daraus abgeleitete Backup-Aufbewahrung und Wiederherstellungstests.

Einrichtungsreihenfolge: Neon, Temporal Cloud, Render API samt erfolgreicher
Pre-Deploy-Migration, anschließend Render Worker. Danach folgen der vollständige
Report-Test, die Prüfung eines fehlgeschlagenen Migrations-Deployments und ein
Wiederherstellungstest. Produktionsressourcen sind noch nicht angelegt.

Bei vorgebauten Images werden Releases ausdrücklich über CI/API oder das
Dashboard ausgelöst. Ein neuer GHCR-Push löst allein kein Render-Deployment aus.
Die Automatisierung muss erst den API-Erfolg abwarten und danach den Worker
aktualisieren. Sie übernimmt die in Staging geprüften Digests ohne Neubau.
Siehe [Render Deployments](https://render.com/docs/deploys).

## Gemeinsame Vorbereitung

1. In Temporal Cloud einen eigenen Produktions-Namespace und passenden
   Service-Account/API-Key anlegen. Namespace und Endpoint aus dessen Konsole
   übernehmen. Der Server läuft in Temporal Cloud; unser Worker läuft beim
   Anwendungsanbieter und verbindet sich ausgehend per TLS.
2. Eine eigene Neon-Produktionsdatenbank anlegen. Einen zur gewählten Region
   passenden, zunächst direkten PostgreSQL-Endpoint verwenden. Zertifikatsprüfung
   mit `sslmode=verify-full` und dem System-CA-Bundle einschalten. Den Connection
   String einschließlich URL-kodierter Zugangsdaten als Secret speichern.
3. Die erfolgreich in Staging geprüften API- und Workerimage-Digests aus GHCR
   übernehmen. Für Produktion keine Images neu bauen und keine veränderlichen
   `latest`-Tags verwenden. Registry-Zugriff beim Anbieter hinterlegen.
4. `production.env.example` in Anbieter-Secrets und normale Variablen übertragen.
   Für Produktion eigene Zugangsdaten verwenden. Einen zufälligen API-Schlüssel
   mit mindestens 32 Zeichen vergeben und nur berechtigten Clients geben.
5. Im API-Dienst die native Pre-Deploy-Phase für **jedes** Deployment gemäß
   [Migrationsanleitung](migrations.md) konfigurieren. Sie verwendet das neue
   API-Image und dessen Runtime-Variablen, auch beim ersten Deployment. Kein
   zusätzlicher Dauer-Service und keine Migration im normalen Startbefehl.

## Gewählt: Render

- API als **Web Service / Existing Image** aus dem geprüften APIimage-Digest
  anlegen. Der vorhandene Startbefehl bindet an `0.0.0.0` und berücksichtigt
  `PORT`. HTTPS und Routing übernimmt Render. Healthcheck-Pfad `/ready`.
- Worker als **Background Worker / Existing Image** aus dem geprüften
  Workerimage-Digest anlegen. Standardbefehl unverändert lassen; kein
  eingehender Port und kein öffentlicher Webdienst sind erforderlich.
- Im API-Dienst `/app/.venv/bin/python -m reports.store` als Pre-Deploy Command setzen
  (bei Render für bezahlte Dienste verfügbar). Der Befehl muss erfolgreich
  enden, bevor die neue API-Version startet. Worker-Releases separat nach
  erfolgreichem API-Deployment auslösen; die Plattform koordiniert beide Dienste
  nicht automatisch. Eine lokale Entwicklungsmaschine erhält dafür keine
  Produktionsdaten oder Dumps.

Render unterstützt vorgebaute Images und Hintergrund-Worker:
[Images](https://render.com/docs/deploying-an-image),
[Background Workers](https://render.com/docs/background-workers),
[Pre-Deploy Command](https://render.com/docs/deploys#pre-deploy-command).

## Alternative Railway (nicht eingerichtet)

- Zwei getrennte Dienste aus den vorgebauten API-/Workerimages erstellen;
  keine Builds aus dem Repository konfigurieren.
- API: öffentliche HTTPS-Domain, Healthcheck `/ready`, Startbefehl aus dem Image
  und den vom Anbieter gelieferten `PORT` verwenden.
- Worker: Standardbefehl aus dem Workerimage verwenden, keine öffentliche Domain.
- Im API-Dienst `/app/.venv/bin/python -m reports.store` als Pre-Deploy Command setzen und
  dessen Erfolg vor dem ersten Worker-Start abwarten.

Die konkreten Image-/Registry- und Job-Einstellungen beim Setup anhand der
[Railway-Dokumentation](https://docs.railway.com/services) und
[Pre-Deploy Command](https://docs.railway.com/deployments/pre-deploy-command) prüfen.
Render und Railway sind Alternativen; das Beispiel benötigt nur einen davon.

## Freigabe

Mit dem Produktions-API-Schlüssel den Smoke-Test aus einer berechtigten
Cloud-/CI-Umgebung ausführen. Logs und Fehleralarme der Anbieter einschalten,
Backup-Aufbewahrung und Wiederherstellung bei Neon prüfen und einen
Wiederherstellungstest durchführen. Die erste Bereitstellung ist erst nach
diesen Prüfungen als abgeschlossen zu dokumentieren.

Weitere Grundlagen: [Temporal Cloud](https://docs.temporal.io/cloud),
[Neon-Verbindungen](https://neon.com/docs/connect/connect-from-any-app).
