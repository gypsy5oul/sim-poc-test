"""The prepaid-plan agent: MCP tools, a confirmation gate, and a plan draft in session state."""

import json
import os
import re
from typing import Optional

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.tools import ToolContext
from google.adk.tools.mcp_tool import McpToolset, StreamableHTTPConnectionParams

from .rag import search_plan_knowledge

MCP_URL = os.environ.get("MCP_URL", "http://localhost:8200/mcp")

AFFIRMATIVE = re.compile(
    r"^(yes|y|yep|yeah|confirm(ed)?|go ahead|proceed|create it|sure|ok(ay)?|do it)\W*$",
    re.IGNORECASE,
)


def save_plan_draft(
    tool_context: ToolContext,
    plan_type: Optional[str] = None,
    validity_days: Optional[int] = None,
    data_type: Optional[str] = None,
    data_gb: Optional[float] = None,
    voice: Optional[str] = None,
    sms_per_day: Optional[int] = None,
    price: Optional[float] = None,
) -> dict:
    """Record or update fields of the plan the user is currently building.
    Call this as soon as you learn a new field's value, or when the user
    corrects a field they already gave -- new values always overwrite old
    ones. Only pass the fields you actually have; leave the rest out.
    """
    updates = {k: v for k, v in locals().items() if k != "tool_context" and v is not None}
    draft = tool_context.state.get("plan_draft", {})
    draft.update(updates)
    tool_context.state["plan_draft"] = draft
    tool_context.state["awaiting_plan_confirmation"] = None  # a correction invalidates approval
    return draft


def needs_approval(tool_context: ToolContext) -> bool:
    """Confirmation gate for create_prepaid_plan: allow only when the plan was
    validated in an earlier turn (a summary was shown) and this turn's reply
    is a plain affirmative.
    """
    content = tool_context.user_content
    if not content or not content.parts:
        return True
    text = "".join(part.text or "" for part in content.parts).strip()
    if not AFFIRMATIVE.match(text):
        return True
    flag = tool_context.state.get("awaiting_plan_confirmation")
    return not flag or flag == tool_context.invocation_id


def track_plan_state(tool, args, tool_context, tool_response):
    """Tracks confirmation state across the validate -> summary -> create flow."""
    if tool.name not in ("validate_prepaid_plan", "create_prepaid_plan") or tool_response.get("isError"):
        return
    # MCP responses arrive wrapped as {"content": [{"text": "<json>"}], ...}.
    result = json.loads(tool_response["content"][0]["text"])
    if tool.name == "validate_prepaid_plan" and result.get("valid"):
        tool_context.state["awaiting_plan_confirmation"] = tool_context.invocation_id
    elif tool.name == "create_prepaid_plan" and "plan_id" in result:
        tool_context.state["plan_draft"] = {}
        tool_context.state["awaiting_plan_confirmation"] = None


INSTRUCTION = """You are a prepaid mobile plan assistant. You help customers create
new prepaid plans, look up existing plans, and answer questions about plan
types and rules. You have no built-in knowledge of plan types, fields, or
rules -- always retrieve that from search_plan_knowledge first; never invent
rules, limits, or data.

Figure out the user's intent first:
- CREATE a plan: they want a new plan defined.
- QUERY existing plans: use search_prepaid_plans / get_prepaid_plan for
  operational questions ("what plans exist", "show me 28 day combos") --
  these tools have the live data, knowledge does not.
- RULE/KNOWLEDGE question ("what plan types are there", "what are the
  rules", "how much data can a data plan have"): call search_plan_knowledge
  and answer from what it returns, no other tool call needed.

When creating a plan:
1. Call search_plan_knowledge to learn which fields are required for the
   plan type (once type is known) before asking the user for anything.
2. Extract every field already given in the user's message and call
   save_plan_draft with all of them at once (corrections overwrite old
   values). A short reply that doesn't obviously state a field (e.g. a bare
   number or "unlimited") almost always answers the question you just
   asked -- map it to that field rather than guessing at a different one.
3. Ask for only the next missing required field, one natural question at a
   time. If the type is vague, propose the closest type and confirm it.
4. Once every required field is filled in, call validate_prepaid_plan, then
   show a summary: Type / Validity / Data / Voice / SMS / Price (in ₹),
   and ask "Shall I create this plan?"
5. Only call create_prepaid_plan after the user explicitly confirms (e.g.
   says "yes"). Never call it right after the summary. Once created, report
   the new plan_id.

Current plan draft in progress: {plan_draft?}
"""

read_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=MCP_URL),
    tool_filter=["search_prepaid_plans", "get_prepaid_plan", "validate_prepaid_plan"],
)

create_tools = McpToolset(
    connection_params=StreamableHTTPConnectionParams(url=MCP_URL),
    tool_filter=["create_prepaid_plan"],
    require_confirmation=needs_approval,
)

root_agent = Agent(
    name="prepaid_plan_agent",
    model=LiteLlm(
        model=f"openai/{os.environ['LLM_MODEL']}",
        api_base=os.environ["LLM_BASE_URL"],
        api_key=os.environ["LLM_API_KEY"],
        extra_body={"chat_template_kwargs": {"enable_thinking": False}},
    ),
    instruction=INSTRUCTION,
    tools=[search_plan_knowledge, save_plan_draft, read_tools, create_tools],
    after_tool_callback=track_plan_state,
)
