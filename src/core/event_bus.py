import asyncio
from typing import Any


class EventBus:
    def __init__(self, maxsize: int = 10000):
        self.q: asyncio.Queue[Any] = asyncio.Queue(maxsize=maxsize)
    async def publish(self, item: Any):
        await self.q.put(item)
    async def consume(self) -> Any:
     return await self.q.get()
    def size(self) -> int:
     return self.q.qsize()