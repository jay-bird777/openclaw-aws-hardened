# OpenClaw-style Agent on AWS (Hardened)

This project deploys an always-on personal agent container on AWS using Terraform with security-focused defaults:
- No inbound SSH (SSM Session Manager access only)
- Secrets stored in SSM Parameter Store (SecureString)
- Docker Compose runtime on EC2
- CloudWatch log group + basic alarms
- IMDSv2 enforced

## Architecture
- VPC (public subnet)
- EC2 t3.micro (free-tier friendly)
- IAM role with least-privilege SSM Parameter reads
- CloudWatch Log Group: `/<project>/agent`

## Prereqs
- AWS account
- AWS CLI configured: `aws configure`
- Terraform installed (>= 1.5)

## 1) Create SSM parameters (secrets)
```bash
export AWS_REGION=us-west-2
export PREFIX=/openclaw/agent
./scripts/bootstrap-params.sh
