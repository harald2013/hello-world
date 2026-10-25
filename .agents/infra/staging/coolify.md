# Coolify

Reference for the Coolify instance that hosts the `staging` environment of
this repository.
A UUID is the identifier Coolify uses in its API and MCP tools.

## Instance workhorse

URL: http://workhorse:8000/

Reach this instance through MCP Jungle under the server name `coolify-workhorse`.
Its tools are named `coolify-workhorse__…`.

```
workhorse
└── server localhost
    └── project report-example
        └── environment staging
            ├── postgres
            ├── temporal
            ├── temporal-ui
            ├── api
            └── worker
```

The project uses the existing dedicated staging Docker network `infrastructure-staging` (`oluvljjdh550m6de7ifsdfe8`). Its historical name is
retained after removal of the former Infrastructure project. IDP remains on
its separate `coolify` network.

### Servers

| Name | UUID | Description |
| --- | --- | --- |
| localhost | k2pzw09j1owsdf32hanppxcg | Workhorse, reachable at host.docker.internal |

### Projects

| Name | UUID | Description |
| --- | --- | --- |
| report-example | paxi2fhovbegez4lh7gxdgjj | Portable report example; synthetic staging data |

### Environments

| Name | UUID | Description |
| --- | --- | --- |
| staging | vnrcu8rqf21fbjhfr1rp2hmt | Independent image applications |

### Resources

| Name | UUID | Kind | Deployment | Description |
| --- | --- | --- | --- | --- |
| postgres | fsew7ydowsjgjbbnickyi65b | application | Image: `postgres` | Staging postgres; network alias `report-postgres`; not exposed |
| temporal | 4gfrxde9n3p9frl40uchk8kp | application | Image: `temporalio/auto-setup` | Staging temporal; network alias `report-temporal`; not exposed |
| temporal-ui | kswxe11wew0loawo3bjznsth | application | Image: `temporalio/ui` | Temporal UI; network alias `report-temporal-ui`; https://workhorse.tail8fba42.ts.net:18444/ (tailnet only), host loopback 127.0.0.1:18081 |
| api | xjpuw1wkf44xr8kr7pw8frob | application | Image: `ghcr.io/harald2013/hello-world-api` | Staging API; network alias `report-api`; https://workhorse.tail8fba42.ts.net:18443/ (tailnet only), host loopback 127.0.0.1:18080 |
| worker | dfubqqftacrok6fw7cqydmiz | application | Image: `ghcr.io/harald2013/hello-world-worker` | Staging worker; network alias `report-worker`; not exposed |

PostgreSQL uses the named persistent volume `report-example-postgres-data-v2`
(storage UUID `edcemtmh5vakw7axotdeiqo0`) at
`/var/lib/postgresql/data`. Image versions and deployment results are read live.

PostgreSQL uses consistent container naming and must stop before replacement.
Never run two PostgreSQL containers against this volume. The retired volume
`fsew7ydowsjgjbbnickyi65b-report-example-postgres-data` is retained unattached
after the initial setup incident; it must not be mounted by running services.
