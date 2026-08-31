# Errors

Command failures and integration errors.

---

- 2026-08-31 - OpenClaw config validation blocked heartbeat audit
  - What happened: `openclaw hooks list` failed because `/home/vin/.openclaw/openclaw.json` now has invalid keys (`lastTouchedAt`, `gateway.controlUi.allowInsecureAuth`, `gateway.tailscale.resetOnExit`, `gateway.nodes.denyCommands`) and requires `agents.ownership=explicit`.
  - Do differently: validate `openclaw.json` against the current schema or run `openclaw doctor` before depending on hooks output.
