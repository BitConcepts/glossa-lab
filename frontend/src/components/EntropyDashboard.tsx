/**
 * EntropyDashboard — live entropy metrics for any corpus.
 * Shows H1, H2, conditional entropy, TTR, Zipf correlation, sparklines.
 * Supports comparing up to 3 corpora side-by-side.
 */
import { useEffect, useState } from "react";
import { getCorpusEntropy, listTexts, type EntropyResult, type TextResponse } from "../api";
import { useToast } from "../hooks/useToast";

function BarChart({ data, height = 120, color = "#2563eb" }: {
  data: { label: string; value: number }[]; height?: number; color?: string;
}) {
  if (!data.length) return null;
  const max = Math.max(...data.map(d => d.value), 1);
  const W = 600; const w = W / data.length;
  return (
    <svg viewBox={`0 0 ${W} ${height}`} style={{ width: "100%", height, display: "block" }}>
      {data.map((d, i) => {
        const bh = Math.max(2, (d.value / max) * (height - 20));
        return (
          <g key={i}>
            <rect x={i * w + 1} y={height - bh - 16} width={Math.max(2, w - 2)} height={bh} fill={color} opacity={0.85} rx={1} />
            {data.length <= 30 && (
              <text x={i * w + w / 2} y={height - 3} textAnchor="middle" fontSize={Math.min(9, w - 1)} fill="#6b7280">
                {d.label.slice(0, 4)}
              </text>
            )}
          </g>
        );
      })}
    </svg>
  );
}

function Sparkline({ values, color = "#2563eb", label = "" }: { values: number[]; color?: string; label?: string }) {
  if (values.length < 2) return null;
  const h = 60; const W = 400;
  const max = Math.max(...values); const min = Math.min(...values);
  const range = max - min || 1;
  const step = W / (values.length - 1);
  const pts = values.map((v, i) => `${i * step},${h - ((v - min) / range) * (h - 4) - 2}`).join(" ");
  return (
    <div>
      {label && <div style={{ fontSize: 10, color: "#9ca3af", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 2 }}>{label}</div>}
      <svg viewBox={`0 0 ${W} ${h}`} style={{ width: "100%", height: h, display: "block" }}>
        <polyline points={pts} fill="none" stroke={color} strokeWidth={1.5} />
        <text x={0} y={8} fontSize={8} fill="#9ca3af">{max.toFixed(2)}</text>
        <text x={0} y={h - 2} fontSize={8} fill="#9ca3af">{min.toFixed(2)}</text>
      </svg>
    </div>
  );
}

const COLORS = ["#2563eb", "#7c3aed", "#16a34a", "#d97706", "#dc2626"];

interface Slot { textId: string; entropy: EntropyResult | null; loading: boolean; name: string; }

export function EntropyDashboard() {
  const { toast } = useToast();
  const [texts, setTexts] = useState<TextResponse[]>([]);
  const [slots, setSlots] = useState<Slot[]>([{ textId: "", entropy: null, loading: false, name: "" }]);

  useEffect(() => {
    listTexts().then(setTexts).catch(() => {});
  }, []);

  const addSlot = () => {
    if (slots.length >= 5) return;
    setSlots((s) => [...s, { textId: "", entropy: null, loading: false, name: "" }]);
  };

  const removeSlot = (i: number) => setSlots((s) => s.filter((_, j) => j !== i));

  const loadSlot = async (i: number, textId: string) => {
    const t = texts.find((x) => x.id === textId);
    setSlots((s) => s.map((slot, j) => j === i ? { ...slot, textId, loading: true, name: t?.name ?? textId, entropy: null } : slot));
    try {
      const e = await getCorpusEntropy(textId);
      setSlots((s) => s.map((slot, j) => j === i ? { ...slot, loading: false, entropy: e } : slot));
    } catch (err) {
      toast(err instanceof Error ? err.message : "Failed", "error");
      setSlots((s) => s.map((slot, j) => j === i ? { ...slot, loading: false } : slot));
    }
  };

  const loaded = slots.filter((s) => s.entropy);

  const metrics: Array<{ key: keyof EntropyResult; label: string; unit: string; color: string; desc: string }> = [
    { key: "h1", label: "H1 Entropy", unit: "bits", color: "#2563eb", desc: "Unigram Shannon entropy" },
    { key: "conditional_h", label: "Cond. Entropy", unit: "bits", color: "#7c3aed", desc: "H(X|X-1) — predictability" },
    { key: "h2_h1_ratio", label: "H2/H1 Ratio", unit: "", color: "#d97706", desc: "~1.5 for natural language" },
    { key: "type_token_ratio", label: "TTR", unit: "", color: "#16a34a", desc: "Lexical diversity" },
    { key: "zipf_correlation", label: "Zipf ρ", unit: "", color: "#6b7280", desc: "Rank-freq correlation (−1 ideal)" },
  ];

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "0.75rem" }}>
        <h2 style={{ margin: 0 }}>Entropy Dashboard</h2>
        {slots.length < 5 && (
          <button onClick={addSlot} style={{ padding: "4px 12px", background: "#1e3a5f", color: "#fff", border: "none", borderRadius: 4, fontSize: 12, cursor: "pointer" }}>
            + Add Corpus
          </button>
        )}
      </div>

      <p style={{ margin: "0 0 1rem", fontSize: 13, color: "#6b7280" }}>
        Select up to 5 corpora to compare entropy and linguistic statistics side-by-side.
      </p>

      {/* Corpus selectors */}
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap", marginBottom: "1.5rem" }}>
        {slots.map((slot, i) => (
          <div key={i} style={{ display: "flex", gap: 6, alignItems: "center", padding: "8px 12px", border: `2px solid ${COLORS[i]}40`, borderRadius: 8, background: COLORS[i] + "08" }}>
            <span style={{ width: 10, height: 10, borderRadius: "50%", background: COLORS[i], flexShrink: 0 }} />
            <select
              value={slot.textId}
              onChange={(e) => { if (e.target.value) loadSlot(i, e.target.value); }}
              style={{ padding: "4px 8px", border: "1px solid #d1d5db", borderRadius: 4, fontSize: 12, background: "#fff" }}
            >
              <option value="">— select corpus —</option>
              {texts.map((t) => <option key={t.id} value={t.id}>{t.name} ({t.corpus_type})</option>)}
            </select>
            {slot.loading && <span style={{ fontSize: 11, color: "#6b7280" }}>Loading…</span>}
            {slots.length > 1 && (
              <button onClick={() => removeSlot(i)} style={{ border: "none", background: "none", cursor: "pointer", color: "#9ca3af", fontSize: 14 }}>×</button>
            )}
          </div>
        ))}
      </div>

      {/* Metric comparison */}
      {loaded.length > 0 && (
        <>
          <div style={{ overflowX: "auto", marginBottom: "1.5rem" }}>
            <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 13 }}>
              <thead>
                <tr>
                  <th style={{ textAlign: "left", padding: "8px 12px 8px 0", borderBottom: "2px solid #e5e7eb", color: "#374151" }}>Metric</th>
                  {loaded.map((s, i) => (
                    <th key={i} style={{ textAlign: "right", padding: "8px 12px 8px 0", borderBottom: "2px solid #e5e7eb" }}>
                      <span style={{ color: COLORS[slots.indexOf(s)] }}>{s.name.slice(0, 20)}</span>
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {metrics.map(({ key, label, unit }) => (
                  <tr key={key}>
                    <td style={{ padding: "6px 12px 6px 0", borderBottom: "1px solid #f3f4f6", fontWeight: 600, color: "#374151" }}>{label}</td>
                    {loaded.map((s, i) => {
                      const v = s.entropy?.[key];
                      const fmt = typeof v === "number" ? (Number.isInteger(v) ? v.toLocaleString() : v.toFixed(4)) : "—";
                      return (
                        <td key={i} style={{ padding: "6px 12px 6px 0", borderBottom: "1px solid #f3f4f6", textAlign: "right", fontFamily: "monospace", color: COLORS[slots.indexOf(s)] }}>
                          {fmt} <span style={{ fontSize: 10, color: "#9ca3af" }}>{unit}</span>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Charts per corpus */}
          {loaded.map((s, ci) => {
            const color = COLORS[slots.indexOf(s)];
            return (
              <div key={ci} style={{ marginBottom: "1.5rem", border: "1px solid #e5e7eb", borderRadius: 8, overflow: "hidden" }}>
                <div style={{ background: color + "15", padding: "10px 16px", borderBottom: "1px solid #e5e7eb", display: "flex", gap: 8, alignItems: "center" }}>
                  <span style={{ width: 10, height: 10, borderRadius: "50%", background: color, flexShrink: 0 }} />
                  <strong style={{ color, fontSize: 13 }}>{s.name}</strong>
                  <span style={{ fontSize: 12, color: "#6b7280" }}>
                    {s.entropy!.token_count.toLocaleString()} tokens · alphabet {s.entropy!.type_count}
                  </span>
                </div>
                <div style={{ padding: "14px 16px" }}>
                  <div style={{ marginBottom: 12 }}>
                    <div style={{ fontSize: 11, fontWeight: 700, color: "#9ca3af", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 6 }}>
                      Token Frequency (top 30)
                    </div>
                    <BarChart
                      data={s.entropy!.zipf_table.slice(0, 30).map(d => ({ label: d.token, value: d.freq }))}
                      color={color} height={110}
                    />
                  </div>
                  <Sparkline
                    values={s.entropy!.zipf_table.map(d => d.log_freq)}
                    color={color}
                    label="Zipf: log-rank vs log-frequency"
                  />
                </div>
              </div>
            );
          })}
        </>
      )}

      {loaded.length === 0 && (
        <div style={{ textAlign: "center", padding: "2rem", color: "#9ca3af", fontSize: 14 }}>
          <div style={{ fontSize: 32, marginBottom: 8 }}>📊</div>
          Select a corpus above to compute entropy metrics
        </div>
      )}
    </div>
  );
}
