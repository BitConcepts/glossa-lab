# Linux Service Integration

## systemd User Service

The backend can be managed as a systemd user service.

### Install

```bash
chmod +x services/linux/install.sh
./services/linux/install.sh
```

Installs `glossa-lab.service` into `~/.config/systemd/user/`.

### Usage

```bash
systemctl --user start glossa-lab
systemctl --user stop glossa-lab
systemctl --user status glossa-lab
```

### Uninstall

```bash
./services/linux/uninstall.sh
```

## Notes

- Uses user-level service (not system-level) for local development installs.
- The service unit runs `shell.sh run` which uses `python -m uvicorn`.
- Restarts on failure with a 5-second delay.
