# Railway — production

## Instance

- Instance or account: Default Workspace (`0610c2d4-bd3f-41d0-85eb-201765a22101`)
- URL: https://railway.com/project/1e9af838-3bcd-47fa-b938-06ad91320c18
- MCP server: `railway`, tools named `railway__…`

## Structure

```text
Default Workspace
└── project report-example
    └── environment production
        ├── service api
        │   └── custom domain api.report-example.ratzberger.net
        ├── service worker
        └── service backup
```

## Artifacts

| Name | ID | Kind | Description |
| --- | --- | --- | --- |
| report-example | 1e9af838-3bcd-47fa-b938-06ad91320c18 | project | Private application project |
| production | 15457c1a-9b64-458a-8049-0424a16aa501 | environment | Production environment |
| api | 4147303e-c268-41f1-9215-b10170b1393d | service | Image source ghcr.io/harald2013/hello-world-api; native pre-deploy migration; Neon and Temporal Cloud |
| worker | e0b02921-9ef7-48e7-9876-f1a8e2520470 | service | Image source ghcr.io/harald2013/hello-world-worker; no public port |
| backup | 624056df-2bcb-4c74-a456-3ae79b816a9b | service | Image source ghcr.io/harald2013/hello-world-backup; every twelve hours, Neon dumps to Cloudflare R2 |
| api.report-example.ratzberger.net | 4cfafd53-0dce-493e-8201-8641bae11741 | custom domain | API port 8000; World4You CNAME to 1yha62x4.up.railway.app |

All application services use Amsterdam (`europe-west4-drams3a`), one replica.
Backup start command: `python3 /app/backup.py`; cron `0 */12 * * *` UTC; restart policy NEVER.
Runtime secrets are Railway variables. Read deployment and certificate status live.
