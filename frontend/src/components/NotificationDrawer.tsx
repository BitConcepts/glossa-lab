/**
 * NotificationDrawer — persisted notification center.
 * Bell icon in header with unread badge. Slide-in drawer from right.
 * All notifications saved until cleared. Integrates with ToastProvider.
 */
import { useEffect, useRef } from "react";
import { type ToastType, useToast } from "../hooks/useToast";

const TYPE_ICONS: Record<ToastType, string> = {
  success: "✓",
  error: "✗",
  warning: "⚠",
  info: "ℹ",
};

const TYPE_COLORS: Record<ToastType, { bg: string; text: string; dot: string }> = {
  success: { bg: "#f0fdf4", text: "#16a34a", dot: "#16a34a" },
  error:   { bg: "#fef2f2", text: "#dc2626", dot: "#dc2626" },
  warning: { bg: "#fef3c7", text: "#d97706", dot: "#d97706" },
  info:    { bg: "#eff6ff", text: "#2563eb", dot: "#2563eb" },
};

function fmtTime(ts: number): string {
  const d = new Date(ts);
  const now = new Date();
  const diffMs = now.getTime() - d.getTime();
  const diffMin = Math.floor(diffMs / 60000);
  if (diffMin < 1) return "just now";
  if (diffMin < 60) return `${diffMin}m ago`;
  if (diffMin < 1440) return `${Math.floor(diffMin / 60)}h ago`;
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric" }) + " " +
    d.toLocaleTimeString(undefined, { hour: "2-digit", minute: "2-digit" });
}

interface Props {
  open: boolean;
  onClose: () => void;
}

export function NotificationDrawer({ open, onClose }: Props) {
  const { notifications, unreadCount: _uc, markAllRead, clearNotification, clearAllNotifications } = useToast();
  const drawerRef = useRef<HTMLDivElement>(null);

  // Mark as read when opened
  useEffect(() => {
    if (open) markAllRead();
  }, [open, markAllRead]);

  // Click-outside to close
  useEffect(() => {
    if (!open) return;
    const handler = (e: MouseEvent) => {
      if (drawerRef.current && !drawerRef.current.contains(e.target as Node)) {
        onClose();
      }
    };
    const timer = setTimeout(() => window.addEventListener("mousedown", handler), 50);
    return () => { clearTimeout(timer); window.removeEventListener("mousedown", handler); };
  }, [open, onClose]);

  if (!open) return null;

  return (
    <div
      ref={drawerRef}
      style={{
        position: "fixed", top: 0, right: 0, bottom: 0,
        width: 360, background: "#fff",
        boxShadow: "-4px 0 24px rgba(0,0,0,0.12)",
        zIndex: 7000, display: "flex", flexDirection: "column",
        borderLeft: "1px solid #e5e7eb",
        animation: "slideInRight 0.18s ease",
      }}
    >
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "14px 16px", borderBottom: "1px solid #e5e7eb", background: "#fafafa" }}>
        <div>
          <div style={{ fontWeight: 700, fontSize: 14, color: "#111827" }}>Notifications</div>
          <div style={{ fontSize: 11, color: "#9ca3af" }}>{notifications.length} total</div>
        </div>
        <div style={{ display: "flex", gap: 6 }}>
          {notifications.length > 0 && (
            <button onClick={clearAllNotifications} style={{ padding: "3px 10px", border: "1px solid #e5e7eb", borderRadius: 4, background: "#fff", cursor: "pointer", fontSize: 11, color: "#6b7280" }}>
              Clear All
            </button>
          )}
          <button onClick={onClose} style={{ border: "none", background: "none", cursor: "pointer", fontSize: 18, color: "#9ca3af", padding: "0 4px" }}>×</button>
        </div>
      </div>

      {/* List */}
      <div style={{ flex: 1, overflowY: "auto" }}>
        {notifications.length === 0 && (
          <div style={{ textAlign: "center", padding: "3rem 1rem", color: "#9ca3af" }}>
            <div style={{ fontSize: 28, marginBottom: 8 }}>🔔</div>
            <div style={{ fontSize: 13 }}>No notifications yet</div>
          </div>
        )}
        {notifications.map((n) => {
          const c = TYPE_COLORS[n.type] ?? TYPE_COLORS.info;
          return (
            <div
              key={n.id}
              style={{
                display: "flex", gap: 10, padding: "11px 14px",
                borderBottom: "1px solid #f3f4f6",
                background: n.read ? "#fff" : "#f8f9ff",
                alignItems: "flex-start",
              }}
            >
              <div style={{ width: 24, height: 24, borderRadius: "50%", background: c.bg, display: "flex", alignItems: "center", justifyContent: "center", flexShrink: 0, fontSize: 12, fontWeight: 700, color: c.text }}>
                {TYPE_ICONS[n.type]}
              </div>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 13, color: "#111827", lineHeight: 1.4, wordBreak: "break-word" }}>{n.message}</div>
                <div style={{ fontSize: 10, color: "#9ca3af", marginTop: 3 }}>{fmtTime(n.timestamp)}</div>
              </div>
              <button onClick={() => clearNotification(n.id)} style={{ border: "none", background: "none", cursor: "pointer", color: "#9ca3af", fontSize: 14, flexShrink: 0, padding: "0 2px" }}>×</button>
            </div>
          );
        })}
      </div>
      <style>{`@keyframes slideInRight { from { transform: translateX(100%); } to { transform: translateX(0); } }`}</style>
    </div>
  );
}

// ── Bell button (rendered in header) ─────────────────────────────────────────

export function NotificationBell({ onClick }: { onClick: () => void }) {
  const { unreadCount } = useToast();
  return (
    <button
      onClick={onClick}
      title={`Notifications${unreadCount > 0 ? ` (${unreadCount} unread)` : ""}`}
      style={{ position: "relative", padding: "4px 10px", border: "1px solid #e5e7eb", borderRadius: 6, background: "#f9fafb", cursor: "pointer", fontSize: 15, color: "#6b7280" }}
    >
      🔔
      {unreadCount > 0 && (
        <span style={{
          position: "absolute", top: -4, right: -4,
          minWidth: 16, height: 16, borderRadius: 8,
          background: "#dc2626", color: "#fff",
          fontSize: 9, fontWeight: 700,
          display: "flex", alignItems: "center", justifyContent: "center",
          padding: "0 3px",
        }}>
          {unreadCount > 99 ? "99+" : unreadCount}
        </span>
      )}
    </button>
  );
}
