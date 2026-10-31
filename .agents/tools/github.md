# GitHub

How this repository uses GitHub, in every environment. Maintained by agents
under the `tool-context` rule from the development MCP server. Record only
working, current usage. Never store secrets; name only where they come from.
Identifiers and structure per environment live in `.agents/infra/`.

## Access

- Interface: `git` over SSH, the workflow scripts in `scripts/` and the `gh`
  CLI
- Authentication: SSH key for `git`, `gh auth login` for `gh`
- Credential source: the user's SSH agent and `gh` keyring; never print tokens

## Common tasks

### Commit and push a feature branch

```bash
python3 -B scripts/git_commit.py <repository> <message>
python3 -B scripts/git_push.py   <repository> [remote] [base]
```

### Open a PR against main

`gh pr create --base main --head feature/til-<number>-<name>`.

### Find the image of a commit

Image tags are `sha-<full commit SHA>` in
`ghcr.io/harald2013/report-example-api` and
`ghcr.io/harald2013/report-example-worker`; check the run of
`Report example · Container images` with `gh run list --workflow image.yml`.

## Pitfalls

- Never push directly to `main`; changes reach it only through a PR. Merging
  into `main` needs the admin bypass (`gh pr merge --admin`, or "Merge without
  waiting for requirements to be met" in the UI); auto-merge does not work.
- The GitHub App `idp-openhands-agent` (implementation agent) pushes feature
  branches with Contents rw. Contents rw also allows merging a PR through
  `PUT /repos/{owner}/{repo}/pulls/{n}/merge`; only a ruleset that restricts
  updates of the base branch stops that, PR permissions do not.
- Listing or deleting container packages through `gh api` needs the
  `read:packages` or `delete:packages` scope; the default `gh` login lacks
  them. The user adds them with
  `gh auth refresh -h github.com -s read:packages,delete:packages`, which
  needs a browser confirmation.

## References

- [AGENTS.md](../../AGENTS.md#workflow)
