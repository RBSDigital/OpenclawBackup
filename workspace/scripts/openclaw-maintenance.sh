#!/usr/bin/env bash
set -uo pipefail

OPENCLAW_BIN="${OPENCLAW_BIN:-$HOME/.npm-global/bin/openclaw}"
export OPENCLAW_CONFIG_PATH="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
if [ ! -x "$OPENCLAW_BIN" ]; then
  OPENCLAW_BIN="$(command -v openclaw 2>/dev/null || true)"
fi
if [ -z "$OPENCLAW_BIN" ] || [ ! -x "$OPENCLAW_BIN" ]; then
  echo "openclaw binary not found" >&2
  exit 127
fi

configure_openclaw_cli_gateway() {
  [ -z "${OPENCLAW_GATEWAY_URL:-}" ] || return 0
  [ -f "$OPENCLAW_CONFIG_PATH" ] || return 0

  local port bind token addr
  port="$(node -e 'const fs=require("fs"); const c=JSON.parse(fs.readFileSync(process.env.OPENCLAW_CONFIG_PATH,"utf8")); console.log(c.gateway?.port || 18789)' 2>/dev/null || true)"
  bind="$(node -e 'const fs=require("fs"); const c=JSON.parse(fs.readFileSync(process.env.OPENCLAW_CONFIG_PATH,"utf8")); console.log(c.gateway?.bind || "loopback")' 2>/dev/null || true)"
  token="[REDACTED_SECRET] -e 'const fs=require("fs"); const c=JSON.parse(fs.readFileSync(process.env.OPENCLAW_CONFIG_PATH,"utf8")); console.log(typeof c.gateway?.auth?.token =[REDACTED_SECRET] "string" ? c.gateway.auth.token : "")' 2>/dev/null || true)"
  [ -n "$port" ] || port=18789

  if [ "$bind" = "tailnet" ]; then
    addr="$(ss -H -ltn "sport = :$port" 2>/dev/null | awk '{print $4}' | sed "s/.*\\[//;s/\\].*//;s/:$port$//" | grep -Ev '^(127\.|::1|0\.0\.0\.0|\*)$' | head -n 1 || true)"
    if [ -n "$addr" ]; then
      export OPENCLAW_GATEWAY_URL="ws://$addr:$port"
      [ -n "${OPENCLAW_GATEWAY_TOKEN:[REDACTED_SECRET]" ] || [ -z "$token" ] || export OPENCLAW_GATEWAY_TOKEN="[REDACTED_SECRET]"
    fi
  fi
}

configure_openclaw_cli_gateway

REPORT_EMAIL="${REPORT_EMAIL:-vrbs940054@gmail.com}"
GOG_ACCOUNT="${GOG_ACCOUNT:-vrbs940054@gmail.com}"
LOG_DIR="$HOME/.openclaw/logs"
mkdir -p "$LOG_DIR"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_LOG="$LOG_DIR/maintenance-$TS.log"

log() {
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$RUN_LOG"
}

send_report() {
  local msg="$1"
  local subject="OpenClaw daily maintenance report ($(date -u +%F))"
  gog gmail send --account "$GOG_ACCOUNT" --to "$REPORT_EMAIL" --subject "$subject" --body "$msg" >/dev/null 2>&1 || {
    log "FAILED to send email report to $REPORT_EMAIL"
    log "Report body: $msg"
    return 1
  }
  return 0
}

suggestions_common=$'- Check gateway logs: openclaw logs --follow\n- Run diagnostics: openclaw doctor\n- Verify service: systemctl --user status openclaw-gateway.service'
HEALTH_TIMEOUT_SECONDS="${HEALTH_TIMEOUT_SECONDS:-180}"
HEALTH_RETRY_SECONDS="${HEALTH_RETRY_SECONDS:-10}"
SECURITY_AUDIT_SUMMARY=""
SECURITY_AUDIT_CRITICAL=0

security_audit() {
  local security_out secrets_out parsed

  if ! security_out="$("$OPENCLAW_BIN" security audit --deep --json 2>&1)"; then
    printf 'security audit command failed during maintenance\n%s\n' "$security_out"
    return 1
  fi

  if ! secrets_out="$("$OPENCLAW_BIN" secrets audit --json 2>&1)"; then
    printf 'secrets audit command failed during maintenance\n%s\n' "$secrets_out"
    return 1
  fi

  parsed="$(SECURITY_OUT="$security_out" SECRETS_OUT="$secrets_out" node <<'NODE'
const sec = JSON.parse(process.env.SECURITY_OUT || '{}');
const secrets = JSON.parse(process.env.SECRETS_OUT || '{}');
const secSummary = sec.summary || {};
const secFindings = Array.isArray(sec.findings) ? sec.findings : [];
const secretSummary = secrets.summary || {};
const secretFindings = Array.isArray(secrets.findings) ? secrets.findings : [];
const lines = [];
lines.push(`Security audit: critical=${secSummary.critical ?? 0} warn=${secSummary.warn ?? 0} info=${secSummary.info ?? 0}`);
if (secFindings.length) {
  lines.push(`Security findings: ${secFindings.slice(0, 4).map((f) => `${f.title} (${f.severity})`).join('; ')}${secFindings.length > 4 ? '; ...' : ''}`);
}
lines.push(`Secrets audit: plaintext=${secretSummary.plaintextCount ?? 0} unresolved=${secretSummary.unresolvedRefCount ?? 0} shadowed=${secretSummary.shadowedRefCount ?? 0} legacy=${secretSummary.legacyResidueCount ?? 0}`);
if (secretFindings.length) {
  lines.push(`Secret findings: ${secretFindings.slice(0, 4).map((f) => `${f.code} in ${f.file}`).join('; ')}${secretFindings.length > 4 ? '; ...' : ''}`);
}
console.log(String(secSummary.critical ?? 0));
console.log(lines.join('\n'));
NODE
)"

  SECURITY_AUDIT_CRITICAL="$(printf '%s\n' "$parsed" | sed -n '1p')"
  SECURITY_AUDIT_SUMMARY="$(printf '%s\n' "$parsed" | sed -n '2,$p')"

  if [ "${SECURITY_AUDIT_CRITICAL:-0}" -gt 0 ]; then
    return 1
  fi

  printf '%s\n' "$SECURITY_AUDIT_SUMMARY"
}

health_gate() {
  local phase="$1"
  local config_out health_out

  if ! config_out="$("$OPENCLAW_BIN" config validate --json 2>&1)"; then
    printf 'config validation command failed during %s\n%s\n' "$phase" "$config_out"
    return 1
  fi

  if ! health_out="$("$OPENCLAW_BIN" health --json 2>&1)"; then
    printf 'health command failed during %s\n%s\n' "$phase" "$health_out"
    return 1
  fi

  CONFIG_OUT="$config_out" HEALTH_OUT="$health_out" node <<'NODE'
const fs = require('fs');
const cfgPath = process.env.OPENCLAW_CONFIG_PATH;
let cfg, config, health;
try {
  cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
  config = JSON.parse(process.env.CONFIG_OUT || '{}');
  health = JSON.parse(process.env.HEALTH_OUT || '{}');
} catch (err) {
  console.error(`health parse failed: ${err.message}`);
  process.exit(1);
}

const errors = [];
if (config.valid !== true) errors.push('config validate did not return valid=true');
if (health.ok !== true) errors.push('health ok != true');
if (health.plugins?.errors?.length) errors.push(`plugin errors: ${health.plugins.errors.length}`);
for (const [channel, entry] of Object.entries(cfg.channels || {})) {
  if (entry?.enabled !== true) continue;
  const state = health.channels?.[channel];
  if (!state) {
    errors.push(`enabled channel missing from health: ${channel}`);
    continue;
  }
  const accounts = state.accounts ? Object.values(state.accounts) : [state];
  const anyRunning = accounts.some((account) => account?.running === true && account?.connected !== false && !account?.lastError);
  if (!anyRunning) errors.push(`enabled channel not healthy: ${channel}`);
}
if (errors.length) {
  console.error(errors.join('\n'));
  process.exit(1);
}
NODE
}

wait_for_health_gate() {
  local phase="$1"
  local deadline attempt out

  deadline=$(( $(date +%s) + HEALTH_TIMEOUT_SECONDS ))
  attempt=1

  while true; do
    if out="$("$OPENCLAW_BIN" --version 2>&1; health_gate "$phase" 2>&1)"; then
      if [ "$attempt" -gt 1 ]; then
        log "Health gate passed during $phase after $attempt attempts."
      fi
      printf '%s\n' "$out"
      return 0
    fi

    if [ "$(date +%s)" -ge "$deadline" ]; then
      printf '%s\n' "$out"
      return 1
    fi

    log "Health gate not ready during $phase (attempt $attempt); retrying in ${HEALTH_RETRY_SECONDS}s."
    sleep "$HEALTH_RETRY_SECONDS"
    attempt=$((attempt + 1))
  done
}

log "Starting daily OpenClaw maintenance"
BEFORE_VER="$("$OPENCLAW_BIN" --version 2>&1 || true)"
log "Before version: $BEFORE_VER"

# Stop gateway temporarily during updates to release SQLite leases cleanly
log "Stopping gateway service before update to avoid active database lease collisions"
systemctl --user stop openclaw-gateway.service 2>&1 || true

UPDATE_JSON_RAW=""
UPDATE_MODE="openclaw-update"
if ! UPDATE_JSON_RAW="$("$OPENCLAW_BIN" update --yes --no-restart --json 2>&1)"; then
  if echo "$UPDATE_JSON_RAW" | grep -qi 'cannot run from inside the gateway service process'; then
    log "openclaw update blocked in service context; falling back to npm global reinstall"
    UPDATE_MODE="npm-fallback"
    if ! UPDATE_JSON_RAW="$(npm i -g openclaw@latest --no-fund --no-audit --loglevel=error 2>&1)"; then
      systemctl --user start openclaw-gateway.service 2>&1 || true
      MSG="⚠️ OpenClaw daily maintenance failed at UPDATE step (UTC $TS).\n\nError:\n$UPDATE_JSON_RAW\n\nCurrent version: $BEFORE_VER\n\nSuggested fixes:\n$suggestions_common\n- Retry install manually: npm i -g openclaw@latest"
      send_report "$MSG"
      exit 1
    fi
  else
    log "openclaw update returned non-zero, checking if core files were updated..."
    UPDATE_MODE="openclaw-update-advisory"
  fi
fi

echo "$UPDATE_JSON_RAW" >> "$RUN_LOG"

# Sync installed plugins with updated core SDK to prevent runtime export mismatches
log "Synchronizing installed plugins with core..."
PLUGIN_UPDATE_RAW="$("$OPENCLAW_BIN" plugins update --all --accept-capabilities --acknowledge-install-policy-warning 2>&1 || true)"
echo "$PLUGIN_UPDATE_RAW" >> "$RUN_LOG"

# Run non-interactive doctor repairs and session sqlite migrations
log "Running doctor fix and session sqlite migrations..."
DOCTOR_FIX_RAW="$("$OPENCLAW_BIN" doctor --fix --yes --non-interactive 2>&1 || true)"
echo "$DOCTOR_FIX_RAW" >> "$RUN_LOG"
SESSION_MIGRATE_RAW="$("$OPENCLAW_BIN" doctor --session-sqlite import --session-sqlite-all-agents --non-interactive --yes 2>&1 || true)"
echo "$SESSION_MIGRATE_RAW" >> "$RUN_LOG"

if [ "$UPDATE_MODE" = "openclaw-update" ] || [ "$UPDATE_MODE" = "openclaw-update-advisory" ]; then
  PARSED="$(node -e '
let s=""; process.stdin.on("data",d=>s+=d).on("end",()=>{
  try {
    const j=JSON.parse(s);
    const stepNames=(j.steps||[]).map(s=>s.name).filter(Boolean);
    const actions=(j.actions||stepNames||[]).join("; ");
    const out=[
      j.currentVersion||j.before?.version||"unknown",
      j.targetVersion||j.after?.version||"unknown",
      j.effectiveChannel||j.updateChannel||"unknown",
      actions||"none"
    ];
    console.log(out.join("\n"));
  } catch(e) {
    console.log("unknown\nunknown\nunknown\nunable to parse update json");
  }
});
' <<< "$UPDATE_JSON_RAW")"
else
  PARSED="$(printf '%s\n%s\n%s\n%s\n' "${BEFORE_VER}" "latest" "unknown" "npm i -g openclaw@latest")"
fi

UPDATE_CURRENT="$(echo "$PARSED" | sed -n '1p')"
UPDATE_TARGET="$(echo "$PARSED" | sed -n '2p')"
UPDATE_CHANNEL="$(echo "$PARSED" | sed -n '3p')"
UPDATE_ACTIONS="$(echo "$PARSED" | sed -n '4p')"

log "Update step complete: $UPDATE_CURRENT -> $UPDATE_TARGET"

RESTART_OUT=""
if ! RESTART_OUT="$(systemctl --user restart openclaw-gateway.service 2>&1)"; then
  MSG="⚠️ OpenClaw maintenance failed at RESTART step (UTC $TS).\n\nUpdate completed, but gateway restart failed.\n\nError:\n$RESTART_OUT\n\nVersions: before=$BEFORE_VER, update_current=$UPDATE_CURRENT, update_target=$UPDATE_TARGET\n\nSuggested fixes:\n- Check service status: systemctl --user status openclaw-gateway.service\n- Reload user units: systemctl --user daemon-reload\n- Retry restart: systemctl --user restart openclaw-gateway.service"
  send_report "$MSG"
  exit 2
fi
echo "$RESTART_OUT" >> "$RUN_LOG"

AFTER_VER="$("$OPENCLAW_BIN" --version 2>&1 || true)"
STATUS_LINE="$("$OPENCLAW_BIN" update status 2>&1 | head -n 5 | tr '\n' '; ' || true)"

# Post-update health gate (catches broken module/link states and enabled channels that did not come back)
HEALTH_OUT=""
if ! HEALTH_OUT="$(wait_for_health_gate "post-update" 2>&1)"; then
  log "Health gate failed after update/restart. Attempting recovery reinstall."

  RECOVER_OUT=""
  if ! RECOVER_OUT="$(npm i -g openclaw@latest --no-fund --no-audit --loglevel=error 2>&1)"; then
    MSG="⚠️ OpenClaw maintenance failed at HEALTH step (UTC $TS).\n\nPost-update health gate failed, and recovery reinstall failed.\n\nHealth output:\n$HEALTH_OUT\n\nRecovery output:\n$RECOVER_OUT\n\nSuggested fixes:\n$suggestions_common\n- Retry install manually: npm i -g openclaw@latest"
    send_report "$MSG"
    exit 3
  fi

  RECOVER_RESTART_OUT=""
  if ! RECOVER_RESTART_OUT="$(systemctl --user restart openclaw-gateway.service 2>&1)"; then
    MSG="⚠️ OpenClaw maintenance failed at RECOVERY RESTART step (UTC $TS).\n\nRecovery reinstall succeeded, but restart failed.\n\nRestart output:\n$RECOVER_RESTART_OUT\n\nSuggested fixes:\n- Check service status: systemctl --user status openclaw-gateway.service\n- Retry restart: systemctl --user restart openclaw-gateway.service"
    send_report "$MSG"
    exit 4
  fi

  FINAL_HEALTH_OUT=""
  if ! FINAL_HEALTH_OUT="$(wait_for_health_gate "post-recovery" 2>&1)"; then
    MSG="⚠️ OpenClaw maintenance failed after recovery (UTC $TS).\n\nPost-recovery health gate still failing.\n\nOutput:\n$FINAL_HEALTH_OUT\n\nSuggested fixes:\n$suggestions_common"
    send_report "$MSG"
    exit 5
  fi

  log "Recovery reinstall succeeded and health gate passed."
fi

if ! SECURITY_AUDIT_SUMMARY="$(security_audit 2>&1)"; then
  MSG="⚠️ OpenClaw maintenance failed at SECURITY AUDIT step (UTC $TS).\n\nSecurity audit output:\n$SECURITY_AUDIT_SUMMARY\n\nSuggested fixes:\n$suggestions_common\n- Review the security findings and remediate plaintext secrets or insecure flags\n- Re-run the daily maintenance script after the security issues are addressed"
  send_report "$MSG"
  exit 6
fi

MSG="✅ OpenClaw daily maintenance complete (UTC $TS).\n\nUpdated: core package + gateway + installed plugins/skills sync (via openclaw update).\nChannel: $UPDATE_CHANNEL\nVersion: before=$BEFORE_VER -> target=$UPDATE_TARGET -> after=$AFTER_VER\nActions: $UPDATE_ACTIONS\nGateway restart: success\nUpdate status: $STATUS_LINE\nLog: $RUN_LOG"
MSG="$MSG\n\nSecurity audit:\n$SECURITY_AUDIT_SUMMARY"

send_report "$MSG"
log "Maintenance complete"
exit 0
