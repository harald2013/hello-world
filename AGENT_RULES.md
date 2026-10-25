# Agent Rules

## Minimal HTTP service — [ADR 0001](docs/adr/0001-minimal-http-service.md)

- The HTTP service MUST use only the Python standard library at runtime [ADR 0001].
- The service MUST listen on `0.0.0.0:8000` by default [ADR 0001].
- The service MUST return status 200 and plain UTF-8 text for GET requests [ADR 0001].
- The service MUST return `ok` for the `/health` URL path and the configured greeting for every other GET path [ADR 0001].
- The container MUST run the same Python service as local execution [ADR 0001].

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
