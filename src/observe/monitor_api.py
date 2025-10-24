import os
from fastapi import FastAPI
from ..core.state_store import StateStore


app = FastAPI()
state = StateStore("state.db")


@app.get("/health")
async def health():
    return {"status": "ok"}


# You can extend with /signals, /orders, etc.


def run_monitor_api():
    import uvicorn
    port = int(os.getenv("MONITOR_PORT", 8000))
    uvicorn.run(app, host="127.0.0.1", port=port)