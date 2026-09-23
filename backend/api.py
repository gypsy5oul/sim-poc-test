"""FastAPI backend for prepaid plans. Talks only to db.py."""

import logging
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from . import db
from .db import Plan

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("plans")
app = FastAPI(title="Prepaid Plans API")


@app.get("/plans")
def list_plans(
    plan_type: Optional[str] = None,
    validity_days: Optional[int] = None,
    max_price: Optional[float] = None,
    min_data_gb: Optional[float] = None,
):
    plans = db.search(plan_type, validity_days, max_price, min_data_gb)
    log.info("search plan_type=%s validity_days=%s max_price=%s min_data_gb=%s -> %d plans %s",
             plan_type, validity_days, max_price, min_data_gb, len(plans), [p["plan_id"] for p in plans])
    return plans


@app.get("/plans/{plan_id}")
def get_plan(plan_id: str):
    plan = db.get(plan_id)
    log.info("get %s -> %s", plan_id, "found" if plan else "not found")
    if not plan:
        raise HTTPException(status_code=404, detail=f"Plan {plan_id} not found")
    return plan


@app.post("/plans/validate")
def validate_plan(plan: Plan):
    errors = db.validate(plan)
    log.info("validate %s -> %s", plan.model_dump(exclude_none=True), errors or "valid")
    return {"valid": not errors, "errors": errors}


@app.post("/plans", status_code=201)
def create_plan(plan: Plan):
    try:
        created = db.create(plan)
    except ValueError as e:
        log.warning("create rejected %s -> %s", plan.model_dump(exclude_none=True), e.args[0])
        return JSONResponse(status_code=422, content={"errors": e.args[0]})
    log.info("PLAN CREATED %s %s", created["plan_id"], created["plan_name"])
    return created


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8100)
