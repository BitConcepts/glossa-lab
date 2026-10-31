/** Spec 083 (Step 3) — small date/time renderers, viewer's zone. */

export function fmtDay(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

export function fmtDayYear(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

export function fmtTime(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleTimeString(undefined, { hour: "numeric", minute: "2-digit" });
}

/** "09:12 today" / "Oct 30" — the audit/users tables' activity style. */
export function fmtWhenShort(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  const now = new Date();
  const sameDay = d.toDateString() === now.toDateString();
  const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);
  if (sameDay) return `${fmtTime(iso)} today`;
  if (d.toDateString() === yesterday.toDateString()) return `${fmtTime(iso)} yesterday`;
  return fmtDay(iso);
}

/** "Today, 09:41" / "Oct 30, 09:41" — the account activity style. */
export function fmtWhenLong(iso: string | null | undefined): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "—";
  const now = new Date();
  if (d.toDateString() === now.toDateString()) return `Today, ${fmtTime(iso)}`;
  const yesterday = new Date(now.getTime() - 24 * 60 * 60 * 1000);
  if (d.toDateString() === yesterday.toDateString()) return `Yesterday, ${fmtTime(iso)}`;
  return `${fmtDay(iso)}, ${fmtTime(iso)}`;
}
