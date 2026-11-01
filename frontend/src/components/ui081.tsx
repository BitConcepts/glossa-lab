/**
 * ui081 — shared building blocks for the Spec 081 redesign.
 *
 * The approved wireframes (specs/081-ui-redesign-generic-tool/wireframes/)
 * are the requirements for layout and appearance; the tokens here are the
 * wireframe design system's (wireframes.css), adapted to the app's
 * light/dark modes. Verdict colors carry meaning and are never decoration.
 */
import type { ReactNode } from "react";
import { STAGE_NAMES } from "./StageLegend";

// ── Palette ─────────────────────────────────────────────────────────────

export interface Palette {
  bg: string;
  card: string;
  border: string;
  borderSoft: string;
  fg: string;
  bad: string;
  muted: string;
  faint: string;
  accent: string;
  accentSoft: string;
  inputBg: string;
}

export function palette(dark: boolean): Palette {
  return dark
    ? {
        bg: "#0f172a", card: "#1e293b", border: "#334155", borderSoft: "#263449",
        fg: "#e2e8f0", bad: "#f87171", muted: "#94a3b8", faint: "#64748b",
        accent: "#60a5fa", accentSoft: "rgba(37,99,235,0.18)",
        inputBg: "#0f172a",
      }
    : {
        bg: "#f8fafc", card: "#ffffff", border: "#e5e7eb", borderSoft: "#eef1f5",
        fg: "#111827", bad: "#b91c1c", muted: "#64748b", faint: "#94a3b8",
        accent: "#2563eb", accentSoft: "#eff6ff",
        inputBg: "#ffffff",
      };
}

// ── Chips ───────────────────────────────────────────────────────────────

export type ChipTone = "ok" | "bad" | "warn" | "neutral" | "contest" | "line";

const CHIP_COLORS: Record<ChipTone, { bg: string; fg: string; border?: string }> = {
  ok:      { bg: "#f0fdf4", fg: "#15803d" },
  bad:     { bg: "#fef2f2", fg: "#b91c1c" },
  warn:    { bg: "#fffbeb", fg: "#b45309" },
  neutral: { bg: "#f1f5f9", fg: "#475569" },
  contest: { bg: "#f5f3ff", fg: "#7c3aed", border: "1px solid #ddd6fe" },
  line:    { bg: "none",    fg: "#64748b", border: "1px solid #e5e7eb" },
};

export function Chip({ tone, children }: { tone: ChipTone; children: ReactNode }) {
  const c = CHIP_COLORS[tone];
  return (
    <span style={{
      display: "inline-flex", alignItems: "center", gap: 5, padding: "2px 8px",
      borderRadius: 10, fontSize: 11, fontWeight: 700, whiteSpace: "nowrap",
      background: c.bg, color: c.fg, border: c.border ?? "1px solid transparent",
    }}>
      {children}
    </span>
  );
}

// ── Verdict vocabulary (FR-003) ──────────────────────────────────────────

/**
 * Map a lane-1 claim status to the register's plain verdict words.
 * Negative verdicts use the same chip size/weight as positive ones
 * (C081-5) — only the color differs, because color carries the meaning.
 */
export function verdictOf(claimStatus: string): { label: string; tone: ChipTone } {
  switch (claimStatus) {
    case "strongly_supported":
    case "supported":
      return { label: "Supported", tone: "ok" };
    case "partially_supported":
      return { label: "Supported — partial", tone: "ok" };
    case "unsupported":
      return { label: "Not supported", tone: "bad" };
    case "partially_falsified":
      return { label: "Not supported — partially falsified", tone: "bad" };
    case "contradicted":
      return { label: "Contradicted", tone: "bad" };
    case "cannot_be_administered":
      return { label: "Cannot be administered", tone: "neutral" };
    case "awaiting_expert":
      return { label: "Awaiting expert adjudication", tone: "neutral" };
    case "inconclusive":
      return { label: "Inconclusive", tone: "warn" };
    case "untested":
    default:
      return { label: "Insufficient evidence", tone: "warn" };
  }
}

// ── Stage track (five names verbatim, OD-4 / C081-9) ────────────────────

export function StageTrack({ stage }: { stage: string | null | undefined }) {
  const idx = stage ? STAGE_NAMES.indexOf(stage as (typeof STAGE_NAMES)[number]) : -1;
  return (
    <span style={{ display: "inline-flex", alignItems: "center", flexWrap: "wrap" }} data-testid="stage-track">
      {STAGE_NAMES.map((s, i) => (
        <span key={s} style={{ display: "inline-flex", alignItems: "center" }}>
          {i > 0 && <span style={{ color: "#94a3b8", fontSize: 10, padding: "0 3px" }}>→</span>}
          <span style={{
            fontSize: 11, fontWeight: 600, padding: "3px 9px", borderRadius: 10,
            background: i === idx ? "#2563eb" : i < idx ? "#eff6ff" : "#f1f5f9",
            color: i === idx ? "#fff" : i < idx ? "#2563eb" : "#94a3b8",
          }}>
            {s}
          </span>
        </span>
      ))}
    </span>
  );
}

export function StageChip({ stage }: { stage: string | null | undefined }) {
  if (!stage) return <Chip tone="line">not stamped</Chip>;
  return <Chip tone="line">{stage}</Chip>;
}

// ── Page furniture ──────────────────────────────────────────────────────

export function PageHead({
  title, lede, primary, p,
}: {
  title: string;
  lede?: ReactNode;
  primary?: ReactNode;
  p: Palette;
}) {
  return (
    <div style={{ display: "flex", alignItems: "flex-start", gap: 14, flexWrap: "wrap", marginBottom: 18 }}>
      <div style={{ flex: "1 1 320px", minWidth: 0 }}>
        <h1 style={{ fontSize: 22, fontWeight: 750, letterSpacing: "-0.01em", color: p.fg, margin: 0 }}>
          {title}
        </h1>
        {lede && (
          <p style={{ color: p.muted, marginTop: 4, maxWidth: "68ch", fontSize: 14, lineHeight: 1.45 }}>
            {lede}
          </p>
        )}
      </div>
      {primary}
    </div>
  );
}

export function PrimaryButton({
  children, onClick, disabled, testId,
}: {
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  testId?: string;
}) {
  return (
    <button
      data-testid={testId}
      onClick={onClick}
      disabled={disabled}
      style={{
        display: "inline-flex", alignItems: "center", gap: 7, padding: "8px 14px",
        borderRadius: 8, border: "1px solid #2563eb", background: "#2563eb",
        fontSize: 13, fontWeight: 600, color: "#fff", cursor: disabled ? "default" : "pointer",
        opacity: disabled ? 0.55 : 1, minHeight: 44,
      }}
    >
      {children}
    </button>
  );
}

export function QuietButton({
  children, onClick, disabled,
}: {
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        display: "inline-flex", alignItems: "center", gap: 7, padding: "8px 14px",
        borderRadius: 8, border: "1px solid #e5e7eb", background: "#fff",
        fontSize: 13, fontWeight: 600, color: "#111827", cursor: disabled ? "default" : "pointer",
        opacity: disabled ? 0.55 : 1, minHeight: 44,
      }}
    >
      {children}
    </button>
  );
}

export function SmallButton({
  children, onClick, disabled, primary,
}: {
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  primary?: boolean;
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      style={{
        display: "inline-flex", alignItems: "center", gap: 6, padding: "5px 10px",
        borderRadius: 8, fontSize: 12, fontWeight: 600, cursor: disabled ? "default" : "pointer",
        border: primary ? "1px solid #2563eb" : "1px solid #e5e7eb",
        background: primary ? "#2563eb" : "#fff",
        color: primary ? "#fff" : "#111827",
        opacity: disabled ? 0.55 : 1, minHeight: 32, flexShrink: 0,
      }}
    >
      {children}
    </button>
  );
}

export function Card({ p, children, style }: { p: Palette; children: ReactNode; style?: React.CSSProperties }) {
  return (
    <div style={{
      background: p.card, border: `1px solid ${p.border}`, borderRadius: 10,
      padding: "16px 18px", ...style,
    }}>
      {children}
    </div>
  );
}

export function CardTitle({ p, children, sub }: { p: Palette; children: ReactNode; sub?: ReactNode }) {
  return (
    <h3 style={{ fontSize: 13, fontWeight: 700, color: p.fg, margin: "0 0 8px" }}>
      {children}
      {sub && <span style={{ fontWeight: 400, color: p.muted, fontSize: 12 }}> — {sub}</span>}
    </h3>
  );
}

export function RowItem({ p, children, style }: { p: Palette; children: ReactNode; style?: React.CSSProperties }) {
  return (
    <div style={{
      display: "flex", gap: 12, padding: "12px 0",
      borderBottom: `1px solid ${p.borderSoft}`, alignItems: "flex-start", ...style,
    }}>
      {children}
    </div>
  );
}

export function RowTitle({ p, children }: { p: Palette; children: ReactNode }) {
  return <div style={{ fontWeight: 650, fontSize: 13.5, color: p.fg }}>{children}</div>;
}

export function RowMeta({ p, children, style }: { p: Palette; children: ReactNode; style?: React.CSSProperties }) {
  return <div style={{ fontSize: 12, color: p.muted, marginTop: 2, lineHeight: 1.5, ...style }}>{children}</div>;
}

/** The missing-act callout (wireframe pattern): names the human act owed. */
export function MissingAct({ children }: { children: ReactNode }) {
  return (
    <div style={{
      fontSize: 12, marginTop: 6, padding: "7px 10px", borderRadius: 7,
      background: "#fffbeb", color: "#92400e", lineHeight: 1.5,
    }}>
      {children}
    </div>
  );
}

// ── Tabs row (Evidence & sources / Data / Analysis / Reports) ───────────

export function TabsRow<T extends string>({
  tabs, active, onSelect, p,
}: {
  tabs: { id: T; label: string }[];
  active: T;
  onSelect: (t: T) => void;
  p: Palette;
}) {
  return (
    <div style={{ display: "flex", gap: 2, borderBottom: `1px solid ${p.border}`, marginBottom: 16, overflowX: "auto" }}>
      {tabs.map((t) => (
        <button
          key={t.id}
          onClick={() => onSelect(t.id)}
          style={{
            padding: "8px 14px", border: "none", background: "none", cursor: "pointer",
            fontSize: 13, whiteSpace: "nowrap",
            fontWeight: active === t.id ? 700 : 400,
            color: active === t.id ? p.accent : p.muted,
            borderBottom: `2px solid ${active === t.id ? p.accent : "transparent"}`,
            marginBottom: -1, minHeight: 44,
          }}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}

// ── Time helpers ────────────────────────────────────────────────────────

/** "5 h 50 m", "12 m", "3 d 2 h" — raw seconds are never shown (FR-007). */
export function humanizeUptime(totalSeconds: number): string {
  const sec = Math.max(0, Math.floor(totalSeconds));
  const d = Math.floor(sec / 86400);
  const h = Math.floor((sec % 86400) / 3600);
  const m = Math.floor((sec % 3600) / 60);
  if (d > 0) return `${d} d ${h} h`;
  if (h > 0) return `${h} h ${m} m`;
  if (m > 0) return `${m} m`;
  return "under a minute";
}

/** Local HH:MM clock for an ISO timestamp ("" when unparseable). */
export function fmtClock(iso: string | undefined | null): string {
  if (!iso) return "";
  const d = new Date(iso);
  if (isNaN(d.getTime())) return "";
  return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: false });
}

/** Local "Oct 29, 14:02" for an ISO timestamp. */
export function fmtDayTime(iso: string | undefined | null): string {
  if (!iso) return "—";
  const d = new Date(iso);
  if (isNaN(d.getTime())) return String(iso).slice(0, 10);
  return (
    d.toLocaleDateString([], { month: "short", day: "numeric" }) +
    ", " +
    d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", hour12: false })
  );
}
