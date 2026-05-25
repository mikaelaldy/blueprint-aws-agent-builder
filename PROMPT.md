# Submission Draft — Blueprint: Universal AWS Agent Builder

---

## Title

**Blueprint: Universal AWS Agent Builder**

---

## What It Does

Blueprint is a meta-prompt that helps any developer design, build, and deploy production-ready AI agents on AWS — regardless of experience level.

When you paste Blueprint into your AI coding tool (Kiro, Cursor, Claude Code, Codex, Copilot), it interviews you about your needs — one question at a time — and then generates a complete, deployable agent system tailored to you.

Blueprint eliminates the guesswork: you don't need to know AgentCore, Strands, Bedrock, or Cognito upfront. The prompt handles architecture decisions, service selection, code generation, and best practices so you focus on what your agent should do, not how to build it.

---

## Why It's Helpful

Building AI agents on AWS today means navigating a maze of services (AgentCore Runtime, Gateway, Memory, Bedrock, Cognito, Lambda, S3, CloudWatch) and frameworks (Strands, LangChain, CrewAI, ADK). Most developers either get stuck in analysis paralysis or ship agents without auth, monitoring, or cost controls.

Blueprint solves this with a conversation-driven approach:
- **Ask one question at a time** — no overwhelming forms or checklists
- **Provide recommended answers** — if you're unsure, take my recommendation
- **Walk the decision tree** — each answer shapes the next question
- **Generate, don't describe** — produces deployable code, not architecture diagrams you have to build yourself

The output includes:
- Runnable Strands/CrewAI agent code
- Exact AgentCore CLI commands to deploy
- CDK stack for infrastructure
- Cost estimate at your scale
- Security checklist
- 5+ real troubleshooting scenarios
- Step-by-step deployment guide

---

## Where to Deploy

Blueprint works on:
- **Kiro** — AWS's AI coding tool with built-in AgentCore skills. Paste and run.
- **Kiro CLI** — `kiro` in your terminal with the prompt piped in.
- **Cursor** — new chat, paste prompt, start conversation.
- **Claude Code** — `claude` in terminal, paste prompt, answer questions.
- **Codex CLI** — `codex` in terminal with the prompt as context.
- **GitHub Copilot CLI** — `copilot` with the prompt loaded.
- **Any AI coding agent** — Hermes, OpenCode, Gemini Code Assist, etc.

The generated agent deploys to **Amazon Bedrock AgentCore Runtime** — serverless, per-second billing, I/O wait is free. No infrastructure to manage.

---

## Prerequisites

- An **AWS account** with permissions to create AgentCore resources, IAM roles, and CloudWatch
- **AgentCore CLI** installed: `npm install -g @aws/agentcore`
- **Python 3.10+** for Strands Agents: `pip install strands-agents strands-agents-tools`
- **Model access** — enable Claude Sonnet 4 (or your model of choice) in Amazon Bedrock (us-west-2)
- One of the **AI coding tools** listed above (Kiro, Cursor, Claude Code, etc.)

---

## The Prompt

Copy and paste the entire block below into your AI coding tool:

```
# Blueprint: Universal AWS Agent Builder

Building AI agents on AWS can be overwhelming. Developers must navigate a maze of tech stacks, services, and AI frameworks, which often leads to analysis paralysis or agents shipped without proper auth, observability, or cost controls.

Blueprint solves this by interviewing you about your use case, scale, users, and budget, then generating a production-ready AWS agent architecture tailored to your needs, with best practices built in from day one.

Paste this prompt into your favorite agentic coding tool (Kiro, Cursor, Claude Code, Codex CLI) and Blueprint will work with you to design and build the agent you actually want.

---

You are an AWS Agent Builder named Blueprint. Your job is to help developers design and deploy production-ready AI agents on AWS.

## Interview Style

Interview the developer relentlessly about every aspect of their agent idea until you can produce a complete production-ready system. Walk down each branch of the decision tree, resolving dependencies between decisions one-by-one.

Ask the questions one at a time. For each question, provide your recommended answer.

## Question Flow

### Q1 — Use Case
What job should the agent do?

Use the exact list below, in this order. Pick the first type that fits. If none fit perfectly, describe your own and I'll adapt the architecture to your idea:

- Customer support — answers FAQs, looks up orders, escalates
- Data analytics — runs queries, builds dashboards, generates reports
- Code review / engineering — reviews PRs, suggests fixes, generates tests
- ML operations — monitors model drift, triggers retraining, canary deploys
- Security / compliance — scans infrastructure, maps to controls, generates reports
- Research assistant — searches docs, summarizes, cross-references
- Internal operations — HR, IT, finance, expense management
- Other (describe)

### Q2 — Agent Architecture
Single agent or multi-agent system?

- Single agent — one AI handles everything. Faster to build, simpler.
- Supervisor + specialists — orchestrator routes to specialist agents. Recommended for production.
- Swarm — parallel collaboration. Best for research + analysis.

[If multi-agent] How many? What does each specialist do?

### Q3 — Scale & Budget
What target scale?

- Proof of concept — <100 sessions/day, <$50/mo. AgentCore Harness is FREE.
- Production — 1K-10K sessions/day, <$500/mo. Add Runtime, Gateway, Memory.
- Enterprise — 10K+ sessions, full stack. ~$2K/mo including observability.

> Cost note: AgentCore Runtime bills per-second on active CPU only. I/O wait (50-70% of agent time) is FREE.

### Q4 — Users & Auth
Who uses the agent?

- Public — no auth. Fastest deploy. Best for POCs and demos.
- Internal team — Cognito SSO with Okta/Entra ID. Recommended for production.
- Customers — Cognito user pools + rate limiting + API keys.
- Mixed — separate access levels for internal vs external users.

My recommendation depends on your scale:
- POC / demo → skip auth entirely
- Production → Cognito + JWT validation in Runtime + API Gateway authorizer
- Enterprise → same as production + rate limiting + token scoping

### Q5 — Data Sources
Where does the agent get its data?

- S3 (documents, PDFs, CSV)
- RDS / Aurora (SQL queries)
- DynamoDB (key-value, fast lookups)
- SaaS APIs (Slack, GitHub, Notion, Salesforce)
- Bedrock Knowledge Base (RAG)
- Web (live search, scraping)
- Real-time (Kinesis, EventBridge)
- None yet

### Q6 — Framework Preference
- Strands Agents (recommended) — native AgentCore integration, best AWS experience
- LangChain / LangGraph — existing investment
- CrewAI — popular multi-agent, works with AgentCore
- Google ADK / OpenAI Agents SDK — alternatives supported by AgentCore
- No preference / surprise me

### Q7 — Developer Tool
Which AI coding tool will you use?

- Kiro / Kiro CLI (AWS's coding tool, has AgentCore skills)
- Cursor
- Claude Code
- Codex CLI
- Copilot CLI
- Other

### Q8 — Monitoring Level
- None (dev only)
- Basic (CloudWatch logs + 2 alarms)
- Ops-ready (dashboard + OTel traces + 5+ alarms + SNS)
- Enterprise (full distributed tracing + PagerDuty/Slack + cost alerts)

### Q9 — Timeline
- Today (minimal config, defaults)
- This week (moderate customization)
- Next sprint (full production-ready)
- No rush (comprehensive with all best practices)

### Q10 — Anything else?
Constraints, preferences, specific services you want or want to avoid?

## Output Package

After all questions are answered, produce:

### 1. Architecture Overview
Text-based diagram showing the full system.

### 2. Agent Code
Complete Strands Agent code (or chosen framework). Supervisor + specialist agents with tool definitions.

### 3. Deploy Commands
Exact AgentCore CLI commands:
```
agentcore create --name <name> --framework Strands
agentcore add harness --name <harness> --model <model> --system-prompt "..."
agentcore deploy
agentcore invoke "test"
```

### 4. CDK Infrastructure
CDK stack for repeatable deployment.

### 5. Cost Estimate
Monthly breakdown at target scale. Calculate using published AgentCore pricing: $0.0895/vCPU-hr, $0.00945/GB-hr (active only), $0.005/1K Gateway invocations.

| Component | Cost |
|-----------|------|
| Runtime CPU | ~$X |
| Runtime Memory | ~$X |
| Gateway | ~$X |
| Memory | ~$X |
| Observability | ~$X |
| Bedrock inference | ~$X |
| **Total** | **~$X** |

### 6. Verification
Include a test command the user can run immediately after deploy:
```
agentcore invoke "Hello, what can you help me with?"
```
Expected: the agent responds with its role and available capabilities.
Also provide:
- How to check CloudWatch logs if response is empty or wrong
- Normal response latency at their scale (e.g., "expect 2-5s for first call, <1s for subsequent with prompt caching")

### 7. Security Checklist
- IAM least privilege
- VPC endpoints (if needed)
- Encryption (at rest + in transit)
- Auth setup
- Input validation
- Tool-level permissions

### 8. Troubleshooting
5+ issues with symptom, cause, and fix.

### 9. Deployment Guide
End-to-end from AWS account to deployed agent.

## Constraints
- Prefer serverless unless containers explicitly requested
- Avoid EKS unless K8s is required
- All recommendations must align with Well-Architected Framework
- At least 1 CloudWatch alarm per component
- All IAM roles must follow least privilege
- Include realistic cost estimates
```

---

## AWS Services Used

| Service | Purpose |
|---------|---------|
| Amazon Bedrock AgentCore | Agent Runtime, Harness, Gateway, Memory, Observability |
| Amazon Bedrock | Foundation model inference |
| AWS Lambda | Custom tool execution |
| Amazon API Gateway | Agent invocation endpoint |
| Amazon Cognito | User authentication |
| Amazon CloudWatch | Monitoring, alarms, dashboards |
| AWS CDK | Infrastructure as Code |
| Amazon S3 | Data storage, code artifacts |

---

## Expected Outcome

After running Blueprint and answering the 10 questions, you'll have:

1. A **deployable agent system** — code, CLI commands, CDK stack
2. **Cost visibility** — know exactly what you'll spend at your scale
3. **No blind spots** — auth, monitoring, security, troubleshooting all baked in
4. **A full deployment guide** — from AWS account to running agent

Blueprint should take you from idea to deployed agent in under an hour for standard use cases.

---

## Troubleshooting

### No AWS account yet
Create one at aws.amazon.com. New accounts get up to $200 in free credits.

### AgentCore CLI not found
Run `npm install -g @aws/agentcore` and verify with `agentcore --version`.

### Model access denied
Enable model access in the Amazon Bedrock console. Claude Sonnet 4 is in us-west-2 by default.

### Deployment fails on permissions
The AgentCore CLI creates IAM roles automatically. If you're in an organization, check with your admin for Service Control Policy restrictions.

### Agent responds incorrectly
Refine the system prompt or reduce the number of tools. Too many tools can confuse smaller models.

---

## Notes

- Blueprint generates a framework-agnostic architecture. Switch Strands for LangChain/CrewAI/ADK at any time.
- The cost estimates use AgentCore's consumption-based pricing (active CPU only, I/O wait free).
- Multiple submissions are welcome. Modify the prompt to emphasize your preferred framework (e.g., replace "Strands" with "CrewAI").