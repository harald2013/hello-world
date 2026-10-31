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
    ├── ruleset protect-main
    ├── ruleset protect-tags
    ├── installation idp-openhands-agent
    ├── workflow Report example · Tests and checks
    ├── workflow Report example · Container images
    ├── package report-example-api
    ├── package report-example-worker
    └── package report-example-backup
```

## Artifacts

| Name | ID | Kind | Description |
| --- | --- | --- | --- |
| harald2013/report-example | 1406819325 | repository | Public; renamed from `hello-world` on 2026-10-26, GitHub redirects the old URLs; remote `git@github.com:harald2013/report-example.git`; default branch `main` protected by the rulesets below, changes only through PRs; merged head branches are deleted automatically (`delete_branch_on_merge`) |
| main | main | branch | PR base; source of staging images |
| protect-main | 26270188 | ruleset | Default branch: no deletion, no force push, changes only through PRs, updates restricted; bypass only for the role Repository admin and only when merging a PR (`gh pr merge --admin` or "bypass rules" in the UI) |
| protect-tags | 26274857 | ruleset | All tags: no creation, update or deletion; bypass only for the role Repository admin |
| idp-openhands-agent | 177241581 | github app installation | App ID 5556242, installed only on this repository; Contents rw and Metadata r, no webhook; push identity of the OpenHands implementation agent; private key only on the VM `wh-openhands` (`harald2013/infrastructure`, `openhands/README.md`) |
| Report example · Tests and checks | .github/workflows/ci.yml | workflow | Runs on PRs and pushes to `main` |
| Report example · Container images | .github/workflows/image.yml | workflow | Pushes to `main` and `feature/**` publish API, worker and backup images tagged `sha-<commit>` |
| report-example-api | ghcr.io/harald2013/report-example-api | container package | API image; Coolify staging application `api` |
| report-example-worker | ghcr.io/harald2013/report-example-worker | container package | Worker image; Coolify staging application `worker` |
| report-example-backup | ghcr.io/harald2013/report-example-backup | container package | Backup image for the Railway scheduled job |
