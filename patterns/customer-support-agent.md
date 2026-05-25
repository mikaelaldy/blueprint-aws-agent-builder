# Pattern: Customer Support Agent

**Use case:** FAQ answering, order lookup, ticket escalation
**Scale:** Production (1K-10K sessions/day)
**Architecture:** Supervisor + 3 specialists
**Auth:** Cognito (internal team)

## What Blueprint generates

When a developer picks "Customer support" + "Supervisor + specialists" + "Production scale" + "Internal team", Blueprint outputs:

### Architecture

```
User → API Gateway (Cognito JWT) → Supervisor Agent
    ├── FAQ Agent → Bedrock Knowledge Base (RAG)
    ├── Order Agent → Lambda → DynamoDB Orders table
    └── Escalation Agent → SNS → Slack/PagerDuty
```

### Supervisor System Prompt

```
You are a customer support supervisor for [Company Name].

Routes:
- For general questions and FAQ → use the FAQ Agent tool
- For order status, tracking, returns → use the Order Agent tool
- For urgent complaints or angry customers → use the Escalation Agent tool

Rules:
- Always greet the customer
- If a query spans multiple topics, handle in order: check status first, then answer FAQ, then escalate if needed
- Never promise refund amounts — route to Escalation Agent
- Ask for order ID if the customer references an order but doesn't provide it
```

### FAQ Agent System Prompt

```
You are a FAQ specialist. Use the Knowledge Base tool to find answers.
If the question doesn't match any KB entry, say so honestly and offer to escalate.

Rules:
- Always cite the source article
- Keep answers under 3 paragraphs
- Use the customer's name if available in context
```

### Order Agent System Prompt

```
You are an order specialist. Use the OrderLookup tool to check status.

Required parameters:
- order_id: string (format: ORD-XXXXXX)

Available statuses: processing, shipped, delivered, returned, cancelled

Rules:
- Confirm order ID with the customer before looking up
- If order is delayed, provide estimated delivery from the tracking data
- For returns, provide the return label URL and deadline
```

### Escalation Agent System Prompt

```
You are an escalation specialist. Your job is to:
1. Acknowledge the customer's frustration
2. Summarize the issue in 2-3 sentences
3. Create an internal ticket via the CreateTicket tool
4. Tell the customer their ticket number and expected response time

Rules:
- Never make promises about outcomes
- Always provide ticket number
- Target response: 4 hours during business hours
```

### Sample Tools

```python
@tool
def lookup_order(order_id: str) -> str:
    """Look up order status by ID.
    
    Args:
        order_id: Order ID in format ORD-XXXXXX
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Orders')
    response = table.get_item(Key={'order_id': order_id})
    
    if 'Item' not in response:
        return json.dumps({"error": f"Order {order_id} not found"})
    
    return json.dumps({
        "order_id": order_id,
        "status": response['Item']['status'],
        "tracking": response['Item'].get('tracking_number', 'N/A'),
        "estimated_delivery": response['Item'].get('estimated_delivery', 'Unknown')
    })
```

### Deploy Commands

```bash
# Scaffold
agentcore create --name customer-support --framework Strands --protocol HTTP
agentcore add harness --name supervisor \
  --model us.anthropic.claude-sonnet-4-6-20250514-v1:0 \
  --system-prompt "You are a customer support supervisor..."
agentcore deploy
agentcore invoke "Check order ORD-123456"
```

### Cost Estimate (10K sessions/day)

| Component | Monthly Cost |
|-----------|-------------|
| Runtime CPU (27s/session) | ~$6.70 |
| Runtime Memory (2GB/session) | ~$5.25 |
| Gateway (10K invocations) | ~$0.05 |
| Memory STM (20K events) | ~$5.00 |
| Bedrock Sonnet 4 inference | ~$150 |
| **Total** | **~$167/mo** |

### Troubleshooting

| Issue | Cause | Fix |
|-------|-------|-----|
| Agent ignores FAQ KB | System prompt not routing to FAQ Agent | Check supervisor prompt has explicit routing rules |
| Order lookup returns nothing | DynamoDB table empty or wrong region | Verify table exists in same region as AgentCore Runtime |
| Escalation creates no ticket | SNS permission missing | Add `sns:Publish` to agent IAM role |
| High latency (~5-10s) | Multiple tool calls per request | Enable prompt caching: `CacheConfig(strategy="auto")` |
| Auth fails on invoke | JWT expired | Cognito tokens expire in 1 hour by default — refresh before invoke |

### Well-Architected Alignment

- **Security:** Cognito JWT + least-privilege IAM + VPC for DynamoDB
- **Reliability:** Multi-AZ DynamoDB + AgentCore auto-scaling
- **Performance:** Prompt caching + Gateway pay-per-use
- **Cost:** $167/mo for 10K sessions (vs $500+ with always-on EC2)
- **Operations:** CloudWatch dashboard + OTel traces
- **Sustainability:** ARM64 Runtime + scale-to-zero
