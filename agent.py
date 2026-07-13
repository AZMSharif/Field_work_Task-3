"""
LogiTrack AI - Core Agent Architecture
Defines the agent factories, middleware stack, and structured output schemas.
"""
from dotenv import load_dotenv
load_dotenv()

import warnings, logging
warnings.filterwarnings("ignore")
logging.getLogger("google.genai").setLevel(logging.ERROR)

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ToolRetryMiddleware,
    ModelCallLimitMiddleware,
    PIIMiddleware,
    HumanInTheLoopMiddleware,
)
from langgraph.checkpoint.memory import InMemorySaver
from pydantic import BaseModel, Field
from typing import Literal

from tools import track_shipment, lookup_order, check_warehouse_stock, file_damage_claim, request_reshipment, shipping_policy
from guardrails import fraud_and_policy_guard

# ═══════════════════════════════════════════════════════════════
# Configuration
# ═══════════════════════════════════════════════════════════════
MODEL = "google_genai:gemini-3.1-flash-lite"

ALL_TOOLS = [
    track_shipment,
    lookup_order,
    check_warehouse_stock,
    file_damage_claim,
    request_reshipment,
    shipping_policy,
]

SYSTEM_PROMPT = (
    "You are LogiTrack, an intelligent logistics assistant for LogiTrack Fulfillment Services. "
    "You help operations staff and customers investigate shipment issues, track packages, "
    "check warehouse inventory, file damage claims, and process reshipments.\n\n"
    "RULES:\n"
    "1. Answer ONLY from tool results — NEVER invent order, tracking, stock, or claim details.\n"
    "2. If a tool returns an error or 'not found', say so plainly and suggest a next step.\n"
    "3. Always look up the order first (lookup_order) to understand the context.\n"
    "4. Before approving reshipment, ALWAYS check warehouse stock first (check_warehouse_stock).\n"
    "5. For damage claims, verify the order was actually delivered before filing.\n"
    "6. Be concise, professional, and action-oriented."
)


# ═══════════════════════════════════════════════════════════════
# Structured Output Schema
# ═══════════════════════════════════════════════════════════════
class ShipmentResolution(BaseModel):
    """Structured response schema for the logistics agent."""
    resolution_type: Literal[
        "tracking_update",
        "damage_claim_filed",
        "reshipment_approved",
        "stock_unavailable",
        "escalated",
        "info_provided",
    ] = Field(description="The type of resolution provided to the customer")
    answer: str = Field(description="The full reply to send the customer")
    action_taken: str = Field(description="Summary of tools used and actions performed")
    estimated_delivery: str = Field(description="New estimated delivery date if applicable, else 'N/A'")
    requires_escalation: bool = Field(description="True if this issue needs human manager review")


# ═══════════════════════════════════════════════════════════════
# Agent Factories
# ═══════════════════════════════════════════════════════════════

def create_basic_agent():
    """Agent configured with core tools for testing basic inference."""
    return create_agent(
        model=MODEL,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
    )


def create_memory_agent():
    """Agent configured with short-term memory (InMemorySaver) for multi-turn conversations."""
    return create_agent(
        model=MODEL,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),
    )


def create_structured_agent():
    """Agent configured to return a validated ShipmentResolution object."""
    return create_agent(
        model=MODEL,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        response_format=ShipmentResolution,
    )


def create_guarded_agent():
    """Agent with active guardrails for fraud detection and PII redaction."""
    return create_agent(
        model=MODEL,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        middleware=[
            PIIMiddleware("email", strategy="redact", apply_to_input=True),
            fraud_and_policy_guard,
        ],
    )


def create_full_agent():
    """
    Production-grade agent with full capabilities:
      - Short-term memory (InMemorySaver)
      - API Fault Tolerance (ToolRetryMiddleware)
      - Safety Limits (ModelCallLimitMiddleware)
      - PII Redaction (PIIMiddleware)
      - Anti-Fraud Guardrails (@before_model)
      - Human-in-the-Loop Reshipment Approval
    """
    return create_agent(
        model=MODEL,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=InMemorySaver(),
        middleware=[
            ToolRetryMiddleware(max_retries=2),
            ModelCallLimitMiddleware(run_limit=10, exit_behavior="end"),
            PIIMiddleware("email", strategy="redact", apply_to_input=True),
            fraud_and_policy_guard,
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "request_reshipment": {
                        "allowed_decisions": ["approve", "edit", "reject"],
                    },
                    # Read-only tools bypass HITL
                    "track_shipment": False,
                    "lookup_order": False,
                    "check_warehouse_stock": False,
                    "file_damage_claim": False,
                    "shipping_policy": False,
                },
                description_prefix="📦 Reshipment pending manager approval",
            ),
        ],
    )
