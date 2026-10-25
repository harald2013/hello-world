# ADR 0004: Datenbankschema vor dem Rollout mit Render migrieren

- Status: Teilweise ersetzt durch ADR 0006 (Anbieterwahl)
- Datum: 2026-10-25
- Geltungsbereich: Deployment und Datenbankschema des Beispielprojekts

## Kontext

Das fertige Anwendungsimage wird ohne Plattform-Build aus einer Registry geladen.
Schemaänderungen müssen vor dem Start einer neuen Version erfolgreich sein,
während die bisherige Version weiter verfügbar bleibt. Für das konkrete Beispiel
wurde Render ausgewählt. Es existiert noch kein Render-Service; diese Entscheidung
legt den Ablauf fest, behauptet aber keine erfolgreiche Plattform-Abnahme.

## Entscheidung

Migrationen laufen bei jedem API-Deployment in Renders nativer Pre-Deploy-Phase
als temporärer Prozess aus dem neuen API-Image mit dessen Runtime-Konfiguration.
Nur ein erfolgreicher Abschluss erlaubt den weiteren Rollout. Der Worker wird
anschließend mit dem passenden Image aktualisiert; eine automatische Reihenfolge
zwischen getrennten Render-Diensten wird nicht vorausgesetzt.

Der Migrationsprozess liefert einen eindeutigen Exit-Code und protokolliert Erfolg
oder Fehlertyp ohne Zugangsdaten. Transaktionale Schemaänderungen werden bei einem
SQL-Fehler zurückgerollt. Ein Datenbank-Lock serialisiert konkurrierende Aufrufe;
begrenzte Wartezeiten führen im Fehlerfall zum Abbruch statt zu einem offenen Job.
Lokal bleibt Compose für einen einmaligen Migrationsprozess verantwortlich.

Während einer Migration arbeiten alte API und Worker noch auf der Datenbank.
Schemaänderungen müssen daher mit diesen Verbrauchern kompatibel sein.
Spätere strukturelle Änderungen benötigen versionierte Migrationen; die aktuelle
wiederholbare Initialisierung allein aktualisiert keine vorhandenen Tabellen.

## Betrachtete Alternativen

Migrationen beim normalen Anwendungsstart würden an jede skalierte Instanz
gekoppelt und erschweren einen kontrollierten Rollout. Ein dauerhaft laufender
Migrationsdienst verursacht unnötigen Betrieb und Kosten. Ein manueller externer
Job erzwingt die Reihenfolge nicht als Bestandteil jedes Deployments. Railway
bietet eine alternative Release-Phase, wird für dieses Beispiel aber nicht gewählt.

## Konsequenzen

Das API-Image enthält auch alle Migrationsabhängigkeiten. Ein bezahlter Render-Dienst
und dessen Pre-Deploy-Ressourcen sind erforderlich. Container-Tests prüfen Erfolg,
Wiederholung und Fehler-Rollback; ein separater Plattformtest muss nachweisen, dass
ein fehlgeschlagener Job die bisherige Anwendung verfügbar lässt. Eine erfolgreiche
Migration wird bei späterem App-Fehler nicht automatisch rückgängig gemacht.
Destruktive Schemaänderungen benötigen eine eigene gestufte Freigabe.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
