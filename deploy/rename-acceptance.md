# Umbenennung in report-example am 2026-10-26

Das Repository `harald2013/hello-world` heißt seit 2026-10-26
`harald2013/report-example` (TIL-181). Der Image-Workflow bildet die Namen aus
dem Repository und veröffentlicht seitdem unter
`ghcr.io/harald2013/report-example-{api,worker,backup}`. Die früheren Packages
`hello-world-*` bleiben für Rollbacks auf ältere Digests erhalten; kein Dienst
nutzt sie mehr.

Revision: `e477bf2b73eea51fbc0fe086d01b636a89e98837`. Gegenüber dem
UI-Rollout ändern sich nur Projektname und UI-Titel; das Schema bleibt gleich.
Alle drei Images sind öffentlich und ohne Anmeldung abrufbar.

| Rolle | Digest |
| --- | --- |
| API | ghcr.io/harald2013/report-example-api@sha256:bd34658ff549699a4b4915d4506709665794809586c7d4e534268ebdc5ebbadc |
| Worker | ghcr.io/harald2013/report-example-worker@sha256:8a27f960960285ef5e22f8c925550df5f0b8a7ccb7462e3792171d6f4c8d7657 |
| Backup | ghcr.io/harald2013/report-example-backup@sha256:169d9a8cf6bd7f8b25ae805e7f30edf057cf841285e41d416fccb0b5f333c4d0 |

## Staging

Coolify API-Deployment `ukiod4fjvootwnfam9dkzrdt` und Worker-Deployment
`mt26qsupbrz4uzz4a9kj5zmd` sind finished; die API ist healthy und weiter nur
über `127.0.0.1:18080` gebunden. PostgreSQL und Temporal blieben unverändert.

Der Smoke-Test lief im API-Container, ohne den Schlüssel auszulesen: Report
`dda15d14-c2bb-4d6a-a2fa-76e7630cca27` wurde fertig und das Ergebnis in der
Datenbank bestätigt. `/ui/` über das Tailnet zeigt „Report example“; POST
`/reports` ohne Token liefert 401.

## Produktion

Jeder Dienst wurde einzeln vorgemerkt, der Patch geprüft und übernommen.

- API-Deployment `61414a50-44d7-45c3-877a-41bfec680cfa` ist SUCCESS:
  Migration completed um 08:32:14 UTC, danach App-Start und GET /ready mit 200.
- Worker-Deployment `70dbd8e7-301f-4ce7-aa0d-c20c15fb6fa2` wurde erst danach
  ausgelöst und ist SUCCESS.
- Cloud-Testbericht `7beff492-1af4-4ef4-91d2-9e57a6db13b0` über Temporal Cloud
  liefert Anzahl 3, Summe 60, Mittelwert 20; die Neon-Zeile ist unabhängig mit
  Status completed und demselben Ergebnis bestätigt.
- Backup-Deployment `84b6148d-1f6c-40bf-a2f5-0a9e03c0d1c3` ist SUCCESS; Cron
  `0 */12 * * *` UTC bleibt gesetzt. `ops/backup.py` ist unverändert, das
  Image wurde aber neu gebaut und installiert seine apt-Pakete frisch. Ein Lauf
  mit dem neuen Image ist noch nicht nachgewiesen: Der nächste reguläre Cron-Lauf
  muss `Backup completed` melden und ein Archiv unter
  `report-example/production/` ablegen.

Das TLS-Zertifikat der eigenen Domain fehlt weiterhin (TIL-178); ein HTTP-Smoke
über die öffentliche Domain ist deshalb nicht Teil dieses Nachweises.
