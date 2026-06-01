---
owner: manager-bot
created: 2026-05-30
last_verified: 2026-05-30
status: accepted
confidence: high
source: manager-bot daily memory 2026-05-29
tags:
  - durable-memory
  - discord
  - routing
---

# Discord Channel Recovery

## Summary

If an agent channel disappears from the Discord Agents view, check the Discord channel category before assuming the OpenClaw agent registration is broken.

## Details

On 2026-05-29, `#modeling-studio` was missing from the Agents view even though `modeler-bot` was still registered and bound in OpenClaw. The issue was that the Discord channel had no category parent. Restoring the channel to the Discord `Agents` category fixed visibility.

## Related

- `modeler-bot`
- `#modeling-studio`
- `#manager-hq`

## Review Notes

- Next review: if agent channels go missing again
- Staleness risk: low, unless Discord category structure changes
