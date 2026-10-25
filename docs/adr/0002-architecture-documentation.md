# ADR 0002: Architekturentscheidungen und Agentenregeln gemeinsam pflegen

- Status: Akzeptiert
- Datum: 2026-10-25
- Geltungsbereich: Architekturdokumentation im gesamten Repository

## Kontext

Die Regeln des MCP-Servers `development-mcp` sollen in diesem Projekt gelten.
Bisher enthält das Repository eine Anleitung für Agenten, aber keine getrennte
Dokumentation der Architekturentscheidungen und ihrer verbindlichen Leitplanken.
Menschen benötigen Gründe und Abwägungen, Agenten kurze aktuelle Regeln.
Die Entscheidung betrifft die Dokumentation und führt keine zusätzlichen
Laufzeitdienste oder Werkzeuge in die Anwendung ein.

## Entscheidung

Architekturentscheidungen werden auf Deutsch in `docs/adr/` des jeweils
betroffenen Bereichs abgelegt. Dateinamen verwenden eine fortlaufende, noch
unbenutzte vierstellige Nummer und ein Thema; bestehende Nummern bleiben stabil.
Jede Entscheidung enthält Status, Datum, Geltungsbereich, Kontext, Entscheidung,
betrachtete Alternativen und Konsequenzen. Begründungen, Systemgrenzen und
akzeptierte Nachteile werden festgehalten, kurzlebige Implementierungsdetails
ausgelassen.

Die zugehörigen technischen Leitplanken stehen auf Englisch in
`AGENT_RULES.md`. Kurze imperative Regeln verweisen auf die Entscheidung;
Abschnittsüberschriften verlinken das Ursprungsdokument. Jeder ADR endet mit
einem relativen Rückverweis. Die Agentenanleitung verlinkt die geltenden Regeln.
Repository-weite Regeln liegen im Wurzelverzeichnis, zusätzliche Modulregeln
im engsten betroffenen Bereich ohne geerbte Regeln zu duplizieren.

Neue Dokumente beruhen auf den Vorlagen des MCP-Servers `development-mcp`.
Entscheidung, aktuelle Regeln und betroffene Anleitung werden gemeinsam
geändert. Nach Änderungen wird das vollständige betroffene Dokumentenpaket
mit dessen Architekturvalidator geprüft und zusätzlich inhaltlich auf Sprache,
Begründung, Geltungsbereich, Vollständigkeit und Duplikate überprüft.

## Betrachtete Alternativen

Alle Informationen in der Agentenanleitung zu sammeln wäre zunächst kürzer,
würde aber Begründung und aktuelle Anweisung vermischen. Nur ADRs zu pflegen
würde Agenten bei jeder Aufgabe zum Lesen ausführlicher Begründungen zwingen.
Nur Regeln zu pflegen ließe die Abwägungen bei späteren Änderungen verloren
gehen. Die getrennten, gegenseitig verlinkten Dokumente erfüllen beide Zwecke.

## Konsequenzen

Entscheidungen werden nachvollziehbar und Agenten können die gültigen
Leitplanken gezielt laden. Jede Architekturänderung verursacht zusätzlichen
Dokumentationsaufwand. Gegenseitige Verweise und die gemeinsame Änderung
verringern das Risiko widersprüchlicher Dokumente. Die automatisierte Prüfung
erkennt Strukturprobleme, ersetzt aber keine inhaltliche Prüfung.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
