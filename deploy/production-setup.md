# Produktionsaufbau am 2026-10-25

## Angelegt und konfiguriert

- Railway-Projekt report-example, Umgebung production, drei Dienste api,
  worker und backup in Amsterdam. IDs stehen im Infrastrukturinventar.
- Neon Free: Projekt report-example, PostgreSQL 16, Datenbank reports mit
  Rolle reports in AWS Frankfurt, 0.25 CU.
- API Pre-Deploy-Migration und Deployment-Healthcheck /ready konfiguriert.
- API-Image aus der Staging-Abnahme als ausstehende Railway-Änderung vorgemerkt:
  ghcr.io/harald2013/hello-world-api@sha256:771e6965c0f1a45c428cac86be8c4bdf62636876b850a20a879b4e74d605c721.
- Worker-Digest erst nach API-Erfolg verbinden:
  ghcr.io/harald2013/hello-world-worker@sha256:70e3979beea9e0506b2cc488542fa723b510804188d6cf71cc20207aab7bf325.
- Custom Domain api.report-example.ratzberger.net auf API-Port 8000 angelegt.
- Nicht geheime Runtime-Variablen und R2-Ziel eingetragen. Kein erfolgreicher
  Cloud-Deploymentlauf wird damit behauptet.

## Noch vor dem Start

Die automatische Freigabeprüfung hat die Übertragung der neu angelegten Neon-
Zugangsdaten und des neu erzeugten API-Tokens zu Railway abgewiesen. Die explizite
Benutzerfreigabe dafür ist angefragt. Diese Secrets sind daher noch nicht gesetzt.
TEMPORAL_API_KEY muss für API und Worker aus den Benutzer-Secrets verfügbar sein;
versiegelte Werte nicht auslesen oder überschreiben.

Der Backup-Dienst benötigt AWS_ACCESS_KEY_ID und AWS_SECRET_ACCESS_KEY direkt als
Railway-Secrets. Kein Secret gehört in dieses Dokument. Backupimage erst nach
Build/Tests veröffentlichen und dessen geprüften Digest verwenden.

Die Neon-API meldet am neu angelegten Endpoint suspend_timeout_seconds=0.
Explizites Setzen des Intervalls beim Projektanlegen wurde vom Free-Konto mit
HTTP 412 abgewiesen. Automatisches Suspend ist deshalb noch nicht nachgewiesen;
vor Dauerbetrieb in der Neon-Konsole prüfen, damit das Compute-Kontingent reicht.

## DNS bei World4You

| Typ | Name relativ zu ratzberger.net | Wert |
| --- | --- | --- |
| CNAME | api.report-example | 1yha62x4.up.railway.app |
| TXT | _railway-verify.api.report-example | railway-verify=730f21febf635facad9aa4bffc837cce93c8c1ca0f3265b60365e27bdb91a895 |

Werte stammen aus Railways Domain-Antwort. DNS-Verbreitung und Zertifikat sind
noch zu prüfen. Der TXT-Wert ist ein öffentlicher DNS-Nachweis, kein API-Secret.

## Offene Abnahme

Erfolgreiche Migration, API-Rollout und danach Worker-Rollout, authentifizierter
Report, R2-Upload, echte Wiederherstellung in isolierter Datenbank sowie
Fehler- und Backup-Frischealarme stehen aus. Die 24-Stunden-Ziele sind daher noch
nicht als erfüllt nachgewiesen. Keine Fehlermigration gegen Produktion ausführen.
