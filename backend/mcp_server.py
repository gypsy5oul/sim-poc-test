"""MCP server exposing prepaid-plan operations to the agent. Calls api.py over HTTP."""

import os
from typing import Optional

import httpx
from mcp.server.fastmcp import FastMCP

API_URL = os.environ.get("API_URL", "http://localhost:8100")
mcp = FastMCP("prepaid-plans", host="0.0.0.0", port=int(os.environ.get("MCP_PORT", 8200)))


def _api(method: str, path: str, **kwargs):
    """Calls the backend API and unwraps its response; 404/422 come back as plain dicts."""
    resp = httpx.request(method, f"{API_URL}{path}", **kwargs)
    if resp.status_code == 404:
        return {"error": resp.json().get("detail", "not found")}
    if resp.status_code == 422:
        return resp.json()
    resp.raise_for_status()
    return resp.json()


@mcp.tool()
def search_prepaid_plans(
    plan_type: Optional[str] = None,
    validity_days: Optional[int] = None,
    max_price: Optional[float] = None,
    min_data_gb: Optional[float] = None,
) -> list[dict]:
    """Search existing plans, e.g. "show me 28 day combo plans" or "cheapest
    data plan". Never use this for plan-type or rules questions -- that's
    general knowledge, not a search.

    Args:
        plan_type: DATA, VOICE, COMBO, or UNLIMITED.
        validity_days: Exact validity in days.
        max_price: Max price, in rupees.
        min_data_gb: Minimum data in GB (per day or total, per data_type).
    """
    params = {k: v for k, v in locals().items() if v is not None}
    return _api("GET", "/plans", params=params)


@mcp.tool()
def get_prepaid_plan(plan_id: str) -> dict:
    """Look up one prepaid plan by its id, e.g. "PP-0003".

    Args:
        plan_id: The plan id, formatted like "PP-0001".
    """
    return _api("GET", f"/plans/{plan_id}")


@mcp.tool()
def validate_prepaid_plan(
    plan_type: str,
    validity_days: int,
    price: float,
    data_type: Optional[str] = None,
    data_gb: Optional[float] = None,
    voice: Optional[str] = None,
    sms_per_day: Optional[int] = None,
) -> dict:
    """Checks a draft plan against the business rules. Call once all fields
    for the plan type are known, before showing the summary to the user.

    Args:
        plan_type: DATA, VOICE, COMBO, or UNLIMITED.
        validity_days: 1-365.
        price: Rupees, must be greater than 0.
        data_type: PER_DAY (daily allowance) or TOTAL (whole period).
            Required whenever data_gb is set. UNLIMITED is always PER_DAY.
        data_gb: Data allowance in GB. Required for DATA, COMBO, UNLIMITED.
        voice: "UNLIMITED", minutes as a string, or omitted. Required for
            VOICE and COMBO.
        sms_per_day: Optional, any plan type.

    Returns:
        {"valid": bool, "errors": [str, ...]}
    """
    body = {k: v for k, v in locals().items() if v is not None}
    return _api("POST", "/plans/validate", json=body)


@mcp.tool()
def create_prepaid_plan(
    plan_type: str,
    validity_days: int,
    price: float,
    data_type: Optional[str] = None,
    data_gb: Optional[float] = None,
    voice: Optional[str] = None,
    sms_per_day: Optional[int] = None,
) -> dict:
    """Creates a new prepaid plan. IMPORTANT: only call this after the user
    has seen the summary and explicitly confirmed (e.g. "yes") -- never
    right after collecting fields or after validating.

    Args:
        Same fields as validate_prepaid_plan.

    Returns:
        The created plan with its new plan_id (e.g. "PP-0007"), or
        {"errors": [str, ...]} if validation failed.
    """
    body = {k: v for k, v in locals().items() if v is not None}
    return _api("POST", "/plans", json=body)


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
