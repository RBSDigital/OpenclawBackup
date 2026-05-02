#!/usr/bin/env bash
set -uo pipefail

OPENCLAW_BIN="${OPENCLAW_BIN:-$HOME/.npm-global/bin/openclaw}"
if [ ! -x "$OPENCLAW_BIN" ]; then
  OPENCLAW_BIN="$(command -v openclaw 2>/dev/null || true)"
fi
if [ -z "$OPENCLAW_BIN" ] || [ ! -x "$OPENCLAW_BIN" ]; then
  echo "openclaw binary not found" >&2
  exit 127
fi

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

log "Starting daily OpenClaw maintenance"
BEFORE_VER="$("$OPENCLAW_BIN" --version 2>&1 || true)"
log "Before version: $BEFORE_VER"

UPDATE_JSON_RAW=""
UPDATE_MODE="openclaw-update"
if ! UPDATE_JSON_RAW="$("$OPENCLAW_BIN" update --yes --no-restart --json 2>&1)"; then
  if echo "$UPDATE_JSON_RAW" | grep -qi 'cannot run from inside the gateway service process'; then
    log "openclaw update blocked in service context; falling back to npm global reinstall"
    UPDATE_MODE="npm-fallback"
    if ! UPDATE_JSON_RAW="$(npm i -g openclaw@latest --no-fund --no-audit --loglevel=error 2>&1)"; then
      MSG="⚠️ OpenClaw daily maintenance failed at UPDATE step (UTC $TS).\n\nError:\n$UPDATE_JSON_RAW\n\nCurrent version: $BEFORE_VER\n\nSuggested fixes:\n$suggestions_common\n- Retry install manually: npm i -g openclaw@latest"
      send_report "$MSG"
      exit 1
    fi
  else
    MSG="⚠️ OpenClaw daily maintenance failed at UPDATE step (UTC $TS).\n\nError:\n$UPDATE_JSON_RAW\n\nCurrent version: $BEFORE_VER\n\nSuggested fixes:\n$suggestions_common\n- Retry update manually: openclaw update --yes"
    send_report "$MSG"
    exit 1
  fi
fi

echo "$UPDATE_JSON_RAW" >> "$RUN_LOG"

if [ "$UPDATE_MODE" = "openclaw-update" ]; then
  PARSED="$(node -e '
let s=""; process.stdin.on("data",d=>s+=d).on("end",()=>{
  try {
    const j=JSON.parse(s);
    const actions=(j.actions||[]).join("; ");
    const out=[
      j.currentVersion||"unknown",
      j.targetVersion||"unknown",
      j.effectiveChannel||"unknown",
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

# Post-update health gate (catches broken module/link states)
HEALTH_OUT=""
if ! HEALTH_OUT="$("$OPENCLAW_BIN" --version 2>&1; "$OPENCLAW_BIN" status 2>&1)"; then
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
  if ! FINAL_HEALTH_OUT="$("$OPENCLAW_BIN" --version 2>&1; "$OPENCLAW_BIN" status 2>&1)"; then
    MSG="⚠️ OpenClaw maintenance failed after recovery (UTC $TS).\n\nPost-recovery health gate still failing.\n\nOutput:\n$FINAL_HEALTH_OUT\n\nSuggested fixes:\n$suggestions_common"
    send_report "$MSG"
    exit 5
  fi

  log "Recovery reinstall succeeded and health gate passed."
fi

MSG="✅ OpenClaw daily maintenance complete (UTC $TS).\n\nUpdated: core package + gateway + installed plugins/skills sync (via openclaw update).\nChannel: $UPDATE_CHANNEL\nVersion: before=$BEFORE_VER -> target=$UPDATE_TARGET -> after=$AFTER_VER\nActions: $UPDATE_ACTIONS\nGateway restart: success\nUpdate status: $STATUS_LINE\nLog: $RUN_LOG"

send_report "$MSG"
log "Maintenance complete"
exit 0
