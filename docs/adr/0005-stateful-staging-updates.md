# ADR 0005: Exklusiver Volume-Zugriff bei Staging-Updates

- Status: Akzeptiert
- Datum: 2026-10-25
- Geltungsbereich: PostgreSQL als einzelne Coolify-Anwendung in Staging

## Kontext

Die Staging-Vorlage betreibt PostgreSQL als eigenständige Image-Anwendung mit
persistentem Volume. Coolify kann bei einem Rolling-Update alte und neue
Container überlappend ausführen. Zwei PostgreSQL-Prozesse dürfen jedoch niemals
dasselbe Datenverzeichnis öffnen. Ein einzelner gesunder Container beweist
nicht, dass während eines Updates exklusiver Zugriff bestand.

## Entscheidung

PostgreSQL wird vor einem Austausch vollständig gestoppt. Konsistente
Containernamen in Coolify verhindern überlappende Instanzen; vor Änderungen
werden die aktuelle Konfiguration und nachher der laufende Container geprüft.
Das Volume bleibt erhalten. Der Ablauf akzeptiert eine kurze Staging-Unterbrechung
und wird mit einem tatsächlich ausgeführten Austausch und anschließendem
Datenzugriff geprüft. Eine reine Versionsänderung darf keine zweite schreibende
Instanz starten.

## Betrachtete Alternativen

Ein Rolling-Update mit gemeinsamem Volume gefährdet die Datenintegrität.
Replikation und ein koordinierter Datenbank-Failover würden ein anderes
Betriebskonzept mit zusätzlichem Aufwand erfordern. Ein Coolify-Datenbanktyp
wäre ebenfalls möglich, würde aber die hier gewählte Vorlage eigenständiger
Image-Anwendungen verändern. Für Produktion bleibt Neon zuständig.

## Konsequenzen

Das Beispiel zeigt bewusst keine hochverfügbare Datenbank. Updates verursachen
eine kurze Unterbrechung. Ein beschädigtes Volume darf nicht durch einen
unbemerkten Reset ersetzt werden: vorhandene Daten müssen erhalten und die
Wiederherstellung ausdrücklich dokumentiert werden. Nur beim erstmaligen Setup
mit verwerfbaren synthetischen Daten kann ein frisches Volume eingerichtet
werden; das bisherige Volume bleibt dabei zur Untersuchung erhalten.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
