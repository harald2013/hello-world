# Migrationen in der Railway-Pre-Deploy-Phase

Railway ist für dieses Beispiel ausgewählt. Die Dienste sind angelegt; die
Plattform-Abnahme steht noch aus. ADR 0006 ersetzt die frühere Render-Auswahl.

## Image und Befehl

```text
/app/.venv/bin/python -m reports.store
```

Das API-Image enthält Python, psycopg und den Migrationscode. Das Dockerfile setzt
zusätzlich `/app/.venv/bin` im PATH. Keine Installation und kein Build auf Railway
sind nötig. Die Migration verwendet die Runtime-Variablen aus
[production.env.example](production.env.example), einschließlich Produktions-TLS
und API-Token-Validierung, verbindet sich aber nur zur Datenbank.

Der Prozess meldet `Migration started`, bei Erfolg `Migration completed` und
Exit-Code 0. Bei Fehlern meldet er `Migration failed (<Fehlertyp>)` und Exit-Code 1;
Verbindungsdetails und Secrets werden nicht ausgegeben. PostgreSQL führt DDL
und Advisory Lock in einer Transaktion aus. Ein SQL-Fehler rollt diese zurück.
Der Lock serialisiert konkurrierende Jobs; das aktuelle Statement-Limit beträgt
5 Sekunden, auch beim Warten auf den Lock. Timeout blockiert das Release.

Aktuell initialisiert der Befehl eine Tabelle wiederholbar. Er ersetzt noch kein
versioniertes Migrationssystem für spätere Schemaänderungen.

## Railway konfigurieren

1. API als Dienst aus dem bereits geprüften APIimage-Digest konfigurieren.
   Keine Plattform-Builds. Runtime-Variablen und Registry-Zugriff setzen.
2. In Settings → Deploy den Pre-Deploy Command
   `/app/.venv/bin/python -m reports.store` setzen. Native Pre-Deploy-Phase
   bei jedem Deployment ausführen lassen. Healthcheck `/ready`, Port 8000.
3. Erst nach erfolgreichem API-Deployment das passende Workerimage ausrollen.
   Der Worker erhält keinen eigenen Pre-Deploy-Befehl. Kein paralleles Commit
   eines Railway-Patches, das API und Worker zugleich aktualisiert.
4. Secrets im Dashboard hinterlegen; keine Migration im normalen Startbefehl
   und kein dauerhafter Migrationsdienst.

## Lokaler Container-Nachweis

```bash
docker compose up --build -d --wait --wait-timeout 240
docker compose run --rm --no-deps -T api python < scripts/check_migrations.py
```

Der temporäre Container verwendet das API-Image und wird durch `--rm` entfernt.
Der Test legt ausschließlich im lokalen Compose-Postgres eine temporäre Datenbank
an, löst nach DDL einen SQL-Fehler aus, prüft Exit-Code und Rollback, führt den
echten Befehl zweimal erfolgreich aus und prüft die weiterhin laufende API.
Die Testdatenbank wird anschließend gelöscht. CI und Image-Veröffentlichung
führen diesen Test aus. Das prüft die Migration, nicht Railways Deploymentlogik.

## Ausstehende Plattform-Abnahme

In einer eigenen Railway-Testumgebung mit synthetischen Daten durchführen:

1. Eine funktionierende alte Version bereitstellen. Service-ID, bisherigen
   Image-Digest und Deployment-ID als Vergleich festhalten.
2. Neuen getesteten Digest setzen und explizit deployen. In den Logs Start und
   Erfolg der Migration mit Exit-Code 0 nachweisen. Die neue API darf erst danach
   starten; nach erfolgreichem `/ready` wird der Traffic umgeschaltet und die
   alte Instanz heruntergefahren. Währenddessen die bisherige API abrufen.
3. Nur im Testdienst den Pre-Deploy-Befehl vorübergehend durch
   `/app/.venv/bin/python -c 'raise SystemExit(1)'` ersetzen und erneut deployen.
   Deployment muss fehlschlagen; neue Version darf nicht live gehen. Die bisherige
   Deployment-ID und erreichbare alte API müssen erhalten bleiben. Dieser Test
   prüft die Plattformsperre ohne absichtlich schädliches SQL.
4. Den echten Befehl wiederherstellen, erneut deployen, `/ready` und den
   authentifizierten Smoke-Test prüfen. Logs und Deployment-IDs ohne Secrets als
   Abnahme-Nachweis festhalten. Fehlerfälle nicht gegen Produktion ausprobieren.

Alte API und Worker laufen während der Migration weiter. Deshalb müssen
Schemaänderungen rückwärtskompatibel sein (Expand/Contract). Ein erfolgreicher
Migrationsjob mit anschließend fehlgeschlagenem App-Start setzt das Schema nicht
automatisch zurück. Destruktive Änderungen erst nach separater Freigabe und dem
Entfernen aller alten Verbraucher durchführen.

Quellen: [Railway Pre-Deploy](https://docs.railway.com/deployments/pre-deploy-command),
[Healthchecks](https://docs.railway.com/deployments/healthchecks).
