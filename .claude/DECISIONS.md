# Architectural Decision Records

> Record significant design choices so future sessions understand WHY, not just WHAT.
> Format: ADR-NNN with Date, Status (Proposed/Accepted/Superseded), Context, Decision, Consequences.

---

## ADR-001: Clean restart in src/ over refactoring app/
**Date:** 2026-03-22
**Status:** Accepted

**Context:** The existing `app/` directory (315 lines) has critical architectural issues: app.py duplicates logic from alpaca_client.py and strategy.py instead of importing them, uses print() instead of logging, has hardcoded thresholds, and bare exception handling. The total codebase is small enough that rewriting is less risky than untangling the dependencies.

**Decision:** Archive `app/` as legacy reference code. Build fresh in `src/` with proper architecture from day one: dependency injection, logging, config management, testable design.

**Consequences:**
- Need to recreate all functionality in src/
- Old code available as reference in app/ (won't be deleted)
- Clean separation avoids inheriting technical debt
- Slightly more upfront work but much cleaner foundation

---

## ADR-002: pyproject.toml as single project config
**Date:** 2026-03-22
**Status:** Accepted

**Context:** Dependencies were in `docs/requirements.txt` (non-standard location, no version pinning). Need test and lint tooling config too.

**Decision:** Use `pyproject.toml` for all project config: dependencies (with version pins), pytest config, ruff config, build system. Remove reliance on docs/requirements.txt for fresh installs.

**Consequences:**
- Standard Python packaging (`pip install -e ".[dev]"`)
- Version pins prevent surprise breakage
- Single file for tool config (ruff, pytest)
- docs/requirements.txt kept for reference but not primary

---

## ADR-003: Strategy plugin pattern with BaseStrategy ABC
**Date:** 2026-03-22
**Status:** Accepted

**Context:** The project vision includes plug-in support for multiple strategies. Need an extensible pattern that doesn't require modifying core code to add strategies.

**Decision:** Abstract base class `BaseStrategy` in `src/strategies/base.py`. Each strategy is a separate module implementing `evaluate(ticker, df) -> Signal`. SignalManager loads strategies by name from config.yaml.

**Consequences:**
- Adding a new strategy = create a new file in src/strategies/
- Config.yaml controls which strategies are active
- Signal dataclass provides consistent output format
- Slight overhead of ABC pattern, but worth it for extensibility

---

## ADR-004: config.yaml for strategy params, .env for secrets
**Date:** 2026-03-22
**Status:** Accepted

**Context:** Strategy parameters (thresholds, tickers, timeframes) were hardcoded. Secrets (API keys) need to stay out of version control.

**Decision:** Two-tier config: `.env` for secrets (gitignored), `config.yaml` for strategy params (committed). `src/config.py` merges both into a single config dict.

**Consequences:**
- Strategy params are version-controlled and shareable
- Secrets never in git (enforced by .gitignore)
- config.example.yaml serves as documentation
- Single config.py module as source of truth

---

## ADR-005: Comprehensive .claude/ context system for AI continuity
**Date:** 2026-03-22
**Status:** Accepted

**Context:** AI-assisted development sessions are stateless — each new session starts without memory of previous work. Need persistent context so every session maintains strategic alignment and knows current state.

**Decision:** `.claude/` directory committed to git with 5 files: BACKLOG.md (work items), DECISIONS.md (this file), SPRINT.md (current sprint), SESSIONS.md (session log), LESSONS.md (patterns/gotchas). Protocol defined in CLAUDE.md for reading these at session start and updating at session end.

**Consequences:**
- Every AI session has full context in ~5 file reads
- Decisions are preserved and searchable
- Sprint state persists across sessions
- Small maintenance overhead per session (update 2-3 files)
- Git history shows project evolution through context files
