# CI Delivery and Recovery Coverage

## Summary

Two recovery-related ops gaps were repaired and validated on `2026-06-01`.

## Durable Notes

- Systemd services that send reports through the user-local `gog` binary need an explicit environment drop-in that exposes the binary path and required delivery environment.
- Recovery backups for the multi-agent setup need to include plural agent workspaces, the shared Agent Memory Vault, and a recovery manifest.
- Keep backup staging recovery-focused. Include durable agent configuration and memory while excluding reinstallable caches, toolchains, databases, sandboxes, and oversized workspace artifacts.

## Validation

- CI Manager report delivery succeeded after the environment fix.
- A private redacted recovery snapshot including the expanded coverage pushed successfully.

## Follow-Up

- Reconciled three stale failed-delivery queue artifacts before cleanup: two duplicated delivered lane messages and one obsolete modeler toolchain handoff whose requested outcome was already satisfied.
- After explicit authorization, moved all three stale artifacts to recoverable trash and verified the failed-delivery queue was empty.
