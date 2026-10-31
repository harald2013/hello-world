# Temporal — production

## Instance

- Instance or account: Temporal Cloud account of the user; namespace supplied by the user
- Plan and region: Developer; AWS `eu-central-1`
- URL: https://cloud.temporal.io
- MCP server: `temporal-cloud`, tools named `temporal_cloud__…`

## Structure

```text
Temporal Cloud
└── namespace default-namespace.rq4it
    └── task queue reports-v1
```

## Artifacts

| Name | ID | Kind | Description |
| --- | --- | --- | --- |
| default-namespace.rq4it | default-namespace.rq4it | namespace | gRPC endpoint `default-namespace.rq4it.tmprl.cloud:7233`; TLS with a namespace-scoped API key from `TEMPORAL_API_KEY`; may also hold workflows of other applications of the user |
| reports-v1 | reports-v1 | task queue | Report workflows and activities of the Railway `worker` |
