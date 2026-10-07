# Errors

Command failures and integration errors.

---

## [ERR-20261006-001] discord-channel-discovery

**Logged**: 2026-10-06T00:00:00Z
**Priority**: medium
**Status**: pending
**Area**: infra

### Summary
Delegated Discord channel/category discovery was rejected because the plugin required the exact current conversation and account context.

### Error
`Delegated discord:channel-list requires the exact current conversation and account for this plugin.`

### Context
- Operation: read-only discovery of the target guild's channels before an agent/channel setup.
- Guild: `1485914371766091809`.
- No mutation was attempted after the rejection; IDs were not guessed.

### Suggested Fix
Run discovery from the exact Discord conversation/account context or have the owning manager session provide the verified category and channel IDs.

### Metadata
- Reproducible: unknown
- Related Files: /home/vin/.openclaw/openclaw.json

---
