#!/usr/bin/env bash
# Glossa Lab — record a supervisor alert when the backend unit fails.
#
# Invoked by glossa-lab-backend-alert.service (the backend unit's
# OnFailure target). Writes a durable OWNER_NEEDED marker plus a
# supervisor log line; never restarts anything itself.
set -euo pipefail

STATE_DIR="${1:?usage: record-owner-needed.sh STATE_DIR}"
mkdir -p "$STATE_DIR"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
MSG="OWNER NEEDED: glossa-lab-backend failed (restart cap or unit failure) at $TS"
printf '%s\n' "$MSG" > "$STATE_DIR/OWNER_NEEDED"
printf '%s %s\n' "$TS" "$MSG" >> "$STATE_DIR/supervisor.log"
logger -t glossa-lab "$MSG" 2>/dev/null || true
echo "$MSG"
