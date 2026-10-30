# Staging-Abnahme

## Abnahme auf wh-coolify am 2026-10-30

Ziel: Coolify auf wh-coolify, Projekt `report-example`, Umgebung `staging`
([ADR 0008](../docs/adr/0008-staging-on-wh-coolify.md)). Fünf eigenständige
Docker-Image-Anwendungen im eigenen Netz `report-example-staging`; kein
Compose-Deployment. Frischer Start mit synthetischen Daten, keine Datenübernahme.

API und Worker: Image-Tag `sha-e477bf2b73eea51fbc0fe086d01b636a89e98837`.
PostgreSQL `16.6`, Temporal `1.29.7`, Temporal UI `2.51.0`.

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

Image-Digests wurden nicht vom Host zurückgelesen, weil Agenten auf wh-coolify
keinen SSH-Zugang haben. Für eine Übernahme nach Produktion gelten die Digests
des Image-Workflows. Diese Abnahme bestätigt keine Hochverfügbarkeit;
PostgreSQL, API und UI werden bei einem Austausch kurz unterbrochen.
