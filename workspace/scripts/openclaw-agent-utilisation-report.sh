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
LOG_DIR="${LOG_DIR:-$HOME/.openclaw/logs}"
WORKSPACES_DIR="${WORKSPACES_DIR:-$HOME/.openclaw/workspaces}"
AGENTS_DIR="${AGENTS_DIR:-$HOME/.openclaw/agents}"
mkdir -p "$LOG_DIR"

TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
DATE_UTC="$(date -u +%F)"
RUN_LOG="$LOG_DIR/agent-utilisation-$TS.log"

log(){ echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$RUN_LOG" >&2; }

send_mail(){
  local subject="$1" body="$2"
  if [ -z "$GOG_BIN" ]; then log "gog not installed; cannot email report"; return 1; fi
  "$GOG_BIN" gmail send --account "$GOG_ACCOUNT" --to "$REPORT_EMAIL" --subject "$subject" --body "$body" >>"$RUN_LOG" 2>&1
}

capture(){
  local label="$1"; shift
  local out rc
  set +e
  out="$(timeout 30 "$@" 2>&1)"
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

agent_summary_json(){
  node <<'NODE'
const fs = require('fs');
const path = require('path');

const home = process.env.HOME;
const workspacesDir = process.env.WORKSPACES_DIR;
const agentsDir = process.env.AGENTS_DIR;
const now = Date.now();

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
  } catch { return 0; }
}
function sessionInfo(agent) {
  const p = path.join(agentsDir, agent, 'sessions', 'sessions.json');
  let j;
  try { j = JSON.parse(read(p) || '{}'); } catch { return { count: 0, aborted: 0, maxTokens: 0, highContext: [] }; }
  const sessions = Array.isArray(j.sessions)
    ? j.sessions
    : (j.sessions && typeof j.sessions === 'object' ? Object.values(j.sessions) : Object.values(j || {}));
  const highContext = [];
  let maxUpdated = 0, maxTokens = 0, aborted = 0;
  for (const s of sessions) {
    const updated = Number(s.updatedAt || 0);
    const total = Number(s.totalTokens || 0);
    const context = Number(s.contextTokens || 0);
    maxUpdated = Math.max(maxUpdated, updated);
    maxTokens = Math.max(maxTokens, total);
    if (s.abortedLastRun) aborted++;
    if (context && total / context >= 0.70) {
      highContext.push({ key: [REDACTED_SECRET] || s.sessionId || 'unknown', total, context });
    }
  }
  return {
    count: sessions.length,
    aborted,
    maxTokens,
    lastActiveHours: maxUpdated ? Math.round((now - maxUpdated) / 36e5) : null,
    highContext,
  };
}

const agents = fs.existsSync(workspacesDir)
  ? fs.readdirSync(workspacesDir).filter(a => fs.existsSync(path.join(workspacesDir, a, 'AGENTS.md'))).sort()
  : [];

const rows = agents.map(agent => {
  const root = path.join(workspacesDir, agent);
  const identity = read(path.join(root, 'IDENTITY.md')).split('\n').find(l => /Name:|Vibe:/.test(l)) || '';
  const heartbeat = read(path.join(root, 'HEARTBEAT.md'));
  const memoryDir = path.join(root, 'memory');
  const memNewest = newestMtime(memoryDir);
  const sess = sessionInfo(agent);
  return {
    agent,
    identity: identity.replace(/^[-#*\s]*/, '').trim(),
    hasSoul: fs.existsSync(path.join(root, 'SOUL.md')),
    hasRoutingNotes: /#|bot|owns|route|lane|status|check/i.test(read(path.join(root, 'TOOLS.md')) + '\n' + read(path.join(root, 'SOUL.md'))),
    heartbeatLines: heartbeat.split('\n').filter(l => l.trim() && !l.trim().startsWith('#')).length,
    memoryFiles: fs.existsSync(memoryDir) ? fs.readdirSync(memoryDir).filter(f => /^\d{4}-\d{2}-\d{2}\.md$/.test(f)).length : 0,
    memoryAgeHours: memNewest ? Math.round((now - memNewest) / 36e5) : null,
    sessions: sess,
  };
});

console.log(JSON.stringify(rows, null, 2));
NODE
}

build_report(){
  local timers maintenance_status backup_status health_status config_status cron_status skills_status agent_json latest_maintenance latest_backup openclaw_perm

  log "Building agent utilisation and efficiency report"
  timers="$(systemctl --user list-timers --all 'openclaw*' 2>&1 || true)"
  latest_maintenance="$(latest_file 'maintenance-*.log')"
  latest_backup="$(latest_file 'github-backup-*.log')"
  openclaw_perm="$(stat -c '%a' "$HOME/.openclaw" 2>/dev/null || echo unknown)"

  if [ -n "$latest_maintenance" ]; then
    maintenance_status="$(tail -n 12 "$latest_maintenance" 2>/dev/null || true)"
  else
    maintenance_status="No maintenance log found."
  fi
  if [ -n "$latest_backup" ]; then
    backup_status="$(tail -n 12 "$latest_backup" 2>/dev/null || true)"
  else
    backup_status="No backup log found."
  fi

  set +e
  health_status="$(capture "openclaw health" "$OPENCLAW_BIN" health --json)"
  health_rc=$?
  config_status="$(capture "openclaw config validate" "$OPENCLAW_BIN" config validate --json)"
  config_rc=$?
  cron_status="$(capture "openclaw cron list" "$OPENCLAW_BIN" cron list --json)"
  cron_rc=$?
  skills_status="$(capture "openclaw skills list" "$OPENCLAW_BIN" skills list --json)"
  skills_rc=$?
  set -e

  agent_json="$(WORKSPACES_DIR="$WORKSPACES_DIR" AGENTS_DIR="$AGENTS_DIR" agent_summary_json)"

  HEALTH_RC="$health_rc" CONFIG_RC="$config_rc" CRON_RC="$cron_rc" SKILLS_RC="$skills_rc" \
  OPENCLAW_PERM="$openclaw_perm" AGENT_JSON="$agent_json" TIMERS="$timers" \
  MAINTENANCE_STATUS="$maintenance_status" BACKUP_STATUS="$backup_status" \
  HEALTH_STATUS="$health_status" CONFIG_STATUS="$config_status" CRON_STATUS="$cron_status" SKILLS_STATUS="$skills_status" \
  node <<'NODE'
const agents = JSON.parse(process.env.AGENT_JSON || '[]');
const recs = [];
const owners = new Map();
function add(owner, text) {
  recs.push({ owner, text });
  if (!owners.has(owner)) owners.set(owner, []);
  owners.get(owner).push(text);
}

if (process.env.HEALTH_RC !== '0') add('ops-bot', 'OpenClaw health check is failing or cannot reach the gateway; investigate gateway bind/transport before relying on scheduler-driven coordination.');
if (process.env.CRON_RC !== '0') add('ops-bot', 'OpenClaw cron list failed; verify gateway scheduler access and include cron health in backup/maintenance checks.');
if (process.env.CONFIG_RC !== '0') add('admin-bot', 'Config validation failed; preview any config repair before applying changes.');
if (process.env.OPENCLAW_PERM !== '700') add('admin-bot', `~/.openclaw permissions are ${process.env.OPENCLAW_PERM}; tighten to 700 after reviewing service access.`);

for (const a of agents) {
  if (!a.hasSoul) add('manager-bot', `${a.agent}: missing SOUL.md, so routing/personality boundaries are weak.`);
  if (a.heartbeatLines === 0) add(a.agent, `${a.agent}: HEARTBEAT.md has no active routine checks; add 2-4 lightweight checks appropriate to the lane.`);
  if (a.memoryFiles === 0) add(a.agent, `${a.agent}: no daily memory files found; start writing notable operational decisions and lessons.`);
  if (a.memoryAgeHours !== null && a.memoryAgeHours > 168) add(a.agent, `${a.agent}: memory has not been updated in ${a.memoryAgeHours}h; review recent work and capture durable lessons.`);
  if (a.sessions.aborted > 0) add(a.agent, `${a.agent}: ${a.sessions.aborted} session(s) show abortedLastRun; inspect whether work was interrupted or stuck.`);
  for (const s of a.sessions.highContext || []) add(a.agent, `${a.agent}: session near context pressure (${s.total}/${s.context} tokens); summarize/archive before further long work.`);
}

if (!recs.some(r => r.owner === 'ops-bot')) add('ops-bot', 'Continue daily maintenance/backup checks and explicitly verify the new utilisation report timer is firing after backup.');

const lines = [];
lines.push(`OpenClaw utilisation and efficiency report (${new Date().toISOString().slice(0,10)} UTC)`);
lines.push('');
lines.push('Executive status');
lines.push(`- Agents found: ${agents.length}`);
lines.push(`- OpenClaw dir permissions: ${process.env.OPENCLAW_PERM}`);
lines.push(`- health rc=${process.env.HEALTH_RC}, config rc=${process.env.CONFIG_RC}, cron rc=${process.env.CRON_RC}, skills rc=${process.env.SKILLS_RC}`);
lines.push('');
lines.push('Agent utilisation');
for (const a of agents) {
  const memAge = a.memoryAgeHours === null ? 'none' : `${a.memoryAgeHours}h`;
  const active = a.sessions.lastActiveHours === null ? 'none' : `${a.sessions.lastActiveHours}h`;
  lines.push(`- ${a.agent}: sessions=${a.sessions.count}, lastActive=${active}, maxTokens=${a.sessions.maxTokens}, memoryAge=${memAge}, heartbeatItems=${a.heartbeatLines}`);
}
lines.push('');
lines.push('Routine health');
lines.push('Timers:');
lines.push(process.env.TIMERS.trim() || 'No timer output.');
lines.push('');
lines.push('Latest maintenance log tail:');
lines.push(process.env.MAINTENANCE_STATUS.trim());
lines.push('');
lines.push('Latest backup log tail:');
lines.push(process.env.BACKUP_STATUS.trim());
lines.push('');
lines.push('Recommended actions by owner');
for (const [owner, items] of owners.entries()) {
  lines.push(`- ${owner}:`);
  for (const item of items.slice(0, 6)) lines.push(`  - ${item}`);
}
if (owners.size === 0) lines.push('- No immediate action needed.');
lines.push('');
lines.push('Continuous improvement prompts for tomorrow');
lines.push('- Identify one repeated manual workflow per active agent and decide whether it should become a skill, script, or routing note.');
lines.push('- Check whether backup and maintenance reports include enough detail to recover without reading full logs.');
lines.push('- Confirm any recommended admin/security changes are routed for preview before execution.');
lines.push('');
lines.push(`Full run log: ${process.env.RUN_LOG || 'see ~/.openclaw/logs/agent-utilisation-*'}`);
console.log(lines.join('\n'));
NODE
}

REPORT_BODY="$(RUN_LOG="$RUN_LOG" build_report)"
SUBJECT="OpenClaw utilisation & efficiency report ($DATE_UTC)"

if send_mail "$SUBJECT" "$REPORT_BODY"; then
  log "Sent utilisation report to $REPORT_EMAIL"
else
  log "FAILED to send utilisation report to $REPORT_EMAIL"
  printf '%s\n' "$REPORT_BODY" >>"$RUN_LOG"
  exit 1
fi

printf '%s\n' "$REPORT_BODY" >>"$RUN_LOG"
exit 0
