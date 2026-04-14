# Glossa Lab — User Manual

**Version**: 1.0 · BitConcepts Research Platform

---

## What is Glossa Lab?

Glossa Lab is an agentic computational linguistics research platform for the statistical analysis and mapping inference of ancient and unknown writing systems. It combines:

- **Corpus management** — upload, register, and manage sign-sequence corpora
- **Structural analysis** — entropy, Zipf, positional profiles (T/I/M), writing-system classification
- **Mapping inference** — statistical SA-based sign-to-phoneme hypothesis generation
- **Study pipelines** — composable graph-based experiment workflows
- **Glossa AI** — an embedded research assistant that can run analyses, propose hypotheses, and navigate the tool
- **Reports** — PDF and JSON export of all experimental results

---

## Quick Start

1. **Start the backend**: `setup-os.cmd start` (Windows) or `./setup-os.sh start` (Linux/macOS)
2. **Open the UI**: navigate to `http://localhost:8080` in your browser
3. **Upload a corpus**: click **Corpora** in the left sidebar → **Upload**
4. **Ask Glossa AI**: click the **Glossa AI** button in the sidebar to open the assistant panel
5. **Run an experiment**: go to **Experiments**, find an experiment in the palette, or ask Glossa AI to run one

---

## Interface Overview

### Left Sidebar

| Section | Description |
|---|---|
| **Corpora** | Upload and manage sign-sequence corpus files |
| **Experiments** | Browse and run computational experiments |
| **Pipelines** | Async job management |
| **Studies** | Compose multi-step research workflows |
| **Reports** | View and export experiment results |
| **Entropy** | Visualise corpus entropy and Zipf distributions |
| **Signs** | Browse the sign dictionary |
| **Timeline** | Research activity timeline |
| **Hypotheses** | Track research hypotheses |
| **Notebooks** | Research notes and session summaries |
| **AI Tools** | Advanced Glossa AI tooling |
| **Status** | System health and metrics |
| **Jobs** | Background job queue |
| **Settings** | API keys, model selection, environment |

### Bottom Panel (IDE-style)

The bottom panel (toggle with **Ctrl+J**) shows:

- **Logs** — live structured log stream from the backend; click **Purge** to clear old entries
- **Jobs** — job queue with expandable details; click any job to see results
- **Terminal** — command-line access to the backend environment

### Glossa AI Panel

Click the **✨ Glossa AI** button in the sidebar to open the AI assistant. It can:

- Answer research questions about the corpus and experiments
- Propose and run experiments automatically
- Navigate to relevant UI sections after completing actions
- Create hypotheses and notebook entries

**Tips:**
- Use **Shift+Enter** for multi-line messages
- Use **Copy** button (⏩) to copy the full conversation
- Set context (Global / Corpus / Experiment / Study / Research) to give the AI relevant data
- After an experiment completes, a **View [section] →** link appears — click it to navigate without losing your chat

---

## Mock Study Walkthrough: NW Semitic Test1 Analysis

This walkthrough follows the actual analysis performed for Dr. Andreas Fuls of TU Berlin, using a 101-word NW Semitic syllabic corpus.

### Step 1: Upload the Corpus

1. Go to **Corpora** in the sidebar
2. Click **Upload Corpus**
3. Upload your sign-sequence file in one of these formats:
   - **Text file** (`.txt`): one word per line, signs separated by `-` (e.g. `066-069-090-112`)
   - **CSV** or **JSON** supported
4. Give the corpus a name (e.g. "NW Semitic Test1") and set the type to **Ancient**
5. Click **Create**

The corpus is now registered with a unique ID and is available across all experiments.

### Step 2: Structural Fingerprint

Open **Glossa AI** and ask:

> "Analyse the structural fingerprint of the NW Semitic Test1 corpus — entropy, Zipf, word-length distribution, and writing-system classification."

Glossa AI will:
1. Compute H₁ unigram entropy and compare to known writing systems
2. Fit a Zipf curve and report R²
3. Show the word-length distribution
4. Classify the writing system (alphabetic / syllabic / logographic) based on the Ashraf (2018) entropy method

**What to expect:** an entropy of ~5.6 bits places the corpus in the syllabic tier (between alphabetic ~4.2–4.6 and logographic >7.5 bits).

### Step 3: Reading Direction Confirmation

For any corpus that might be RTL (right-to-left):

> "Apply the Ashraf (2018) handedness method to confirm the reading direction of this corpus."

The method compares:
- **Entropy at position 0** (leftmost in file) — lower = more constrained = word-END
- **Entropy at position -1** (rightmost) — higher = less constrained = word-BEGIN

If position 0 has lower entropy, reading is RIGHT-TO-LEFT. All subsequent positional analysis should use reversed sequences.

### Step 4: Positional Profile Analysis

> "Compute the T/I/M positional profiles for all signs — which are terminal, initial, and medial?"

The system classifies each sign by how often it appears at:
- **T** (terminal) — end of word
- **I** (initial) — beginning of word
- **M** (medial) — middle of word

**Key findings from the Fuls collaboration:**
- Sign **066** (RTL-corrected): T=0.967 — dominant word-final sign, consistent with the -m suffix (mem)
- Sign **073** (RTL-corrected): I=1.000 — pure word-initial sign
- Sign **112**: I=1.000 in RTL — second most frequent word-initial sign

These are your highest-priority anchor targets.

### Step 5: Run Mapping Inference (No Anchors)

Go to **Experiments** and run `fuls_nw_semitic_decipher_run`, or ask Glossa AI:

> "Run the mapping inference on this corpus with no anchors, 20 seeds."

This produces:
- A proposed consonant assignment for each sign (the modal assignment across 20 runs)
- A stability/consistency score (% of runs agreeing on the modal)
- High-confidence signs (≥75% consistency)

**What to expect at 4 tokens/sign:** ~55–60% mean consistency, 10–17 high-confidence signs. The signal is frequency-driven; sequential order is not detectable at this corpus density.

### Step 6: Run Mapping Inference (With Verified Anchors)

If you have verified sign-to-sound assignments from linguistic knowledge, add them as anchors:

> "Run the mapping inference again with these anchors: 004=T, 066=M, 208=N, 128=L, 080=W. Show the results."

With 6 anchors, expect:
- Mean consistency rises to ~64%
- High-confidence signs approximately double (10 → 23)
- All 6 anchor signs lock to 100% consistency

### Step 7: Robustness Validation

To demonstrate that the signal is real and not dependent on the specific language model:

> "Run the validation suite — random corpus control, cross-LM test, sequence information test."

Key results:
- **Random corpus control**: real corpus should be 15–20pp above random
- **Cross-LM test**: Hebrew, Blended NW Semitic, Uniform — signal should persist across non-uniform LMs
- **Sequence information test**: determines whether the signal depends on within-word order or only frequencies

### Step 8: Export the Report

Go to **Reports** or ask Glossa AI:

> "Generate the PDF report of all experimental results."

The report includes all tables, figures, and a summary of findings. It is saved to the `reports/` directory and is viewable directly in the Reports panel.

---

## Understanding the Results

### Consistency Metric

**Mapping consistency** (0–100%) is the fraction of independent SA runs that propose the same consonant assignment for a given sign. It measures:

- **What it IS**: stability of the statistical inference (real signal detection)
- **What it IS NOT**: accuracy or correctness of the assignment

At 4 tokens/sign, consistency does not predict accuracy — the solution space is underdetermined. The system's value is in **narrowing candidates from 22 to ~2–3** (10x compression) and in **amplifying verified anchors** across the corpus.

### Compression Ratio

The system reduces the per-sign search space from the full target alphabet (22 consonants) to ~2.4 candidates at 80% posterior coverage — a ~10x compression ratio.

### Anchor Amplifier

Adding one verified anchor produces a gain on non-anchored signs approximately **12x** the naïve combinatorial expectation. The constraint propagates through the statistical structure of the corpus.

### Writing System Classification

The Ashraf (2018) method classifies writing direction empirically from the data:
- Lower entropy at position 0 = word-END = right-to-left writing
- Lower entropy at position -1 = word-END = left-to-right writing

---

## Corpus File Formats

### Text format (recommended)

```
066-069-090-112
003-069-090-112
066-069-100-073
```

One word per line, signs separated by `-`. Signs can be numeric codes or strings.

**Reading direction**: list signs in file order (left-to-right in the file). If the script is RTL, the system will reverse sequences internally after direction is confirmed.

### JSON format

```json
{
  "inscriptions": [
    {"sequence": ["066", "069", "090", "112"]},
    {"sequence": ["003", "069", "090", "112"]}
  ]
}
```

### CSV format

```
066,069,090,112
003,069,090,112
```

---

## Glossa AI Tips

### Getting the best results

1. **Set context to Research** for the deepest integration with experimental results and the LEDGER
2. **Ask for specific actions**: "Run experiment X", "Create hypothesis Y", "Navigate to Reports"
3. **Provide anchors explicitly**: "Rerun with anchors 004=T, 066=M"
4. **Ask for validation**: "Is the signal statistically significant vs random baseline?"

### Action types Glossa AI can perform

| Action | What it does |
|---|---|
| Run experiment | Executes a registered experiment, shows View → link when done |
| Run pipeline | Queues an async job |
| Create hypothesis | Saves a testable hypothesis to the Hypotheses panel |
| Create notebook | Saves a research note |
| Open view | Navigates to a UI panel |
| Acquire corpus | Downloads and registers a corpus from a known source |
| Execute script | Runs custom Python analysis code |
| Query corpus | Searches for sign patterns in the corpus |
| Summarize session | Saves the conversation to Notebooks |

### Conversation continuity

Glossa AI maintains full conversation context within a session. To preserve context across sessions:

1. Ask Glossa AI: "Summarize this session and save it to notebooks"
2. Next session: start with "Load context from research mode" or upload the saved notebook

---

## Troubleshooting

| Issue | Solution |
|---|---|
| Logs show old entries | Click **Purge** in the Logs panel to clear the log file |
| Action fails with "Unknown action type" | The AI proposed an invalid action; try rephrasing the request |
| Low consistency results | Expected at low token density; add anchor assignments to improve |
| GPU not used | Install CuPy (`pip install cupy-cuda12x`) to enable GPU acceleration |
| Experiments not appearing | Click the reload button in the Experiments panel |

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| **Ctrl+K** | Open command palette |
| **Ctrl+J** | Toggle bottom panel |
| **Shift+Enter** | New line in Glossa AI input |
| **Enter** | Send message in Glossa AI |

---

## Reference: Writing System Classification

| Type | H₁ range | Signs | Examples |
|---|---|---|---|
| Abjad (consonant alphabet) | 4.1–4.7 | 22–30 | Hebrew, Ugaritic, Phoenician |
| Syllabary | 4.7–7.5 | 40–120 | Linear B, Cypriot, Old Persian |
| Logographic | >7.5 | 400+ | Sumerian, Chinese |

The test1 corpus (H₁ = 5.607, 78 signs) classifies as **SYLLABIC** with HIGH confidence, nearest known system: Linear B (Mycenaean Greek).

---

*Glossa Lab — BitConcepts Research Programme*
