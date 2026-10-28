# Linux Service Integration — supervised backend + tray

Glossa Lab on Linux follows the Syncyard spec 007 pattern
(windowless supervision): a service manager supervises the backend
with a restart cap and an owner-visible alert, and the tray is a
per-user autostart application carrying the Glossa Lab icon. There
is exactly one install path:

```bash
./setup-os.sh install        # or directly:
services/linux/install.sh    # add --system on machines with no user manager
```

## What the installer does

`services/linux/install.sh` is idempotent and installs **both**
halves:

1. **Dependencies** — creates `backend/venv` if needed and installs
   `backend[tray]` (backend + pystray/Pillow) into it.
   `--skip-dependencies` and `--venv-python PATH` cover pre-provisioned
   environments.
2. **Backend unit** — renders `glossa-lab-backend.service` into the
   systemd unit directory:
   - runs `uvicorn glossa_lab.main:create_app --factory` on
     127.0.0.1:8001 directly (no shell wrapper, no reload);
   - `Restart=on-failure`, 5-second delay, **start limit 3 starts
     per hour** (`StartLimitBurst=3` / `StartLimitIntervalSec=3600`);
   - on failure the `glossa-lab-backend-alert.service` writes an
     `OWNER_NEEDED` marker and a `supervisor.log` line into the
     state directory — the backend never crash-loops silently;
   - stdout/stderr append to `<state dir>/backend.log`;
   - a legacy `glossa-lab.service` unit in the same directory is
     stopped, disabled, and removed, so two supervisors never race.
3. **Tray + icon** — renders `glossa-lab-tray.desktop` into
   `~/.config/autostart/` and installs the Glossa Lab brand icon
   (`tray/glossa_tray/assets/glossa-lab.png`, the blue gradient tile
   with a white "G" used by the web UI) into
   `~/.local/share/icons/hicolor/256x256/apps/glossa-lab.png`.
   The installer prints the installed icon's SHA-256.
4. **Verification** — enables and starts the unit, then runs
   `healthcheck.py` (bounded, 30 attempts): HTTP 200 on `/docs`,
   a healthy `/api/v1/health`, and an `/openapi.json` title/version
   match — identity, not just liveness. The result lands in
   `<state dir>/health-status.json`; a passing check clears any
   stale `OWNER_NEEDED` marker.

## Modes and paths

| | user mode (default) | `--system` mode |
|---|---|---|
| unit directory | `~/.config/systemd/user/` | `/etc/systemd/system/` |
| state directory | `~/.local/state/glossa-lab/` | `/var/lib/glossa-lab/` |
| support files | `~/.local/share/glossa-lab/supervisor/` | `/usr/local/lib/glossa-lab/` |
| manager | `systemctl --user` | `systemctl` |

System mode exists for headless machines where no user manager is
running (for example the Muse VM: root has no user runtime
directory, so `systemctl --user` cannot work there). The tray half
is per-user in both modes — a tray needs a desktop session.

`--render-only` writes every file but touches no service manager;
tests use it. `--no-start` installs and enables without starting.
`--no-tray` skips the tray half.

## Usage

```bash
systemctl --user status glossa-lab-backend     # or: ./setup-os.sh status
systemctl --user restart glossa-lab-backend
journalctl --user -u glossa-lab-backend        # supervisor actions
cat ~/.local/state/glossa-lab/OWNER_NEEDED     # present only on alert
```

`setup-os.sh` honours `GLOSSA_SERVICE_MODE=system` to talk to the
system manager instead of the user manager.

## Uninstall

```bash
services/linux/uninstall.sh            # add --system in system mode
```

Removes the units, the tray autostart entry, and the installed
icon. State and logs are kept — they are the supervisor's record.
