# ADR 0008: Staging auf der Coolify-Instanz wh-coolify

- Status: Akzeptiert
- Datum: 2026-10-30
- Geltungsbereich: Staging-Umgebung des Beispielprojekts

## Kontext

ADR 0003 legte Staging auf die Coolify-Instanz workhorse. Die internen Dienste
ziehen auf die neue Coolify-Instanz wh-coolify um; workhorse soll keine
Staging-Anwendungen mehr betreiben. Die Referenzarchitektur
ADR-reference-architecture-staging des Development MCP verlangt ein eigenes
Docker-Netz je Projekt und Host-Ports nur auf `127.0.0.1`, die Tailscale Serve
im Tailnet veröffentlicht. Die auf wh-coolify installierte Coolify-Version
lehnt Portbindungen mit IP-Präfix über ihre API ab und setzt `--publish` in
den Docker-Optionen nicht um. Auf wh-coolify gibt es außerdem keinen
SSH-Zugang für Agenten. Die bisherigen Tailnet-Ports 18443 und 18444 lagen
im Bereich, den die Portregeln für lokale Entwicklung reservieren.

## Entscheidung

Staging läuft als Coolify-Projekt `report-example` mit Umgebung `staging` auf
wh-coolify. Die fünf Rollen bleiben einzelne Docker-Image-Anwendungen in einem
eigenen Docker-Netz mit festem Subnetz. Daten werden nicht übernommen; Staging
beginnt mit einem frischen Volume und synthetischen Daten.

Abweichend von ADR-reference-architecture-staging bindet keine Anwendung einen
Host-Port. API und Temporal UI erhalten feste Adressen im Projektnetz. Tailscale
Serve auf wh-coolify terminiert HTTPS und leitet direkt an diese Adressen weiter.
Damit bleibt jeder Dienst ohne öffentlichen Port, ohne Bindung an alle
Host-Interfaces und nur im Tailnet erreichbar. Die Tailnet-Ports liegen im
Block 15100 bis 15119 innerhalb des Bereichs für Coolify-Anwendungen.

Werte, die mehrere Anwendungen brauchen, sind Shared Variables der Umgebung.
Der einmalige Schemajob und Prüfungen mit dem API-Schlüssel laufen als
einmalige Coolify-Aufgabe im API-Container; der Schlüssel verlässt den
Container dabei nicht.

## Betrachtete Alternativen

Staging auf workhorse zu belassen hätte den Umzug der internen Dienste
blockiert. Das gemeinsame Netz des IDP auf wh-coolify zu nutzen hätte die
Trennung der Projekte aufgehoben. Loopback-Bindings über Änderungen am
generierten Deployment oder direkt in der Coolify-Datenbank würden bei jedem
Deployment unbemerkt verloren gehen können. Eine Übernahme der Staging-Daten
hätte einen Host-Eingriff erfordert, ohne dass synthetische Daten ihn
rechtfertigen.

## Konsequenzen

Feste Adressen im Projektnetz müssen vor jeder neuen Anwendung als frei geprüft
werden; nach Deployments sind Serve-Ziel und Containeradresse gemeinsam zu
prüfen. Das feste Subnetz wird am Host angelegt, bevor Coolify es als Ziel
verwendet. Die Abweichung entfällt, sobald die installierte Coolify-Version
Loopback-Bindings über ihre API unterstützt. Produktion ist nicht von
wh-coolify abhängig.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
