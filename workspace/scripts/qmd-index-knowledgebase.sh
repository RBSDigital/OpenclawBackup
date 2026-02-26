#!/usr/bin/env bash
set -euo pipefail

VAULT_PATH="${VAULT_PATH:-/home/vin/AdaOC_Knowledgebase}"
QMD_SOURCE="${QMD_SOURCE:-$HOME/.cache/qmd/sources/AdaOC_Knowledgebase}"
COLLECTION_NAME="${COLLECTION_NAME:-adaoc_kb}"
INDEX_NAME="${INDEX_NAME:-adaoc_kb}"
LOG_DIR="${LOG_DIR:-$HOME/.openclaw/logs}"
mkdir -p "$QMD_SOURCE" "$LOG_DIR"
RUN_LOG="$LOG_DIR/qmd-index-$(date -u +%Y-%m-%dT%H:%M:%SZ).log"

log(){ echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a "$RUN_LOG"; }

command -v qmd >/dev/null 2>&1 || { log "ERROR: qmd not installed"; exit 127; }

if [ ! -d "$VAULT_PATH" ]; then
  log "ERROR: Vault path not found: $VAULT_PATH"
  exit 2
fi

log "Syncing markdown files from vault"
rsync -a --delete --prune-empty-dirs \
  --include='*/' \
  --include='*.md' \
  --exclude='.obsidian/***' \
  --exclude='.trash/***' \
  --exclude='Templates/***' \
  --exclude='*' \
  "$VAULT_PATH/" "$QMD_SOURCE/" >>"$RUN_LOG" 2>&1

MD_COUNT=$(find "$QMD_SOURCE" -type f -name '*.md' | wc -l | awk '{print $1}')
log "Synced markdown files: $MD_COUNT"

if ! qmd --index "$INDEX_NAME" collection list | grep -q "^$COLLECTION_NAME\b"; then
  log "Adding collection $COLLECTION_NAME"
  qmd --index "$INDEX_NAME" collection add "$QMD_SOURCE" --name "$COLLECTION_NAME" --mask "**/*.md" >>"$RUN_LOG" 2>&1
else
  log "Collection already exists: $COLLECTION_NAME"
fi

log "Updating index"
qmd --index "$INDEX_NAME" update >>"$RUN_LOG" 2>&1

log "Embedding vectors (incremental)"
qmd --index "$INDEX_NAME" embed >>"$RUN_LOG" 2>&1

log "QMD indexing completed"
qmd --index "$INDEX_NAME" status | tee -a "$RUN_LOG"
