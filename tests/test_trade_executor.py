"""Tests for the TradeExecutor module."""

import csv
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from alpaca.common.exceptions import APIError

from src.strategies.base import Signal
from src.trade_executor import TradeExecutor


# ---------------------------------------------------------------------------
# Initialization tests
# ---------------------------------------------------------------------------


class TestTradeExecutorInit:

    def test_dry_run_mode_no_client(self, trade_executor_config):
        """Dry-run mode initializes without building a TradingClient."""
        executor = TradeExecutor(trade_executor_config)
        assert executor.mode == "dry-run"
        assert executor._client is None

    def test_invalid_mode_raises(self, trade_executor_config):
        """An unrecognized mode raises ValueError."""
        trade_executor_config["execution"]["mode"] = "turbo"
        with pytest.raises(ValueError, match="Invalid execution mode"):
            TradeExecutor(trade_executor_config)

    def test_default_qty_from_config(self, trade_executor_config):
        """default_qty is read from config."""
        trade_executor_config["execution"]["default_qty"] = 5
        executor = TradeExecutor(trade_executor_config)
        assert executor._default_qty == 5


# ---------------------------------------------------------------------------
# Dry-run execution tests
# ---------------------------------------------------------------------------


class TestTradeExecutorDryRun:

    def test_dry_run_returns_results(self, trade_executor_config, sample_buy_signal):
        """execute() returns a list of result dicts with all expected keys."""
        executor = TradeExecutor(trade_executor_config)
        results = executor.execute([sample_buy_signal])

        assert len(results) == 1
        result = results[0]
        assert result["ticker"] == "AAPL"
        assert result["action"] == "buy"
        assert result["qty"] == 1
        assert result["mode"] == "dry-run"
        assert "timestamp" in result

    def test_dry_run_filters_hold_signals(self, trade_executor_config, sample_signals):
        """Hold signals are filtered out — only buy/sell processed."""
        executor = TradeExecutor(trade_executor_config)
        results = executor.execute(sample_signals)

        # sample_signals has 1 buy + 1 sell + 1 hold → 2 actionable
        assert len(results) == 2
        actions = {r["action"] for r in results}
        assert actions == {"buy", "sell"}

    def test_dry_run_status(self, trade_executor_config, sample_buy_signal):
        """Dry-run results have status='dry-run'."""
        executor = TradeExecutor(trade_executor_config)
        results = executor.execute([sample_buy_signal])

        assert results[0]["status"] == "dry-run"
        assert results[0]["order_id"] is None

    def test_dry_run_empty_signals(self, trade_executor_config):
        """Empty signal list returns empty results."""
        executor = TradeExecutor(trade_executor_config)
        results = executor.execute([])
        assert results == []


# ---------------------------------------------------------------------------
# Paper/live mode tests (mocked TradingClient)
# ---------------------------------------------------------------------------


class TestTradeExecutorPaper:

    def _make_paper_executor(self, config, mock_client):
        """Build a paper-mode executor with injected mock client."""
        config["execution"]["mode"] = "paper"
        return TradeExecutor(config, client=mock_client)

    def test_paper_submits_order(self, trade_executor_config, sample_buy_signal):
        """Paper mode calls submit_order with a MarketOrderRequest."""
        mock_client = MagicMock()
        mock_order = MagicMock()
        mock_order.id = "order-123"
        mock_client.submit_order.return_value = mock_order

        executor = self._make_paper_executor(trade_executor_config, mock_client)
        results = executor.execute([sample_buy_signal])

        mock_client.submit_order.assert_called_once()
        assert results[0]["status"] == "submitted"

    def test_paper_api_error_returns_failed(self, trade_executor_config, sample_buy_signal):
        """APIError during order submission returns status='failed'."""
        mock_client = MagicMock()
        mock_client.submit_order.side_effect = APIError("Insufficient buying power")

        executor = self._make_paper_executor(trade_executor_config, mock_client)
        results = executor.execute([sample_buy_signal])

        assert len(results) == 1
        assert results[0]["status"] == "failed"
        assert "API error" in results[0]["reason"]

    def test_paper_captures_order_id(self, trade_executor_config, sample_buy_signal):
        """Successful order captures order.id in the result."""
        mock_client = MagicMock()
        mock_order = MagicMock()
        mock_order.id = "abc-def-789"
        mock_client.submit_order.return_value = mock_order

        executor = self._make_paper_executor(trade_executor_config, mock_client)
        results = executor.execute([sample_buy_signal])

        assert results[0]["order_id"] == "abc-def-789"


# ---------------------------------------------------------------------------
# Trade logging tests
# ---------------------------------------------------------------------------


class TestTradeExecutorLogging:

    def test_trade_logged_to_csv(self, trade_executor_config, sample_buy_signal):
        """With log_trades=true, a CSV row is written."""
        trade_executor_config["execution"]["log_trades"] = True
        executor = TradeExecutor(trade_executor_config)
        executor.execute([sample_buy_signal])

        log_path = Path(trade_executor_config["_root_dir"]) / "logs" / "trades.csv"
        assert log_path.exists()

        with open(log_path) as f:
            reader = csv.DictReader(f)
            rows = list(reader)

        assert len(rows) == 1
        assert rows[0]["ticker"] == "AAPL"
        assert rows[0]["action"] == "buy"
        assert rows[0]["status"] == "dry-run"

    def test_no_log_when_disabled(self, trade_executor_config, sample_buy_signal):
        """With log_trades=false, no CSV file is created."""
        trade_executor_config["execution"]["log_trades"] = False
        executor = TradeExecutor(trade_executor_config)
        executor.execute([sample_buy_signal])

        log_path = Path(trade_executor_config["_root_dir"]) / "logs" / "trades.csv"
        assert not log_path.exists()
