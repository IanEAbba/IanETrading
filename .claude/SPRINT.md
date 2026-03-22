# Current Sprint

**Sprint:** Phase 1a — DataFetcher
**Goal:** Build DataFetcher class with Alpaca API integration, retry logic, and caching
**Started:** 2026-03-22
**Target End:** 2026-03-29

## Items
- [x] Migrate from deprecated alpaca-trade-api to alpaca-py (ADR-006)
- [x] Create src/data_fetcher.py — DataFetcher class
- [x] Implement fetch(ticker, timeframe, limit) → DataFrame
- [x] Add retry logic with tenacity (configurable attempts, exponential backoff)
- [x] Add optional CSV caching to data/ directory
- [x] Add parse_timeframe() for config string → TimeFrame conversion
- [x] Add fetch_multiple(tickers) → {ticker: DataFrame}
- [x] Write tests/test_data_fetcher.py (12 tests across 4 test classes)
- [x] Add shared test fixtures to conftest.py (mock_bars_response, mock_alpaca_client, etc.)

## Blockers
- None

## Notes
- Phase 1a completed in same session as Phase 0 (2026-03-22)
- alpaca-py 0.43.2 installed and working; alpaca-trade-api still in environment but unused
- All 21 tests passing (9 momentum + 12 data_fetcher), ruff clean
- Ready to begin Phase 1b (SignalManager) next session

---

# Next Sprint

**Sprint:** Phase 1b — SignalManager
**Goal:** Build SignalManager that loads strategy plugins from config and evaluates tickers
**Estimated:** 1 session (~2-3 hours)

## Items
- [ ] Create src/signal_manager.py — SignalManager class
- [ ] Implement evaluate_all(tickers, data) → list of Signals
- [ ] Strategy loading from config (which strategies are enabled)
- [ ] Write tests/test_signal_manager.py (5+ tests)
