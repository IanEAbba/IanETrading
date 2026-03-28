"""Configuration loader for IanETrading.

Merges environment variables (.env) with strategy configuration (config.yaml).
Environment variables take precedence for secrets; config.yaml holds strategy params.
"""

import logging
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# Project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent

# Default config file location
DEFAULT_CONFIG_PATH = ROOT_DIR / "config.yaml"


def load_config(config_path: str | None = None) -> dict:
    """Load and merge configuration from .env and config.yaml.

    Args:
        config_path: Path to YAML config file. Defaults to project root config.yaml.

    Returns:
        dict with all configuration values.

    Raises:
        FileNotFoundError: If config.yaml doesn't exist and no path provided.
        ValueError: If required environment variables are missing.
    """
    # Load .env file (secrets)
    load_dotenv(ROOT_DIR / ".env")

    # Validate required env vars
    required_env = ["APCA_API_KEY_ID", "APCA_API_SECRET_KEY"]
    missing = [var for var in required_env if not os.getenv(var)]
    if missing:
        raise ValueError(
            f"Missing required environment variables: {', '.join(missing)}. "
            f"Copy .env.example to .env and fill in your Alpaca API keys."
        )

    # Load config.yaml (strategy params)
    yaml_path = Path(config_path) if config_path else DEFAULT_CONFIG_PATH
    if yaml_path.exists():
        with open(yaml_path) as f:
            yaml_config = yaml.safe_load(f) or {}
        logger.info("Loaded config from %s", yaml_path)
    else:
        logger.warning("No config.yaml found at %s, using defaults", yaml_path)
        yaml_config = {}

    # Build merged config
    config = {
        "alpaca": {
            "key_id": os.getenv("APCA_API_KEY_ID"),
            "secret_key": os.getenv("APCA_API_SECRET_KEY"),
            "base_url": os.getenv("APCA_API_BASE_URL", "https://paper-api.alpaca.markets"),
        },
        "tickers": yaml_config.get("tickers", ["AAPL", "MSFT", "NVDA", "TSLA", "AMZN"]),
        "data": yaml_config.get("data", {
            "timeframe": "1Min",
            "bar_limit": 30,
            "cache_enabled": False,
            "retry_attempts": 3,
        }),
        "strategies": yaml_config.get("strategies", {
            "momentum": {
                "enabled": True,
                "price_threshold": 1.0,
                "volume_multiplier": 2.0,
            }
        }),
        "execution": yaml_config.get("execution", {
            "mode": "dry-run",
            "default_qty": 1,
            "log_trades": True,
        }),
    }

    return config
