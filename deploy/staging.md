# Staging auf workhorse

Das Projekt `report-example` mit der Umgebung `staging` ist auf workhorse
angelegt. Die tatsächlichen Ressourcen, UUIDs, Netzwerk-Aliase und privaten
HTTPS-Adressen stehen in [COOLIFY.md](../COOLIFY.md). IDP dient als Beispiel
für Image-Anwendungen; seine Dienste und Zugangsdaten werden nicht verwendet.
Staging enthält ausschließlich synthetische Daten.

Die Anwendung verwendet das nach dem Entfernen von `Infrastructure` erhaltene
Netz `infrastructure-staging`. Der Name ist historisch; die fünf Anwendungen
gehören zum Projekt `report-example`. Das Netz ist vom IDP-Anwendungsnetz
getrennt. PostgreSQL erhält ein eigenes persistentes Volume.

API: https://workhorse.tail8fba42.ts.net:18443/docs  
Temporal UI: https://workhorse.tail8fba42.ts.net:18444/

Beide Adressen sind nur im Tailnet erreichbar. Tailscale Serve leitet auf die
Loopback-Bindings `127.0.0.1:18080` und `127.0.0.1:18081` weiter. PostgreSQL,
Temporal und Worker haben weder Host-Port noch öffentliche Domain. Der
API-Schlüssel liegt als Laufzeit-Secret `API_TOKEN` an der API-Anwendung in
Coolify; zum Verwenden gezielt dort abrufen und nicht in Dokumentation kopieren.

Der [Abnahmenachweis](staging-acceptance.md) enthält Image-Digests und Ergebnisse
der echten Deployment-, Persistenz- und Wiederanlauftests.

## Einzelne Ressourcen

In Coolify auf workhorse das Projekt `report-example` mit Umgebung
`staging` verwenden. Jede der folgenden Rollen wird eine eigenständige
Docker-Image-Anwendung. Compose wird hier nicht verwendet.

| Rolle | Imagequelle | Interner Alias | Port / Daten |
| --- | --- | --- | --- |
| PostgreSQL | `postgres:16.6` | `report-postgres` | 5432 intern; Volume `/var/lib/postgresql/data` |
| Temporal | `temporalio/auto-setup:1.29.7` | `report-temporal` | 7233 intern |
| Temporal UI | `temporalio/ui:2.51.0` | `report-temporal-ui` | 8080; nur privater Zugriff |
| API | `ghcr.io/harald2013/hello-world-api:sha-<commit>` | `report-api` | 8000; HTTPS über Tailscale Serve |
| Worker | `ghcr.io/harald2013/hello-world-worker:sha-<commit>` | `report-worker` | Kein eingehender Port |

`<commit>` ist der volle Commit des erfolgreich geprüften Image-Builds.
Für API und Worker dieselbe Revision verwenden. Der Image-Workflow veröffentlicht
auch Feature-Branch-Revisionen, damit Staging keinen Merge voraussetzt. Die unveränderlichen Image-Digests
nach dem Build festhalten und für die Übernahme nach Produktion verwenden.
Alle Rollen erhalten ein gemeinsames, nur für Staging vorgesehenes Netz und
die oben genannten Aliase. Datenbank, Temporal und Worker nicht öffentlich
veröffentlichen. API und UI bleiben ebenfalls ausschließlich im Tailnet. Der PostgreSQL-Container hält hier auch die separaten Datenbanken
für Temporals Ausführungshistorie; das ist ausschließlich ein Demo-/Staging-Aufbau.

## Konfiguration und Reihenfolge

1. PostgreSQL vor einem Austausch vollständig stoppen. In Coolify muss
   `is_consistent_container_name_enabled=true` aktiv sein. Niemals zwei
   PostgreSQL-Container mit demselben Datenverzeichnis starten. Das wurde durch
   einen echten Austausch mit anschließendem Datenzugriff überprüft.
   PostgreSQL-Konfiguration: `POSTGRES_USER=reports`, `POSTGRES_DB=reports`, eigenes zufälliges
   `POSTGRES_PASSWORD`. Healthcheck `pg_isready -U reports -d reports`.
2. Temporal nach gesundem PostgreSQL starten: `DB=postgres12`, `DB_PORT=5432`,
   `POSTGRES_USER=reports`, `POSTGRES_PWD` aus dem Secret,
   `POSTGRES_SEEDS=report-postgres`, `BIND_ON_IP=0.0.0.0`,
   `DEFAULT_NAMESPACE=default`. Mit dem Admin-Tools-Image aus Compose die
   Bereitschaft des Namespace prüfen; bis dahin API/Worker nicht starten.
3. Temporal UI mit `TEMPORAL_ADDRESS=report-temporal:7233` starten. Die UI
   ausschließlich privat zugänglich machen.
4. API-/Worker-Konfiguration anhand `staging.env.example` als Coolify-Secrets
   und normale Variablen setzen. Zugangsdaten im Datenbank-URI URL-kodieren.
5. Als einmaligen Job das geprüfte API-Image mit `python -m reports.store`
   im selben Netz und mit denselben Variablen starten. Exitcode 0 abwarten.
   Der Job initialisiert das Schema und ist keine dauerhaft laufende Anwendung.
6. Worker und API starten. API-Healthcheck als Kommando im Image (Python-Standardbibliothek):
   `python -m reports.healthcheck`,
   Timeout mindestens 10 Sekunden. Für den Worker keinen HTTP-Healthcheck
   konfigurieren; Prozessüberwachung und erfolgreich verarbeitete Aufträge prüfen.
7. Authentifizierten Smoke-Test gegen die Staging-API ausführen:

```bash
API_BASE_URL=https://STAGING-API API_TOKEN="$STAGING_API_TOKEN" \
  uv run python scripts/smoke.py
```

Für einen Wiederanlauftest einen Auftrag mit 120 Sekunden Verzögerung anlegen,
auf den Datenbankeintrag warten und nur die Worker-Anwendung in Coolify neu
starten. Derselbe Auftrag muss anschließend fertig werden. Den lokalen
`--restart-worker`-Schalter nicht gegen Staging verwenden.

Die tatsächlich eingerichteten URLs, UUIDs, Aliase und Volumes gehören nach
`COOLIFY.md`. Aktuelle Versionen und Deployment-Ergebnisse live prüfen; sie
gehören nicht in diese stabile Ressourcenübersicht.

## Konfiguration der installierten Coolify-Version

Das MCP-Tool unterstützt derzeit weder `ports_mappings` noch Kommando-Healthchecks.
Die native API unterstützt Kommando-Healthchecks mit `health_check_type=cmd`,
lehnt aber in dieser Version Loopback-Portbindungen ab. Die Portbindungen
der beiden neuen Anwendungen wurden deshalb gezielt über Coolifys Anwendungsmodell
konfiguriert und anschließend über die API und Docker zurückgelesen. Der API-
Healthcheck nutzt `python -m reports.healthcheck`, weil Coolify im Kommando nur
einfache Zeichen zulässt. Der Image-Startbefehl bleibt unverändert. Bei späteren Änderungen zuerst die aktuellen Fähigkeiten prüfen;
keine Ports vorübergehend auf allen Host-Interfaces veröffentlichen.

## Aufbauvorfall und Wiederherstellung

Beim initialen Einrichten wurde PostgreSQL mit dem Rolling-Verfahren aktualisiert.
Die überlappenden Prozesse beschädigten das neu angelegte Demo-Datenverzeichnis.
Es waren noch keine Benutzerberichte vorhanden. PostgreSQL und Temporal wurden
gestoppt, die Ersatzstrategie korrigiert und ein frisches Volume eingerichtet.
Das alte Volume bleibt unbenutzt zur Untersuchung erhalten; seine Zuordnung
und das aktive Volume stehen in `COOLIFY.md`. Das ist keine Wiederherstellungs-
strategie für Nutzdaten. Für bestehende Daten sind Backups und eine ausdrücklich
geplante Wiederherstellung erforderlich; siehe [ADR 0005](../docs/adr/0005-stateful-staging-updates.md).
