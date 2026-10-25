# Staging-Abnahme am 2026-10-25

Ziel: Coolify auf workhorse, Projekt `report-example`, Umgebung `staging`.
Fünf eigenständige Docker-Image-Anwendungen; kein Compose-Deployment.
Strukturelle Zuordnung und private URLs: [COOLIFY.md](../COOLIFY.md).

## Geprüfte Revision

API und Worker: `13abb021929b2efafb8d0807e6dd96169453dad9`.
[Image-Build und Containerprüfungen](https://github.com/harald2013/hello-world/actions/runs/40180228337)
und [CI](https://github.com/harald2013/hello-world/actions/runs/40180232374)
sind erfolgreich. Spätere reine Dokumentations-Commits ändern diese ausgerollte
Revision nicht. Die folgenden Digests wurden am Host aus den laufenden Images
zurückgelesen und können für eine spätere Übernahme verwendet werden.

| Rolle | Image-Digest |
| --- | --- |
| postgres | `postgres@sha256:557fea37a744d5f4c8faab304b0a90858b53ab119735a88c131fd19dab802f36` |
| temporal | `temporalio/auto-setup@sha256:f14912b699cf73015ad5c4fc18d522d4b014db90e794039214dfb7c022c2644f` |
| temporal-ui | `temporalio/ui@sha256:5c72329a014fb247ef66d051dd45b3a5c251d06f82709a852e364f0fd8b69a04` |
| api | `ghcr.io/harald2013/hello-world-api@sha256:771e6965c0f1a45c428cac86be8c4bdf62636876b850a20a879b4e74d605c721` |
| worker | `ghcr.io/harald2013/hello-world-worker@sha256:70e3979beea9e0506b2cc488542fa723b510804188d6cf71cc20207aab7bf325` |

## Ergebnisse auf dem Zielhost

- `TestOnly` und `Infrastructure` einschließlich ihrer drei Anwendungen entfernt;
  nachfolgende Projektabfrage enthält sie nicht mehr. Bestehende Datenvolumes
  wurden nicht pauschal gelöscht.
- `report-example` enthält ausschließlich die Umgebung `staging` und ihre fünf
  Image-Anwendungen. IDP-Anwendungen wurden nicht geändert.
- Migration aus dem neuen API-Image als temporärer Container vor dem API-Rollout:
  `Migration started`, `Migration completed`, Exitcode 0. Kein dauerhafter
  Migrationsdienst und kein Migrationsbefehl im normalen App-Start.
- API und Worker verwenden dieselbe geprüfte Revision. API, PostgreSQL und UI
  melden im laufenden Docker-Healthcheck `healthy`. Temporal und Worker haben
  absichtlich keinen HTTP-Healthcheck; Namespace und echte Verarbeitung geprüft.
- Readiness-Kommando `python -m reports.healthcheck` im laufenden API-Container
  mit Exitcode 0 geprüft; mit geschlossenem Zielport Exitcode 1.
- API und UI sind über Tailscale HTTPS erreichbar; Docker bindet ihre Host-Ports
  ausschließlich an `127.0.0.1`. PostgreSQL, Temporal und Worker haben keine
  Host-Portbindungen. Alle fünf Anwendungen befinden sich im Staging-Netz.
- Unauthentifizierter `POST /reports` liefert 401. Authentifizierte API meldet
  `environment=staging`. Ein Bericht mit `[10, 20, 30]` wird fertig und liefert
  Anzahl 3, Summe 60, Minimum 10, Maximum 30 und Mittelwert 20.
- Temporal UI liefert HTTP 200 und kann über ihren eigenen HTTPS-API-Endpunkt
  den Staging-Namespace `default` lesen.
- Wiederanlauftest auf der endgültigen Revision: Bericht `a6a53969-e596-4726-b0ba-19c6f6d5cb49`
  mit `[2, 4, 6]` und 45 Sekunden Timer begonnen; Datenbankeintrag abgewartet;
  Worker über Coolify ersetzt. Derselbe Bericht wird fertig und liefert
  Summe 12 und Mittelwert 4. Worker-Deployment: `lyytr33mkrhqfm9kvo4celeu`.
- PostgreSQL mit konsistentem Containernamen erneut deployt: Coolify protokolliert
  zuerst das Entfernen des alten Containers und danach den Start des neuen.
  Genau eine laufende PostgreSQL-Instanz bestätigt; gespeicherter Bericht
  `8995e20b-d950-4be2-bd23-f349d07f4eb7` bleibt danach lesbar, neue Berichte
  werden erfolgreich verarbeitet. Deployment: `xmykwl9zq35jogdjny5xl1bn`.
- Repository-Verifikation: Ruff und 24 Tests erfolgreich; Coolify-Mapping und
  vollständige Architektur-Dokumentation über Development MCP validiert.

API-Deployment: `vdmngqt2nqmblpxtskbblldy`. Worker-Deployment vor dem
Wiederanlauftest: `oycbziagyjyff8mui8ghjjv3`. UI-Deployment:
`wxbvi1ug1tbktplg5hxmx2rv`. Alle wurden in Coolify mit `finished` bestätigt.

## Grenzen und Aufbauvorfall

Das erste PostgreSQL-Volume wurde beim Einrichten durch überlappende
Rolling-Update-Prozesse beschädigt. Es enthielt noch keine Benutzerberichte.
Der Aufbau wurde gestoppt, auf exklusiven Zugriff umgestellt und mit einem
frischen Volume fortgesetzt; das beschädigte Volume blieb erhalten. Details
und Betriebsregel stehen in [staging.md](staging.md) und
[ADR 0005](../docs/adr/0005-stateful-staging-updates.md).

Diese Abnahme betrifft Staging mit synthetischen Daten. Sie bestätigt keine
Hochverfügbarkeit: PostgreSQL sowie die an Loopback-Ports gebundenen API-/UI-
Anwendungen werden bei einem Austausch kurz unterbrochen. Native Render-
Pre-Deploy-Phasen und die Isolation eines fehlgeschlagenen Render-Releases sind
weiterhin am noch anzulegenden Render-Testservice zu prüfen. Produktion und
allgemeine Development-MCP-Regeln wurden nicht ausgerollt.
