# Security-Bot Heartbeat Checklist

Vincent has configured security-bot to run periodic checks to keep the setup hardened, healthy, and growing in capabilities:

- Every 24 hours, perform a security and operational health audit:
  1. Inspect ~/.config/systemd/user/ overrides (e.g. openclaw-gateway.service.d/override.conf) to ensure they have 600 permissions, contain no hardcoded secrets in env variables, and delegate to %h/.config/openclaw/gog.env instead.
  2. Verify ~/.openclaw/workspace and ~/.openclaw/workspaces directory permissions are secure (should be 700).
  3. Query ~/.openclaw/state/openclaw.sqlite for any failed delivery queue entries.
  4. Verify the self-improvement hook is active in `openclaw hooks list`.
  5. Check if the `.learnings/` folders exist in your active workspace.
- If any vulnerabilities or operational failures are detected:
  - Compile the findings and proposed safe fixes into a structured checklist report.
  - Post the report to the Discord security channel (or peer-channel) and ask Vincent for permission to run the repairs.
  - Wait for Vincent to reply "Proceed" or "Approved" before executing any commands or making changes to the system.
- Reply `HEARTBEAT_OK` if no new issues are found or if the audit has already been reported.
