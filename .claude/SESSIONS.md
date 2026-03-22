# Session Log

> Append new sessions at the top. Each entry captures what was done, decisions made, and what's next.

---

## Session 2026-03-22 (Part 2) — Phase 1a: DataFetcher
**Branch:** claude/add-claude-documentation-oJu6O
**Duration:** ~45 min

**What was done:**
- Researched alpaca-trade-api vs alpaca-py: confirmed alpaca-trade-api is deprecated (last release Jan 2024)
- Migrated dependency from alpaca-trade-api to alpaca-py (v0.43.2) in pyproject.toml
- Verified all alpaca-py imports: StockHistoricalDataClient, StockBarsRequest, TimeFrame, APIError
- Inspected alpaca-py source: Bar model fields, BarSet.df (MultiIndex), APIError properties
- Created src/data_fetcher.py:
  - DataFetcher class with dependency injection (accepts config dict + optional client)
  - fetch(ticker, timeframe, limit) → standardized OHLCV DataFrame
  - fetch_multiple(tickers) → {ticker: DataFrame} dict
  - parse_timeframe() maps config strings ("1Min","5Min","1Day") to TimeFrame objects
  - Tenacity retry on APIError/ConnectionError with configurable attempts + exponential backoff
  - Optional CSV caching to data/{TICKER}_{date}.csv (daily freshness)
  - MultiIndex flattening (Alpaca returns symbol+timestamp MultiIndex)
  - Returns empty DataFrame with correct columns on failure (never crashes)
- Added 4 new fixtures to conftest.py: mock_bars_response, mock_empty_bars_response, mock_alpaca_client, data_fetcher_config
- Created tests/test_data_fetcher.py with 12 tests across 4 classes:
  - TestParseTimeframe (3 tests): standard, custom, invalid
  - TestDataFetcherFetch (6 tests): correct columns, empty data, retry, max retry, config defaults, override args
  - TestDataFetcherMultiple (1 test): multi-ticker dict return
  - TestDataFetcherCache (2 tests): save/load cycle, disabled skips writes
- All 21 tests passing, ruff clean

**Decisions made:**
- ADR-006: Migrate from alpaca-trade-api to alpaca-py

**What's next:**
- Phase 1b: Build SignalManager (src/signal_manager.py)
- Phase 1c: Build TradeExecutor (src/trade_executor.py)
- Phase 2: Wire up src/main.py + GitHub Actions

**Open questions:**
- None

---

## Session 2026-03-22 — Project Restructuring & Foundation
**Branch:** claude/add-claude-documentation-oJu6O
**Duration:** ~1 hour

**What was done:**
- Comprehensive project analysis: read all code, docs, git history
- Identified critical bugs: app.py duplicates logic, division-by-zero in strategy.py, no tests/logging/CI
- Created full restructuring plan (Phase 0-5, ~17 weeks total)
- Executed Phase 0 — Foundation:
  - Created pyproject.toml with pinned deps + dev tools (pytest, ruff)
  - Created .env.example and config.example.yaml
  - Built src/ structure: config.py, strategies/base.py, strategies/momentum.py
  - Built tests/: conftest.py with fixtures, test_momentum_strategy.py (9 tests)
  - Created .claude/ context system (BACKLOG, DECISIONS, SPRINT, SESSIONS, LESSONS)
  - Archived legacy app/ with deprecation notice
  - Updated CLAUDE.md with new structure + AI session protocol
  - Updated .gitignore

**Decisions made:**
- ADR-001: Clean restart in src/ (not refactor app/)
- ADR-002: pyproject.toml as single project config
- ADR-003: Strategy plugin pattern with BaseStrategy ABC
- ADR-004: config.yaml for params, .env for secrets
- ADR-005: .claude/ context system for AI continuity

**What's next:**
- Phase 1a: Build DataFetcher class (src/data_fetcher.py)
- Phase 1b: Build SignalManager (src/signal_manager.py)
- Phase 1c: Build TradeExecutor (src/trade_executor.py)
- Phase 2: Wire up src/main.py + GitHub Actions

**Open questions:**
- None currently
