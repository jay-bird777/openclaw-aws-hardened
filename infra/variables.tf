variable "aws_region" {
  type        = string
  description = "AWS region"
  default     = "us-west-2"
}

variable "project_name" {
  type        = string
  description = "Name prefix for resources"
  default     = "openclaw-aws-hardened"
}

variable "instance_type" {
  type        = string
  description = "EC2 instance type (free-tier friendly)"
  default     = "t3.micro"
}

variable "agent_image" {
  type        = string
  description = "Docker image for your agent (placeholder by default)"
  default     = "ghcr.io/example/agent:latest"
}

variable "agent_container_name" {
  type        = string
  description = "Container name"
  default     = "agent"
}

variable "agent_ssm_param_prefix" {
  type        = string
  description = "SSM parameter prefix for agent secrets"
  default     = "/openclaw/agent"
}

variable "allowed_outbound_cidrs" {
  type        = list(string)
  description = "Outbound egress CIDRs"
  default     = ["0.0.0.0/0"]
}

variable "tags" {
  type        = map(string)
  description = "Extra tags"
  default     = {}
}
