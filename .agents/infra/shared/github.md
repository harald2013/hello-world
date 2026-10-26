# GitHub — shared

Artifacts of GitHub in the `shared` environment of this repository.
Maintained by agents under the `tool-context` rule from the development MCP
server. Record stable identifiers and structure only; read pull requests,
checks, image tags and commits live. Never store secrets.

## Instance

- Instance or account: github.com, personal account `harald2013`
- Plan and region: GitHub Free; region not applicable
- URL: https://github.com/harald2013/report-example
- MCP server: none; use the `gh` CLI

## Structure

```
harald2013
└── repository report-example
    ├── branch main
    ├── workflow Report example · Tests and checks
    ├── workflow Report example · Container images
    ├── package report-example-api
    ├── package report-example-worker
    ├── package report-example-backup
    ├── package hello-world-api (former name)
    ├── package hello-world-worker (former name)
    └── package hello-world-backup (former name)
```

## Artifacts

| Name | ID | Kind | Description |
| --- | --- | --- | --- |
| harald2013/report-example | 1406819325 | repository | Public; renamed from `hello-world` on 2026-10-26, GitHub redirects the old URLs; remote `git@github.com:harald2013/report-example.git`; default branch `main` without branch protection, changes only through PRs |
| main | main | branch | PR base; source of staging images |
| Report example · Tests and checks | .github/workflows/ci.yml | workflow | Runs on PRs and pushes to `main` |
| Report example · Container images | .github/workflows/image.yml | workflow | Pushes to `main` and `feature/**` publish API, worker and backup images tagged `sha-<commit>` |
| report-example-api | ghcr.io/harald2013/report-example-api | container package | API image; Coolify staging application `api` |
| report-example-worker | ghcr.io/harald2013/report-example-worker | container package | Worker image; Coolify staging application `worker` |
| report-example-backup | ghcr.io/harald2013/report-example-backup | container package | Backup image for the Railway scheduled job |
| hello-world-api | ghcr.io/harald2013/hello-world-api | container package | Former API image repository; no new images; Railway `api` until switched (TIL-181); keep for rollback |
| hello-world-worker | ghcr.io/harald2013/hello-world-worker | container package | Former worker image repository; no new images; Railway `worker` until switched (TIL-181); keep for rollback |
| hello-world-backup | ghcr.io/harald2013/hello-world-backup | container package | Former backup image repository; no new images; Railway `backup` until switched (TIL-181); keep for rollback |
