# Windows Service Integration

## Startup Registration

The tray app can be registered to start automatically at user login via a Startup folder shortcut.

### Install

```cmd
services\windows\install.cmd
```

Creates a `.lnk` shortcut in the user's Startup folder that runs `shell.cmd tray`.

### Uninstall

```cmd
services\windows\uninstall.cmd
```

Removes the startup shortcut.

## Notes

- Uses Startup folder (not registry or scheduled task) for simplicity and transparency.
- The tray app polls the backend health API — it does not contain backend logic.
- To start the backend without the tray: `shell.cmd run`
