/**
 * Program home (Spec 081 step 5, T017; wireframe 02; FR-005).
 *
 * Where the active program stands in its own loop: claims and their
 * verdicts first (negatives unfiltered, un-greyed, full weight),
 * the digestion queue with its doorway, the program's data counts,
 * and the foundation check — the canonical /foundation/status set
 * ONLY, labelled as the program's record (D2.1; the API-native set
 * belongs to the Status surface, labelled separately). Exactly one
 * primary action: register a claim — the loop's entry act.
 *
 * Retires DashboardView as the home surface (D2.2): the AI narrative,
 * the feed furniture, the embedded DeciphermentPanel and the embedded
 * research-loop panel leave the home; the loop and discovery remain
 * as one-line statuses with doorways. The retired components
 * themselves are removed in step 9 (T021).
 *
 * Amendment 2 (D2.2 refinement, 2026-10-30): what the panel led with
 * was never panel furniture — the program's standing position and
 * its lane-2 stage summary are program data, and they lead THIS
 * surface instead. The standing position renders from the active
 * program's own record (`standing_position`; a program that states
 * none shows none — the absence is the record's, never filled in by
 * the shell), and the stage summary renders the decipherment
 * payload's `by_stage` anchor counts under the FR-029-08 framing
 * (an index into the anchor records, not a measure of decipherment)
 * with the OD-4 legend. The Spec 029 E2/G guards assert these blocks
 * here now, their text and intent unchanged; DeciphermentPanel keeps
 * its own rendering for the surfaces that still mount it.
 *
 * Every figure on this page is read from an endpoint at render time.
 * The wireframe's specimen numbers (the 94-strict / 44-pending anchor
 * split, the evidence-basis claim split) are NOT endpoint-exposed
 * and are never printed here (D3); the anchors card shows the /signs
 * totals and confidence tiers only.
 */
import { useEffect, useMemo, useState, type CSSProperties, type ReactNode } from "react";
import {
  getDashboardDecipherment,
  getDiscoveryStats,
  getFoundationStatus,
  getSignsSummary,
  getStudyLoopStatus,
  listIndusClaims,
  type DeciphermentProgress,
  type FoundationStatus,
  type IndusClaim,
  type SignsSummary,
  type StudyLoopStatus,
} from "../api";
import { useProject } from "../hooks/useProject";
import { effectiveStage } from "./DigestionBoard";
import { STAGE_NAMES, StageLegend, stageColor } from "./StageLegend";
import {
  Card,
  Chip,
  PageHead,
  PrimaryButton,
  fmtDayTime,
  palette,
  verdictOf,
  type ChipTone,
} from "./ui081";

type Route =
  | "claims"
  | "digestion"
  | "data"
  | "foundation-check"
  | "loop"
  | "discovery";

export function ProgramHome({
  darkMode,
  onNavigate,
}: {
  darkMode: boolean;
  onNavigate: (route: Route) => void;
}) {
  const p = palette(darkMode);
  const { activeProject } = useProject();

  const [claims, setClaims] = useState<IndusClaim[] | null>(null);
  const [claimsTotal, setClaimsTotal] = useState<number | null>(null);
  const [claimsError, setClaimsError] = useState<string | null>(null);
  const [foundation, setFoundation] = useState<FoundationStatus | null>(null);
  const [foundationError, setFoundationError] = useState<string | null>(null);
  const [signs, setSigns] = useState<SignsSummary | null>(null);
  const [signsError, setSignsError] = useState<string | null>(null);
  const [loop, setLoop] = useState<StudyLoopStatus | null>(null);
  const [loopError, setLoopError] = useState<string | null>(null);
  const [inbox, setInbox] = useState<number | null>(null);
  const [decipher, setDecipher] = useState<DeciphermentProgress | null>(null);

  useEffect(() => {
    let cancelled = false;
    listIndusClaims({ limit: 500 })
      .then((r) => {
        if (cancelled) return;
        setClaims(r.claims);
        setClaimsTotal(r.total);
      })
      .catch((e) => {
        if (!cancelled) {
          setClaimsError(e instanceof Error ? e.message : "The claims register did not answer.");
        }
      });
    getFoundationStatus()
      .then((r) => { if (!cancelled) setFoundation(r); })
      .catch((e) => {
        if (!cancelled) {
          setFoundationError(e instanceof Error ? e.message : "The foundation status did not answer.");
        }
      });
    getSignsSummary()
      .then((r) => { if (!cancelled) setSigns(r); })
      .catch((e) => {
        if (!cancelled) {
          setSignsError(e instanceof Error ? e.message : "The signs summary did not answer.");
        }
      });
    getStudyLoopStatus()
      .then((r) => { if (!cancelled) setLoop(r); })
      .catch((e) => {
        if (!cancelled) {
          setLoopError(e instanceof Error ? e.message : "The loop status did not answer.");
        }
      });
    getDiscoveryStats("status")
      .then((r) => { if (!cancelled) setInbox(r.counts["new"] ?? 0); })
      .catch(() => { /* the card states its absence plainly */ });
    getDashboardDecipherment()
      .then((r) => { if (!cancelled) setDecipher(r); })
      .catch(() => { /* no stage summary renders — the payload's absence is stated by its absence */ });
    return () => { cancelled = true; };
  }, []);

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

  const waiting = useMemo(() => {
    if (!claims) return null;
    return claims.filter((c) => {
      const s = effectiveStage(c);
      return s === "checked" || s === "explained" || s === "accepted";
    }).length;
  }, [claims]);

  const latest = useMemo(() => {
    if (!claims) return [];
    return [...claims]
      .sort((a, b) => (b.extracted_at ?? "").localeCompare(a.extracted_at ?? ""))
      .slice(0, 5);
  }, [claims]);

  const linkStyle: CSSProperties = {
    background: "none",
    border: "none",
    padding: 0,
    cursor: "pointer",
    color: p.accent,
    fontSize: 12.5,
    fontFamily: "inherit",
    textAlign: "left",
  };

  const statCard = (children: ReactNode) => (
    <Card p={p} style={{ padding: 16, display: "flex", flexDirection: "column", gap: 6, minWidth: 0 }}>
      {children}
    </Card>
  );

  return (
    <div data-testid="program-home">
      <PageHead
        p={p}
        title={activeProject?.label ?? "Program"}
        lede={
          activeProject?.question?.trim()
            ? activeProject.question
            : activeProject?.description ?? "The active program."
        }
        primary={
          <PrimaryButton onClick={() => onNavigate("claims")}>
            + Register a claim
          </PrimaryButton>
        }
      />

      {/* Amendment 2: the program's standing position leads the home,
          rendered from the program's own record. A program whose
          record states no position renders no block — the shell
          never supplies one. */}
      {activeProject?.standing_position?.trim() ? (
        <div
          data-testid="standing-position"
          style={{
            border: `1px solid ${p.border}`,
            borderRadius: 10,
            padding: "12px 16px",
            marginBottom: 14,
          }}
        >
          <div style={{ fontSize: 12.5, fontWeight: 700, color: p.fg, marginBottom: 3 }}>
            Standing position
          </div>
          <div style={{ fontSize: 12.5, color: p.muted, lineHeight: 1.55 }}>
            {activeProject.standing_position}
          </div>
        </div>
      ) : null}

      {/* Amendment 2: the lane-2 stage summary over the anchor
          records, from the decipherment payload's by_stage counts —
          the same data and the same FR-029-08 framing the panel
          rendering carries (an index into the records, not a
          measure of decipherment), with the OD-4 legend. */}
      {decipher?.available && decipher.anchors ? (
        <div data-testid="stage-summary" style={{ marginBottom: 14 }}>
          <div style={{ fontSize: 12.5, fontWeight: 700, color: p.fg, marginBottom: 4 }}>
            Anchor claims by stage — lane 2 (human-paced settlement)
          </div>
          <div style={{ display: "flex", gap: 14, flexWrap: "wrap", marginBottom: 6 }}>
            {STAGE_NAMES.map((s) => (
              <span key={s} style={{ fontSize: 12.5 }}>
                <span style={{ fontWeight: 700, color: stageColor(s) }}>{s}</span>
                <span style={{ color: p.muted }}>: {decipher.anchors.by_stage?.[s] ?? 0}</span>
              </span>
            ))}
            {(decipher.anchors.n_unstamped_stage ?? 0) > 0 && (
              <span style={{ fontSize: 12.5, color: p.muted }}>
                not stamped: {decipher.anchors.n_unstamped_stage}
              </span>
            )}
          </div>
          <div style={{ fontSize: 11.5, color: p.muted, marginBottom: 8 }}>
            These counts are an index into the anchor records — how many records stand
            at each stage — not a measure of decipherment.
          </div>
          <StageLegend fg={p.fg} muted={p.muted} border={p.border} />
        </div>
      ) : null}

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(210px, 1fr))",
          gap: 14,
          marginBottom: 14,
        }}
      >
        {statCard(
          <>
            <div style={{ fontSize: 30, fontWeight: 600, color: p.fg, lineHeight: 1.1 }}>
              {claimsTotal ?? "—"}
            </div>
            <div style={{ fontSize: 12.5, color: p.muted }}>claims in the register</div>
            {claimsError ? (
              <div style={{ fontSize: 12, color: p.bad }}>{`This instance states: ${claimsError}`}</div>
            ) : (
              <div style={{ display: "flex", flexWrap: "wrap", gap: 5 }}>
                {verdictGroups.map((g) => (
                  <Chip key={g.label} tone={g.tone}>{`${g.n} ${g.label.toLowerCase()}`}</Chip>
                ))}
                {claims && verdictGroups.length === 0 && (
                  <span style={{ fontSize: 12, color: p.muted }}>No claims recorded yet.</span>
                )}
              </div>
            )}
          </>,
        )}

        {statCard(
          <>
            <div style={{ fontSize: 30, fontWeight: 600, color: p.fg, lineHeight: 1.1 }}>
              {waiting ?? "—"}
            </div>
            <div style={{ fontSize: 12.5, color: p.muted }}>claims waiting on a human</div>
            <div style={{ fontSize: 12.5, color: p.muted }}>
              Digestion advances only by a named person's recorded act — never automatically.
            </div>
            <button type="button" style={linkStyle} onClick={() => onNavigate("digestion")}>
              Open the digestion board →
            </button>
          </>,
        )}

        {statCard(
          <>
            <div style={{ fontSize: 30, fontWeight: 600, color: p.fg, lineHeight: 1.1 }}>
              {signs ? signs.total : "—"}
            </div>
            <div style={{ fontSize: 12.5, color: p.muted }}>anchors recorded</div>
            {signsError ? (
              <div style={{ fontSize: 12, color: p.bad }}>{`This instance states: ${signsError}`}</div>
            ) : signs ? (
              <>
                <div style={{ fontSize: 12.5, color: p.muted }}>
                  {`${signs.high} high-confidence · ${signs.medium} medium · ${signs.low} low`}
                </div>
                <div style={{ fontSize: 12.5, color: p.muted }}>
                  {`${activeProject?.corpus_ids.length ?? 0} corpora attached to this program`}
                </div>
              </>
            ) : null}
            <button type="button" style={linkStyle} onClick={() => onNavigate("data")}>
              Open data →
            </button>
          </>,
        )}

        {statCard(
          <>
            <div
              style={{
                fontSize: 26,
                fontWeight: 600,
                lineHeight: 1.15,
                color: foundation ? (foundation.n_fail > 0 ? p.bad : "#15803d") : p.fg,
              }}
            >
              {foundation?.verdict ?? "—"}
            </div>
            <div style={{ fontSize: 12.5, color: p.muted }}>
              foundation check — the integrity gate (this program's canonical record)
            </div>
            {foundationError ? (
              <div style={{ fontSize: 12, color: p.bad }}>{`This instance states: ${foundationError}`}</div>
            ) : foundation ? (
              <div style={{ fontSize: 12.5, color: p.muted }}>
                {`${foundation.n_ok} pass · ${foundation.n_fail} fail · ${foundation.n_warn} warn · checked ${foundation.last_checked_at ? fmtDayTime(foundation.last_checked_at) : "never"}`}
              </div>
            ) : null}
            <button type="button" style={linkStyle} onClick={() => onNavigate("foundation-check")}>
              Open the check →
            </button>
          </>,
        )}
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit, minmax(320px, 1fr))",
          gap: 14,
          alignItems: "start",
        }}
      >
        <Card p={p} style={{ padding: 16, minWidth: 0 }}>
          <h3 style={{ margin: "0 0 4px", fontSize: 14, color: p.fg }}>
            Latest verdicts{" "}
            <span style={{ color: p.muted, fontWeight: 400, fontSize: 12 }}>
              — newest first; negative results carry the same weight as positive ones
            </span>
          </h3>
          {claimsError ? (
            <div style={{ fontSize: 12.5, color: p.bad }}>{`This instance states: ${claimsError}`}</div>
          ) : latest.length === 0 ? (
            <div style={{ fontSize: 12.5, color: p.muted }}>
              {claims ? "No claims recorded yet." : "Loading…"}
            </div>
          ) : (
            latest.map((c) => {
              const v = verdictOf(c.claim_status);
              return (
                <div
                  key={c.claim_id}
                  style={{
                    display: "flex",
                    gap: 10,
                    padding: "10px 0",
                    borderTop: `1px solid ${p.borderSoft}`,
                    alignItems: "flex-start",
                  }}
                >
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ fontSize: 13.5, fontWeight: 600, color: p.fg, overflowWrap: "anywhere" }}>
                      {c.normalized_claim}
                    </div>
                    <div style={{ fontSize: 12, color: p.muted, marginTop: 2 }}>
                      {`${c.claim_id} · ${c.claim_type}${c.extracted_at ? ` · ${fmtDayTime(c.extracted_at)}` : ""}`}
                    </div>
                  </div>
                  <Chip tone={v.tone}>{v.label}</Chip>
                </div>
              );
            })
          )}
          <p style={{ fontSize: 12, color: p.muted, margin: "10px 0 0" }}>
            What this does not show: a verdict settles one claim under one frozen test. It
            does not settle the program's subject, and a “supported” verdict is only ever
            as strong as the evidence named on the claim.
          </p>
        </Card>

        <div style={{ display: "grid", gap: 14, minWidth: 0 }}>
          <Card p={p} style={{ padding: 16 }}>
            <h3 style={{ margin: "0 0 8px", fontSize: 14, color: p.fg }}>Research loop</h3>
            {loopError ? (
              <div style={{ fontSize: 12.5, color: p.bad }}>{`This instance states: ${loopError}`}</div>
            ) : loop ? (
              <div style={{ display: "flex", gap: 10, alignItems: "flex-start" }}>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ fontSize: 13.5, fontWeight: 600, color: p.fg }}>
                    {loop.running ? "Running" : "Stopped"}
                  </div>
                  <div style={{ fontSize: 12, color: p.muted, marginTop: 2 }}>
                    {loop.running
                      ? `${loop.iterations ?? loop.cycles_completed ?? 0} cycles so far this session.`
                      : "Nothing runs unattended until you start it."}
                  </div>
                </div>
                <Chip tone={loop.running ? "ok" : "neutral"}>
                  {loop.running ? "Running" : "Idle"}
                </Chip>
              </div>
            ) : (
              <div style={{ fontSize: 12.5, color: p.muted }}>Loading…</div>
            )}
            <button
              type="button"
              style={{ ...linkStyle, marginTop: 10 }}
              onClick={() => onNavigate("loop")}
            >
              Open the loop
            </button>
          </Card>

          <Card p={p} style={{ padding: 16 }}>
            <h3 style={{ margin: "0 0 8px", fontSize: 14, color: p.fg }}>Discovery</h3>
            <div style={{ fontSize: 13.5, fontWeight: 600, color: p.fg }}>
              {inbox === null ? "—" : `${inbox} item${inbox === 1 ? "" : "s"} waiting for triage`}
            </div>
            <div style={{ fontSize: 12, color: p.muted, marginTop: 2 }}>
              From the program's sources.
            </div>
            <button
              type="button"
              style={{ ...linkStyle, marginTop: 10 }}
              onClick={() => onNavigate("discovery")}
            >
              Open the inbox
            </button>
          </Card>
        </div>
      </div>
    </div>
  );
}
