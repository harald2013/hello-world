# ADR 0006: Verteilung der Produktion auf gemanagte Cloud-Dienste

- Status: Akzeptiert
- Datum: 2026-10-25
- Geltungsbereich: Produktionsbetrieb des Beispielprojekts

## Kontext

ADR 0003 legt gemanagten Produktionsbetrieb fest. Für das konkrete Beispiel
brauchen wir eine eindeutige Zuordnung der Komponenten und eine Reihenfolge
für die Einrichtung. Der Benutzer hat diese Verteilung bestätigt. Es bestehen
noch keine Produktionsressourcen; diese Entscheidung beschreibt das Zielbild.

## Entscheidung

Render betreibt die API als Web Service und unseren Python-Worker als Background
Worker aus den in Staging geprüften Images. Temporal Cloud betreibt die
Workflow-Infrastruktur samt Verwaltungsoberfläche. Neon betreibt PostgreSQL
für Anwendungsdaten. Temporal verwaltet seine Historie unabhängig von dieser
Datenbank. GHCR bleibt die Registry der unveränderlichen Anwendungsimages.

Frankfurt ist für alle drei Laufzeitanbieter die Zielregion; für Temporal Cloud
und Neon wird die AWS-Region gewählt. Die tatsächliche Verfügbarkeit wird vor
dem Anlegen geprüft. Verbindungen zwischen Anbietern werden über TLS geschützt;
eine gemeinsame private Netzwerkgrenze wird nicht vorausgesetzt.

Zuerst werden Neon und Temporal Cloud vorbereitet, anschließend die API mit ihrer
temporären Pre-Deploy-Migration und danach der Worker. Die Release-Reihenfolge
und Migrationsbedingungen aus ADR 0004 gelten weiterhin. Produktionsreleases
werden ausdrücklich über CI/API oder das Dashboard ausgelöst. Ein Registry-Push
allein gilt nicht als Deployment.

Budget, konkrete Tarife, Domain, tolerierbarer Datenverlust und
Wiederherstellungszeit bleiben offen. Diese Betriebsparameter werden vor der
kostenpflichtigen Einrichtung festgelegt. Das Zielbild ist keine Aussage über
eine bereits abgenommene Produktion. Lokal und Staging bleiben gemäß ADR 0003
unverändert.

## Betrachtete Alternativen

Railway bleibt als Alternative zu Render dokumentiert. Beide parallel zu nutzen
würde dem kleinen Beispiel eine zusätzliche Betriebsplattform hinzufügen.
Temporal und PostgreSQL in Produktion selbst zu betreiben widerspricht dem
gewünschten Betriebsmodell. Unterschiedliche Zielregionen würden zusätzliche
Netzwerklatenz verursachen und werden ohne konkreten Bedarf nicht gewählt.

## Konsequenzen

Das Beispiel zeigt die Grenze zwischen eigenem Anwendungscode und gemanagter
Infrastruktur. Der eigene Worker benötigt weiterhin Laufzeitressourcen und
Anwendungspflege auf Render. Anbieterübergreifende Verbindungen, getrennte
Zugangsdaten, Abrechnung und Überwachung müssen berücksichtigt werden.
Gemanagter Betrieb ersetzt weder Wiederherstellungstests noch die Abnahme eines
fehlgeschlagenen Releases. Frankfurt als gemeinsame Region garantiert keine
vollständige Datenresidenz für sämtliche Anbieterfunktionen.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
