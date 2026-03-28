"""TradeExecutor — Order submission and trade logging.

Consumes Signal objects from SignalManager, filters for actionable signals
(buy/sell), and either logs them (dry-run) or submits orders via the
Alpaca TradingClient (paper/live modes).  All trades are optionally
recorded to a CSV log.
"""

import csv
import logging
from datetime import datetime, timezone
from pathlib import Path

from alpaca.common.exceptions import APIError
from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.trading.requests import MarketOrderRequest

from src.strategies.base import Signal

logger = logging.getLogger(__name__)

_VALID_MODES = {"dry-run", "paper", "live"}

_CSV_COLUMNS = [
    "timestamp", "ticker", "action", "qty", "mode", "status", "order_id", "reason",
]


class TradeExecutor:
    """Executes trades based on strategy signals.

    Supports three modes:
    - **dry-run**: Logs what *would* happen, no API calls.
    - **paper**: Submits orders to Alpaca paper trading.
    - **live**: Submits real orders (use with extreme caution).

    Args:
        config: Full config dict from load_config().
        client: Optional pre-built TradingClient (for testing).
    """

    def __init__(self, config: dict, client: TradingClient | None = None):
        exec_cfg = config.get("execution", {})
        alpaca_cfg = config.get("alpaca", {})

        self._mode = exec_cfg.get("mode", "dry-run")
        if self._mode not in _VALID_MODES:
            raise ValueError(
                f"Invalid execution mode '{self._mode}'. "
                f"Must be one of: {', '.join(sorted(_VALID_MODES))}"
            )

        self._default_qty = int(exec_cfg.get("default_qty", 1))
        self._log_trades = exec_cfg.get("log_trades", True)

        # Build or inject TradingClient
        if client is not None:
            self._client = client
        elif self._mode in ("paper", "live"):
            paper = self._mode == "paper"
            self._client = TradingClient(
                api_key=alpaca_cfg.get("key_id"),
                secret_key=alpaca_cfg.get("secret_key"),
                paper=paper,
            )
        else:
            self._client = None  # dry-run needs no client

        if self._mode == "live":
            logger.warning("LIVE TRADING MODE ENABLED — real orders will be submitted")

        # Ensure logs/ directory exists
        self._log_dir = Path(config.get("_root_dir", ".")) / "logs"
        if self._log_trades:
            self._log_dir.mkdir(parents=True, exist_ok=True)

        logger.info(
            "TradeExecutor initialized — mode=%s, default_qty=%d",
            self._mode, self._default_qty,
        )

    @property
    def mode(self) -> str:
        """Current execution mode."""
        return self._mode

    def execute(self, signals: list[Signal]) -> list[dict]:
        """Execute actionable signals (buy/sell), skipping holds.

        Args:
            signals: List of Signal objects from SignalManager.evaluate_all().

        Returns:
            List of result dicts, one per actionable signal.
        """
        actionable = [s for s in signals if s.action in ("buy", "sell")]
        logger.info(
            "Processing %d actionable signal(s) out of %d total",
            len(actionable), len(signals),
        )

        results = []
        for signal in actionable:
            result = self._execute_one(signal)
            results.append(result)

        return results

    def _execute_one(self, signal: Signal) -> dict:
        """Execute a single signal.

        Args:
            signal: A Signal with action "buy" or "sell".

        Returns:
            Result dict with keys: ticker, action, qty, mode, status,
            order_id, reason, timestamp.
        """
        now = datetime.now(timezone.utc).isoformat()
        result = {
            "ticker": signal.ticker,
            "action": signal.action,
            "qty": self._default_qty,
            "mode": self._mode,
            "status": "pending",
            "order_id": None,
            "reason": signal.reason,
            "timestamp": now,
        }

        if self._mode == "dry-run":
            result["status"] = "dry-run"
            logger.info(
                "[%s] DRY-RUN %s %d share(s) — %s",
                signal.ticker, signal.action.upper(), self._default_qty, signal.reason,
            )
        else:
            self._submit_order(signal, result)

        if self._log_trades:
            self._log_trade(result)

        return result

    def _submit_order(self, signal: Signal, result: dict) -> None:
        """Submit an order via the Alpaca TradingClient.

        Args:
            signal: The Signal driving this order.
            result: Mutable result dict — updated in place with status/order_id.
        """
        side = OrderSide.BUY if signal.action == "buy" else OrderSide.SELL
        order_data = MarketOrderRequest(
            symbol=signal.ticker,
            qty=self._default_qty,
            side=side,
            time_in_force=TimeInForce.GTC,
        )

        try:
            order = self._client.submit_order(order_data)
            result["status"] = "submitted"
            result["order_id"] = str(order.id)
            logger.info(
                "[%s] SUBMITTED %s %d share(s) — order_id=%s",
                signal.ticker, signal.action.upper(), self._default_qty, order.id,
            )
        except APIError as e:
            result["status"] = "failed"
            result["reason"] = f"API error: {e}"
            logger.error("[%s] Order failed: %s", signal.ticker, e)
        except Exception:
            result["status"] = "error"
            logger.exception("[%s] Unexpected error submitting order", signal.ticker)

    def _log_trade(self, result: dict) -> None:
        """Append a trade result to the CSV log.

        Args:
            result: Trade result dict with standard keys.
        """
        log_path = self._log_dir / "trades.csv"
        write_header = not log_path.exists()

        try:
            with open(log_path, "a", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=_CSV_COLUMNS)
                if write_header:
                    writer.writeheader()
                writer.writerow({col: result.get(col, "") for col in _CSV_COLUMNS})
        except OSError:
            logger.exception("Failed to write trade log to %s", log_path)
