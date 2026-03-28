# Session Log

> Append new sessions at the top. Each entry captures what was done, decisions made, and what's next.

---

## Session 2026-03-28 — Documentation Sync
**Branch:** claude/add-claude-documentation-oJu6O
**Duration:** ~10 min

**What was done:**
- Synced .claude/ context files: SESSIONS.md was missing Phase 1c entry, BACKLOG.md still showed Phase 1c as current
- Added Phase 1c session log (Part 4)
- Updated BACKLOG.md: marked Phase 1c done, promoted Phase 2 to "Now"
- Verified all 43 tests pass and ruff is clean

**Decisions made:**
- None

**What's next:**
- Phase 2: Create src/main.py (CLI orchestrator) + GitHub Actions workflow

**Open questions:**
- None

---

## Session 2026-03-22 (Part 4) — Phase 1c: TradeExecutor
**Branch:** claude/add-claude-documentation-oJu6O
**Duration:** ~20 min

**What was done:**
- Created src/trade_executor.py (160 lines):
  - TradeExecutor class with dependency injection (config + optional TradingClient)
  - Three execution modes: dry-run (no API), paper (Alpaca paper), live (with loud warning)
  - execute(signals) filters for actionable buy/sell, returns list[dict] results
  - _submit_order() builds MarketOrderRequest, calls TradingClient.submit_order()
  - Error isolation per order: APIError -> status="failed", Exception -> status="error"
  - CSV trade logging via stdlib csv module to logs/trades.csv
  - Mode validation on init (ValueError for unrecognized modes)
- Added 3 fixtures to conftest.py: sample_buy_signal, sample_signals, trade_executor_config
- Created tests/test_trade_executor.py with 12 tests across 4 classes:
  - TestTradeExecutorInit (3): dry-run no client, invalid mode, default_qty from config
  - TestTradeExecutorDryRun (4): returns results, filters holds, status, empty signals
  - TestTradeExecutorPaper (3): submits order, API error handling, captures order_id
  - TestTradeExecutorLogging (2): CSV created, no CSV when disabled
- Fixed 2 ruff issues (unused import, line length)
- All 43 tests passing (9 momentum + 12 data_fetcher + 10 signal_manager + 12 trade_executor), ruff clean

**Decisions made:**
- Result format is list[dict] (simple, serializable, no new dataclass)
- CSV logging uses stdlib csv (no new dependency)
- GTC time-in-force for all market orders (matches legacy behavior)
- Live mode gets logger.warning on init but no additional safeguard (Phase 5 concern)

**What's next:**
- Phase 2: Create src/main.py (CLI orchestrator) + GitHub Actions workflow

**Open questions:**
- None

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
