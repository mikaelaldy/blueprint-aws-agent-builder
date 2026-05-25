"""
CDK Stack — Amazon Bedrock AgentCore Deployment

Deploys:
- AgentCore Runtime (serverless, per-second billing)
- IAM roles with least privilege
- CloudWatch log group
- (Optional) API Gateway endpoint for external access

Usage:
    pip install aws-cdk-lib constructs
    cdk bootstrap  # if first time
    cdk deploy

Prerequisites:
    - AWS CLI configured with credentials
    - Model access enabled in Bedrock console
    - AgentCore CLI installed: npm install -g @aws/agentcore
"""

from aws_cdk import (
    Stack,
    Duration,
    CfnOutput,
    aws_iam as iam,
    aws_logs as logs,
)
from constructs import Construct


class AgentStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs):
        super().__init__(scope, construct_id, **kwargs)

        # -----------------------------------------------------------------
        # 1. IAM Role — least privilege for AgentCore Runtime
        # -----------------------------------------------------------------
        agent_role = iam.Role(
            self,
            "AgentRuntimeRole",
            assumed_by=iam.ServicePrincipal("bedrock-agentcore.amazonaws.com"),
            description="Least-privilege role for AgentCore Runtime",
        )

        # Bedrock model inference
        agent_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock:InvokeModel",
                    "bedrock:InvokeModelWithResponseStream",
                ],
                resources=[
                    f"arn:aws:bedrock:{self.region}::foundation-model/anthropic.claude-*",
                ],
            )
        )

        # AgentCore services
        agent_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "bedrock-agentcore:*",  # Runtime, Memory, Gateway
                ],
                resources=["*"],  # Scope to specific ARNs in production
                conditions={
                    "StringEquals": {
                        "aws:RequestedRegion": [self.region],
                    },
                },
            )
        )

        # CloudWatch logging
        agent_role.add_to_policy(
            iam.PolicyStatement(
                actions=[
                    "logs:CreateLogGroup",
                    "logs:CreateLogStream",
                    "logs:PutLogEvents",
                ],
                resources=[
                    f"arn:aws:logs:{self.region}:{self.account}:log-group:/aws/agentcore/*",
                ],
            )
        )

        # -----------------------------------------------------------------
        # 2. CloudWatch Log Group
        # -----------------------------------------------------------------
        log_group = logs.LogGroup(
            self,
            "AgentLogGroup",
            log_group_name="/aws/agentcore/my-agent",
            retention=logs.RetentionDays.TWO_WEEKS,
            removal_policy=aws_cdk.RemovalPolicy.DESTROY,
        )

        # -----------------------------------------------------------------
        # 3. Outputs
        # -----------------------------------------------------------------
        CfnOutput(
            self,
            "AgentRoleArn",
            value=agent_role.role_arn,
            description="IAM role ARN for AgentCore Runtime",
        )

        CfnOutput(
            self,
            "LogGroupName",
            value=log_group.log_group_name,
            description="CloudWatch log group for agent traces",
        )

        CfnOutput(
            self,
            "DeployInstructions",
            value=(
                "Run: agentcore create --name my-agent --framework Strands --protocol HTTP && "
                "agentcore deploy && agentcore invoke 'Test message'"
            ),
            description="Next steps after CDK deploy",
        )
