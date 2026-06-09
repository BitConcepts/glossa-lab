/**
 * Locale-aware date/time formatting using the browser's Intl API.
 * Respects the host's locale, timezone, and 12/24-hour preference.
 *
 * All functions accept ISO 8601 strings or Date objects.
 */

/** Full date + time: "Apr 6, 2026, 1:14 PM EDT" */
export function fmtDateTime(value: string | Date): string {
  const d = typeof value === "string" ? new Date(value) : value;
  if (isNaN(d.getTime())) return String(value);
  return d.toLocaleString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
    timeZoneName: "short",
  });
}

/** Date only: "Apr 6, 2026" */
export function fmtDate(value: string | Date): string {
  const d = typeof value === "string" ? new Date(value) : value;
  if (isNaN(d.getTime())) return String(value);
  return d.toLocaleDateString(undefined, {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

/** Time only: "1:14 PM EDT" */
export function fmtTime(value: string | Date): string {
  const d = typeof value === "string" ? new Date(value) : value;
  if (isNaN(d.getTime())) return String(value);
  return d.toLocaleTimeString(undefined, {
    hour: "numeric",
    minute: "2-digit",
    timeZoneName: "short",
  });
}

/** Compact date+time for tables: "Apr 6, 1:14 PM" (no year/TZ to save space) */
export function fmtDateTimeCompact(value: string | Date): string {
  const d = typeof value === "string" ? new Date(value) : value;
  if (isNaN(d.getTime())) return String(value);
  const now = new Date();
  const sameYear = d.getFullYear() === now.getFullYear();
  return d.toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    ...(sameYear ? {} : { year: "numeric" }),
    hour: "numeric",
    minute: "2-digit",
  });
}

/** Duration from seconds → HH:MM:SS (or MM:SS if < 1 hour).
 *  fmtDuration(90)   → "01:30"
 *  fmtDuration(3661) → "1:01:01"
 */
export function fmtDuration(totalSeconds: number): string {
  const sec = Math.max(0, Math.round(totalSeconds));
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;
  const mm = String(m).padStart(2, "0");
  const ss = String(s).padStart(2, "0");
  return h > 0 ? `${h}:${mm}:${ss}` : `${mm}:${ss}`;
}

/** Elapsed time → always HH:MM:SS zero-padded.
 *  fmtElapsed(90)    → "00:01:30"
 *  fmtElapsed(3661)  → "01:01:01"
 *  Used for job elapsed/ETA display (REQ-JOBS-001).
 */
export function fmtElapsed(totalSeconds: number): string {
  const sec = Math.max(0, Math.round(totalSeconds));
  const h = Math.floor(sec / 3600);
  const m = Math.floor((sec % 3600) / 60);
  const s = sec % 60;
  return `${String(h).padStart(2, "0")}:${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

/** Relative time: "3 minutes ago", "2 days ago" */
export function fmtRelative(value: string | Date): string {
  const d = typeof value === "string" ? new Date(value) : value;
  if (isNaN(d.getTime())) return String(value);
  const diff = (Date.now() - d.getTime()) / 1000; // seconds
  if (diff < 60) return "just now";
  if (diff < 3600) return `${Math.floor(diff / 60)}m ago`;
  if (diff < 86400) return `${Math.floor(diff / 3600)}h ago`;
  if (diff < 86400 * 7) return `${Math.floor(diff / 86400)}d ago`;
  return fmtDate(d);
}
