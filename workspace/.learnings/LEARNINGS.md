# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice

---

## 2026-09-02: Multi-Agent Route Bindings Require Channel-Wide Fallbacks
- **Category**: correction / best_practice
- **Context**: In multi-agent configurations with `agents.ownership: "explicit"`, if an inbound message arrives on a channel or DM that doesn't match an exact channel ID binding, OpenClaw throws `AgentSelectionRequiredError: Multiple agents are configured, but <channel> account default routing has no explicit owner.`
- **Correction**: Always define a channel-wide binding for each configured channel in `openclaw.json` (e.g. `{ "match": { "channel": "telegram" }, "agentId": "manager-bot" }` and `{ "match": { "channel": "discord" }, "agentId": "manager-bot" }`), and define `agents.defaults.systemAgent.agentId = "manager-bot"` for ambient system commands.

## 2026-09-02: Core Package Upgrades Require Simultaneous Plugin Synchronization
- **Category**: best_practice / insight
- **Context**: OpenClaw SDK changes between minor versions (e.g., 2026.7.1 -> 2026.8.2) can deprecate or remove exports from `openclaw/plugin-sdk/*`. Managed plugins in `~/.openclaw/npm/projects/` (such as `@openclaw/discord`) fail to load if not updated concurrently.
- **Correction**: Always run `openclaw plugins update --all --accept-capabilities --acknowledge-install-policy-warning` during or immediately following core updates.

## 2026-09-02: Maintenance Upgrades Must Ensure Non-Disruptive Gateway Transitions
- **Category**: best_practice / insight
- **Context**: Upgrading OpenClaw on disk while the gateway is running leaves the old binary in memory while SQLite schemas are upgraded to a newer version on disk. The old in-memory gateway crashes on incoming events due to schema version mismatches.
- **Correction**: The maintenance routine must guarantee an immediate gateway service restart after package installation, regardless of whether post-upgrade doctor checks return advisory warnings.

## 2026-09-02: visibleReplies in GroupChat Must Be "automatic" for Direct Model Delivery
- **Category**: correction / best_practice
- **Context**: Setting `messages.groupChat.visibleReplies: "message_tool"` causes OpenClaw to suppress normal assistant text responses in guild channels unless the model explicitly calls `message(action="send")`. The turn finishes with `[source-reply/private-final] agent produced a long private final reply without calling the configured delivery tool (message_tool_only); response kept private and not delivered to the source channel`.
- **Correction**: Set `messages.groupChat.visibleReplies: "automatic"` so assistant replies are automatically dispatched to Discord and other group/guild channels.
