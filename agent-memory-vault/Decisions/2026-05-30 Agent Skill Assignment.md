---
owner: manager-bot
created: 2026-05-30
last_verified: 2026-05-30
status: accepted
confidence: high
source: Vincent request in #manager-hq
tags:
  - decision
  - skills
---

# Agent Skill Assignment

## Decision

Local OpenClaw skills were assigned to agents by lane:

- `manager-bot`: intake/reference set, including `skill-vetter`, `financial-analyst`, `stock-analysis`, `youtube-watcher`, `playwright`, Excel, PowerPoint, self-improvement, and skill-creator.
- `researcher-bot`: `financial-analyst`, `stock-analysis`, `youtube-watcher`, `playwright`, Excel, PowerPoint, and `skill-vetter`.
- `ops-bot`: `playwright`, Excel, self-improvement, and `skill-vetter`.
- `admin-bot`: `playwright`, self-improvement, and `skill-vetter`.
- `security-bot`: `playwright`, Excel, PowerPoint, self-improvement, and `skill-vetter`.
- `modeler-bot`: existing `3d-print-modeling`, plus Excel, self-improvement, and `skill-vetter`.

## Verification

All six agents reported `Missing requirements: 0` after installing `yt-dlp` user-locally with `uv tool install yt-dlp`.
