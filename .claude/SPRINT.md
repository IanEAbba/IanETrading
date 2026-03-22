# Current Sprint

**Sprint:** Phase 1b — SignalManager
**Goal:** Build SignalManager that loads strategy plugins from config and evaluates tickers
**Started:** 2026-03-22
**Target End:** 2026-03-29

## Items
- [x] Create src/signal_manager.py — SignalManager class
- [x] Strategy registry mapping config names → classes
- [x] Config-driven loading (enabled/disabled per strategy)
- [x] evaluate_all(data) → list of Signals with error isolation
- [x] Write tests/test_signal_manager.py (10 tests across 2 classes)

## Blockers
- None

## Notes
- Phase 1b completed same day as Phase 0 and 1a (2026-03-22)
- All 31 tests passing (9 momentum + 12 data_fetcher + 10 signal_manager), ruff clean
- Ready to begin Phase 1c (TradeExecutor) next session

---

# Next Sprint

**Sprint:** Phase 1c — TradeExecutor
**Goal:** Build TradeExecutor with dry-run/paper modes, trade logging, and error handling
**Estimated:** 1 session (~2-3 hours)

## Items
- [ ] Create src/trade_executor.py — TradeExecutor class
- [ ] Implement execute(signals) with dry-run and paper modes
- [ ] Add trade logging to logs/trades.csv
- [ ] Error handling for API/balance errors
- [ ] Write tests/test_trade_executor.py (5+ tests)
