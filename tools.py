"""
LogiTrack AI - Core Tool Definitions
These tools allow the agent to read and mutate the logistics databases.
"""
import json
import random
from langchain.tools import tool
from logistics_data import ORDERS, SHIPMENTS, WAREHOUSE, CLAIMS, reshipment_log


@tool
def shipping_policy() -> str:
    """Return LogiTrack's shipping and reshipment policy.
    Use when a customer asks about policies, timelines, or eligibility for reshipment/claims.
    This is a hard-coded company policy — no lookup needed."""
    return (
        "LogiTrack Shipping & Reshipment Policy:\n"
        "1. Damage claims must be filed within 7 days of delivery.\n"
        "2. Reshipments are available for items confirmed lost or damaged in transit.\n"
        "3. Reshipments over $100 require manager approval.\n"
        "4. Out-of-stock items will be backordered or refunded at customer's choice.\n"
        "5. All reshipments include free expedited shipping (2-3 business days).\n"
        "6. Customers with 3+ claims per quarter are subject to fraud review."
    )

# Active state tracking for network fault tolerance
_track_attempts = {"n": 0}
ENABLE_API_RETRY_TEST = True  # Used to validate ToolRetryMiddleware


@tool
def track_shipment(order_id: str) -> str:
    """Track a shipment by order ID. Returns carrier, status, location, and recent tracking events.
    Always use this if a customer asks 'where is my order?'
    NOTE: May raise ConnectionError if the carrier API is down.
    """
    if ENABLE_API_RETRY_TEST:
        _track_attempts["n"] += 1
        if _track_attempts["n"] == 1:
            raise ConnectionError("Carrier API timeout: No response from logistics partner. Please try again.")

    if order_id not in SHIPMENTS:
        return f"Error: No tracking data found for {order_id}."
    
    return json.dumps(SHIPMENTS[order_id])


@tool
def lookup_order(order_id: str) -> str:
    """Look up an order's details including items, quantities, prices, and shipping address."""
    if order_id not in ORDERS:
        return f"Error: Order {order_id} not found."
    
    return json.dumps(ORDERS[order_id])


@tool
def check_warehouse_stock(sku: str) -> str:
    """Check current warehouse inventory levels for a specific SKU.
    Required before approving any reshipment."""
    if sku not in WAREHOUSE:
        return f"Error: SKU {sku} does not exist in our catalog."
    
    data = WAREHOUSE[sku]
    return f"SKU: {sku} | Item: {data['name']} | Stock Available: {data['stock']} units | Location: {data['location']}"


@tool
def file_damage_claim(order_id: str, item_sku: str, damage_description: str) -> str:
    """File a formal damage claim for an item in a specific order.
    Returns the new Claim ID."""
    if order_id not in ORDERS:
        return f"Error: Order {order_id} not found. Cannot file claim."
    
    has_item = any(item["sku"] == item_sku for item in ORDERS[order_id]["items"])
    if not has_item:
        return f"Error: SKU {item_sku} was not found in order {order_id}."
    
    claim_id = f"CLM-{random.randint(1000, 9999)}"
    CLAIMS[claim_id] = {
        "order_id": order_id,
        "sku": item_sku,
        "issue": damage_description,
        "status": "submitted",
        "date": "2026-07-14"
    }
    
    return f"SUCCESS. Damage claim {claim_id} filed. Estimated resolution: 2026-07-21."


@tool
def request_reshipment(order_id: str, sku: str) -> str:
    """Request a replacement shipment for a lost or damaged item.
    NOTE: This is a restricted action. It will pause the agent and wait for manager approval."""
    if order_id not in ORDERS:
        return f"Error: Order {order_id} not found."
    if sku not in WAREHOUSE:
        return f"Error: SKU {sku} not recognized."
    if WAREHOUSE[sku]["stock"] < 1:
        return f"Error: SKU {sku} is out of stock. Cannot reship."
    
    cost = next((i["price"] for i in ORDERS[order_id]["items"] if i["sku"] == sku), 0.0)
    
    new_tracking = f"RSHP-{random.randint(1000, 9999)}"
    reshipment_log.append({
        "order_id": order_id,
        "sku": sku,
        "item_name": WAREHOUSE[sku]["name"],
        "cost": cost,
        "new_tracking_id": new_tracking,
        "estimated_delivery": "2026-07-20",
        "status": "reshipment_confirmed"
    })
    
    # Deduct stock
    WAREHOUSE[sku]["stock"] -= 1
    
    return f"SUCCESS. Item reshipped. New tracking ID: {new_tracking}."
