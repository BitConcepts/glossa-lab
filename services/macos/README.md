# macOS Service Integration

## LaunchAgent

The backend can be managed as a macOS LaunchAgent.

### Install

```bash
chmod +x services/macos/install.sh
./services/macos/install.sh
```

Installs `com.glossalab.backend.plist` into `~/Library/LaunchAgents/`.

### Usage

```bash
launchctl load ~/Library/LaunchAgents/com.glossalab.backend.plist
launchctl unload ~/Library/LaunchAgents/com.glossalab.backend.plist
```

### Uninstall

```bash
./services/macos/uninstall.sh
```

## Notes

- Uses user-level LaunchAgent (not LaunchDaemon) for local installs.
- `RunAtLoad` is `false` by default — load manually or set to `true` for auto-start.
- Stdout/stderr logged to `logs/backend-stdout.log` and `logs/backend-stderr.log`.
