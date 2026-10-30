/**
 * Claims surface (Spec 081 step 3, T015; wireframes 03–04; FR-018).
 *
 * The program-scoped claims register + claim detail, consuming the
 * /programs/{id} endpoints (the /indus-evidence paths are the
 * one-release shim). The register keeps the two kinds of standing in
 * separate columns, as the wireframe draws them: the machine verdict
 * (lane 1) and the human settlement stage (lane 2) — never merged
 * into one score or one word.
 *
 * Hypotheses fold into this register (Q7 ruling): a hypothesis is a
 * claim whose falsifier is not yet sharp, shown here as an
 * early-state entry — not as a separate tracker, and never dressed
 * as a tested claim.
 *
 * Registration: a claim enters this register by registering its
 * source in Evidence & sources, where extraction states the
 * falsifier the claim stands or falls by; a claim without one
 * cannot be entered. There is no direct-entry form, because the
 * register's records are extracted claims with their source
 * provenance — the doorway below states this rather than faking a
 * write path the API does not have.
 *
 * IndusEvidenceView keeps its own claims tab (and its Spec 029
 * source pin) until step 6 consolidates Evidence & sources.
 */
import { useEffect, useMemo, useState, type CSSProperties } from "react";
import {
  getProgramClaimTrail,
  listProgramClaims,
  listProgramHypotheses,
  type ClaimTrail,
  type IndusClaim,
  type IndusHypothesisModel,
} from "../api";
import { useProject } from "../hooks/useProject";
import { effectiveStage, missingActFor } from "./DigestionBoard";
import { NotUnderstood } from "./StageLegend";
import {
  Card,
  Chip,
  MissingAct,
  PageHead,
  PrimaryButton,
  QuietButton,
  StageChip,
  StageTrack,
  fmtDayTime,
  palette,
  verdictOf,
  type ChipTone,
} from "./ui081";

type Route = "evidence";

export function ClaimsView({
  darkMode,
  onNavigate,
}: {
  darkMode: boolean;
  onNavigate: (route: Route) => void;
}) {
  const p = palette(darkMode);
  const { activeProject } = useProject();
  const programId = activeProject?.id ?? null;

  const [claims, setClaims] = useState<IndusClaim[] | null>(null);
  const [total, setTotal] = useState<number | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [hypotheses, setHypotheses] = useState<IndusHypothesisModel[]>([]);
  const [filter, setFilter] = useState<string>("all");
  const [query, setQuery] = useState("");
  const [compact, setCompact] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [selected, setSelected] = useState<IndusClaim | null>(null);
  const [trail, setTrail] = useState<ClaimTrail | null>(null);
  const [trailError, setTrailError] = useState<string | null>(null);

  useEffect(() => {
    if (!programId) return;
    let cancelled = false;
    listProgramClaims(programId, { limit: 500 })
      .then((r) => {
        if (cancelled) return;
        setClaims(r.claims);
        setTotal(r.total);
        // Digestion-board doorway: a card click records the claim to
        // open here (step 3 lands the deep link PR-4 deferred).
        try {
          const want = sessionStorage.getItem("glossa_open_claim");
          if (want) {
            sessionStorage.removeItem("glossa_open_claim");
            const hit = r.claims.find((c) => c.claim_id === want);
            if (hit) setSelected(hit);
          }
        } catch { /* sessionStorage unavailable — the register still works */ }
      })
      .catch((e) => {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "The claims register did not answer.");
        }
      });
    listProgramHypotheses(programId)
      .then((r) => { if (!cancelled) setHypotheses(r.models); })
      .catch(() => { /* hypotheses are a fold-in; their absence is not an error state */ });
    return () => { cancelled = true; };
  }, [programId]);

  useEffect(() => {
    if (!selected || !programId) {
      setTrail(null);
      setTrailError(null);
      return;
    }
    let cancelled = false;
    setTrail(null);
    setTrailError(null);
    getProgramClaimTrail(programId, selected.claim_id)
      .then((r) => { if (!cancelled) setTrail(r); })
      .catch((e) => {
        if (!cancelled) {
          setTrailError(e instanceof Error ? e.message : "The claim trail did not answer.");
        }
      });
    return () => { cancelled = true; };
  }, [selected, programId]);

  const verdictGroups = useMemo(() => {
    if (!claims) return [];
    const counts = new Map<string, { label: string; tone: ChipTone; n: number }>();
    for (const c of claims) {
      const v = verdictOf(c.claim_status);
      const cur = counts.get(v.label) ?? { label: v.label, tone: v.tone, n: 0 };
      cur.n += 1;
      counts.set(v.label, cur);
    }
    return [...counts.values()].sort((a, b) => b.n - a.n);
  }, [claims]);

  const visible = useMemo(() => {
    if (!claims) return [];
    const q = query.trim().toLowerCase();
    return claims.filter((c) => {
      if (filter !== "all" && verdictOf(c.claim_status).label !== filter) return false;
      if (q && !`${c.normalized_claim} ${c.claim_id}`.toLowerCase().includes(q)) return false;
      return true;
    });
  }, [claims, filter, query]);

  if (!programId) {
    return (
      <div data-testid="claims-surface">
        <PageHead p={p} title="Claims" lede="No active program — claims belong to a program." />
      </div>
    );
  }

  if (selected) {
    return (
      <ClaimDetail
        claim={selected}
        trail={trail}
        trailError={trailError}
        darkMode={darkMode}
        onBack={() => setSelected(null)}
      />
    );
  }

  const cellPad = compact ? "6px 10px" : "10px 12px";
  const rowFont = compact ? 12 : 12.5;

  const th: CSSProperties = {
    textAlign: "left", fontSize: 11, fontWeight: 700, color: p.muted,
    textTransform: "uppercase", letterSpacing: 0.4, padding: cellPad,
  };
  const td: CSSProperties = {
    padding: cellPad, fontSize: rowFont, color: p.fg,
    borderTop: `1px solid ${p.borderSoft}`, verticalAlign: "top",
  };

  return (
    <div data-testid="claims-surface">
      <PageHead
        p={p}
        title="Claims"
        lede={
          "Every claim is registered with the evidence that could prove it wrong (its " +
          "falsifier). A claim without one is not a claim here — it cannot be entered. " +
          "Machine checks give a verdict; people settle claims through digestion, in " +
          "five stages: created, checked, explained, accepted, digested."
        }
        primary={
          <PrimaryButton onClick={() => setShowRegister((s) => !s)}>
            + Register a claim
          </PrimaryButton>
        }
      />

      {showRegister && (
        <Card p={p} style={{ padding: 16, marginBottom: 14 }}>
          <div style={{ fontSize: 13.5, fontWeight: 600, color: p.fg, marginBottom: 4 }}>
            How a claim enters this register
          </div>
          <div style={{ fontSize: 12.5, color: p.muted, lineHeight: 1.55, marginBottom: 10 }}>
            A claim is registered by registering its source in Evidence &amp; sources:
            extraction reads the source and states each claim with the falsifier it
            stands or falls by. Claims are never typed in directly — a register entry
            without its source and its falsifier would be a claim this program could
            not check, so the register does not offer one.
          </div>
          <QuietButton onClick={() => onNavigate("evidence")}>
            Open Evidence &amp; sources →
          </QuietButton>
        </Card>
      )}

      <div
        style={{
          display: "flex", flexWrap: "wrap", gap: 6, alignItems: "center",
          marginBottom: 12,
        }}
      >
        <button
          type="button"
          onClick={() => setFilter("all")}
          style={filterChipStyle(p, filter === "all")}
        >
          {`All · ${total ?? "—"}`}
        </button>
        {verdictGroups.map((g) => (
          <button
            key={g.label}
            type="button"
            onClick={() => setFilter(g.label)}
            style={filterChipStyle(p, filter === g.label)}
          >
            {`${g.label} · ${g.n}`}
          </button>
        ))}
        <span style={{ flex: 1 }} />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search claims…"
          aria-label="Search claims"
          style={{
            padding: "6px 10px", fontSize: 12.5, borderRadius: 8,
            border: `1px solid ${p.border}`, background: "transparent", color: p.fg,
            fontFamily: "inherit", minWidth: 180,
          }}
        />
        <label
          style={{
            display: "flex", gap: 6, alignItems: "center",
            fontSize: 12.5, color: p.muted, cursor: "pointer",
          }}
        >
          <input
            type="checkbox"
            checked={compact}
            onChange={(e) => setCompact(e.target.checked)}
          />
          Compact
        </label>
      </div>

      {error ? (
        <div style={{ fontSize: 12.5, color: p.bad }}>{`This instance states: ${error}`}</div>
      ) : !claims ? (
        <div style={{ fontSize: 12.5, color: p.muted }}>Loading…</div>
      ) : (
        <Card p={p} style={{ padding: 0, overflow: "hidden" }}>
          <table style={{ width: "100%", borderCollapse: "collapse" }}>
            <thead>
              <tr>
                <th style={th}>Claim</th>
                <th style={th}>Falsifier — what would prove it wrong</th>
                <th style={th}>Verdict (machine checks)</th>
                <th style={th}>Digestion (human settlement)</th>
              </tr>
            </thead>
            <tbody>
              {visible.map((c) => {
                const v = verdictOf(c.claim_status);
                const stage = effectiveStage(c);
                return (
                  <tr
                    key={c.claim_id}
                    onClick={() => setSelected(c)}
                    style={{ cursor: "pointer" }}
                    data-testid="claim-row"
                  >
                    <td style={td}>
                      <div style={{ fontWeight: 600, overflowWrap: "anywhere" }}>
                        {c.normalized_claim}
                      </div>
                      <div style={{ fontSize: 11.5, color: p.muted, marginTop: 2 }}>
                        {`${c.claim_id} · ${c.claim_type}`}
                      </div>
                    </td>
                    <td style={{ ...td, color: p.muted }}>
                      {c.falsification_condition?.trim()
                        ? c.falsification_condition
                        : "No falsifier recorded — this claim cannot be settled until one is stated."}
                    </td>
                    <td style={td}>
                      <Chip tone={v.tone}>{v.label}</Chip>
                    </td>
                    <td style={td}>
                      <span style={{ display: "flex", gap: 6, flexWrap: "wrap", alignItems: "center" }}>
                        <StageChip stage={stage} />
                        {c.bundle?.attribution_contested && (
                          <Chip tone="contest">contested</Chip>
                        )}
                      </span>
                    </td>
                  </tr>
                );
              })}
              {visible.length === 0 && (
                <tr>
                  <td style={td} colSpan={4}>
                    <span style={{ color: p.muted }}>
                      {claims.length === 0
                        ? "No claims recorded yet — a claim enters by registering its source in Evidence & sources."
                        : "No claims match this filter."}
                    </span>
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </Card>
      )}

      {hypotheses.length > 0 && (
        <div style={{ marginTop: 18 }}>
          <h3 style={{ margin: "0 0 4px", fontSize: 14, color: p.fg }}>
            Hypotheses{" "}
            <span style={{ color: p.muted, fontWeight: 400, fontSize: 12 }}>
              — folded into this register: a hypothesis is a claim whose falsifier is
              not yet sharp, shown as an early state, not a separate tracker
            </span>
          </h3>
          <Card p={p} style={{ padding: 0, overflow: "hidden" }}>
            <table style={{ width: "100%", borderCollapse: "collapse" }}>
              <tbody>
                {hypotheses.map((h) => (
                  <tr key={h.model_id} data-testid="hypothesis-row">
                    <td style={td}>
                      <div style={{ fontWeight: 600, overflowWrap: "anywhere" }}>
                        {h.model_name || h.model_id}
                      </div>
                      <div style={{ fontSize: 11.5, color: p.muted, marginTop: 2 }}>
                        {`${h.model_id} · hypothesis · ${h.status || "unstated status"} · ` +
                          `${h.n_claims} core claims · ${h.n_tests} tests planned`}
                      </div>
                    </td>
                    <td style={{ ...td, color: p.muted }}>
                      Not yet sharp — the falsifier is stated when the hypothesis is
                      sharp enough to test.
                    </td>
                    <td style={td}>
                      <Chip tone="neutral">No verdict yet</Chip>
                    </td>
                    <td style={td}>
                      <StageChip stage="created" />
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Card>
        </div>
      )}
    </div>
  );
}

function filterChipStyle(
  p: ReturnType<typeof palette>,
  active: boolean
): CSSProperties {
  return {
    padding: "5px 11px", borderRadius: 999, fontSize: 12, fontFamily: "inherit",
    border: `1px solid ${active ? p.accent : p.border}`,
    background: active ? p.accent : "transparent",
    color: active ? "#fff" : p.fg,
    cursor: "pointer", fontWeight: active ? 700 : 500,
  };
}

function ClaimDetail({
  claim,
  trail,
  trailError,
  darkMode,
  onBack,
}: {
  claim: IndusClaim;
  trail: ClaimTrail | null;
  trailError: string | null;
  darkMode: boolean;
  onBack: () => void;
}) {
  const p = palette(darkMode);
  const v = verdictOf(claim.claim_status);
  const stage = effectiveStage(claim);
  const missing = missingActFor(stage);
  const score = claim.lane1_score ?? claim.aee_score ?? null;
  const contest = claim.bundle?.contest_record ?? null;
  const transitions = trail?.stage_transitions ?? [];
  const evidenceRefs = trail?.evidence ?? [];

  const laneHead: CSSProperties = {
    fontSize: 12, fontWeight: 700, color: p.fg, marginBottom: 8,
    textTransform: "uppercase", letterSpacing: 0.4,
  };

  return (
    <div data-testid="claim-detail">
      <button
        type="button"
        onClick={onBack}
        style={{
          background: "none", border: "none", padding: 0, cursor: "pointer",
          color: p.accent, fontSize: 12.5, fontFamily: "inherit", marginBottom: 10,
        }}
      >
        ← All claims
      </button>

      <PageHead
        p={p}
        title={claim.normalized_claim}
        lede={
          `${claim.claim_id} · ${claim.claim_type}` +
          `${claim.extracted_at ? ` · registered ${fmtDayTime(claim.extracted_at)}` : ""}` +
          " — this page keeps the two kinds of standing apart: what machines have " +
          "checked, and what people have settled."
        }
      />

      <Card p={p} style={{ padding: 16, marginBottom: 14 }}>
        <div style={laneHead}>Falsifier</div>
        <div style={{ fontSize: 11.5, color: p.muted, marginBottom: 6 }}>
          Stated when the claim was registered; the claim stands or falls by it.
        </div>
        <div style={{ fontSize: 13, color: p.fg, lineHeight: 1.6 }}>
          {claim.falsification_condition?.trim()
            ? claim.falsification_condition
            : "No falsifier recorded — this claim cannot be settled until one is stated."}
        </div>
      </Card>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
          gap: 14, alignItems: "start",
        }}
      >
        <Card p={p} style={{ padding: 16 }}>
          <div data-testid="lane1-region">
            <div style={laneHead}>Lane 1 — machine-speed verification (checking only)</div>
            <div style={{ display: "flex", gap: 8, alignItems: "center", marginBottom: 10 }}>
              <Chip tone={v.tone}>{v.label}</Chip>
              <span style={{ fontSize: 12.5, color: p.muted }}>
                {`claim status: ${claim.claim_status}`}
              </span>
            </div>
            {score ? (
              <div style={{ fontSize: 12.5, color: p.fg, marginBottom: 10 }}>
                {`AEE score ${score.propagated_score} · band: ${score.band}`}
                <div style={{ fontSize: 11.5, color: p.muted, marginTop: 2 }}>
                  AEE library scoring — a lane-1 checking figure, never a settlement.
                </div>
              </div>
            ) : (
              <div style={{ fontSize: 12.5, color: p.muted, marginBottom: 10 }}>
                No AEE score on this record.
              </div>
            )}
            {claim.glossa_lab_evidence?.trim() && (
              <div style={{ marginBottom: 10 }}>
                <div style={{ fontSize: 12, fontWeight: 700, color: p.fg, marginBottom: 3 }}>
                  Evidence on file
                </div>
                <div style={{ fontSize: 12.5, color: p.muted, lineHeight: 1.55 }}>
                  {claim.glossa_lab_evidence}
                </div>
              </div>
            )}
            <NotUnderstood
              value={claim.not_understood}
              fg={p.fg}
              muted={p.muted}
            />
          </div>
        </Card>

        <Card p={p} style={{ padding: 16 }}>
          <div data-testid="lane2-region">
            <div style={laneHead}>Lane 2 — human-paced settlement</div>
            <StageTrack stage={stage} />
            <div style={{ fontSize: 12.5, color: p.muted, marginTop: 8, lineHeight: 1.55 }}>
              {claim.stage?.stage_source
                ? `Stage stamped from ${claim.stage.stage_source}` +
                  `${claim.stage.stage_as_of ? ` · as of ${fmtDayTime(claim.stage.stage_as_of)}` : ""}.`
                : "No stage stamp on this record yet."}
            </div>
            {claim.bundle?.attribution_contested && (
              <div style={{ marginTop: 10 }}>
                <Chip tone="contest">Attribution contested</Chip>
                <div style={{ fontSize: 12.5, color: p.muted, marginTop: 6, lineHeight: 1.55 }}>
                  {contest?.contested_by
                    ? `Contested by ${contest.contested_by}` +
                      `${contest.contested_on ? ` · ${contest.contested_on}` : ""}` +
                      " — a contested attribution caps the claim at checked until it is answered."
                    : "A contested attribution caps the claim at checked until it is answered."}
                </div>
              </div>
            )}
            {missing && (
              <div style={{ marginTop: 12 }}>
                <MissingAct>
                  <b>Missing:</b> {missing}
                </MissingAct>
              </div>
            )}
            {stage === "created" && (
              <div style={{ fontSize: 12.5, color: p.muted, marginTop: 12, lineHeight: 1.55 }}>
                Nothing has been checked yet — machine checks are the next act, and
                they can advance this claim to checked, never beyond.
              </div>
            )}
          </div>
        </Card>
      </div>

      <Card p={p} style={{ padding: 16, marginTop: 14 }}>
        <div style={laneHead}>Trail — the inspectable record</div>
        {trailError ? (
          <div style={{ fontSize: 12.5, color: p.bad }}>
            {`This instance states: ${trailError}`}
          </div>
        ) : !trail ? (
          <div style={{ fontSize: 12.5, color: p.muted }}>Loading…</div>
        ) : (
          <>
            <div style={{ fontSize: 12.5, color: p.muted, marginBottom: 8 }}>
              {`${evidenceRefs.length} evidence ref${evidenceRefs.length === 1 ? "" : "s"}` +
                ` · ${trail.origin_group_count ?? 0} origin groups` +
                `${trail.source_pointer ? ` · source: ${trail.source_pointer}` : ""}`}
            </div>
            {transitions.length === 0 ? (
              <div style={{ fontSize: 12.5, color: p.muted }}>
                No stage transitions recorded.
              </div>
            ) : (
              transitions.map((t, i) => (
                <div
                  key={i}
                  style={{
                    fontSize: 12.5, color: p.fg, padding: "6px 0",
                    borderTop: i === 0 ? "none" : `1px solid ${p.borderSoft}`,
                  }}
                >
                  {`${String(t.from_stage ?? "—")} → ${String(t.to_stage ?? "—")}`}
                  <span style={{ color: p.muted }}>
                    {`${t.actor ? ` · ${String(t.actor)}` : ""}${t.at ? ` · ${fmtDayTime(String(t.at))}` : ""}`}
                  </span>
                </div>
              ))
            )}
          </>
        )}
      </Card>
    </div>
  );
}
