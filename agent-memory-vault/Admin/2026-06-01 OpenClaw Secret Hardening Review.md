# OpenClaw Secret Hardening Review

## Summary

A read-only manager heartbeat review on `2026-06-01` confirmed that an admin hardening preview is still needed.

## Verified State

- The OpenClaw home directory remains mode `775`.
- `openclaw secrets audit --check` reports plaintext secret-bearing fields and legacy authentication residue.
- No raw secret values were copied into shared notes or Discord.

## Next Action

Admin lane should preview:

- impact of tightening the OpenClaw home directory to `700`
- supported SecretRef migration steps
- separate handling for legacy OAuth or auth-profile residue
- validation and rollback plan before applying high-risk changes
