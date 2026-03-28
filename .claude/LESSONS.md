# Lessons & Conventions

> Patterns, gotchas, and evolving standards. Read this before writing code.

## Code Conventions
- **Logging:** Always use `logging` module, never `print()`. Use `logger = logging.getLogger(__name__)` at module level.
- **Config:** All strategy parameters must be configurable via config.yaml. No hardcoded thresholds.
- **Type hints:** Use on all function signatures. Use `str | None` syntax (Python 3.10+).
- **Docstrings:** Google-style with Args:/Returns: sections.
- **Strategies:** Must inherit `BaseStrategy` and implement `evaluate() -> Signal`.
- **Error handling:** Catch specific exceptions, not bare `except`. Always log the error.
- **Language:** Code and comments in English. Korean comments acceptable in docs/ only (owner preference).

## Testing Patterns
- Use `pytest-mock` for API mocking
- Shared fixtures in `tests/conftest.py` (sample DataFrames for bullish/flat/empty/single-bar)
- Test edge cases: empty data, missing columns, zero values, boundary thresholds
- Naming: `test_<behavior>` not `test_<method_name>`

## Architecture
- Three-tier: DataFetcher → SignalManager → TradeExecutor
- Dependency injection: pass config dicts, not global state
- src/config.py is the single config source — merges .env + config.yaml

## Gotchas
- Alpaca API returns empty bars outside market hours — DataFetcher returns empty DataFrame with correct columns
- **alpaca-py (not alpaca-trade-api)** is the active SDK. alpaca-trade-api is deprecated (ADR-006)
- alpaca-py `get_stock_bars()` returns MultiIndex DataFrame (symbol, timestamp) — must `droplevel("symbol")`
- alpaca-py TimeFrame objects don't support `==` comparison — use `str(tf)` for assertions
- alpaca-py needs `pytz` at runtime (not listed in its own deps — install if missing)
- `GitHub_Token` in sprint_automation.py should be `GITHUB_TOKEN` — fix when touching that file
- Legacy app/strategy.py uses `volume_multiplier=2.0` but app/app.py hardcodes `1.5` — src/ uses 2.0 (configurable)
- Division by zero: always check denominator before calculating price_change or volume_ratio

## Development Process
- Every AI session: read CLAUDE.md → SPRINT.md → SESSIONS.md before coding
- Every AI session end: update SPRINT.md, SESSIONS.md, BACKLOG.md; commit all
- Feature branches: `claude/<description>-<id>`
- Quality gates before merge: ruff passes, pytest passes, no print() in src/
