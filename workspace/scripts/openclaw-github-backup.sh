#!/usr/bin/env bash
set -euo pipefail

OPENCLAW_BIN="${OPENCLAW_BIN:-$HOME/.npm-global/bin/openclaw}"
[ -x "$OPENCLAW_BIN" ] || OPENCLAW_BIN="$(command -v openclaw || true)"
[ -x "$OPENCLAW_BIN" ] || { echo "ERROR: openclaw binary not found"; exit 127; }

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

# Collect critical files
mkdir -p "$STAGING_DIR/workspace" "$STAGING_DIR/systemd-user" "$STAGING_DIR/openclaw"
rsync -a --delete --exclude '.git' /home/vin/.openclaw/workspace/ "$STAGING_DIR/workspace/" >>"$RUN_LOG" 2>&1 || fail "rsync workspace failed"
cp -a ~/.config/systemd/user/openclaw* "$STAGING_DIR/systemd-user/" 2>/dev/null || true
cp -a ~/.openclaw/openclaw.json "$STAGING_DIR/openclaw/" 2>/dev/null || true
cp -a ~/.openclaw/cron "$STAGING_DIR/openclaw/" 2>/dev/null || true
cp -a ~/.openclaw/memory "$STAGING_DIR/openclaw/" 2>/dev/null || true
cp -a ~/.openclaw/skills "$STAGING_DIR/openclaw/" 2>/dev/null || true

"$OPENCLAW_BIN" cron list --json > "$STAGING_DIR/openclaw/cron-list.json" 2>>"$RUN_LOG" || fail "openclaw cron list failed"
"$OPENCLAW_BIN" skills list --json > "$STAGING_DIR/openclaw/skills-list.json" 2>>"$RUN_LOG" || fail "openclaw skills list failed"

# Redact secrets in all text files
python3 - <<'PY' "$STAGING_DIR" >>"$RUN_LOG" 2>&1 || exit 90
import os,re,sys
root=sys.argv[1]
patterns=[
 (re.compile(r'(AIza[0-9A-Za-z\-_]{20,})'),'[GOOGLE_API_KEY]'),
 (re.compile(r'(ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})'),'[GITHUB_TOKEN]'),
 (re.compile(r'(xox[baprs]-[A-Za-z0-9-]{10,})'),'[SLACK_TOKEN]'),
 (re.compile(r'([0-9]{8,10}:[A-Za-z0-9_-]{20,})'),'[TELEGRAM_BOT_TOKEN]'),
 (re.compile(r'(?i)(discord[^\n\r:=]{0,20}[=:]\s*)([A-Za-z0-9._-]{20,})'),r'\1[DISCORD_BOT_TOKEN]'),
 (re.compile(r'(?i)(token|api[_-]?key|secret|password|passphrase|client_secret|refresh_token|access_token)(\s*[=:]\s*)([^\s"\']+)'),r'\1\2[REDACTED_SECRET]'),
 (re.compile(r'(https?://[^\s/]+:[^@\s]+@[^\s]+)'),'[REDACTED_PRIVATE_URL]'),
]
text_ext={'.md','.txt','.json','.yaml','.yml','.env','.ini','.conf','.service','.timer','.sh','.py','.js','.ts','.toml','.cfg','.xml','.csv','.log'}
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
PY
if [ $? -eq 90 ]; then fail "secret scan/redaction failed"; fi

# Sync staging into repo (preserve git metadata)
rsync -a --delete --exclude '.git' "$STAGING_DIR/" "$BACKUP_WORKDIR/" >>"$RUN_LOG" 2>&1 || fail "sync into backup repo failed"

git -C "$BACKUP_WORKDIR" rev-parse --is-inside-work-tree >>"$RUN_LOG" 2>&1 || fail "backup repo git metadata missing (.git)"
git config user.name "$GIT_AUTHOR_NAME" >>"$RUN_LOG" 2>&1 || fail "git config user.name failed"
git config user.email "$GIT_AUTHOR_EMAIL" >>"$RUN_LOG" 2>&1 || fail "git config user.email failed"
git add -A || fail "git add failed"
if git diff --cached --quiet; then
  log "No changes since last backup"
  send_mail "OpenClaw backup OK ($TS)" "Backup completed: no changes." || true
  exit 0
fi

CHANGED_SUMMARY="$(git diff --cached --name-status | sed -n '1,25p' | tr '\n' '; ')"
COMMIT_MSG="backup: $(date -u +%F) agent-config snapshot"

git commit -m "$COMMIT_MSG" -m "Changes: $CHANGED_SUMMARY" >>"$RUN_LOG" 2>&1 || fail "git commit failed"
git push origin "$BACKUP_REPO_BRANCH" >>"$RUN_LOG" 2>&1 || fail "git push failed"

AFTER_HASH="$(git rev-parse --short HEAD)"
ONE_LINE="Backup OK: commit $AFTER_HASH pushed to $BACKUP_REPO_BRANCH at $TS"
send_mail "OpenClaw backup OK ($TS)" "$ONE_LINE" || fail "backup succeeded but email confirmation failed"
log "$ONE_LINE"