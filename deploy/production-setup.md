# Produktionsaufbau am 2026-10-25

## Angelegt und konfiguriert

- Railway-Projekt report-example, Umgebung production, drei Dienste api,
  worker und backup in Amsterdam. IDs stehen im Infrastrukturinventar.
- Neon Free: Projekt report-example, PostgreSQL 16, Datenbank reports mit
  Rolle reports in AWS Frankfurt, 0.25 CU.
- API Pre-Deploy-Migration und Deployment-Healthcheck /ready konfiguriert.
- Ausgerolltes API-Image aus der Staging-Abnahme:
  ghcr.io/harald2013/hello-world-api@sha256:771e6965c0f1a45c428cac86be8c4bdf62636876b850a20a879b4e74d605c721.
- Worker-Digest nach erfolgreichem API-Deployment ausgerollt:
  ghcr.io/harald2013/hello-world-worker@sha256:70e3979beea9e0506b2cc488542fa723b510804188d6cf71cc20207aab7bf325.
- Custom Domain api.report-example.ratzberger.net auf API-Port 8000 angelegt.
- Nicht geheime Runtime-Variablen und R2-Ziel eingetragen. Kein erfolgreicher
  Cloud-Deploymentlauf wird damit behauptet.

## Deploymentnachweise

Nach ausdrücklicher Benutzerfreigabe sind DATABASE_URL und API_TOKEN als Railway-
Secrets übertragen. TEMPORAL_API_KEY ist bei API und Worker vorhanden.

Der erste API-Versuch `8a023489-37ac-4b12-b78b-f46d661b2732` scheiterte im
Pre-Deploy mit OperationalError. Der Neon-Connection-String verwies auf den
Pooler, obwohl dieser deaktiviert war. Alle drei Dienste verwenden jetzt den
direkten Endpoint bei weiterhin vollständiger Zertifikatsprüfung.

API-Deployment `2e834382-cb32-4b8d-bede-a29b822b9ab4` ist erfolgreich:
Migration completed um 20:21:01 UTC, danach App-Start und GET /ready mit 200.
Worker-Deployment `7820d6d5-c7b0-4759-84cb-d8c4004955b7` wurde erst danach
ausgelöst und von Railway als SUCCESS bestätigt.

Ein über Temporal MCP gestarteter synthetischer Bericht
`b625b974-b035-47cf-b064-b9f7e8ba94d6` mit Werten [10,20,30] wurde vom
Railway-Worker verarbeitet: Anzahl 3, Summe 60, Mittelwert 20. Die passende
Neon-Zeile wurde separat mit Status completed und demselben Ergebnis bestätigt. Dieser Nachweis ersetzt keinen HTTP-Test
über die öffentliche API-Domain.

Backupimage nach erfolgreichen CI- und Image-Prüfungen veröffentlicht:
`ghcr.io/harald2013/hello-world-backup@sha256:4385d0245aa9e8dc794dc0529f7f6a21a26560d18582a10cd6be87c5c2aa4dcb`.
Die Quelle ist in Railway vorgemerkt. AWS_ACCESS_KEY_ID und AWS_SECRET_ACCESS_KEY
müssen direkt beim Backup-Dienst gesetzt werden; erst dann den Job aktivieren.

Die Neon-API meldet am neu angelegten Endpoint suspend_timeout_seconds=0.
Explizites Setzen des Intervalls beim Projektanlegen wurde vom Free-Konto mit
HTTP 412 abgewiesen. Automatisches Suspend ist deshalb noch nicht nachgewiesen;
vor Dauerbetrieb in der Neon-Konsole prüfen, damit das Compute-Kontingent reicht.

## DNS bei World4You

| Typ | Name relativ zu ratzberger.net | Wert |
| --- | --- | --- |
| CNAME | api.report-example | 1yha62x4.up.railway.app |
| TXT | _railway-verify.api.report-example | railway-verify=730f21febf635facad9aa4bffc837cce93c8c1ca0f3265b60365e27bdb91a895 |

Werte stammen aus Railways Domain-Antwort. Nach der DNS-Änderung meldet Railway
Ownership verified und CNAME propagated. Die Zertifikatsausstellung scheitert
jedoch mit „Let's Encrypt rate limit reached“, retryable=false. Ein echter
HTTPS-Aufruf bestätigt einen Hostname-Mismatch; die Zertifikatsprüfung bleibt
aktiv. HTTP-Smoke und öffentliche Freigabe warten deshalb auf ein gültiges
Zertifikat. Nicht wiederholt neu anfordern, solange Railway keinen Retry erlaubt. Der TXT-Wert ist ein öffentlicher DNS-Nachweis, kein API-Secret.

## Offene Abnahme

Authentifizierter HTTP-Report über die eigene Domain, R2-Upload, echte
Wiederherstellung in isolierter Datenbank sowie
Fehler- und Backup-Frischealarme stehen aus. Die 24-Stunden-Ziele sind daher noch
nicht als erfüllt nachgewiesen. Keine Fehlermigration gegen Produktion ausführen.
