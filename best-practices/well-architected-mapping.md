# AWS Well-Architected Framework — Agent Mapping

How each AWS agent service satisfies the 6 Well-Architected pillars.

| Pillar | Service | How it applies |
|--------|---------|---------------|
| **Security** | AgentCore Runtime | True session isolation — each user gets a dedicated microVM. No shared state between sessions. |
| **Security** | AgentCore Identity | JWT validation, Cognito/Okta/Entra ID integration, OAuth delegation for SaaS tools. |
| **Security** | AgentCore Gateway | SigV4 auth for MCP tools, OAuth for private APIs. Scoped per-tool permissions. |
| **Security** | IAM (CDK roles) | Least-privilege by default — no `*` permissions in generated templates. |
| **Reliability** | AgentCore Runtime | Auto-scaling from zero to thousands of concurrent sessions. No capacity planning. |
| **Reliability** | AgentCore Memory | Persistent state survives session restarts. Long-term memory for personalization. |
| **Reliability** | CloudWatch | Logs, metrics, and alarms for agent health monitoring. |
| **Performance Efficiency** | AgentCore Runtime | Consumption-based pricing — I/O wait (50-70% of agent time) is FREE. Pay only for active CPU. |
| **Performance Efficiency** | Strands Agents SDK | Native prompt caching — reuses system prompts and context across calls. |
| **Performance Efficiency** | AgentCore Harness | Config-first architecture — change model/tools without code rewrites. |
| **Cost Optimization** | AgentCore Runtime | Per-second billing with 1-second minimum. No idle compute costs. |
| **Cost Optimization** | AgentCore Gateway | Pay per invocation ($0.005/1K). No fixed costs for unused tools. |
| **Cost Optimization** | AgentCore Memory | Pay per event/record/retrieval. No minimum storage commitment. |
| **Cost Optimization** | CloudWatch alarms | Budget alerts prevent cost surprises. |
| **Operational Excellence** | AgentCore Observability | OpenTelemetry traces across full agent chain. Distributed tracing for multi-agent. |
| **Operational Excellence** | CDK / Terraform | Infrastructure as Code — reproducible, version-controlled deployments. |
| **Operational Excellence** | AgentCore CLI | Single workflow from scaffold to deploy: `agentcore create` → `agentcore dev` → `agentcore deploy`. |
| **Sustainability** | AgentCore Runtime | ARM64 (Graviton) by default — better performance per watt. |
| **Sustainability** | AgentCore Runtime | No idle compute — agents scale to zero when not in use. |

## Security Checklist for Agents

- [ ] IAM role uses least privilege (no `*` actions or resources)
- [ ] AgentCore Identity configured for JWT validation
- [ ] VPC endpoints for private data sources (RDS, DynamoDB)
- [ ] S3 buckets have Block Public Access enabled
- [ ] Secrets stored in AWS Secrets Manager (not environment variables)
- [ ] Tool-level permissions scoped (each agent only gets tools it needs)
- [ ] Rate limiting on API Gateway endpoint
- [ ] CloudTrail enabled for audit logging
- [ ] Input validation in Lambda tool functions
- [ ] Encryption at rest (S3, RDS, DynamoDB) and in transit (TLS)

## Cost Estimate Reference

Use published AgentCore pricing (May 2026):

| Component | Price | Notes |
|-----------|-------|-------|
| Runtime CPU | $0.0895/vCPU-hr | Active only, I/O wait free |
| Runtime Memory | $0.00945/GB-hr | 128MB minimum |
| Gateway invocations | $0.005/1K calls | ListTools, InvokeTool, Ping |
| Gateway search | $0.025/1K calls | Tool discovery |
| Memory STM | $0.25/1K events | Short-term memory |
| Memory LTM | $0.75/1K records/mo | Long-term memory storage |
| Harness | **FREE** | Only pay for Runtime |
| Identity | Free via Runtime | Standalone: $0.010/1K requests |
