# OpenClaw Security Audit

Date: 2026-07-01 UTC
Scope: `/home/vin/.openclaw/openclaw.json`, `/home/vin/.openclaw/agents/main/agent/openclaw-agent.sqlite`, `/home/vin/.openclaw/agents/manager-bot/agent/openclaw-agent.sqlite`, and the daily maintenance routine in [openclaw-maintenance.sh](/home/vin/.openclaw/workspace/scripts/openclaw-maintenance.sh#L63).

## Executive Summary

I ran the built-in OpenClaw security checks:

- `openclaw security audit --deep --json`
- `openclaw secrets audit --json`

Result: no critical findings, but there are several material warnings that should be cleaned up. The biggest issue is plaintext credential storage in OpenClaw config/state, followed by an insecure Control UI auth toggle and a few gateway hardening gaps. I also wired the daily maintenance script to run a security audit automatically so this stops being a one-off check.

## Findings

### High

#### 1. Plaintext credentials are stored in local OpenClaw config/state

Evidence:

- `/home/vin/.openclaw/openclaw.json`
- `/home/vin/.openclaw/agents/main/agent/openclaw-agent.sqlite`
- `/home/vin/.openclaw/agents/manager-bot/agent/openclaw-agent.sqlite`

What the audit reported:

- `gateway.auth.token` stored as plaintext
- `channels.telegram.botToken` stored as plaintext
- `channels.discord.token` stored as plaintext
- `profiles.openai:default.key` stored as plaintext
- `profiles.google:default.key` stored as plaintext
- `profiles.ollama:default.key` stored as plaintext

Impact:

Anyone who can read those files can recover gateway and channel credentials. That turns a local file-read bug, backup leak, or compromised workspace into account-level exposure.

### Medium

#### 2. Control UI insecure auth toggle is enabled

Evidence:

- `openclaw security audit --deep --json`
- finding: `gateway.controlUi.allowInsecureAuth=true`

Impact:

This weakens the Control UI trust model and increases the chance of accidental exposure if the UI is proxied or made reachable beyond localhost.

#### 3. Reverse proxy trust is not configured

Evidence:

- `openclaw security audit --deep --json`
- finding: `gateway.trustedProxies` is empty while `gateway.bind` is loopback

Impact:

If the Control UI is ever exposed through a reverse proxy, local-client checks can be spoofed unless trusted proxy IPs are configured.

#### 4. Shared-gateway hardening is weak if multiple users are expected

Evidence:

- `openclaw security audit --deep --json`
- heuristic warning: sandbox is off and `workspaceOnly=false` appears in agent contexts

Impact:

This is acceptable only if the gateway is truly a personal-assistant boundary. If untrusted users can reach the same gateway, the current settings are too permissive for shared use.

### Low

#### 5. Legacy OAuth residue remains in agent state

Evidence:

- `/home/vin/.openclaw/agents/main/agent/openclaw-agent.sqlite`
- findings for `profiles.openai:chatgpt-default` and `profiles.openai:vincentreynolds1@gmail.com`

Impact:

This is lower risk than plaintext secrets, but it is still state that should be reviewed and pruned if those credentials are no longer needed.

## What I Changed

I added a recurring security-audit step to the daily maintenance script:

- [openclaw-maintenance.sh](/home/vin/.openclaw/workspace/scripts/openclaw-maintenance.sh#L63-L105) now runs `openclaw security audit --deep --json` and `openclaw secrets audit --json`.
- [openclaw-maintenance.sh](/home/vin/.openclaw/workspace/scripts/openclaw-maintenance.sh#L277-L284) now includes the security audit summary in the normal maintenance email.

The script still fails hard only for critical security findings or command-level audit failures. Warnings are reported in the daily summary so the routine stays useful instead of noisy.

## Verification

- `bash -n /home/vin/.openclaw/workspace/scripts/openclaw-maintenance.sh` passed.
- `openclaw security audit --deep --json` returned `critical=0, warn=4, info=1`.
- `openclaw secrets audit --json` returned `plaintextCount=9, legacyResidueCount=2`.

## Recommended Follow-up

1. Move plaintext gateway and channel credentials to SecretRef-backed storage or another non-plaintext mechanism.
2. Disable `gateway.controlUi.allowInsecureAuth` unless you are actively debugging and keeping the UI local-only.
3. Populate `gateway.trustedProxies` if the Control UI is proxied, or keep it strictly localhost-only.
4. Decide whether this gateway is personal-only or shared. If shared, tighten sandboxing and workspace scoping before treating it as multi-user.
