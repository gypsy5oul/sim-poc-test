"""SQLite storage for prepaid plans, plus the one place business rules live."""

import os
import sqlite3
from typing import Literal, Optional

from pydantic import BaseModel

DB_PATH = os.environ.get("DB_PATH", "plans.db")

PlanType = Literal["DATA", "VOICE", "COMBO", "UNLIMITED"]
DataType = Literal["PER_DAY", "TOTAL"]

REQUIRED = {
    "DATA": ["data_type", "data_gb"],
    "VOICE": ["voice"],
    "COMBO": ["data_type", "data_gb", "voice"],
    "UNLIMITED": ["data_gb"],
}
FORBIDDEN = {
    "DATA": ["voice"],
    "VOICE": ["data_type", "data_gb"],
}
RANGES = {
    "validity_days": (1, 365),
    "price": (10, 5000),
    "sms_per_day": (0, 100),
}
DATA_GB_RANGE = {"PER_DAY": (0.5, 5), "TOTAL": (1, 300)}
VOICE_MINUTES_RANGE = (1, 10000)


class Plan(BaseModel):
    """A prepaid plan. Used as both the API request body and MCP tool params.

    voice: "UNLIMITED", a number of minutes as a string (e.g. "300"), or None.
    data_type: PER_DAY (data_gb applies each day) or TOTAL (data_gb for the
      whole validity period). Required whenever data_gb is set.
    UNLIMITED plans always have unlimited voice and per-day data (the FUP,
    in data_gb); data_type is forced to PER_DAY for them.
    """

    plan_type: PlanType
    validity_days: int
    price: float
    data_type: Optional[DataType] = None
    data_gb: Optional[float] = None
    voice: Optional[str] = None
    sms_per_day: Optional[int] = None
    plan_name: Optional[str] = None


conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.row_factory = sqlite3.Row
conn.execute(
    """
    CREATE TABLE IF NOT EXISTS plans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        plan_id TEXT UNIQUE NOT NULL, plan_name TEXT NOT NULL,
        plan_type TEXT NOT NULL, validity_days INTEGER NOT NULL,
        data_type TEXT, data_gb REAL,
        voice TEXT CHECK (voice IS NULL OR voice = 'UNLIMITED' OR voice GLOB '[0-9]*'),
        sms_per_day INTEGER, price REAL NOT NULL,
        status TEXT NOT NULL DEFAULT 'ACTIVE',
        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    )
    """
)
conn.commit()


def validate(plan: Plan) -> list[str]:
    errors = []
    for field in REQUIRED.get(plan.plan_type, []):
        if getattr(plan, field) in (None, ""):
            errors.append(f"{field} is required for plan_type {plan.plan_type}")
    for field in FORBIDDEN.get(plan.plan_type, []):
        if getattr(plan, field) is not None:
            errors.append(f"{field} must not be set for plan_type {plan.plan_type}")
    for field, (lo, hi) in RANGES.items():
        value = getattr(plan, field)
        if value is not None and not (lo <= value <= hi):
            errors.append(f"{field} must be between {lo} and {hi}")
    if plan.data_gb is not None:
        if plan.plan_type != "UNLIMITED" and plan.data_type is None:
            errors.append("data_type is required when data_gb is given")
        data_type = "PER_DAY" if plan.plan_type == "UNLIMITED" else plan.data_type
        lo, hi = DATA_GB_RANGE.get(data_type, (0, float("inf")))
        if not (lo <= plan.data_gb <= hi):
            errors.append(f"data_gb must be between {lo} and {hi} for {data_type}")
    if plan.voice is not None and plan.voice != "UNLIMITED":
        lo, hi = VOICE_MINUTES_RANGE
        if not plan.voice.isdigit() or not (lo <= int(plan.voice) <= hi):
            errors.append(f"voice must be 'UNLIMITED' or minutes between {lo} and {hi}")
    return errors


def _plan_name(plan: Plan) -> str:
    if plan.plan_name:
        return plan.plan_name
    parts = [plan.plan_type.title(), f"{plan.validity_days}D"]
    if plan.data_gb is not None:
        unit = "GB/day" if plan.data_type == "PER_DAY" else "GB"
        parts.append(f"{plan.data_gb:g}{unit}")
    return " ".join(parts) + f" ₹{plan.price:g}"


def _insert(plan: Plan) -> str:
    next_id = (conn.execute("SELECT MAX(id) AS m FROM plans").fetchone()["m"] or 0) + 1
    plan_id = f"PP-{next_id:04d}"
    data = {**plan.model_dump(), "plan_id": plan_id, "plan_name": _plan_name(plan)}
    cols = ", ".join(data)
    placeholders = ", ".join(f":{k}" for k in data)
    conn.execute(f"INSERT INTO plans ({cols}) VALUES ({placeholders})", data)
    conn.commit()
    return plan_id


def create(plan: Plan) -> dict:
    errors = validate(plan)
    if errors:
        raise ValueError(errors)
    if plan.plan_type == "UNLIMITED":
        plan = plan.model_copy(update={"voice": "UNLIMITED", "data_type": "PER_DAY"})
    return get(_insert(plan))


def get(plan_id: str) -> Optional[dict]:
    row = conn.execute("SELECT * FROM plans WHERE plan_id = ?", (plan_id,)).fetchone()
    return dict(row) if row else None


def search(
    plan_type: Optional[str] = None,
    validity_days: Optional[int] = None,
    max_price: Optional[float] = None,
    min_data_gb: Optional[float] = None,
) -> list[dict]:
    filters = {
        "plan_type = ?": plan_type,
        "validity_days = ?": validity_days,
        "price <= ?": max_price,
        "data_gb >= ?": min_data_gb,
    }
    clauses = ["status = 'ACTIVE'"] + [c for c, v in filters.items() if v is not None]
    params = [v for v in filters.values() if v is not None]
    rows = conn.execute(
        f"SELECT * FROM plans WHERE {' AND '.join(clauses)} ORDER BY id", params
    ).fetchall()
    return [dict(row) for row in rows]


SEEDS = [
    dict(plan_type="DATA", validity_days=28, data_type="PER_DAY", data_gb=1.5, price=179),
    dict(plan_type="VOICE", validity_days=28, voice="300", sms_per_day=100, price=99),
    dict(plan_type="COMBO", validity_days=28, data_type="PER_DAY", data_gb=1.5, voice="UNLIMITED", sms_per_day=100, price=249),
    dict(plan_type="UNLIMITED", validity_days=28, data_gb=2.0, sms_per_day=100, price=299),
    dict(plan_type="COMBO", validity_days=56, data_type="PER_DAY", data_gb=1.5, voice="UNLIMITED", sms_per_day=100, price=479),
    dict(plan_type="COMBO", validity_days=84, data_type="PER_DAY", data_gb=2.0, voice="UNLIMITED", sms_per_day=100, price=719),
]


def _seed() -> None:
    if conn.execute("SELECT COUNT(*) AS n FROM plans").fetchone()["n"] > 0:
        return
    for s in SEEDS:
        create(Plan(**s))


_seed()
