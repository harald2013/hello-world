# Cloudflare — production

## Instance

- Instance or account: Cloudflare account (`960c285a06dcb6cb9a4f8212c9b5ae46`), supplied by the user
- Plan and region: plan not recorded, read it in the dashboard; R2 EU jurisdiction
- URL: https://dash.cloudflare.com
- MCP server: none; S3 access from the Railway service `backup`

## Structure

```text
Cloudflare account
└── bucket default-bucket
    └── prefix report-example/production/
```

## Artifacts

| Name | ID | Kind | Description |
| --- | --- | --- | --- |
| default-bucket | default-bucket | bucket | Private, EU jurisdiction, shared with other uses of the user; S3 endpoint `https://960c285a06dcb6cb9a4f8212c9b5ae46.eu.r2.cloudflarestorage.com` |
| report-example/production/ | report-example/production/ | prefix | Database dumps of the Railway service `backup`; seven-day retention; the only deletion scope of this project |

Access keys come from the user's existing R2 S3 access and are set as
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` on the Railway service `backup`.
