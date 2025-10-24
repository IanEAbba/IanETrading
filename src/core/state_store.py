import sqlite3
from pathlib import Path
from datetime import datetime
from typing import Optional


class StateStore:
    def __init__(self, path: str = "state.db"):
        self.path = Path(path)
        self.conn = sqlite3.connect(self.path)
        self._init()
    def _init(self):
        cur = self.conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS health (
            key TEXT PRIMARY KEY,
            value TEXT,
            updated_at TEXT
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            action TEXT,
            confidence REAL,
            reason TEXT,
            ts TEXT
        )
        """)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT,
            side TEXT,
            qty REAL,
            client_id TEXT,
            ts TEXT,
            status TEXT
        )
        """)
        self.conn.commit()
    def set_health(self, key: str, value: str):
        cur = self.conn.cursor()
        cur.execute("REPLACE INTO health(key,value,updated_at) VALUES(?,?,?)",
            (key, value, datetime.utcnow().isoformat()))
        self.conn.commit()
    def add_signal(self, symbol: str, action: str, confidence: float, reason: str, ts: datetime):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO signals(symbol,action,confidence,reason,ts) VALUES(?,?,?,?,?)",
            (symbol, action, confidence, reason, ts.isoformat()))
        self.conn.commit()
    def add_order(self, symbol: str, side: str, qty: float, client_id: str, ts: datetime, status: str):
        cur = self.conn.cursor()
        cur.execute("INSERT INTO orders(symbol,side,qty,client_id,ts,status) VALUES(?,?,?,?,?,?)",
            (symbol, side, qty, client_id, ts.isoformat(), status))
        self.conn.commit()