# DEPRECATED — Legacy Prototype Code

> **This directory is archived.** All active development has moved to `src/`.

The files in `app/` are the original prototype from April 2025. They are kept as reference but are no longer maintained or imported by the project.

**Use instead:**
- `src/config.py` — replaces inline dotenv/REST setup in app.py
- `src/strategies/momentum.py` — replaces strategy.py (with bug fixes and proper logging)
- `src/data_fetcher.py` — replaces alpaca_client.py (with retry and caching)
- `src/trade_executor.py` — new module for order execution
- `src/main.py` — replaces app.py as the entry point

See [ADR-001](.claude/DECISIONS.md) for the rationale behind this decision.
