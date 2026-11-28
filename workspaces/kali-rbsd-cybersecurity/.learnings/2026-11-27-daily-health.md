# 2026-11-27 daily health observation

- Evidence (2026-11-27 08:48 UTC): config validation passed and `openclaw.json` matched `openclaw.json.last-good`; gateway was reachable and active in `openclaw status` with host uptime 40d10h; Discord was connected and the Kali peer-specific route remained visible; workspace and engagement-gate files were present and hashed.
- Durable drift: the recurring global-install update failure and loopback-only gateway binding remain admin-review items. `rg` is unavailable locally, so the routine used `find`/`sed` fallback. No network testing, package change, restart, permission change, credential change, or service alteration was performed.
- Improvement: keep the fallback file-discovery path documented and continue grouping recurring update/install failure, loopback binding, and route-precedence evidence in the admin-desk audit while reporting only redacted status and evidence paths.
