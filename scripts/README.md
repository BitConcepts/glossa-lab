# Scripts

This directory contains helper scripts for Glossa Lab.

Scripts in this directory exist to make development, startup, packaging, testing, and environment setup more explicit and reproducible.

They should reduce tribal knowledge, not hide behavior.

## Responsibilities

Scripts here may support:

- local development startup
- environment bootstrap
- backend/frontend convenience commands
- service installation and removal
- packaging and build helpers
- smoke tests
- diagnostics and health checks
- cross-platform setup workflows

## Design rules

All scripts should be:

- explicit
- documented
- safe to run intentionally
- narrow in scope
- reproducible
- cross-platform aware where applicable

Scripts must not become a hidden control plane for the application.

If a script changes runtime behavior, startup behavior, packaging behavior, or service installation behavior, that behavior must also be documented in the relevant docs.

## Expectations

- scripts should prefer clear names over clever names
- scripts should do one thing or one closely related workflow
- destructive operations should be clearly labeled
- platform-specific scripts should be separated or clearly named
- output should be readable and useful for debugging
- failures should be obvious and actionable

## Platform guidance

Where applicable, scripts should make platform scope explicit:

- Windows-specific scripts
- Linux-specific scripts
- macOS-specific scripts
- cross-platform scripts

Do not assume behavior is identical across operating systems unless it is confirmed and documented.

## Planned usage areas

Expected future additions include scripts for:

- local backend startup
- local frontend startup
- combined development startup
- Windows service/setup helpers
- Linux systemd install/uninstall helpers
- macOS startup/service helpers
- packaging/build flows
- smoke-test runs
- environment setup and validation

## Documentation rule

If a script becomes part of the expected developer or install workflow, it should be referenced in:

- `README.md`
- `docs/workflow.md`
- `docs/services.md` if it affects services/startup
- other relevant docs as needed

## Safety rule

Scripts should be safe by default where practical.

If a script is destructive, privileged, or install-affecting, it should make that obvious in:
- its filename
- its output
- its documentation
