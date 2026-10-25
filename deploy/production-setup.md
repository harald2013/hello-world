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
- Runtime-Konfiguration und R2-Secrets sind eingetragen; Deploymentnachweise folgen unten.

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
R2-Secrets sind inzwischen beim Backup-Dienst hinterlegt. Der erste tatsächliche
Einmallauf (`bce44073-570c-4b8b-9f42-d294c28b710b`) scheiterte beim pg_dump:
libpq expandiert eine vollständige Verbindungs-URL aus PGDATABASE nicht und suchte
deshalb einen lokalen Unix-Socket. Der Backup-Code setzt jetzt einzelne
PGHOST-/PGPORT-/PGUSER-/PGPASSWORD-/PGDATABASE-Variablen und prüft TLS weiterhin
vollständig. Ein lokaler Gegenversuch reproduzierte den Socket-Fehler, und drei
neue Regressionstests prüfen URL-Dekodierung und die strikte TLS-Konfiguration.
Die korrigierte Image-Version aus Revision 7b7f838232db6f570752eafbda3e2ed59de469da
ist veröffentlicht (Image-Prüfung 40231699246 erfolgreich):
`ghcr.io/harald2013/hello-world-backup@sha256:503d572aa9d4125bdb6280156051b4691c67566e5b755a4b21494c17a44f421b`.

Einmallauf `e69168e3-63a1-4e65-b3c0-7f2787abf0c9` meldet am 25.10.2026 um
20:42:06 UTC `Backup completed`. Das Archiv wurde in R2 gespeichert:
`report-example/production/2026/10/25/204202-84dc9a9cf47546f9a9b5b865fddb1d02.dump`.
SHA256: `72c72d74c07567cd065a033b787d38b80509b4d10f2737b410b2e1a3e6fe8344`.

Restore-Lauf `c56bf2b9-d931-498e-97d3-632b6eb8837d` lädt das Archiv direkt im
Railway-Container, prüft die SHA256 und spielt es ausschließlich in die frische
Neon-Testdatenbank reports_restore_check_20261025 ein. Der Prozess meldet
`Restore verified` und zwei Sekunden Laufzeit; anschließend wurde der bekannte
Bericht über Neon separat mit Status completed und Summe 60 bestätigt.
Die Testdatenbank wurde danach entfernt; die Datenbankliste enthält wieder nur reports. Es wurde kein Dump auf einen
Entwicklerrechner übertragen. Dies ist eine erfolgreiche Probe für den kleinen
Demobestand, keine pauschale RTO-Garantie für beliebige Datenmengen.

Der normale Startbefehl ist wieder `python3 /app/backup.py`, Cron
`0 */12 * * *` (UTC) und Restart-Policy NEVER. Kein permanenter Backup-Prozess.
Ein erfolgreich registriertes Cron-Deployment allein beweist keinen Lauf;
maßgeblich sind Ausführungslogs und das nachprüfbare Archiv.

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

Authentifizierter HTTP-Report über die eigene Domain, Fehler- und Backup-
Frischealarme sowie Release-Fehlerisolation in einer separaten Testumgebung
stehen aus. Upload und isolierte Wiederherstellungsprobe sind nachgewiesen. Die 24-Stunden-Ziele sind daher noch
nicht als erfüllt nachgewiesen. Keine Fehlermigration gegen Produktion ausführen.

## UI-Aktualisierung

Die UI wird nach der Prüfung derselben Images in Coolify auf Railway übernommen.
Aktuelle UI-Rollout-Digests, Plattform-IDs und Prüfergebnisse stehen in
[ui-acceptance.md](ui-acceptance.md). Die ursprünglichen Deployment-IDs weiter
oben dokumentieren den ersten Aufbau.
