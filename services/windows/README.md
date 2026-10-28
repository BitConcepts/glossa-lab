# Windows Service Integration

## Canonical install path (Spec 080)

There is exactly ONE Windows installer: `setup-os.cmd` at the repo
root. It registers the `GlossaLab` scheduled task (at logon), whose
action is `wscript.exe //nologo scripts\launch-tray.vbs` — the tray
starts with no visible window (governance rule H25). The tray then
starts and supervises the backend.

For a unattended host bring-up plus verification, use:

```cmd
scripts\install-desktop-host.cmd
scripts\verify-desktop-host.cmd
```

### Install

```cmd
setup-os.cmd install
```

(`services\windows\install.cmd` only delegates to it.)

The installer verifies the packaged tray icon assets
(`tray\glossa_tray\assets\glossa-lab.ico` / `.png`) against pinned
SHA-256 hashes and refuses to install on any mismatch.

### Uninstall

```cmd
setup-os.cmd uninstall
```

(`services\windows\uninstall.cmd` delegates and also removes any
legacy Startup-folder shortcut.)

## Retired path

The old Startup-folder shortcut pointing at `shell.cmd tray` is
retired (it bypassed the H25 VBS wrappers). Do not recreate it.

## Notes

- The tray app polls the backend health API and, on Windows,
  restarts a backend that died on its own (capped at 3 restarts per
  hour; a user stop is never overridden — Spec 080 FR-006).
- The backend data directory is deterministic in installed mode:
  `%LOCALAPPDATA%\GlossaLab\data` (`GLOSSA_MODE=installed` is set by
  the launch chain), never dependent on the caller's working
  directory.
- To start the backend without the tray: `shell.cmd run`
  (production factory semantics on 127.0.0.1:8001).
