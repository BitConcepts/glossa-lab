/**
 * Lightweight toast notification system + persistent notification history.
 * Usage: const { toast } = useToast();
 *        toast("Saved!", "success");
 * Notifications are also stored in a persistent history accessible via useNotifications().
 */
import { createContext, useCallback, useContext, useEffect, useRef, useState } from "react";

export type ToastType = "success" | "error" | "info" | "warning";

export interface Toast {
  id: number;
  message: string;
  type: ToastType;
}

export interface Notification {
  id: number;
  message: string;
  type: ToastType;
  timestamp: number;
  read: boolean;
}

interface ToastCtx {
  toast: (message: string, type?: ToastType, duration?: number) => void;
  notifications: Notification[];
  unreadCount: number;
  markAllRead: () => void;
  clearNotification: (id: number) => void;
  clearAllNotifications: () => void;
}

const ToastContext = createContext<ToastCtx>({
  toast: () => {},
  notifications: [],
  unreadCount: 0,
  markAllRead: () => {},
  clearNotification: () => {},
  clearAllNotifications: () => {},
});

let _counter = 0;

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const timers = useRef<Map<number, ReturnType<typeof setTimeout>>>(new Map());

  const dismiss = useCallback((id: number) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
    const t = timers.current.get(id);
    if (t) { clearTimeout(t); timers.current.delete(id); }
  }, []);

  const toast = useCallback((message: string, type: ToastType = "info", duration = 3500) => {
    const id = ++_counter;
    setToasts((prev) => [...prev.slice(-5), { id, message, type }]);
    // Also persist to notification history
    setNotifications((prev) => [
      { id, message, type, timestamp: Date.now(), read: false },
      ...prev.slice(0, 99), // keep max 100
    ]);
    const timer = setTimeout(() => dismiss(id), duration);
    timers.current.set(id, timer);
  }, [dismiss]);

  const markAllRead = useCallback(() =>
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true }))), []);

  const clearNotification = useCallback((id: number) =>
    setNotifications((prev) => prev.filter((n) => n.id !== id)), []);

  const clearAllNotifications = useCallback(() => setNotifications([]), []);

  const unreadCount = notifications.filter((n) => !n.read).length;

  useEffect(() => () => { timers.current.forEach(clearTimeout); }, []);

  const bg: Record<ToastType, string> = {
    success: "#16a34a", error: "#dc2626", info: "#2563eb", warning: "#d97706",
  };

  return (
    <ToastContext.Provider value={{ toast, notifications, unreadCount, markAllRead, clearNotification, clearAllNotifications }}>
      {children}
      <div style={{
        position: "fixed", bottom: 20, right: 20, display: "flex",
        flexDirection: "column", gap: 8, zIndex: 9999, pointerEvents: "none",
      }}>
        {toasts.map((t) => (
          <div
            key={t.id}
            style={{
              background: bg[t.type], color: "#fff",
              padding: "10px 16px", borderRadius: 8,
              fontSize: 13, fontWeight: 500,
              boxShadow: "0 4px 16px rgba(0,0,0,0.18)",
              display: "flex", alignItems: "center", gap: 10,
              pointerEvents: "auto", cursor: "pointer",
              animation: "slideIn 0.2s ease",
              maxWidth: 360,
            }}
            onClick={() => dismiss(t.id)}
          >
            <span style={{ flex: 1 }}>{t.message}</span>
            <span style={{ opacity: 0.7, fontSize: 16, flexShrink: 0 }}>×</span>
          </div>
        ))}
      </div>
      <style>{`@keyframes slideIn{from{transform:translateX(100%);opacity:0}to{transform:translateX(0);opacity:1}}`}</style>
    </ToastContext.Provider>
  );
}

export function useToast(): ToastCtx {
  return useContext(ToastContext);
}
