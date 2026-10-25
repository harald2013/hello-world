# Report example

Kleine Vorlage für lokale Entwicklung, Staging und gemanagte Produktion.
Die API nimmt Zahlen entgegen, ein Temporal-Worker erstellt nach einer kurzen
Wartezeit einen Bericht, PostgreSQL speichert das Ergebnis. Eine zusätzliche
Weboberfläche ist für dieses erste Beispiel nicht erforderlich; die API ist
über curl und die interaktive Dokumentation unter `/docs` bedienbar.

| Rolle | Lokal | Staging | Produktion |
| --- | --- | --- | --- |
| API | Anwendungsimage in Compose | Dasselbe Image einzeln in Coolify | Dasselbe Image auf Render oder Railway |
| Worker | Workerimage in Compose | Dasselbe Image einzeln in Coolify | Dasselbe Image beim Anwendungsanbieter |
| Prozesssteuerung | Temporal-Container | Temporal-Container auf workhorse | Temporal Cloud |
| Anwendungsdaten | PostgreSQL-Container | PostgreSQL-Container auf workhorse | Neon |

Der Code und die Konfigurationen liegen hier. Ein Staging- oder SaaS-Deployment
wird durch das Auschecken oder Starten dieses Beispiels nicht angelegt.
Der lokale Durchlauf ist die erste Stufe; echte Anbieterressourcen werden
anschließend eingerichtet. Die Vorlage wird vor der Ableitung allgemeiner
Development-MCP-Regeln praktisch erprobt.

## Lokal starten

Docker mit Compose v2 oder neuer ist erforderlich:

```bash
cp .env.example .env
docker compose up --build -d --wait --wait-timeout 240
curl --fail http://127.0.0.1:18000/ready
```

Die API läuft auf `http://127.0.0.1:18000`, die Temporal-Oberfläche auf
`http://127.0.0.1:18243`. PostgreSQL hat keinen veröffentlichten Port.
Die Zugangsdaten aus `.env.example` sind ausschließlich für lokale Testdaten.
Bei belegten Ports die Werte in `.env` ändern.

```bash
curl --fail -X POST http://127.0.0.1:18000/reports \
  -H 'Content-Type: application/json' \
  -d '{"values": [10, 20, 30], "delay_seconds": 10}'
# Die Antwort enthält id und url. Anschließend die zurückgegebene URL abrufen:
curl --fail http://127.0.0.1:18000/reports/BERICHTS-ID
```

Nach der Verarbeitung enthält `result` Anzahl, Summe, Minimum, Maximum und
Mittelwert. Status vor Abschluss kommt aus Temporal; fertige Ergebnisse bleiben
in PostgreSQL und sind auch nach Ablauf der Temporal-Historie abrufbar.
Ein fehlender Worker lässt den Auftrag zunächst warten. Nach einer Stunde endet
ein nicht abgeschlossener Workflow durch sein Ausführungszeitlimit. Datenbankfehler
werden pro Aktivität bis zu zehnmal wiederholt.

POST erzeugt immer einen neuen Auftrag. Bei einem Verbindungsabbruch kann der
Auftrag schon angenommen worden sein: erneutes POST kann daher einen weiteren
Bericht erzeugen. Die API behauptet keine Exactly-once-Zustellung von HTTP-Anfragen.

## Durchlauf und Wiederaufnahme prüfen

Python ab 3.12 und `uv` werden für die Prüfbefehle benötigt:

```bash
uv sync --locked
./scripts/verify
uv run python scripts/smoke.py
uv run python scripts/smoke.py --restart-worker
docker compose exec -T api python < scripts/check_store.py
```

Der letzte Befehl startet einen Bericht mit 30 Sekunden Wartezeit, wartet auf
den ersten Datenbankeintrag, startet ausschließlich den lokalen Beispiel-Worker
neu und prüft das persistierte Ergebnis. Im Temporal UI ist die ursprüngliche
Workflow-ID weiterhin sichtbar. Der Befehl muss im Repository-Verzeichnis gegen
die lokale Compose-Umgebung laufen.

`scripts/verify` prüft Ruff, API-Verträge, Konfiguration und einen echten
Temporal-Testserver mit Wiederholung, Worker-Wechsel und History-Replay. Beim
ersten Lauf lädt das Temporal-SDK sein Testserver-Binary; alternativ kann
`TEMPORAL_TEST_SERVER` auf ein vorhandenes Binary zeigen. Der zusätzliche
Smoke-Test prüft die echte API, Temporal und PostgreSQL gemeinsam.

```bash
docker compose down       # Container stoppen; Daten bleiben erhalten
docker compose down -v    # Nur lokale synthetische Beispieldaten löschen
```

## Images und Betriebsanleitungen

Der [CI-Workflow](.github/workflows/ci.yml) führt `scripts/verify` und den
vollständigen Compose-Durchlauf aus. Der [Image-Workflow](.github/workflows/image.yml)
veröffentlicht geprüfte API- und Workerimages nach GHCR mit `sha-<voller-commit>`.
API und Worker sind Build-Ziele desselben Dockerfiles und laufen als Benutzer
ohne Root-Rechte. Schema-Initialisierung verwendet das API-Image als einmaligen Job.

- [Staging: einzelne Coolify-Anwendungen](deploy/staging.md)
- [Produktion: Render, Temporal Cloud und Neon](deploy/production.md)
- [Migrationen: Render Pre-Deploy und Container-Tests](deploy/migrations.md)
- [Konfiguration und Betriebsprüfungen](deploy/operations.md)
- [Architekturentscheidung](docs/adr/0003-report-example.md)

Die bisherigen Entwicklungsskripte unter `scripts/git_*.py` bleiben unverändert.
