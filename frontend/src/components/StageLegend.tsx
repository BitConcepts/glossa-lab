/**
 * StageLegend — shared Spec 029 Phase E2 rendering pieces.
 *
 * Lane discipline (FR-029-09 / FR-029-10; claims F029-C06/C07/C13;
 * OD-4): lane 1 is machine-speed verification (verdicts, AEE scores
 * and bands, extraction statuses — checking vocabulary only); lane 2
 * is human-paced settlement (the lifecycle stage, explanation and
 * digestion records, contest state). The two are rendered in
 * separate, labelled regions and never in each other's vocabulary.
 *
 * The five stage names are Tao's, verbatim (OD-4) — created,
 * checked, explained, accepted, digested — on every surface, with
 * no synonym mapping. The legend below is the OD-4 one-line reader
 * aid; it defines the names, it does not rename them.
 */
import type { BundleSerialization } from "../api";

// ── The five stages, verbatim (OD-4) ───────────────────────────────────────

export const STAGE_NAMES = [
  "created",
  "checked",
  "explained",
  "accepted",
  "digested",
] as const;

export type StageName = (typeof STAGE_NAMES)[number];

/** Plain-language definitions for the legend (OD-4 reader aid). */
export const STAGE_DEFINITIONS: Record<StageName, string> = {
  created: "the claim has been recorded; nothing about it has been checked yet",
  checked:
    "machine-speed checks have run against the claim's evidence — being created and checked alone never settles a claim",
  explained:
    "a named human has written an account of the claim that other people can read and challenge",
  accepted:
    "a named human's explanation of the claim is on record and the claim stands accepted on the strength of that account",
  digested:
    "scholars independent of the program have engaged with the explanation — reused it, challenged it and been answered, or built on how it works",
};

const STAGE_COLORS: Record<string, string> = {
  created: "#64748b",
  checked: "#2563eb",
  explained: "#7c3aed",
  accepted: "#b45309",
  digested: "#15803d",
};

/** Stage colours live in the lane-2 region alone (FR-029-10). */
export function stageColor(stage: string | null | undefined): string {
  return (stage && STAGE_COLORS[stage]) || "#64748b";
}

// ── The OD-4 legend ────────────────────────────────────────────────────────

export function StageLegend({
  fg,
  muted,
  border,
}: {
  fg: string;
  muted: string;
  border: string;
}) {
  return (
    <div
      data-testid="stage-legend"
      style={{
        border: `1px solid ${border}`,
        borderRadius: 8,
        padding: "10px 14px",
        marginBottom: 14,
      }}
    >
      <div style={{ fontSize: 11, fontWeight: 700, color: fg, marginBottom: 4 }}>
        The five stages — lane 2 (human-paced settlement)
      </div>
      <div style={{ fontSize: 11, color: fg, marginBottom: 6 }}>
        {STAGE_NAMES.join(" → ")}
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 2 }}>
        {STAGE_NAMES.map((s) => (
          <div key={s} style={{ fontSize: 11, lineHeight: 1.45 }}>
            <span style={{ fontWeight: 700, color: stageColor(s) }}>{s}</span>
            <span style={{ color: muted }}> — {STAGE_DEFINITIONS[s]}.</span>
          </div>
        ))}
      </div>
      <div style={{ fontSize: 11, color: muted, marginTop: 6, fontStyle: "italic" }}>
        Creation and checking alone never settle a claim: a claim is settled only
        by moving through all five stages.
      </div>
    </div>
  );
}

// ── What remains not understood (FR-029-09; F029-C13) ─────────────────────

/**
 * Rendered with every verdict. A record that carries an authored
 * `not_understood` statement renders it verbatim. A record that
 * lacks one renders the absence as a visible gap — the record is
 * incomplete, and no machine-generated text is substituted for the
 * missing human statement (Phase E2 honesty rule).
 */
export function NotUnderstood({
  value,
  fg,
  muted,
}: {
  value?: string | null;
  fg: string;
  muted: string;
}) {
  const authored = typeof value === "string" && value.trim().length > 0;
  return (
    <div
      data-testid="not-understood"
      data-state={authored ? "recorded" : "not-yet-recorded"}
      style={{
        marginTop: 6,
        padding: "7px 10px",
        borderRadius: 6,
        border: authored ? "1px solid transparent" : "1px dashed #d97706",
        background: authored ? "transparent" : "#d9770614",
      }}
    >
      <span style={{ fontWeight: 700, color: authored ? muted : "#d97706" }}>
        What remains not understood:{" "}
      </span>
      {authored ? (
        <span style={{ color: fg }}>{value}</span>
      ) : (
        <span style={{ color: "#d97706" }}>
          not yet recorded — this record is incomplete. Writing this statement
          is lane-2 human work; no machine-generated text is substituted for it.
        </span>
      )}
    </div>
  );
}

// ── Contest display (FR-029-05; F029-C05; OD-3) ────────────────────────────

/**
 * A bundle parent's attribution contest renders on the parent,
 * wherever the parent renders. While a contest is active the
 * parent's stage is capped at `checked`, and the cap is shown.
 * A claim with no bundle record renders that honest absence: it
 * has not been decomposed, so there is no contest state to show.
 */
export function ContestDisplay({
  bundle,
  fg,
  muted,
}: {
  bundle?: BundleSerialization | null;
  fg: string;
  muted: string;
}) {
  if (!bundle) {
    return (
      <div data-testid="contest-display" data-state="no-bundle" style={{ marginTop: 6 }}>
        <span style={{ color: muted }}>Attribution contest: </span>
        <span style={{ color: fg }}>
          none recorded — this claim is not a bundle parent, so it carries no
          attribution sub-claim and no contest state.
        </span>
      </div>
    );
  }
  const attribution = bundle.sub_claims?.find((s) => s.kind === "attribution");
  const contestState = attribution?.contest_state ?? "unexamined";
  const contested = Boolean(bundle.attribution_contested);
  const caps = bundle.stage_computation?.caps_applied ?? [];
  const capped = caps.length > 0;
  const record = bundle.contest_record;
  return (
    <div data-testid="contest-display" data-state={contested ? "contested" : contestState} style={{ marginTop: 6 }}>
      <span style={{ color: muted }}>Attribution contest state: </span>
      <span style={{ color: fg, fontWeight: 600 }}>{contestState}</span>
      {contested && (
        <div
          style={{
            marginTop: 6,
            padding: "7px 10px",
            borderRadius: 6,
            border: "1px solid #dc2626",
            background: "#dc262614",
          }}
        >
          <div style={{ fontWeight: 700, color: "#dc2626" }}>
            Attribution contested — this claim&apos;s stage is capped at checked
            while the contest is active.
          </div>
          {capped && (
            <div style={{ color: fg, marginTop: 2 }}>
              Cap applied by the parent-stage computation: {caps.join(", ")}.
            </div>
          )}
          {record && (
            <div style={{ color: fg, marginTop: 2 }}>
              Contested by {record.contested_by ?? "—"}
              {record.contested_on ? ` on ${record.contested_on}` : ""}
              {record.evidence && record.evidence.length > 0
                ? ` · Contest evidence: ${record.evidence.join(", ")}`
                : ""}
            </div>
          )}
        </div>
      )}
      {!contested && capped && (
        <div style={{ color: fg, marginTop: 2 }}>
          Stage caps applied by the parent-stage computation: {caps.join(", ")}.
        </div>
      )}
    </div>
  );
}
