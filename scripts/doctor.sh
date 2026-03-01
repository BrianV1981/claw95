#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

PASS=0
WARN=0
FAIL=0

ok(){ echo "[doctor] PASS: $*"; PASS=$((PASS+1)); }
warn(){ echo "[doctor] WARN: $*"; WARN=$((WARN+1)); }
bad(){ echo "[doctor] FAIL: $*"; FAIL=$((FAIL+1)); }

if command -v python3 >/dev/null 2>&1; then ok "python3 available"; else bad "python3 missing"; fi

if [[ -d .venv ]]; then ok ".venv exists"; else warn ".venv missing (run scripts/preflight.sh)"; fi

if [[ -f config/policy.yaml ]]; then ok "config/policy.yaml present"; else bad "config/policy.yaml missing"; fi

if [[ -f logs/events.jsonl ]]; then ok "events log exists"; else warn "events log not created yet (start server first)"; fi

if ss -H -lnt "sport = :8765" | grep -q 8765; then
  ok "port 8765 in use (server likely running)"
else
  warn "port 8765 not in use (server not running)"
fi

if [[ -f config/policy.yaml ]]; then
  if grep -q 'discord_webhook_url: ""' config/policy.yaml; then
    warn "discord webhook sink disabled (discord_webhook_url empty)"
  else
    ok "discord webhook sink appears configured"
  fi

  if grep -q 'markdown_enabled: true' config/policy.yaml; then ok "markdown sink enabled"; else warn "markdown sink disabled"; fi
  if grep -q 'jsonl_enabled: true' config/policy.yaml; then ok "jsonl sink enabled"; else warn "jsonl sink disabled"; fi
fi

if [[ -f logs/transcript.md ]]; then
  ok "transcript file present"
else
  warn "transcript file missing (will appear after first messages if sink enabled)"
fi

echo ""
echo "[doctor] summary: PASS=$PASS WARN=$WARN FAIL=$FAIL"
if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
