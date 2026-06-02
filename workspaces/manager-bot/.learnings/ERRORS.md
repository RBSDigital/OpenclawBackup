# Errors

Command failures and integration errors.

---

## 2026-05-30 - `yt-dlp` dependency install fallback

**Context**: While making the `youtube-watcher` skill executable for agent workspaces, `python3 -m pip install --user yt-dlp` failed because the system Python did not have `pip`.

**Impact**: `youtube-watcher` remained marked as missing requirements until an alternate installer was used.

**Resolution**: Used `uv tool install yt-dlp`, which installed `/home/vin/.local/bin/yt-dlp` and cleared the missing requirement in `openclaw skills check`.

**Lesson**: On this host, prefer `uv tool install <tool>` for user-local Python CLI dependencies when `pip` is unavailable.

---

## 2026-05-31 - Cross-agent activation blocked by session visibility

**Context**: Manager heartbeat routed P1 ops work to `#ops-center`, but the lane remained idle. A direct `sessions_send(agentId="ops-bot")` attempt was rejected because `tools.sessions.visibility=tree` blocks cross-agent access. A fallback `sessions_spawn(agentId="ops-bot")` attempt was also rejected because this manager session may spawn only `manager-bot`.

**Impact**: `manager-bot` can post specialist handoffs but cannot directly wake `ops-bot` with the current runtime policy.

**Resolution**: Escalated the activation constraint to `#manager-hq` for a runtime-policy or ownership decision.

**Lesson**: After a specialist Discord handoff remains idle, test the configured-agent activation path once. If both cross-agent send and spawn are forbidden, escalate the policy constraint instead of repeating lane nudges.

---

## 2026-05-31 - Discord connector target syntax

**Context**: A heartbeat lane read failed when the Discord channel ID was passed through `channelId`, and failed again when `channel:<id>` was passed as the `channel` selector.

**Impact**: The lane review needed two retries.

**Resolution**: Used `channel="discord"` with `target="channel:<discord-channel-id>"`.

**Lesson**: For Discord reads in this runtime, select the backend with `channel` and encode the destination in `target`.

---

## 2026-06-01 - Interrupted generated backup checkout blocks rerun

**Context**: A validation run of `openclaw-github-backup.service` was stopped during its push after the expanded workspace snapshot included oversized reinstallable binaries. The next run failed because the generated backup checkout still had local changes and `git pull --rebase` refuses to proceed with an unclean worktree.

**Impact**: The first clean rerun stopped before staging a corrected snapshot.

**Resolution**: Preserved the interrupted generated checkout under a timestamped directory, added a 20 MB workspace-file cap, and allowed the service to clone a clean workdir.

**Lesson**: Recovery-focused backup expansion should exclude reinstallable large artifacts before the first push. After interrupting a generated backup checkout, preserve it and reclone before validation.
