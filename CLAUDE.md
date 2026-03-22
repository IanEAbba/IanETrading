# CLAUDE.md — AI Assistant Guide for IanETrading

## Project Overview

IanETrading is a **Smart Money Momentum automated trading bot** built in Python. It uses the Alpaca Markets API to detect institutional buying behavior (unusual volume spikes + price breakouts) and execute trades. The project is in early-stage development (Sprint 1).

**Owner:** Hamin Hong (@IanEAbba)

## Repository Structure

```
IanETrading/
├── app/                          # Core application code
│   ├── app.py                   # Main entry point — momentum check loop
│   ├── alpaca_client.py         # Alpaca REST API wrapper (get_bars, submit_order, etc.)
│   └── strategy.py              # Momentum detection logic (check_momentum)
├── docs/                        # Project documentation
│   ├── requirements.txt         # Python dependencies
│   ├── Requirements.md          # Functional & non-functional requirements
│   ├── projectPlan.md           # 8-10 week project timeline
│   └── SystemRequest.md         # Business case, scope, feasibility
├── management/                  # DevOps/automation scripts
│   └── sprint_automation.py     # GitHub Issues/project board automation
├── images/                      # Assets (flowchart diagram)
├── index.html                   # Simple landing page
└── README.md                    # High-level project overview
```

## Tech Stack

- **Python 3.10+** — primary language
- **alpaca-trade-api** — Alpaca Markets REST API client (paper + live trading)
- **pandas** — OHLCV data manipulation via DataFrames
- **python-dotenv** — environment variable management
- **requests** — HTTP (used in sprint automation)
- **schedule** — task scheduling (planned)

## Key Entry Points & Functions

| File | Key Functions | Purpose |
|------|--------------|---------|
| `app/app.py` | `check_momentum(ticker)` | Main loop: iterates tickers, checks signals |
| `app/alpaca_client.py` | `get_account()`, `get_bars()`, `submit_order()` | Alpaca API wrapper |
| `app/strategy.py` | `check_momentum(df, price_thresh, volume_multiplier)` | Returns `True` if momentum detected |
| `management/sprint_automation.py` | `create_issue()`, `add_to_project()` | GitHub project board automation |

Default tickers: `AAPL, MSFT, NVDA, TSLA, AMZN`

## Environment Variables

Required in a `.env` file at project root:

```
APCA_API_KEY_ID=your_key
APCA_API_SECRET_KEY=your_secret
APCA_API_BASE_URL=https://paper-api.alpaca.markets
```

For sprint automation:
```
GITHUB_TOKEN=your_github_token
```

**Never commit `.env` files.** They are in `.gitignore`.

## Running the Project

```bash
# Install dependencies
pip install -r docs/requirements.txt

# Run the momentum checker
python app/app.py
```

No formal build system — direct Python execution.

## Architecture

The codebase follows a three-tier modular design:

1. **Data Layer** — `alpaca_client.py` wraps Alpaca REST API calls
2. **Strategy Layer** — `strategy.py` contains stateless signal detection logic
3. **Execution Layer** — planned (TradeExecutor module in Sprint 1)

### Planned Refactoring (Sprint 1)

The codebase is being restructured into:
- `DataFetcher` — class-based data fetching with retry/caching
- `SignalManager` — extracted from strategy.py, config-driven
- `TradeExecutor` — order submission with dry-run mode
- Entry point will move to `src/main.py`
- GitHub Actions workflow at `.github/workflows/daily.yml`

## Code Conventions

- **Docstrings:** Google-style with `Args:` / `Returns:` sections
- **Comments:** Mixed English/Korean (owner preference)
- **Functions:** Prefer stateless utility functions; classes being introduced in Sprint 1
- **Error handling:** Try/except around API calls with logging
- **Type hints:** Minimal — used in function signatures (e.g., `ticker: str`)
- **Data format:** Pandas DataFrames for all OHLCV data
- **Config:** Environment variables via dotenv, strategy thresholds as function params

## Testing

No test framework is configured yet. Planned approach:
- Mock Alpaca API for unit tests
- Backtesting with sample data
- Walk-forward and out-of-sample validation via Google Colab

## CI/CD

Not yet implemented. Planned:
- **GitHub Actions** with daily cron (`0 14 * * 1-5` UTC, market hours)
- Secrets: `ALPACA_KEY`, `ALPACA_SECRET` in GitHub Secrets
- Entry: `python src/main.py`

## Git Conventions

- **Primary branch:** `main`
- **Commit style:** Short descriptive messages; issue-closing commits use `closes #N`
- No linting or pre-commit hooks configured

## Important Notes for AI Assistants

1. This is an **early-stage project** — keep changes simple and incremental
2. Dependencies are in `docs/requirements.txt` (not project root)
3. The `.env` file is required but never committed — always remind about setup
4. Paper trading URL (`paper-api.alpaca.markets`) is the default — never default to live trading
5. Strategy parameters (`price_thresh`, `volume_multiplier`) should remain configurable, not hardcoded
6. When adding new modules, follow the planned `DataFetcher` / `SignalManager` / `TradeExecutor` pattern from Sprint 1 planning
