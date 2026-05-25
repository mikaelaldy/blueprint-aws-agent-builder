"""
Multi-Agent Supervisor Pattern — Strands Agents SDK + Amazon Bedrock AgentCore

This template demonstrates the "Agents as Tools" pattern:
- A supervisor agent routes requests to specialist agents
- Each specialist has its own tools and system prompt
- Results are streamed back via Server-Sent Events (SSE)

Usage:
    pip install strands-agents strands-agents-tools
    agentcore create --name my-agent --framework Strands --protocol HTTP
    # Replace app/MyAgent/main.py with this file
    agentcore deploy
    agentcore invoke "Find me products under $50"
"""

from strands import Agent, tool
from strands_tools import http_request, retrieve


# ---------------------------------------------------------------------------
# Specialist Agent 1: Research
# ---------------------------------------------------------------------------
research_agent = Agent(
    system_prompt="""You are a research specialist.
    Your job is to gather factual, well-sourced information.
    Always cite sources when possible.
    Return structured findings — bullet points or tables preferred.""",
    tools=[http_request, retrieve],
)


# ---------------------------------------------------------------------------
# Specialist Agent 2: Product Recommendations
# ---------------------------------------------------------------------------
product_agent = Agent(
    system_prompt="""You are a product recommendation specialist.
    Given user preferences, search for and recommend products.
    Always return: product name, price, key features, and a link.
    Order results by relevance or rating.""",
    tools=[http_request, retrieve],
)


# ---------------------------------------------------------------------------
# Specialist Agent 3: Data Analysis
# ---------------------------------------------------------------------------
@tool
def analyze_data(data: str, question: str) -> str:
    """
    Analyze structured data and answer a specific question.

    Args:
        data: CSV, JSON, or markdown table data
        question: The analytical question to answer

    Returns:
        Analysis results with numbers and a brief explanation
    """
    analysis_agent = Agent(
        system_prompt="""You are a data analysis specialist.
        Given data and a question, perform calculations and reasoning.
        Return your answer as a number or short summary.
        Show your work step by step.""",
    )
    return analysis_agent(f"Data:\n{data}\n\nQuestion: {question}")


# ---------------------------------------------------------------------------
# Supervisor Agent (orchestrator)
# ---------------------------------------------------------------------------
supervisor = Agent(
    system_prompt="""You are a supervisor that routes user requests to the right specialist:

    - **Research questions** and factual lookups → use the research_agent tool
    - **Product recommendations** and shopping advice → use the product_agent tool
    - **Data analysis** and number crunching → use the analyze_data tool
    - **Simple questions** not requiring specialist knowledge → answer directly

    Always pick the most appropriate tool. If the user asks something that
    spans multiple specialists, call them in sequence and combine the results.

    Before answering, confirm which tool(s) you plan to use with a brief
    one-line note so the user can see your reasoning.""",
    tools=[research_agent, product_agent, analyze_data],
)


# ---------------------------------------------------------------------------
# Entry point for AgentCore Runtime
# ---------------------------------------------------------------------------
def invoke(payload: dict) -> str:
    """Called by AgentCore Runtime when a user sends a message."""
    prompt = payload.get("prompt", "")
    return supervisor(prompt)


# ---------------------------------------------------------------------------
# Local testing (not used in production — agentcore invoke handles this)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Running locally...")
    print(invoke({"prompt": "Find me products under $50"}))
