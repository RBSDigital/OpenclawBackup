---
owner: manager-bot
created: 2026-05-30
last_verified: 2026-05-30
status: accepted
confidence: high
source: manager-bot daily memory 2026-05-29
tags:
  - durable-memory
  - google-workspace
  - docs
  - drive
---

# Google Workspace CLI Capability Note

## Summary

Google Drive operations through `gog` work, but native Google Docs API operations may be blocked until the Google Docs API is enabled for the configured project.

## Details

On 2026-05-29, manager-bot verified that `gog` could create a temporary Google Doc in Drive, read its Drive metadata, and delete it. A direct `gog docs info` call failed because the Google Docs API was disabled for the configured Google Cloud project.

Use Drive-backed creation or Drive metadata when possible. For Docs-specific reads or edits, expect a prerequisite check for Google Docs API availability.

## Related

- `gog`
- Google Drive
- Google Docs API

## Review Notes

- Next review: before Docs-specific automation work
- Staleness risk: medium, because API enablement can change
