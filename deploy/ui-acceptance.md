# UI-Rollout am 2026-10-25

Revision: `7c8e93577b8941a44654edfa70829661ca2db185`.
[Erfolgreiche Image-Veröffentlichung](https://github.com/harald2013/hello-world/actions/runs/40234054553).
32 Python-Tests, Browserprüfungen und ein echter lokaler Report-Durchlauf sind
für diese UI bereits durchgeführt.

## Unveränderte Images für Staging und Produktion

| Rolle | Digest |
| --- | --- |
| API | ghcr.io/harald2013/hello-world-api@sha256:6be1c7bc67ebd77e2f5431c0d849493703655cbd8ae8be8909e1fa492d6dae0c |
| Worker | ghcr.io/harald2013/hello-world-worker@sha256:9ad64e911c88e1f7c48cb707cc01a806b8046e1e990eb2937763ddb4773622bd |

## Staging

Coolify API-Deployment `rjv9phfbajdxzzj9ocrcksrw` und Worker-Deployment
`0idsshochs45os0uziyw9zw1` sind finished. Nur die Anwendungstags wurden geändert;
PostgreSQL und Temporal blieben bestehen.

Über die gültige Tailnet-HTTPS-Adresse wurde /ui/ mit Hello World und wurden die
CSS-/JavaScript-Dateien jeweils mit HTTP 200 geprüft. Ein unauthentifizierter
Report-Aufruf liefert 401. Ein authentifizierter Bericht wurde innerhalb des
API-Containers gestartet, ohne den Schlüssel auszulesen oder auszugeben.
Report `674f0373-51c8-40d1-867b-f1fb791a90b9` wird fertig, Summe 60 und Mittelwert 20.

UI: https://workhorse.tail8fba42.ts.net:18443/ui/

## Produktion

Die API wird zuerst mit nativer Pre-Deploy-Migration aktualisiert. Erst nach
Migrationserfolg und erfolgreicher Readiness wird der passende Worker ausgerollt.
API-Deployment `dd8c24a9-d61b-487b-a3f4-93b6b4543a39` ist SUCCESS:
Migration completed um 21:35:37 UTC, danach App-Start und GET /ready mit 200.
Worker-Deployment `bc438f66-6d72-43bd-b4c5-d181715ed29f` wurde anschließend
mit SUCCESS bestätigt. Beide Dienste verwenden die oben in Staging geprüften
Digests. Der Backup-Dienst wurde bei diesem Rollout nicht geändert.

Cloud-Testbericht `a0b0c98c-db11-4179-8aaa-ec9e5e385061` wurde nach dem
Worker-Rollout über Temporal Cloud gestartet und liefert Anzahl 3, Summe 60,
Mittelwert 20. Die fertige Neon-Zeile wurde unabhängig überprüft.

UI-Pfad: https://api.report-example.ratzberger.net/ui/
DNS ist bestätigt; Railway meldet für das Zertifikat weiterhin ein Let's-Encrypt-
Limit mit retryable=false. Der öffentliche Browserzugriff wird daher noch nicht
als erfolgreich behauptet. Es wird kein TLS-Check deaktiviert.
