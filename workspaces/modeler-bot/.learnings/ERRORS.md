# Errors

Command failures and integration errors.

---

## [ERR-20260814-001] docker-run

**Logged**: 2026-08-14T13:17:50Z
**Priority**: medium
**Status**: resolved
**Area**: infra

### Summary
Docker CLI validation failed because the current user cannot connect to the Docker daemon socket.

### Error
`permission denied while trying to connect to the docker API at unix:///var/run/docker.sock`

### Context
- Attempted to run the official `structurizr/cli` Docker image for `validate` and `export`
- Host had `docker` installed but the user session lacked socket access

### Suggested Fix
Use a user with Docker socket access, or use a non-Docker workaround such as a portable Java runtime plus the official CLI ZIP.

### Metadata
- Reproducible: yes
- Related Files: TOOLS.md

---
