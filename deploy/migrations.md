# Migrationen in der Render-Pre-Deploy-Phase

Render ist für dieses Beispiel ausgewählt. Ein Render-Service existiert noch
nicht; die Konfiguration ist vorbereitet, die Plattform-Abnahme steht aus.
Railway bleibt eine alternative Betriebsoption, wird hier nicht eingerichtet.

## Image und Befehl

```text
/app/.venv/bin/python -m reports.store
```

Das API-Image enthält Python, psycopg und den Migrationscode. Das Dockerfile setzt
zusätzlich `/app/.venv/bin` im PATH. Keine Installation und kein Build auf Render
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

## Render konfigurieren

1. Den API-Dienst als bezahlten **Web Service / Existing Image** anlegen. Als
   Image den zuvor getesteten API-Digest verwenden, Registry-Zugang hinterlegen.
   Region und Tarif auswählen; kein Repository-Build und kein persistenter Disk.
2. Runtime-Variablen setzen. Unter **Settings → Build & Deploy → Pre-Deploy
   Command** exakt den obigen Befehl eintragen. Den Docker-Startbefehl aus dem
   Image übernehmen; Healthcheck `/ready` setzen.
3. Pre-Deploy bei jedem Release ausführen lassen, auch beim ersten. Kein
   separater Migrations-Dauerdienst und keine Migration in CMD/Entrypoint.
4. Nach erfolgreichem API-Deployment den passenden Worker-Digest ausrollen.
   Der Worker erhält dieselben Runtime-Werte, aber keinen Pre-Deploy-Befehl.
   Die beiden Dienste werden von Render nicht automatisch gemeinsam geordnet.

[render.yaml.example](render.yaml.example) bildet diese Einstellungen als
Blueprint-Vorlage ab. Die Digest-Platzhalter ersetzen; `starter` und `frankfurt`
sind Vorschläge. Die Vorlage wird nicht automatisch angewendet. Beim ersten
Setup zunächst nur den API-Eintrag übernehmen und erst nach dessen erfolgreicher
Pre-Deploy-Phase den Worker ergänzen. Secrets für beide Dienste konsistent setzen.

Vorgebaute Images werden bei Render nicht allein durch einen Registry-Push neu
ausgerollt. Den getesteten neuen Digest setzen und ein manuelles/API-Deployment
auslösen. Dadurch läuft die native Pre-Deploy-Phase automatisiert pro Deployment.

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
führen diesen Test aus. Das prüft die Migration, nicht Renders Deploymentlogik.

## Ausstehende Plattform-Abnahme

In einer eigenen Render-Testumgebung mit synthetischen Daten durchführen:

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

Quellen: [Render-Deployment und Pre-Deploy](https://render.com/docs/deploys),
[Blueprint-Spezifikation](https://render.com/docs/blueprint-spec),
[vorgebaute Images](https://render.com/docs/deploying-an-image).
