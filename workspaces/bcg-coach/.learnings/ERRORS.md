# Errors

Command failures and integration errors.

---

## 2026-10-24: Managed browser CDP launch failure

OpenClaw's managed Chromium repeatedly exited before CDP port 18800 became reachable, although the same Chromium binary launched successfully with a fresh temporary profile. The browser tool was also not exposed in the agent tool catalog. Diagnose the managed profile, executable selection and agent-level tool exposure separately; do not assume missing system libraries are the cause.
