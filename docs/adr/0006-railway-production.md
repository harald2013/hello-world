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

Produktion folgt der Referenzarchitektur `ADR-reference-architecture-production`
des `development-mcp`: vorgebaute, in Staging geprüfte Images auf Railway,
Pre-Deploy-Migration der API vor dem Worker, Neon mit TLS über den direkten
Endpoint, Temporal Cloud, unabhängige Backups nach Cloudflare R2, getrennte
Healthchecks für Deployment und Monitoring sowie deren Abnahmeliste. Dieses ADR
hält nur die projektspezifischen Werte und Abweichungen fest.

Projektspezifische Werte:

- Railway-Hobby-Workspace in Amsterdam, weil Railway keine Region Frankfurt
  anbietet; Neon Free in AWS Frankfurt mit fester Compute-Größe von 0.25 CU.
- Budget 50 Euro monatlich, höchstens 100 Berichte pro Tag; RPO und RTO je
  24 Stunden.
- Backups alle zwölf Stunden mit sieben Tagen Aufbewahrung im privaten
  EU-Bucket des Benutzers unter dem Präfix `report-example/production/`.
- Die API-Domain liegt in der Zone des Benutzers bei World4You.
- Benachrichtigungen gehen an die E-Mail-Adresse des Benutzers und werden in
  Railway eingerichtet.

Abweichung von der Referenz: Der Benutzer stellt einen bestehenden
Temporal-Cloud-Namespace bereit, der auch Workflows anderer Anwendungen
enthalten kann, statt eines eigenen Namespace für diese Anwendung und Umgebung.
Ein eigener Namespace verursacht für das kleine Beispiel zusätzlichen
Verwaltungsaufwand. Abfragen bleiben deshalb auf die Task Queue und die
Berichtskennungen dieser Anwendung beschränkt.

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
bewiesenen Garantien. Als abgenommen gilt Produktion erst mit den Nachweisen,
die die Referenzarchitektur verlangt; sie stehen in `deploy/production-setup.md`.

Die technischen Leitplanken stehen in der
[AGENT_RULES.md](../../AGENT_RULES.md).
