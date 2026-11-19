/**
 * Data (Spec 081 step 6, T018): the program's data surface —
 * inscriptions, corpora and anchor sets as peer tabs. The anchor-set
 * editor was promoted out of the corpora view, where it sat as an
 * afterthought at the bottom of the page; here it is a named peer
 * (and labelled user-defined sets only, per D1).
 *
 * The inscriptions index leads: the first thing a researcher does
 * with this surface is find one inscription and open its evidence
 * trail (the four layers, as the researcher dashboard's explorer
 * presents them). Before it was added, the surface offered no way
 * from here to any inscription at all.
 */
import { useEffect, useState, type CSSProperties } from "react";
import {
  getDashboardInscription,
  getDashboardInscriptions,
  type DashboardInscriptionDetail,
  type DashboardInscriptions,
} from "../api";
import { AnchorSetsView } from "./AnchorSetsView";
import { CorporaView } from "./CorporaView";
import { Card, PageHead, palette, TabsRow, type Palette } from "./ui081";

type DataTab = "inscriptions" | "corpora" | "anchors";

const TABS: { id: DataTab; label: string }[] = [
  { id: "inscriptions", label: "Inscriptions" },
  { id: "corpora", label: "Corpora" },
  { id: "anchors", label: "Anchor sets" },
];

function LayerLine({ p, k, v }: { p: Palette; k: string; v: unknown }) {
  return (
    <div style={{ fontSize: 12.5, padding: "1px 0" }}>
      <span style={{ color: p.muted }}>{k}: </span>
      {v == null || v === "" ? <em>not recorded</em> : String(v)}
    </div>
  );
}

function InscriptionDetail({ p, detail }: { p: Palette; detail: DashboardInscriptionDetail }) {
  const { observation, transcription, hypothesis, claim } = detail.layers;
  const head: CSSProperties = {
    fontSize: 12, fontWeight: 700, color: p.fg, margin: "10px 0 4px",
    textTransform: "uppercase", letterSpacing: 0.4,
  };
  return (
    <div>
      <div style={head}>Observation</div>
      <LayerLine p={p} k="Catalogue identity" v={observation.glossa_id} />
      <LayerLine p={p} k="Object class" v={observation.artifact_type} />
      <LayerLine p={p} k="Site" v={observation.site_name} />
      <LayerLine p={p} k="Current holding" v={observation.current_holding} />
      <LayerLine p={p} k="Material" v={observation.material} />
      <div style={head}>Transcription</div>
      <LayerLine p={p} k="Sign scheme" v={transcription.sign_id_scheme} />
      <LayerLine p={p} k="Diplomatic" v={transcription.diplomatic} />
      <LayerLine p={p} k="Normalized" v={transcription.normalized} />
      <div style={head}>Hypothesis</div>
      {hypothesis.readings_for_signs.length === 0
        ? <div style={{ fontSize: 12.5 }}>{hypothesis.absent_reason}</div>
        : hypothesis.readings_for_signs.map((r) => (
          <div key={r.sign} style={{ fontSize: 12.5, padding: "1px 0" }}>
            <strong>{r.sign}</strong> — “{r.reading}” ({r.confidence ?? "unrated"})
          </div>
        ))}
      <div style={head}>Claim — this inscription's evidence trail</div>
      {claim.claims.length === 0
        ? <div style={{ fontSize: 12.5 }}>{claim.absent_reason}</div>
        : claim.claims.map((c) => (
          <div key={c.id} style={{ fontSize: 12.5, padding: "1px 0" }}>
            <strong>{c.id}</strong> — {c.statement} ({c.status})
          </div>
        ))}
      <div style={{ fontSize: 12.5, color: p.muted, marginTop: 8 }}>
        The claim layer is the evidence trail: every statement the record makes
        about this inscription, at its recorded standing, with the evidence it
        rests on reachable from the Claims and Evidence &amp; sources surfaces.
      </div>
    </div>
  );
}

function InscriptionsTab({ darkMode }: { darkMode: boolean }) {
  const p = palette(darkMode);
  const [list, setList] = useState<DashboardInscriptions | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [detail, setDetail] = useState<DashboardInscriptionDetail | null>(null);
  const [detailError, setDetailError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    getDashboardInscriptions({ corpus: "indus_canonical_export", offset: 0, limit: 50 })
      .then((r) => { if (!cancelled) setList(r); })
      .catch((e) => {
        if (!cancelled) setError(e instanceof Error ? e.message : "The inscriptions index did not answer.");
      });
    return () => { cancelled = true; };
  }, []);

  useEffect(() => {
    if (!selectedId) { setDetail(null); return; }
    let cancelled = false;
    setDetail(null);
    setDetailError(null);
    getDashboardInscription(selectedId)
      .then((r) => { if (!cancelled) setDetail(r); })
      .catch((e) => {
        if (!cancelled) setDetailError(e instanceof Error ? e.message : "The inscription did not answer.");
      });
    return () => { cancelled = true; };
  }, [selectedId]);

  const th: CSSProperties = {
    textAlign: "left", fontSize: 11, fontWeight: 700, color: p.muted,
    textTransform: "uppercase", letterSpacing: 0.4, padding: "6px 8px",
  };
  const td: CSSProperties = {
    fontSize: 12.5, color: p.fg, padding: "6px 8px",
    borderTop: `1px solid ${p.borderSoft}`, verticalAlign: "top",
  };

  return (
    <Card p={p} style={{ padding: 16 }}>
      <div style={{ fontSize: 13.5, fontWeight: 600, color: p.fg, marginBottom: 4 }}>
        Inscriptions — the canonical export
      </div>
      <div style={{ fontSize: 12.5, color: p.muted, lineHeight: 1.55, marginBottom: 8 }}>
        Every inscription in the identity-verified canonical corpus. Select one
        to open its four layers: observation, transcription, hypothesis, and the
        claim layer that is its evidence trail.
      </div>
      {error && <div style={{ fontSize: 12.5, color: p.bad }}>{error}</div>}
      {list?.unavailable_reason && (
        <div style={{ fontSize: 12.5, color: p.bad }}>{list.unavailable_reason}</div>
      )}
      {!list && !error && <div style={{ fontSize: 12.5, color: p.muted }}>Loading…</div>}
      {list && (
        <table style={{ width: "100%", borderCollapse: "collapse" }}>
          <thead>
            <tr>
              <th style={th}>Inscription</th>
              <th style={th}>Site</th>
              <th style={th}>Object class</th>
              <th style={th}>Signs</th>
              <th style={th}>Transcription</th>
            </tr>
          </thead>
          <tbody>
            {list.items.map((r) => (
              <tr
                key={r.glossa_id}
                onClick={() => setSelectedId(r.glossa_id)}
                style={{ cursor: "pointer", background: selectedId === r.glossa_id ? p.accentSoft : "transparent" }}
              >
                <td style={td}><strong>{r.glossa_id}</strong></td>
                <td style={td}>{r.site_name ?? "site not recorded"}</td>
                <td style={td}>{r.artifact_type ?? "class not recorded"}</td>
                <td style={td}>{r.sign_instance_count ?? "—"}</td>
                <td style={{ ...td, fontFamily: "monospace" }}>{r.text_code_diplomatic}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {list && (
        <div style={{ fontSize: 12, color: p.muted, marginTop: 8 }}>
          {`Showing ${list.items.length} of ${list.total.toLocaleString()} inscriptions — the full index, with filters, is the inscription explorer on the researcher dashboard.`}
        </div>
      )}
      {selectedId && (
        <div style={{ marginTop: 12, borderTop: `1px solid ${p.border}`, paddingTop: 6 }}>
          <div style={{ fontSize: 13.5, fontWeight: 600, color: p.fg }}>{selectedId}</div>
          {detailError && <div style={{ fontSize: 12.5, color: p.bad }}>{detailError}</div>}
          {!detail && !detailError && <div style={{ fontSize: 12.5, color: p.muted }}>Loading…</div>}
          {detail && <InscriptionDetail p={p} detail={detail} />}
        </div>
      )}
    </Card>
  );
}

export function DataView({ darkMode }: { darkMode: boolean }) {
  const p = palette(darkMode);
  const [tab, setTab] = useState<DataTab>("inscriptions");

  return (
    <div style={{ maxWidth: 1180, margin: "0 auto", width: "100%" }}>
      <PageHead
        p={p}
        title="Data"
        lede="The texts and sets the program's work runs on. What is registered here is what the analysis and the loop can see — nothing else is quietly in scope."
      />
      <TabsRow p={p} tabs={TABS} active={tab} onSelect={setTab} />
      {tab === "inscriptions" && <InscriptionsTab darkMode={darkMode} />}
      {tab === "corpora" && <CorporaView darkMode={darkMode} />}
      {tab === "anchors" && <AnchorSetsView />}
    </div>
  );
}
