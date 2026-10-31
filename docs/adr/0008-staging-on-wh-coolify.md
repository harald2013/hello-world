# ADR 0008: Staging auf der Coolify-Instanz wh-coolify

- Status: Akzeptiert; am 2026-10-31 auf ADR-reference-architecture-staging zurückgeführt (TIL-221)
- Datum: 2026-10-30
- Geltungsbereich: Staging-Umgebung des Beispielprojekts

## Kontext

ADR 0003 legte Staging auf die Coolify-Instanz workhorse. Die internen Dienste
ziehen auf die neue Coolify-Instanz wh-coolify um; workhorse soll keine
Staging-Anwendungen mehr betreiben. Aufbau und Veröffentlichung von Staging
regelt die Referenzarchitektur ADR-reference-architecture-staging des
Development MCP. Die auf wh-coolify installierte Coolify-Version kann über ihre
API keinen Host-Port nur an `127.0.0.1` binden. Für diesen Fall sieht die
Referenz die Variante mit fester Container-Adresse vor; sie braucht kein
Abweichungs-ADR. Auf wh-coolify gibt es außerdem keinen SSH-Zugang für
Agenten. Die bisherigen Tailnet-Ports 18443 und 18444 lagen im Bereich, den
die Portregeln für lokale Entwicklung reservieren.

Dieses ADR hält nur die Entscheidungen fest, die das Projekt über die Referenz
hinaus trifft.

## Entscheidung

Staging folgt ADR-reference-architecture-staging in der Variante mit fester
Container-Adresse. Es läuft als Coolify-Projekt `report-example` mit Umgebung
`staging` auf wh-coolify, im eigenen Docker-Netz `report-example-staging`.

Daten werden nicht übernommen; Staging beginnt mit einem frischen Volume und
synthetischen Daten.

API und Temporal UI verwenden Tailnet-Ports aus dem Block 15100 bis 15119.
Der Block ist im Portregister von wh-coolify im idp-Repository für dieses
Projekt reserviert.

Der einmalige Schemajob und Prüfungen mit dem API-Schlüssel laufen als
einmalige Coolify-Aufgabe im API-Container. Agenten lesen den Schlüssel nicht
aus Coolify aus; er verlässt den Container nicht.

Produktion ist nicht von wh-coolify abhängig.

## Betrachtete Alternativen

Staging auf workhorse zu belassen hätte den Umzug der internen Dienste
blockiert. Das gemeinsame Netz des IDP auf wh-coolify zu nutzen hätte die
Trennung der Projekte aufgehoben. Eine Übernahme der Staging-Daten hätte einen
Host-Eingriff erfordert, ohne dass synthetische Daten ihn rechtfertigen. Den
API-Schlüssel für Prüfungen aus Coolify auszulesen wäre einfacher, brächte ihn
aber in Agentenausgaben und Protokolle.

Eine eigene Begründung der festen Container-Adressen in diesem ADR entfällt,
seit die Referenz die Variante abdeckt. Ein neues ADR, das dieses ersetzt,
hätte dieselben Projektentscheidungen nur unter neuer Nummer wiederholt.

## Konsequenzen

Feste Adressen, Serve-Routen und das Subnetz stehen im Coolify-Inventar der
Umgebung; die Prüfung nach jedem Deployment regelt die Referenz. Eine
Änderung des Portblocks erfordert zuerst eine Änderung des Registers im
idp-Repository. Die Variante mit fester Container-Adresse entfällt, sobald die
installierte Coolify-Version Loopback-Bindungen über ihre API unterstützt.
Produktion bleibt von einem Ausfall oder Umzug von wh-coolify unberührt.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
