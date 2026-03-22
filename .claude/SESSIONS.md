# Session Log

> Append new sessions at the top. Each entry captures what was done, decisions made, and what's next.

---

## Session 2026-03-22 (Part 3) — Phase 1b: SignalManager
**Branch:** claude/add-claude-documentation-oJu6O
**Duration:** ~15 min

**What was done:**
- Created src/signal_manager.py:
  - Strategy registry: dict mapping config names → BaseStrategy subclasses
  - Config-driven loading: reads strategies section, skips disabled/unknown
  - evaluate_all(data) runs all enabled strategies against all tickers
  - Error isolation: catches strategy exceptions, returns hold signal instead
  - Logging throughout (info for loads, warning for skips, exception for errors)
- Created tests/test_signal_manager.py with 10 tests across 2 classes:
  - TestSignalManagerLoading (5): enabled, disabled, unknown, empty, names property
  - TestSignalManagerEvaluate (5): multi-ticker, buy, hold, empty data, exception handling
- All 31 tests passing, ruff clean

**Decisions made:**
- Strategy registry is a simple dict (no dynamic imports) — sufficient for current needs
- Return ALL signals including hold — TradeExecutor filters for actionable ones
- Error isolation per strategy — one broken strategy can't crash the pipeline

**What's next:**
- Phase 1c: Build TradeExecutor (src/trade_executor.py)
- Phase 2: Wire up src/main.py + GitHub Actions

**Open questions:**
- None

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
- Created tests/test_data_fetcher.py with 12 tests across 4 classes
- All 21 tests passing, ruff clean

**Decisions made:**
- ADR-006: Migrate from alpaca-trade-api to alpaca-py

**What's next:**
- Phase 1b: Build SignalManager (src/signal_manager.py)

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
- Executed Phase 0 — Foundation

**Decisions made:**
- ADR-001 through ADR-005 (see DECISIONS.md)

**What's next:**
- Phase 1a: Build DataFetcher class

**Open questions:**
- None currently
