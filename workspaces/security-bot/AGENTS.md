# AGENTS.md - Security Bot Workspace

This workspace belongs to `security-bot`.

## Startup

Use runtime-provided context first. Read `SOUL.md`, `TOOLS.md`, and project notes only when needed for the current task.

## Scope Policy

Before active scanning or testing, require:

- Target/domain/IP/repo/system
- Authorization basis
- Allowed techniques
- Rate limits
- Time window
- Stop conditions
- Reporting destination

Passive research and local repository analysis can proceed when the target is local or clearly supplied by Vincent.

## Storage

- `reports/` - finished findings and summaries
- `scans/` - raw or structured scan output
- `triage/` - alert/log/email investigations
- `policies/` - GRC and threat-modeling work
- `sandboxes/` - local isolated fixtures only
- `projects/<slug>/` - larger task state

## Shared Agent Memory Vault

Use `/home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault` only for sanitized defensive security memory that should be reusable by the agent team.

- Consult `Security/`, `Decisions/`, and `Sources/` before substantial defensive security, GRC, or triage work.
- Write procedures, scope templates, detection conventions, and sanitized lessons with `owner`, `created`, `last_verified`, `confidence`, and source/path references.
- Do not store secrets, credentials, exploit-enabling details, sensitive findings, raw logs with secrets, private user context, or another agent's private memory in the vault.
- Keep raw scan output in `scans/` or project folders unless a sanitized summary should be promoted.

## Tool Use

Prefer safe defaults:

- Use non-destructive flags.
- Keep scan rates conservative.
- Save raw outputs when they support findings.
- Do not run untrusted binaries on the host.
- Use Docker/network isolation for suspicious files or exploit modernization.

## Escalation

- Source-heavy public research can involve `researcher-bot`.
- Operational monitoring and host health belongs with `ops-bot`.
- Privileged system changes belong with `admin-bot`.
- Coordination and summaries go through `manager-bot`.

## Self-Improvement

- Capture problems, corrections, errors, and insights immediately under `.learnings/`.
- Use `.learnings/ERRORS.md` for tool or integration failures, `.learnings/LEARNINGS.md` for user corrections and insights, and `.learnings/FEATURE_REQUESTS.md` for missing capabilities.
- Write entries as short, structured markdown blocks so they can be parsed by `manager-bot`'s daily review and promoted to the right long-term location.
- Log first, improve second.

## Tools

### Local notes (migrated from TOOLS.md)

# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup: camera names and locations, SSH hosts and aliases, preferred TTS voices, speaker/room names, device nicknames, anything environment-specific.

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## OpenClaw Heartbeat

- `openclaw hooks list` may require `operator.admin`; verify scope before relying on it for heartbeat checks.
- If hooks/status output looks schema-related, run `openclaw doctor` first.

## Related

- [Agent workspace](/concepts/agent-workspace)



# TOOLS.md - Security Bot Local Notes

## Installed Tool Groups

System/package tools:
- Available on host: `python3`, `uv`, `curl`, `jq`, `docker` binary.
- DNS tools already available on host: `dig`, `host`, `nslookup`.
- Docker socket is not usable by `vin` without permission changes.
- `sudo` currently requires a password, so root-level system installs are not used.

User-local tools are installed under this workspace where possible.

Use:

```bash
./bin/security-env <tool> ...
```

Installed in `bin/`:
- `gitleaks`
- `syft`
- `grype`
- `trivy`
- `gobuster`
- `subfinder`
- `httpx`
- `nuclei`
- `naabu`
- `dnsx`
- `katana`
- `nmap`
- `nping`
- `whois`
- `yara`
- `yarac`
- `clamscan`
- `freshclam`
- `sigtool`
- `shellcheck`
- `unzip`
- `zipinfo`

The Debian package based tools above are extracted under `apt-extract/` and wrapped from `bin/`; they are not system-installed.

ClamAV local database:
- `clamav-db/`
- Updated with `./bin/security-env freshclam`
- `clamscan` wrapper uses this local database by default.

Installed in `.venv/`:
- `semgrep`
- `bandit`
- `pip-audit`
- `detect-secrets`
- `checkov`
- `cyclonedx-py`
- `yara-python`
- `stix2`
- `vol` / Volatility 3
- `oletools`
- `ioc-finder`
- `sslyze`

Pending root/admin changes if needed:
- Docker group/socket access for sandboxed container workflows.
- Optional true system-wide package installs if Vincent wants these tools on global `PATH`.

## Default Safety

- Active scanning requires explicit authorized scope.
- Do not run untrusted binaries directly on the VPS.
- Prefer local fixtures and Docker sandboxes with networking disabled for suspicious content.
- Keep findings evidence-led and remediation-focused.

## Common Output Paths

- Raw scans: `scans/<date>-<slug>/`
- Finished reports: `reports/<date>-<slug>.md`
- Triage notes: `triage/<date>-<case>.md`
- Policy/GRC reviews: `policies/<date>-<topic>.md`

## Shared Agent Memory Vault

- Path: `/home/vin/ObsidianVaults/AdaKTVault/06_system/agent-memory-vault`
- Primary folders: `Security/`, `Sources/`, `Decisions/`
- Promote only sanitized defensive procedures, scope templates, detection conventions, and lessons.
- Keep raw scan output, sensitive findings, secrets, and exploit-enabling details out of shared memory.
