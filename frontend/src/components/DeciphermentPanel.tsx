/**
 * DeciphermentPanel — dashboard tile showing Indus script decipherment progress.
 *
 * Fetches from GET /api/v1/dashboard/decipherment and renders:
 *   - Current confidence level + weighted %
 *   - Progression sparkline (rounds)
 *   - Anchor breakdown (HIGH / MEDIUM / LOW)
 *   - Token coverage bar
 *   - Tamil-Brahmi correlation
 *   - "What Remains" list
 */

import { useEffect, useState } from "react";
import { getDashboardDecipherment, type DeciphermentProgress, type DeciphermentRound } from "../api";

const LEVEL_COLORS: Record<string, { bg: string; fg: string; border: string }> = {
  "NEAR-COMPLETE": { bg: "#dcfce7", fg: "#15803d", border: "#86efac" },
  "SUBSTANTIAL":   { bg: "#dbeafe", fg: "#1d4ed8", border: "#93c5fd" },
  "MODERATE":      { bg: "#fef3c7", fg: "#b45309", border: "#fcd34d" },
  "PARTIAL":       { bg: "#fce7f3", fg: "#be185d", border: "#f9a8d4" },
  "EARLY":         { bg: "#f3f4f6", fg: "#4b5563", border: "#d1d5db" },
};

function ProgressBar({ value, max = 100, color = "#3b82f6", label }: { value: number; max?: number; color?: string; label?: string }) {
  const pct = Math.min(100, (value / max) * 100);
  return (
    <div style={{ width: "100%", marginBottom: 4 }}>
      {label && <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 2 }}>{label}</div>}
      <div style={{ background: "#e5e7eb", borderRadius: 4, height: 14, overflow: "hidden", position: "relative" }}>
        <div style={{ width: `${pct}%`, background: color, height: "100%", borderRadius: 4, transition: "width 0.3s" }} />
        <span style={{ position: "absolute", right: 6, top: 0, fontSize: 10, lineHeight: "14px", color: pct > 60 ? "#fff" : "#374151", fontWeight: 600 }}>
          {value.toFixed(1)}%
        </span>
      </div>
    </div>
  );
}

function Sparkline({ data, width = 200, height = 40 }: { data: number[]; width?: number; height?: number }) {
  if (data.length < 2) return null;
  const minV = Math.min(...data) * 0.95;
  const maxV = Math.max(...data) * 1.05;
  const range = maxV - minV || 1;
  const step = width / (data.length - 1);
  const points = data.map((v, i) => `${i * step},${height - ((v - minV) / range) * height}`).join(" ");
  return (
    <svg width={width} height={height} style={{ display: "block" }}>
      <polyline points={points} fill="none" stroke="#3b82f6" strokeWidth={2} />
      {data.map((v, i) => (
        <circle key={i} cx={i * step} cy={height - ((v - minV) / range) * height} r={2.5} fill="#3b82f6" />
      ))}
    </svg>
  );
}

export function DeciphermentPanel() {
  const [data, setData] = useState<DeciphermentProgress | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getDashboardDecipherment()
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div style={{ padding: 16, color: "#9ca3af" }}>Loading decipherment metrics…</div>;
  if (error) return <div style={{ padding: 16, color: "#ef4444" }}>Error: {error}</div>;
  if (!data?.available) return null;

  const cur = data.current_state;
  const levelStyle = cur ? LEVEL_COLORS[cur.level] || LEVEL_COLORS.EARLY : LEVEL_COLORS.EARLY;
  const anchors = data.anchors;
  const byConf = anchors.by_confidence || {};

  return (
    <div style={{ border: `1px solid ${levelStyle.border}`, borderRadius: 8, padding: 16, background: "#fff", marginBottom: 16 }}>
      {/* Header */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
        <div>
          <span style={{ fontSize: 16, fontWeight: 700, color: "#111827" }}>🔤 Indus Script Decipherment</span>
          <span style={{
            marginLeft: 8, padding: "2px 8px", borderRadius: 4, fontSize: 11, fontWeight: 600,
            background: levelStyle.bg, color: levelStyle.fg,
          }}>
            {cur?.level || "N/A"} — {cur?.weighted_pct || 0}%
          </span>
        </div>
        <span style={{ fontSize: 12, color: "#6b7280" }}>{data.n_rounds} rounds</span>
      </div>

      {/* Metrics grid */}
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 12 }}>
        <div>
          <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 4 }}>Signs Assigned</div>
          <div style={{ fontSize: 20, fontWeight: 700, color: "#111827" }}>
            {cur?.signs_assigned || 0} <span style={{ fontSize: 13, color: "#9ca3af" }}>/ {cur?.signs_total || 390}</span>
          </div>
          <div style={{ fontSize: 11, marginTop: 2 }}>
            <span style={{ color: "#15803d", fontWeight: 600 }}>H:{byConf.HIGH || 0}</span>{" "}
            <span style={{ color: "#2563eb", fontWeight: 600 }}>M:{byConf.MEDIUM || 0}</span>{" "}
            <span style={{ color: "#d97706", fontWeight: 600 }}>L:{byConf.LOW || 0}</span>
          </div>
        </div>
        <div>
          <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 4 }}>Tamil-Brahmi Correlation</div>
          <div style={{ fontSize: 20, fontWeight: 700, color: (cur?.tamil_brahmi_corr || 0) > 0.7 ? "#15803d" : "#b45309" }}>
            {(cur?.tamil_brahmi_corr || 0).toFixed(3)}
          </div>
          <div style={{ fontSize: 11, color: "#6b7280" }}>
            {(cur?.tamil_brahmi_corr || 0) > 0.8 ? "Strong match" : (cur?.tamil_brahmi_corr || 0) > 0.5 ? "Moderate match" : "Weak match"}
          </div>
        </div>
      </div>

      {/* Progress bars */}
      <ProgressBar value={(cur?.token_coverage || 0) * 100} color="#3b82f6" label="Token Coverage" />
      <ProgressBar value={cur?.fully_decoded_pct || 0} color="#10b981" label="Inscriptions Fully Decoded" />
      <ProgressBar value={cur?.weighted_pct || 0} color="#8b5cf6" label="Weighted Confidence" />

      {/* Sparkline */}
      {data.progression.length >= 2 && (
        <div style={{ marginTop: 12 }}>
          <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 4 }}>Confidence Progression</div>
          <Sparkline data={data.progression.map(r => r.weighted_pct)} width={280} height={36} />
        </div>
      )}

      {/* What remains */}
      {cur?.remaining && cur.remaining.length > 0 && (
        <div style={{ marginTop: 12 }}>
          <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 4 }}>What Remains</div>
          <ul style={{ margin: 0, paddingLeft: 16, fontSize: 11, color: "#374151" }}>
            {cur.remaining.slice(0, 5).map((r, i) => <li key={i} style={{ marginBottom: 2 }}>{r}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}
