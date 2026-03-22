# CLAUDE.md — AI Assistant Guide for IanETrading

## Session Protocol

**EVERY AI session must start by reading these files in order:**
1. This file (`CLAUDE.md`) — project structure and conventions
2. `.claude/SPRINT.md` — current sprint state and in-progress items
3. `.claude/SESSIONS.md` — last session summary and "what's next"
4. `.claude/BACKLOG.md` — if starting new work, pick from "Now" section
5. `.claude/LESSONS.md` — before writing code, review patterns and gotchas

**EVERY AI session must end by updating:**
1. `.claude/SPRINT.md` — check off completed items, note blockers
2. `.claude/SESSIONS.md` — append session summary (what was done, what's next, decisions)
3. `.claude/BACKLOG.md` — move completed items to Done, add discovered items
4. `.claude/DECISIONS.md` — add any new architectural decisions (ADR format)
5. `.claude/LESSONS.md` — add any new patterns or gotchas discovered
6. `CLAUDE.md` — if project structure or conventions changed

---

## Project Overview

IanETrading is a **Smart Money Momentum automated trading bot** built in Python. It uses the Alpaca Markets API to detect institutional buying behavior (unusual volume spikes + price breakouts) and execute trades.

**Owner:** Hamin Hong (@IanEAbba)
**Current Phase:** Phase 1b — SignalManager (DataFetcher complete)

## Repository Structure

```
IanETrading/
├── src/                              # Active codebase (clean restart as of 2026-03-22)
│   ├── __init__.py
│   ├── config.py                    # Config loader — merges .env + config.yaml
│   ├── main.py                      # Entry point (TODO: Phase 2)
│   ├── data_fetcher.py              # DataFetcher class (TODO: Phase 1a)
│   ├── signal_manager.py            # SignalManager class (TODO: Phase 1b)
│   ├── trade_executor.py            # TradeExecutor class (TODO: Phase 1c)
│   └── strategies/                  # Strategy plugins
│       ├── __init__.py
│       ├── base.py                  # BaseStrategy ABC + Signal dataclass
│       └── momentum.py             # Smart Money Momentum strategy
├── tests/                           # Test suite (pytest)
│   ├── conftest.py                  # Shared fixtures (sample OHLCV DataFrames)
│   └── test_momentum_strategy.py   # 9 tests for momentum strategy
├── .claude/                         # AI session context (committed to git)
│   ├── BACKLOG.md                   # Prioritized work items
│   ├── DECISIONS.md                 # Architectural Decision Records
│   ├── SPRINT.md                    # Current sprint state
│   ├── SESSIONS.md                  # Session log (what was done, what's next)
│   └── LESSONS.md                   # Patterns, gotchas, conventions
├── app/                             # DEPRECATED — legacy prototype (see app/DEPRECATED.md)
├── docs/                            # Project documentation
│   ├── Requirements.md              # Functional & non-functional requirements
│   ├── projectPlan.md               # 8-10 week project timeline
│   ├── SystemRequest.md             # Business case, scope, feasibility
│   └── requirements.txt             # Legacy deps file (use pyproject.toml instead)
├── management/
│   └── sprint_automation.py         # GitHub Issues/project board automation
├── images/
│   └── Flowchart.png                # Architecture diagram
├── pyproject.toml                   # Package config, deps, linting, testing
├── config.example.yaml              # Strategy config template
├── .env.example                     # Environment variable template
├── .gitignore
├── index.html                       # Simple landing page
└── README.md
```

## Tech Stack

- **Python 3.10+** — primary language
- **alpaca-py >=0.30** — Official Alpaca Markets SDK (replaced deprecated alpaca-trade-api)
- **pandas >=2.0** — OHLCV data manipulation
- **pyyaml >=6.0** — config file parsing
- **tenacity >=8.0** — retry logic with exponential backoff
- **python-dotenv >=1.0** — environment variable management
- **pytest >=7.0** — test framework (dev dependency)
- **ruff >=0.3** — linting (dev dependency)

## Key Entry Points

| File | Key Classes/Functions | Purpose |
|------|----------------------|---------|
| `src/config.py` | `load_config()` | Loads .env + config.yaml into merged config dict |
| `src/strategies/base.py` | `BaseStrategy`, `Signal` | Strategy ABC and signal dataclass |
| `src/strategies/momentum.py` | `MomentumStrategy.evaluate()` | Detects volume spikes + price breakouts |
| `src/data_fetcher.py` | `DataFetcher.fetch()` | Alpaca API wrapper with retry + caching |
| `src/signal_manager.py` | `SignalManager.evaluate_all()` | Runs strategies against tickers (TODO) |
| `src/trade_executor.py` | `TradeExecutor.execute()` | Order submission + dry-run (TODO) |
| `src/main.py` | `main()` | Pipeline orchestrator (TODO) |

## Setup

```bash
# Install (production + dev tools)
pip install -e ".[dev]"

# Copy config templates
cp .env.example .env          # Fill in Alpaca API keys
cp config.example.yaml config.yaml  # Adjust strategy params

# Run tests
pytest

# Lint
ruff check src/

# Run bot (once main.py is built)
python -m src.main --dry-run
```

## Configuration

**Two-tier config system (ADR-004):**
- `.env` — secrets only (API keys). Gitignored. See `.env.example`.
- `config.yaml` — strategy params, tickers, execution mode. Committed. See `config.example.yaml`.
- `src/config.py` merges both into a single dict.

## Architecture

Three-tier modular design with strategy plugin pattern (ADR-003):

```
main.py (orchestrator)
  ├── config.py          (loads .env + config.yaml)
  ├── data_fetcher.py    (Alpaca API with retry/cache)
  ├── signal_manager.py  (loads + runs strategy plugins)
  │     └── strategies/  (BaseStrategy → MomentumStrategy, etc.)
  └── trade_executor.py  (dry-run / paper / live mode)
```

## Code Conventions

- **Logging:** `logging` module only, never `print()`. Use `logger = logging.getLogger(__name__)`.
- **Docstrings:** Google-style with `Args:` / `Returns:` sections.
- **Type hints:** On all function signatures. Use `str | None` syntax (3.10+).
- **Error handling:** Catch specific exceptions, not bare `except`. Always log errors.
- **Config:** All thresholds configurable via config.yaml. No hardcoded values.
- **Strategies:** Must inherit `BaseStrategy` and implement `evaluate() -> Signal`.
- **Language:** Code and comments in English. Korean acceptable in docs/ only.
- **Data format:** Pandas DataFrames with standard OHLCV columns.

## Quality Gates (before merging to main)

1. `ruff check src/` — zero warnings
2. `pytest` — all tests pass
3. No `print()` in src/
4. All new functions have docstrings
5. No hardcoded secrets
6. `.claude/` context files updated

## Testing

- Framework: pytest + pytest-mock
- Fixtures: `tests/conftest.py` has sample DataFrames (bullish, flat, empty, single-bar)
- Pattern: test edge cases — empty data, missing columns, zero values, boundary thresholds
- Naming: `test_<behavior>` not `test_<method_name>`

## Important Notes for AI Assistants

1. **Read .claude/ context files** at session start — they contain current state and decisions
2. **Paper trading only** — `paper-api.alpaca.markets` is default. Never default to live trading.
3. **Strategy params must be configurable** — via config.yaml, not hardcoded
4. **app/ is deprecated** — all new code goes in src/. See app/DEPRECATED.md.
5. **Dependencies in pyproject.toml** — not docs/requirements.txt (legacy)
6. **Update .claude/ files** at session end — this is how continuity is maintained
7. The development roadmap lives in `.claude/BACKLOG.md` — check "Now" section for priorities

## Development Roadmap (Summary)

| Phase | Focus | Status |
|-------|-------|--------|
| **Phase 0** | Foundation (pyproject.toml, src/, tests/, .claude/) | Complete |
| **Phase 1** | Core modules (DataFetcher, SignalManager, TradeExecutor) | Next |
| **Phase 2** | Integration pipeline + GitHub Actions CI/CD | Planned |
| **Phase 3** | Backtesting + paper trading validation | Planned |
| **Phase 4** | Advanced features (multi-strategy, alerts, monitoring) | Planned |
| **Phase 5** | Production readiness (Docker, AWS, observability) | Planned |

See `.claude/BACKLOG.md` for detailed task breakdown.
