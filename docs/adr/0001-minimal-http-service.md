# ADR 0001: Minimaler HTTP-Dienst mit Python-Standardbibliothek

- Status: Akzeptiert
- Datum: 2026-10-25
- Geltungsbereich: HTTP-Dienst und Container im gesamten Repository

## Kontext

Das Projekt stellt einen kleinen HTTP-Dienst bereit, der eine Textbegrüßung
und einen Health-Endpunkt liefert. Seine Systemgrenze umfasst den Python-Prozess
und dessen HTTP-Schnittstelle; Datenhaltung und externe Dienste gehören nicht
zum bestehenden Funktionsumfang. Die Dokumentation hält die vorhandene
Architektur fest.

## Entscheidung

Der Dienst verwendet zur Laufzeit ausschließlich die Python-Standardbibliothek.
Er lauscht standardmäßig auf allen IPv4-Schnittstellen an Port 8000. GET-Anfragen
liefern Status 200 und Klartext mit UTF-8-Zeichensatz. Der URL-Pfad `/health`
liefert `ok`; alle anderen GET-Pfade liefern die konfigurierte Begrüßung.
Query-Parameter ändern diese Pfadzuordnung nicht.

Lokaler Betrieb und Container führen denselben Python-Dienst aus. Der Container
stellt damit dieselbe HTTP-Schnittstelle bereit. Diese kleine Architektur passt
zum begrenzten Funktionsumfang und benötigt keine zusätzlichen Laufzeitpakete.

## Betrachtete Alternativen

Ein Webframework könnte Routing und spätere Erweiterungen erleichtern, würde
für die vorhandenen zwei Antwortvarianten aber zusätzliche Abhängigkeiten
einführen. Eine getrennte Implementierung für den Container würde Wartung und
Abgleich des Verhaltens erschweren. Beide Alternativen werden für den aktuellen
Umfang verworfen.

## Konsequenzen

Der Dienst bleibt leicht nachvollziehbar und mit wenigen Bestandteilen
ausführbar. Die Standardbibliothek stellt nur begrenzte Funktionen für komplexe
Webanwendungen bereit; das ist für den aktuellen Umfang akzeptiert. Neue
Anforderungen an Routing, Parallelität oder Produktionsbetrieb erfordern eine
erneute Architekturprüfung. Die Bindung an alle Schnittstellen erlaubt den
Zugriff über Container-Portfreigaben; die Erreichbarkeit bestimmt die jeweilige
Betriebsumgebung.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
