# Backlog

> Ordered by priority within each section. Update every session.
> Move items to "Done" when completed. Add discovered items as they surface.

## Now (Current Sprint — Phase 0: Foundation)
- [x] Create pyproject.toml with all dependencies and tool config
- [x] Create .env.example and config.example.yaml
- [x] Create src/ module structure (config.py, strategies/base.py, momentum.py)
- [x] Create tests/ framework with conftest.py fixtures
- [x] Create .claude/ context system
- [x] Add deprecation notice to app/
- [x] Update CLAUDE.md with new structure and session protocol
- [x] Update .gitignore for new directories
- [x] Verify: pip install, ruff, pytest all work

## Next (Phase 1: Core Modules)
- [ ] Create src/data_fetcher.py — DataFetcher class with fetch(), retry, caching
- [ ] Write tests/test_data_fetcher.py — mock API, verify DataFrame shape, test retry
- [ ] Create src/signal_manager.py — loads strategies from config, evaluates tickers
- [ ] Write tests/test_signal_manager.py — multi-strategy loading, signal aggregation
- [ ] Create src/trade_executor.py — order submission + dry-run mode + trade logging
- [ ] Write tests/test_trade_executor.py — dry-run, mock orders, error scenarios
- [ ] Create src/main.py — orchestrates full pipeline with CLI args

## Later (Phase 2+)
- [ ] Create .github/workflows/daily.yml — scheduled + manual dispatch
- [ ] Integration test: end-to-end pipeline in dry-run mode
- [ ] Backtesting notebook (notebooks/backtest_momentum.ipynb)
- [ ] 5-day paper trading validation run
- [ ] Second strategy plugin (VWAP breakout or mean reversion)
- [ ] Telegram alert integration
- [ ] Portfolio tracking / position management
- [ ] Performance dashboard (CLI or FastAPI)
- [ ] Dockerize the application
- [ ] AWS EC2/Lambda deployment

## Done (Recent Completions)
- [x] Created CLAUDE.md for AI assistant guidance — 2026-03-22
- [x] Phase 0: Foundation scaffolding complete — 2026-03-22
