#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_BIN="${OPENCLAW_BIN:-$HOME/.npm-global/bin/openclaw}"
export OPENCLAW_CONFIG_PATH="${OPENCLAW_CONFIG_PATH:-$HOME/.openclaw/openclaw.json}"
[ -x "$OPENCLAW_BIN" ] || OPENCLAW_BIN="$(command -v openclaw || true)"
[ -x "$OPENCLAW_BIN" ] || { echo "ERROR: openclaw binary not found"; exit 127; }

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

GOG_BIN="${GOG_BIN:-$(command -v gog || true)}"
REPORT_EMAIL="${REPORT_EMAIL:-vrbs940054@gmail.com}"
GOG_ACCOUNT="${GOG_ACCOUNT:-vrbs940054@gmail.com}"
CI_NOTIFY="${CI_NOTIFY:-1}"
LOG_DIR="${LOG_DIR:-$HOME/.openclaw/logs}"
WORKSPACES_DIR="${WORKSPACES_DIR:-$HOME/.openclaw/workspaces}"
AGENTS_DIR="${AGENTS_DIR:-$HOME/.openclaw/agents}"
STATE_PATH="${STATE_PATH:-$WORKSPACES_DIR/manager-bot/memory/ci-manager-state.json}"
mkdir -p "$LOG_DIR" "$(dirname "$STATE_PATH")"

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DATE_UTC="$(date -u +%F)"
RUN_LOG="$LOG_DIR/ci-manager-$TS.log"
DISCOVERY_PATH="$LOG_DIR/ci-manager-discovery-$TS.json"

log(){ echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$RUN_LOG" >&2; }

send_mail(){
  local subject="$1" body="$2"
  if [ "$CI_NOTIFY" != "1" ]; then log "CI_NOTIFY=$CI_NOTIFY; skipped email"; return 0; fi
  if [ -z "$GOG_BIN" ]; then log "gog not installed; cannot email report"; return 1; fi
  "$GOG_BIN" gmail send --account "$GOG_ACCOUNT" --to "$REPORT_EMAIL" --subject "$subject" --body "$body" >>"$RUN_LOG" 2>&1
}

capture(){
  local label="$1"; shift
  local out rc
  set +e
  out="$(timeout 45 "$@" 2>&1)"
  rc=$?
  set -e
  printf '### %s (rc=%s)\n%s\n\n' "$label" "$rc" "$out" >>"$RUN_LOG"
  printf '%s' "$out"
  return "$rc"
}

latest_file(){
  local pattern="$1"
  find "$LOG_DIR" -maxdepth 1 -type f -name "$pattern" -printf '%T@ %p\n' 2>/dev/null | sort -nr | sed -n '1s/^[^ ]* //p'
}

collect_json(){
  TIMERS="$TIMERS" UNITS="$UNITS" DISK="$DISK" DU_SUMMARY="$DU_SUMMARY" \
  DELIVERY_JSON="$DELIVERY_JSON" AGENT_JSON="$AGENT_JSON" \
  HEALTH_RC="$HEALTH_RC" CONFIG_RC="$CONFIG_RC" CRON_RC="$CRON_RC" \
  HEALTH_STATUS="$HEALTH_STATUS" CONFIG_STATUS="$CONFIG_STATUS" CRON_STATUS="$CRON_STATUS" \
  LATEST_MAINTENANCE="$LATEST_MAINTENANCE" LATEST_BACKUP="$LATEST_BACKUP" \
  MAINTENANCE_TAIL="$MAINTENANCE_TAIL" BACKUP_TAIL="$BACKUP_TAIL" \
  BINDINGS="$BINDINGS" STATE_PATH="$STATE_PATH" RUN_LOG="$RUN_LOG" DISCOVERY_PATH="$DISCOVERY_PATH" \
  node <<'NODE'
const fs = require('fs');
const path = require('path');

function parseJson(s, fallback) {
  try { return JSON.parse(s || ''); } catch { return fallback; }
}
function read(p) {
  try { return fs.readFileSync(p, 'utf8'); } catch { return ''; }
}
function stat(p) {
  try { return fs.statSync(p); } catch { return null; }
}
function newestMtime(dir) {
  try {
    return fs.readdirSync(dir)
      .map(f => stat(path.join(dir, f)))
      .filter(Boolean)
      .reduce((m, s) => Math.max(m, s.mtimeMs), 0);
  } catch {
    return 0;
  }
}

const workspacesDir = process.env.WORKSPACES_DIR || path.join(process.env.HOME, '.openclaw/workspaces');
const agentsDir = process.env.AGENTS_DIR || path.join(process.env.HOME, '.openclaw/agents');
const now = Date.now();

const agents = fs.existsSync(workspacesDir)
  ? fs.readdirSync(workspacesDir).filter(a => fs.existsSync(path.join(workspacesDir, a, 'AGENTS.md'))).sort()
  : [];

const agentRows = agents.map(agent => {
  const root = path.join(workspacesDir, agent);
  const sessionsDir = path.join(agentsDir, agent, 'sessions');
  const sessionFiles = fs.existsSync(sessionsDir)
    ? fs.readdirSync(sessionsDir).filter(f => /\.jsonl$/.test(f))
    : [];
  const lastSessionMtime = sessionFiles.reduce((max, f) => {
    const s = stat(path.join(sessionsDir, f));
    return s ? Math.max(max, s.mtimeMs) : max;
  }, 0);
  const memNewest = newestMtime(path.join(root, 'memory'));
  const heartbeat = read(path.join(root, 'HEARTBEAT.md'));
  const tools = read(path.join(root, 'TOOLS.md'));
  const soul = read(path.join(root, 'SOUL.md'));
  return {
    agent,
    hasSoul: Boolean(soul.trim()),
    hasTools: Boolean(tools.trim()),
    heartbeatItems: heartbeat.split('\n').filter(l => l.trim() && !l.trim().startsWith('#') && !l.trim().startsWith('```')).length,
    memoryAgeHours: memNewest ? Math.round((now - memNewest) / 36e5) : null,
    sessionFiles: sessionFiles.length,
    lastSessionHours: lastSessionMtime ? Math.round((now - lastSessionMtime) / 36e5) : null,
  };
});

const delivery = parseJson(process.env.DELIVERY_JSON, { failedCount: 0, oldestFailed: null, files: [] });
const findings = [];
function add(severity, owner, summary, nextAction) {
  const id = 'ci-' + new Date().toISOString().slice(0, 10) + '-' + String(findings.length + 1).padStart(3, '0');
  findings.push({ id, severity, owner, summary, firstSeenAt: new Date().toISOString(), lastSeenAt: new Date().toISOString(), status: 'open', nextAction });
}

if (process.env.HEALTH_RC !== '0') add('P0', 'ops-bot', 'OpenClaw health check failed or timed out.', 'Inspect gateway transport and recent maintenance logs.');
if (process.env.CONFIG_RC !== '0') add('P0', 'admin-bot', 'OpenClaw config validation failed.', 'Preview config repair before applying changes.');
if (process.env.CRON_RC !== '0') add('P1', 'ops-bot', 'OpenClaw cron list failed.', 'Verify scheduler access and gateway auth path.');
if (delivery.failedCount > 0) add('P1', 'ops-bot', `${delivery.failedCount} failed delivery queue item(s) exist.`, 'Inspect failed delivery targets and clear only after confirming no retry loop.');
if (/visibility is restricted|tools\.sessions\.visibility|agentId is not allowed/i.test(read(process.env.RUN_LOG))) {
  add('P1', 'ops-bot', 'Cross-agent handoff is blocked by session visibility or spawn policy.', 'Preview the least-privilege config change or document direct-channel handoff as the operating pattern.');
}
for (const a of agentRows) {
  if (!a.hasSoul) add('P1', 'manager-bot', `${a.agent} has no SOUL.md content.`, 'Restore lane identity before routing work there.');
  if (a.heartbeatItems === 0) add('P2', a.agent, `${a.agent} has no active heartbeat checklist items.`, 'Add lightweight lane-specific routine checks if the lane needs proactive monitoring.');
  if (a.memoryAgeHours !== null && a.memoryAgeHours > 168) add('P2', a.agent, `${a.agent} memory is stale at ${a.memoryAgeHours}h.`, 'Review recent work and capture durable lessons.');
}

const overall = findings.some(f => f.severity === 'P0') ? 'Blocked' : findings.some(f => f.severity === 'P1') ? 'Attention' : 'OK';
const state = {
  lastRunAt: new Date().toISOString(),
  lastReportPath: process.env.RUN_LOG,
  discoveryPath: process.env.DISCOVERY_PATH,
  openFindings: findings,
  quietFindings: [],
};
fs.writeFileSync(process.env.STATE_PATH, JSON.stringify(state, null, 2) + '\n');

const discovery = {
  generatedAt: new Date().toISOString(),
  timers: process.env.TIMERS,
  units: process.env.UNITS,
  latestMaintenance: process.env.LATEST_MAINTENANCE || null,
  latestBackup: process.env.LATEST_BACKUP || null,
  bindings: process.env.BINDINGS,
  delivery,
  agents: agentRows,
};
fs.writeFileSync(process.env.DISCOVERY_PATH, JSON.stringify(discovery, null, 2) + '\n');

const bySeverity = { P0: [], P1: [], P2: [] };
for (const f of findings) bySeverity[f.severity]?.push(f);

const lines = [];
lines.push(`OpenClaw CI Manager Report (${new Date().toISOString().slice(0, 10)} UTC)`);
lines.push('');
lines.push('Executive status');
lines.push(`- Overall: ${overall}`);
lines.push(`- Checks run: health, config validate, cron list, timers, units, disk, backup log, maintenance log, delivery queue, agent bindings`);
lines.push(`- New findings: ${findings.length}`);
lines.push(`- Human action required: ${bySeverity.P0.length ? 'yes, P0 finding present' : 'no immediate action'}`);
lines.push('');
lines.push('Infrastructure utilisation');
lines.push('- Disk:');
lines.push((process.env.DISK || 'No disk output.').trim());
lines.push('- OpenClaw storage summary:');
lines.push((process.env.DU_SUMMARY || 'No storage summary.').trim());
lines.push('');
lines.push('Routine health');
lines.push('- Timers:');
lines.push((process.env.TIMERS || 'No timer output.').trim());
lines.push('- Latest maintenance tail:');
lines.push((process.env.MAINTENANCE_TAIL || 'No maintenance log found.').trim());
lines.push('- Latest backup tail:');
lines.push((process.env.BACKUP_TAIL || 'No backup log found.').trim());
lines.push('');
lines.push('Agent and workflow health');
for (const a of agentRows) {
  const mem = a.memoryAgeHours === null ? 'none' : `${a.memoryAgeHours}h`;
  const sess = a.lastSessionHours === null ? 'none' : `${a.lastSessionHours}h`;
  lines.push(`- ${a.agent}: sessionFiles=${a.sessionFiles}, lastSession=${sess}, memoryAge=${mem}, heartbeatItems=${a.heartbeatItems}`);
}
lines.push('');
lines.push('Recommendations');
for (const sev of ['P0', 'P1', 'P2']) {
  lines.push(`- ${sev}:`);
  const rows = bySeverity[sev];
  if (!rows.length) lines.push('  - none');
  for (const f of rows.slice(0, 8)) lines.push(`  - ${f.owner}: ${f.summary} Next: ${f.nextAction}`);
}
lines.push('');
lines.push('Evidence');
lines.push(`- Report log: ${process.env.RUN_LOG}`);
lines.push(`- Discovery artifact: ${process.env.DISCOVERY_PATH}`);
lines.push(`- State file: ${process.env.STATE_PATH}`);
console.log(lines.join('\n'));
NODE
}

log "Starting OpenClaw CI Manager discovery"

TIMERS="$(systemctl --user list-timers --all 'openclaw*' --no-pager 2>&1 || true)"
UNITS="$(systemctl --user list-unit-files 'openclaw*' --no-pager 2>&1 || true)"
DISK="$(df -h "$HOME" "$HOME/.openclaw" 2>&1 || true)"
DU_SUMMARY="$(du -sh "$HOME/.openclaw/logs" "$HOME/.openclaw/workspaces" "$HOME/.openclaw/agents" "$HOME/.openclaw/backups" "$HOME/.openclaw/media" 2>/dev/null || true)"
LATEST_MAINTENANCE="$(latest_file 'maintenance-*.log')"
LATEST_BACKUP="$(latest_file 'github-backup-*.log')"
MAINTENANCE_TAIL="$([ -n "$LATEST_MAINTENANCE" ] && tail -n 12 "$LATEST_MAINTENANCE" 2>/dev/null || true)"
BACKUP_TAIL="$([ -n "$LATEST_BACKUP" ] && tail -n 12 "$LATEST_BACKUP" 2>/dev/null || true)"
BINDINGS="$(capture "openclaw agents bindings" "$OPENCLAW_BIN" agents bindings || true)"

DELIVERY_JSON="$(python3 - <<'PY'
import sqlite3, json, os
db_path = os.path.expanduser('~/.openclaw/state/openclaw.sqlite')
res = {"failedCount": 0, "oldestFailed": None, "files": []}
if os.path.exists(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT id, enqueued_at, last_error, target, channel FROM delivery_queue_entries WHERE status='failed' ORDER BY enqueued_at ASC")
        rows = cursor.fetchall()
        failed_count = len(rows)
        files = []
        for r in rows[:10]:
            files.append({
                "file": f"db_entry:{r[0]}",
                "enqueuedAt": r[1],
                "lastError": r[2],
                "to": r[3],
                "channel": r[4]
            })
        oldest = None
        if rows:
            oldest = {
                "file": f"db_entry:{rows[0][0]}",
                "enqueuedAt": rows[0][1],
                "lastError": rows[0][2],
                "to": rows[0][3],
                "channel": rows[0][4]
            }
        res = {"failedCount": failed_count, "oldestFailed": oldest, "files": files}
    except Exception as e:
        pass
print(json.dumps(res))
PY
)"

set +e
HEALTH_STATUS="$(capture "openclaw health" "$OPENCLAW_BIN" health --json)"
HEALTH_RC=$?
CONFIG_STATUS="$(capture "openclaw config validate" "$OPENCLAW_BIN" config validate --json)"
CONFIG_RC=$?
CRON_STATUS="$(capture "openclaw cron list" "$OPENCLAW_BIN" cron list --json)"
CRON_RC=$?
set -e

AGENT_JSON="[]"
REPORT_BODY="$(WORKSPACES_DIR="$WORKSPACES_DIR" AGENTS_DIR="$AGENTS_DIR" collect_json)"
SUBJECT="OpenClaw CI Manager report ($DATE_UTC)"

if send_mail "$SUBJECT" "$REPORT_BODY"; then
  log "CI Manager report delivered or notification skipped"
else
  log "FAILED to deliver CI Manager report"
  printf '%s\n' "$REPORT_BODY" >>"$RUN_LOG"
  exit 1
fi

printf '%s\n' "$REPORT_BODY" >>"$RUN_LOG"
log "CI Manager complete"
exit 0
