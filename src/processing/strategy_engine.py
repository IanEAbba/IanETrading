from collections import deque
from typing import Dict, Deque, Optional
from datetime import datetime
from ..core.models import Bar, Signal
import os


class StrategyEngine:
    """Simple SMA crossover with confidence as normalized distance.
    Replace later with Smart Money divergence rules.
    """
    def __init__(self):
        self.fast_n = int(os.getenv("SMA_FAST", 5))
        self.slow_n = int(os.getenv("SMA_SLOW", 20))
        self.min_conf = float(os.getenv("MIN_CONFIDENCE", 0.6))
        self.buffers: Dict[str, Deque[float]] = {}
        self.slow_buffers: Dict[str, Deque[float]] = {}


    def _push(self, sym: str, price: float):
        if sym not in self.buffers:
            self.buffers[sym] = deque(maxlen=self.fast_n)
            self.slow_buffers[sym] = deque(maxlen=self.slow_n)
        self.buffers[sym].append(price)
        self.slow_buffers[sym].append(price)


    def on_bar(self, bar: Bar) -> Optional[Signal]:
        self._push(bar.symbol, bar.close)
        fb, sb = self.buffers[bar.symbol], self.slow_buffers[bar.symbol]
        if len(sb) < self.slow_n:
            return None
        fast = sum(fb)/len(fb)
        slow = sum(sb)/len(sb)
        diff = fast - slow
        denom = max(1e-6, slow)
        conf = min(1.0, abs(diff)/denom)
        if diff > 0 and conf >= self.min_conf:
            return Signal(symbol=bar.symbol, action="BUY", confidence=conf, reason=f"SMA{self.fast_n}>{self.slow_n}", ts=bar.ts)
        if diff < 0 and conf >= self.min_conf:
            return Signal(symbol=bar.symbol, action="SELL", confidence=conf, reason=f"SMA{self.fast_n}<{self.slow_n}", ts=bar.ts)
        return None