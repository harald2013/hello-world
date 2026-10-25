# Temporal — production

## Instance

- Instance or account: Temporal Cloud, namespace supplied by user
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
| default-namespace.rq4it | default-namespace.rq4it | namespace | User-supplied endpoint default-namespace.rq4it.tmprl.cloud:7233; Railway API and worker connect using TLS |

Credentials originate from a namespace-scoped Temporal Cloud key entered as
TEMPORAL_API_KEY in each Railway application service. Do not read unrelated workflows.
