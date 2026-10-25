# Konfiguration und Betrieb

| Variable | Bedeutung |
| --- | --- |
| `APP_ENV` | `local`, `test`, `staging`, `production` |
| `DATABASE_URL` | PostgreSQL-Verbindung; in Produktion mit `sslmode=verify-full` und CA-Bundle |
| `TEMPORAL_ADDRESS` | gRPC-Endpoint mit Port |
| `TEMPORAL_NAMESPACE` | Getrennter Namespace pro Umgebung |
| `TEMPORAL_TASK_QUEUE` | `reports-v1`; API und Worker müssen denselben Wert verwenden |
| `TEMPORAL_TLS` | In Produktion `true` |
| `TEMPORAL_API_KEY` | API-Key für Temporal Cloud; in Produktion erforderlich |
| `API_TOKEN` | Bearer-Token; in Staging/Produktion mindestens 32 Zeichen |
| `PORT` | API-Port im Container, Standard 8000 |

API-Aufrufe mit Authentifizierung senden `Authorization: Bearer <API_TOKEN>`.
Gesundheitsprüfungen enthalten keine Daten und bleiben ohne Token erreichbar.
`/health` prüft nur den API-Prozess. `/ready` prüft Schema und Temporal-Service;
ein gesunder Temporal-Service beweist nicht, dass ein Worker Aufträge abarbeitet.
Der Smoke-Test prüft deshalb den vollständigen Weg bis zum gespeicherten Ergebnis.

Schema-Initialisierung ist wiederholbar und wird separat ausgeführt. Das erste
Schema verwendet eine additive Tabelle. Spätere Schemaänderungen benötigen
versionierte Migrationen mit Rückwärtskompatibilität; `CREATE TABLE IF NOT EXISTS`
aktualisiert keine bestehende Tabelle.

## Version übernehmen und zurücksetzen

1. Image-Workflow baut und prüft eine Revision und veröffentlicht ihre zwei Images.
2. In Staging genau diese Images starten und den Smoke-/Wiederanlauftest ausführen.
3. Image-Digests sowie Konfiguration der letzten guten Version im Release-Nachweis
   festhalten. In Produktion dieselben Digests einsetzen.
4. Bei einem Fehler API und Worker auf das vorherige geprüfte Image-Paar setzen.
   Datenbanken und Temporal-Historien nicht löschen. Danach `/ready` und den
   Smoke-Test prüfen. Ein fehlgeschlagener Workflow wird durch den Image-Rollback
   allein nicht erneut gestartet.

Die Vorlage enthält ein deterministisches Workflow-Verhalten. Änderungen daran
benötigen History-Replay und gegebenenfalls Workflow-Versionierung vor dem Rollout.
Ein Image-Rollback ist keine automatische Daten- oder Schema-Rücksetzung.

## Umgebung trennen

Lokale und Staging-Daten sind synthetisch. Produktionsdaten, Dumps und
produktive Logs bleiben in den vorgesehenen Cloud-Systemen. Accounts, Secrets,
Datenbanken und Temporal-Namespaces werden getrennt gehalten. Die erste Vorlage
verwendet einen gemeinsamen API-Schlüssel; Benutzerverwaltung, Rechte pro Bericht,
Rate-Limits und automatische Produktions-Releases sind weitere Ausbauschritte.
