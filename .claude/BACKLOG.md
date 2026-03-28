# Backlog

> Ordered by priority within each section. Update every session.
> Move items to "Done" when completed. Add discovered items as they surface.

## Now (Current Sprint — Phase 2: Integration Pipeline + CI/CD)
- [ ] Create src/main.py — orchestrates full pipeline with CLI args
- [ ] Create .github/workflows/daily.yml — scheduled + manual dispatch
- [ ] Integration test: end-to-end pipeline in dry-run mode

## Later (Phase 3+)
- [ ] Backtesting notebook (notebooks/backtest_momentum.ipynb)
- [ ] 5-day paper trading validation run
- [ ] Second strategy plugin (VWAP breakout or mean reversion)
- [ ] Telegram alert integration
- [ ] Portfolio tracking / position management
- [ ] Performance dashboard (CLI or FastAPI)
- [ ] Dockerize the application
- [ ] AWS EC2/Lambda deployment

## Done (Recent Completions)
- [x] Phase 1c: TradeExecutor with dry-run/paper/live modes, CSV logging, 12 tests — 2026-03-22
- [x] Phase 1b: SignalManager with strategy registry, config loading, 10 tests — 2026-03-22
- [x] Phase 1a: DataFetcher with alpaca-py, retry, caching, 12 tests — 2026-03-22
- [x] ADR-006: Migrated from deprecated alpaca-trade-api to alpaca-py — 2026-03-22
- [x] Phase 0: Foundation scaffolding complete — 2026-03-22
- [x] Created CLAUDE.md for AI assistant guidance — 2026-03-22
