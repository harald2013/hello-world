# Agent Rules

## Report example — [ADR 0003](docs/adr/0003-report-example.md)

- The example MUST use Python, a FastAPI API, a Temporal worker, and PostgreSQL [ADR 0003].
- Workflow code MUST remain deterministic; database operations MUST run in retryable, idempotent activities [ADR 0003].
- API and worker images MUST be built once per revision and promoted unchanged between environments [ADR 0003].
- Local services MUST use Docker Compose and publish ports only on loopback [ADR 0003].
- Staging MUST deploy individual images on workhorse through Coolify and MUST NOT use Compose [ADR 0003].
- Production MUST use managed application hosting, Temporal Cloud, and Neon; it MUST NOT depend on workhorse [ADR 0003].
- Local and staging environments MUST use synthetic data and separate credentials from production [ADR 0003].
- Runtime configuration MUST come from environment variables; secrets MUST NOT enter images, source control, or logs [ADR 0003].
- Staging and production APIs MUST require an API token; production MUST enable Temporal TLS and database certificate verification [ADR 0003].
- Agents MUST keep deployed resource metadata separate from deployment instructions and MUST NOT invent resource identifiers [ADR 0003].

## Pre-deploy migrations — [ADR 0004](docs/adr/0004-pre-deploy-migrations.md)

- Render API deployments MUST run migrations from the new API image in the native pre-deploy phase and MUST stop on failure [ADR 0004].
- Migrations MUST NOT run in normal API or worker startup commands or in a dedicated permanent service [ADR 0004].
- Migration processes MUST return a nonzero exit code on failure and MUST NOT log secrets [ADR 0004].
- Database migrations MUST serialize concurrent execution and use bounded waits and transactions where supported [ADR 0004].
- Schema changes MUST remain compatible with running API and worker versions; later schema changes MUST use versioned migrations [ADR 0004].
- Worker releases MUST follow successful API pre-deploy completion; agents MUST NOT assume cross-service deployment ordering [ADR 0004].
- Agents MUST verify migration success and rollback in containers and failed-release isolation on the target platform before claiming deployment acceptance [ADR 0004].

## Architecture documentation — [ADR 0002](docs/adr/0002-architecture-documentation.md)

- Agents MUST document architectural decisions in German ADRs under the applicable scope's `docs/adr/` directory [ADR 0002].
- Agents MUST use the next unused four-digit ADR number, `NNNN-topic.md` filenames, and `ADR NNNN` identifiers without renumbering existing ADRs [ADR 0002].
- Agents MUST create missing ADRs and rule files from the Development Instructor MCP templates and replace every placeholder [ADR 0002].
- ADRs MUST include status, date, scope, context, decision, considered alternatives, and consequences [ADR 0002].
- ADRs MUST explain system boundaries, reasons, and accepted trade-offs and end with a relative link to the corresponding `AGENT_RULES.md` [ADR 0002].
- ADRs MUST NOT contain SDK method names, exact line numbers, transient variable names, or implementation snapshots [ADR 0002].
- Agents MUST create or update the German ADR and its English rules in the same change [ADR 0002].
- Each rule MUST be brief, direct, imperative, contain `MUST`, `MUST NOT`, `DO`, or `DON'T`, and end with its originating ADR identifier in square brackets followed by a period [ADR 0002].
- Each rule section MUST link its originating ADR from its heading [ADR 0002].
- Rule files MUST NOT contain historical narrative, rationale, or superseded instructions [ADR 0002].
- Agents MUST place rules at the narrowest applicable scope and MUST NOT duplicate inherited rules in module rule files [ADR 0002].
- Agents MUST link applicable rule files from `AGENTS.md` and read inherited and active-scope rules before working [ADR 0002].
- Agents MUST update the affected ADR status, current rules, and relevant documentation together when changing a decision [ADR 0002].
- Agents MUST validate architecture documentation through `standards_validate_content` for `architecture-documentation`, submitting a complete JSON path-to-content mapping of applicable `AGENTS.md`, `AGENT_RULES.md`, and referenced ADRs, and fix all errors [ADR 0002].
- Agents MUST manually review language, rationale, scope, completeness, and inherited-rule duplication after document changes [ADR 0002].
