# ADR 0006: Produktion auf Railway mit unabhängigen Backups

- Status: Akzeptiert
- Datum: 2026-10-25
- Geltungsbereich: Produktionsbetrieb des gesamten Beispielprojekts

## Kontext

Der Benutzer ersetzt Render vollständig durch seinen bestehenden Railway-Hobby-
Workspace. Das Beispiel verwendet höchstens 100 Berichte pro Tag, ein Budget von
50 Euro monatlich und ausschließlich die vorgesehenen kleinen Berichtsdaten.
Datenverlust und Wiederherstellungszeit sollen jeweils höchstens 24 Stunden
betragen. Diese Entscheidung ersetzt die Render-Anbieterwahl aus ADR 0004;
dessen Migrations- und Kompatibilitätsanforderungen bleiben gültig.

## Entscheidung

API und Worker laufen als getrennte, vorgebaute und in Staging geprüfte Images
auf Railway. Ein temporärer nativer Pre-Deploy-Prozess des API-Dienstes migriert
die Neon-Datenbank. Erst nach erfolgreichem API-Deployment wird der Worker
aktualisiert. Die Datenbank liegt in Neon Free in AWS Frankfurt. Railway läuft
in Amsterdam, weil Railway keine Region Frankfurt anbietet. Temporal Cloud
übernimmt die Prozesssteuerung; der Benutzer stellt Namespace und Zugang bereit.
Alle Verbindungen zu Datenbank und Temporal verwenden TLS mit Zertifikatsprüfung.
Render ist für diese Produktion keine Abhängigkeit.

Die Plattform prüft die API-Abhängigkeiten beim Deployment. Häufige externe
Überwachung verwendet dagegen den reinen Prozess-Healthcheck, damit eine ruhende
Neon-Datenbank nicht durch Monitoring dauerhaft aktiv gehalten wird. Das tatsächliche
Suspend-Verhalten und der Verbrauch werden am Anbieter überprüft.

Ein eigener kurzlebiger Backup-Container auf Railway erstellt alle zwölf Stunden
einen PostgreSQL-Dump. Gegenüber dem Ziel von 24 Stunden erlaubt dies einen
zeitlichen Puffer. Sicherungen liegen sieben Tage im privaten EU-Bucket des
unabhängigen Anbieters Cloudflare R2. Nur das für dieses Projekt reservierte
Präfix darf bereinigt werden, und erst nach erfolgreichem Upload. Container-
Dateien sind temporär und werden nicht auf einer lokalen Entwicklerstation
abgelegt. Eine echte Wiederherstellungsprobe und die Überwachung fehlgeschlagener
oder ausbleibender Backups gehören zur Produktionsabnahme.

Die API verwendet die eigene Domain bei World4You. Benachrichtigungen gehen an
die bisher als Render-Kontoadresse bezeichnete E-Mail-Adresse des Benutzers;
mit dem Plattformwechsel müssen sie in Railway eingerichtet und geprüft werden.
Zugangsdaten werden ausschließlich als Anbieter-Secrets gespeichert.

## Betrachtete Alternativen

Render verursacht für dieses Beispiel zusätzliche Instanzkosten neben dem bereits
vorhandenen Railway-Tarif und wird auf ausdrücklichen Benutzerwunsch ersetzt.
Neon Launch mit automatischen Backups wurde angeboten; der Benutzer wählt Neon
Free mit separaten Sicherungen. Speicher bei Neon selbst würde Datenbank und
Backup-Zugang an denselben Anbieter binden. Backups auf workhorse würden eine
lokale Produktionsabhängigkeit schaffen. Migrationen im normalen Startprozess
oder in einem dauerhaften Migrationsdienst bleiben ausgeschlossen.

## Konsequenzen

Das Produktionssetup benötigt keinen eigenen Server. Anwendung, Prozesssteuerung,
Datenbank und Backup-Speicher haben getrennte Verantwortlichkeiten und Secrets.
Railway rechnet Verbrauch über das enthaltene Hobby-Guthaben hinaus ab; das
Guthaben ist keine Kostenobergrenze. Neon Free hat begrenzte Compute-Ressourcen.
Die Wiederherstellungsziele sind Betriebsziele, keine durch diese Entscheidung
bewiesenen Garantien. Für eine abgeschlossene Abnahme fehlen ohne erfolgreiche
Zielplattformtests ausdrücklich die Nachweise zu Release-Isolation und Restore.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
