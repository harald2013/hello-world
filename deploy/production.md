# Gemanagte Produktion

Ziel ist der Betrieb eigener Anwendungscode-Images ohne selbst administrierte
Produktionsserver. API und Worker laufen auf Render **oder** Railway,
Prozesssteuerung in Temporal Cloud, Anwendungsdaten in Neon. workhorse ist für
Laufzeit und Wiederherstellung der Produktion keine Abhängigkeit.

Diese Anleitung legt keine kostenpflichtigen Ressourcen an. Regionen, Tarife,
Verfügbarkeitszusagen und Wiederherstellungsziele sind vor dem echten Setup zu
wählen. Die Bezeichnungen der Dienste garantieren diese Eigenschaften nicht.

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
5. Vor dem ersten Start mit dem API-Image `python -m reports.store` als einmaligen
   Job ausführen. Dieselben Datenbank-/Temporal-Umgebungsvariablen setzen; der
   Befehl prüft die Produktionskonfiguration und legt das Anwendungsschema an.

## Variante Render

- API als **Web Service / Existing Image** aus dem geprüften APIimage-Digest
  anlegen. Der vorhandene Startbefehl bindet an `0.0.0.0` und berücksichtigt
  `PORT`. HTTPS und Routing übernimmt Render. Healthcheck-Pfad `/ready`.
- Worker als **Background Worker / Existing Image** aus dem geprüften
  Workerimage-Digest anlegen. Standardbefehl unverändert lassen; kein
  eingehender Port und kein öffentlicher Webdienst sind erforderlich.
- Im API-Dienst `python -m reports.store` als Pre-Deploy Command setzen
  (bei Render für bezahlte Dienste verfügbar). Der Befehl muss erfolgreich
  enden, bevor API und anschließend Worker starten. Eine lokale
  Entwicklungsmaschine erhält dafür keine Produktionsdaten oder Dumps.

Render unterstützt vorgebaute Images und Hintergrund-Worker:
[Images](https://render.com/docs/deploying-an-image),
[Background Workers](https://render.com/docs/background-workers),
[Pre-Deploy Command](https://render.com/docs/deploys#pre-deploy-command).

## Variante Railway

- Zwei getrennte Dienste aus den vorgebauten API-/Workerimages erstellen;
  keine Builds aus dem Repository konfigurieren.
- API: öffentliche HTTPS-Domain, Healthcheck `/ready`, Startbefehl aus dem Image
  und den vom Anbieter gelieferten `PORT` verwenden.
- Worker: Standardbefehl aus dem Workerimage verwenden, keine öffentliche Domain.
- Im API-Dienst `python -m reports.store` als Pre-Deploy Command setzen und
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
