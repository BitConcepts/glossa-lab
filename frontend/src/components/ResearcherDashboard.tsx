/**
 * Researcher dashboard — the program's front door for a working
 * researcher, built to the approved wireframes: a home that states
 * the census and what the program does not claim, then six features
 * (program status, inscription explorer, hypothesis comparison,
 * evidence inspection, experiment reproduction, researcher
 * contribution), each reading the records themselves through the
 * dashboard read model and holding its stated refusals on the
 * surface: no number that is not the census of record, no reading
 * shown above its standing, no translation where none is held, no
 * lineage-less evidence, no automatic promotion anywhere, and no
 * candidate without a falsifier.
 */
import { useEffect, useMemo, useState, type CSSProperties, type ReactNode } from "react";
import {
  getDashboardClaim,
  getDashboardClaimExport,
  getDashboardClaims,
  getDashboardContributions,
  getDashboardCorpora,
  getDashboardHome,
  getDashboardHypotheses,
  getDashboardInscription,
  getDashboardInscriptions,
  getDashboardMatrix,
  getDashboardProgramStatus,
  getDashboardResult,
  getDashboardResults,
  getFoundationStatus,
  getStudyLoopStatus,
  rerunDashboardResult,
  submitDashboardContribution,
  type DashboardClaimDetail,
  type DashboardContributions,
  type DashboardCorpus,
  type DashboardHome,
  type DashboardHypotheses,
  type DashboardInscriptionDetail,
  type DashboardInscriptions,
  type DashboardProgramStatus,
  type DashboardResultDetail,
  type DashboardResults,
  type DashboardRerun,
} from "../api";
import {
  Card,
  CardTitle,
  Chip,
  PageHead,
  PrimaryButton,
  QuietButton,
  SmallButton,
  palette,
  type Palette,
} from "./ui081";

type Section =
  | "home" | "status" | "inscriptions" | "hypotheses"
  | "evidence" | "reproduction" | "contribute";

const SECTIONS: { id: Section; label: string; blurb: string }[] = [
  { id: "status", label: "Program status", blurb: "Is the enterprise sound, current, and unblocked — from the foundation check, the ledger gate record, and the loop's own status surface." },
  { id: "inscriptions", label: "Inscription explorer", blurb: "Work with the inscriptions themselves: observation, transcription, hypothesis, and claim kept in four labelled layers, never blended." },
  { id: "hypotheses", label: "Hypothesis comparison", blurb: "The language hypotheses and rival readings side by side, each at its recorded standing — and no translation where none is held." },
  { id: "evidence", label: "Evidence inspection", blurb: "Trace any claim to the evidence under it: lineage, derivation, and the matrix cell it rests on, with the audit trail exportable as the records themselves." },
  { id: "reproduction", label: "Experiment reproduction", blurb: "Re-run a published result against scratch stores only, and compare the quantities run against run — never pooled, never written into a standing." },
  { id: "contribute", label: "Researcher contribution", blurb: "Submit a candidate reading or claim into the adjudication pipeline. A falsifier is required; approval is a named human act; nothing is promoted automatically." },
];

function useFetch<T>(fn: () => Promise<T>, deps: unknown[]): {
  data: T | null; error: string | null; loading: boolean;
} {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fn()
      .then((r) => { if (!cancelled) { setData(r); setError(null); } })
      .catch((e) => {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "The record did not answer.");
        }
      })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
  return { data, error, loading };
}

function StateNote({ p, error, loading, empty }: {
  p: Palette; error: string | null; loading: boolean; empty?: boolean;
}) {
  if (loading) return <p style={{ color: p.muted, fontSize: 13 }}>Reading the record…</p>;
  if (error) return <p style={{ color: p.bad, fontSize: 13 }}>This instance states: {error}</p>;
  if (empty) return <p style={{ color: p.muted, fontSize: 13 }}>Nothing of record.</p>;
  return null;
}

const statBlock: CSSProperties = {
  flex: "1 1 150px", minWidth: 140, padding: "10px 12px",
};
const statNum: CSSProperties = { fontSize: 26, fontWeight: 750, lineHeight: 1.1 };
const statLabel: CSSProperties = { fontSize: 12, marginTop: 2 };
const statSource: CSSProperties = { fontSize: 11, overflowWrap: "anywhere" };
const inputStyle = (p: Palette): CSSProperties => ({
  background: p.inputBg, color: p.fg, border: `1px solid ${p.border}`,
  borderRadius: 8, padding: "7px 9px", fontSize: 13, width: "100%",
});
const labelStyle: CSSProperties = {
  fontSize: 12, fontWeight: 650, display: "block", marginBottom: 4,
};

// ── Home ─────────────────────────────────────────────────────────────

function HomeSection({ p, go }: { p: Palette; go: (s: Section) => void }) {
  const { data, error, loading } = useFetch<DashboardHome>(getDashboardHome, []);
  if (!data) return <StateNote p={p} error={error} loading={loading} />;
  const c = data.census;
  return (
    <div data-testid="dashboard-home">
      <Card p={p} style={{ marginBottom: 14 }}>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
          <div style={statBlock}>
            <div style={statNum} data-testid="census-claims">{c.claims.toLocaleString()}</div>
            <div style={{ ...statLabel, color: p.muted }}>claims in the ledger</div>
            <div style={{ ...statSource, color: p.faint }}>{c.sources.claims}</div>
          </div>
          <div style={statBlock}>
            <div style={statNum}>{c.studies}</div>
            <div style={{ ...statLabel, color: p.muted }}>studies</div>
            <div style={{ ...statSource, color: p.faint }}>{c.sources.studies}</div>
          </div>
          <div style={statBlock}>
            <div style={statNum}>{c.anchors_total}</div>
            <div style={{ ...statLabel, color: p.muted }}>recorded anchor signs</div>
            <div style={{ ...statSource, color: p.faint }}>{c.sources.anchors}</div>
          </div>
          <div style={statBlock}>
            <div style={statNum}>{data.falsifier_census.covered ?? "—"} / {data.falsifier_census.total ?? "—"}</div>
            <div style={{ ...statLabel, color: p.muted }}>claims carrying a falsifier</div>
            <div style={{ ...statSource, color: p.faint }}>
              {(data.falsifier_census.gap_claims ?? []).length} carry none — findable as a class in Evidence inspection
            </div>
          </div>
        </div>
        {data.freshness.stale && (
          <p style={{ color: p.bad, fontSize: 12, margin: "6px 12px 10px" }}>
            The generated map is stale against the ledger it was generated from; figures are stated with that flag, never silently.
          </p>
        )}
      </Card>

      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p} sub="The strongest readings in the record, with the identifiability outcome the protocol of record returned for each — stated, not buried.">
          Standing of the strongest readings
        </CardTitle>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
          {data.identifiability.map((i) => (
            <span key={i.sign} style={{ fontSize: 13 }}>
              <strong>{i.sign}</strong> — {i.reading}{" "}
              <Chip tone="warn">NOT IDENTIFIABLE</Chip>
            </span>
          ))}
        </div>
        <p style={{ color: p.muted, fontSize: 12, marginTop: 8 }}>
          Source: {data.identifiability_record}. NOT IDENTIFIABLE does not disprove a
          reading; it states that the record names no observation the reading fits
          and its rivals do not.
        </p>
      </Card>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: 12, marginBottom: 14 }}>
        {SECTIONS.map((s) => (
          <Card key={s.id} p={p}>
            <div style={{ fontWeight: 700, fontSize: 15, marginBottom: 4 }}>{s.label}</div>
            <p style={{ color: p.muted, fontSize: 13, lineHeight: 1.45, margin: "0 0 10px" }}>{s.blurb}</p>
            <PrimaryButton onClick={() => go(s.id)}>Open {s.label}</PrimaryButton>
          </Card>
        ))}
      </div>

      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p}>What this program does not claim</CardTitle>
        <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13, lineHeight: 1.55 }}>
          {data.does_not_claim.map((d) => <li key={d}>{d}</li>)}
        </ul>
      </Card>

      <Card p={p}>
        <CardTitle p={p} sub={data.recent_adjudications_basis}>Recent adjudications</CardTitle>
        {data.recent_adjudications.length === 0 && <StateNote p={p} error={null} loading={false} empty />}
        {data.recent_adjudications.map((a, idx) => (
          <div key={idx} style={{ fontSize: 13, padding: "5px 0", borderTop: idx ? `1px solid ${p.borderSoft}` : undefined }}>
            <strong>{a.date}</strong> · study {a.study} · <Chip tone={a.outcome === "NOT SUPPORTED" || a.outcome === "INCONSISTENT" ? "bad" : "neutral"}>{a.outcome}</Chip>{" "}
            <span style={{ color: p.muted }}>{a.relation} {a.claims.length} claim{a.claims.length === 1 ? "" : "s"}</span>
          </div>
        ))}
        {data.pending_validations?.count != null && (
          <p style={{ color: p.muted, fontSize: 12, marginTop: 8 }}>
            Pending validations: {data.pending_validations.count} — {data.pending_validations.reason}
          </p>
        )}
      </Card>
    </div>
  );
}

// ── Program status ───────────────────────────────────────────────────

function StatusSection({ p }: { p: Palette }) {
  const status = useFetch<DashboardProgramStatus>(getDashboardProgramStatus, []);
  const foundation = useFetch(getFoundationStatus, []);
  const loop = useFetch(getStudyLoopStatus, []);
  const d = status.data;
  return (
    <div data-testid="dashboard-status">
      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(280px, 1fr))", gap: 12, marginBottom: 14 }}>
        <Card p={p}>
          <CardTitle p={p}>Foundation check</CardTitle>
          <StateNote p={p} error={foundation.error} loading={foundation.loading} />
          {foundation.data && (
            <div style={{ fontSize: 13, lineHeight: 1.6 }}>
              <div>Verdict: <strong>{foundation.data.verdict ?? "not recorded"}</strong></div>
              <div>{foundation.data.n_ok} ok · {foundation.data.n_fail} fail · {foundation.data.n_warn} warn</div>
              <div style={{ color: p.muted }}>Last checked: {foundation.data.last_checked_at ?? "never recorded"}</div>
            </div>
          )}
        </Card>
        <Card p={p}>
          <CardTitle p={p}>Research loop</CardTitle>
          <StateNote p={p} error={loop.error} loading={loop.loading} />
          {loop.data && (
            <div style={{ fontSize: 13, lineHeight: 1.6 }}>
              <div>State: <strong>{loop.data.running ? "running" : "not running"}</strong> (the loop's own status surface)</div>
              {loop.data.iterations != null && <div>Iterations: {loop.data.iterations}</div>}
              {loop.data.last_run_at && <div style={{ color: p.muted }}>Last run: {loop.data.last_run_at}</div>}
            </div>
          )}
        </Card>
        <Card p={p}>
          <CardTitle p={p}>Ledger and map</CardTitle>
          <StateNote p={p} error={status.error} loading={status.loading} />
          {d && (
            <div style={{ fontSize: 13, lineHeight: 1.6 }}>
              <div>Ledger: {d.census.ledger_lines.toLocaleString()} lines · {d.census.claims.toLocaleString()} claims</div>
              <div>Ledger SHA-256 now: <span style={{ fontFamily: "monospace", fontSize: 11 }}>{d.freshness.ledger_sha256_now?.slice(0, 16)}…</span></div>
              <div>Map stale against ledger: <strong>{d.freshness.stale ? "yes" : "no"}</strong></div>
            </div>
          )}
        </Card>
      </div>

      {d && (
        <>
          <Card p={p} style={{ marginBottom: 14 }}>
            <CardTitle p={p}>Census by standing</CardTitle>
            <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
              {Object.entries(d.claims_by_status).map(([k, v]) => (
                <span key={k} style={{ fontSize: 13 }}>{k}: <strong>{v}</strong></span>
              ))}
            </div>
          </Card>
          <Card p={p} style={{ marginBottom: 14 }}>
            <CardTitle p={p} sub={`From the gap register of record (${d.blocked_items_source}). An item with no recorded owner says so; this surface never infers progress or an owner.`}>
              Blocked items, with their blockers
            </CardTitle>
            {d.blocked_items.map((b, i) => (
              <div key={i} style={{ fontSize: 13, padding: "5px 0", borderTop: i ? `1px solid ${p.borderSoft}` : undefined }}>
                <strong>{b.id ?? "unnamed"}</strong> — {b.text}{" "}
                <span style={{ color: p.muted }}>Owner: {b.owner ?? b.owner_note}.</span>
              </div>
            ))}
          </Card>
          <Card p={p}>
            <CardTitle p={p} sub={d.recent_landing_records_basis}>Recent landing records</CardTitle>
            {d.recent_landing_records.map((r) => (
              <div key={r.path} style={{ fontSize: 13, padding: "4px 0" }}>
                <span style={{ fontFamily: "monospace", fontSize: 12 }}>{r.path}</span>
                {r.date && <span style={{ color: p.muted }}> · {r.date}</span>}
              </div>
            ))}
          </Card>
        </>
      )}
    </div>
  );
}

// ── Inscription explorer ─────────────────────────────────────────────

function InscriptionsSection({ p }: { p: Palette }) {
  const corpora = useFetch(getDashboardCorpora, []);
  const [corpus, setCorpus] = useState("indus_canonical_export");
  const [site, setSite] = useState("");
  const [objectClass, setObjectClass] = useState("");
  const [sign, setSign] = useState("");
  const [lenMin, setLenMin] = useState("");
  const [lenMax, setLenMax] = useState("");
  const [offset, setOffset] = useState(0);
  const params = useMemo(() => {
    const q: Record<string, string | number> = { corpus, offset, limit: 50 };
    if (site) q.site = site;
    if (objectClass) q.object_class = objectClass;
    if (sign) q.sign = sign;
    if (lenMin) q.length_min = Number(lenMin);
    if (lenMax) q.length_max = Number(lenMax);
    return q;
  }, [corpus, site, objectClass, sign, lenMin, lenMax, offset]);
  const list = useFetch<DashboardInscriptions>(() => getDashboardInscriptions(params), [JSON.stringify(params)]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const detail = useFetch<DashboardInscriptionDetail | null>(
    () => (selectedId ? getDashboardInscription(selectedId) : Promise.resolve(null)),
    [selectedId],
  );
  const [signFocus, setSignFocus] = useState<number | null>(null);
  const corpusEntry: DashboardCorpus | undefined = corpora.data?.corpora.find((c) => c.key === corpus);

  return (
    <div data-testid="dashboard-inscriptions">
      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p} sub="Only identity-verified corpora can be explored. A corpus whose identity fails is listed unavailable with the reason, under no other label.">
          Corpus
        </CardTitle>
        <StateNote p={p} error={corpora.error} loading={corpora.loading} />
        {corpora.data?.corpora.map((c) => (
          <div key={c.key} style={{ fontSize: 13, padding: "5px 0", borderTop: `1px solid ${p.borderSoft}` }}>
            <label style={{ display: "flex", gap: 8, alignItems: "baseline", cursor: c.explorable ? "pointer" : "default" }}>
              <input
                type="radio" name="corpus" checked={corpus === c.key}
                disabled={!c.explorable}
                onChange={() => { setCorpus(c.key); setOffset(0); setSelectedId(null); }}
              />
              <span>
                <strong>{c.name}</strong>{" "}
                {c.identity_status === "verified"
                  ? <Chip tone="ok">identity verified</Chip>
                  : <Chip tone="bad">unavailable</Chip>}
                {!c.explorable && c.identity_status === "verified" && (
                  <span style={{ color: p.muted }}> — identity verified, but this corpus carries no inscription-level export in the record, so there is nothing here to explore.</span>
                )}
                {c.unavailable_reason && <span style={{ color: p.bad }}> — {c.unavailable_reason}</span>}
                <div style={{ color: p.muted, fontSize: 12 }}>
                  Source: {c.source} · Orientation basis: {c.orientation_basis}
                </div>
              </span>
            </label>
          </div>
        ))}
      </Card>

      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p}>Filters</CardTitle>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
          <div style={{ flex: "1 1 160px" }}>
            <label style={labelStyle}>Site</label>
            <select style={inputStyle(p)} value={site} onChange={(e) => { setSite(e.target.value); setOffset(0); }} data-testid="filter-site">
              <option value="">any site</option>
              {Object.entries(list.data?.facets.sites ?? {}).map(([s, n]) => (
                <option key={s} value={s}>{s} ({n})</option>
              ))}
            </select>
          </div>
          <div style={{ flex: "1 1 160px" }}>
            <label style={labelStyle}>Object class</label>
            <select style={inputStyle(p)} value={objectClass} onChange={(e) => { setObjectClass(e.target.value); setOffset(0); }}>
              <option value="">any class</option>
              {Object.entries(list.data?.facets.object_classes ?? {}).map(([s, n]) => (
                <option key={s} value={s}>{s} ({n})</option>
              ))}
            </select>
          </div>
          <div style={{ flex: "1 1 140px" }}>
            <label style={labelStyle}>Sign present (as recorded)</label>
            <input style={inputStyle(p)} value={sign} onChange={(e) => { setSign(e.target.value); setOffset(0); }} placeholder="e.g. 145" data-testid="filter-sign" />
          </div>
          <div style={{ flex: "0 1 110px" }}>
            <label style={labelStyle}>Min length</label>
            <input style={inputStyle(p)} value={lenMin} inputMode="numeric" onChange={(e) => { setLenMin(e.target.value); setOffset(0); }} />
          </div>
          <div style={{ flex: "0 1 110px" }}>
            <label style={labelStyle}>Max length</label>
            <input style={inputStyle(p)} value={lenMax} inputMode="numeric" onChange={(e) => { setLenMax(e.target.value); setOffset(0); }} />
          </div>
        </div>
      </Card>

      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p} sub="Catalogue identity and context — not readings. Select a result to open its four layers.">
          {list.data ? `${list.data.total.toLocaleString()} inscriptions` : "Inscriptions"}
        </CardTitle>
        <StateNote p={p} error={list.error} loading={list.loading} />
        {list.data?.unavailable_reason && (
          <p style={{ color: p.bad, fontSize: 13 }}>{corpusEntry?.name}: {list.data.unavailable_reason}</p>
        )}
        {list.data?.items.map((r) => (
          <button
            key={r.glossa_id}
            onClick={() => { setSelectedId(r.glossa_id); setSignFocus(null); }}
            style={{
              display: "block", width: "100%", textAlign: "left", background: "none",
              border: "none", borderTop: `1px solid ${p.borderSoft}`, padding: "7px 2px",
              cursor: "pointer", color: p.fg, fontSize: 13,
            }}
          >
            <strong>{r.glossa_id}</strong> · {r.artifact_type ?? "class not recorded"} ·{" "}
            {r.site_name ?? "site not recorded"} · {r.sign_instance_count ?? "—"} signs ·{" "}
            <span style={{ fontFamily: "monospace" }}>{r.text_code_diplomatic}</span>
          </button>
        ))}
        {list.data && list.data.total > 50 && (
          <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
            <QuietButton disabled={offset === 0} onClick={() => setOffset(Math.max(0, offset - 50))}>Previous 50</QuietButton>
            <QuietButton disabled={offset + 50 >= list.data.total} onClick={() => setOffset(offset + 50)}>Next 50</QuietButton>
            <span style={{ fontSize: 12, color: p.muted, alignSelf: "center" }}>
              {offset + 1}–{Math.min(offset + 50, list.data.total)} of {list.data.total.toLocaleString()}
            </span>
          </div>
        )}
      </Card>

      {selectedId && (
        <Card p={p}>
          <CardTitle p={p} sub="Four labelled layers, never blended. Selecting a sign highlights only that sign's statements in each layer.">
            {selectedId}
          </CardTitle>
          <StateNote p={p} error={detail.error} loading={detail.loading} />
          {detail.data && <InscriptionLayers p={p} detail={detail.data} signFocus={signFocus} setSignFocus={setSignFocus} />}
        </Card>
      )}
    </div>
  );
}

function LayerBlock({ p, title, children }: { p: Palette; title: string; children: ReactNode }) {
  return (
    <div style={{ borderTop: `1px solid ${p.borderSoft}`, padding: "10px 0" }}>
      <div style={{ fontSize: 12, fontWeight: 700, letterSpacing: "0.04em", textTransform: "uppercase", color: p.muted, marginBottom: 6 }}>{title}</div>
      {children}
    </div>
  );
}

function InscriptionLayers({ p, detail, signFocus, setSignFocus }: {
  p: Palette; detail: DashboardInscriptionDetail;
  signFocus: number | null; setSignFocus: (n: number | null) => void;
}) {
  const { observation, transcription, hypothesis, claim } = detail.layers;
  const focused = signFocus != null ? transcription.positions[signFocus] : null;
  const kv = (k: string, v: unknown) => (
    <div style={{ fontSize: 13, padding: "2px 0" }}>
      <span style={{ color: p.muted }}>{k}: </span>{v == null || v === "" ? <em>not recorded</em> : String(v)}
    </div>
  );
  return (
    <div>
      <LayerBlock p={p} title="Observation">
        {kv("Catalogue identity", observation.glossa_id)}
        {kv("Object class", observation.artifact_type)}
        {kv("Site", observation.site_name)}
        {kv("Current holding", observation.current_holding)}
        {kv("Material", observation.material)}
        {kv("Accession number", observation.accession_number)}
        {kv("Rights status", observation.rights_status)}
        {kv("Source system", observation.source_system)}
        <div style={{ fontSize: 12, color: p.muted, marginTop: 4 }}>{String(observation.note ?? "")}</div>
      </LayerBlock>
      <LayerBlock p={p} title="Transcription">
        {kv("Sign scheme", transcription.sign_id_scheme)}
        {kv("Diplomatic", transcription.diplomatic)}
        {kv("Normalized", transcription.normalized)}
        {kv("Open export transcription", transcription.open_export?.diplomatic)}
        <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginTop: 8 }}>
          {transcription.positions.map((pos) => (
            <button
              key={pos.position}
              onClick={() => setSignFocus(signFocus === pos.position ? null : pos.position)}
              style={{
                border: `1px solid ${signFocus === pos.position ? p.accent : p.border}`,
                background: signFocus === pos.position ? p.accentSoft : "transparent",
                color: p.fg, borderRadius: 8, padding: "5px 8px", fontSize: 12, cursor: "pointer",
                fontFamily: "monospace",
              }}
              data-testid={`sign-pos-${pos.position}`}
            >
              {pos.token}{pos.grapheme ? ` · ${pos.grapheme}` : ""}
            </button>
          ))}
        </div>
        {focused && (
          <div style={{ fontSize: 13, marginTop: 8 }}>
            Position {focused.position + 1}: sign {focused.token}
            {focused.grapheme ? `, grapheme identity ${focused.grapheme}` : ", no grapheme identity resolved on this record"}
            {focused.anchor_reading
              ? ` — the anchors register records the reading “${focused.anchor_reading.reading}” (${focused.anchor_reading.confidence}) for this sign.`
              : " — no reading is recorded for this sign."}
          </div>
        )}
        <div style={{ fontSize: 12, color: p.muted, marginTop: 4 }}>{transcription.note}</div>
      </LayerBlock>
      <LayerBlock p={p} title="Hypothesis">
        {hypothesis.readings_for_signs.length === 0
          ? <p style={{ fontSize: 13 }}>{hypothesis.absent_reason}</p>
          : hypothesis.readings_for_signs.map((r) => (
            <div key={r.sign} style={{ fontSize: 13, padding: "2px 0" }}>
              <strong>{r.sign}</strong> — “{r.reading}” <Chip tone="neutral">{r.confidence ?? "unrated"}</Chip>
            </div>
          ))}
        <div style={{ fontSize: 12, color: p.muted, marginTop: 4 }}>{hypothesis.note}</div>
      </LayerBlock>
      <LayerBlock p={p} title="Claim">
        {claim.claims.length === 0
          ? <p style={{ fontSize: 13 }}>{claim.absent_reason}</p>
          : claim.claims.map((c) => (
            <div key={c.id} style={{ fontSize: 13, padding: "2px 0" }}>
              <strong>{c.id}</strong> — {c.statement} <Chip tone="neutral">{c.status}</Chip>
            </div>
          ))}
      </LayerBlock>
    </div>
  );
}

// ── Hypothesis comparison ────────────────────────────────────────────

function HypothesesSection({ p }: { p: Palette }) {
  const { data, error, loading } = useFetch<DashboardHypotheses>(getDashboardHypotheses, []);
  const [filter, setFilter] = useState("");
  if (!data) return <StateNote p={p} error={error} loading={loading} />;
  const readings = data.readings.filter(
    (r) => !filter || r.sign.toLowerCase().includes(filter.toLowerCase())
      || (r.reading ?? "").toLowerCase().includes(filter.toLowerCase()),
  );
  return (
    <div data-testid="dashboard-hypotheses">
      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p}>Translations</CardTitle>
        <p style={{ fontSize: 13, margin: 0 }}>{data.translations.statement}</p>
      </Card>

      {data.nonlinguistic_position && (
        <Card p={p} style={{ marginBottom: 14 }}>
          <CardTitle p={p} sub={data.nonlinguistic_position.basis}>
            The nonlinguistic position
          </CardTitle>
          <p style={{ fontSize: 13 }}>{data.nonlinguistic_position.statement}</p>
          <div style={{ fontSize: 13 }}>
            Standing in the ledger: <Chip tone="bad">{data.nonlinguistic_position.status}</Chip>
          </div>
          {data.nonlinguistic_position.falsifier && (
            <p style={{ fontSize: 13 }}><span style={{ color: p.muted }}>Its falsifier, verbatim:</span> {data.nonlinguistic_position.falsifier}</p>
          )}
          {data.nonlinguistic_position.does_not_establish && (
            <p style={{ fontSize: 13 }}><span style={{ color: p.muted }}>What it does not establish:</span> {data.nonlinguistic_position.does_not_establish}</p>
          )}
        </Card>
      )}

      {data.models.map((m) => (
        <Card key={String(m.model_id)} p={p} style={{ marginBottom: 14 }}>
          <CardTitle p={p} sub={`Type: ${m.model_type ?? "not recorded"} · Status: ${m.status ?? "not recorded"}`}>
            {String(m.model_name ?? m.model_id)}
          </CardTitle>
          <div style={{ fontSize: 13, lineHeight: 1.55 }}>
            {(m.source_documents ?? (m.source_document ? [m.source_document] : [])).length > 0 && (
              <div>
                <span style={{ color: p.muted }}>Basis (sources of record): </span>
                {(m.source_documents ?? [m.source_document]).map((s: unknown, i: number) => (
                  <span key={i}>{typeof s === "string" ? s : (s as { title?: string; file?: string })?.title ?? (s as { file?: string })?.file ?? JSON.stringify(s)}{i < (m.source_documents ?? [m.source_document]).length - 1 ? "; " : ""}</span>
                ))}
              </div>
            )}
            {Array.isArray(m.core_claims) && m.core_claims.map((cc: Record<string, unknown>, i: number) => (
              <div key={i} style={{ borderTop: `1px solid ${p.borderSoft}`, padding: "6px 0" }}>
                <div>{String(cc.normalized_claim ?? "")}</div>
                <div style={{ color: p.muted }}>
                  Standing: {String(cc.claim_status ?? "not recorded")}
                  {cc.proposed_value ? ` · proposed value: ${String(cc.proposed_value)}` : ""}
                </div>
                {typeof cc.falsification_condition === "string" && (
                  <div><span style={{ color: p.muted }}>Falsification condition:</span> {cc.falsification_condition}</div>
                )}
              </div>
            ))}
            {m.current_score && (
              <div style={{ borderTop: `1px solid ${p.borderSoft}`, paddingTop: 6 }}>
                <span style={{ color: p.muted }}>Model scores, as recorded (effect sizes and advantages as the record states them — never a bare p-value): </span>
                {Object.entries(m.current_score as Record<string, unknown>).map(([k, v]) => (
                  <span key={k} style={{ marginRight: 10 }}>{k}: <strong>{String(v)}</strong></span>
                ))}
              </div>
            )}
            {Array.isArray(m.glossa_lab_evidence?.sa_results) && (
              <div style={{ borderTop: `1px solid ${p.borderSoft}`, paddingTop: 6 }}>
                {m.glossa_lab_evidence.sa_results.map((r: Record<string, unknown>, i: number) => (
                  <div key={i} style={{ padding: "2px 0" }}>
                    {String(r.experiment ?? "")} — {Object.entries(r).filter(([k]) => !["experiment", "notes", "status"].includes(k)).map(([k, v]) => `${k}: ${String(v)}`).join(" · ")}
                  </div>
                ))}
              </div>
            )}
          </div>
        </Card>
      ))}

      <Card p={p}>
        <CardTitle p={p} sub={data.readings_basis}>
          Rival readings, sign by sign
        </CardTitle>
        <div style={{ maxWidth: 260, marginBottom: 10 }}>
          <input style={inputStyle(p)} value={filter} onChange={(e) => setFilter(e.target.value)} placeholder="Filter by sign or reading" data-testid="reading-filter" />
        </div>
        <div style={{ maxHeight: 480, overflow: "auto" }}>
          {readings.map((r) => (
            <div key={r.sign} style={{ fontSize: 13, padding: "5px 0", borderTop: `1px solid ${p.borderSoft}` }}>
              <strong>{r.sign}</strong> — “{r.reading ?? "no reading recorded"}”{" "}
              <Chip tone="neutral">{r.confidence ?? "unrated"}</Chip>{" "}
              {r.identifiability
                ? <><Chip tone="warn">NOT IDENTIFIABLE</Chip> <span style={{ color: p.muted }}>{r.identifiability.outcome}</span></>
                : <span style={{ color: p.muted }}>{r.validation_status ?? ""}</span>}
            </div>
          ))}
        </div>
      </Card>
    </div>
  );
}

// ── Evidence inspection ──────────────────────────────────────────────

function EvidenceSection({ p }: { p: Palette }) {
  const matrix = useFetch(getDashboardMatrix, []);
  const [standing, setStanding] = useState("");
  const [study, setStudy] = useState("");
  const [sign, setSign] = useState("");
  const [falsifier, setFalsifier] = useState("");
  const [q, setQ] = useState("");
  const [offset, setOffset] = useState(0);
  const params = useMemo(() => {
    const out: Record<string, string | number> = { offset, limit: 50 };
    if (standing) out.standing = standing;
    if (study) out.study = study;
    if (sign) out.sign = sign;
    if (falsifier) out.falsifier = falsifier;
    if (q) out.q = q;
    return out;
  }, [standing, study, sign, falsifier, q, offset]);
  const claims = useFetch(() => getDashboardClaims(params), [JSON.stringify(params)]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const detail = useFetch<DashboardClaimDetail | null>(
    () => (selectedId ? getDashboardClaim(selectedId) : Promise.resolve(null)),
    [selectedId],
  );
  const [exportNote, setExportNote] = useState<string | null>(null);

  const doExport = async (claimId: string) => {
    try {
      const payload = await getDashboardClaimExport(claimId);
      const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `claim-audit-trail-${claimId}.json`;
      a.click();
      URL.revokeObjectURL(url);
      setExportNote("Audit trail exported — the records themselves, not a summary of them.");
    } catch (e) {
      setExportNote(e instanceof Error ? e.message : "The export did not answer.");
    }
  };

  const d = detail.data;
  return (
    <div data-testid="dashboard-evidence">
      {matrix.data && (
        <Card p={p} style={{ marginBottom: 14 }}>
          <CardTitle p={p} sub={matrix.data.drill_down}>The claim-by-evidence matrix</CardTitle>
          <div style={{ fontSize: 13 }}>
            {matrix.data.rows_total.toLocaleString()} claim rows · {matrix.data.rows_with_cells.toLocaleString()} with cells ·{" "}
            {matrix.data.columns_total} columns ({Object.entries(matrix.data.columns_by_class).map(([k, v]) => `${v} ${k}`).join(", ")}) ·{" "}
            {matrix.data.cells_total.toLocaleString()} cells
          </div>
        </Card>
      )}
      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p} sub={claims.data?.falsifier_gap_note}>
          Find a claim
        </CardTitle>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
          <div style={{ flex: "1 1 150px" }}>
            <label style={labelStyle}>Standing</label>
            <select style={inputStyle(p)} value={standing} onChange={(e) => { setStanding(e.target.value); setOffset(0); }} data-testid="claim-standing">
              <option value="">any standing</option>
              {["draft", "untested", "partially_supported", "strongly_supported", "partially_falsified", "contradicted", "unsupported", "superseded"].map((s) => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>
          <div style={{ flex: "1 1 130px" }}>
            <label style={labelStyle}>Study</label>
            <select style={inputStyle(p)} value={study} onChange={(e) => { setStudy(e.target.value); setOffset(0); }}>
              <option value="">any study</option>
              {(matrix.data?.study_columns ?? []).map((s) => <option key={s} value={s}>{s}</option>)}
            </select>
          </div>
          <div style={{ flex: "1 1 130px" }}>
            <label style={labelStyle}>Sign</label>
            <input style={inputStyle(p)} value={sign} onChange={(e) => { setSign(e.target.value); setOffset(0); }} placeholder="e.g. M044" />
          </div>
          <div style={{ flex: "1 1 150px" }}>
            <label style={labelStyle}>Falsifier</label>
            <select style={inputStyle(p)} value={falsifier} onChange={(e) => { setFalsifier(e.target.value); setOffset(0); }} data-testid="claim-falsifier">
              <option value="">present or absent</option>
              <option value="present">present</option>
              <option value="absent">absent — the gap class</option>
            </select>
          </div>
          <div style={{ flex: "1 1 200px" }}>
            <label style={labelStyle}>Search</label>
            <input style={inputStyle(p)} value={q} onChange={(e) => { setQ(e.target.value); setOffset(0); }} placeholder="statement or claim id" />
          </div>
        </div>
        <StateNote p={p} error={claims.error} loading={claims.loading} />
        {claims.data && (
          <div style={{ fontSize: 12, color: p.muted, marginTop: 8 }}>{claims.data.total.toLocaleString()} claims match</div>
        )}
        {claims.data?.items.map((c) => (
          <button
            key={c.id}
            onClick={() => setSelectedId(c.id)}
            style={{
              display: "block", width: "100%", textAlign: "left", background: "none",
              border: "none", borderTop: `1px solid ${p.borderSoft}`, padding: "7px 2px",
              cursor: "pointer", color: p.fg, fontSize: 13,
            }}
          >
            <strong>{c.id}</strong> — {c.statement.slice(0, 140)}{c.statement.length > 140 ? "…" : ""}{" "}
            <Chip tone="neutral">{c.status}</Chip>{" "}
            {c.falsifier_present
              ? <Chip tone="ok">falsifier recorded</Chip>
              : <Chip tone="bad">no falsifier — the gap</Chip>}
          </button>
        ))}
        {claims.data && claims.data.total > 50 && (
          <div style={{ display: "flex", gap: 8, marginTop: 10 }}>
            <QuietButton disabled={offset === 0} onClick={() => setOffset(Math.max(0, offset - 50))}>Previous 50</QuietButton>
            <QuietButton disabled={offset + 50 >= claims.data.total} onClick={() => setOffset(offset + 50)}>Next 50</QuietButton>
          </div>
        )}
      </Card>

      {selectedId && (
        <div data-testid="claim-detail">
        <Card p={p}>
          <CardTitle p={p}>{selectedId}</CardTitle>
          <StateNote p={p} error={detail.error} loading={detail.loading} />
          {d && (
            <div style={{ fontSize: 13, lineHeight: 1.55 }}>
              <p style={{ marginTop: 0 }}>{String(d.statement ?? "")}</p>
              <div><span style={{ color: p.muted }}>Falsifier, verbatim:</span> {d.falsifier ? String(d.falsifier) : <em>none recorded — this claim is in the falsifier-less class</em>}</div>
              <div><span style={{ color: p.muted }}>What this claim does not establish:</span> {d.does_not_establish ? String(d.does_not_establish) : <em>not recorded</em>}</div>
              <div>
                <span style={{ color: p.muted }}>Standing:</span> {String(d.status ?? "")} · <span style={{ color: p.muted }}>Stage:</span> {String(d.stage ?? "no stage recorded")}
                {d.supersession?.supersedes && <> · supersedes {String(d.supersession.supersedes)}</>}
                {(d.supersession?.superseded_by ?? []).length > 0 && <> · superseded by {(d.supersession.superseded_by as string[]).join(", ")}</>}
              </div>
              <LayerBlock p={p} title="Lineage — claim, evidence, derivation, source">
                <div><span style={{ color: p.muted }}>Source of record:</span>{" "}
                  {d.lineage?.source_document
                    ? <>{String(d.lineage.source_document.path ?? "")} · SHA-256 <span style={{ fontFamily: "monospace", fontSize: 11 }}>{String(d.lineage.source_document.sha256 ?? "").slice(0, 16)}…</span></>
                    : <em>none recorded</em>}
                </div>
                {(d.lineage?.evidence_refs ?? []).map((ref: string, i: number) => (
                  <div key={i}>Evidence reference: <span style={{ fontFamily: "monospace", fontSize: 12 }}>{ref}</span></div>
                ))}
                {(d.lineage?.sign_records ?? []).map((sr: Record<string, unknown>, i: number) => (
                  <div key={i}>Sign record: {JSON.stringify(sr)}</div>
                ))}
                <div style={{ color: p.muted, fontSize: 12 }}>{String(d.lineage?.note ?? "")}</div>
              </LayerBlock>
              <LayerBlock p={p} title="Matrix cells on this claim">
                {(d.matrix_cells ?? []).length === 0 && <em>No cells — this claim's row of the matrix is empty, and the surface says so.</em>}
                {(d.matrix_cells ?? []).map((cell: Record<string, unknown>, i: number) => (
                  <div key={i} style={{ padding: "3px 0" }}>
                    Column <strong>{String(cell.column ?? "")}</strong> ({String(cell.column_class ?? "")}) · relation {String(cell.relation ?? "")} · rule {String(cell.rule ?? "")}
                    {(cell.citations as string[] | undefined)?.length ? <div style={{ color: p.muted, fontSize: 12 }}>Citations: {(cell.citations as string[]).join(" · ")}</div> : null}
                  </div>
                ))}
              </LayerBlock>
              <div style={{ marginTop: 12, display: "flex", gap: 10, alignItems: "center" }}>
                <PrimaryButton onClick={() => void doExport(selectedId)}>Export the audit trail</PrimaryButton>
                {exportNote && <span style={{ fontSize: 12, color: p.muted }}>{exportNote}</span>}
              </div>
            </div>
          )}
        </Card>
        </div>
      )}
    </div>
  );
}

// ── Experiment reproduction ──────────────────────────────────────────

const QUANTITY_KEYS = ["assigned_count", "assigned_share", "consistent", "conflicts", "scope_signs", "contexts_touched", "strict_contexts"] as const;

function ReproductionSection({ p }: { p: Palette }) {
  const { data, error, loading } = useFetch<DashboardResults>(getDashboardResults, []);
  const [compare, setCompare] = useState<string[]>([]);
  const [detailId, setDetailId] = useState<string | null>(null);
  const detail = useFetch<DashboardResultDetail | null>(
    () => (detailId ? getDashboardResult(detailId) : Promise.resolve(null)),
    [detailId],
  );
  const [rerun, setRerun] = useState<DashboardRerun | null>(null);
  const [rerunError, setRerunError] = useState<string | null>(null);
  const [rerunning, setRerunning] = useState(false);

  const doRerun = async (runId: string) => {
    setRerunning(true);
    setRerunError(null);
    setRerun(null);
    try {
      setRerun(await rerunDashboardResult(runId));
    } catch (e) {
      setRerunError(e instanceof Error ? e.message : "The re-run did not answer.");
    } finally {
      setRerunning(false);
    }
  };

  if (!data) return <StateNote p={p} error={error} loading={loading} />;
  const toggleCompare = (record: string) =>
    setCompare((cur) => (cur.includes(record) ? cur.filter((x) => x !== record) : [...cur.slice(-1), record]));
  const compared = data.settling_runs.filter((r) => compare.includes(r.record));
  return (
    <div data-testid="dashboard-reproduction">
      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p} sub={data.semantics_note}>{data.label ?? "Published results"}</CardTitle>
        <p style={{ fontSize: 13, margin: 0 }}>
          A result whose execution record is incomplete is listed as not reproducible, with the
          missing pieces named. A re-run first verifies the corpus against its pin of record,
          runs against scratch stores only, and its outcome is compared per quantity — it is
          never written into a standing.
        </p>
      </Card>

      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p}>Settling results of record</CardTitle>
        {data.settling_runs.map((r) => (
          <div key={r.record} style={{ fontSize: 13, padding: "6px 0", borderTop: `1px solid ${p.borderSoft}` }}>
            <strong>{r.record}</strong> · candidate {r.candidate} · scenario {r.scenario} ·{" "}
            assigned {r.assigned_count} · consistent {r.consistent} · conflicts {r.conflicts}{" "}
            <SmallButton onClick={() => setDetailId(r.record)}>Execution of record</SmallButton>{" "}
            <SmallButton onClick={() => void doRerun(r.record)} disabled={rerunning}>Re-run (scratch only)</SmallButton>{" "}
            <label style={{ fontSize: 12, color: p.muted }}>
              <input type="checkbox" checked={compare.includes(r.record)} onChange={() => toggleCompare(r.record)} /> compare
            </label>
          </div>
        ))}
        {compared.length === 2 && (
          <div style={{ marginTop: 10 }}>
            <div style={{ fontWeight: 650, fontSize: 13, marginBottom: 4 }}>
              Run against run — {compared[0].record} vs {compared[1].record} (never pooled)
            </div>
            <table style={{ fontSize: 13, borderCollapse: "collapse" }}>
              <tbody>
                {QUANTITY_KEYS.map((k) => (
                  <tr key={k}>
                    <td style={{ padding: "3px 10px 3px 0", color: p.muted }}>{k}</td>
                    <td style={{ padding: "3px 10px" }}>{String((compared[0] as unknown as Record<string, unknown>)[k] ?? "—")}</td>
                    <td style={{ padding: "3px 10px" }}>{String((compared[1] as unknown as Record<string, unknown>)[k] ?? "—")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
        {rerunError && <p style={{ color: p.bad, fontSize: 13 }}>This instance states: {rerunError}</p>}
        {rerun && (
          <div style={{ marginTop: 10, fontSize: 13 }} data-testid="rerun-result">
            <div><strong>Re-run of {String(rerun.run_id)}</strong> · corpus identity: {String(rerun.corpus_identity)} · record written to scratch only: <span style={{ fontFamily: "monospace", fontSize: 11 }}>{String(rerun.scratch_record)}</span></div>
            <table style={{ borderCollapse: "collapse", marginTop: 6 }}>
              <tbody>
                {QUANTITY_KEYS.map((k) => (
                  <tr key={k}>
                    <td style={{ padding: "3px 10px 3px 0", color: p.muted }}>{k}</td>
                    <td style={{ padding: "3px 10px" }}>recorded: {String(rerun.quantities?.recorded?.[k] ?? "—")}</td>
                    <td style={{ padding: "3px 10px" }}>re-run: {String(rerun.quantities?.rerun?.[k] ?? "—")}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <div style={{ color: p.muted }}>{String(rerun.standing_effect)}</div>
            {rerun.comparison?.status === "comparison refused" && (
              <div style={{ color: p.bad }}>Comparison refused: {String(rerun.comparison.reason)}</div>
            )}
          </div>
        )}
      </Card>

      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p}>Run index — every run of record</CardTitle>
        <div style={{ maxHeight: 420, overflow: "auto" }}>
          {data.runs.map((r, i) => (
            <div key={`${r.run_id ?? r.record ?? i}`} style={{ fontSize: 13, padding: "5px 0", borderTop: `1px solid ${p.borderSoft}` }}>
              <strong>{r.run_id ?? r.record}</strong> · candidate {r.candidate ?? "—"} ·{" "}
              {r.reproducible
                ? <Chip tone="ok">execution record complete</Chip>
                : <><Chip tone="bad">not reproducible</Chip> <span style={{ color: p.muted }}>missing: {r.missing.join(", ")}</span></>}{" "}
              <SmallButton onClick={() => setDetailId(r.run_id ?? r.record ?? "")}>Execution of record</SmallButton>
            </div>
          ))}
        </div>
      </Card>

      {detailId && (
        <Card p={p}>
          <CardTitle p={p}>Execution of record — {detailId}</CardTitle>
          <StateNote p={p} error={detail.error} loading={detail.loading} />
          {detail.data && (
            <div style={{ fontSize: 13, lineHeight: 1.55 }}>
              <div><span style={{ color: p.muted }}>Candidate:</span> {String(detail.data.summary?.candidate ?? "—")} · <span style={{ color: p.muted }}>Semantics:</span> {String(detail.data.summary?.semantics ?? "—")}</div>
              {(detail.data.summary?.missing ?? []).length > 0 && (
                <div style={{ color: p.bad }}>Not reproducible — missing pieces of the execution record: {(detail.data.summary.missing as string[]).join(", ")}</div>
              )}
              <div style={{ color: p.muted, marginTop: 4 }}>Input pins of record:</div>
              <pre style={{ fontSize: 11, overflow: "auto", background: p.bg, padding: 10, borderRadius: 8 }}>
                {JSON.stringify(detail.data.summary?.input_pins ?? {}, null, 2)}
              </pre>
              {detail.data.record_file && (
                <>
                  <div style={{ color: p.muted }}>The run record itself:</div>
                  <pre style={{ fontSize: 11, overflow: "auto", maxHeight: 300, background: p.bg, padding: 10, borderRadius: 8 }}>
                    {JSON.stringify(detail.data.record_file, null, 2).slice(0, 6000)}
                  </pre>
                </>
              )}
            </div>
          )}
        </Card>
      )}
    </div>
  );
}

// ── Researcher contribution ──────────────────────────────────────────

function ContributeSection({ p }: { p: Palette }) {
  const list = useFetch<DashboardContributions>(getDashboardContributions, []);
  const [statement, setStatement] = useState("");
  const [falsifier, setFalsifier] = useState("");
  const [refs, setRefs] = useState("");
  const [doesNot, setDoesNot] = useState("");
  const [subject, setSubject] = useState("");
  const [submitter, setSubmitter] = useState("");
  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState<string | null>(null);
  const [refreshKey, setRefreshKey] = useState(0);
  const trail = useFetch<DashboardContributions>(getDashboardContributions, [refreshKey]);

  const submit = async () => {
    setSubmitError(null);
    setSubmitted(null);
    if (!falsifier.trim()) {
      setSubmitError("The form cannot submit without a falsifier: a candidate the record cannot prove wrong is not a candidate.");
      return;
    }
    try {
      const rec = await submitDashboardContribution({
        statement: statement.trim(),
        falsifier: falsifier.trim(),
        evidence_refs: refs.split(",").map((x) => x.trim()).filter(Boolean),
        does_not_establish: doesNot.trim() || undefined,
        subject_sign: subject.trim() || undefined,
        submitted_by: submitter.trim(),
      });
      setSubmitted(`Candidate ${rec.contribution_id} is in the staging queue at stage “staged”. Submission implies no approval, verification, or promotion.`);
      setRefreshKey((k) => k + 1);
    } catch (e) {
      setSubmitError(e instanceof Error ? e.message : "The submission did not answer.");
    }
  };

  return (
    <div data-testid="dashboard-contribute">
      {list.data && (
        <Card p={p} style={{ marginBottom: 14 }}>
          <CardTitle p={p}>Boundaries, stated on the surface</CardTitle>
          <ul style={{ margin: 0, paddingLeft: 18, fontSize: 13, lineHeight: 1.55 }}>
            <li>{list.data.boundaries.research_assistant}</li>
            <li>{list.data.boundaries.approval}</li>
            <li>{list.data.boundaries.promotion}</li>
          </ul>
        </Card>
      )}
      <Card p={p} style={{ marginBottom: 14 }}>
        <CardTitle p={p} sub="The candidate lands in the staging queue. Its falsifier and evidence references are carried on the candidate record itself, where the adjudication gates read them.">
          Submit a candidate
        </CardTitle>
        <div style={{ display: "grid", gap: 10 }}>
          <div>
            <label style={labelStyle}>Statement (the candidate reading or claim)</label>
            <textarea style={{ ...inputStyle(p), minHeight: 54 }} value={statement} onChange={(e) => setStatement(e.target.value)} data-testid="contrib-statement" />
          </div>
          <div>
            <label style={labelStyle}>Falsifier — required; the form cannot submit without it</label>
            <textarea style={{ ...inputStyle(p), minHeight: 44 }} value={falsifier} onChange={(e) => setFalsifier(e.target.value)} data-testid="contrib-falsifier" />
          </div>
          <div>
            <label style={labelStyle}>Evidence references, picked from the record (claim ids, anchor signs, or run ids, comma-separated)</label>
            <input style={inputStyle(p)} value={refs} onChange={(e) => setRefs(e.target.value)} placeholder="e.g. M044" data-testid="contrib-refs" />
          </div>
          <div style={{ display: "flex", gap: 10, flexWrap: "wrap" }}>
            <div style={{ flex: "1 1 220px" }}>
              <label style={labelStyle}>What this does not establish</label>
              <input style={inputStyle(p)} value={doesNot} onChange={(e) => setDoesNot(e.target.value)} />
            </div>
            <div style={{ flex: "1 1 160px" }}>
              <label style={labelStyle}>Subject sign (from the record)</label>
              <input style={inputStyle(p)} value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="e.g. M044" />
            </div>
            <div style={{ flex: "1 1 200px" }}>
              <label style={labelStyle}>Your name (the named submitter)</label>
              <input style={inputStyle(p)} value={submitter} onChange={(e) => setSubmitter(e.target.value)} data-testid="contrib-submitter" />
            </div>
          </div>
          <div>
            <PrimaryButton onClick={() => void submit()}>Submit to the staging queue</PrimaryButton>
          </div>
          {submitError && <p style={{ color: p.bad, fontSize: 13, margin: 0 }} data-testid="contrib-error">{submitError}</p>}
          {submitted && <p style={{ color: p.muted, fontSize: 13, margin: 0 }} data-testid="contrib-ok">{submitted}</p>}
        </div>
      </Card>

      <Card p={p}>
        <CardTitle p={p} sub="Every transition on a candidate is an act with a named actor. A refusal names the gate that refused.">
          Adjudication trail — candidates from this surface
        </CardTitle>
        <StateNote p={p} error={trail.error} loading={trail.loading} />
        {trail.data && trail.data.contributions.length === 0 && (
          <p style={{ fontSize: 13, color: p.muted }}>No candidate has been submitted through this surface yet.</p>
        )}
        {trail.data?.contributions.map((c) => (
          <div key={c.contribution_id} style={{ fontSize: 13, padding: "7px 0", borderTop: `1px solid ${p.borderSoft}` }}>
            <strong>{c.contribution_id}</strong> — {c.statement}{" "}
            <Chip tone="neutral">{c.review_status}</Chip>{" "}
            <span style={{ color: p.muted }}>stage: {c.stage ?? "none — submission sets no standing"}</span>
            <div style={{ color: p.muted }}>Falsifier: {c.falsifier}</div>
            <div style={{ color: p.muted }}>Submitted by {c.submitted_by} · {c.submitted_at}</div>
            {c.stage_history.map((h, i) => (
              <div key={i} style={{ fontSize: 12, color: p.muted }}>
                {String(h.timestamp ?? "")} — {String(h.to_stage ?? "")} by {String(h.actor ?? "")}: {String(h.reason ?? "")}
              </div>
            ))}
          </div>
        ))}
      </Card>
    </div>
  );
}

// ── Shell ────────────────────────────────────────────────────────────

export function ResearcherDashboard({ darkMode }: { darkMode: boolean }) {
  const p = palette(darkMode);
  const [section, setSection] = useState<Section>("home");
  return (
    <div data-testid="researcher-dashboard" style={{ maxWidth: 1180, margin: "0 auto", width: "100%" }}>
      <PageHead
        p={p}
        title="Researcher dashboard"
        lede="The program's front door: the census of record, the strongest readings at their recorded standing, and the six working surfaces — each reading the records themselves and stating its refusals on its face."
      />
      <div style={{ display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 16 }}>
        {[{ id: "home" as Section, label: "Home" }, ...SECTIONS].map((s) => (
          <button
            key={s.id}
            onClick={() => setSection(s.id)}
            data-testid={`section-${s.id}`}
            style={{
              border: `1px solid ${section === s.id ? p.accent : p.border}`,
              background: section === s.id ? p.accentSoft : "transparent",
              color: p.fg, borderRadius: 999, padding: "6px 12px", fontSize: 13, cursor: "pointer",
              fontWeight: section === s.id ? 700 : 500,
            }}
          >
            {s.label}
          </button>
        ))}
      </div>
      {section === "home" && <HomeSection p={p} go={setSection} />}
      {section === "status" && <StatusSection p={p} />}
      {section === "inscriptions" && <InscriptionsSection p={p} />}
      {section === "hypotheses" && <HypothesesSection p={p} />}
      {section === "evidence" && <EvidenceSection p={p} />}
      {section === "reproduction" && <ReproductionSection p={p} />}
      {section === "contribute" && <ContributeSection p={p} />}
    </div>
  );
}
