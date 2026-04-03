/**
 * Experiments View — launch and monitor analysis experiments.
 * Shows status of each experiment and links to results.
 */

import { useState } from "react";

interface Experiment {
  id: string;
  name: string;
  category: string;
  description: string;
  command: string;
  resultsFile?: string;
  requiresKey?: string;
  estimatedTime: string;
  status: "ready" | "needs_key" | "ran";
  lastRun?: string;
}

const EXPERIMENTS: Experiment[] = [
  {
    id: "ocr_tables",
    name: "OCR — Bigram & Frequency Tables",
    category: "Data Extraction",
    description:
      "Uses Mistral Pixtral to OCR pages 717–745 of Mahadevan (1977) — " +
      "the bigram pairwise frequency table (22 pages) and sign frequency/positional " +
      "distribution table (7 pages). Extracts complete bigram matrix and converts " +
      "M77 → Fuls sign numbers. ~30 minutes.",
    command: "python ocr_mahadevan.py --target tables",
    resultsFile: "reports/mahadevan_bigrams.json",
    requiresKey: "mistral_api_key",
    estimatedTime: "~30 min",
    status: "needs_key",
  },
  {
    id: "ocr_texts",
    name: "OCR — Inscription Sequences (2906 texts)",
    category: "Data Extraction",
    description:
      "OCR pages 39–162 of Mahadevan (1977) to extract the actual inscription " +
      "sign sequences. Enables Ventris grid, Markov model, contact zone analysis. " +
      "~2 hours for 124 pages.",
    command: "python ocr_mahadevan.py --target texts",
    resultsFile: "reports/mahadevan_texts.json",
    requiresKey: "mistral_api_key",
    estimatedTime: "~2 hours",
    status: "needs_key",
  },
  {
    id: "progression",
    name: "Fuls Progression Benchmark",
    category: "Validation",
    description:
      "Runs all analysis pipelines across the 5 writing system tiers " +
      "(Ugaritic → Hebrew → Linear B → Sumerian → Indus) validating the progression " +
      "Fuls proposed. Produces the progression_report.json for the collaboration email.",
    command: "python -m glossa_lab.experiments.progression_report",
    resultsFile: "reports/progression.json",
    estimatedTime: "~1 min",
    status: "ran",
    lastRun: "2026-04-03",
  },
  {
    id: "indus_atlas",
    name: "Indus Structural Atlas",
    category: "Analysis",
    description:
      "Full 11-section structural analysis of the Indus script from Fuls (2023) " +
      "statistics. Covers: corpus stats, block entropy (Rao 2009), Zipf (Yadav 2010), " +
      "positional analysis, sign polyvalence (sign 550), paradigm detection, " +
      "structural fingerprint, Ventris grid, word-structure typology.",
    command: "python -m glossa_lab.experiments.indus_structural_atlas",
    resultsFile: "reports/indus_structural_atlas.json",
    estimatedTime: "~1 min",
    status: "ran",
    lastRun: "2026-04-03",
  },
  {
    id: "real_catalog",
    name: "Real Catalog Analysis",
    category: "Analysis",
    description:
      "Analyzes real positional data extracted from Fuls (2023) Catalog — " +
      "713 signs with T/M/I/Solo counts. Runs NWSP classification, Zipf fit, " +
      "structural fingerprint, word-structure typology on the real data.",
    command: "python analyze_fuls_ebooks.py",
    resultsFile: "reports/real_indus_catalog_analysis.json",
    estimatedTime: "~1 min",
    status: "ran",
    lastRun: "2026-04-03",
  },
  {
    id: "kandles_bias",
    name: "Kandles Bias Comparison",
    category: "Experiments",
    description:
      "Compares Kandles phonological fingerprint scores with and without language-specific " +
      "bias profiles. Tests whether Luwian scores higher under its own phonological categories " +
      "vs the default Greek mapping.",
    command: "python -m glossa_lab.experiments.run_kandles_biased_experiments --trials 30",
    resultsFile: "reports/kandles_biased_results.json",
    estimatedTime: "~5 min",
    status: "ready",
  },
  {
    id: "ventris_validation",
    name: "Ventris Grid Validation (Linear B)",
    category: "Validation",
    description:
      "Validates our GPU-backed Ventris affinity analysis by testing it against " +
      "the known Linear B CV grid. Measures F1 score for row (same vowel) and " +
      "column (same consonant) groupings. Proof of concept for Indus application.",
    command: "python -m glossa_lab.experiments.ventris_validation",
    estimatedTime: "~10 sec",
    status: "ready",
  },
  {
    id: "markov_model",
    name: "Markov Model (Rao 2009 replication)",
    category: "Analysis",
    description:
      "Builds a bigram Markov model of the Indus script (Rao et al. 2009 approach). " +
      "Requires Mahadevan OCR inscription sequences. Once available, trains on M77 corpus, " +
      "generates sample texts, identifies contact-zone anomalies (Mesopotamian inscriptions).",
    command: "# Requires OCR texts first\npython ocr_mahadevan.py --target texts",
    requiresKey: "mistral_api_key",
    estimatedTime: "After OCR",
    status: "needs_key",
  },
];

const CATEGORY_COLORS: Record<string, string> = {
  "Data Extraction": "#7c3aed",
  "Validation": "#16a34a",
  "Analysis": "#2563eb",
  "Experiments": "#d97706",
};

export function ExperimentsView() {
  const [filter, setFilter] = useState<string>("all");
  const categories = ["all", ...Array.from(new Set(EXPERIMENTS.map((e) => e.category)))];

  const visible = filter === "all"
    ? EXPERIMENTS
    : EXPERIMENTS.filter((e) => e.category === filter);

  return (
    <div>
      <h2 style={{ marginTop: 0 }}>Experiments</h2>

      <div style={{
        background: "#f0fdf4",
        border: "1px solid #86efac",
        borderRadius: 8,
        padding: "10px 14px",
        marginBottom: "1.5rem",
        fontSize: 13,
      }}>
        <strong>How to run:</strong> Copy the command and run it from the repo root
        (<code>C:\...\glossa-lab</code>). Results save to <code>reports/</code> and
        are automatically picked up by the Studies view.
      </div>

      {/* Category filter */}
      <nav style={{ display: "flex", gap: 6, marginBottom: "1.5rem", flexWrap: "wrap" }}>
        {categories.map((c) => (
          <button key={c} onClick={() => setFilter(c)} style={{
            padding: "4px 14px", border: "1px solid", borderRadius: 20, cursor: "pointer",
            fontSize: 12, fontWeight: filter === c ? 600 : 400,
            background: filter === c ? (CATEGORY_COLORS[c] ?? "#1e3a5f") : "#fff",
            borderColor: filter === c ? (CATEGORY_COLORS[c] ?? "#1e3a5f") : "#d1d5db",
            color: filter === c ? "#fff" : "#374151",
          }}>
            {c.charAt(0).toUpperCase() + c.slice(1)}
          </button>
        ))}
      </nav>

      <div style={{ display: "grid", gap: "1rem" }}>
        {visible.map((exp) => (
          <ExperimentCard key={exp.id} exp={exp} />
        ))}
      </div>
    </div>
  );
}

function ExperimentCard({ exp }: { exp: Experiment }) {
  const [expanded, setExpanded] = useState(false);
  const catColor = CATEGORY_COLORS[exp.category] ?? "#6b7280";

  const statusInfo = {
    ran:       { label: "Ran", color: "#16a34a", bg: "#dcfce7" },
    ready:     { label: "Ready", color: "#2563eb", bg: "#dbeafe" },
    needs_key: { label: "Needs API key", color: "#d97706", bg: "#fef3c7" },
  }[exp.status];

  return (
    <div style={{
      border: "1px solid #e5e7eb",
      borderRadius: 8,
      overflow: "hidden",
      boxShadow: "0 1px 3px rgba(0,0,0,0.04)",
    }}>
      {/* Header */}
      <div
        style={{
          display: "flex", alignItems: "center", gap: 12, padding: "12px 16px",
          cursor: "pointer", background: "#fafafa",
          borderBottom: expanded ? "1px solid #e5e7eb" : "none",
        }}
        onClick={() => setExpanded((x) => !x)}
      >
        <span style={{ fontSize: 14, flex: 1, fontWeight: 600 }}>{exp.name}</span>
        <span style={{
          fontSize: 11, padding: "2px 8px", borderRadius: 10,
          background: catColor + "20", color: catColor, fontWeight: 600,
        }}>
          {exp.category}
        </span>
        <span style={{
          fontSize: 11, padding: "2px 8px", borderRadius: 10,
          background: statusInfo.bg, color: statusInfo.color, fontWeight: 600,
        }}>
          {statusInfo.label}
        </span>
        <span style={{ fontSize: 11, color: "#9ca3af" }}>{exp.estimatedTime}</span>
        <span style={{ fontSize: 16, color: "#9ca3af" }}>{expanded ? "▲" : "▼"}</span>
      </div>

      {expanded && (
        <div style={{ padding: "14px 16px" }}>
          <p style={{ margin: "0 0 1rem 0", fontSize: 13, color: "#374151", lineHeight: 1.6 }}>
            {exp.description}
          </p>

          {exp.requiresKey && exp.status === "needs_key" && (
            <div style={{
              background: "#fef3c7", border: "1px solid #fcd34d",
              borderRadius: 6, padding: "8px 12px", marginBottom: "0.75rem", fontSize: 12,
            }}>
              Requires <strong>{exp.requiresKey}</strong> — set it in the Settings tab.
            </div>
          )}

          {exp.resultsFile && exp.status === "ran" && (
            <div style={{
              background: "#f0fdf4", border: "1px solid #86efac",
              borderRadius: 6, padding: "8px 12px", marginBottom: "0.75rem", fontSize: 12,
            }}>
              Results saved at <code>{exp.resultsFile}</code>
              {exp.lastRun && <> · Last run: {exp.lastRun}</>}
            </div>
          )}

          <div style={{ marginTop: "0.5rem" }}>
            <label style={{ fontSize: 12, fontWeight: 600, color: "#374151", display: "block", marginBottom: 4 }}>
              Command (run from repo root):
            </label>
            <pre style={{
              background: "#1e293b", color: "#e2e8f0", padding: "10px 14px",
              borderRadius: 6, fontSize: 12, fontFamily: "monospace",
              margin: 0, overflowX: "auto", lineHeight: 1.7,
            }}>
              {exp.command}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
}
