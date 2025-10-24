from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional
from ..core.models import Tick, Bar


class BarAggregator:
    def __init__(self, timeframe: str = "1m"):
        assert timeframe == "1m", "This minimal scaffold implements 1m only"
        self.timeframe = timeframe
        self.current: Dict[str, Optional[Bar]] = defaultdict(lambda: None)


    def _minute_bucket(self, ts: datetime) -> datetime:
        return ts.replace(second=0, microsecond=0)


    def on_event(self, ev) -> List[Bar]:
        out: List[Bar] = []
        if not isinstance(ev, Tick):
            return out
        bkt = self._minute_bucket(ev.ts)
        bar = self.current.get(ev.symbol)
        if bar is None or self._minute_bucket(bar.ts) != bkt:
            if bar is not None:
                out.append(bar)
            bar = Bar(symbol=ev.symbol, ts=bkt, open=ev.price, high=ev.price, low=ev.price, close=ev.price, volume=ev.size, timeframe="1m")
            self.current[ev.symbol] = bar
        else:
            bar.high = max(bar.high, ev.price)
            bar.low = min(bar.low, ev.price)
            bar.close = ev.price
            bar.volume += ev.size
        return out


    def flush(self) -> List[Bar]:
        # Optionally emit all open bars (e.g., on shutdown)
        bars = [b for b in self.current.values() if b is not None]
        self.current.clear()
        return bars