from typing import Tuple
from ..core.state_store import StateStore
from ..core.models import Signal
import os


class RiskManager:
    def __init__(self):
        self.max_positions = int(os.getenv("MAX_POSITIONS", 3))
        self.max_dd = float(os.getenv("MAX_DRAWDOWN_PCT", 0.10))
    def validate(self, sig: Signal, state: StateStore) -> Tuple[bool, str]:
        # Minimal examples: position count & placeholder drawdown gate
        # You can extend with hours guard, per-symbol limits, etc.
        # For now: always allow since we don't track portfolio fully.
        return True, "ok"