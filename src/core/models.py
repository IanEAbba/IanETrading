from dataclasses import dataclass
from typing import Literal, Optional
from datetime import datetime


Action = Literal["BUY", "SELL", "HOLD"]


@dataclass
class Tick:
    symbol: str
    ts: datetime
    price: float
    size: int


@dataclass
class Bar:
    symbol: str
    ts: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    timeframe: str # e.g., "1m"


@dataclass
class Signal:
    symbol: str
    action: Action
    confidence: float
    reason: str
    ts: datetime


@dataclass
class OrderIntent:
    symbol: str
    side: Literal["buy","sell"]
    qty: float
    ts: datetime
    client_id: Optional[str] = None