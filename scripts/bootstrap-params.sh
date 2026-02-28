#!/usr/bin/env bash
set -euo pipefail

: "${AWS_REGION:?Set AWS_REGION}"
: "${PREFIX:?Set PREFIX}"

prompt_secret () {
  local label="$1"
  echo -n "$label: "
  read -r -s v
  echo
  echo "$v"
}

prompt_plain () {
  local label="$1"
  echo -n "$label (optional, press Enter to skip): "
  read -r v
  echo "$v"
}

BOT_TOKEN="$(prompt_secret 'Enter Discord Bot Token')"
ALLOWED_CHANNEL_ID="$(prompt_plain 'Enter Allowed Channel ID')"

aws ssm put-parameter --region "$AWS_REGION" --name "$PREFIX/DISCORD_BOT_TOKEN" \
  --type SecureString --value "$BOT_TOKEN" --overwrite >/dev/null
echo "✅ Saved $PREFIX/DISCORD_BOT_TOKEN"

if [[ -n "$ALLOWED_CHANNEL_ID" ]]; then
  aws ssm put-parameter --region "$AWS_REGION" --name "$PREFIX/DISCORD_ALLOWED_CHANNEL_ID" \
    --type String --value "$ALLOWED_CHANNEL_ID" --overwrite >/dev/null
  echo "✅ Saved $PREFIX/DISCORD_ALLOWED_CHANNEL_ID"
else
  echo "ℹ️ Skipped DISCORD_ALLOWED_CHANNEL_ID"
fi
