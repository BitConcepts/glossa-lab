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
import { getDashboardDecipherment, type DeciphermentProgress } from "../api";

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
  const byConf = data.anchors.by_confidence || {};

  // Archived = no round progression AND no current_state (works with both old and
  // new backend responses — old backend omits the `archived` field but still
  // returns current_state: null when the V8-V24 round files are gone).
  const isArchived = data.archived || (data.n_rounds === 0 && !data.current_state && data.anchors.total > 0);

  if (isArchived) {
    const totalSigns  = data.anchors.corpus_signs  ?? 390;
    const totalAnchors = data.anchors.total_all ?? totalSigns;
    const icitTotal   = (data.anchors as any).icit_total_signs ?? 0;
    // When ICIT inventory is known, show coverage against the full 713-sign catalogue
    const coverageDenom = icitTotal > 0 ? icitTotal : totalAnchors;
    const high        = byConf.HIGH   ?? 0;
    const medium      = byConf.MEDIUM ?? 0;
    const candidate   = byConf.CANDIDATE ?? 0;
    const nHM         = high + medium;
    const tokenCovPct = Math.round((data.anchors.corpus_token_coverage ?? 0) * 100);
    const hmSignPct   = Math.round((nHM / coverageDenom) * 100);
    const highSignPct = Math.round((high / coverageDenom) * 100);
    const currentPhase = (data as any).current_phase ?? 0;
    const saAggregate  = (data as any).sa_aggregate ?? 0;
    const nEvidence    = (data as any).n_evidence_items ?? 0;
    const fullyDecPct  = Math.round(((data as any).fully_decoded_pct ?? 0) * 100);
    const nFullyDec    = (data as any).n_fully_decoded ?? 0;
    const totalSeals   = (data as any).total_seals ?? 1670;

    // Determine status badge — show research phase, not coverage (coverage is in bars)
    const statusBg = "#dbeafe";
    const statusFg = "#1d4ed8";
    const statusText = `🔬 Active Research — Phase ${currentPhase}`;

    return (
      <div style={{ border: "1px solid #d1d5db", borderRadius: 8, padding: 16, background: "#fff", marginBottom: 16 }}>

        {/* Header */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 10 }}>
          <div>
            <span style={{ fontSize: 16, fontWeight: 700, color: "#111827" }}>🔤 Indus Script Decipherment</span>
            <span style={{
              marginLeft: 8, padding: "2px 8px", borderRadius: 4,
              fontSize: 11, fontWeight: 600,
              background: statusBg, color: statusFg, border: `1px solid ${statusBg}`,
            }}>{statusText}</span>
          </div>
          {nEvidence > 0 && (
            <span style={{ fontSize: 12, color: "#6b7280" }}>{nEvidence} evidence items</span>
          )}
        </div>

        {/* Metrics grid — 4 key numbers a researcher needs */}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr 1fr", gap: 10, marginBottom: 12 }}>
          <div>
            <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 4 }}>Anchor Coverage</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: nHM >= coverageDenom ? "#15803d" : "#111827" }}>
              {nHM}<span style={{ fontSize: 13, color: "#9ca3af" }}>/{coverageDenom}</span>
            </div>
            <div style={{ fontSize: 11, marginTop: 2 }}>
              <span style={{ color: "#15803d", fontWeight: 600 }}>H:{high}</span>{" "}
              <span style={{ color: "#2563eb", fontWeight: 600 }}>M:{medium}</span>
              {candidate > 0 && <span style={{ color: "#d97706", fontWeight: 600 }}> C:{candidate}</span>}
            </div>
          </div>
          <div>
            <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 4 }}>Token Coverage</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: tokenCovPct >= 85 ? "#15803d" : "#b45309" }}>
              {tokenCovPct}%
            </div>
            <div style={{ fontSize: 11, color: "#6b7280" }}>of 7,002 tokens</div>
          </div>
          <div>
            <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 4 }}>SA Confidence</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: saAggregate >= 0.5 ? "#15803d" : "#b45309" }}>
              {saAggregate > 0 ? `${Math.round(saAggregate * 100)}%` : "—"}
            </div>
            <div style={{ fontSize: 11, color: "#6b7280" }}>aggregate</div>
          </div>
          <div>
            <div style={{ fontSize: 11, color: "#6b7280", marginBottom: 4 }}>Seals Decoded</div>
            <div style={{ fontSize: 20, fontWeight: 700, color: fullyDecPct >= 65 ? "#15803d" : "#b45309" }}>
              {fullyDecPct > 0 ? `${fullyDecPct}%` : "—"}
            </div>
            <div style={{ fontSize: 11, color: "#6b7280" }}>{nFullyDec > 0 ? `${nFullyDec.toLocaleString()}/${totalSeals.toLocaleString()}` : ""}</div>
          </div>
        </div>

        {/* Progress bars */}
        <ProgressBar value={tokenCovPct}  color="#059669" label={`Token coverage (${tokenCovPct}% of 7,002 corpus tokens)`} />
        <ProgressBar value={hmSignPct}    color="#3b82f6" label={`H+M anchor coverage (${nHM}/${coverageDenom} sign readings confirmed)`} />
        <ProgressBar value={highSignPct}  color="#15803d" label={`HIGH confidence (${high} signs — SA + DEDR + external corroboration)`} />

        {/* ICIT 2026 inventory coverage */}
        {(data.anchors as any).icit_total_signs && (
          <ProgressBar
            value={Math.round(((data.anchors as any).icit_coverage_pct ?? 0) * 100)}
            color="#8b5cf6"
            label={`ICIT 2026 inventory coverage (${totalAnchors}/${(data.anchors as any).icit_total_signs} signs — ${Math.round(((data.anchors as any).icit_coverage_pct ?? 0) * 100)}%)`}
          />
        )}

        {/* Munda SA discrimination badge */}
        {(data as any).munda_sa && (
          <div style={{ marginTop: 8, padding: "6px 10px", borderRadius: 6, background: "#fef3c7", border: "1px solid #fbbf24", fontSize: 11 }}>
            <span style={{ fontWeight: 600, color: "#92400e" }}>⚖️ Competing LM Test (Phase 300):</span>{" "}
            Dravidian {Math.round(((data as any).munda_sa.dravidian_consistency ?? 0) * 100)}% vs
            Munda {Math.round(((data as any).munda_sa.munda_consistency ?? 0) * 100)}% vs
            Hebrew {Math.round(0.697 * 100)}% — 
            <span style={{ fontWeight: 600 }}>
              {(data as any).munda_sa.discriminative ? "SA non-discriminative" : "SA non-discriminative"}
            </span>
            {" "}(anchored SA provides the real signal)
          </div>
        )}

        {/* Archaeological context badge */}
        {(data as any).archaeology && (
          <div style={{ marginTop: 6, padding: "6px 10px", borderRadius: 6, background: "#ecfdf5", border: "1px solid #6ee7b7", fontSize: 11 }}>
            <span style={{ fontWeight: 600, color: "#065f46" }}>🏛️ Archaeological Context (Phase 302):</span>{" "}
            Guild-identity model scores {(data as any).archaeology.score_pct}% across 9 sites —
            <span style={{ fontWeight: 600 }}> {(data as any).archaeology.verdict}</span>
          </div>
        )}

        {/* Status footer */}
        <div style={{ marginTop: 10, fontSize: 11, color: "#6b7280" }}>
          {(data.anchors as any).icit_total_signs
            ? `${totalAnchors} of ${(data.anchors as any).icit_total_signs} ICIT signs have proposed readings (${high} HIGH, ${medium} MEDIUM). The ICIT corpus was updated to 713 signs with corrected inscriptions in 2026 (Fuls, personal communication); ${(data.anchors as any).icit_total_signs - totalAnchors} signs in the 2026 revision were not in the publicly accessible version.`
            : nHM >= totalAnchors
              ? `All ${totalAnchors} signs have proposed readings (${high} HIGH, ${medium} MEDIUM).`
              : `${totalAnchors - nHM} sign(s) remaining without proposed readings.`
          }
        </div>
      </div>
    );
  }

  const cur = data.current_state;
  const levelStyle = cur ? LEVEL_COLORS[cur.level] || LEVEL_COLORS.EARLY : LEVEL_COLORS.EARLY;

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
