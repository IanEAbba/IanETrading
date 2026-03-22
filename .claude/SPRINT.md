# Current Sprint

**Sprint:** Phase 0 — Foundation
**Goal:** Set up project tooling, create src/ structure, establish test framework, build context system
**Started:** 2026-03-22
**Target End:** 2026-03-29

## Items
- [x] Create pyproject.toml with all deps and tool config
- [x] Create .env.example and config.example.yaml
- [x] Create src/ module structure (config.py, strategies/base.py, momentum.py)
- [x] Create tests/ framework with conftest.py fixtures and momentum strategy tests
- [x] Create .claude/ context directory with all 5 files
- [x] Add deprecation notice to app/
- [x] Update CLAUDE.md with new structure and session protocol
- [x] Update .gitignore for logs/, data/, .venv/
- [x] Verify: pip install -e ".[dev]", ruff check, pytest all pass

## Blockers
- None

## Notes
- Phase 0 completed in single session (2026-03-22)
- Ready to begin Phase 1 (Core Modules) next session
- Priority for Phase 1: DataFetcher first (enables SignalManager and TradeExecutor)

---

# Next Sprint

**Sprint:** Phase 1a — DataFetcher
**Goal:** Build DataFetcher class with Alpaca API integration, retry logic, and caching
**Estimated:** 1 session (~2-3 hours)

## Items
- [ ] Create src/data_fetcher.py — DataFetcher class
- [ ] Implement fetch(ticker, timeframe, limit) → DataFrame
- [ ] Add retry logic with tenacity (3 retries, exponential backoff)
- [ ] Add optional CSV caching to data/ directory
- [ ] Write tests/test_data_fetcher.py (4+ tests)
