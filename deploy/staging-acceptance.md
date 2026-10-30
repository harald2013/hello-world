# Staging-Abnahme

Der Abschnitt [Umzug auf wh-coolify](#umzug-auf-wh-coolify-am-2026-10-30)
belegt den aktuellen Aufbau. Die Abnahme vom 2026-10-25 betrifft die
frühere Umgebung auf workhorse.

## Abnahme auf workhorse am 2026-10-25

Ziel: Coolify auf workhorse, Projekt `report-example`, Umgebung `staging`.
Fünf eigenständige Docker-Image-Anwendungen; kein Compose-Deployment.
Strukturelle Zuordnung und private URLs: [.agents/infra/staging/coolify.md](../.agents/infra/staging/coolify.md).

### Geprüfte Revision

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

### Ergebnisse auf dem Zielhost

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

### Grenzen und Aufbauvorfall

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

## Umzug auf wh-coolify am 2026-10-30

Ziel: Coolify auf wh-coolify, Projekt `report-example`, Umgebung `staging`
([ADR 0008](../docs/adr/0008-staging-on-wh-coolify.md)). Fünf eigenständige
Docker-Image-Anwendungen im eigenen Netz `report-example-staging`; kein
Compose-Deployment. Frischer Start mit synthetischen Daten, keine Datenübernahme.

API und Worker: Image-Tag `sha-e477bf2b73eea51fbc0fe086d01b636a89e98837`, dieselbe
Revision wie zuvor auf workhorse. PostgreSQL `16.6`, Temporal `1.29.7`,
Temporal UI `2.51.0`.

- Alle fünf Anwendungen deployt; PostgreSQL, Temporal UI und API melden
  `healthy`. Temporal legt den Namespace `default` an. Keine Anwendung hat eine
  Domain oder einen Host-Port.
- Schemajob `python -m reports.store` als einmalige Coolify-Aufgabe im
  API-Container: `Migration started`, `Migration completed`. Der vorher
  gestartete Worker brach mit fehlender Tabelle ab und lief nach einem Neustart.
- Über das Tailnet liefern `/ready`, `/health`, `/ui/` und die Temporal UI
  HTTP 200; `POST /reports` ohne oder mit falschem Schlüssel liefert 401.
- Authentifizierter Bericht `4900bcfd-f18d-44c7-bbbd-39e733080ac1` mit
  `[1, 2, 3]` wird fertig: Anzahl 3, Summe 6, Mittelwert 2. Der Schlüssel
  wurde nur im API-Container verwendet.
- Wiederanlauftest: Bericht `cd9fb8e8-d411-4cf4-9a23-562c94b67b85` mit
  `[4, 5, 6]` und 60 Sekunden Timer um 11:17:03 UTC angelegt; Worker-Neustart
  `hrdgvsvtgje1gmtppezkwqp8` von 11:17:08 bis 11:17:20 UTC. Derselbe Bericht
  wird um 11:18:03 UTC fertig: Summe 15, Mittelwert 5.
- PostgreSQL-Austausch `jwrepestgnf8jztfxad2nvvk` mit konsistentem
  Containernamen: Coolify entfernt zuerst den alten Container, PostgreSQL
  meldet danach ein sauber heruntergefahrenes Datenverzeichnis. Bericht
  `4900bcfd-…` bleibt lesbar; neuer Bericht `9fd0791b-2775-4ac6-8976-0d789129a86a`
  mit `[10, 20, 30]` wird fertig: Summe 60, Mittelwert 20.
- Die fünf Anwendungen auf workhorse sind gestoppt; ihre Volumes bleiben
  erhalten.

Image-Digests wurden nicht vom Host zurückgelesen, weil Agenten auf wh-coolify
keinen SSH-Zugang haben. Für eine Übernahme nach Produktion gelten die Digests
des Image-Workflows. Diese Abnahme bestätigt keine Hochverfügbarkeit;
PostgreSQL, API und UI werden bei einem Austausch kurz unterbrochen.
