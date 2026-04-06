/**
 * CommandPalette — Cmd+K / Ctrl+K command palette.
 * Fuzzy search over all tabs and common actions.
 */
import { useEffect, useRef, useState } from "react";

export interface PaletteCommand {
  id: string;
  label: string;
  description?: string;
  icon?: string;
  action: () => void;
}

interface Props {
  commands: PaletteCommand[];
  onClose: () => void;
}

export function CommandPalette({ commands, onClose }: Props) {
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState(0);
  const inputRef = useRef<HTMLInputElement>(null);

  const filtered = commands.filter((c) =>
    !query || c.label.toLowerCase().includes(query.toLowerCase()) ||
    c.description?.toLowerCase().includes(query.toLowerCase())
  );

  useEffect(() => {
    inputRef.current?.focus();
    setSelected(0);
  }, []);

  useEffect(() => {
    setSelected(0);
  }, [query]);

  const run = (cmd: PaletteCommand) => {
    cmd.action();
    onClose();
  };

  const handleKey = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowDown") { e.preventDefault(); setSelected((s) => Math.min(s + 1, filtered.length - 1)); }
    if (e.key === "ArrowUp") { e.preventDefault(); setSelected((s) => Math.max(s - 1, 0)); }
    if (e.key === "Enter" && filtered[selected]) run(filtered[selected]);
    if (e.key === "Escape") onClose();
  };

  return (
    <div
      style={{
        position: "fixed", inset: 0, background: "rgba(0,0,0,0.5)",
        display: "flex", alignItems: "flex-start", justifyContent: "center",
        paddingTop: "15vh", zIndex: 9000,
      }}
      onClick={(e) => { if (e.target === e.currentTarget) onClose(); }}
    >
      <div style={{
        width: 580, maxWidth: "95vw", background: "#fff", borderRadius: 12,
        boxShadow: "0 25px 60px rgba(0,0,0,0.25)", overflow: "hidden",
      }}>
        <div style={{ padding: "12px 16px", borderBottom: "1px solid #f3f4f6", display: "flex", alignItems: "center", gap: 8 }}>
          <span style={{ color: "#9ca3af", fontSize: 16 }}>⌘</span>
          <input
            ref={inputRef}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKey}
            placeholder="Search commands…"
            style={{ flex: 1, border: "none", outline: "none", fontSize: 15, color: "#111827" }}
          />
          <kbd style={{ padding: "2px 6px", background: "#f3f4f6", borderRadius: 4, fontSize: 11, color: "#6b7280", border: "1px solid #e5e7eb" }}>ESC</kbd>
        </div>

        <div style={{ maxHeight: 400, overflowY: "auto" }}>
          {filtered.length === 0 && (
            <div style={{ padding: "20px 16px", textAlign: "center", color: "#9ca3af", fontSize: 13 }}>
              No commands found for "{query}"
            </div>
          )}
          {filtered.map((cmd, i) => (
            <div
              key={cmd.id}
              onClick={() => run(cmd)}
              onMouseEnter={() => setSelected(i)}
              style={{
                display: "flex", gap: 12, alignItems: "center",
                padding: "10px 16px", cursor: "pointer",
                background: selected === i ? "#f5f3ff" : "#fff",
                borderLeft: selected === i ? "2px solid #7c3aed" : "2px solid transparent",
              }}
            >
              {cmd.icon && <span style={{ fontSize: 16, width: 20, textAlign: "center", flexShrink: 0 }}>{cmd.icon}</span>}
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ fontSize: 13, fontWeight: 500, color: "#111827" }}>{cmd.label}</div>
                {cmd.description && <div style={{ fontSize: 11, color: "#9ca3af" }}>{cmd.description}</div>}
              </div>
              {selected === i && (
                <kbd style={{ padding: "2px 6px", background: "#f3f4f6", borderRadius: 4, fontSize: 10, color: "#6b7280", border: "1px solid #e5e7eb", flexShrink: 0 }}>↵</kbd>
              )}
            </div>
          ))}
        </div>

        <div style={{ padding: "8px 16px", borderTop: "1px solid #f3f4f6", display: "flex", gap: 12, fontSize: 11, color: "#9ca3af" }}>
          <span>↑↓ Navigate</span>
          <span>↵ Open</span>
          <span>ESC Close</span>
        </div>
      </div>
    </div>
  );
}
