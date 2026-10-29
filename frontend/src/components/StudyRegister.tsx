/**
 * StudyRegister — the program record's two register lists, built for
 * the Reports & ledger screen (wireframe 12) against the hardening
 * register endpoint (PR #443, Leg B delta D0):
 *
 *  1. The spec-study register (GET /api/v1/spec-studies): every
 *     spec-kit study in the serving repo's specs/ tree, with the
 *     outcome headline its own record carries — verbatim, never
 *     paraphrased. A study with no outcome record is shown as having
 *     none (never as executed); duplicate spec numbers are flagged on
 *     both entries; the restricted entry (Spec 072) renders name-only,
 *     exactly as the endpoint serves it.
 *  2. Program items: records that are not spec directories (the
 *     Step 0-G validation line; the repair audit work packages) —
 *     the register screen's second list, per the hardening relay.
 *
 * Empty and error states are explicit (Leg B delta D1): a failed or
 * empty load is labelled an instance state, never a silent blank.
 */
import { useEffect, useMemo, useState } from "react";
import { getSpecStudies, type SpecStudy } from "../api";
import { Card, CardTitle, Chip, palette, type Palette, RowItem, RowMeta, RowTitle } from "./ui081";
import { PROGRAM_ITEMS } from "./programItems";

function humanizeSlug(slug: string): string {
  return slug.replace(/[-_]+/g, " ").replace(/^./, (c) => c.toUpperCase());
}

function StudyRow({ p, s, duplicate }: { p: Palette; s: SpecStudy; duplicate: boolean }) {
  return (
    <RowItem p={p}>
      <div style={{ flex: 1, minWidth: 0 }}>
        <div style={{ display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
          <RowTitle p={p}>Spec {s.spec_id} — {s.title ?? humanizeSlug(s.slug)}</RowTitle>
          {duplicate && <Chip tone="warn">Duplicate number — two register entries</Chip>}
          {s.restricted && <Chip tone="contest">Restricted</Chip>}
        </div>
        {s.restricted ? (
          <RowMeta p={p}>
            Name-only record. The register serves this entry from its directory
            name; its contents are never read.
          </RowMeta>
        ) : s.has_outcome && s.outcome_headline ? (
          <div style={{ color: p.fg, fontSize: 13.5, marginTop: 2 }}>{s.outcome_headline}</div>
        ) : s.has_outcome ? (
          <RowMeta p={p}>An outcome record exists; it carries no headline line.</RowMeta>
        ) : (
          <RowMeta p={p}>No outcome recorded — this study is not shown as executed.</RowMeta>
        )}
        <RowMeta p={p} style={{ overflowWrap: "anywhere" }}>{s.directory}</RowMeta>
      </div>
    </RowItem>
  );
}

export function StudyRegister({ darkMode }: { darkMode: boolean }) {
  const p = palette(darkMode);
  const [studies, setStudies] = useState<SpecStudy[] | null>(null);
  const [source, setSource] = useState<string>("");
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let live = true;
    getSpecStudies()
      .then((r) => {
        if (!live) return;
        setStudies(r.studies);
        setSource(r.source);
      })
      .catch((e: unknown) => {
        if (live) setError(e instanceof Error ? e.message : "load failed");
      });
    return () => { live = false; };
  }, []);

  const duplicates = useMemo(() => {
    const seen = new Map<string, number>();
    (studies ?? []).forEach((s) => seen.set(s.spec_id, (seen.get(s.spec_id) ?? 0) + 1));
    return new Set([...seen.entries()].filter(([, n]) => n > 1).map(([id]) => id));
  }, [studies]);

  const withOutcome = (studies ?? []).filter((s) => s.has_outcome).length;

  return (
    <div style={{ display: "grid", gap: 16, minWidth: 0 }}>
      <Card p={p} style={{ minWidth: 0 }}>
        <CardTitle p={p} sub="Every spec-kit study in the program record, with the outcome its own record carries. Headlines are the records' own words — never paraphrased.">
          Study register
        </CardTitle>
        {error ? (
          <RowMeta p={p} style={{ color: p.bad }}>
            The study register could not be loaded from this instance ({error}).
            The record itself lives in the serving repo's specs/ tree — treat
            this as an instance state, not an empty program.
          </RowMeta>
        ) : studies === null ? (
          <RowMeta p={p}>Loading the register…</RowMeta>
        ) : studies.length === 0 ? (
          <RowMeta p={p}>
            This instance returned no studies. The register is read from the
            serving repo's specs/ tree; an empty answer here is an instance
            state, not the program's record.
          </RowMeta>
        ) : (
          <>
            <RowMeta p={p}>
              {studies.length} register entries · {withOutcome} with an outcome
              record{source ? ` · Source: ${source}` : ""}
            </RowMeta>
            <div>
              {studies.map((s) => (
                <StudyRow key={`${s.spec_id}-${s.slug}`} p={p} s={s} duplicate={duplicates.has(s.spec_id)} />
              ))}
            </div>
          </>
        )}
      </Card>

      <Card p={p} style={{ minWidth: 0 }}>
        <CardTitle p={p} sub="Instruments and audits that are not spec directories, so the register above cannot carry them: the Step 0-G validation line and the external repair audit. Each row is its record's own verdict.">
          Program items — records outside the spec register
        </CardTitle>
        <div>
          {PROGRAM_ITEMS.map((item) => (
            <RowItem key={item.id} p={p}>
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{ display: "flex", alignItems: "baseline", gap: 8, flexWrap: "wrap" }}>
                  <RowTitle p={p}>{item.name}</RowTitle>
                  <Chip tone={item.tone}>{item.date}</Chip>
                </div>
                <div style={{ color: p.fg, fontSize: 13.5, marginTop: 2 }}>{item.verdict}</div>
                {item.note && <RowMeta p={p}>{item.note}</RowMeta>}
                <RowMeta p={p}>Record: {item.record}</RowMeta>
              </div>
            </RowItem>
          ))}
        </div>
      </Card>
    </div>
  );
}
