/**
 * Pipelines View — gallery of registered pipelines (live from backend catalog).
 */

import { useEffect, useState } from "react";
import {
  deletePipeline,
  duplicatePipeline,
  getPipelineCatalog,
  importPipeline,
  type CatalogPipeline,
} from "../api";

interface Pipeline {
  id: string;
  label: string;
  group: string;
  description: string;
  inputs: string;
  outputs: string;
  defaultParams: string;
  needsLM: boolean;
  default_params?: Record<string, unknown>;
  registered?: boolean;
  module?: string;
  custom?: boolean;
}

const PIPELINES_FALLBACK: Pipeline[] = [
  // Pure statistical — no language model
  {
    id: "block_entropy",
    label: "Block Entropy",
    group: "Statistical (no LM)",
    description:
      "Computes H_n (normalized) for n = 1..max_n. Sub-linear growth is the " +
      "hallmark of natural language (Rao 2009). Used to confirm Indus H1 = 0.739.",
    inputs: "text_id, max_n (default 6)",
    outputs: "block_entropies[], normalized values, linguistic classification",
    defaultParams: '{"text_id": "", "max_n": 6}',
    needsLM: false,
  },
  {
    id: "char_freq",
    label: "Character Frequency",
    group: "Statistical (no LM)",
    description:
      "Sign frequency distribution with Zipf exponent fit. Yadav (2010) found " +
      "Indus follows Zipf-Mandelbrot with α≈1.00; we measured 1.555 from Fuls catalog.",
    inputs: "text_id",
    outputs: "frequencies, rank_frequency[], zipf_exponent",
    defaultParams: '{"text_id": ""}',
    needsLM: false,
  },
  {
    id: "positional",
    label: "Positional Analysis",
    group: "Statistical (no LM)",
    description:
      "For each sign: initial_rate, medial_rate, terminal_rate. Identifies dominant " +
      "positional preferences. Validated against known TMK/INITIAL signs in Fuls catalog.",
    inputs: "text_id",
    outputs: "profiles[] per sign with dominant_position",
    defaultParams: '{"text_id": ""}',
    needsLM: false,
  },
  {
    id: "nwsp",
    label: "NWSP — Fuls Method",
    group: "Statistical (no LM)",
    description:
      "Exact implementation of Fuls (2013) Normalized Weighted Sign Position. " +
      "NWP(p,L) = (p-1)/(L-1)*9+1, weight=L. Classifies signs as ITM/TMK/INITIAL/NUM/CON/MED. " +
      "Maps to Fuls' ICIT function codes.",
    inputs: "text_id, min_occurrences (default 4)",
    outputs: "signs[] with histogram, classification, ICIT code mapping",
    defaultParams: '{"text_id": "", "min_occurrences": 4}',
    needsLM: false,
  },
  {
    id: "sign_polyvalence",
    label: "Sign Polyvalence",
    group: "Statistical (no LM)",
    description:
      "Detects signs with bimodal positional histograms — the hallmark of polyvalent " +
      "signs serving dual functions. Reproduces Fuls' sign 550 analysis. " +
      "74% of Indus signs show bimodal patterns (logo-syllabic expected).",
    inputs: "text_id, min_freq (default 5)",
    outputs: "candidates[] sorted by bimodality_score",
    defaultParams: '{"text_id": "", "min_freq": 5}',
    needsLM: false,
  },
  {
    id: "sign_cluster",
    label: "Sign Clustering",
    group: "Statistical (no LM)",
    description:
      "Distributional clustering: groups signs by similar co-occurrence contexts. " +
      "Signs appearing before/after the same other signs cluster together.",
    inputs: "text_id, min_freq, top_n",
    outputs: "clusters[] with member signs",
    defaultParams: '{"text_id": "", "min_freq": 3, "top_n": 20}',
    needsLM: false,
  },
  {
    id: "cooccurrence",
    label: "Co-occurrence Network",
    group: "Statistical (no LM)",
    description:
      "Builds a sign co-occurrence graph and detects communities using " +
      "the Louvain algorithm. Community structure reveals semantic groupings.",
    inputs: "text_id, window (default 2), min_freq, min_edge_weight",
    outputs: "node_count, edge_count, community_count, communities[]",
    defaultParams: '{"text_id": "", "window": 2, "min_freq": 3, "min_edge_weight": 2}',
    needsLM: false,
  },
  {
    id: "paradigm",
    label: "Paradigm Detection",
    group: "Statistical (no LM)",
    description:
      "Finds paradigmatic alternations: same stem, different suffix. High paradigm " +
      "count indicates rich morphological system. Indus: 102 paradigms vs Ugaritic: 2.",
    inputs: "text_id, min_stem_freq, min_variants",
    outputs: "paradigm_count, paradigms[]",
    defaultParams: '{"text_id": "", "min_stem_freq": 2, "min_variants": 2}',
    needsLM: false,
  },
  {
    id: "structural_fingerprint",
    label: "Structural Fingerprint",
    group: "Statistical (no LM)",
    description:
      "10-dimensional fingerprint: H1, H2/H1, Zipf-α, V/N, hapax%, mean positional entropy, " +
      "polyvalence%, inscription length, boundary-bias variance, paradigmatic rate. " +
      "GPU-accelerated comparison against database of 9 known writing systems.",
    inputs: "text_id, compare_to_db (default true)",
    outputs: "vector[10], dimensions{}, nearest_scripts[], notes[]",
    defaultParams: '{"text_id": "", "compare_to_db": true}',
    needsLM: false,
  },
  {
    id: "sign_function_estimator",
    label: "Sign Function Estimator",
    group: "Statistical (no LM)",
    description:
      "Probabilistic classifier: P(numeral), P(determinative), P(logogram), P(phonetic), " +
      "P(boundary_marker) per sign. Uses 9 distributional features. Calibration note: " +
      "undercalibrated for short-inscription corpora.",
    inputs: "text_id, min_freq (default 3)",
    outputs: "signs[] with probabilities, system_summary, interpretation",
    defaultParams: '{"text_id": "", "min_freq": 3}',
    needsLM: false,
  },
  {
    id: "numerals",
    label: "Numeral Detection",
    group: "Statistical (no LM)",
    description:
      "Identifies likely numeral signs by positional context and frequency patterns. " +
      "Numerals appear before commodity signs at consistent positions.",
    inputs: "text_id",
    outputs: "numeral_candidates[], numeral_patterns[]",
    defaultParams: '{"text_id": ""}',
    needsLM: false,
  },
  {
    id: "word_structure_hypothesis",
    label: "Word-Structure Typology",
    group: "Statistical (no LM)",
    description:
      "Tests inscription length distribution against 6 language family profiles. " +
      "No phoneme assumptions. Result: Proto-Dravidian ranks first for Indus " +
      "(KL=0.444 vs Sumerian 0.742). Validated on Ugaritic, Linear B, Sumerian.",
    inputs: "text_id",
    outputs: "ranked_hypotheses[], winner, margin",
    defaultParams: '{"text_id": ""}',
    needsLM: false,
  },
  {
    id: "distributional_decipherment",
    label: "Distributional Decipherment",
    group: "Statistical (no LM)",
    description:
      "Jensen-Shannon divergence clustering and Ventris grid method without language " +
      "assumptions. Groups signs by vowel class (similar left context) and consonant " +
      "class (similar right context). GPU-backed N×N cosine similarity matrix.",
    inputs: "text_id, target_language",
    outputs: "vowel_clusters[], consonant_clusters[], sign_classification{}",
    defaultParams: '{"text_id": "", "target_language": "generic"}',
    needsLM: false,
  },
  {
    id: "logosyllabic",
    label: "Logosyllabic Analysis (Ventris)",
    group: "Statistical (no LM)",
    description:
      "Full Ventris-style analysis: sign classification (logogram/syllabogram/" +
      "determinative) + affinity clustering (GPU cosine, complete-linkage) + " +
      "candidate CV readings + vocabulary matching.",
    inputs: "text_id, target_language (sumerian|linear_b|generic)",
    outputs: "sign_classification{}, affinity{}, proposed_readings{}, candidate_words[]",
    defaultParams: '{"text_id": "", "target_language": "generic"}',
    needsLM: false,
  },
  // Language model required
  {
    id: "kandles",
    label: "Kandles Fingerprint",
    group: "Language Model Required",
    description:
      "Merkur patent (US 2024/0248922) phonological colour fingerprint. Maps signs " +
      "to 8 colour groups by initial sound. Compares grid distributions via cosine similarity. " +
      "Language-specific bias profiles for Luwian, Hurrian, Semitic, Dravidian.",
    inputs: "text_id, mode (color_code|grid|compare), profile",
    outputs: "color_distribution{}, similarity score",
    defaultParams: '{"text_id": "", "mode": "grid"}',
    needsLM: true,
  },
  {
    id: "decipher",
    label: "Decipher (SA + Structural Constraints)",
    group: "Language Model Required",
    description:
      "Simulated-annealing substitution cipher solver with Semitic structural constraints and cognate anchors. " +
      "Constraints: use_word_bigrams, ocp_weight, root_prior_weight (root co-occurrence prior), positional_weight. " +
      "anchors: dict of locked cipher\u2192target sign correspondences (e.g. pan-Semitic cognates). " +
      "Validated: Tier 1b 100%, Tier 2B 66.7%, Tier 1a 6.7% mean (best 20% at 25 restarts). " +
      "See also: beam_decipher_benchmark for systematic search.",
    inputs: "text_id, target_text_id, max_iterations, restarts, use_word_bigrams, ocp_weight, root_prior_weight, positional_weight, anchors",
    outputs: "proposed_mapping{}, kandles_confidence, score",
    defaultParams: '{"text_id": "", "target_text_id": "", "max_iterations": 12000, "restarts": 8, "use_word_bigrams": false, "ocp_weight": 0.0, "positional_weight": 0.005}',
    needsLM: true,
  },
  {
    id: "hypothesis",
    label: "Hypothesis Engine",
    group: "Language Model Required",
    description:
      "Iterative hypothesize-test-score-learn loop over multiple language family " +
      "hypotheses. Tests Dravidian vs Sanskrit vs Luwian vs Semitic. Includes " +
      "Kandles bias profiles per language family.",
    inputs: "text_id, max_iterations",
    outputs: "results[] with scores per hypothesis, suggested_next[]",
    defaultParams: '{"text_id": "", "max_iterations": 5000}',
    needsLM: true,
  },
];

const GROUP_COLORS: Record<string, string> = {
  "Statistical (no LM)": "#16a34a",
  "Language Model Required": "#dc2626",
};

export function PipelinesView() {
  const [filter, setFilter] = useState<string>("all");
  const [selected, setSelected] = useState<string | null>(null);
  const [pipelines, setPipelines] = useState<Pipeline[]>(PIPELINES_FALLBACK);
  const [importPath, setImportPath] = useState("");
  const [importing, setImporting] = useState(false);
  const [importMsg, setImportMsg] = useState<{ ok: boolean; text: string } | null>(null);
  const [showImport, setShowImport] = useState(false);

  const handleDeleted = (id: string) => setPipelines((p) => p.filter((x) => x.id !== id));

  const handleImport = async () => {
    if (!importPath.trim()) return;
    setImporting(true);
    setImportMsg(null);
    try {
      const res = await importPipeline(importPath.trim()) as { imported?: boolean; file?: string };
      setImportMsg({ ok: true, text: `Imported: ${res.file ?? importPath}` });
      setImportPath("");
      load();
    } catch (e: unknown) {
      setImportMsg({ ok: false, text: e instanceof Error ? e.message : String(e) });
    } finally {
      setImporting(false);
    }
  };

  const load = () => {
    getPipelineCatalog()
      .then((entries: CatalogPipeline[]) => setPipelines(entries.map((e) => ({
        ...e,
        needsLM: e.needs_lm,
        defaultParams: JSON.stringify(e.default_params, null, 2),
        custom: !e.registered,
      }))))
      .catch(() => {});
  };

  useEffect(() => { load(); }, []);

  const groups = ["all", ...Array.from(new Set(pipelines.map((p) => p.group)))];
  const visible = filter === "all" ? pipelines : pipelines.filter((p) => p.group === filter);

  return (
    <div>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: "0.25rem" }}>
        <h2 style={{ marginTop: 0 }}>Pipelines</h2>
        <button
          onClick={() => { setShowImport((x) => !x); setImportMsg(null); }}
          style={{ padding: "5px 12px", border: "1px solid #d1d5db", borderRadius: 5, cursor: "pointer", fontSize: 12, background: showImport ? "#f3f4f6" : "#fff", color: "#374151" }}
        >
          {showImport ? "× Cancel" : "+ Import"}
        </button>
      </div>

      {showImport && (
        <div style={{
          background: "#f8fafc", border: "1px solid #e5e7eb",
          borderRadius: 8, padding: "12px 16px", marginBottom: "1rem",
        }}>
          <p style={{ margin: "0 0 8px", fontSize: 13, color: "#374151" }}>
            Enter the absolute path of a Python file that defines a class inheriting
            from <code>PipelineBase</code>. It will be copied into the pipelines directory.
          </p>
          <div style={{ display: "flex", gap: 8 }}>
            <input
              value={importPath}
              onChange={(e) => setImportPath(e.target.value)}
              onKeyDown={(e) => { if (e.key === "Enter") void handleImport(); }}
              placeholder="C:\path\to\my_pipeline.py"
              style={{
                flex: 1, padding: "7px 10px", border: "1px solid #d1d5db",
                borderRadius: 5, fontSize: 12, outline: "none", fontFamily: "monospace",
              }}
            />
            <button
              onClick={() => void handleImport()}
              disabled={importing || !importPath.trim()}
              style={{ padding: "7px 16px", border: "none", borderRadius: 5, cursor: "pointer", fontSize: 12, fontWeight: 600, background: "#1e3a5f", color: "#fff" }}
            >
              {importing ? "Importing…" : "Import"}
            </button>
          </div>
          {importMsg && (
            <div style={{
              marginTop: 8, fontSize: 12, padding: "6px 10px", borderRadius: 5,
              background: importMsg.ok ? "#f0fdf4" : "#fef2f2",
              color: importMsg.ok ? "#16a34a" : "#b91c1c",
              border: `1px solid ${importMsg.ok ? "#86efac" : "#fca5a5"}`,
            }}>
              {importMsg.text}
            </div>
          )}
        </div>
      )}

      <p style={{ fontSize: 13, color: "#6b7280", marginTop: 0, marginBottom: "1.25rem" }}>
        {pipelines.length} registered analysis pipelines. Statistical pipelines require no language model —
        all results are vocabulary-free and circularity-free. Select a pipeline to launch
        a job from the Jobs tab.
      </p>

      {/* Group filter */}
      <nav style={{ display: "flex", gap: 6, marginBottom: "1.5rem", flexWrap: "wrap" }}>
        {groups.map((g) => {
          const color = GROUP_COLORS[g] ?? "#1e3a5f";
          return (
            <button key={g} onClick={() => setFilter(g)} style={{
              padding: "4px 14px", border: "1px solid", borderRadius: 20, cursor: "pointer",
              fontSize: 12, fontWeight: filter === g ? 600 : 400,
              background: filter === g ? color : "#fff",
              borderColor: filter === g ? color : "#d1d5db",
              color: filter === g ? "#fff" : "#374151",
            }}>
          {g === "all" ? `All (${pipelines.length})` : `${g} (${pipelines.filter(p => p.group === g).length})`}
            </button>
          );
        })}
      </nav>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))", gap: "0.75rem" }}>
        {visible.map((p) => (
          <PipelineCard
            key={p.id}
            pipeline={p}
            expanded={selected === p.id}
            onToggle={() => setSelected(selected === p.id ? null : p.id)}
            onDeleted={handleDeleted}
            onDuplicated={load}
          />
        ))}
      </div>

      {/* Legend */}
      <div style={{ marginTop: "1.5rem", padding: "12px 16px", background: "#f9fafb", borderRadius: 8, fontSize: 12, color: "#6b7280" }}>
        <strong style={{ color: "#374151" }}>Scientific note:</strong> All 14 statistical pipelines
        are safe to run on any corpus without language assumptions. The 3 pipelines marked
        "Language Model Required" use bigram statistics from a target language — these must use
        separate training/test corpora to avoid circularity (Fuls 2013; Snyder 2010 protocol).
      </div>
    </div>
  );
}

function PipelineCard({
  pipeline: p,
  expanded,
  onToggle,
  onDeleted,
  onDuplicated,
}: {
  pipeline: Pipeline;
  expanded: boolean;
  onToggle: () => void;
  onDeleted: (id: string) => void;
  onDuplicated: () => void;
}) {
  const groupColor = GROUP_COLORS[p.group] ?? "#6b7280";
  const [duplicating, setDuplicating] = useState(false);
  const [deleting, setDeleting] = useState(false);
  const [confirmDel, setConfirmDel] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleDuplicate = async (ev: React.MouseEvent) => {
    ev.stopPropagation();
    setDuplicating(true);
    try { await duplicatePipeline(p.id); onDuplicated(); }
    catch (e: unknown) { setError(e instanceof Error ? e.message : String(e)); }
    finally { setDuplicating(false); }
  };

  const handleDelete = async (ev: React.MouseEvent) => {
    ev.stopPropagation();
    if (!confirmDel) { setConfirmDel(true); return; }
    setDeleting(true);
    try { await deletePipeline(p.id); onDeleted(p.id); }
    catch (e: unknown) { setError(e instanceof Error ? e.message : String(e)); setDeleting(false); setConfirmDel(false); }
  };

  return (
    <div style={{
      border: `1px solid ${expanded ? groupColor : "#e5e7eb"}`,
      borderRadius: 8, overflow: "hidden",
      transition: "border-color 0.15s",
    }}>
      <div
        style={{ padding: "12px 14px", background: expanded ? groupColor + "08" : "#fff", cursor: "pointer" }}
        onClick={onToggle}
      >
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 4 }}>
          <code style={{ fontSize: 13, fontWeight: 700, color: "#1e3a5f" }}>{p.id}</code>
          <div style={{ display: "flex", gap: 4, alignItems: "center" }}>
            {p.custom && (
              <span style={{
                fontSize: 9, padding: "1px 5px", borderRadius: 6,
                background: "#f3f4f6", color: "#6b7280", fontWeight: 600,
              }}>custom</span>
            )}
            <span style={{
              fontSize: 10, padding: "1px 6px", borderRadius: 8,
              background: groupColor + "20", color: groupColor, fontWeight: 600, whiteSpace: "nowrap",
            }}>
              {p.needsLM ? "LM" : "No LM"}
            </span>
            <button
              onClick={handleDuplicate}
              disabled={duplicating}
              title="Duplicate pipeline"
              style={btnMicro}
            >{duplicating ? "…" : "⎘"}</button>
            {p.custom && (
              <button
                onClick={handleDelete}
                disabled={deleting}
                title={confirmDel ? "Click again to confirm" : "Delete pipeline"}
                style={{
                  ...btnMicro,
                  background: confirmDel ? "#fef2f2" : undefined,
                  color: confirmDel ? "#b91c1c" : undefined,
                }}
              >{deleting ? "…" : confirmDel ? "Confirm?" : "🗑"}</button>
            )}
          </div>
        </div>
        <div style={{ fontSize: 13, fontWeight: 600, color: "#111827", marginBottom: 4 }}>{p.label}</div>
        <p style={{ margin: 0, fontSize: 12, color: "#6b7280", lineHeight: 1.5 }}>
          {expanded ? p.description : p.description.slice(0, 100) + (p.description.length > 100 ? "…" : "")}
        </p>
      </div>

      {error && (
        <div style={{ padding: "6px 14px", fontSize: 12, color: "#b91c1c", background: "#fef2f2" }}>
          {error}
        </div>
      )}

      {expanded && (
        <div style={{ padding: "0 14px 14px", borderTop: `1px solid ${groupColor}30`, marginTop: 8 }}>
          <div style={{ marginBottom: 8 }}>
            <span style={metaLabel}>Inputs:</span>
            <code style={metaValue}>{p.inputs}</code>
          </div>
          <div style={{ marginBottom: 10 }}>
            <span style={metaLabel}>Outputs:</span>
            <span style={{ fontSize: 12, color: "#374151" }}>{p.outputs}</span>
          </div>
          <div style={{ marginBottom: 10 }}>
            <span style={metaLabel}>Default params:</span>
            <pre style={{
              background: "#1e293b", color: "#e2e8f0", padding: "6px 10px",
              borderRadius: 4, fontSize: 11, fontFamily: "monospace",
              margin: "4px 0 0", overflowX: "auto",
            }}>
              {p.defaultParams}
            </pre>
          </div>
          {p.module && (
            <div style={{ fontSize: 11, color: "#9ca3af", marginBottom: 8 }}>Module: <code>{p.module}</code></div>
          )}
        </div>
      )}
    </div>
  );
}

const metaLabel: React.CSSProperties = {
  fontSize: 11, fontWeight: 600, color: "#6b7280",
  display: "block", marginBottom: 2, textTransform: "uppercase", letterSpacing: "0.05em",
};

const metaValue: React.CSSProperties = {
  fontSize: 11, color: "#374151", fontFamily: "monospace",
};

const btnMicro: React.CSSProperties = {
  padding: "2px 7px", border: "1px solid #e5e7eb", borderRadius: 4,
  cursor: "pointer", fontSize: 11, fontWeight: 600,
  background: "#fff", color: "#374151",
};
