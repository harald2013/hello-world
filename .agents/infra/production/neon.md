# Neon — production

## Instance

- Instance or account: DefaultOrga (`org-round-art-12574450`), Free
- URL: https://console.neon.tech/app/projects/raspy-bar-83546186
- MCP server: `neon`, tools named `neon__…`

## Structure

```text
DefaultOrga
└── project report-example
    └── branch production
        ├── database reports
        └── read-write endpoint
```

## Artifacts

| Name | ID | Kind | Description |
| --- | --- | --- | --- |
| report-example | raspy-bar-83546186 | project | PostgreSQL 16 in AWS Frankfurt; application database for Railway |
| production | br-steep-feather-b97rn1r2 | branch | Default branch |
| reports | reports | database | Role reports; connection source is Neon get_connection_string, stored as Railway DATABASE_URL |
| endpoint | ep-weathered-rain-b9sk6ls0 | compute | 0.25 CU; ep-weathered-rain-b9sk6ls0.c-7.eu-central-1.aws.neon.tech |
