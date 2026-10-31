# World4You — production

## Instance

- Instance or account: World4You customer account of the user (ID not recorded)
- Plan and region: tariff for mail and domain only; DNS hosting of `ratzberger.net`
- URL: https://www.world4you.com
- MCP server: none; records are changed by the user in the web interface

## Structure

```text
World4You customer account
└── zone ratzberger.net
    ├── record CNAME api.report-example
    └── record TXT _railway-verify.api.report-example
```

## Artifacts

| Name | ID | Kind | Description |
| --- | --- | --- | --- |
| ratzberger.net | ratzberger.net | zone | Domain of the user; other records are outside this project |
| api.report-example | api.report-example CNAME | record | Routing: CNAME to `1yha62x4.up.railway.app`, the Railway custom domain `api.report-example.ratzberger.net` |
| _railway-verify.api.report-example | _railway-verify.api.report-example TXT | record | Ownership verification of the same Railway custom domain; value from Railway's domain configuration |
