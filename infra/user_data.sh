#!/usr/bin/env bash
set -euo pipefail

# Terraform replaces ONLY these:
PROJECT_NAME="${project_name}"
AWS_REGION="${aws_region}"
AGENT_IMAGE="${agent_image}"
AGENT_CONTAINER_NAME="${agent_container_name}"
SSM_PREFIX="${agent_ssm_param_prefix}"

export DEBIAN_FRONTEND=noninteractive

apt-get update -y
apt-get install -y ca-certificates curl jq awscli

if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh
  usermod -aG docker ubuntu || true
fi

apt-get install -y docker-compose-plugin

mkdir -p /opt/app
cd /opt/app

# IMPORTANT: below this point, do NOT use dollar-curly braces (example removed). Terraform will try to template it.
cat > docker-compose.yml <<YAML
services:
  agent:
    image: $AGENT_IMAGE
    container_name: $AGENT_CONTAINER_NAME
    restart: unless-stopped
    env_file:
      - /opt/app/agent.env
    logging:
      driver: awslogs
      options:
        awslogs-region: $AWS_REGION
        awslogs-group: /$PROJECT_NAME/agent
        awslogs-stream: $AGENT_CONTAINER_NAME
YAML

touch /opt/app/agent.env
chmod 600 /opt/app/agent.env

get_param () {
  local name="$1"
  aws ssm get-parameter \
    --region "$AWS_REGION" \
    --name "$name" \
    --with-decryption \
    --query 'Parameter.Value' \
    --output text 2>/dev/null || true
}

write_env () {
  local key="$1"
  local val="$2"

  if [[ -z "$val" || "$val" == "None" ]]; then
    return 0
  fi

  if grep -q "^$key=" /opt/app/agent.env; then
    sed -i "s|^$key=.*|$key=$val|g" /opt/app/agent.env
  else
    echo "$key=$val" >> /opt/app/agent.env
  fi
}

write_env "TELEGRAM_BOT_TOKEN" "$(get_param "$SSM_PREFIX/TELEGRAM_BOT_TOKEN")"
write_env "TELEGRAM_CHAT_ID"   "$(get_param "$SSM_PREFIX/TELEGRAM_CHAT_ID")"
write_env "MODEL_PROVIDER"     "$(get_param "$SSM_PREFIX/MODEL_PROVIDER")"
write_env "MODEL_API_KEY"      "$(get_param "$SSM_PREFIX/MODEL_API_KEY")"
write_env "DISCORD_WEBHOOK_URL" "$(get_param "$SSM_PREFIX/DISCORD_WEBHOOK_URL")"
