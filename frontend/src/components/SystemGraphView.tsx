/**
 * System graph — the layered map surface (Spec 086 Stage 5, T503).
 *
 * Five screens over the published, gate-verified map artifact
 * (glossa-indus/map/map-data.json, served by /api/v1/indus-map):
 * system view, claim view, evidence view, matrix view, settling
 * panel. The surface renders the artifact exactly (C086-17): every
 * number, statement and citation below comes from the artifact as
 * served; nothing is recomputed or hand-tuned here. Q1: there is
 * no graph canvas in v1 — the views are tables and lists, because
 * the claim×claim pairs are coverage data, not relations.
 *
 * The standing position leads the system view (C086-20): the
 * Indus script is not deciphered; this map renders the program's
 * epistemic state, labeled as such.
 */
import { useCallback, useEffect, useState, type CSSProperties, type ReactNode } from "react";
import {
  fetchIndusMapClaim,
  fetchIndusMapClaimEvidence,
  fetchIndusMapMatrix,
  fetchIndusMapSettling,
  fetchIndusMapSystem,
  type IndusMapEnvelope,
  type IndusMapHeader,
  type IndusMapStamp,
} from "../api";

type Screen = "system" | "claim" | "evidence" | "matrix" | "settling";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type AnyRec = Record<string, any>;

const SPECIMEN_CLAIM = "parpola_2010_dravidian_solution_manual_002";
const CONTRAST_CLAIM = "yadav_2009_arxiv_manual_002";
const SCORE_LABEL =
  "AEE score — aee/scoring.py (ScoringEngine) output over the ledger's relation set.";

interface Palette {
  fg: string;
  muted: string;
  border: string;
  cardBg: string;
  softBg: string;
}

function palette(dark: boolean): Palette {
  return dark
    ? { fg: "#e2e8f0", muted: "#94a3b8", border: "#334155", cardBg: "#1e293b", softBg: "#0f172a" }
    : { fg: "#17202b", muted: "#5b6b7d", border: "#d9dee5", cardBg: "#ffffff", softBg: "#f4f6f9" };
}

const fmt = (n: number) => n.toLocaleString("en-US");
const shortHash = (h: string) => `${h.slice(0, 8)}…`;
const pct = (share: number) => `${(share * 100).toFixed(1)}%`;
const REL_COLOR: Record<string, string> = {
  supports: "#15803d",
  opposes: "#b91c1c",
  constrains: "#7c3aed",
};

function Cites({ p, children }: { p: Palette; children: ReactNode }) {
  return (
    <div style={{ fontSize: 11, color: p.muted, marginTop: 10 }}>
      <span style={{ fontWeight: 700, letterSpacing: 0.4, textTransform: "uppercase", fontSize: 10 }}>Cites </span>
      {children}
    </div>
  );
}

function LayerTag({ children, color }: { children: ReactNode; color: string }) {
  return (
    <span
      style={{
        fontSize: 10, fontWeight: 700, letterSpacing: 0.6, textTransform: "uppercase",
        color, border: `1px solid ${color}`, borderRadius: 4, padding: "1px 6px",
      }}
    >
      {children}
    </span>
  );
}

function Card({ p, children, style }: { p: Palette; children: ReactNode; style?: CSSProperties }) {
  return (
    <div
      style={{
        background: p.cardBg, border: `1px solid ${p.border}`, borderRadius: 10,
        padding: "16px 18px", ...style,
      }}
    >
      {children}
    </div>
  );
}

function CardHead({ tag, tagColor, title }: { tag: string; tagColor: string; title: string }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 8, marginBottom: 10 }}>
      <h3 style={{ margin: 0, fontSize: 15 }}>{title}</h3>
      <LayerTag color={tagColor}>{tag}</LayerTag>
    </div>
  );
}

function BigStat({ children }: { children: ReactNode }) {
  return <div style={{ fontSize: 26, fontWeight: 700, lineHeight: 1.15 }}>{children}</div>;
}

function Row({ p, children }: { p: Palette; children: ReactNode }) {
  return (
    <div
      style={{
        display: "flex", justifyContent: "space-between", gap: 12, padding: "5px 0",
        borderBottom: `1px dashed ${p.border}`, fontSize: 13,
      }}
    >
      {children}
    </div>
  );
}

function NavLink({ onClick, children }: { onClick: () => void; children: ReactNode }) {
  return (
    <button
      onClick={onClick}
      style={{
        background: "none", border: "none", color: "#2563eb", cursor: "pointer",
        fontSize: 13, fontWeight: 600, padding: 0, textAlign: "left",
      }}
    >
      {children}
    </button>
  );
}

function HeaderStrip({ header, stamp }: { header: IndusMapHeader; stamp: IndusMapStamp }) {
  const statusLine = Object.entries(header.claims_by_status)
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([s, n]) => `${s.replace(/_/g, " ")} ${fmt(n)}`)
    .join(" · ");
  const block: CSSProperties = { flex: "1 1 220px", minWidth: 200 };
  const big: CSSProperties = { fontSize: 24, fontWeight: 700 };
  const lbl: CSSProperties = { fontSize: 12, opacity: 0.85 };
  const cites: CSSProperties = { fontSize: 11, opacity: 0.75, marginTop: 6 };
  return (
    <div>
      <div
        data-testid="indus-map-header"
        style={{
          background: "linear-gradient(135deg,#33506e,#22364e)", color: "#fff",
          borderRadius: 10, padding: "18px 20px",
        }}
      >
        <h2 style={{ margin: "0 0 4px", fontSize: 21 }}>System graph — the Indus program as one system</h2>
        <p style={{ margin: "0 0 14px", fontSize: 13, opacity: 0.9, maxWidth: 900 }}>
          The layered map (Spec 086): system → claim → evidence. Every element below is generated
          from the claims ledger and verified by the gate; every element cites the ledger ids it
          comes from. Nothing on this screen is hand-written.
        </p>
        <div style={{ display: "flex", gap: 22, flexWrap: "wrap" }}>
          <div style={block}>
            <div style={big}>{fmt(header.claims_total)} claims in the ledger</div>
            <div style={lbl}>{statusLine}</div>
            <div style={cites}>Cites: glossa-indus/ledger/claims.jsonl ({fmt(header.as_of.ledger_lines)} lines)</div>
          </div>
          <div style={block}>
            <div style={big}>{pct(header.validated_anchor_share)} of anchor signs validated (strict)</div>
            <div style={lbl}>
              {fmt(header.anchors_strict)} of {fmt(header.anchors_total)} anchors strict ·{" "}
              {fmt(header.pending_validations.count)} validations pending
            </div>
            <div style={cites}>Cites: backend/reports/INDUS_FINAL_ANCHORS.json · Phase-108 provenance register</div>
          </div>
          <div style={block}>
            <div style={{ ...big, fontSize: 16, lineHeight: 1.35 }}>
              Nearest dated items
              {header.nearest_dated_items.map((it) => (
                <div key={`${it.date}-${it.study}`} style={{ fontWeight: 400, fontSize: 13 }}>
                  {it.date} — study {it.study} outcome {it.outcome} ({it.claims.length}{" "}
                  {it.claims.length === 1 ? "claim" : "claims"})
                </div>
              ))}
            </div>
            <div style={cites}>Cites: dated study-outcome blocks in the ledger (the Q4 definition)</div>
          </div>
        </div>
      </div>
      <div
        style={{
          display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap",
          fontSize: 12, marginTop: 8,
        }}
      >
        <span data-testid="indus-map-stamp">
          map data · ledger {shortHash(header.as_of.ledger_sha256)} ·{" "}
          {stamp.stale ? (
            <strong style={{ color: "#b91c1c" }}>STALE — the ledger has moved since this map was generated</strong>
          ) : (
            "fresh"
          )}
        </span>
        <span>map: glossa-indus/map · definitions {header.as_of.map_defs} · gate-verified</span>
      </div>
    </div>
  );
}

function ScreenTabs({ p, active, go }: { p: Palette; active: Screen; go: (s: Screen) => void }) {
  const tabs: { id: Screen; label: string }[] = [
    { id: "system", label: "System view" },
    { id: "matrix", label: "Matrix" },
    { id: "settling", label: "Settling" },
  ];
  return (
    <div style={{ display: "flex", gap: 4, borderBottom: `1px solid ${p.border}`, margin: "16px 0 18px" }}>
      {tabs.map((t) => (
        <button
          key={t.id}
          onClick={() => go(t.id)}
          style={{
            background: "none", border: "none", cursor: "pointer", fontSize: 14,
            padding: "8px 14px", color: active === t.id ? "#2563eb" : p.muted,
            fontWeight: active === t.id ? 700 : 400,
            borderBottom: active === t.id ? "2px solid #2563eb" : "2px solid transparent",
            marginBottom: -1,
          }}
        >
          {t.label}
        </button>
      ))}
    </div>
  );
}

function SystemScreen({
  p, header, data, go, openClaim,
}: {
  p: Palette;
  header: IndusMapHeader;
  data: AnyRec;
  go: (s: Screen) => void;
  openClaim: (id: string) => void;
}) {
  const inv = data.sign_inventory as AnyRec;
  const cov = data.matrix_coverage as AnyRec;
  const pop = data.claim_population as AnyRec;
  const fal = data.falsifier_census as AnyRec;
  const aee = data.aee_state_census as AnyRec;
  const un = data.unresolved as AnyRec;
  const signBlock = data.sign_sign_block_summary as AnyRec;
  const sets = inv.assignment_sets as AnyRec[];
  const setById = (id: string) => sets.find((s) => s.id === id);
  const columnsTotal = Object.values(cov.columns_by_class as Record<string, number>).reduce((a, b) => a + b, 0);
  const mentionClaims = new Set((un.sign_mentions as AnyRec[]).map((m) => m.record as string));
  const grid: CSSProperties = {
    display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(330px,1fr))", gap: 14,
  };
  return (
    <div>
      <div
        data-testid="indus-map-standing-position"
        style={{
          background: "#fffbeb", border: "1px solid #f59e0b", borderLeft: "4px solid #f59e0b",
          borderRadius: 8, padding: "12px 16px", fontSize: 13.5, color: "#17202b", marginBottom: 14,
        }}
      >
        <strong>Standing position: the Indus script is not deciphered.</strong> This map renders the
        program&apos;s epistemic state — what is claimed, what bears on it, and what the recorded
        relations imply under stated rules. It is not a decipherment, and no element on it claims
        to be one.
      </div>
      <div style={grid}>
        <Card p={p}>
          <CardHead tag="Ledger" tagColor="#2563eb" title="Sign inventory & validation" />
          <BigStat>{fmt(inv.frame_scope as number)} signs in the Mahadevan frame</BigStat>
          <div style={{ marginTop: 8 }}>
            <Row p={p}><span>Register records (anchors register)</span><strong>{fmt(inv.register_records as number)}</strong></Row>
            <Row p={p}><span>In the Mahadevan frame</span><strong>{fmt(inv.frame_scope as number)}</strong></Row>
            <Row p={p}><span>Out of frame, named in the assignment sets</span><strong>{(inv.out_of_frame_records as string[]).join(", ")}</strong></Row>
            <Row p={p}>
              <span>Incumbent assignment set covers</span>
              <strong>{fmt(setById("incumbent")?.assignments as number)} of {fmt(inv.frame_scope as number)} ({pct((setById("incumbent")?.assignments as number) / (inv.frame_scope as number))})</strong>
            </Row>
            <Row p={p}>
              <span>Full-register set covers</span>
              <strong>{fmt(setById("full-register")?.assignments as number)} of {fmt(inv.frame_scope as number)}</strong>
            </Row>
            <Row p={p}><span>Strict-validated (strict_sa_independent)</span><strong>{fmt(header.anchors_strict)}</strong></Row>
            <Row p={p}><span>Pending validations</span><strong>{fmt(header.pending_validations.count)}</strong></Row>
          </div>
          <div style={{ background: p.softBg, borderRadius: 6, padding: "9px 11px", fontSize: 12.5, marginTop: 10 }}>
            The signaries disagree on the inventory itself: published sign lists run 557 (Shakti) /
            527 (M77 concordance) / 584 (Nair) signs. That is why a validated share is always stated
            against a named frame, never as a bare number.
          </div>
          <Cites p={p}>anchor register records · assignment-sets.json (incumbent, full-register) · the strict rule as recorded in the register</Cites>
          <div style={{ marginTop: 8 }}><NavLink onClick={() => go("settling")}>See the settling panel →</NavLink></div>
        </Card>

        <Card p={p}>
          <CardHead tag="Matrix" tagColor="#7c3aed" title="Matrix coverage" />
          <BigStat>{fmt(cov.cells_total as number)} cells over {fmt(cov.rows_total as number)} claims × {fmt(columnsTotal)} columns</BigStat>
          <div style={{ marginTop: 8 }}>
            <Row p={p}><span><strong style={{ color: "#15803d" }}>supports</strong> — every one on a document column</span><strong>{fmt(cov.cells_by_relation.supports as number)}</strong></Row>
            <Row p={p}><span><strong style={{ color: "#b91c1c" }}>opposes</strong> — every one on a study column</span><strong>{fmt(cov.cells_by_relation.opposes as number)}</strong></Row>
            {(cov.conflict_hotspots as AnyRec[]).map((o) => (
              <div key={`${o.row}-${o.column}`} style={{ fontSize: 12, color: p.muted, padding: "2px 0 2px 14px", overflowWrap: "anywhere" }}>
                study {o.column as string} × {o.row as string}
              </div>
            ))}
            <Row p={p}><span><strong>constrains</strong> — the class is empty and says so</span><strong>{fmt(cov.cells_by_relation.constrains as number)}</strong></Row>
            <Row p={p}><span>Rows with no cells (of {fmt(cov.rows_total as number)})</span><strong>{fmt((cov.empty_rows as string[]).length)}</strong></Row>
            <Row p={p}><span>Anchor columns unused (no claim×anchor cells)</span><strong>{fmt(cov.columns_by_class.anchors as number)} of {fmt(cov.columns_by_class.anchors as number)}</strong></Row>
            <Row p={p}><span>Research-check columns unused</span><strong>{fmt((cov.unused_columns.research_checks as string[]).length)} of {fmt(cov.columns_by_class.research_checks as number)}</strong></Row>
            <Row p={p}><span>Study columns with only non-bearing outcomes</span><strong>{(cov.study_columns_without_cells as string[]).join(", ")}</strong></Row>
            <Row p={p}><span>Corpus-text columns in v1</span><strong>{fmt(cov.columns_by_class.corpus_texts as number)}</strong></Row>
          </div>
          <Cites p={p}>glossa-indus/matrix/matrix.json coverage block (gate-recomputed cell-for-cell)</Cites>
          <div style={{ marginTop: 8 }}><NavLink onClick={() => go("matrix")}>Open the matrix →</NavLink></div>
        </Card>

        <Card p={p}>
          <CardHead tag="Ledger" tagColor="#2563eb" title="Claim population" />
          <BigStat>{fmt(header.claims_total)} claims, staged on the program&apos;s ladder</BigStat>
          <div style={{ marginTop: 8 }}>
            {(["created", "explained", "checked", "accepted", "digested"] as const)
              .filter((stage) => (pop.by_stage as Record<string, number>)[stage] != null)
              .map((stage) => (
                <Row p={p} key={stage}><span>stage: {stage}</span><strong>{fmt((pop.by_stage as Record<string, number>)[stage])}</strong></Row>
              ))}
            {(Object.entries(pop.by_stage as Record<string, number>))
              .filter(([stage]) => !["created", "explained", "checked", "accepted", "digested"].includes(stage))
              .map(([stage, n]) => (
                <Row p={p} key={stage}><span>stage: {stage}</span><strong>{fmt(n)}</strong></Row>
              ))}
            <Row p={p}><span>no stage recorded (bare count only)</span><strong>{fmt(pop.no_stage_recorded as number)}</strong></Row>
            {(Object.entries(pop.by_population as Record<string, number>)).map(([population, n]) => (
              <Row p={p} key={population}><span>population: {population}</span><strong>{fmt(n)}</strong></Row>
            ))}
            <Row p={p}><span>carry a falsifier</span><strong>{fmt(fal.covered as number)} of {fmt(fal.total as number)}</strong></Row>
            <div style={{ fontSize: 12.5, padding: "6px 0" }}>
              The {fmt((fal.total as number) - (fal.covered as number))} falsifier gaps are all in
              the extracted population (extracted {fal.by_population.extracted.covered as number}/
              {fal.by_population.extracted.total as number} · bundle{" "}
              {fal.by_population.bundle.covered as number}/{fal.by_population.bundle.total as number}).
            </div>
            <Row p={p}>
              <span>AEE state recorded</span>
              <strong>{(aee.with_state as number) === 0 ? `none — aee_state null on ${fmt(aee.without_state as number)} of ${fmt(aee.total as number)}` : `${fmt(aee.with_state as number)} of ${fmt(aee.total as number)}`}</strong>
            </Row>
          </div>
          <Cites p={p}>ledger stage / population fields · falsifier coverage per the Stage 1 validator</Cites>
          <div style={{ marginTop: 8 }}><NavLink onClick={() => openClaim(SPECIMEN_CLAIM)}>Open the claim view →</NavLink></div>
        </Card>

        <Card p={p}>
          <CardHead tag="Ledger" tagColor="#2563eb" title="Unresolved sign mentions" />
          <BigStat>{fmt((un.sign_mentions as AnyRec[]).length)} mentions do not resolve</BigStat>
          <p style={{ fontSize: 13, margin: "8px 0" }}>
            on {mentionClaims.size} claims. Shown verbatim; a mention that resolves to no anchor
            record is an empty state, not an error to hide.
          </p>
          {(un.sign_mentions as AnyRec[]).map((m, i) => (
            <div key={i} style={{ fontSize: 12.5, padding: "5px 0", borderBottom: `1px dashed ${p.border}`, overflowWrap: "anywhere" }}>
              “{m.mention as string}” —{" "}
              <NavLink onClick={() => openClaim(m.record as string)}>{m.record as string}</NavLink>
            </div>
          ))}
          {(un.sign_refs_without_anchor_record as AnyRec[]).map((r) => (
            <div key={r.sign_ref as string} style={{ fontSize: 12.5, padding: "5px 0", borderBottom: `1px dashed ${p.border}`, overflowWrap: "anywhere" }}>
              {r.sign_ref as string} read as <strong>M{(r.sign_ref as string).split(":")[1]}</strong>{" "}
              under the matrix&apos;s key: {r.reason as string} —{" "}
              <NavLink onClick={() => openClaim(r.row as string)}>{r.row as string}</NavLink>
            </div>
          ))}
          <Cites p={p}>ledger sign_refs verbatim · matrix coverage (unresolved sign mentions) · matrix-defs R-S1</Cites>
        </Card>

        <Card p={p}>
          <CardHead tag="Matrix" tagColor="#7c3aed" title="Sign × sign block (imported)" />
          <BigStat>{fmt(signBlock.edge_count as number)} sign-interaction edges over {fmt(signBlock.node_count as number)} signs</BigStat>
          <div style={{ marginTop: 8 }}>
            <Row p={p}><span>Pipeline reports (adjacent + co-occurrence)</span><strong>{fmt(signBlock.edge_count as number)}</strong></Row>
            <Row p={p}><span>Edge records the matrix carries</span><strong>{fmt(signBlock.edges_emitted as number)}</strong></Row>
            <Row p={p}><span>Nodes</span><strong>{fmt(signBlock.node_count as number)}</strong></Row>
            <Row p={p}><span>Corpus snapshot</span><strong>{shortHash(signBlock.corpus_sha256 as string)}</strong></Row>
          </div>
          <p style={{ fontSize: 12.5 }}>
            An imported block, not a claims relation: sign-interaction counts from the Phase-133
            pipeline over the corpus snapshot. It never enters the claims×evidence relations.
          </p>
          <Cites p={p}>matrix sign×sign block · corpus snapshot {shortHash(signBlock.corpus_sha256 as string)}</Cites>
        </Card>
      </div>
      <p style={{ fontSize: 12.5, color: p.muted, marginTop: 16 }}>
        How to read this map: the system view (this screen) shows the whole; the claim view shows
        one claim with everything the ledger says about it; the evidence view shows what bears on
        it and whether each citation carries the relation it is cited for. The matrix and the
        settling panel are the same data in their computed forms.
      </p>
    </div>
  );
}

function Chip({ children, bg }: { children: ReactNode; bg: string }) {
  return (
    <span style={{ background: bg, borderRadius: 999, padding: "2px 10px", fontSize: 12, fontWeight: 600, color: "#17202b" }}>
      {children}
    </span>
  );
}

function ClaimScreen({
  p, claim, contrast, go, openEvidence,
}: {
  p: Palette;
  claim: AnyRec;
  contrast: AnyRec | null;
  go: (s: Screen) => void;
  openEvidence: (id: string) => void;
}) {
  const cells = claim.matrix_row.cells as AnyRec[];
  const bearing = claim.settling_bearing as AnyRec | null;
  return (
    <div>
      <div style={{ fontSize: 12.5, color: p.muted, marginBottom: 6 }}>
        <NavLink onClick={() => go("system")}>System graph</NavLink> / Claim
      </div>
      <h2 style={{ fontSize: 21, margin: "0 0 8px" }}>{claim.statement as string}</h2>
      <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 16 }}>
        <Chip bg="#e0eaff">status: {claim.status as string}</Chip>
        <Chip bg="#e5e7eb">stage: {(claim.stage as string) ?? "no stage recorded"}</Chip>
        <Chip bg="#e5e7eb">population: {claim.population as string}</Chip>
        {(claim.sign_refs as string[]).length > 0 ? (
          <Chip bg="#fef3c7">sign_refs: {(claim.sign_refs as string[]).join(" · ")}</Chip>
        ) : (
          <Chip bg="#e5e7eb">no sign_refs</Chip>
        )}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(330px,1fr))", gap: 14 }}>
        <Card p={p}>
          <CardHead tag="Ledger" tagColor="#2563eb" title="The claim as ledgered" />
          <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: 0.5, textTransform: "uppercase", color: p.muted }}>Falsifier</div>
          {(claim.falsifier as string[] | null) ? (
            (claim.falsifier as string[]).map((f, i) => (
              <p key={i} style={{ fontSize: 13.5, margin: "4px 0" }}>“{f}”</p>
            ))
          ) : (
            <p style={{ fontSize: 13.5, margin: "4px 0" }}>
              No falsifier recorded — one of the named gaps in the falsifier census.
            </p>
          )}
          <p style={{ fontSize: 12.5, color: p.muted, margin: "2px 0 10px" }}>
            {claim.falsifier_counts.present as number} present ·{" "}
            {claim.falsifier_counts.evaluable == null
              ? "evaluable not recorded (no settling run touches this claim)"
              : `${claim.falsifier_counts.evaluable as number} evaluable under a settling run`}
          </p>
          <div style={{ fontSize: 11, fontWeight: 700, letterSpacing: 0.5, textTransform: "uppercase", color: p.muted }}>This does not establish</div>
          <p style={{ fontSize: 13.5, margin: "4px 0" }}>{(claim.does_not_establish as string) ?? "Not recorded on this entry."}</p>
          {(claim.sources as AnyRec[]).map((s, i) => (
            <div key={i} style={{ fontSize: 12.5, color: p.muted, marginTop: 8 }}>
              Source: {s.document_id as string} ({s.role as string}) · {s.path as string} · sha256 {shortHash(s.sha256 as string)}
            </div>
          ))}
          <Cites p={p}>ledger entry {claim.id as string}</Cites>
        </Card>

        <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
          <Card p={p}>
            <CardHead tag="Computed · settling" tagColor="#b45309" title="Settling bearing" />
            {!bearing ? (
              <p style={{ fontSize: 13.5, margin: 0 }}>
                No settling run touches this claim: it carries no sign_refs a run&apos;s candidate
                assigns, so no run record names it. The absence is shown, not filled.
              </p>
            ) : (
              <>
                {(bearing.runs as AnyRec[]).map((r) => (
                  <div key={r.record as string} style={{ fontSize: 13.5, padding: "4px 0" }}>
                    <strong>{r.candidate as string}</strong> run — via {(r.via_signs as string[]).join(", ")}: supporting{" "}
                    {r.tallies.supporting as number} · opposing {r.tallies.opposing as number} · constraining{" "}
                    {r.tallies.constraining as number} · falsifiers {r.falsifiers_present as number} present ·{" "}
                    {r.falsifiers_evaluable as number} evaluable
                  </div>
                ))}
                <p style={{ fontSize: 13 }}>
                  Divergent between the two runs: {bearing.divergent ? "yes" : "no"} — the per-sign
                  detail is on the evidence view.
                </p>
              </>
            )}
            <p style={{ fontSize: 12.5, color: p.muted }}>
              S-R2 value-independence (GAP-S2): the tallies count relation types only — a claim
              whose signs a run assigns still counts its ledgered relations, whatever the readings
              are. The count cannot see a reading&apos;s content; that limitation is registered in
              the semantics, not hidden here.
            </p>
            <Cites p={p}>run records under glossa-indus/ledger/runs/ · comparison record (T405)</Cites>
          </Card>

          <Card p={p}>
            <CardHead tag="Ledger field" tagColor="#2563eb" title="Displayed score" />
            <p style={{ fontSize: 13.5, margin: "0 0 6px" }}>
              <strong>{SCORE_LABEL}</strong>
            </p>
            {(claim.displayed_score as AnyRec).state === "empty" ? (
              <p style={{ fontSize: 13, margin: 0 }}>
                No AEE state is recorded on this claim — aee_state: null, as on all claims in the
                ledger. The slot renders the definition and the empty state; it never renders a
                number the ledger does not carry, and the map computes no score of its own.
              </p>
            ) : (
              <p style={{ fontSize: 13, margin: 0 }}>
                aee_state as recorded on the ledger entry: {JSON.stringify(claim.aee_state)}.
              </p>
            )}
            <Cites p={p}>ledger field aee_state on {claim.id as string} (null)</Cites>
          </Card>
        </div>

        <Card p={p} style={{ gridColumn: "1 / -1" }}>
          <CardHead tag="Matrix" tagColor="#7c3aed" title="Its matrix row" />
          {cells.length === 0 ? (
            <div>
              <p style={{ fontSize: 13.5, margin: "0 0 8px" }}>
                This claim&apos;s matrix row is <strong>empty</strong>: no document, study, anchor,
                research check or corpus text bears a recorded relation on it. An empty row is a
                fact about the record, shown as one.
              </p>
              {contrast && (
                <div style={{ background: p.softBg, borderRadius: 6, padding: "10px 12px", fontSize: 13 }}>
                  <strong>For contrast — a populated row:</strong> {contrast.id as string} carries{" "}
                  {(contrast.matrix_row.cells as AnyRec[]).length} cells:
                  {(contrast.matrix_row.cells as AnyRec[]).map((c, i) => (
                    <span key={i}>
                      {" "}<strong style={{ color: REL_COLOR[c.relation as string] }}>{c.relation as string}</strong> on{" "}
                      {c.column as string} (rule {c.rule as string});
                    </span>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div>
              {cells.map((c, i) => (
                <div key={i} style={{ fontSize: 13.5, padding: "4px 0", borderBottom: `1px dashed ${p.border}` }}>
                  <strong style={{ color: REL_COLOR[c.relation as string] }}>{c.relation as string}</strong> — {c.column as string}{" "}
                  ({c.column_class as string}, rule {c.rule as string}) · citations: {(c.citations as string[]).join(" · ")}
                </div>
              ))}
            </div>
          )}
          <Cites p={p}>matrix row for {claim.id as string} · matrix-defs v1 rules R1–R4</Cites>
        </Card>
      </div>
      <div style={{ marginTop: 14, display: "flex", gap: 16 }}>
        <NavLink onClick={() => openEvidence(claim.id as string)}>Evidence view →</NavLink>
        <NavLink onClick={() => go("system")}>← System view</NavLink>
      </div>
    </div>
  );
}

function EvidenceScreen({
  p, claim, evidence, go, openClaim, goMatrix,
}: {
  p: Palette;
  claim: AnyRec;
  evidence: AnyRec;
  go: (s: Screen) => void;
  openClaim: (id: string) => void;
  goMatrix: () => void;
}) {
  const summary = evidence.column_summary as AnyRec;
  const classNote: Record<string, string> = {
    documents: "its own document is provenance (a source), never a bearing cell",
    studies: "no study outcome block cites this claim",
    anchors: "the whole class is unused in the matrix (no claim×anchor cells exist)",
    research_checks: "checks attach as annotations; every verdict is null (advisory)",
    corpus_texts: "the class carries no columns in v1",
  };
  const signRecords = evidence.sign_records as AnyRec[];
  const doc = evidence.source_document as AnyRec | null;
  const annotations = claim.annotations as AnyRec[];
  return (
    <div>
      <div style={{ fontSize: 12.5, color: p.muted, marginBottom: 6 }}>
        <NavLink onClick={() => go("system")}>System graph</NavLink> /{" "}
        <NavLink onClick={() => openClaim(claim.id as string)}>Claim</NavLink> / Evidence
      </div>
      <h2 style={{ fontSize: 21, margin: "0 0 4px" }}>What bears on this claim</h2>
      <p style={{ fontSize: 13, color: p.muted, margin: "0 0 16px" }}>
        {claim.id as string} — “{claim.statement as string}” Every column class is accounted for,
        including the empty ones.
      </p>
      <div style={{ display: "flex", gap: 10, flexWrap: "wrap", marginBottom: 14 }}>
        {(Object.entries(summary) as [string, AnyRec][]).map(([cls, v]) => (
          <div key={cls} style={{ flex: "1 1 180px", background: p.cardBg, border: `1px solid ${p.border}`, borderRadius: 8, padding: "10px 12px" }}>
            <div style={{ fontSize: 12, fontWeight: 700, textTransform: "capitalize" }}>{cls.replace(/_/g, " ")}</div>
            <div style={{ fontSize: 18, fontWeight: 700 }}>
              {fmt(v.columns as number)} cols · {(v.cells as number) === 0 ? "0 cells" : `${fmt(v.cells as number)} cells`}
            </div>
            <div style={{ fontSize: 11.5, color: p.muted }}>{(v.cells as number) === 0 ? classNote[cls] : "cells on this claim — see its matrix row"}</div>
          </div>
        ))}
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(330px,1fr))", gap: 14 }}>
        {doc && (
          <Card p={p}>
            <CardHead tag="Ledger" tagColor="#2563eb" title="Source of record" />
            <div style={{ fontSize: 13.5 }}>
              <div><strong>{doc.document_id as string}</strong> — {doc.role as string}</div>
              <div style={{ color: p.muted, fontSize: 12.5, overflowWrap: "anywhere" }}>{doc.path as string}</div>
              <div style={{ color: p.muted, fontSize: 12.5 }}>sha256 {shortHash(doc.sha256 as string)}</div>
            </div>
            <p style={{ fontSize: 12.5, color: p.muted }}>
              The document the claim was extracted from. Provenance is not a bearing relation: a
              claim&apos;s own document never appears as a supports cell for it.
            </p>
            <Cites p={p}>ledger sources[] on {claim.id as string} · source-file hash verified by the gate (V1)</Cites>
          </Card>
        )}

        {annotations.length > 0 && (
          <Card p={p}>
            <CardHead tag="Ledger" tagColor="#2563eb" title="Research checks recorded against this claim" />
            {annotations.map((a) => (
              <div key={a.id as string} style={{ fontSize: 13.5 }}>
                <div>
                  <strong>{(a.id as string).replace("annotation/", "")}</strong> · checked{" "}
                  {(a.bearing.checked_at as string).slice(0, 10)}
                </div>
                <div style={{ fontSize: 12.5, color: p.muted }}>
                  {a.bearing.neighbors_surfaced as number} nearest neighbours surfaced ·{" "}
                  {a.bearing.gaps as number} gap(s) found · verdict:{" "}
                  {a.bearing.verdict == null ? "none recorded (advisory)" : (a.bearing.verdict as string)} ·{" "}
                  protocol {a.bearing.protocol as string}
                </div>
                <div style={{ fontSize: 12.5, color: p.muted, overflowWrap: "anywhere" }}>
                  sidecar {a.sidecar.path as string} · sha256 {shortHash(a.sidecar.sha256 as string)}
                </div>
              </div>
            ))}
            <p style={{ fontSize: 12.5, color: p.muted }}>
              An annotation is a ledgered record about the claim, written under the audit
              protocol. It is not a verdict on the claim and changes no status.
            </p>
            <Cites p={p}>ledger annotations targeting {claim.id as string}</Cites>
          </Card>
        )}

        {signRecords.length > 0 && (
          <Card p={p} style={{ gridColumn: "1 / -1" }}>
            <CardHead tag="Ledger + register" tagColor="#2563eb" title="Its sign references, in both layers' keys" />
            <div style={{ overflowX: "auto" }}>
              <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 13 }}>
                <thead>
                  <tr>
                    {["Sign (ledger ref)", "The matrix's record", "The register's record (settling key)", "Strict set"].map((h) => (
                      <th key={h} style={{ textAlign: "left", padding: "6px 8px", borderBottom: `1px solid ${p.border}`, color: p.muted, fontSize: 12 }}>{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {signRecords.map((r) => (
                    <tr key={r.sign_ref as string}>
                      <td style={{ padding: "6px 8px", borderBottom: `1px solid ${p.border}` }}>{r.sign_ref as string}</td>
                      <td style={{ padding: "6px 8px", borderBottom: `1px solid ${p.border}` }}>
                        {r.matrix_key as string} — {r.matrix_record ? "a register record exists under this key (unused as a matrix column)" : "no anchor record under this key"}
                      </td>
                      <td style={{ padding: "6px 8px", borderBottom: `1px solid ${p.border}` }}>
                        {r.settle_record
                          ? `${r.settle_key as string} — reading ${r.settle_record.reading as string}, confidence ${r.settle_record.confidence as string}`
                          : `${r.settle_key as string} — no register record under this key either`}
                      </td>
                      <td style={{ padding: "6px 8px", borderBottom: `1px solid ${p.border}` }}>{r.settle_record?.strict ? "yes" : "no"}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            {signRecords.some((r) => r.divergence) && (
              <div style={{ background: "#fef2f2", border: "1px solid #fca5a5", borderLeft: "4px solid #b91c1c", borderRadius: 6, padding: "10px 12px", fontSize: 13, color: "#17202b", marginTop: 10 }}>
                <strong>Two layers name the same signs differently — and the map shows both.</strong>{" "}
                The matrix generator keys an anchor record M + the number as written, unpadded (M64),
                which matches no register key, so the matrix&apos;s anchor columns carry no sign
                cells. The settling layer keys records M + the number padded to three digits
                (M064), which resolves. Both keys are shown wherever a sign is named; neither is
                silently corrected.
              </div>
            )}
            <Cites p={p}>ledger sign_refs on {claim.id as string} · matrix-defs §2 key rule · glossa-settle-1 §2 key rule · anchor register records</Cites>
          </Card>
        )}
      </div>
      <div style={{ marginTop: 14, display: "flex", gap: 16 }}>
        <NavLink onClick={() => openClaim(claim.id as string)}>← Claim view</NavLink>
        <NavLink onClick={goMatrix}>Open the matrix →</NavLink>
      </div>
    </div>
  );
}

function MatrixScreen({
  p, data, rowClaims, selected, filterClaim, go, openClaim,
}: {
  p: Palette;
  data: AnyRec;
  rowClaims: AnyRec[];
  selected: AnyRec | null;
  filterClaim: AnyRec | null;
  go: (s: Screen) => void;
  openClaim: (id: string) => void;
}) {
  const cov = data.coverage as AnyRec;
  const byClass = cov.columns_by_class as Record<string, number>;
  const relations = cov.cells_by_relation as Record<string, number>;
  const signBlock = data.sign_sign_block as AnyRec;
  const specimenCols: string[] = [];
  for (const rc of rowClaims) {
    for (const c of rc.matrix_row.cells as AnyRec[]) {
      if (!specimenCols.includes(c.column as string)) specimenCols.push(c.column as string);
    }
  }
  const cellFor = (rc: AnyRec, col: string) =>
    (rc.matrix_row.cells as AnyRec[]).find((c) => c.column === col);
  const selCell = selected
    ? (selected.matrix_row.cells as AnyRec[]).find((c) => c.column_class === "studies")
    : null;
  const chip: CSSProperties = {
    border: `1px solid ${p.border}`, borderRadius: 999, padding: "3px 11px",
    fontSize: 12.5, background: p.cardBg,
  };
  return (
    <div>
      <h2 style={{ fontSize: 21, margin: "0 0 4px" }}>Claims × evidence — the generated matrix</h2>
      <p style={{ fontSize: 13, color: p.muted, margin: "0 0 14px", maxWidth: 900 }}>
        The claims×evidence matrix is a generated layer: every cell below is recomputed from the
        ledger by the gate on every run. Relations are stated as words — supports, opposes,
        constrains — never as colors or heat.
      </p>
      <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 8 }}>
        <span style={{ ...chip, background: "#2563eb", color: "#fff", borderColor: "#2563eb", fontWeight: 700 }}>Claims × Evidence (primary form)</span>
        <span style={chip}>Sign × Sign block (imported · {fmt(signBlock.node_count as number)} nodes)</span>
        {filterClaim && (
          <span style={chip}>
            Sign row-filter: any sign_ref — 1 claim · {(filterClaim.sign_refs as string[]).join(" · ")}
          </span>
        )}
      </div>
      <div style={{ display: "flex", gap: 6, flexWrap: "wrap", marginBottom: 14 }}>
        <span style={chip}>Documents {fmt(byClass.documents)}</span>
        <span style={chip}>Studies {fmt(byClass.studies)}</span>
        <span style={{ ...chip, opacity: 0.55 }}>Anchors {fmt(byClass.anchors)} — all unused</span>
        <span style={{ ...chip, opacity: 0.55 }}>Research checks {fmt(byClass.research_checks)} — all unused</span>
        <span style={{ ...chip, opacity: 0.55 }}>Corpus texts {fmt(byClass.corpus_texts)}</span>
        <span style={{ ...chip, color: "#15803d", fontWeight: 700 }}>supports {fmt(relations.supports)}</span>
        <span style={{ ...chip, color: "#b91c1c", fontWeight: 700 }}>opposes {fmt(relations.opposes)}</span>
        <span style={chip}>constrains {fmt(relations.constrains)}</span>
      </div>
      <Card p={p} style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ overflowX: "auto" }}>
          <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 12.5 }}>
            <thead>
              <tr style={{ background: p.softBg }}>
                <th style={{ textAlign: "left", padding: "8px 12px", borderBottom: `1px solid ${p.border}` }}>Claim (row)</th>
                {specimenCols.map((c) => (
                  <th key={c} style={{ textAlign: "left", padding: "8px 12px", borderBottom: `1px solid ${p.border}` }}>{c}</th>
                ))}
                <th style={{ textAlign: "left", padding: "8px 12px", borderBottom: `1px solid ${p.border}`, color: p.muted }}>anchors ({fmt(byClass.anchors)}, unused)</th>
                <th style={{ textAlign: "left", padding: "8px 12px", borderBottom: `1px solid ${p.border}`, color: p.muted }}>research checks ({fmt(byClass.research_checks)}, unused)</th>
                <th style={{ textAlign: "left", padding: "8px 12px", borderBottom: `1px solid ${p.border}`, color: p.muted }}>corpus texts (0)</th>
              </tr>
            </thead>
            <tbody>
              {rowClaims.map((rc) => (
                <tr key={rc.id as string}>
                  <td style={{ padding: "7px 12px", borderBottom: `1px solid ${p.border}` }}>
                    <NavLink onClick={() => openClaim(rc.id as string)}>{rc.id as string}</NavLink>
                    {(rc.matrix_row.cells as AnyRec[]).length === 0 && (
                      <span style={{ color: p.muted }}> — empty row</span>
                    )}
                  </td>
                  {specimenCols.map((c) => {
                    const cell = cellFor(rc, c);
                    return (
                      <td key={c} style={{ padding: "7px 12px", borderBottom: `1px solid ${p.border}` }}>
                        {cell ? (
                          <strong style={{ color: REL_COLOR[cell.relation as string] }}>{cell.relation as string}</strong>
                        ) : (
                          <span style={{ color: p.muted }}>·</span>
                        )}
                      </td>
                    );
                  })}
                  <td style={{ padding: "7px 12px", borderBottom: `1px solid ${p.border}`, color: p.muted }}>—</td>
                  <td style={{ padding: "7px 12px", borderBottom: `1px solid ${p.border}`, color: p.muted }}>—</td>
                  <td style={{ padding: "7px 12px", borderBottom: `1px solid ${p.border}`, color: p.muted }}>—</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <div style={{ padding: "9px 12px", fontSize: 12, color: p.muted, borderTop: `1px solid ${p.border}` }}>
          Showing {rowClaims.length} of {fmt(cov.rows_total as number)} rows · relations are words,
          never colors or heat · unused classes are aggregated, never drawn as empty grids · the
          full matrix is served from the gated artifact and paged, never truncated silently.
        </div>
      </Card>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(330px,1fr))", gap: 14, marginTop: 14 }}>
        {selected && selCell && (
          <div style={{ background: "#eff6ff", border: "1px solid #bfdbfe", borderLeft: "4px solid #2563eb", borderRadius: 8, padding: "12px 14px", fontSize: 13, color: "#17202b" }}>
            <strong>Selected cell — {selected.id as string} × study {selCell.column as string}:</strong>{" "}
            <strong style={{ color: "#b91c1c" }}>{selCell.relation as string}</strong> (rule {selCell.rule as string}).
            Its citations are the claim id itself and the dated outcome appends on the study record —
            the governing append carries the relation; the superseded append stays on the cell,
            labeled. The gate requires every citation on a cell to carry its relation (Amendment 1).
            <div style={{ marginTop: 6, color: "#5b6b7d", fontSize: 12 }}>
              Citations: {(selCell.citations as string[]).join(" · ")}
            </div>
          </div>
        )}
        <div style={{ background: p.softBg, border: `1px solid ${p.border}`, borderRadius: 8, padding: "12px 14px", fontSize: 13 }}>
          <strong>{fmt((cov.empty_rows as string[]).length)} rows carry no cells at all</strong> —{" "}
          {(cov.empty_rows as string[]).slice(0, 4).join(", ")} and{" "}
          {fmt((cov.empty_rows as string[]).length - 4)} more — named in the coverage data, not
          silently absent.
          {filterClaim && (
            <>
              {" "}Filtering by any sign_ref returns exactly one row: {filterClaim.id as string}.
            </>
          )}
        </div>
      </div>
      <div style={{ marginTop: 14 }}>
        <NavLink onClick={() => go("system")}>← System view</NavLink>
      </div>
    </div>
  );
}

function SettlingScreen({ p, data, go }: { p: Palette; data: AnyRec; go: (s: Screen) => void }) {
  const runs = data.runs as AnyRec[];
  const comp = (data.comparison as AnyRec).result as AnyRec;
  const scenarios = (data.canonicals as AnyRec).scenarios as AnyRec[];
  const reach = data.reach as AnyRec;
  const sets = (data.assignment_sets as AnyRec).sets as AnyRec[];
  const deltas = comp.coverage_deltas as AnyRec;
  const deltaLine = (key: string) =>
    `${deltas[key].incumbent as number} → ${deltas[key].full_register as number}`;
  const th: CSSProperties = { textAlign: "left", padding: "6px 8px", borderBottom: `1px solid ${p.border}`, color: p.muted, fontSize: 12 };
  const td: CSSProperties = { padding: "6px 8px", borderBottom: `1px solid ${p.border}` };
  return (
    <div>
      <h2 style={{ fontSize: 21, margin: "0 0 4px" }}>Settling — what the recorded assignments imply</h2>
      <p style={{ fontSize: 13.5, margin: "0 0 14px", maxWidth: 900 }}>{data.label as string}</p>
      <div style={{ background: "#fffbeb", border: "1px solid #f59e0b", borderLeft: "4px solid #f59e0b", borderRadius: 8, padding: "12px 16px", fontSize: 13.5, color: "#17202b", marginBottom: 14 }}>
        <strong>This panel is a computed layer.</strong> A settling run reads the ledger&apos;s
        relations and an assignment set, and writes only a run record; it never changes a
        claim&apos;s status, stage, or any ledgered verdict (C086-16). What it establishes is what
        the ledger implies under the registered rules — not what the script says.
      </div>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(330px,1fr))", gap: 14 }}>
        <Card p={p}>
          <CardHead tag="Ledger" tagColor="#2563eb" title="Run inputs" />
          <Row p={p}><span>Semantics</span><strong>{data.semantics as string} (registered, readonly)</strong></Row>
          {sets.map((s) => (
            <Row p={p} key={s.id as string}>
              <span>Assignment set: {s.id as string} ({s.frame as string})</span>
              <strong>{fmt(s.assignments as number)} assignments</strong>
            </Row>
          ))}
          <Row p={p}><span>Scope (both runs)</span><strong>full frame — mahadevan, {fmt(runs[0]?.scope_signs as number)} signs in frame</strong></Row>
          <p style={{ fontSize: 12.5, color: p.muted }}>
            User-built anchor sets saved in the app are excluded in v1 (Spec 086 §8 Q3): a run the
            gate cannot recompute cannot be carried by the map. The exclusion is stated, not silent.
          </p>
          <div style={{ background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 6, padding: "9px 11px", fontSize: 12.5, color: "#17202b" }}>
            <strong>Pins.</strong> Every run record pins the ledger, corpus and register hashes it
            ran over. A comparison is only as good as its pins: if the two runs&apos; pins differ,
            the comparison is falsified, not reinterpreted (C086-15). The gate checks the pins on
            every run.
          </div>
          <Cites p={p}>glossa-indus/ledger/assignment-sets.json · run records&apos; pins blocks</Cites>
        </Card>

        <Card p={p}>
          <CardHead tag="Computed · settling" tagColor="#b45309" title="Canonical scenarios (the semantics' own record)" />
          {scenarios.map((c) => (
            <div key={c.id as string} style={{ fontSize: 13, padding: "5px 0", borderBottom: `1px dashed ${p.border}` }}>
              <strong>{c.id as string}</strong> — {(c.expected.assigned as AnyRec[]).length === 0
                ? "null candidate (no assignments)"
                : `${(c.expected.assigned as AnyRec[]).length} assignments: ${(c.expected.assigned as AnyRec[]).map((a) => `${a.sign as string}→${a.value as string}`).join(", ")}`}
              <div style={{ color: p.muted, fontSize: 12.5 }}>
                contexts {c.expected.contexts_touched as number} · consistent {c.expected.consistent as number} ·{" "}
                non-strict {c.expected.non_strict_contexts as number} · conflicts {(c.expected.conflicts as AnyRec[]).length} ·{" "}
                forced {(c.expected.forced as AnyRec[]).map((f) => `${f.sign as string}→${f.value as string}`).join(", ") || "none"} ·{" "}
                touches {c.expected.claims_touched_count as number} claim(s)
              </div>
              {(c.expected.conflicts as AnyRec[]).map((cf, i) => (
                <div key={i} style={{ color: "#b91c1c", fontSize: 12.5 }}>
                  conflict: {cf.sign as string}, {cf.anchor as string}, {cf.assigned_value as string} ≠ {cf.anchor_reading as string}
                </div>
              ))}
            </div>
          ))}
          <Cites p={p}>glossa-indus/ledger/settling-canonical.json (gate-recomputed under V8)</Cites>
        </Card>
      </div>

      <Card p={p} style={{ marginTop: 14 }}>
        <CardHead tag="Computed · settling" tagColor="#b45309" title="Stored runs of record (T405)" />
        <div style={{ overflowX: "auto" }}>
          <table style={{ borderCollapse: "collapse", width: "100%", fontSize: 13 }}>
            <thead>
              <tr>
                {["Run", "Assigned", "Contexts", "Strict ctx", "Consistent", "Non-strict", "Conflicts", "Agreement", "Forced"].map((h) => (
                  <th key={h} style={th}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {runs.map((r) => (
                <tr key={r.record as string}>
                  <td style={td}><strong>{r.candidate as string}</strong><div style={{ color: p.muted, fontSize: 11.5 }}>{r.record as string}</div></td>
                  <td style={td}>{fmt(r.assigned_count as number)}</td>
                  <td style={td}>{fmt(r.contexts_touched as number)}</td>
                  <td style={td}>{fmt(r.strict_contexts as number)}</td>
                  <td style={td}>{fmt(r.consistent as number)}</td>
                  <td style={td}>{fmt(r.non_strict_contexts as number)}</td>
                  <td style={td}>{fmt((r.conflicts as AnyRec[]).length)}</td>
                  <td style={td}>{(r.strict_agreement_share as number).toFixed(2)}</td>
                  <td style={td}>{fmt((r.forced as AnyRec[]).length)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <p style={{ fontSize: 12.5, color: p.muted, margin: "8px 0 0" }}>
          {runs.map((r) => `${r.candidate as string}: ledger ${shortHash(r.pins.ledger.sha256 as string)} · corpus ${shortHash(r.pins.corpus_snapshot.sha256 as string)} · anchors ${shortHash(r.pins.anchors_register.sha256_raw_bytes as string)}`).join(" · ")} — same pins on both runs.
        </p>
        <Cites p={p}>glossa-indus/ledger/runs/ (2 run records) · semantics glossa-settle-1</Cites>
      </Card>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit,minmax(330px,1fr))", gap: 14, marginTop: 14 }}>
        <Card p={p}>
          <CardHead tag="Computed · settling" tagColor="#b45309" title="Divergence view — the stored comparison" />
          <BigStat>
            {(comp.claims_compared as AnyRec[]).length} claim compared · {(comp.per_claim_divergences as AnyRec[]).length} divergent
          </BigStat>
          {(comp.claims_compared as AnyRec[]).map((cc) => (
            <div key={cc.claim as string} style={{ fontSize: 13.5, padding: "6px 0" }}>
              {cc.claim as string} — tallies incumbent {cc.incumbent_tallies.supporting as number}/
              {cc.incumbent_tallies.opposing as number}/{cc.incumbent_tallies.constraining as number} ·
              full-register {cc.full_register_tallies.supporting as number}/
              {cc.full_register_tallies.opposing as number}/{cc.full_register_tallies.constraining as number} ·
              divergent: {cc.divergent ? "yes" : "no"}
            </div>
          ))}
          <Row p={p}><span>Assigned: incumbent → full-register</span><strong>{deltaLine("assigned_count")}</strong></Row>
          <Row p={p}><span>Contexts</span><strong>{deltaLine("contexts_touched")}</strong></Row>
          <Row p={p}><span>Conflicts</span><strong>{deltaLine("conflicts")}</strong></Row>
          <Row p={p}>
            <span>Signs assigned by the full-register run only</span>
            <strong>{fmt((comp.signs_assigned_by_one_only.full_register_only as string[]).length)}</strong>
          </Row>
          <p style={{ fontSize: 12.5, color: p.muted }}>
            Pre-registered expectations: {comp.pre_registered_expectations_note as string}
          </p>
          <Cites p={p}>comparison record under specs/086 (T405) · pins verified by the gate</Cites>
        </Card>

        <Card p={p}>
          <CardHead tag="Computed · settling" tagColor="#b45309" title="Reach — what no run here can touch" />
          <Row p={p}>
            <span>Positional-class rule (S-R3)</span>
            <strong style={{ color: "#b45309" }}>{reach.s_r3.status as string}</strong>
          </Row>
          <p style={{ fontSize: 13 }}>{reach.s_r3.note as string}</p>
          <Row p={p}>
            <span>Claims no run of record touches</span>
            <strong>{fmt(reach.claims_untouched_by_any_run as number)} of {fmt(reach.claims_total as number)}</strong>
          </Row>
          <p style={{ fontSize: 12.5, color: p.muted }}>
            A run touches a claim only through the claim&apos;s ledgered sign_refs.{" "}
            {fmt(reach.claims_with_sign_refs as number)} of {fmt(reach.claims_total as number)} claims
            carry any, so the settling layer&apos;s stated reach over the claim population is
            exactly that narrow — shown, not rounded up.
          </p>
          <Cites p={p}>run records&apos; claims_touched · ledger sign_refs census</Cites>
        </Card>
      </div>
      <div style={{ marginTop: 14, display: "flex", gap: 16 }}>
        <NavLink onClick={() => go("system")}>← System view</NavLink>
        <NavLink onClick={() => go("matrix")}>Open the matrix →</NavLink>
      </div>
    </div>
  );
}

export function SystemGraphView({ darkMode }: { darkMode: boolean }) {
  const p = palette(darkMode);
  const [screen, setScreen] = useState<Screen>("system");
  const [header, setHeader] = useState<IndusMapHeader | null>(null);
  const [stamp, setStamp] = useState<IndusMapStamp | null>(null);
  const [system, setSystem] = useState<AnyRec | null>(null);
  const [matrix, setMatrix] = useState<AnyRec | null>(null);
  const [settling, setSettling] = useState<AnyRec | null>(null);
  const [claim, setClaim] = useState<AnyRec | null>(null);
  const [contrast, setContrast] = useState<AnyRec | null>(null);
  const [evidence, setEvidence] = useState<AnyRec | null>(null);
  const [rowClaims, setRowClaims] = useState<AnyRec[]>([]);
  const [selected, setSelected] = useState<AnyRec | null>(null);
  const [filterClaim, setFilterClaim] = useState<AnyRec | null>(null);
  const [error, setError] = useState<string | null>(null);

  const absorb = useCallback((env: IndusMapEnvelope) => {
    setHeader(env.header);
    setStamp(env.stamp);
  }, []);

  useEffect(() => {
    let live = true;
    fetchIndusMapSystem()
      .then((env) => {
        if (!live) return;
        absorb(env);
        setSystem(env.system as AnyRec);
      })
      .catch((e: Error) => live && setError(e.message));
    return () => {
      live = false;
    };
  }, [absorb]);

  const go = useCallback(
    (s: Screen) => {
      setScreen(s);
      setError(null);
      if (s === "matrix" && !matrix) {
        fetchIndusMapMatrix()
          .then(async (env) => {
            absorb(env);
            const m = env.matrix as AnyRec;
            setMatrix(m);
            const firstRows = (m.rows as AnyRec[]).slice(0, 5).map((r) => r.id as string);
            const ids = [...firstRows, CONTRAST_CLAIM, SPECIMEN_CLAIM];
            const recs = await Promise.all(ids.map((id) => fetchIndusMapClaim(id)));
            const byId = new Map(recs.map((r) => [(r.claim as AnyRec).id as string, r.claim as AnyRec]));
            setRowClaims(
              [...firstRows, CONTRAST_CLAIM].map((id) => byId.get(id)).filter(Boolean) as AnyRec[],
            );
            setSelected(byId.get(CONTRAST_CLAIM) ?? null);
            setFilterClaim(byId.get(SPECIMEN_CLAIM) ?? null);
          })
          .catch((e: Error) => setError(e.message));
      }
      if (s === "settling" && !settling) {
        fetchIndusMapSettling()
          .then((env) => {
            absorb(env);
            setSettling(env.settling as AnyRec);
          })
          .catch((e: Error) => setError(e.message));
      }
      if (s === "system" && !system) {
        fetchIndusMapSystem()
          .then((env) => {
            absorb(env);
            setSystem(env.system as AnyRec);
          })
          .catch((e: Error) => setError(e.message));
      }
    },
    [absorb, matrix, settling, system],
  );

  const openClaim = useCallback(
    (id: string) => {
      setError(null);
      fetchIndusMapClaim(id)
        .then(async (env) => {
          absorb(env);
          const rec = env.claim as AnyRec;
          setClaim(rec);
          setContrast(null);
          if ((rec.matrix_row.cells as AnyRec[]).length === 0 && id !== CONTRAST_CLAIM) {
            const c = await fetchIndusMapClaim(CONTRAST_CLAIM);
            setContrast(c.claim as AnyRec);
          }
          setScreen("claim");
        })
        .catch((e: Error) => setError(e.message));
    },
    [absorb],
  );

  const openEvidence = useCallback(
    (id: string) => {
      setError(null);
      Promise.all([fetchIndusMapClaim(id), fetchIndusMapClaimEvidence(id)])
        .then(([cEnv, eEnv]) => {
          absorb(eEnv);
          setClaim(cEnv.claim as AnyRec);
          setEvidence(eEnv.evidence as AnyRec);
          setScreen("evidence");
        })
        .catch((e: Error) => setError(e.message));
    },
    [absorb],
  );

  if (error) {
    return (
      <div style={{ padding: 24 }}>
        <h2 style={{ marginTop: 0 }}>System graph</h2>
        <p>The map data could not be loaded: {error}</p>
      </div>
    );
  }
  if (!header || !stamp) {
    return <div style={{ padding: 24, color: p.muted }}>Loading the layered map…</div>;
  }
  const showTabs = screen === "system" || screen === "matrix" || screen === "settling";
  return (
    <div style={{ padding: "20px 24px", maxWidth: 1240, margin: "0 auto" }}>
      <HeaderStrip header={header} stamp={stamp} />
      {showTabs && <ScreenTabs p={p} active={screen} go={go} />}
      {screen === "system" && (system ? (
        <SystemScreen p={p} header={header} data={system} go={go} openClaim={openClaim} />
      ) : (
        <div style={{ color: p.muted }}>Loading…</div>
      ))}
      {screen === "matrix" && (matrix ? (
        <MatrixScreen p={p} data={matrix} rowClaims={rowClaims} selected={selected} filterClaim={filterClaim} go={go} openClaim={openClaim} />
      ) : (
        <div style={{ color: p.muted }}>Loading…</div>
      ))}
      {screen === "settling" && (settling ? (
        <SettlingScreen p={p} data={settling} go={go} />
      ) : (
        <div style={{ color: p.muted }}>Loading…</div>
      ))}
      {screen === "claim" && claim && (
        <ClaimScreen p={p} claim={claim} contrast={contrast} go={go} openEvidence={openEvidence} />
      )}
      {screen === "evidence" && claim && evidence && (
        <EvidenceScreen p={p} claim={claim} evidence={evidence} go={go} openClaim={openClaim} goMatrix={() => go("matrix")} />
      )}
    </div>
  );
}
