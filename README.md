# Blueprint: Universal AWS Agent Builder

> *A meta-prompt that interviews you about your AI agent needs and generates a complete, deployable AWS AgentCore system.*

**What it solves:** Building AI agents on AWS means navigating a maze of services (AgentCore, Bedrock, Lambda, Cognito) and frameworks (Strands, LangChain, CrewAI). Most developers either get stuck in analysis paralysis or ship agents with no auth, monitoring, or cost controls.

**How it works:** Paste the prompt from `PROMPT.md` into Kiro, Cursor, Claude Code, Codex CLI, or any AI coding tool. Blueprint interviews you one question at a time — then generates:

- Runnable Strands agent code
- Exact AgentCore CLI commands to deploy
- CDK infrastructure stack
- Cost estimate at your scale
- Security checklist
- 5+ troubleshooting scenarios
- Full deployment guide

## Quick Start

1. Copy the prompt from [PROMPT.md](./PROMPT.md)
2. Paste into your AI coding tool (Kiro, Cursor, Claude Code, etc.)
3. Answer 10 questions about your agent idea
4. Deploy with the generated AgentCore CLI commands

## Prerequisites

- AWS account with AgentCore permissions
- `npm install -g @aws/agentcore`
- `pip install strands-agents strands-agents-tools`
- Model access enabled in Amazon Bedrock (us-west-2)

## License

MIT
