/**
 * useContextMenu — right-click context menu for copy/paste/select-all.
 * Attach via onContextMenu={show} and render <ContextMenu /> wherever needed.
 */
import { useCallback, useEffect, useState } from "react";

export interface ContextMenuItem {
  label: string;
  icon?: string;
  action: () => void;
  disabled?: boolean;
}

interface ContextMenuState {
  x: number;
  y: number;
  items: ContextMenuItem[];
}

export function useContextMenu() {
  const [menu, setMenu] = useState<ContextMenuState | null>(null);

  const show = useCallback((e: React.MouseEvent, items: ContextMenuItem[]) => {
    e.preventDefault();
    e.stopPropagation();
    const x = Math.min(e.clientX, window.innerWidth - 180);
    const y = Math.min(e.clientY, window.innerHeight - items.length * 34 - 8);
    setMenu({ x, y, items });
  }, []);

  const close = useCallback(() => setMenu(null), []);

  useEffect(() => {
    if (!menu) return;
    const handler = () => setMenu(null);
    window.addEventListener("click", handler, { once: true });
    window.addEventListener("keydown", (e) => { if (e.key === "Escape") setMenu(null); }, { once: true });
    return () => window.removeEventListener("click", handler);
  }, [menu]);

  return { menu, show, close };
}

export function ContextMenuOverlay({ menu, onClose }: {
  menu: ContextMenuState | null;
  onClose: () => void;
}) {
  if (!menu) return null;
  return (
    <div
      style={{
        position: "fixed", left: menu.x, top: menu.y,
        background: "#fff", border: "1px solid #e5e7eb", borderRadius: 6,
        boxShadow: "0 8px 24px rgba(0,0,0,0.12)", zIndex: 8000,
        minWidth: 160, padding: "4px 0", fontSize: 13,
      }}
      onClick={(e) => e.stopPropagation()}
    >
      {menu.items.map((item, i) => (
        <div
          key={i}
          onClick={() => { if (!item.disabled) { item.action(); onClose(); } }}
          style={{
            padding: "7px 14px", cursor: item.disabled ? "not-allowed" : "pointer",
            display: "flex", alignItems: "center", gap: 8,
            color: item.disabled ? "#9ca3af" : "#111827",
            background: "transparent",
          }}
          onMouseEnter={(e) => { if (!item.disabled) (e.currentTarget as HTMLDivElement).style.background = "#f3f4f6"; }}
          onMouseLeave={(e) => { (e.currentTarget as HTMLDivElement).style.background = "transparent"; }}
        >
          {item.icon && <span style={{ fontSize: 14, width: 16 }}>{item.icon}</span>}
          {item.label}
        </div>
      ))}
    </div>
  );
}

/** Convenience: build Copy/Select-All items for a text value */
export function copyItems(text: string, label = "Copy"): ContextMenuItem[] {
  return [
    {
      label,
      icon: "⎘",
      action: () => navigator.clipboard.writeText(text).catch(() => {}),
    },
    {
      label: "Copy All (plain text)",
      icon: "📋",
      action: () => navigator.clipboard.writeText(text).catch(() => {}),
    },
  ];
}
