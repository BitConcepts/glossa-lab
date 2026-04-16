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

### 1. Start the backend

Windows: double-click the **Glossa Lab** tray icon (system tray, bottom-right), or run:

\`\`\`
setup-os.cmd start
\`\`\`

macOS / Linux:

\`\`\`
./setup-os.sh start
\`\`\`

The backend runs on **port 8001** by default. To change the port, right-click the tray icon and choose **Change Port...**.

### 2. Open the UI

Navigate to **\`http://localhost:8001\`** in your browser. On Windows, the tray icon provides an **Open UI** link.

### 3. Upload your first corpus

1. Click **Corpora** in the left sidebar
2. Open **+ Upload / import corpus** and paste or import a sign-sequence file
3. Optionally click **🌍 Browse World Language Corpus Catalogue** to import a pre-curated corpus in one click

### 4. Run an experiment

- Go to **Experiments** in the sidebar — select a graph experiment from the list and click **Run**
- Or open **✨ Glossa AI** and ask: *"Run the NW Semitic analysis"*

### 5. View results

Results appear in **Reports & Data**. The Reports tab shows PDF/Markdown outputs; the Data tab shows JSON/CSV artefacts.

---

### Keyboard Shortcuts

| Shortcut | Action |
| Ctrl+K | Open command palette |
| Ctrl+J | Toggle bottom panel |
| Shift+Enter | New line in Glossa AI |
| Enter | Send Glossa AI message |

---

### Tray Icon (Windows/macOS)

Right-click the tray icon for:
- **Open UI** — opens the browser to the current port
- **Port: 8001** — shows the current backend port
- **Change Port...** — opens a dialog to set a new port (saved to \`~/.glossa-lab/config.json\`)
- **Stop Backend** — terminates the backend process
    `,
  },
  {
    id: "interface",
    title: "Interface",
    content: `
## Interface Overview

### Left Sidebar

| Section | Description |
| Corpora | Upload, inspect, sanitize, and manage sign-sequence corpora |
| Experiments | Browse, run, and build graph experiments |
| Pipelines | Async job management |
| Studies | Compose multi-experiment research workflows |
| Reports | PDF and Markdown outputs from experiments |
| Data | JSON and CSV data artefacts |
| Entropy | Visualise H1, Zipf, and positional entropy |
| Signs | Browse the sign dictionary |
| Hypotheses | Create and track research hypotheses |
| Notebooks | Research notes and session summaries |
| Jobs | Background job queue with result viewer |
| Status | CPU, RAM, GPU, DB, and backend uptime |
| Settings | API keys, model selection, environment |

---

### Corpora Panel

The Corpora panel is the entry point for all data:

- **Upload / import corpus** (collapsed by default): paste or load a text/CSV/JSON file. Set the name, type, tokenisation mode (space/line/character), and reading direction.
- **Browse World Language Corpus Catalogue**: a curated list of ~50 ancient, modern, and undeciphered corpora. Click **↓ Import** to instantly load any corpus with a bundled data module. Others show a **Source ↗** link.
- **Anchor Sets**: create, view, and delete named anchor-pair collections. Each pair maps a cipher sign to a target phoneme/syllable with a confidence rating (high/medium/low). Anchor sets are reusable across experiments via the **AnchorSetLoader** node.
- **Corpus cards**: each uploaded corpus is a collapsible card. Click a card to expand it.

Inside each corpus card, tabs provide:

| Tab | Description |
| Browse | Paginated view of all tokens. Search box filters results. Right-click to copy. |
| Edit | Change name, type, reading direction, tokenisation, and raw content. |
| Stats | H1 entropy, Zipf, TTR, token-type breakdown, and Unicode category distribution. |
| N-grams | Top n-grams by count, with a bar chart. |
| Concordance | KWIC search: find a token and see context left/right. |
| AI | Ask Glossa AI to analyse, detect anomalies, or critique the corpus. |
| Compare | Side-by-side entropy metric comparison against another corpus. |

---

### Experiments Panel

All user-visible experiments are **graph experiments** — JSON files that describe a directed acyclic graph (DAG) of atomic computation nodes. There are no Python experiment classes visible to users.

- **Palette** (left): atomic nodes grouped by category. Drag onto the canvas.
- **Graph canvas** (centre): connect nodes with edges. Data flows left to right.
- **Node inspector** (right): click a node to edit its parameters.
- **Run** button: executes the graph and streams results to the Jobs panel.
- **Sub-Experiments**: drag a graph experiment from the palette to embed it as a **SubExperiment** node, with explicit input/output ports.

Node categories include: Corpus Loaders, Language Models, Mapping Inference, Structural Analysis, Anchors, Filters, Evaluation, and Reporting.

---

### Study Builder

A Study is a graph of Experiments — it composes multiple experiments into a pipeline.

1. Open **Studies** in the sidebar
2. Drag experiment nodes from the palette onto the canvas
3. Connect outputs of one experiment to inputs of the next
4. Independent branches execute in parallel
5. Click **Run Study** to start all branches

Results from each experiment node appear in the Results panel after execution.

---

### Reports & Data Panel

The panel has two tabs:

- **Reports**: generated PDF and Markdown reports. Click to open in-browser, or download.
- **Data**: raw JSON and CSV artefacts from experiments. Download or inspect inline.

Both tabs support sorting by date (newest first) and filtering by keyword.

---

### Bottom Panel (Ctrl+J)

| Tab | Description |
| Logs | Live colour-coded backend log stream. Green=INFO, Yellow=WARN, Red=ERROR. Click Purge to clear. |
| Jobs | Job queue with status, progress, and expandable result JSON. |
| Terminal | Command-line access to the backend environment. |

---

### Glossa AI Panel

Click **✨ Glossa AI** to open the assistant panel. Key features:

- **Context selector**: choose Global, Corpus, Experiment, Study, or Research. Research context loads the full LEDGER and notebooks.
- **Shift+Enter** for multi-line messages; **Enter** to send.
- **Copy** (⏩) copies the full conversation history.
- **Actions** auto-execute and show **View [page] →** links on completion.
- After any action, click the View link to navigate without losing the chat.
    `,
  },
  {
    id: "glossa-ai",
    title: "Glossa AI",
    content: `
## Glossa AI Assistant

Glossa AI is an embedded AI research assistant. Open it by clicking **✨ Glossa AI** in the sidebar.

### Context Modes

| Context | What it loads |
| Global | General linguistics and scripting knowledge only |
| Corpus | The selected corpus content and statistics |
| Experiment | The selected experiment spec and recent results |
| Study | The selected study graph and all connected experiment results |
| Research | Full LEDGER, all notebooks, all hypothesis entries, all corpus summaries |

Use **Research** context for deep integration with your ongoing work. It is the most powerful mode.

---

### Automatic Actions

Glossa AI detects when you are asking for an action and executes it automatically, then shows a **View [page] →** navigation link.

| Action | Effect |
| run_experiment | Runs a graph experiment by name or ID. Shows progress in Jobs panel. |
| run_pipeline | Queues an async pipeline job. |
| create_hypothesis | Saves a structured hypothesis to the Hypotheses panel. |
| create_notebook | Saves a research note to Notebooks. |
| open_view | Navigates to any UI panel. |
| acquire_corpus | Downloads and registers a remote corpus by URL or known name. |
| execute_script | Runs a Python snippet in the backend environment. |
| query_corpus | Searches for a token pattern in a corpus and returns a concordance. |
| summarize_session | Saves the full conversation as a Notebook entry. |

---

### Effective Prompting

**Be specific about the corpus and experiment:**

> "Run the Fuls RTL corrected analysis on the NW Semitic Test1 corpus."

**Provide anchor assignments directly:**

> "Rerun with anchors: 004=T, 066=M, 208=N, 128=L, 080=W."

**Ask for validation:**

> "Is this result significantly above the random baseline? Compare H1 and TTR."

**Request chained workflows:**

> "Upload the Geez corpus, run the anchor convergence benchmark, and generate a PDF report."

**Summarise findings:**

> "Summarise the results of today's session and save to notebooks."

---

### Conversation Continuity

Glossa AI maintains context within a session. To preserve it across browser reloads:

1. At session end: *"Summarize this session and save it to notebooks."*
2. Next session: switch to **Research** context — LEDGER and notebooks are loaded automatically.
3. The LEDGER is a persistent record of all completed experiments, decisions, and findings.

---

### Limitations

- Glossa AI requires a configured LLM (set in **Settings**). Ollama (local) or OpenAI API are supported.
- Actions that require backend compute (experiments, scripts) run asynchronously. Check the **Jobs** tab for results.
- The AI does not have access to file system paths outside the backend data directory.
    `,
  },
  {
    id: "corpus",
    title: "Working with Corpora",
    content: `
## Working with Corpora

### Supported File Formats

**Text (recommended)** — one word/inscription per line, signs separated by \`-\`:

\`\`\`
066-069-090-112
003-069-090-112
066-069-100-073
\`\`\`

**JSON** — list of inscription objects:

\`\`\`json
{
  "inscriptions": [
    {"sequence": ["066", "069", "090", "112"]},
    {"sequence": ["003", "069", "090", "112"]}
  ]
}
\`\`\`

**CSV** — comma-separated, one word per line:

\`\`\`
066,069,090,112
003,069,090,112
\`\`\`

---

### Uploading a Corpus

1. Click **Corpora** → **+ Upload / import corpus**
2. Enter a **Name** and choose a **Type** (linguistic, ancient, dna, code, random, other)
3. Set **Tokenisation**: Space-separated (one token per space), Line-per-token, or Character-level
4. Set **Reading Direction**: LTR, RTL, or Unknown. Use **🔍 Auto-detect** to apply the Ashraf method.
5. Paste your corpus content or click **↑ Import File** to load a .txt / .csv / .json file
6. Click **Upload**

---

### Detecting Reading Direction (Ashraf 2018)

The Ashraf positional entropy method determines RTL vs LTR empirically:

- Compute unigram entropy at each word position
- **Lower entropy at position 0** (leftmost in file) → position 0 is word-END → RTL script
- **Lower entropy at position −1** (rightmost) → position −1 is word-END → LTR script

Click **🔍 Auto-detect** in the Edit tab, or ask Glossa AI:
> "Apply the Ashraf (2018) handedness method to this corpus."

Once confirmed RTL, all positional analyses (T/I/M profiles, anchor selection) will use reversed sequences.

---

### Inspecting Corpus Statistics

Open the **Stats** tab on any corpus card to see:

- **H1 (bits)** — unigram entropy. Abjad: 4.1–4.7, Syllabary: 4.7–7.5, Logographic: >7.5
- **H2/H1 ratio** — bigram compression relative to unigram. <1.0 = strong sequential structure
- **Conditional H** — entropy of a sign given the preceding sign
- **TTR** (Type-Token Ratio) — vocabulary richness
- **Zipf ρ** — Pearson correlation of log-rank vs log-freq (Zipf fit quality)
- **Hapax count** — number of tokens appearing exactly once
- **Token-type breakdown** — distribution of Unicode categories across tokens (numeric, Latin, non-Latin, punctuation). A warning flag appears if more than 5% of tokens are mixed-category.

---

### Sanitizing a Corpus (TokenFilter Node)

Real-world corpora often contain noise: punctuation, Latin annotations mixed with ancient glyphs, or rare hapax tokens. Use the **TokenFilter** atomic node in your experiment graph to clean the corpus before analysis.

TokenFilter parameters:

| Parameter | Description |
| unicode_range | Keep only tokens whose characters fall within a Unicode codepoint range (e.g. 0x1200-0x137F for Ethiopic/Geez) |
| blocklist | A list of specific tokens to always remove |
| min_frequency | Drop tokens appearing fewer than N times in the corpus |
| invert | If true, remove tokens matching the range (instead of keeping them) |

Example: for a Geez corpus contaminated with punctuation, set \`unicode_range = [0x1200, 0x137F]\` to keep only Geez syllabic characters.

---

### Browsing the World Corpus Catalogue

The catalogue contains ~50 pre-curated corpora from ancient, modern, and undeciphered writing systems.

1. Click **🌍 Browse World Language Corpus Catalogue** in the Corpora panel
2. Filter by **All / Undeciphered / Deciphered** and search by language name
3. Click **↓ Import** on any corpus with a local module — it loads instantly with no download
4. Corpora without a local module show a **Source ↗** link to their public-domain origin

---

### Creating Anchor Sets

Anchor sets store verified sign-to-sound assignments that you can reuse across experiments.

1. Click **⚓ Anchor Sets** in the Corpora panel
2. Click **+ New Set**
3. Enter a name (e.g. "Fuls Ugaritic Anchors") and optional language
4. Paste anchor pairs, one per line, in the format:

\`\`\`
cipher_sign   target   confidence   note
004           T        high         Fuls verified 2024
066           M        high         Word-final mem
208           N        high         Positional I=0.92
\`\`\`

5. Click **Create**. The anchor set is now available to the **AnchorSetLoader** node in experiments.

Confidence levels: **high** (green), **medium** (yellow), **low** (red) — shown as colour-coded badges.
    `,
  },
  {
    id: "experiments",
    title: "Experiment Builder",
    content: `
## Experiment Builder

All experiments in Glossa Lab are **graph experiments** — directed acyclic graphs (DAGs) where each node is an atomic computation step. There is no Python coding required.

---

### Hierarchy

- **Study** — a graph of Experiments. Composed in the Study Builder.
- **Experiment** — a graph of atomic Nodes. Composed in the Experiment Builder.
- **Atomic Node** — a single computation step implemented internally in Python.

---

### Anatomy of the Experiment Builder

- **Palette (left)**: all available atomic nodes, grouped by category. Drag onto the canvas.
- **Canvas (centre)**: the experiment graph. Connect node output ports to input ports of downstream nodes.
- **Node Inspector (right)**: click any node to view and edit its parameters.
- **Run button**: executes the graph. Results stream to the Jobs panel.

---

### Node Categories and Key Nodes

**Corpus Loaders**
- *CorpusLoader* — loads a corpus from the database by ID
- *CorpusLM* — loads a corpus and builds a language model from it directly (no Python file needed)
- *BuiltinLM* — loads a pre-seeded language model (Old Hebrew, Geez, Phoenician, etc.)

**Structural Analysis**
- *EntropyAnalyzer* — computes H1, H2, conditional entropy, Zipf, TTR
- *WritingSystemClassifier* — classifies as abjad/syllabary/logographic from H1 and alphabet size
- *PositionalProfiler* — computes T/I/M (terminal/initial/medial) probabilities per sign

**Corpus Filters**
- *TokenFilter* — removes tokens by Unicode range, explicit blocklist, or minimum frequency

**Mapping Inference**
- *MappingInference* — SA-based sign-to-phoneme inference engine (main decipherment node)
- *AnchorInjector* — locks specified sign-phoneme assignments before inference
- *AnchorSetLoader* — loads a saved anchor set from the database by ID
- *AnchorConvergenceBenchmark* — sweeps over anchor counts (0, 1, 2, 3, ...) and measures convergence

**Evaluation**
- *ConsistencyEvaluator* — measures across-seed agreement
- *AnchorAccuracyEvaluator* — evaluates held-out anchor recovery rate
- *RandomBaselineComparator* — compares results to a shuffled-corpus baseline

**Reporting**
- *JSONReportWriter* — writes results to JSON in the Data panel
- *MarkdownReportWriter* — writes a Markdown summary to the Reports panel
- *PDFReportWriter* — generates a PDF from a report template
- *ReportGenerator* — uses a user-defined report template (from the Report Templates UI)

**Sub-Experiments**
- *SubExperiment* — embeds another experiment as a reusable node. Drag from the Experiments section of the palette.
- *ExperimentInput* / *ExperimentOutput* — declare explicit ports for an experiment to be used as a subroutine.

---

### Connecting Nodes

- Drag from an **output port** (right side of a node) to an **input port** (left side of another node)
- Port types must be compatible (e.g. \`corpus\` output → \`corpus\` input)
- Incompatible connections are shown in red
- Multiple outputs can feed into the same input (last writer wins)
- A node with no upstream inputs reads its params from the Node Inspector

---

### Example: NW Semitic Decipherment

\`\`\`
CorpusLoader → TokenFilter → AnchorSetLoader → MappingInference → ConsistencyEvaluator → JSONReportWriter
                            ⇓                                                              ⇓
                     AnchorInjector                                               MarkdownReportWriter
\`\`\`

---

### GPU / CPU Acceleration

MappingInference and other numerically intensive nodes automatically use GPU (CuPy) if available, and fall back to CPU (NumPy) with multi-core parallelism otherwise. No configuration is required.

To enable GPU: install CuPy matching your CUDA version:
\`\`\`
pip install cupy-cuda12x
\`\`\`
    `,
  },
  {
    id: "results",
    title: "Understanding Results",
    content: `
## Understanding Results

### Writing System Classification

| Type | H1 range | Alphabet size | Examples |
| Abjad (consonant alphabet) | 4.1–4.7 bits | 22–30 signs | Hebrew, Ugaritic, Phoenician |
| Syllabary | 4.7–7.5 bits | 40–120 signs | Linear B, Old Persian, Geez |
| Logographic | >7.5 bits | 400+ signs | Sumerian, Chinese, Egyptian |

The classifier uses H1 (unigram entropy) and alphabet size jointly. A corpus at H1 = 5.6 bits with 78 signs classifies as **SYLLABIC** (nearest comparator: Linear B).

---

### Mapping Consistency

**Consistency** (0–100%) is the fraction of independent SA inference runs that agree on the same phoneme assignment for a given sign.

- **What it IS**: a measure of *signal stability* — whether the data reliably points to one assignment
- **What it IS NOT**: accuracy or correctness. A sign with 90% consistency could still be wrongly assigned if the corpus is small.
- At 4 tokens/sign, consistency does not predict accuracy. The corpus is underdetermined.

Interpretation guidelines:

| Consistency | Interpretation |
| ≥80% | Strong signal: the corpus reliably constrains this sign |
| 60–80% | Moderate signal: plausible but check against anchors |
| <60% | Weak signal: multiple competing solutions, more data needed |

---

### Compression Ratio

Before any anchors, the system reduces the search space from the full phoneme alphabet (e.g. 22 consonants for a Semitic target) to ~2.4 candidates at 80% posterior coverage. This is a **~10x compression ratio** achieved purely from corpus statistics.

This means the system eliminates ~90% of wrong assignments even with no external knowledge.

---

### Anchor Amplifier Effect

Adding one verified anchor produces improvement on non-anchored signs approximately **12x** the naive combinatorial expectation. This is because the constraint propagates through the co-occurrence structure of the corpus.

Empirical benchmark (Geez syllabic corpus, structured anchors):

| Anchors | Free-sign accuracy |
| 0 | 4.5% (random baseline) |
| 1 | 7.2% (+60% gain) |
| 3 | 12.1% (+170% gain vs baseline) |
| 6 | cluster collapse observed |

Random anchors (placebo condition) produce no consistent improvement.

---

### Positional Profiles (T/I/M)

The positional profiler classifies each sign as:

- **T** (terminal) — predominantly at word-end. High T values → likely grammatical suffixes or determinatives.
- **I** (initial) — predominantly at word-start. High I values → likely prefixes or determinatives.
- **M** (medial) — mainly in the middle of words. Most signs in large alphabets are medial.

High T or I signs are the highest-priority anchor candidates because their function constrains phoneme assignment most strongly.

---

### RTL Correction

For right-to-left scripts, all positional analysis must use reversed sequences. The Ashraf method detects this automatically. After RTL correction, the T/I/M labels apply to the linguistically correct word positions.

Example: Sign 066 in NW Semitic has file-position T=0.022 (near word-start in file), but after RTL correction has T=0.967 (dominant word-final sign, consistent with mem −m suffix).

---

### Known Limitations

1. **Low-density corpora (~4 tok/sign)**: consistency does not predict accuracy. The correct assignment is in the top-3 candidates in ~13% of cases, which matches the random baseline. Add anchors to improve.
2. **Fragmented solutions**: with no anchors, each SA run finds a different local optimum. 50 seeds may produce 40–50 distinct full solutions. Only consistency aggregation makes the results interpretable.
3. **Frequency-dominated signal**: at 4 tok/sign, the dominant signal is unigram frequency. Within-word sequential order is not detectable. You need ≥10 tok/sign for sequence-level information to emerge.
4. **LM quality**: a language model that does not match the target script type (e.g. using a Hebrew LM for a syllabic corpus) reduces accuracy. Use CorpusLM with an appropriate reference corpus.
    `,
  },
  {
    id: "troubleshooting",
    title: "Troubleshooting",
    content: `
## Troubleshooting

### Common Issues

| Issue | Solution |
| Logs show stale entries | Click **Purge** (orange) in the Logs panel to clear the file. Then **Clear** (grey) to reset display. |
| Logs not updating | The EventSource stream may have dropped. Click Purge to trigger a reconnect. |
| Action fails with error | The AI proposed an invalid action. Rephrase: "Run experiment X" instead of vague phrasing. |
| Low consistency results | Expected at low token density (~4 tok/sign). Add verified anchor assignments. |
| Anchor amplifier not working | Anchors may conflict with each other or with LM priors. Use high-confidence anchors only. |
| GPU not used | Install CuPy: \`pip install cupy-cuda12x\`. Check GPU with \`nvidia-smi\`. |
| Experiments not listed | Click the reload (↻) button in the Experiments panel. |
| PDF has white squares | Non-Latin-1 characters in report text. Use ASCII equivalents or ask Glossa AI to transliterate. |
| Backend not responding | Windows: \`setup-os.cmd restart\`. macOS/Linux: \`./setup-os.sh restart\`. |
| UI shows wrong port | Check backend port in tray icon. Default is 8001. Match URL to the displayed port. |
| Corpus import fails | Check file encoding (UTF-8 required). Ensure format matches: one word per line, signs separated by \`-\`. |
| World catalogue import unavailable | The corpus has no bundled module; download from Source ↗ and upload manually. |
| Anchor set not loading in experiment | Ensure the AnchorSetLoader node's \`anchor_set_id\` parameter matches the correct set ID. |
| TokenFilter removes all tokens | Check that \`unicode_range\` covers your script's codepoints. Use Stats tab to confirm token categories. |
| Graph experiment not running | Check node connections: all required input ports must be connected. Red ports indicate missing connections. |
| SubExperiment node fails | The referenced experiment must have ExperimentInput/ExperimentOutput ports defined. |

---

### Log Levels

The Logs panel shows colour-coded entries:
- **Green** — INFO, started, ready
- **Yellow** — WARNING
- **Red** — ERROR, exception, failed
- **Grey** — DEBUG

If the stream appears stuck, click **Purge** to clear and restart the log stream.

---

### Backend Health

Open **Status** in the sidebar to check:
- CPU, RAM, disk, and GPU usage
- Backend uptime and process ID
- Database connection status (SQLite path)
- Ollama model status (if using local LLM)

If backend does not start:
1. Check that port 8001 is not in use by another process
2. Look at the Logs panel for startup errors
3. If the port is in use, change it via the tray icon **Change Port...** menu

---

### Performance Tips

- Use **GPU** (CuPy) for inference with >20 seeds — 3–10x faster than CPU
- Use **ProcessPoolExecutor** path (CPU) for small-scale experiments (<10 seeds) to avoid CUDA overhead
- Keep corpus files under 50,000 tokens for interactive Stats tab performance
- Set \`min_frequency\` in TokenFilter to remove hapax tokens when corpus is sparse
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
      // Skip markdown separator rows like |---|---|
      if (/^\|[-:\s|]+\|$/.test(line)) return "";
      const cells = line.split("|").slice(1, -1).map(c => c.trim());
      // First row in a table block — if all cells look like headers (bold or after a header), wrap in <th>
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
