/**
 * HelpView — In-app documentation viewer.
 * Renders the user manual and experiment guide with a simple tab navigation.
 */
import { useState } from "react";

interface Section {
  id: string;
  title: string;
  content: string;
}

const MANUAL_SECTIONS: Section[] = [
  {
    id: "quickstart",
    title: "Quick Start",
    content: `
## Quick Start

1. **Start the backend**: run \`setup-os.cmd start\` (Windows) or \`./setup-os.sh start\` (Linux/macOS)
2. **Open the UI**: \`http://localhost:8080\`
3. **Upload a corpus**: Corpora → Upload
4. **Open Glossa AI**: click the ✨ Glossa AI button in the sidebar
5. **Run an experiment**: Experiments → select → Run, or ask Glossa AI

### Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| Ctrl+K | Command palette |
| Ctrl+J | Toggle bottom panel |
| Shift+Enter | New line in AI input |
| Enter | Send AI message |
    `,
  },
  {
    id: "interface",
    title: "Interface",
    content: `
## Interface Overview

### Left Sidebar

| Section | Description |
|---|---|
| Corpora | Upload and manage sign-sequence corpora |
| Experiments | Browse and run computational experiments |
| Pipelines | Async job management |
| Studies | Compose multi-step research workflows |
| Reports | View and export experiment results |
| Entropy | Visualise entropy and Zipf distributions |
| Signs | Browse the sign dictionary |
| Hypotheses | Track research hypotheses |
| Notebooks | Research notes |
| Jobs | Background job queue |
| Settings | API keys, model selection |

### Bottom Panel (Ctrl+J)

- **Logs** — live backend log stream. Click **Purge** to clear old entries
- **Jobs** — job queue with expandable details (click any job row for results)
- **Terminal** — command-line access

### Glossa AI Panel

Click **✨ Glossa AI** to open the assistant. Features:
- **Context selector**: Global / Corpus / Experiment / Study / Research
- **Shift+Enter** for multi-line messages
- Copy button (⏩) copies the full conversation
- Actions auto-execute and show **View [page] →** links when done
    `,
  },
  {
    id: "glossa-ai",
    title: "Glossa AI",
    content: `
## Glossa AI Assistant

Glossa AI can perform the following actions automatically:

| Action | What it does |
|---|---|
| run_experiment | Runs a registered experiment, shows View → link |
| run_pipeline | Queues an async job |
| create_hypothesis | Saves to Hypotheses panel |
| create_notebook | Saves a research note |
| open_view | Navigates to a UI section |
| acquire_corpus | Downloads and registers a corpus |
| execute_script | Runs custom Python code |
| query_corpus | Searches sign patterns |
| summarize_session | Saves conversation to Notebooks |

### Tips

1. Set context to **Research** for deepest integration
2. Ask for specific actions: "Run experiment X", "Create hypothesis Y"
3. Provide anchors: "Rerun with anchors 004=T, 066=M"
4. After actions complete, click the View link to navigate without losing your chat

### Conversation Continuity

To preserve sessions across browser reloads:
- Ask: "Summarize this session and save it to notebooks"
- Next session: switch to Research context — LEDGER and notebooks are loaded automatically
    `,
  },
  {
    id: "corpus",
    title: "Corpus Formats",
    content: `
## Corpus File Formats

### Text (recommended)

\`\`\`
066-069-090-112
003-069-090-112
066-069-100-073
\`\`\`

One word per line, signs separated by \`-\`. Signs can be numeric codes or strings.

**Reading direction**: list signs in file order (left-to-right in the file). If the script is RTL, confirm direction using the Ashraf method and the system will reverse sequences internally.

### JSON

\`\`\`json
{
  "inscriptions": [
    {"sequence": ["066", "069", "090", "112"]},
    {"sequence": ["003", "069", "090", "112"]}
  ]
}
\`\`\`

### CSV

\`\`\`
066,069,090,112
003,069,090,112
\`\`\`

### Reading Direction (Ashraf 2018 Method)

The system can detect reading direction automatically:
- **Lower entropy at position 0** (leftmost in file) → word-END → RTL script
- **Lower entropy at position -1** (rightmost in file) → word-END → LTR script

Ask Glossa AI: "Apply the Ashraf handedness method to confirm reading direction."
    `,
  },
  {
    id: "experiments",
    title: "Experiments Guide",
    content: `
## Building Experiments

### Structure

\`\`\`python
# backend/glossa_lab/experiments/my_analysis.py
from glossa_lab.experiment_base import ExperimentBase
from pathlib import Path
import json
from datetime import datetime, timezone

REPORTS = Path(__file__).resolve().parent.parent.parent.parent / "reports"

class MyAnalysis(ExperimentBase):
    id             = "my_analysis"
    name           = "My Analysis"
    category       = "Validation"
    description    = "What this experiment does."
    estimated_time = "~1 min"
    command        = "python -m glossa_lab.experiments.my_analysis"

    def run(self, **kwargs) -> dict:
        result = {"answer": 42}
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
        (REPORTS / f"my_analysis_{ts}.json").write_text(
            json.dumps(result, indent=2), encoding="utf-8"
        )
        return result

if __name__ == "__main__":
    from glossa_lab.cli_bridge import run_with_reporting
    run_with_reporting("my_analysis", "My Analysis", MyAnalysis().run, verbose=True)
\`\`\`

### GPU/CPU Policy (H10)

Always check for GPU before numerical batch operations:

\`\`\`python
try:
    import cupy as xp
    _GPU = xp.cuda.is_available()
except ImportError:
    import numpy as xp
    _GPU = False
\`\`\`

When GPU unavailable, parallelize with ProcessPoolExecutor:

\`\`\`python
import os
from concurrent.futures import ProcessPoolExecutor

with ProcessPoolExecutor(max_workers=min(n_seeds, os.cpu_count() or 4)) as ex:
    results = list(ex.map(run_one_seed, seeds))
\`\`\`

### Study Pipelines

1. Go to **Studies** to open the graph canvas
2. Drag nodes from the palette onto the canvas
3. Connect nodes with edges (left to right = data flow)
4. Independent branches execute in parallel
5. Click **Run Study** to execute

### Example Pipeline: NW Semitic Analysis

\`\`\`
[Corpus] --> [Structural Analysis] --> [Mapping Inference] --> [Report]
                                   --> [Writing System Classification]
\`\`\`
    `,
  },
  {
    id: "results",
    title: "Understanding Results",
    content: `
## Understanding Results

### Mapping Consistency

**Consistency** (0–100%) = fraction of independent SA runs agreeing on the modal consonant for a sign.

- **What it IS**: stability of statistical inference (signal detection)
- **What it IS NOT**: accuracy or correctness
- At 4 tokens/sign, consistency does not predict accuracy

### Compression Ratio

The system narrows each sign from 22 possible consonants to ~2.4 candidates (80% posterior coverage) — a **~10x compression ratio** — before any external knowledge is applied.

### Anchor Amplifier

Adding 1 verified anchor produces improvement on non-anchored signs ~**12x** the naïve combinatorial expectation. Constraints propagate through the corpus structure.

### Writing System Classification

| Type | H1 range | Signs | Examples |
|---|---|---|---|
| Abjad | 4.1–4.7 | 22–30 | Hebrew, Ugaritic, Phoenician |
| Syllabary | 4.7–7.5 | 40–120 | Linear B, Old Persian |
| Logographic | >7.5 | 400+ | Sumerian, Chinese |

### Limitations

1. **Calibration**: at sparse densities (~4 tok/sign), consistency ≠ accuracy. The correct assignment is in the top-3 candidates in ~13% of cases (matches random baseline).
2. **Fragmented solutions**: with no anchors, each SA run finds a different local optimum (40–50 distinct solutions from 50 seeds).
3. **Frequency-driven**: at 4 tok/sign, the signal is primarily from unigram frequencies; within-word order is not detectable.

### What improves results

1. More corpus data (target: 10+ tokens/sign)
2. Verified anchor assignments from linguistic knowledge
3. A vocalized language model (for syllabic corpora)
    `,
  },
  {
    id: "troubleshooting",
    title: "Troubleshooting",
    content: `
## Troubleshooting

| Issue | Solution |
|---|---|
| Logs show old entries | Click **Purge** in the Logs panel |
| Action fails with error | The AI may have proposed an invalid action type; rephrase the request |
| Low consistency results | Expected at low token density; add verified anchor assignments |
| GPU not used | Install CuPy: \`pip install cupy-cuda12x\` |
| Experiments not listed | Click the reload (↻) button in the Experiments panel |
| PDF has white squares | Non-Latin-1 characters in report text; use ASCII equivalents |
| Backend not responding | Check \`setup-os.cmd status\`; restart with \`setup-os.cmd restart\` |

### Log Levels

The Logs panel shows colour-coded entries:
- **Green** — INFO/started/ready
- **Yellow** — WARNING
- **Red** — ERROR/exception/failed
- **Grey** — DEBUG

If logs look stale, click **Purge** (orange) to clear the log file and reset the display, then **Clear** (grey) to clear just the display.

### Backend Health

Go to **Status** in the sidebar for:
- CPU, RAM, disk, GPU usage
- Backend uptime
- Database connection status
- Ollama model status
    `,
  },
];

function renderSection(content: string): string {
  // Simple markdown → HTML for inline rendering (tables, code, bold, headers)
  let html = content
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/```[\w]*\n?([\s\S]*?)```/g,
      "<pre style='background:#1e293b;color:#e2e8f0;padding:8px 12px;border-radius:5px;font-size:11px;overflow-x:auto;margin:6px 0'>$1</pre>")
    .replace(/`([^`]+)`/g,
      "<code style='background:#f1f5f9;padding:1px 4px;border-radius:3px;font-size:12px;font-family:monospace'>$1</code>")
    .replace(/^## (.+)$/gm, "<h2 style='font-size:15px;font-weight:700;margin:14px 0 6px;color:#1e3a5f'>$1</h2>")
    .replace(/^### (.+)$/gm, "<h3 style='font-size:13px;font-weight:700;margin:10px 0 4px;color:#0f766e'>$1</h3>")
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(/^---$/gm, "<hr style='border:none;border-top:1px solid #e5e7eb;margin:12px 0'>")
    .replace(/^\| (.+) \|$/gm, (line) => {
      const cells = line.split("|").slice(1, -1).map(c => c.trim());
      return `<tr>${cells.map(c =>
        `<td style='padding:5px 10px;border:1px solid #e5e7eb;font-size:12px'>${c}</td>`
      ).join("")}</tr>`;
    })
    .replace(/^[-*] (.+)$/gm, "<li style='margin:3px 0;margin-left:16px'>$1</li>")
    .replace(/\n\n/g, "</p><p style='margin:6px 0'>")
    .replace(/\n/g, "<br>")
    .replace(/^/, "<p style='margin:0'>").replace(/$/, "</p>");

  // Fix table rows
  if (html.includes("<tr>")) {
    html = html.replace(/(<tr>.*?<\/tr>)+/gs, match =>
      `<div style='overflow-x:auto;margin:8px 0'><table style='border-collapse:collapse;font-size:12px;width:100%'>${match}</table></div>`
    );
  }
  return html;
}

export function HelpView() {
  const [activeId, setActiveId] = useState("quickstart");
  const section = MANUAL_SECTIONS.find(s => s.id === activeId) ?? MANUAL_SECTIONS[0];

  return (
    <div style={{ display: "flex", height: "100%", overflow: "hidden", fontFamily: "system-ui, sans-serif" }}>
      {/* Sidebar navigation */}
      <div style={{
        width: 180, background: "#f8fafc", borderRight: "1px solid #e5e7eb",
        display: "flex", flexDirection: "column", flexShrink: 0, overflowY: "auto",
      }}>
        <div style={{ padding: "12px 14px 8px", borderBottom: "1px solid #e5e7eb" }}>
          <div style={{ fontSize: 13, fontWeight: 700, color: "#1e3a5f" }}>📘 Help</div>
          <div style={{ fontSize: 10, color: "#9ca3af" }}>Glossa Lab v1.0</div>
        </div>
        {MANUAL_SECTIONS.map(s => (
          <button
            key={s.id}
            onClick={() => setActiveId(s.id)}
            style={{
              display: "block", width: "100%", textAlign: "left",
              padding: "8px 14px", border: "none", fontSize: 12,
              background: activeId === s.id ? "#eff6ff" : "none",
              color: activeId === s.id ? "#1d4ed8" : "#374151",
              fontWeight: activeId === s.id ? 600 : 400,
              borderLeft: activeId === s.id ? "3px solid #1d4ed8" : "3px solid transparent",
              cursor: "pointer",
            }}
          >
            {s.title}
          </button>
        ))}
        <div style={{ flex: 1 }} />
        <div style={{ padding: "8px 14px", fontSize: 10, color: "#9ca3af", borderTop: "1px solid #e5e7eb" }}>
          <div>Full docs: <code style={{ fontSize: 9 }}>docs/user-manual.md</code></div>
          <div style={{ marginTop: 2 }}>Experiments: <code style={{ fontSize: 9 }}>docs/guides/</code></div>
        </div>
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflowY: "auto", padding: "20px 28px" }}>
        <div
          style={{ maxWidth: 760, fontSize: 13, lineHeight: 1.7, color: "#111827" }}
          dangerouslySetInnerHTML={{ __html: renderSection(section.content) }}
        />
      </div>
    </div>
  );
}
