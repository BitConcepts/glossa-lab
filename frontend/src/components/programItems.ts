/**
 * programItems — program records that are NOT spec directories and so
 * never appear in the spec-study register (GET /api/v1/spec-studies):
 * the Step 0-G instrument validation line (G44-I / G44-S / G44-S2)
 * and the external repair audit's work packages (Spec 081 hardening
 * relay, 2026-10-29; Leg B reconciliation, "Non-spec program items").
 *
 * This is program data, kept with the program-record surface (Reports
 * & ledger) — never in the shell. Every row carries the record's own
 * verdict, at full prominence for negative verdicts, and names its
 * record. When a line is superseded, the row carries the FINAL state
 * (G44-I: the Amendment 3 rerun verdict of 2026-10-28, which closed
 * the line — not only the 2026-10-26 halt that preceded it).
 *
 * Records live in the program's goal record files; the citation is
 * shown as the row's record line (there is no served URL for them —
 * no link is fabricated).
 */

export interface ProgramItem {
  id: string;
  name: string;
  /** ISO date of the record (the final record, when a line has several). */
  date: string;
  /** The record's own verdict, verbatim in substance. */
  verdict: string;
  tone: "bad" | "warn" | "neutral" | "ok";
  /** Citation of the record this row rests on. */
  record: string;
  note?: string;
}

export const PROGRAM_ITEMS: ProgramItem[] = [
  {
    id: "g44-i",
    name: "G44-I — Step 0-G implantation instrument (Amendments 1–3)",
    date: "2026-10-28",
    verdict: "FAILED — KI-2 TRIGGERED · Step 0-G line CLOSED",
    tone: "bad",
    record: "Run records 2026-10-26 (design-feasibility halt) and 2026-10-28 (Amendment 3 rerun verdict)",
    note: "Leg 1B margin +0.0017 against a +0.05 bar. Method M4 remains gated — draft only; the 44 pending readings carry no weight.",
  },
  {
    id: "g44-s",
    name: "G44-S — Step 0-G successor instrument validation",
    date: "2026-10-26",
    verdict: "FAILED — legs 1 and 1B (planted recovery 0.405 vs bar 0.60; 2 of 44 signs recovered)",
    tone: "bad",
    record: "2026-10-26-g44s-validation-record.md",
  },
  {
    id: "g44-s2",
    name: "G44-S2 — Step 0-G second successor validation",
    date: "2026-10-26",
    verdict: "INCOMPLETE — GENERATION DEFECT (stopped at profile-ledger construction; §8 kill criterion K2 triggered; no instrument verdict)",
    tone: "warn",
    record: "2026-10-26-g44s2-validation-record.md",
  },
  {
    id: "repair-wp1",
    name: "Repair WP1 — Baseline + containment",
    date: "2026-10-26",
    verdict: "Completed",
    tone: "ok",
    record: "2026-10-26-repair-brief-completion-report.md",
  },
  {
    id: "repair-wp2",
    name: "Repair WP2 — Phonological checking",
    date: "2026-10-26",
    verdict: "Repair completed — certification BLOCKED (a linguist's review is outstanding)",
    tone: "warn",
    record: "2026-10-26-repair-brief-completion-report.md",
  },
  {
    id: "repair-wp3",
    name: "Repair WP3 — Site statistics",
    date: "2026-10-26",
    verdict: "Repair completed — corrected re-evaluation BLOCKED (Holdat CSV and GPU environment outstanding)",
    tone: "warn",
    record: "2026-10-26-repair-brief-completion-report.md",
  },
  {
    id: "repair-wp4",
    name: "Repair WP4 — Circular comparator",
    date: "2026-10-26",
    verdict: "Completed — eligible independent comparisons: 0 of 184 (the comparison set is circular)",
    tone: "neutral",
    record: "2026-10-26-repair-brief-completion-report.md",
  },
  {
    id: "repair-wp5",
    name: "Repair WP5 — Anchor audit",
    date: "2026-10-26",
    verdict: "Completed — 6 of 94 strict entries independently supported · 46 internal-only · 37 require revalidation · 3 expert-pending (M222, M362, M398) · 2 insufficient",
    tone: "neutral",
    record: "2026-10-26-repair-brief-completion-report.md",
  },
  {
    id: "repair-wp6",
    name: "Repair WP6 — Corpus + replay",
    date: "2026-10-26",
    verdict: "Completed",
    tone: "ok",
    record: "2026-10-26-repair-brief-completion-report.md",
  },
  {
    id: "repair-wp7",
    name: "Repair WP7 — Structural calibration",
    date: "2026-10-26",
    verdict: "Prepared (not executed)",
    tone: "neutral",
    record: "2026-10-26-repair-brief-completion-report.md",
  },
  {
    id: "repair-wp8",
    name: "Repair WP8 — Exposure + negative controls",
    date: "2026-10-26",
    verdict: "Prepared (not executed)",
    tone: "neutral",
    record: "2026-10-26-repair-brief-completion-report.md",
  },
  {
    id: "repair-wp9",
    name: "Repair WP9 — Bounded studies",
    date: "2026-10-26",
    verdict: "Prepared but gated — the sequence leg is blocked on the CISI Volume 3 transcription (restricted)",
    tone: "warn",
    record: "2026-10-26-repair-brief-completion-report.md",
  },
  {
    id: "repair-wp10",
    name: "Repair WP10 — Public claims",
    date: "2026-10-26",
    verdict: "Prepared — not published",
    tone: "neutral",
    record: "2026-10-26-repair-brief-completion-report.md",
  },
];
