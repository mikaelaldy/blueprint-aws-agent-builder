import json

import json
"""
Single Agent Template — Strands Agents SDK + Amazon Bedrock AgentCore

Use this template when your use case fits one agent handling everything.
Common for: FAQ bots, internal tools, simple assistants, POCs.

Usage:
    pip install strands-agents strands-agents-tools
    agentcore create --name my-agent --framework Strands --protocol HTTP
    # Replace app/MyAgent/main.py with this file
    agentcore deploy
    agentcore invoke "What are your store hours?"
"""

from strands import Agent, tool
from strands_tools import http_request, retrieve


# ---------------------------------------------------------------------------
# Custom tool example (replace with your own)
# ---------------------------------------------------------------------------
@tool
def lookup_order(order_id: str) -> str:
    """
    Look up an order by its ID.

    Args:
        order_id: The order identifier (e.g., "ORD-12345")

    Returns:
        JSON string with order details: status, items, total, tracking URL
    """
    # Replace with actual API call or database query
    return json.dumps({
        "order_id": order_id,
        "status": "shipped",
        "total": "$49.99",
        "tracking_url": "https://example.com/track/ORD-12345",
    })


# ---------------------------------------------------------------------------
# Main agent
# ---------------------------------------------------------------------------
agent = Agent(
    system_prompt="""You are a helpful customer support assistant for Example Corp.

    Your capabilities:
    - Answer FAQs using the retrieve tool (knowledge base)
    - Look up order status using the lookup_order tool
    - Search the web for current information using http_request

    Rules:
    - Be polite and concise
    - If you cannot help, offer to connect them with a human agent
    - Never make up information — use tools to get facts
    - Always ask for order ID when checking order status
    - Keep responses under 3 paragraphs unless the user asks for detail""",
    tools=[http_request, retrieve, lookup_order],
)


# ---------------------------------------------------------------------------
# Entry point for AgentCore Runtime
# ---------------------------------------------------------------------------
def invoke(payload: dict) -> str:
    """Called by AgentCore Runtime when a user sends a message."""
    prompt = payload.get("prompt", "")
    return agent(prompt)


# ---------------------------------------------------------------------------
# Local testing
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(invoke({"prompt": "What are your store hours?"}))
