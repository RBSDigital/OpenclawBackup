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
