# Heartbeat checklist

Run read-only and stay quiet unless there is an actionable issue.
- Check #admin-desk for pending approvals, permission, credential, or restart requests.
- Validate config read-only (openclaw config validate) and flag schema drift; do not change privileges or restart services without explicit approval.
- Group recurring drift signals (update failures, legacy heartbeat-file lint, loopback onboarding warnings, and skill-precedence collisions) into one admin-review item; do not remediate automatically.
- Review .learnings/ and memory for durable admin lessons; record one concise item when evidenced.
