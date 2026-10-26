# Neon — production

## Instance

- Instance or account: DefaultOrga (`org-round-art-12574450`)
- Plan and region: Free (`free_v3`); AWS Frankfurt (`aws-eu-central-1`)
- URL: https://console.neon.tech/app/projects/raspy-bar-83546186
- MCP server: `neon`, tools named `neon__…`

## Structure

```text
DefaultOrga
└── project report-example
    └── branch production
        ├── database reports
        └── endpoint ep-weathered-rain-b9sk6ls0
```

## Artifacts

| Name | ID | Kind | Description |
| --- | --- | --- | --- |
| report-example | raspy-bar-83546186 | project | PostgreSQL 16 in AWS Frankfurt; maintenance window Wednesday 00:00–01:00 UTC; application database for Railway |
| production | br-steep-feather-b97rn1r2 | branch | Default branch |
| reports | reports | database | Owned by role `reports`; Railway services read it through `DATABASE_URL` |
| ep-weathered-rain-b9sk6ls0 | ep-weathered-rain-b9sk6ls0 | endpoint | Read-write; fixed 0.25 CU; direct host `ep-weathered-rain-b9sk6ls0.c-7.eu-central-1.aws.neon.tech`; pooling not used |
