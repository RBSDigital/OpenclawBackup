# Errors

Command failures and integration errors.

---

## 2026-09-02: AgentSelectionRequiredError on Inbound Events
- **Error**: `AgentSelectionRequiredError: Multiple agents are configured, but <channel> account default routing has no explicit owner.`
- **Cause**: Explicit multi-agent mode without channel fallback route bindings or system agent default.
- **Fix**: Add channel-wide bindings in `openclaw.json` (`bindings` array) pointing to `manager-bot`, and configure `agents.defaults.systemAgent.agentId = "manager-bot"`.

## 2026-09-02: Plugin SyntaxError (Missing SDK Export)
- **Error**: `SyntaxError: The requested module 'openclaw/plugin-sdk/security-runtime' does not provide an export named 'privateFileStore'`
- **Cause**: `@openclaw/discord` plugin v2026.7.1 installed against OpenClaw core v2026.8.2.
- **Fix**: Run `openclaw plugins update --all --accept-capabilities --acknowledge-install-policy-warning` and restart gateway.

## 2026-09-02: SQLite Schema Version Mismatch on Stale Gateway Process
- **Error**: `OpenClaw agent database ... uses newer schema version 19; this OpenClaw build supports 1`
- **Cause**: Core package upgraded on disk while older gateway process stayed active in RAM.
- **Fix**: Restart gateway service via `systemctl --user restart openclaw-gateway.service`.
