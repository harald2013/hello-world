# ADR 0007: Kleine Browseroberfläche im API-Image

- Status: Akzeptiert
- Datum: 2026-10-25
- Geltungsbereich: Browserzugriff auf das Beispielprojekt

## Kontext

Der Benutzer möchte neben der API eine sehr einfache sichtbare Oberfläche als
weiteren Bestandteil der Projektvorlage. Eine Begrüßung und die Bedienung des
vorhandenen Berichtsgenerators genügen. Der zusätzliche Betrieb einer separaten
Frontendplattform ist für diesen Umfang nicht erforderlich.

## Entscheidung

Das API-Image liefert statisches HTML, CSS und JavaScript aus. Die Oberfläche
zeigt eine Begrüßung und verwendet für die Berichtserstellung ausschließlich
die bestehenden APIs derselben Origin. Der öffentliche Seitenrahmen enthält
keine Anwendungsdaten oder Zugangsdaten. Die bestehenden API-Routen behalten
ihre Authentifizierung und Antworten.

Ein benötigter API-Schlüssel wird vom Benutzer im Browser eingegeben. Er darf
weder in ausgelieferten Dateien oder URLs noch in dauerhaftem Browserspeicher
stehen. Ergebnisse werden als Text dargestellt. Die Oberfläche verwendet keine
externen Skripte oder Bibliotheken. Beim bloßen Seitenaufruf werden keine
Backend-Abhängigkeiten abgefragt. Statusabfragen beginnen erst nach einer
Benutzeraktion und enden nach Abschluss oder einer begrenzten Anzahl Versuche.

## Betrachtete Alternativen

Eine reine Hello-World-Seite erfüllt die Sichtbarkeit, zeigt aber den vorhandenen
Workflow nicht. Ein eigenes Frontend mit Buildwerkzeugen und separatem Deployment
würde den gewünschten Umfang überschreiten. Eine dauerhafte Ablage des gemeinsamen
API-Schlüssels im Browser würde das Demo-Zugangsmodell unnötig erweitern.

## Konsequenzen

Die UI wird mit demselben API-Image zwischen Umgebungen übernommen. Neue Hosting-
Dienste oder Laufzeitabhängigkeiten sind nicht nötig. Der gemeinsame API-Schlüssel
bleibt eine Demo-Lösung und ersetzt keine Benutzerverwaltung. Öffentliche Nutzung
in Produktion setzt ein gültiges HTTPS-Zertifikat voraus. Ein Reload leert den
UI-Zustand; der eigentliche Workflow läuft unabhängig davon weiter.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
