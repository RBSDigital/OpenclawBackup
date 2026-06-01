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
BACKUP_REPO_URL="${BACKUP_REPO_URL:-}"
BACKUP_REPO_BRANCH="${BACKUP_REPO_BRANCH:-main}"
BACKUP_WORKDIR="${BACKUP_WORKDIR:-$HOME/.openclaw/backups/agent-backup-repo}"
STAGING_DIR="${STAGING_DIR:-$HOME/.openclaw/backups/staging}"
LOG_DIR="${LOG_DIR:-$HOME/.openclaw/logs}"
GIT_AUTHOR_NAME="${GIT_AUTHOR_NAME:-OpenClaw Backup Bot}"
GIT_AUTHOR_EMAIL="${GIT_AUTHOR_EMAIL:-openclaw-backup@local}"
mkdir -p "$LOG_DIR" "$STAGING_DIR"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
RUN_LOG="$LOG_DIR/github-backup-$TS.log"

log(){ echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$RUN_LOG"; }

send_mail(){
  local subject="$1"; local body="$2"
  if [ -z "$GOG_BIN" ]; then log "gog not installed; cannot email report"; return 1; fi
  "$GOG_BIN" gmail send --account "$GOG_ACCOUNT" --to "$REPORT_EMAIL" --subject "$subject" --body "$body" >>"$RUN_LOG" 2>&1 || return 1
}

fail(){
  local why="$1"
  log "ERROR: $why"
  send_mail "OpenClaw backup FAILED ($TS)" "Backup failed: $why" || true
  exit 1
}

WARNINGS=()

capture_openclaw_json(){
  local label="$1" output="$2"; shift 2
  local err_file="${output%.json}.error.txt"
  if "$OPENCLAW_BIN" "$@" > "$output" 2>"$err_file"; then
    rm -f "$err_file"
    return 0
  fi
  WARNINGS+=("$label failed; see ${err_file#$STAGING_DIR/}")
  printf '{"ok":false,"error":"%s command failed; see sibling .error.txt"}\n' "$label" > "$output"
  log "WARNING: $label failed; continuing backup with diagnostic artifact"
  return 0
}

[ -n "$BACKUP_REPO_URL" ] || fail "BACKUP_REPO_URL is not set (expected private GitHub repo URL)"

# Clone/init backup repo
if [ ! -d "$BACKUP_WORKDIR/.git" ]; then
  rm -rf "$BACKUP_WORKDIR"
  git clone "$BACKUP_REPO_URL" "$BACKUP_WORKDIR" >>"$RUN_LOG" 2>&1 || fail "git clone failed for $BACKUP_REPO_URL"
fi

cd "$BACKUP_WORKDIR"
git fetch origin >>"$RUN_LOG" 2>&1 || fail "git fetch failed"
if git show-ref --verify --quiet "refs/heads/$BACKUP_REPO_BRANCH"; then
  git checkout "$BACKUP_REPO_BRANCH" >>"$RUN_LOG" 2>&1 || fail "checkout branch failed"
else
  git checkout -b "$BACKUP_REPO_BRANCH" >>"$RUN_LOG" 2>&1 || fail "create branch failed"
fi
if git ls-remote --exit-code --heads origin "$BACKUP_REPO_BRANCH" >>"$RUN_LOG" 2>&1; then
  git pull --rebase origin "$BACKUP_REPO_BRANCH" >>"$RUN_LOG" 2>&1 || fail "git pull failed"
else
  log "Remote branch $BACKUP_REPO_BRANCH does not exist yet (new/empty repo)"
fi

rm -rf "$STAGING_DIR"/*
mkdir -p "$STAGING_DIR"

# Collect critical files. Agent workspaces intentionally include private MEMORY.md
# files because this is a private, redacted recovery snapshot. Reinstallable
# toolchains, caches, databases, and generated sandboxes are excluded.
mkdir -p "$STAGING_DIR/workspace" "$STAGING_DIR/workspaces" "$STAGING_DIR/agent-memory-vault" "$STAGING_DIR/systemd-user" "$STAGING_DIR/openclaw" "$STAGING_DIR/openclaw/agents-main" "$STAGING_DIR/openclaw/acpx" "$STAGING_DIR/openclaw/logs"
rsync -a --delete --exclude '.git' /home/vin/.openclaw/workspace/ "$STAGING_DIR/workspace/" >>"$RUN_LOG" 2>&1 || fail "rsync workspace failed"
rsync -a --delete \
  --max-size='20m' \
  --exclude '.git/' \
  --exclude '.venv/' \
  --exclude '__pycache__/' \
  --exclude 'node_modules/' \
  --exclude '.local-tools/' \
  --exclude 'apt-cache/' \
  --exclude 'apt-extract/' \
  --exclude 'clamav-db/' \
  --exclude 'clamav-run/' \
  --exclude 'sandboxes/' \
  /home/vin/.openclaw/workspaces/ "$STAGING_DIR/workspaces/" >>"$RUN_LOG" 2>&1 || fail "rsync agent workspaces failed"
rsync -a --delete \
  /home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault/ \
  "$STAGING_DIR/agent-memory-vault/" >>"$RUN_LOG" 2>&1 || fail "rsync shared Agent Memory Vault failed"
cp -a ~/.config/systemd/user/openclaw* "$STAGING_DIR/systemd-user/" 2>/dev/null || true
cp -a ~/.config/systemd/user/qmd-knowledgebase-index.* "$STAGING_DIR/systemd-user/" 2>/dev/null || true
cp -a ~/.config/systemd/user/*.service.d "$STAGING_DIR/systemd-user/" 2>/dev/null || true
cp -a ~/.openclaw/cron "$STAGING_DIR/openclaw/" 2>/dev/null || true
cp -a ~/.openclaw/memory "$STAGING_DIR/openclaw/" 2>/dev/null || true
cp -a ~/.openclaw/skills "$STAGING_DIR/openclaw/" 2>/dev/null || true
cp -a ~/.openclaw/openclaw.json "$STAGING_DIR/openclaw/openclaw.json" 2>/dev/null || true
cp -a ~/.openclaw/config.json "$STAGING_DIR/openclaw/config.json" 2>/dev/null || true
cp -a ~/.openclaw/devices "$STAGING_DIR/openclaw/" 2>/dev/null || true
cp -a ~/.openclaw/credentials "$STAGING_DIR/openclaw/" 2>/dev/null || true
cp -a ~/.openclaw/agents/main/agent/models.json "$STAGING_DIR/openclaw/agents-main/" 2>/dev/null || true
cp -a ~/.openclaw/agents/main/agent/auth-profiles.json "$STAGING_DIR/openclaw/agents-main/" 2>/dev/null || true
cp -a ~/.openclaw/acpx/codex-home/config.toml "$STAGING_DIR/openclaw/acpx/" 2>/dev/null || true
cp -a ~/.openclaw/logs/config-health.json "$STAGING_DIR/openclaw/logs/" 2>/dev/null || true
tail -n 200 ~/.openclaw/logs/config-audit.jsonl > "$STAGING_DIR/openclaw/logs/config-audit-tail.jsonl" 2>/dev/null || true

capture_openclaw_json "openclaw cron list" "$STAGING_DIR/openclaw/cron-list.json" cron list --json
capture_openclaw_json "openclaw skills list" "$STAGING_DIR/openclaw/skills-list.json" skills list --json
capture_openclaw_json "openclaw plugins list" "$STAGING_DIR/openclaw/plugins-list.json" plugins list --json
capture_openclaw_json "openclaw config validate" "$STAGING_DIR/openclaw/config-validate.json" config validate --json
capture_openclaw_json "openclaw health" "$STAGING_DIR/openclaw/health.json" health --json

OPENCLAW_CONFIG_PATH="$OPENCLAW_CONFIG_PATH" STAGING_DIR="$STAGING_DIR" node <<'NODE'
const fs = require('fs');
const path = require('path');

const home = process.env.HOME;
const configPath = process.env.OPENCLAW_CONFIG_PATH;
const stagingDir = process.env.STAGING_DIR;
const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
const configuredAgents = (config.agents?.list || []).map(agent => ({
  id: agent.id,
  workspace: agent.workspace || null,
  workspaceExists: Boolean(agent.workspace && fs.existsSync(agent.workspace)),
  runtimeDir: path.join(home, '.openclaw', 'agents', agent.id),
  runtimeDirExists: fs.existsSync(path.join(home, '.openclaw', 'agents', agent.id)),
}));
const workspaceDirs = fs.existsSync(path.join(home, '.openclaw', 'workspaces'))
  ? fs.readdirSync(path.join(home, '.openclaw', 'workspaces')).sort()
  : [];
const runtimeDirs = fs.existsSync(path.join(home, '.openclaw', 'agents'))
  ? fs.readdirSync(path.join(home, '.openclaw', 'agents')).sort()
  : [];
const bindings = config.bindings || [];
const manifest = {
  generatedAt: new Date().toISOString(),
  snapshotPolicy: {
    privateMemoryFiles: 'included in private redacted recovery snapshot',
    excludedReinstallableOrGeneratedDirs: [
      '.git', '.venv', '__pycache__', 'node_modules', '.local-tools',
      'apt-cache', 'apt-extract', 'clamav-db', 'clamav-run', 'sandboxes',
    ],
  },
  configuredAgents,
  workspaceDirs,
  runtimeDirs,
  bindings,
  sharedAgentMemoryVault: {
    path: '/home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault',
    exists: fs.existsSync('/home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault'),
  },
  qmd: {
    binaryPresent: ['/home/vin/.local/bin/qmd', '/home/vin/.npm-global/bin/qmd', '/usr/local/bin/qmd', '/usr/bin/qmd']
      .some(p => fs.existsSync(p)),
  },
};
fs.writeFileSync(path.join(stagingDir, 'openclaw', 'agent-recovery-manifest.json'), JSON.stringify(manifest, null, 2) + '\n');
NODE

# Redact secrets in all text files, then fail closed if recognizable secrets remain.
set +e
python3 - <<'PY' "$STAGING_DIR" >>"$RUN_LOG" 2>&1
import os,re,sys
root=sys.argv[1]
patterns=[
 (re.compile(r'(sk-[A-Za-z0-9_\-]{20,})'),'[OPENAI_API_KEY]'),
 (re.compile(r'(AIza[0-9A-Za-z\-_]{20,})'),'[GOOGLE_API_KEY]'),
 (re.compile(r'(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})'),'[GITHUB_TOKEN]'),
 (re.compile(r'(xox[baprs]-[A-Za-z0-9-]{10,})'),'[SLACK_TOKEN]'),
 (re.compile(r'([0-9]{8,10}:[A-Za-z0-9_-]{20,})'),'[TELEGRAM_BOT_TOKEN]'),
 (re.compile(r'\b(mfa\.[A-Za-z0-9_-]{20,}|[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{20,})\b'),'[DISCORD_BOT_TOKEN]'),
 (re.compile(r'(?i)(discord[^\n\r:=]{0,20}[=:]\s*)([A-Za-z0-9._-]{20,})'),r'\1[DISCORD_BOT_TOKEN]'),
 (re.compile(r'(?i)((?:token|api[_-]?key|secret|password|passphrase|client_secret|refresh_token|access_token|key)\s*[=:]\s*)(["\']?)([^\s,"\']+)(["\']?)'),r'\1\2[REDACTED_SECRET]\4'),
 (re.compile(r'(?i)("(?:token|api[_-]?key|secret|password|passphrase|client_secret|refresh_token|access_token|key)"\s*:\s*")([^"]+)(")'),r'\1[REDACTED_SECRET]\3'),
 (re.compile(r'(https?://[^\s/]+:[^@\s]+@[^\s]+)'),'[REDACTED_PRIVATE_URL]'),
 (re.compile(r'-----BEGIN (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY-----.*?-----END (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY-----', re.S),'[REDACTED_PRIVATE_KEY]'),
]
text_ext={'.md','.txt','.json','.jsonl','.yaml','.yml','.env','.ini','.conf','.service','.timer','.sh','.py','.js','.ts','.toml','.cfg','.xml','.csv','.log'}
redacted=0
for dp,_,files in os.walk(root):
    for f in files:
        p=os.path.join(dp,f)
        if os.path.getsize(p)>2_000_000: continue
        ext=os.path.splitext(f)[1].lower()
        if ext and ext not in text_ext: continue
        try:
            b=open(p,'rb').read()
            b.decode('utf-8')
        except Exception:
            continue
        s=b.decode('utf-8')
        orig=s
        for pat,rep in patterns:
            s=pat.sub(rep,s)
        if s!=orig:
            open(p,'w',encoding='utf-8').write(s)
            redacted+=1
print(f"redacted_files={redacted}")

suspect_patterns=[
 ('OpenAI API key', re.compile(r'sk-[A-Za-z0-9_\-]{20,}')),
 ('Google API key', re.compile(r'AIza[0-9A-Za-z\-_]{20,}')),
 ('GitHub token', re.compile(r'ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,}')),
 ('Telegram bot token', re.compile(r'[0-9]{8,10}:[A-Za-z0-9_-]{20,}')),
 ('Discord bot token', re.compile(r'\b(?:mfa\.[A-Za-z0-9_-]{20,}|[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{20,})\b')),
 ('private key', re.compile(r'BEGIN (?:OPENSSH|RSA|EC|DSA) PRIVATE KEY')),
]
findings=[]
for dp,_,files in os.walk(root):
    for f in files:
        p=os.path.join(dp,f)
        if os.path.getsize(p)>2_000_000: continue
        try:
            s=open(p,encoding='utf-8',errors='ignore').read()
        except Exception:
            continue
        for label,pat in suspect_patterns:
            if pat.search(s):
                findings.append(f"{label}: {os.path.relpath(p, root)}")
                break
if findings:
    print('unredacted_secret_findings=' + '; '.join(findings[:20]))
    raise SystemExit(91)
PY
redact_status=$?
set -e
case $redact_status in
  0) ;;
  91) fail "secret scan found unredacted secrets after redaction" ;;
  *) fail "secret scan/redaction failed" ;;
esac

# Sync staging into repo (preserve git metadata)
rsync -a --delete --exclude '.git' "$STAGING_DIR/" "$BACKUP_WORKDIR/" >>"$RUN_LOG" 2>&1 || fail "sync into backup repo failed"

git -C "$BACKUP_WORKDIR" rev-parse --is-inside-work-tree >>"$RUN_LOG" 2>&1 || fail "backup repo git metadata missing (.git)"
git config user.name "$GIT_AUTHOR_NAME" >>"$RUN_LOG" 2>&1 || fail "git config user.name failed"
git config user.email "$GIT_AUTHOR_EMAIL" >>"$RUN_LOG" 2>&1 || fail "git config user.email failed"
git add -A || fail "git add failed"
if git diff --cached --quiet; then
  log "No changes since last backup"
  if [ "${#WARNINGS[@]}" -gt 0 ]; then
    send_mail "OpenClaw backup OK with warnings ($TS)" "Backup completed with warnings: $(printf '%s; ' "${WARNINGS[@]}")" || true
  else
    send_mail "OpenClaw backup OK ($TS)" "Backup completed: no changes." || true
  fi
  exit 0
fi

CHANGED_SUMMARY="$(git diff --cached --name-status | sed -n '1,25p' | tr '\n' '; ')"
COMMIT_MSG="backup: $(date -u +%F) agent-config snapshot"

git commit -m "$COMMIT_MSG" -m "Changes: $CHANGED_SUMMARY" >>"$RUN_LOG" 2>&1 || fail "git commit failed"
git push origin "$BACKUP_REPO_BRANCH" >>"$RUN_LOG" 2>&1 || fail "git push failed"

AFTER_HASH="$(git rev-parse --short HEAD)"
ONE_LINE="Backup OK: commit $AFTER_HASH pushed to $BACKUP_REPO_BRANCH at $TS"
if [ "${#WARNINGS[@]}" -gt 0 ]; then
  ONE_LINE="$ONE_LINE; warnings: $(printf '%s; ' "${WARNINGS[@]}")"
  send_mail "OpenClaw backup OK with warnings ($TS)" "$ONE_LINE" || fail "backup succeeded but email confirmation failed"
else
  send_mail "OpenClaw backup OK ($TS)" "$ONE_LINE" || fail "backup succeeded but email confirmation failed"
fi
log "$ONE_LINE"
