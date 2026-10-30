/**
 * Digestion board (Spec 081 step 4, T016; wireframe 05; FR-004).
 *
 * The human work queue: which claims wait on which named human act,
 * oldest first (Q2 — columns by act owed). The derivation follows
 * the Spec 029 lifecycle: a claim at stage `checked` has no
 * explanation record yet; at `explained` no acceptance record; at
 * `accepted` no digestion record. Where a claim carries the bundle
 * stage computation, its capped stage governs (contest caps applied
 * there, per Spec 029) — the board never presents a stage the
 * computation has capped away. Every card names its missing act
 * (C081-8): a count alone never settles anything, so no row here is
 * just a number.
 *
 * Card clicks record the claim as the operator's intent
 * (sessionStorage `glossa_open_claim`) and open the Claims surface.
 * The interim claims surface does not consume the key yet; the
 * step-3 claims restructure (T015) wires claim-detail deep links.
 */
import { useEffect, useMemo, useState } from "react";
import { listIndusClaims, type IndusClaim } from "../api";
import {
  Card,
  MissingAct,
  PageHead,
  PrimaryButton,
  fmtDayTime,
  palette,
  verdictOf,
} from "./ui081";

type ColumnKey = "explanation" | "acceptance" | "digest";

const STAGE_TO_COLUMN: Record<string, ColumnKey> = {
  checked: "explanation",
  explained: "acceptance",
  accepted: "digest",
};

const COLUMNS: Array<{
  key: ColumnKey;
  title: string;
  missing: string;
}> = [
  {
    key: "explanation",
    title: "Needs explanation",
    missing:
      "an explanation record — what the claim means, and why its evidence is or is not enough.",
  },
  {
    key: "acceptance",
    title: "Needs acceptance",
    missing:
      "an acceptance record — a named person accepts the verdict and what it carries.",
  },
  {
    key: "digest",
    title: "Ready to digest",
    missing:
      "a digestion record — independent scholarly engagement with the claim, by name. Nothing here can be rushed by the tool.",
  },
];

/** The stage the board places a claim by: the bundle computation's
 *  capped stage when present, else the stamped stage object. */
export function effectiveStage(c: IndusClaim): string | null {
  return c.bundle?.stage_computation?.stage ?? c.stage?.stage ?? null;
}

/** The act a claim at this stage is missing (the board's column copy). */
export function missingActFor(stage: string | null): string | null {
  switch (stage) {
    case "checked":
      return "an explanation record — what the claim means, and why its evidence is or is not enough.";
    case "explained":
      return "an acceptance record — a named person accepts the verdict and what it carries.";
    case "accepted":
      return "a digestion record — independent scholarly engagement with the claim, by name. Nothing here can be rushed by the tool.";
    default:
      return null;
  }
}

function stageDate(c: IndusClaim): string | null {
  if (c.stage?.stage_as_of) return c.stage.stage_as_of;
  const at = c.stage?.latest_transition?.at;
  return typeof at === "string" ? at : null;
}

function waitingDays(c: IndusClaim): number | null {
  const d = stageDate(c);
  if (!d) return null;
  const t = Date.parse(d);
  if (Number.isNaN(t)) return null;
  return Math.max(0, Math.floor((Date.now() - t) / 86_400_000));
}

export function DigestionBoard({
  darkMode,
  onNavigate,
}: {
  darkMode: boolean;
  onNavigate: (route: "claims") => void;
}) {
  const p = palette(darkMode);
  const [claims, setClaims] = useState<IndusClaim[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    listIndusClaims({ limit: 500 })
      .then((r) => { if (!cancelled) setClaims(r.claims); })
      .catch((e) => {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "The claims register did not answer.");
        }
      });
    return () => { cancelled = true; };
  }, []);

  const columns = useMemo(() => {
    const by: Record<ColumnKey, IndusClaim[]> = {
      explanation: [],
      acceptance: [],
      digest: [],
    };
    if (claims) {
      for (const c of claims) {
        const col = STAGE_TO_COLUMN[effectiveStage(c) ?? ""];
        if (col) by[col].push(c);
      }
      for (const key of Object.keys(by) as ColumnKey[]) {
        by[key].sort((a, b) =>
          (stageDate(a) ?? "9999").localeCompare(stageDate(b) ?? "9999"),
        );
      }
    }
    return by;
  }, [claims]);

  const longestWaiting = useMemo(() => {
    const all = [...columns.explanation, ...columns.acceptance, ...columns.digest];
    all.sort((a, b) => (stageDate(a) ?? "9999").localeCompare(stageDate(b) ?? "9999"));
    return all[0] ?? null;
  }, [columns]);

  const openClaim = (c: IndusClaim) => {
    try {
      sessionStorage.setItem("glossa_open_claim", c.claim_id);
    } catch { /* intent is best-effort; navigation still happens */ }
    onNavigate("claims");
  };

  return (
    <div data-testid="digestion-board">
      <PageHead
        p={p}
        title="Digestion — the human queue"
        lede={
          <>
            Machine checks finish in minutes; settlement takes people. A claim moves
            created → checked → <b>explained</b> → <b>accepted</b> → <b>digested</b>{" "}
            only when a named person records the act. This board is that queue: every
            row says exactly what is missing. A count alone never settles anything,
            so no row is just a number.
          </>
        }
        primary={
          <PrimaryButton
            disabled={!longestWaiting}
            onClick={() => longestWaiting && openClaim(longestWaiting)}
          >
            Start with the longest-waiting claim
          </PrimaryButton>
        }
      />

      {error ? (
        <Card p={p} style={{ padding: 16 }}>
          <div style={{ fontSize: 13.5, fontWeight: 600, color: p.bad, marginBottom: 4 }}>
            The claims register did not answer on this instance
          </div>
          <div style={{ fontSize: 12.5, color: p.muted }}>
            {`This instance states: ${error}. The board shows no queue rather than an invented one; retry from the shell once the backend responds.`}
          </div>
        </Card>
      ) : !claims ? (
        <div style={{ fontSize: 13, color: p.muted }}>Loading the queue…</div>
      ) : (
        <>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))",
              gap: 14,
              alignItems: "start",
            }}
          >
            {COLUMNS.map((col) => (
              <div
                key={col.key}
                style={{
                  background: "transparent",
                  border: `1px solid ${p.border}`,
                  borderRadius: 12,
                  padding: 12,
                  display: "grid",
                  gap: 10,
                  minWidth: 0,
                }}
              >
                <h3
                  style={{
                    margin: 0,
                    fontSize: 13.5,
                    color: p.fg,
                    display: "flex",
                    alignItems: "center",
                    gap: 8,
                  }}
                >
                  {col.title}
                  <span
                    style={{
                      fontSize: 11.5,
                      fontWeight: 600,
                      color: p.accent,
                      background: p.accentSoft,
                      borderRadius: 999,
                      padding: "1px 8px",
                    }}
                  >
                    {columns[col.key].length}
                  </span>
                </h3>

                {columns[col.key].length === 0 && (
                  <div style={{ fontSize: 12.5, color: p.muted }}>
                    Nothing waits on this act.
                  </div>
                )}

                {columns[col.key].map((c) => {
                  const v = verdictOf(c.claim_status);
                  const days = waitingDays(c);
                  const when = stageDate(c);
                  const stageWord =
                    col.key === "explanation"
                      ? "Checked"
                      : col.key === "acceptance"
                        ? "Explained"
                        : "Accepted";
                  return (
                    <div
                      key={c.claim_id}
                      style={{
                        background: p.card,
                        border: `1px solid ${p.border}`,
                        borderRadius: 10,
                        padding: 12,
                        display: "grid",
                        gap: 6,
                        minWidth: 0,
                      }}
                    >
                      <button
                        type="button"
                        onClick={() => openClaim(c)}
                        style={{
                          background: "none",
                          border: "none",
                          padding: 0,
                          cursor: "pointer",
                          textAlign: "left",
                          fontFamily: "inherit",
                          fontSize: 13.5,
                          fontWeight: 600,
                          color: p.fg,
                          overflowWrap: "anywhere",
                        }}
                      >
                        {c.normalized_claim}
                      </button>
                      <div style={{ fontSize: 12, color: p.muted }}>
                        {`${stageWord}${when ? ` ${fmtDayTime(when)}` : ""}${days !== null ? ` · waiting ${days} day${days === 1 ? "" : "s"}` : ""} · verdict: ${v.label.toLowerCase()}`}
                      </div>
                      {col.key === "digest" ? (
                        <div
                          style={{
                            background: p.accentSoft,
                            color: p.accent,
                            borderRadius: 8,
                            padding: "8px 10px",
                            fontSize: 12.5,
                          }}
                        >
                          <b>Next:</b> {col.missing}
                        </div>
                      ) : (
                        <MissingAct>
                          <b>Missing:</b> {col.missing}
                        </MissingAct>
                      )}
                    </div>
                  );
                })}

                {col.key === "digest" && (
                  <p style={{ fontSize: 12, color: p.muted, margin: 0, padding: 2 }}>
                    Digested is the end of the line: the claim has been taken up by
                    people outside the program and answered. Most claims will sit
                    earlier for a long time. That is the honest state, and the board
                    shows it.
                  </p>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
