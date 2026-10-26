# GitHub — shared

Artifacts of GitHub in the `shared` environment of this repository.
Maintained by agents under the `tool-context` rule from the development MCP
server. Record stable identifiers and structure only; read pull requests,
checks, image tags and commits live. Never store secrets.

## Instance

- Instance or account: github.com, personal account `harald2013`
- Plan and region: GitHub Free; region not applicable
- URL: https://github.com/harald2013/hello-world
- MCP server: none; use the `gh` CLI

## Structure

```
harald2013
└── repository hello-world
    ├── branch main
    ├── workflow Report example · Tests and checks
    ├── workflow Report example · Container images
    ├── package hello-world-api
    ├── package hello-world-worker
    └── package hello-world-backup
```

## Artifacts

| Name | ID | Kind | Description |
| --- | --- | --- | --- |
| harald2013/hello-world | 1406819325 | repository | Public; remote `git@github.com:harald2013/hello-world.git`; default branch `main` without branch protection, changes only through PRs |
| main | main | branch | PR base; source of staging images |
| Report example · Tests and checks | .github/workflows/ci.yml | workflow | Runs on PRs and pushes to `main` |
| Report example · Container images | .github/workflows/image.yml | workflow | Pushes to `main` and `feature/**` publish API, worker and backup images tagged `sha-<commit>` |
| hello-world-api | ghcr.io/harald2013/hello-world-api | container package | API image; Coolify staging application `api` |
| hello-world-worker | ghcr.io/harald2013/hello-world-worker | container package | Worker image; Coolify staging application `worker` |
| hello-world-backup | ghcr.io/harald2013/hello-world-backup | container package | Backup image for the Railway scheduled job |
