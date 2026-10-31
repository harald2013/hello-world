# Neon Auto-Suspend und Compute-Kontingent am 2026-10-31

Ticket TIL-218. Alle Werte wurden am 2026-10-31 zwischen 14:28:39 UTC
(Linear-Startkommentar) und 14:33:51 UTC (Commit dieses Nachweises) live und nur
lesend über den Neon-MCP und den Railway-MCP abgefragt. Projekt
`raspy-bar-83546186`, Endpoint `ep-weathered-rain-b9sk6ls0`, Plan Free
(`free_v3`). IDs stehen im [Neon-Inventar](../.agents/infra/production/neon.md).

## Ergebnis

- Auto-Suspend ist aktiv. Der Endpoint suspendiert nach 5 Minuten (300 s) ohne
  Abfragen. Auf Free lässt sich das weder ändern noch abschalten.
- Das Free-Kontingent von 100 CU-Stunden pro Projekt und Monat reicht für den
  Dauerbetrieb. Hochgerechnet verbraucht der aktuelle Betrieb etwa 1,3 CU-Stunden
  pro Monat, also rund 1,3 % des Kontingents.
- Optionen für einen Planwechsel sind deshalb nicht nötig; eine Einordnung für
  den Fall dauerhafter Aktivität steht unten.

## Auto-Suspend

| Beleg | Befund |
| --- | --- |
| `get_postgres_endpoint` | `suspend_timeout_seconds=0`, `autoscaling_limit_min_cu=0.25`, `autoscaling_limit_max_cu=0.25`, Zustand `idle`, `last_active` 2026-10-31 12:03:21 UTC, `suspended_at` 2026-10-31 12:08:31 UTC |
| `describe_project` | `default_endpoint_settings.suspend_timeout_seconds=0` |
| Neon-Dokumentation | `0` bedeutet den globalen Standardwert von 300 s, `-1` heißt nie suspendieren ([CLI branches](https://neon.com/docs/cli/branches), [AI Agent integration guide](https://neon.com/docs/guides/ai-agent-integration)). Free: „5 min inactivity; cannot disable“ ([Neon plans](https://neon.com/docs/introduction/plans#scale-to-zero)) |
| `list_operations` | 17 Paare `start_compute`/`suspend_compute` seit Anlage; seit 2026-10-26 12:00 UTC liegt jeder Zyklus zwischen 302 und 317 s |

Die frühere Aussage „suspend is not configured“ war eine Fehldeutung des Werts
`0`. Die Zykluslänge von etwa 312 s besteht aus einigen Sekunden Backup und
den 300 s Leerlauf bis zum Suspend. Damit ist das Intervall auch im Betrieb
belegt.

## Verbrauch im laufenden Abrechnungszeitraum

Zeitraum laut `describe_project`: 2026-10-25 10:19:53 UTC bis 2026-11-01
00:00 UTC. Das Kontingent setzt mit jedem Kalendermonat neu ein.

| Metrik | Wert | Anteil am Free-Kontingent |
| --- | --- | --- |
| `active_time_seconds` | 5 788 s (1,61 h) | – |
| `compute_time_seconds` | 1 473 CU-Sekunden (0,41 CU-h) | 0,4 % von 100 CU-h |
| `data_transfer_bytes` | 8 657 113 B (8,7 MB) | 0,2 % von 5 GB |

`compute_time_seconds` zählt bei 0.25 CU eine Viertelsekunde je aktiver Sekunde
([Consumption limits](https://neon.com/docs/guides/consumption-limits)). Die
Summe der Zyklen aus `list_operations` (5 854 s) passt zu `active_time_seconds`.
Neon bezeichnet diese Projektwerte als Näherung, nicht als Abrechnungsgrundlage.

## Was den Compute aufweckt

| Quelle | Datenbankzugriff | Beleg |
| --- | --- | --- |
| backup | `pg_dump` zweimal täglich, Cron `0 */12 * * *` UTC | `ops/backup.py`; Railway-Konfiguration; 11 Zyklen seit 2026-10-26 12:00 UTC, jeweils 00:0x und 12:0x UTC |
| api | Eine Verbindung pro Anfrage, kein Pool: `/ready` und Berichtsabfragen | `reports/store.py`, `reports/api.py`; `/health` und `/ui/` greifen nicht auf die Datenbank zu |
| api, Deployment | Pre-Deploy-Migration und Railway-Healthcheck `/ready`, nur beim Deployment | Railway-Konfiguration `healthcheckPath=/ready`, [production.md](production.md) |
| worker | `ready()` einmal beim Start, danach nur in Report-Aktivitäten | `reports/worker.py` |

Über den Railway-Proxy erreichten die API in den letzten sieben Tagen 855
Anfragen, davon 849 mit 4xx. Unbekannte Pfade und Anfragen ohne gültiges Token
beantwortet die API ohne Datenbankzugriff. `/ready` wurde über den Proxy nicht
aufgerufen. Außerhalb der Backup-Zeiten gab es seit 2026-10-26 12:00 UTC keinen
`start_compute`; diese Anfragen haben den Compute also nicht geweckt. Der
Zyklus am 2026-10-26 um 08:32 UTC gehört zum damaligen Deployment von API und
Worker, die Zyklen am 2026-10-25 zum Aufbau.

## Hochrechnung

Annahme: Monat mit 31 Tagen und 0.25 CU fest.

| Posten | Rechnung | CU-h |
| --- | --- | --- |
| Backup | 2 × 31 × 312 s = 19 344 s = 5,37 h × 0.25 | 1,34 |
| Zusätzliches isoliertes Aufwecken (Report, Deployment) | mindestens 300 s Leerlauf = 0,083 h × 0.25 | 0,021 je Aufwecken |
| Reserve | 100 − 1,34 | 98,7 |

Die Reserve reicht für etwa 4 700 zusätzliche isolierte Aufwecker im Monat,
rund 150 pro Tag. Gleichwertig sind etwa 394 Stunden zusätzlicher aktiver Zeit.

Grenzfall: Ein dauerhaft aktiver Endpoint braucht 744 h × 0.25 = 186 CU-h. Das
liegt über dem Kontingent; nach etwa 400 aktiven Stunden würde Neon den Compute
bis zum nächsten Abrechnungszeitraum suspendieren
([Neon plans](https://neon.com/docs/introduction/plans#what-happens-if-i-exceed-my-free-plan-limits)).
So weit kommt es nur, wenn die Datenbank fortlaufend öfter als alle fünf Minuten
abgefragt wird, etwa durch eine externe Überwachung auf `/ready`. Externe
Überwachung deshalb auf `/health` richten.

Zur Einordnung, nicht beauftragt: Auf Launch kostet eine CU-Stunde 0,106 USD.
Ein dauerhaft aktiver 0.25-CU-Endpoint käme damit auf etwa 19,72 USD im Monat,
zuzüglich Speicher ([Neon plans](https://neon.com/docs/introduction/plans)).
