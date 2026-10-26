# Railway — production

## Instance

- Instance or account: Default Workspace (`0610c2d4-bd3f-41d0-85eb-201765a22101`), personal
- Plan and region: Hobby; Amsterdam (`europe-west4-drams3a`), Railway has no Frankfurt region
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
| api | 4147303e-c268-41f1-9215-b10170b1393d | service | Image: `ghcr.io/harald2013/report-example-api`; one replica; port 8000; pre-deploy `/app/.venv/bin/python -m reports.store`; deployment health check `/ready`; uses Neon and Temporal Cloud |
| worker | e0b02921-9ef7-48e7-9876-f1a8e2520470 | service | Image: `ghcr.io/harald2013/report-example-worker`; one replica; no public port; uses Neon and Temporal Cloud |
| backup | 624056df-2bcb-4c74-a456-3ae79b816a9b | service | Image: `ghcr.io/harald2013/report-example-backup`; one replica; start `python3 /app/backup.py`; cron `0 */12 * * *` UTC; restart policy NEVER; dumps Neon to Cloudflare R2 |
| api.report-example.ratzberger.net | 4cfafd53-0dce-493e-8201-8641bae11741 | custom domain | Port 8000 of `api`; World4You CNAME to `1yha62x4.up.railway.app` |

## Configuration

| Variable | Scope | Secret | Source |
| --- | --- | --- | --- |
| TEMPORAL_ADDRESS | shared | no | Temporal Cloud namespace endpoint |
| TEMPORAL_NAMESPACE | shared | no | Temporal Cloud namespace |
| TEMPORAL_TASK_QUEUE | shared | no | `reports-v1` |
| TEMPORAL_TLS | shared | no | `true` |
| TEMPORAL_API_KEY | shared | yes | Namespace-scoped Temporal Cloud API key |
| APP_ENV | api, worker | no | `production` |
| DATABASE_URL | api, worker, backup | yes | Neon connection string of the direct endpoint, `sslmode=verify-full` |
| API_TOKEN | api | yes | Random bearer token |
| PORT | api | no | `8000` |
| PGSSLROOTCERT | backup | no | `/etc/ssl/certs/ca-certificates.crt` |
| BACKUP_ENDPOINT, BACKUP_BUCKET, BACKUP_PREFIX, BACKUP_RETENTION_DAYS, AWS_DEFAULT_REGION | backup | no | Cloudflare R2 bucket and prefix; retention 7 days; region `auto` |
| AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY | backup | yes | Existing Cloudflare R2 S3 access of the user |

Variable values are never read back; check presence and references in Railway
without printing them.
