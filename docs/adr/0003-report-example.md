# ADR 0003: Berichtsgenerator als Vorlage für drei Betriebsumgebungen

- Status: Akzeptiert
- Datum: 2026-10-25
- Geltungsbereich: Gesamtes Beispielprojekt und seine Betriebsumgebungen

## Kontext

Der bisherige Begrüßungsdienst zeigt weder persistente Daten noch langlebige
Hintergrundverarbeitung. Benötigt wird eine kleine Vorlage, die sich lokal,
auf dem Staging-Host workhorse und bei gemanagten Produktionsanbietern betreiben
lässt. Die produktive Anwendung darf nicht vom lokalen Rechner abhängen.
Diese Entscheidung ersetzt ADR 0001; ADR 0002 bleibt gültig.

## Entscheidung

Eine Python-API nimmt Zahlenreihen entgegen. Ein Temporal-Workflow wartet auf
einem dauerhaften Timer und berechnet danach einen Bericht. Aktivitäten speichern
Eingabe und Ergebnis in PostgreSQL. Der Bericht enthält Anzahl, Summe, Minimum,
Maximum und Mittelwert. PostgreSQL speichert Anwendungsdaten; Temporal verwaltet
seine Ausführungshistorie eigenständig. Der API-Aufruf bestätigt erst nach dem
dauerhaften Workflow-Start. Dadurch ist kein ungesicherter Doppel-Schreibvorgang
zwischen Datenbank und Prozesssteuerung nötig. Aktivitäten können wiederholt
werden und schreiben anhand einer stabilen Berichtsidentität idempotent.

API und Worker werden aus derselben Codebasis als getrennte Images gebaut.
Unveränderliche Image-Versionen werden zwischen Umgebungen übernommen.
Adressen, Zugangsdaten und Umgebungseinstellungen werden zur Laufzeit gesetzt.
API-Authentifizierung ist außerhalb der lokalen Umgebung verpflichtend.

Lokal startet Compose die Anwendung, PostgreSQL, Temporal und dessen Oberfläche.
In Staging laufen die gleichen Images einzeln in Coolify auf workhorse.
PostgreSQL und Temporal bleiben dort intern erreichbar. Test und Staging
verwenden synthetische, verwerfbare Daten. Ihre selbst betriebenen Dienste sind
keine Produktionsvorlage für Datenhaltung oder Verfügbarkeit.

In Produktion laufen API und Worker bei einem gemanagten Anwendungsanbieter
wie Render oder Railway. Temporal Cloud übernimmt den Temporal-Server und Neon
die PostgreSQL-Datenbank. Der eigene Worker bleibt Anwendungscode und läuft beim
Anwendungsanbieter. Produktionsverbindungen verwenden TLS; Datenbankzertifikate
werden geprüft. Konkrete Anbieterressourcen und Tarife sind erst beim tatsächlichen
Setup festzulegen. Das Beispiel allein behauptet kein abgeschlossenes Deployment.

## Betrachtete Alternativen

Eine reine CRUD-Anwendung würde Hintergrundprozesse und Wiederaufnahme nicht
zeigen. Ein umfangreicher fachlicher Prozess würde die Betriebsfragen verdecken.
Eine eigene Jobwarteschlange würde Zustandsverwaltung und Wiederholungen selbst
implementieren. Vollständiger Eigenbetrieb in Produktion widerspricht dem
gewünschten geringen Betriebsaufwand. Deshalb werden ein kleiner Bericht und
gemanagte Produktionsdienste gewählt.

## Konsequenzen

Das Beispiel zeigt persistente Ergebnisse, Wiederaufnahme nach Worker-Neustart,
Healthchecks und die Übernahme derselben Anwendung zwischen Umgebungen.
Zusätzliche Abhängigkeiten und getrennte Diensterollen erhöhen den lokalen
Aufwand gegenüber Hello World. Die PostgreSQL-Verbindungen sind für einen
kleinen Demonstrator ausgelegt; große Last erfordert Pooling und Lasttests.
Ein gemeinsamer API-Schlüssel begrenzt den Demo-Zugriff, ersetzt aber keine
Benutzerverwaltung oder Mandantentrennung. Temporal-Historien enthalten
synthetische Eingaben; echte sensible Daten erfordern eine eigene Schutzentscheidung.
Anbieterbetrieb ersetzt nicht die Pflege von Anwendungscode, Zugangsdaten und
Wiederherstellungsverfahren. Allgemeine MCP-Regeln werden erst nach praktischer
Erprobung der Vorlage abgeleitet.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
