# Errors

Command failures and integration errors.

---

- 2026-08-31 - OpenClaw config validation blocked heartbeat audit
  - What happened: `openclaw hooks list` failed because `/home/vin/.openclaw/openclaw.json` now has invalid keys (`lastTouchedAt`, `gateway.controlUi.allowInsecureAuth`, `gateway.tailscale.resetOnExit`, `gateway.nodes.denyCommands`) and requires `agents.ownership=explicit`.
  - Do differently: validate `openclaw.json` against the current schema or run `openclaw doctor` before depending on hooks output.

- 2026-09-01 - OpenClaw heartbeat blocked by invalid config
  - What happened: The daily heartbeat audit failed because `openclaw hooks list` rejected `/home/vin/.openclaw/openclaw.json` with schema errors (`meta.lastTouchedAt`, `gateway.controlUi.allowInsecureAuth`, `gateway.tailscale.resetOnExit`, `gateway.nodes.denyCommands`, and missing `agents.ownership=explicit`).
  - Do differently: Run `openclaw doctor` or validate `openclaw.json` against the current schema before relying on hook/status checks.

- 2026-09-02 - `openclaw hooks list` now requires explicit admin scope
  - What happened: `openclaw hooks list --agent security-bot` failed with `missing scope: operator.admin`.
  - Do differently: request or verify the needed operator/admin scope before using hooks introspection during heartbeat checks.
