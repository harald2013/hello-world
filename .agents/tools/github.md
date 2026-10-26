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

- Never push directly to `main`; changes reach it only through a PR.
- Listing container packages through `gh api` needs the `read:packages`
  scope; the default `gh` login lacks it.

## References

- [AGENTS.md](../../AGENTS.md#workflow)
