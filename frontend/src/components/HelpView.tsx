/**
 * HelpView — In-app documentation viewer.
 * Full user manual with comprehensive coverage of all platform features.
 *
 * Renderer: tables are processed as complete line-blocks BEFORE any newline→<br>
 * substitution, so no <br> can appear between <tr> elements.
 */
import { useState } from "react";

interface Section {
  id: string;
  title: string;
  content: string;
}

// ---------------------------------------------------------------------------
// Section content
// ---------------------------------------------------------------------------

const MANUAL_SECTIONS: Section[] = [
  // ─── 1. QUICK START ────────────────────────────────────────────────────
  {
    id: "quickstart",
    title: "Quick Start",
    content: `
## Quick Start

Glossa Lab is a self-contained research platform. The backend (FastAPI + SQLite) and the frontend (React) are bundled together and launched from a single command or tray icon.

---

### System Requirements

| Component | Minimum | Recommended |
| OS | Windows 10, macOS 12, Ubuntu 20.04 | Windows 11 or Ubuntu 22.04 |
| Python | 3.10 | 3.11 |
| RAM | 4 GB | 16 GB |
| Disk | 2 GB free | 10 GB free |
| GPU | None (CPU fallback available) | NVIDIA with CUDA 12.x |
| Browser | Chrome 110+, Firefox 115+ | Chrome latest |

---

### Starting the Backend

**Windows — tray icon (recommended)**

Double-click the **Glossa Lab** tray icon in the system tray (bottom-right corner of the taskbar). The backend starts automatically. Right-click the tray icon for options.

**Windows — command line**

\`\`\`
setup-os.cmd start
\`\`\`

**macOS / Linux**

\`\`\`
./setup-os.sh start
\`\`\`

The backend starts on **port 8001** by default and logs startup progress to the terminal and to the in-app Logs panel.

---

### Opening the UI

Navigate your browser to:

\`\`\`
http://localhost:8001
\`\`\`

On Windows, right-click the tray icon and choose **Open UI** — it opens the correct URL automatically even if you changed the port.

---

### Changing the Port

If port 8001 is occupied by another process:

1. Right-click the tray icon → **Change Port...**
2. Enter the new port number
3. Click OK — the backend restarts on the new port
4. The tray icon **Open UI** link updates automatically

Port settings are saved to \`~/.glossa-lab/config.json\` and persist across restarts.

---

### Stopping the Backend

\`\`\`
setup-os.cmd stop
\`\`\`

Or right-click the tray icon → **Stop Backend**.

---

### First Steps

1. **Upload a corpus** — Corpora → **+ Upload / import corpus**
2. **Or import a pre-built corpus** — click **Browse World Language Corpus Catalogue** and click **↓ Import** on any entry with a bundled module
3. **Run an experiment** — Experiments → select a graph experiment → **Run**
4. **Ask Glossa AI** — click **✨ Glossa AI** in the sidebar and describe what you want to do

---

### Keyboard Shortcuts

| Shortcut | Action |
| Ctrl+J | Toggle the bottom panel (Logs / Jobs / Terminal) |
| Ctrl+K | Open the command palette |
| Shift+Enter | Insert newline in Glossa AI input |
| Enter | Send Glossa AI message |
| Esc | Close modal dialogs |

---

### Tray Icon Reference (Windows/macOS)

Right-click the system tray icon for:

| Menu item | Action |
| Open UI | Opens the browser to the backend URL |
| Port: 8001 | Shows current port (read-only label) |
| Change Port... | Opens a dialog to change and persist the port |
| Restart Backend | Stops and restarts the backend process |
| Stop Backend | Terminates the backend process |

---

### Checking Status

Click **Status** in the sidebar to see real-time backend health:

- CPU, RAM, disk, and GPU usage
- Backend process uptime
- SQLite database path and connection state
- Ollama model status (if a local LLM is configured)

If the backend is not running, the Status view shows a **"Backend offline"** indicator.
    `,
  },

  // ─── 2. INTERFACE GUIDE ────────────────────────────────────────────────
  {
    id: "interface",
    title: "Interface Guide",
    content: `
## Interface Guide

The Glossa Lab UI is a single-page application with a persistent sidebar on the left, a main content area in the centre, an optional AI panel on the right, and a bottom panel for logs, jobs, and terminal access.

---

### Left Sidebar — Panel Reference

| Panel | Purpose |
| **Corpora** | Upload, inspect, sanitize, and manage sign-sequence corpora. World Language Catalogue and Anchor Set editor live here. |
| **Experiments** | Browse graph experiments, build new ones in the visual canvas, and run them. |
| **Pipelines** | Manage asynchronous pipeline jobs (long-running background tasks). |
| **Studies** | Compose multi-experiment research workflows as graphs of experiments. |
| **Reports** | View generated PDF and Markdown reports from experiments. |
| **Data** | View generated JSON and CSV artefacts from experiments. |
| **Entropy** | Interactive entropy and Zipf distribution visualiser. |
| **Signs** | Browse the sign dictionary for the active script. |
| **Hypotheses** | Create, track, and annotate research hypotheses. |
| **Notebooks** | Research notes and saved Glossa AI session summaries. |
| **Jobs** | Background job queue with progress and expandable result viewer. |
| **Status** | Live system health metrics (CPU, RAM, GPU, DB, uptime). |
| **Settings** | API keys, LLM model selection, environment configuration. |
| **Help** | This documentation. |

---

### The Corpora Panel

The Corpora panel is the entry point for all data. It has three collapsible sections at the top followed by the corpus card list:

**Upload / import corpus** — collapsed by default. Expand to paste content, set name/type/tokenisation/direction, and upload. Supports .txt, .csv, .json.

**Browse World Language Corpus Catalogue** — expand to browse ~50 pre-curated corpora. Click **↓ Import** for any corpus with a bundled data module.

**Anchor Sets** — expand to create and manage named anchor-pair collections for use in experiments.

**Corpus cards** — one card per uploaded corpus. Click to expand. Inside each expanded card:

| Tab | What you see |
| Browse | Paginated token view with search. Right-click → copy. |
| Edit | Change name, type, direction, tokenisation, raw content. Save re-parses. |
| Stats | Entropy metrics, Zipf bar chart, Zipf sparkline, token-type breakdown. |
| N-grams | Top-N n-grams by count. Select n = 1, 2, 3, 4. |
| Concordance | KWIC search: enter a token to see its left/right context in all words. |
| AI | Ask Glossa AI to analyse, detect anomalies, or critique this corpus. |
| Compare | Side-by-side entropy metric diff against another corpus. |

---

### The Experiments Panel

All experiments are **graph experiments** — JSON-spec directed acyclic graphs. The panel shows:

- **Palette (left)** — all atomic node types grouped by category. Drag onto the canvas.
- **Graph canvas (centre)** — the experiment DAG. Draw edges from output port (right side of a node) to input port (left side).
- **Node inspector (right)** — click a node to view and edit its parameters.
- **Toolbar** — buttons to Save, Run, Clear, and toggle the palette.

Dragging an experiment from the Experiments list in the palette creates a **SubExperiment** node, embedding that experiment as a reusable subroutine.

---

### The Study Builder

Studies compose multiple experiments into a pipeline:

- **Canvas** — drag experiment-nodes from the palette onto the canvas.
- **Connections** — connect the output of one experiment to the input of the next.
- **Parallel branches** — independent branches without data dependencies execute simultaneously.
- **Run Study** button — starts all branches; results stream into the Jobs panel.

---

### Reports and Data Panels

Two separate sidebar items:

**Reports** — shows PDF and Markdown files generated by experiments. Click any entry to preview in-browser. Download button available. Sorted newest-first. Filterable by keyword.

**Data** — shows JSON and CSV artefacts from experiments. Inline JSON viewer for inspection. Download button available. Same sorting and filtering.

---

### Bottom Panel (Ctrl+J)

The bottom panel is toggled with **Ctrl+J** and has three tabs:

**Logs** — a live streaming log view from the backend. Entries are colour-coded: Green (INFO), Yellow (WARN), Red (ERROR), Grey (DEBUG). Two buttons:
- **Purge** (orange) — clears the log file on disk and reconnects the stream (shows only new entries after clearing)
- **Clear** (grey) — clears just the display without touching the file

**Jobs** — a list of queued and completed background jobs. Each row shows job ID, experiment name, status, and elapsed time. Click any row to expand the full result JSON.

**Terminal** — a command-line terminal connected to the backend environment. Useful for inspecting files, running CLI scripts, or debugging.

---

### Glossa AI Panel

Click **✨ Glossa AI** in the sidebar. The panel appears on the right side of the screen.

**Context selector** (top of the panel) — controls what background context the AI receives:

| Mode | Context provided |
| Global | General linguistics knowledge only |
| Corpus | The selected corpus content, stats, and reading direction |
| Experiment | The selected experiment spec and its most recent results |
| Study | The full study graph and results from all connected experiments |
| Research | Full LEDGER, all notebooks, all hypothesis entries, all recent results |

**Research** context provides the most integration but is slower since it loads a large context window.

**Message input** — type in the bottom text box. Press **Enter** to send, **Shift+Enter** for a new line.

**Copy** button (⏩) — copies the full conversation to the clipboard in a structured format.

**Action links** — after Glossa AI completes an action, a **View [page] →** link appears. Clicking it navigates to the relevant UI panel without closing the chat.

---

### Settings Panel

Access via **Settings** in the sidebar. Key sections:

| Setting | Description |
| LLM Provider | Choose between Ollama (local) or OpenAI API |
| Ollama Model | Select from installed local models (e.g. llama3, mistral) |
| OpenAI API Key | Enter your key for GPT-4 or GPT-3.5 access |
| Temperature | Controls AI response creativity (default: 0.3 for research tasks) |
| Max Tokens | Response length limit |
| Backend URL | Override if running backend on a non-default host or port |
    `,
  },

  // ─── 3. CORPUS MANAGEMENT ──────────────────────────────────────────────
  {
    id: "corpora",
    title: "Corpus Management",
    content: `
## Corpus Management

A corpus in Glossa Lab is a collection of sign sequences stored in the database. Each sequence corresponds to one word, inscription, or utterance depending on the writing system.

---

### Supported File Formats

#### Text format (recommended)

One sequence per line. Signs are separated by a delimiter (default: hyphen):

\`\`\`
066-069-090-112
003-069-090-112
066-069-100-073
112-003-066
\`\`\`

Signs can be numeric codes (as above), strings, or Unicode characters. The system treats each space-delimited or line-delimited unit as one token.

#### JSON format

\`\`\`json
{
  "inscriptions": [
    { "id": "INS001", "sequence": ["066", "069", "090", "112"] },
    { "id": "INS002", "sequence": ["003", "069", "090", "112"] }
  ]
}
\`\`\`

The \`id\` field is optional. Only \`sequence\` is used.

#### CSV format

One sequence per line, signs comma-separated:

\`\`\`
066,069,090,112
003,069,090,112
066,069,100,073
\`\`\`

No header row. Every row is treated as one sequence.

#### Unicode script corpora

For corpora written in native Unicode characters (Ge'ez, Hebrew, Arabic, etc.), upload a plain text file where each line is one word written in that script:

\`\`\`
ሰሙኤል
ዳዊት
ሰሎሞን
\`\`\`

The tokeniser will split each word into individual Unicode characters or space-separated syllables depending on the tokenisation mode selected.

---

### Tokenisation Modes

Choose how the uploaded content is split into tokens:

| Mode | When to use |
| **Space-separated** | Signs are separated by spaces. One word per line means each space-delimited unit is one sign. Use for standard Glossa Lab numeric-code corpora. |
| **Line-per-token** | Each line is one token. Use when every word/inscription is already a single unit with no sub-structure to split. |
| **Character-level** | Each Unicode character is one token. Use for native-script corpora (Ge'ez, Hebrew, etc.) where each character is one syllable or consonant. |

---

### Uploading a Corpus

1. Click **Corpora** in the sidebar
2. Expand **+ Upload / import corpus**
3. Fill in the fields:
   - **Name** — a descriptive label (e.g. "NW Semitic Test1")
   - **Type** — linguistic, ancient, dna, code, random, or other
   - **Reading Direction** — LTR, RTL, or Unknown (you can auto-detect later)
   - **Tokenisation** — see modes above
4. Either paste content in the text area or click **↑ Import File** to load a .txt, .csv, or .json file
5. Click **Upload**

The corpus is stored in the SQLite database and immediately available across all experiments.

---

### Reading Direction Detection (Ashraf 2018 Method)

For ancient and unknown scripts, the reading direction is not always known. Glossa Lab implements the Ashraf & Sinha (2018) positional entropy method to infer it empirically from the corpus structure.

**Theory**: In most writing systems, word-initial and word-final positions are morphologically distinct. Word-final positions tend to be occupied by a smaller, more predictable set of signs (grammatical suffixes, determinatives) than word-initial positions. This produces lower entropy at the word-final end of words.

**Method**:
1. Compute the unigram entropy H(p) at each position index across all word sequences
2. Compare H(position=0) vs H(position=−1)
3. If H(0) < H(−1): position 0 is more constrained → position 0 is word-END → **RTL reading direction**
4. If H(−1) < H(0): position −1 is more constrained → position −1 is word-END → **LTR reading direction**

**To run it**:
- Open the corpus card → **Edit** tab → click **🔍 Auto-detect**
- Or ask Glossa AI: *"Apply the Ashraf (2018) handedness method to this corpus"*

**What to expect**:

| Result | Confidence | Meaning |
| RTL, high confidence | H(0) much lower than H(−1) | Clear right-to-left signal |
| LTR, high confidence | H(−1) much lower than H(0) | Clear left-to-right signal |
| low confidence | Small difference between H(0) and H(−1) | Corpus may be too small or too noisy; need more data |

After RTL detection, all subsequent positional analyses (T/I/M profiles, anchor selection) will use reversed sequences automatically.

**Example**: The NW Semitic Test1 corpus (101 words):
- H(position=0) = 3.91 bits
- H(position=−1) = 4.52 bits
- Result: **RTL**, high confidence (H(0) is 0.61 bits lower)

After RTL correction, sign 066 changes from T-rate=0.022 (file position: word-START) to T-rate=0.967 (linguistic position: word-END) — confirming it as a word-final grammatical suffix.

---

### Corpus Statistics (Stats Tab)

Open any corpus card → **Stats** tab to see:

#### Entropy Metrics

| Metric | Formula | Interpretation |
| **H1 (bits)** | −Σ p(s) log₂ p(s) | Unigram entropy. Measures alphabet diversity. Abjad: 4.1–4.7, Syllabary: 4.7–7.5, Logographic: >7.5 |
| **H2 / H1** | H₂ / H₁ | Bigram entropy normalised by unigram. Values <1.0 indicate sequential structure (signs predict each other). |
| **Conditional H** | H(s | s_prev) | Entropy of a sign given the sign before it. Low values = strong sequential dependency. |
| **TTR** | Types / Tokens | Type-Token Ratio. High TTR = diverse vocabulary; low TTR = repetitive. For ancient scripts, TTR typically 0.10–0.30. |
| **Zipf ρ** | Pearson(log-rank, log-freq) | Measures fit to Zipf's law. Values near −1.0 indicate power-law frequency distribution (typical of natural language). |
| **Hapax count** | count(freq=1) | Number of sign types appearing exactly once. High hapax count relative to corpus size indicates data sparsity. |

#### Token-Type Breakdown

The system classifies every token in the corpus into Unicode categories:

| Category | Description |
| **Numeric codes** | Tokens that are all digits or numeric-with-dash patterns (e.g. 066, 066-069). Standard Glossa Lab format. |
| **Latin / ASCII** | Tokens consisting of Latin letters a-z or A-Z. May indicate annotations or transliterations. |
| **Non-Latin Unicode** | Tokens with non-ASCII, non-Latin characters. Typically ancient script glyphs (Ge'ez, Hebrew, Arabic). |
| **Punctuation** | Tokens consisting primarily of punctuation characters. Often noise in ancient corpora. |
| **Mixed** | Tokens that mix two or more category types. Usually indicates formatting artefacts or encoding errors. |

If more than 5% of tokens are **Mixed**, a warning banner recommends using a **TokenFilter** node to sanitize the corpus before analysis.

#### Frequency Charts

- **Token frequency bar chart**: top 30 tokens by frequency. Useful for identifying dominant signs.
- **Zipf sparkline**: log-rank vs log-frequency. A straight line indicates perfect Zipf law fit; deviation at high ranks indicates over-representation of common signs.

---

### N-gram Analysis (N-grams Tab)

N-gram analysis reveals sequential structure: which signs tend to co-occur, and in what order.

**How to use**:
1. Select n (1, 2, 3, or 4)
2. Click **Load**
3. The bar chart shows the top 30 n-grams by frequency
4. The table shows the top 50 with exact counts

**What to look for**:
- Bigrams (n=2) that appear far more than chance reveal syntactic or morphological collocations
- For syllabic scripts, common bigrams often correspond to CV-CV syllable pairs from common words
- A flat bigram distribution (all bigrams equally rare) suggests a random or encrypted corpus
- Trigrams (n=3) that repeat frequently suggest bound morphemes or common lexical items

---

### Concordance Search (Concordance Tab)

KWIC (Key Word In Context) search lets you see every occurrence of a sign in its surrounding context.

**How to use**:
1. Type a sign code (exact match, e.g. \`066\`) or a Unicode character
2. Press **Enter** or click **Search**
3. Results show: position number | left context | **match** (highlighted) | right context

**Use cases**:
- Verify that a high T-rate sign actually appears predominantly at word-end
- Find signs that systematically follow or precede a known anchor
- Identify long contexts (>3 signs) for signs you suspect carry complex semantic load

---

### Benchmark Comparison (Compare Tab)

Compare entropy metrics side-by-side between two corpora.

1. Open a corpus card → **Compare** tab
2. Select a second corpus from the dropdown
3. Click **Compare**
4. The table shows H1, H2/H1, TTR, Zipf ρ, token count, alphabet size, and hapax count for both, with a Δ column highlighting significant differences

**Use cases**:
- Compare a candidate language corpus against a cipher corpus to assess structural similarity before attempting decipherment
- Compare a clean vs sanitized version of the same corpus to verify filtering effects
- Compare a corpus against a known reference (e.g. Ge'ez vs Meroitic) to identify structural analogues

---

### Editing a Corpus (Edit Tab)

The Edit tab lets you modify any corpus attribute or replace its content:

- **Name** — rename the corpus
- **Type** — change the classification
- **Reading Direction** — change manually or click **Auto-detect**
- **Tokenisation** — change the mode used when re-parsing the content field
- **Content** — a text area showing the full corpus as raw text. Edit and click **Save** to re-tokenise and replace.
- **Import File** — replace content from a file

**Important**: clicking **Save** re-tokenises the entire content field using the selected tokenisation mode. If you change the mode without changing the content, the same raw text will be re-parsed differently.

---

### Exporting a Corpus

From the corpus card header row:

- **↓txt** — download as space-separated text (one token per line for the full corpus)
- **↓csv** — download as CSV (one row per sequence, commas between signs)
- **Copy** (⎘) — copy all tokens as a single space-separated string to the clipboard
    `,
  },

  // ─── 4. CORPUS SANITIZATION ────────────────────────────────────────────
  {
    id: "sanitization",
    title: "Corpus Sanitization",
    content: `
## Corpus Sanitization

Ancient and unknown script corpora frequently contain mixed content: punctuation marks, annotation characters, numerals, or other non-linguistic noise that will degrade statistical analysis if left in place. Sanitization removes noise before the corpus reaches the inference engine.

---

### Why Sanitization Matters

A sign-sequence corpus should ideally contain only the signs that belong to the writing system being studied. Noise tokens cause several problems:

- **Inflated alphabet size**: a corpus with 150 genuine signs but 30 punctuation tokens appears to have an alphabet of 180, shifting H1 toward the logographic range
- **Broken bigram structure**: punctuation between words creates spurious bigrams (sign → punctuation → sign) that corrupt the sequential model
- **Distorted positional profiles**: punctuation at word boundaries skews T/I/M rates, making word-final signs appear mixed and word-initial signs appear terminal
- **False anchor candidates**: a high-frequency punctuation token may rank highly in frequency lists, drawing attention away from genuinely frequent signs

**Check the Stats → Token-Type Breakdown** panel before running any experiment. If you see a significant percentage of Punctuation or Mixed tokens, sanitize first.

---

### The TokenFilter Atomic Node

The **TokenFilter** node sits between **CorpusLoader** and the downstream inference nodes in your experiment graph. It filters the token stream in place.

#### Parameters

| Parameter | Type | Default | Description |
| \`unicode_range\` | [int, int] or null | null | If set, keep only tokens whose every character falls within [start, end] (inclusive, decimal codepoints). Tokens with ANY character outside the range are removed. |
| \`blocklist\` | list of strings | [] | Explicit list of token strings to always remove, regardless of other settings. |
| \`min_frequency\` | int | 0 | Remove token types appearing fewer than this many times in the corpus. Setting to 2 removes all hapax legomena. |
| \`invert\` | bool | false | If true, the unicode_range filter is inverted: REMOVE tokens that fall within the range instead of keeping them. |

All parameters can be combined. A token is kept only if it passes ALL active filters.

---

### Unicode Ranges for Common Scripts

| Script | Unicode Range | Decimal range |
| Ethiopic (Ge'ez) | U+1200–U+137F | 4608–4991 |
| Hebrew | U+0590–U+05FF | 1424–1535 |
| Arabic | U+0600–U+06FF | 1536–1791 |
| Coptic | U+2C80–U+2CFF | 11392–11519 |
| Greek | U+0370–U+03FF | 880–1023 |
| Latin Basic | U+0041–U+007A | 65–122 |
| Syriac | U+0700–U+074F | 1792–1871 |
| Old Persian | U+103A0–U+103DF | 66464–66527 |
| Cuneiform | U+12000–U+123FF | 73728–74751 |
| Egyptian Hieroglyphs | U+13000–U+1342F | 77824–78895 |
| Linear B Syllabary | U+10000–U+1007F | 65536–65663 |
| Meroitic | U+10980–U+1099F | 67968–67999 |

For numeric-code corpora (signs written as \`066\`, \`003\`, etc.), no Unicode filter is needed — the tokens are already clean ASCII digits and hyphens.

---

### Workflow: Sanitizing a Ge'ez Corpus

The Ge'ez Genesis corpus (v1) contained 5,478 Ethiopic punctuation characters mixed with 80,221 syllabic tokens.

**Step 1**: Upload the raw corpus. Check **Stats → Token-Type Breakdown**. You will see a significant Punctuation percentage.

**Step 2**: In the Experiment Builder, create or open the relevant experiment graph.

**Step 3**: Insert a **TokenFilter** node between **CorpusLoader** and the downstream analysis nodes.

**Step 4**: In the TokenFilter node inspector, set:
- \`unicode_range = [4608, 4991]\` (Ethiopic block only)

This keeps only tokens whose characters are all in the Ethiopic Unicode block (U+1200–U+137F), removing all Ethiopic punctuation characters (U+1361 word divider, U+1362 full stop, U+1363 comma, U+1364 semicolon, U+1365 colon, U+1367 question mark).

**Step 5**: Run the experiment. The pipeline will use the filtered token stream.

**Verification**: The Ge'ez v2 corpus after filtering: 80,221 tokens (was 85,699), 209 distinct signs (was 215 including punctuation). H1 changed from 5.28 to 5.31 bits — a small shift, confirming the filtering had the expected effect.

---

### Removing Hapax Tokens

When corpus density is low (fewer than 5 tokens per sign), hapax tokens (signs appearing exactly once) contribute noise without information. Removing them concentrates the statistical signal.

**When to use \`min_frequency = 2\`**:
- Corpus has fewer than 2,000 total tokens
- Hapax count > 20% of total sign types
- You are running mapping inference (SA), not just structural analysis

**When NOT to use**:
- You are studying vocabulary diversity (TTR, hapax count are themselves metrics)
- The corpus is large enough that hapax tokens don't dominate

**Effect**: Removing hapax tokens reduces the effective alphabet size, which increases the tokens-per-sign ratio for the remaining signs. This typically improves consistency in SA inference.

---

### Using a Blocklist

The \`blocklist\` parameter is useful when you know specific tokens to exclude, regardless of their Unicode range:

- **Example**: a corpus that uses \`---\` as a word separator, \`[UNK]\` as an unknown sign marker, or numeric references like \`v.1\` embedded in the sign stream
- Set \`blocklist = ["---", "[UNK]", "v.1"]\`
- These tokens are removed wherever they appear

---

### Inverting the Unicode Range Filter

The \`invert = true\` option removes tokens that fall within the range. Use cases:

- Remove only Latin annotation characters from an otherwise Unicode corpus: set \`unicode_range = [65, 122]\` (Latin letters) with \`invert = true\`
- Remove only ASCII punctuation from a mixed corpus: set \`unicode_range = [33, 47]\` (punctuation block) with \`invert = true\`

---

### Validating the Result

After adding TokenFilter to your graph:

1. Run the experiment once with a **JSONReportWriter** output node to capture the filtered token count
2. Check that the token count decreased by the expected amount
3. Re-examine the Stats tab in the Corpora panel for the original corpus — the TokenFilter result is not persisted to the database, only used in-pipeline

To permanently store a sanitized version of a corpus:

1. Export the filtered output as JSON from the Data panel
2. Upload the filtered JSON as a new corpus with a distinct name (e.g. "Ge'ez Genesis v2 — clean")
    `,
  },

  // ─── 5. WORLD CORPUS CATALOGUE ─────────────────────────────────────────
  {
    id: "catalogue",
    title: "World Corpus Catalogue",
    content: `
## World Language Corpus Catalogue

The catalogue provides one-click access to approximately 50 pre-curated corpora spanning ancient, deciphered, modern, and undeciphered writing systems. Each entry includes metadata about script type, language family, period, approximate token count, source, and license.

---

### Opening the Catalogue

1. Click **Corpora** in the sidebar
2. Click **🌍 Browse World Language Corpus Catalogue**
3. The catalogue panel expands. Click **⟳ Refresh** if it is empty on first open.

---

### Filtering and Searching

| Filter | Description |
| **All** | Show all catalogue entries |
| **🔓 Undeciphered** | Show only scripts whose decipherment is disputed or unknown |
| **✔ Deciphered** | Show only scripts whose reading is established |

Use the **search box** to filter by language name or corpus name. The filter applies instantly as you type.

---

### Importing a Corpus

Entries with a bundled local data module show an **↓ Import** button. Click it to:

1. Load the corpus from the bundled Python data module (no download required)
2. Register it in your database
3. Update the button to **✓ Imported**

After importing, the corpus appears in your corpus list and is ready to use in experiments.

Entries without a local module show a **Source ↗** link to the public-domain origin. Download from there and upload manually.

---

### Catalogue Contents by Language Family

#### Ancient Semitic

| Name | Script | Period | Status |
| Old Hebrew Inscriptions | Abjad | 10th–6th c. BCE | Bundled |
| Ugaritic Cuneiform | Abjad | 14th–12th c. BCE | Bundled |
| Phoenician Corpus | Abjad | 11th–2nd c. BCE | Bundled |
| Classical Arabic | Abjad | 7th c. CE | Source link |
| Aramaic Inscriptions | Abjad | 9th–2nd c. BCE | Source link |

#### Ethiopian/Cushitic

| Name | Script | Period | Status |
| Ge'ez Genesis (Ethiopic) | Syllabary | 4th–14th c. CE | Bundled |
| Classical Tigrinya | Syllabary | 19th–20th c. CE | Source link |

#### Aegean

| Name | Script | Period | Status |
| Linear B (Mycenaean Greek) | Syllabary | 14th–12th c. BCE | Source link |
| Cypriot Syllabary | Syllabary | 11th–4th c. BCE | Source link |

#### Indo-European

| Name | Script | Period | Status |
| Old Persian Cuneiform | Syllabary | 6th–4th c. BCE | Bundled |
| Sanskrit Vedic Texts | Abugida | 2nd millennium BCE | Source link |
| Classical Greek | Alphabet | 5th c. BCE | Source link |
| Latin Inscriptions | Alphabet | 3rd c. BCE–5th c. CE | Source link |

#### Egyptian

| Name | Script | Period | Status |
| Coptic New Testament | Alphabet | 3rd–4th c. CE | Bundled |
| Egyptian Hieroglyphic | Logosyllabic | 3200–350 BCE | Source link |

#### East Asian

| Name | Script | Period | Status |
| Classical Chinese (Shijing) | Logographic | 11th–7th c. BCE | Source link |
| Old Chinese Oracle Bones | Logographic | 14th–11th c. BCE | Source link |

#### Modern Typological Comparators

| Name | Script | Status |
| Modern English (WSJ) | Alphabet | Bundled |
| Modern Spanish (News) | Alphabet | Source link |
| Modern Hindi (CFILT) | Abugida | Source link |
| Modern Arabic (News) | Abjad | Source link |
| Modern Japanese (Wikipedia) | Mixed syllabic | Source link |
| Modern Korean (News) | Alphabet/syllabic | Source link |
| Swahili (News) | Alphabet | Source link |
| Finnish (Parliament) | Alphabet | Source link |
| Basque (Wikipedia) | Alphabet | Source link |
| Turkish (News) | Alphabet | Source link |

#### Undeciphered Scripts

| Name | Script type | Period | Status |
| Indus Valley Script | Unknown | 2600–1900 BCE | Bundled |
| Proto-Sinaitic | Proto-abjad | 19th–15th c. BCE | Bundled |
| Meroitic Script | Unknown | 3rd c. BCE–5th c. CE | Bundled |
| Linear A (Minoan) | Syllabary? | 18th–15th c. BCE | Source link |
| Rongorongo (Easter Island) | Unknown | Pre-1860s | Source link |
| Indus Dholavira Signboard | Unknown | ~2600 BCE | Source link |
| Vinca Script | Unknown | 5400–4500 BCE | Source link |

---

### Using Imported Corpora for Language Model Building

Once a corpus is imported, it becomes available for the **CorpusLM** atomic node, which builds a language model directly from any corpus in your database without requiring a Python data module.

Use case: you want to test Indus Script decipherment against a Dravidian language model. Import a Tamil corpus from the catalogue, then in your experiment graph connect:

\`\`\`
CorpusLM (Tamil corpus) → MappingInference ← CorpusLoader (Indus Script corpus)
\`\`\`

The CorpusLM node extracts unigram and bigram frequencies from the Tamil corpus and uses them as the phonological prior for the inference engine — no Python code required.

---

### Assessing Structural Similarity

Before attempting decipherment, use the **Compare** tab on the target corpus and a candidate language corpus to assess structural similarity:

| Metric | What close values suggest |
| H1 | Similar sign inventory complexity; same writing system tier |
| H2/H1 ratio | Similar sequential structure; comparable morphology |
| TTR | Similar vocabulary richness |
| Zipf ρ | Similar sign frequency distribution shape |

Corpora that score close across all four metrics are structurally similar and are better candidates for LM transfer than those that differ significantly in H1 (which would indicate mismatched writing system types).
    `,
  },

  // ─── 6. ANCHOR SETS ────────────────────────────────────────────────────
  {
    id: "anchors",
    title: "Anchor Sets",
    content: `
## Anchor Sets

An anchor is a verified assignment of a cipher sign to a known phoneme or syllable value. Anchors encode external linguistic knowledge — from archaeology, epigraphy, or bilingual texts — that the statistical inference engine cannot derive from the corpus alone.

---

### Why Anchors Work

The Simulated Annealing (SA) inference starts from a random sign-to-phoneme assignment and converges to a local optimum. Without anchors, it finds one of many equally plausible solutions — 40–50 distinct mappings from 50 seeds is typical at 4 tokens/sign.

When you inject k verified anchors, those k assignments are fixed. The SA is now constrained to find the best mapping *consistent with those k assignments*. The constraint propagates through the bigram co-occurrence structure of the corpus: if sign A is anchored to consonant T, then signs that appear immediately before or after A in the corpus get nudged toward phonemes that precede or follow T in the language model.

**Empirical result (Ge'ez Genesis corpus, 80,221 tokens, 209 signs)**:

| Structured anchors | Free-sign accuracy | Seeds converging |
| 0 | 4.5% | 5 distinct solutions |
| 3 | 7.6% | 3 distinct solutions |
| 10 | 12.1% | 3 distinct solutions |
| 20 | 11.8% | 3 distinct solutions |

"Free-sign accuracy" = fraction of non-anchor signs correctly identified. The cluster collapse from 5 to 3 distinct solutions at k=3 is the key convergence signal.

**Random anchors (placebo control)**: accuracy remains flat (4.5%→4.7%→5.1%) and consistency does not rise, confirming that the signal above is structural, not statistical noise.

---

### Selecting Anchor Candidates

The best anchors are signs that:

1. **Have high positional constraint** (high T-rate or I-rate, indicating a specific grammatical function)
2. **Appear frequently** (low-frequency signs have noisy statistics and propagate constraints weakly)
3. **Have a known linguistic value** from external evidence (bilingual texts, iconographic context, comparative linguistics)

#### Using T/I/M Profiles to Identify Candidates

Run the **PositionalProfiler** node on your corpus (after RTL correction if needed). Look for:

- Signs with T-rate > 0.80 — dominant word-final signs. In most Semitic abjads, these are grammatical suffixes (-m, -n, -t). In syllabaries, they are suffix syllables (-u, -ti, etc.)
- Signs with I-rate > 0.80 — dominant word-initial signs. Often prefixes, determinatives, or high-frequency function words
- Signs with M-rate > 0.90 and very high frequency — core consonants or vowel carriers

**NW Semitic example (after RTL correction)**:

| Sign | T-rate | I-rate | Candidate reading | Confidence |
| 066 | 0.967 | 0.016 | M (mem, word-final -m) | High |
| 073 | 0.018 | 1.000 | ? (word-initial, unknown) | High (position), Low (value) |
| 004 | 0.220 | 0.450 | T (tet, mixed position) | High from external source |

Sign 066 is a clear word-final anchor candidate — T-rate of 0.967 across 101 words is statistically robust, and the -m suffix is well-attested in NW Semitic morphology.

---

### Creating an Anchor Set

1. Click **Corpora** in the sidebar
2. Expand **⚓ Anchor Sets**
3. Click **+ New Set**
4. Fill in:
   - **Set Name** — e.g. "Fuls NW Semitic Anchors — verified 2024"
   - **Language** (optional) — e.g. "NW Semitic"
5. Paste anchor pairs in the text area, one per line:

\`\`\`
cipher_sign  target  confidence  note
004          T       high        Fuls 2024 verified, bilingual evidence
066          M       high        T-rate 0.967, morphological suffix
208          N       high        Fuls 2024 verified, iconographic
128          L       medium      Frequency and position consistent
080          W       high        Fuls 2024 verified
003          B       low         Speculative, comparative
\`\`\`

Format per line: **cipher_sign** (space) **target** (space) **confidence** [high/medium/low] (space) **note** (optional, free text)

6. Click **Create**

---

### Confidence Levels

| Level | Colour | Use when |
| **high** | Green | Assignment comes from verified bilingual evidence, epigraphy, or cross-validated statistical result |
| **medium** | Yellow | Assignment is linguistically plausible and supported by positional or frequency data, but not independently verified |
| **low** | Red | Speculative or theoretical assignment; comparative only |

Only **high** confidence anchors should be injected into formal experiments. Medium anchors are useful for exploratory runs. Low confidence anchors should be treated as hypotheses, not inputs.

---

### Using Anchor Sets in Experiments

**Option 1: AnchorSetLoader node** (recommended)

In the Experiment Builder:
1. Add an **AnchorSetLoader** node
2. Set the \`anchor_set_id\` parameter to the ID of your anchor set (shown in the Anchor Sets panel)
3. Connect the \`anchors\` output port to the \`anchors\` input of a **MappingInference** or **AnchorInjector** node

**Option 2: AnchorInjector with inline anchors**

If you have only a small number of anchors and don't need reusability:
1. Add an **AnchorInjector** node
2. In the node inspector, enter anchors directly as a JSON dict: \`{"066": "M", "004": "T", "208": "N"}\`

---

### Anchor Amplifier Effect — Detailed Explanation

The amplifier effect refers to the fact that one anchor produces much more improvement than you would expect from naïve combinatorics.

**Naive expectation**: with 22 target phonemes and 1 anchor that fixes 1 sign, you would expect the accuracy on the remaining 21 signs to increase by 1/22 ≈ 4.5% — because you eliminated one target from consideration for the anchored sign, freeing one phoneme token in the solution.

**Observed**: a single high-quality anchor typically produces a 10–15 percentage point improvement on non-anchor signs — approximately 12× the naïve expectation.

**Why**: because the SA inference uses a language model with bigram statistics. If sign A is anchored to consonant T, then:
- All signs that co-occur frequently before A in the corpus are biased toward phonemes that precede T in the language model
- All signs that co-occur frequently after A are biased toward phonemes that follow T
- These secondary biases propagate further through the co-occurrence network

The amplifier effect is proportional to: (1) the frequency of the anchored sign (more occurrences = more co-occurrence data to propagate), (2) the specificity of the language model (a language model with strong bigram structure propagates more constraint), and (3) the linguistic coherence of the anchor (a correct anchor strengthens the model; an incorrect one distorts it).

---

### Anchor Sweep Experiments

To determine how many anchors are needed and which to prioritise, use the **AnchorConvergenceBenchmark** node. It:

1. Takes a corpus and a candidate anchor set
2. Runs the SA inference at each anchor count k = 0, 1, 2, 3, 5, 10, 20...
3. Measures StructAcc (free), Rand Acc (free), Consistency, and HCI ≥ 75% at each k
4. Returns a summary table and convergence chart

**Interpret the output**:
- Look for the k where **cluster collapse** occurs (N_distinct solutions drops significantly)
- Look for the k where **Consistency** stops rising (diminishing returns)
- The optimal anchor count is typically between cluster-collapse k and the consistency plateau k

---

### Managing Existing Anchor Sets

In the **⚓ Anchor Sets** panel, each set shows:
- Name and language
- Pair count
- Up to 8 pairs as colour-coded badges (green/yellow/red by confidence)
- A **Delete** button

To edit an existing set, delete it and recreate. (Full edit UI is on the roadmap.)
    `,
  },

  // ─── 7. EXPERIMENT BUILDER ─────────────────────────────────────────────
  {
    id: "experiments",
    title: "Experiment Builder",
    content: `
## Experiment Builder

All experiments in Glossa Lab are **graph experiments** — JSON specifications describing a directed acyclic graph (DAG) of atomic computation nodes. The Experiment Builder provides a visual canvas to compose these graphs without writing code.

---

### Architecture

**Hierarchy**:

| Level | Definition |
| Study | A graph of Experiments. Composed in the Study Builder. |
| Experiment | A graph of atomic Nodes. Composed in the Experiment Builder. |
| Atomic Node | A single, indivisible computation step implemented internally in Python. |

Users only interact with atomic nodes and experiments. The Python implementation of each atomic node is managed by the platform and is not user-visible.

**Data flow**: each node has typed input and output **ports**. Data flows left to right along edges connecting output ports to input ports. Incompatible port types are rejected.

---

### Using the Builder

1. Click **Experiments** in the sidebar
2. Click **+ New** or open an existing experiment
3. **Palette** (left) — drag nodes onto the canvas
4. **Canvas** (centre) — connect nodes by dragging from an output port to an input port
5. **Node Inspector** (right) — click a node to view and edit its parameters
6. Click **Run** — the graph executes; progress streams to the Jobs panel

---

### Port Types

| Port type | Colour | Carries |
| corpus | Blue | A token sequence corpus (list of word-lists) |
| lm | Purple | A language model (unigram + bigram frequency table) |
| anchors | Green | An anchor dict mapping sign strings to phoneme strings |
| mapping | Orange | A sign-to-phoneme mapping (inference result) |
| metrics | Teal | Numeric evaluation results |
| report | Grey | A structured report object (PDF/Markdown/JSON) |
| any | White | Passes through any data type |

Connect a **corpus** output to a **corpus** input, an **lm** output to an **lm** input, etc. The canvas highlights compatible ports in green and incompatible ports in red when you drag.

---

### Complete Node Reference

#### Corpus Loaders

**CorpusLoader**
Loads a corpus from the database by ID.

| Parameter | Type | Description |
| corpus_id | string | ID of the corpus to load (copy from the Corpora panel) |
| split | float | Fraction to use as the test split (0.0 = use all). Default 0.0 |
| seed | int | Random seed for the split. Default 42 |

Output ports: \`corpus\` (full or train split), \`test_corpus\` (test split if split > 0)

---

**CorpusLM**
Loads a corpus from the database and builds a language model from it directly. Replaces the need for a Python data module.

| Parameter | Type | Description |
| corpus_id | string | ID of the reference corpus (e.g. a Classical Hebrew corpus) |
| min_freq | int | Minimum frequency for a sign to be included in the LM. Default 1 |
| smoothing | float | Laplace smoothing factor. Default 0.01 |

Output ports: \`lm\` (the language model)

**When to use**: when you want to build a reference LM from any uploaded corpus instead of using the built-in language models. Essential for testing new language hypotheses.

---

**BuiltinLM**
Loads a pre-seeded language model from the platform's data library.

| Parameter | Type | Description |
| lm_name | string | One of: old_hebrew, geez, phoenician, meroitic, proto_sinaitic, old_persian, uniform |

Output ports: \`lm\`

The \`uniform\` LM assigns equal probability to all phonemes — useful as a control (removes all language-prior influence from the inference).

---

#### Structural Analysis

**EntropyAnalyzer**
Computes unigram and bigram entropy metrics for a corpus.

| Parameter | Type | Description |
| include_zipf | bool | Include Zipf law fit. Default true |
| include_positional | bool | Include per-position entropy profile. Default true |

Input ports: \`corpus\`
Output ports: \`metrics\` (H1, H2, H2/H1, conditional H, TTR, Zipf ρ, hapax count, positional H profile)

---

**WritingSystemClassifier**
Classifies the corpus as abjad, syllabary, or logographic based on H1 and alphabet size.

| Parameter | Type | Description |
| thresholds | object | Override default H1 thresholds. Default: {"abjad_max": 4.7, "syllabary_max": 7.5} |

Input ports: \`metrics\` (from EntropyAnalyzer)
Output ports: \`metrics\` (augmented with classification, confidence, nearest_known_system)

---

**PositionalProfiler**
Computes Terminal (T), Initial (I), and Medial (M) probability for every sign.

| Parameter | Type | Description |
| rtl | bool | If true, reverse all sequences before computing. Default false |
| min_occurrences | int | Minimum sign occurrences to include in output. Default 3 |

Input ports: \`corpus\`
Output ports: \`metrics\` (dict of sign → {T, I, M, freq})

---

#### Corpus Filters

**TokenFilter**
Filters tokens from the corpus by Unicode range, blocklist, or minimum frequency.

| Parameter | Type | Description |
| unicode_range | [int, int] | Codepoint range to keep (or remove if invert=true). Null to disable. |
| blocklist | list[str] | Token strings to always remove. |
| min_frequency | int | Remove types with fewer occurrences. Default 0 (disabled). |
| invert | bool | If true, remove tokens matching unicode_range instead of keeping. Default false. |

Input ports: \`corpus\`
Output ports: \`corpus\` (filtered)

---

#### Mapping Inference

**MappingInference**
The core SA-based sign-to-phoneme inference engine. Maps cipher signs to target phonemes by maximising the bigram log-likelihood under the language model.

| Parameter | Type | Description |
| n_seeds | int | Number of independent SA runs. Higher = better consistency, slower. Default 20 |
| n_iterations | int | SA steps per seed. Higher = better convergence per seed. Default 2000 |
| temperature_start | float | Initial SA temperature. Default 2.0 |
| temperature_end | float | Final SA temperature. Default 0.01 |
| cooling_schedule | string | "linear" or "exponential". Default "exponential" |
| target_size | int | Size of the target phoneme set. If 0, uses the LM's phoneme count. Default 0 |

Input ports: \`corpus\`, \`lm\`, \`anchors\` (optional)
Output ports: \`mapping\`, \`metrics\` (per-sign consistency, modal assignment, posterior distribution)

**GPU acceleration**: if CuPy is installed and a CUDA device is available, MappingInference automatically uses the GPU. This gives 3–10× speedup for n_seeds > 20. With GPU unavailable, it parallelises across CPU cores.

---

**AnchorInjector**
Locks specific sign assignments before inference, overriding the SA's freedom to change them.

| Parameter | Type | Description |
| anchors | object | JSON dict mapping sign strings to target phoneme strings: \`{"066": "M", "004": "T"}\` |
| confidence_filter | string | Only inject anchors with this confidence level or higher. One of: high, medium, low, all. Default "all" |

Input ports: \`corpus\`, \`lm\`, \`anchors\` (from AnchorSetLoader, overrides inline param if connected)
Output ports: passes through \`corpus\`, \`lm\`, \`anchors\` (for downstream MappingInference)

---

**AnchorSetLoader**
Loads a saved anchor set from the database.

| Parameter | Type | Description |
| anchor_set_id | string | ID of the anchor set (visible in the Anchor Sets panel) |
| confidence_filter | string | "high", "medium", "low", or "all". Default "all" |

Output ports: \`anchors\`

---

**AnchorConvergenceBenchmark**
Sweeps over a range of anchor counts and measures decipherment quality at each k.

| Parameter | Type | Description |
| anchor_counts | list[int] | Values of k to test. Default [0, 3, 10, 20] |
| n_seeds | int | Seeds per condition. Default 10 |
| n_iterations | int | SA iterations per seed. Default 2000 |
| use_positional_selection | bool | Select anchors by T/I-rate rather than frequency. Default false |

Input ports: \`corpus\`, \`lm\`, \`anchors\` (the full candidate anchor set)
Output ports: \`metrics\` (table: k, struct_acc_free, rand_acc_free, consistency, hci75, n_distinct)

---

#### Evaluation

**ConsistencyEvaluator**
Computes per-sign consistency (fraction of seeds agreeing on the modal assignment) and aggregate metrics.

Input ports: \`mapping\` (from MappingInference, must include all seed results)
Output ports: \`metrics\` (per-sign: modal_assignment, consistency, posterior_top3; aggregate: mean_consistency, hci75_fraction)

---

**AnchorAccuracyEvaluator**
Evaluates held-out anchor recovery: removes a fraction of the anchors and tests whether the SA recovers them.

| Parameter | Type | Description |
| holdout_fraction | float | Fraction of anchors to withhold during inference. Default 0.3 |
| n_trials | int | Number of holdout trials. Default 5 |

Input ports: \`corpus\`, \`lm\`, \`anchors\`
Output ports: \`metrics\` (holdout recovery rate, std dev across trials)

---

**RandomBaselineComparator**
Runs the inference on a shuffled version of the corpus (randomised sign order within words) and compares results to the real corpus.

Input ports: \`corpus\`, \`lm\`, \`mapping\`
Output ports: \`metrics\` (real_consistency, random_consistency, delta, p_value_estimate)

---

#### Reporting Nodes

**JSONReportWriter**
Writes results to a JSON file in the Data panel.

| Parameter | Type | Description |
| filename | string | Output filename (without path). Default: auto-generated with timestamp. |
| include_raw | bool | Include full per-seed raw mapping arrays. Default false. |

Input ports: \`any\` (accepts any upstream result data)
Output ports: none

---

**MarkdownReportWriter**
Writes a Markdown summary to the Reports panel.

| Parameter | Type | Description |
| title | string | Report title. Default: experiment name. |
| include_tables | bool | Include metric tables. Default true. |

Input ports: \`any\`
Output ports: none

---

**PDFReportWriter**
Generates a formatted PDF report from a user-defined template.

| Parameter | Type | Description |
| template_id | string | ID of the report template (from the Report Templates panel). If empty, uses a default layout. |
| author | string | Author name for the report header. |

Input ports: \`any\`
Output ports: none

---

#### Sub-Experiment Nodes

**SubExperiment**
Embeds a complete experiment as a reusable subroutine within the current experiment.

| Parameter | Type | Description |
| experiment_id | string | ID of the experiment to embed. |

Input ports: whatever the embedded experiment's ExperimentInput nodes declare
Output ports: whatever the embedded experiment's ExperimentOutput nodes declare

---

**ExperimentInput**
Declares a named input port for this experiment (enables it to be used as a SubExperiment).

| Parameter | Type | Description |
| port_name | string | Name of the input port. |
| port_type | string | One of: corpus, lm, anchors, mapping, metrics, any |

Output ports: the declared port (passes data in from the caller)

---

**ExperimentOutput**
Declares a named output port for this experiment.

| Parameter | Type | Description |
| port_name | string | Name of the output port. |
| port_type | string | One of: corpus, lm, anchors, mapping, metrics, any |

Input ports: the declared port (captures data to pass back to the caller)

---

### Common Graph Patterns

**Pattern 1: Basic decipherment**
\`\`\`
CorpusLoader → MappingInference ← BuiltinLM
                     ↓
              ConsistencyEvaluator → JSONReportWriter
\`\`\`

**Pattern 2: Anchored decipherment**
\`\`\`
CorpusLoader → TokenFilter → MappingInference ← CorpusLM
AnchorSetLoader ─────────────────↑
                      ↓
               ConsistencyEvaluator → MarkdownReportWriter
\`\`\`

**Pattern 3: Anchor convergence benchmark**
\`\`\`
CorpusLoader → AnchorConvergenceBenchmark ← BuiltinLM
AnchorSetLoader ───────────────────────↑
                          ↓
                    JSONReportWriter
\`\`\`

**Pattern 4: Structural + decipherment pipeline**
\`\`\`
CorpusLoader → EntropyAnalyzer → WritingSystemClassifier → JSONReportWriter
     ↓
PositionalProfiler → JSONReportWriter
     ↓
MappingInference ← BuiltinLM
     ↓
ConsistencyEvaluator → PDFReportWriter
\`\`\`

---

### Debugging Experiment Graphs

| Symptom | Likely cause | Fix |
| Node shows red border | Required input port not connected | Connect all red ports or provide inline param values |
| Job fails with "port type mismatch" | Incompatible port types connected | Check that port colours match at both ends of each edge |
| Inference produces all low consistency | LM type mismatch (e.g. abjad LM for syllabic corpus) | Use CorpusLM with an appropriate reference corpus |
| TokenFilter removes all tokens | unicode_range does not cover your script | Check the codepoint range in the Sanitization section |
| PDF report is blank | PDFReportWriter received no data | Check that at least one metrics node is connected upstream |
    `,
  },

  // ─── 8. STUDY BUILDER ──────────────────────────────────────────────────
  {
    id: "study",
    title: "Study Builder",
    content: `
## Study Builder

A Study is a higher-level graph that composes multiple Experiments into a coordinated research pipeline. Studies are used for multi-step analytical workflows where the output of one experiment feeds the next, or where multiple parallel analyses must be run and their results compared.

---

### Study vs. Experiment

| Aspect | Experiment | Study |
| Nodes | Atomic nodes (CorpusLoader, MappingInference, etc.) | Experiment nodes (references to full experiments) |
| Edges | Connect port-to-port within a single experiment | Connect experiment outputs to experiment inputs |
| Purpose | A single coherent analysis (e.g. one decipherment run) | A coordinated sequence of analyses (e.g. structural analysis → decipherment → validation) |
| Reusability | Experiments can be embedded as SubExperiment nodes in other experiments | Studies can reference any registered experiment |

---

### Creating a Study

1. Click **Studies** in the sidebar
2. Click **+ New Study**
3. Give the study a name (e.g. "NW Semitic Complete Analysis")
4. The Study Builder canvas opens

---

### Adding Experiments to the Canvas

From the **Palette** (left), drag experiment entries onto the canvas. Each experiment is represented as a node showing its name, and its declared input/output ports (if any).

Experiments that declare **ExperimentInput** and **ExperimentOutput** nodes expose explicit ports. Experiments without declared ports can still be used in studies, but they don't accept data inputs from upstream experiments — they operate independently.

---

### Connecting Experiments

Draw an edge from an experiment's **output port** to the **input port** of a downstream experiment. The port type must match.

**Example**: a "Structural Analysis" experiment outputs a \`metrics\` port. A downstream "Decipherment" experiment has an \`ExperimentInput\` of type \`metrics\` to receive the writing-system classification. Connect them.

---

### Parallel Execution

Experiments without data dependencies on each other execute **in parallel**. The runner detects the dependency graph and launches independent branches simultaneously.

**Example study graph**:

\`\`\`
Structural Analysis ──→ Writing System Classification
                                    ↓
Anchor Set Builder ──→ Anchored Decipherment ──→ PDF Report
                                    ↓
Random Baseline ──────────────→ Comparison
\`\`\`

- "Structural Analysis" and "Random Baseline" run in parallel
- "Anchored Decipherment" waits for both its inputs
- "PDF Report" waits for the decipherment and comparison outputs

---

### Running a Study

Click **Run Study** in the Study Builder toolbar. The runner:

1. Resolves the dependency graph
2. Launches independent experiments concurrently
3. Streams progress to the Jobs panel (one job entry per experiment)
4. Passes outputs from completed experiments to downstream experiments
5. Collects all generated reports and data artefacts in the Reports and Data panels

---

### Monitoring Progress

Each experiment in a running study appears as a separate entry in the **Jobs** panel:
- **Pending** (grey) — waiting for upstream dependencies
- **Running** (blue, pulsing) — currently executing
- **Completed** (green) — finished; click to view results
- **Failed** (red) — error; click to see the error message

---

### Study Results

After completion, go to **Reports** and **Data** in the sidebar. Results are tagged with the experiment name and timestamp, making it easy to identify which experiment produced which output.

To compare results across parallel branches, open the relevant artefacts and examine metrics side-by-side.

---

### Example Study: Full NW Semitic Analysis

**Experiments in the study (in dependency order)**:

1. **RTL Detection** — runs EntropyAnalyzer + PositionalProfiler on the raw corpus, outputs RTL confirmation
2. **Structural Fingerprint** — runs EntropyAnalyzer + WritingSystemClassifier
3. **Positional Profile** — runs PositionalProfiler with RTL=true (after step 1)
4. **Baseline Decipherment** — runs MappingInference with 0 anchors
5. **Anchored Decipherment** — runs MappingInference with 6 verified anchors (after step 4 to compare)
6. **Validation Suite** — runs RandomBaselineComparator (parallel with step 5)
7. **PDF Report** — runs PDFReportWriter collecting outputs from steps 2, 3, 4, 5, 6

Steps 1 and 2 run in parallel. Step 3 waits for step 1. Steps 4, 5, 6 run in parallel after step 3. Step 7 waits for steps 2, 3, 4, 5, 6.
    `,
  },

  // ─── 9. REPORTS & DATA ─────────────────────────────────────────────────
  {
    id: "reports",
    title: "Reports & Data",
    content: `
## Reports & Data

Glossa Lab separates experiment outputs into two types: human-readable formatted reports (PDFs and Markdown), and machine-readable structured artefacts (JSON and CSV). These are in two separate sidebar panels.

---

### Reports Panel

Click **Reports** in the sidebar to see all generated PDF and Markdown reports.

**List view** shows:
- Report name and timestamp
- File size
- Source experiment name
- Preview button (opens in-browser)
- Download button

**In-browser preview**: PDFs are rendered inline using the browser's PDF viewer. Markdown reports are rendered with formatting.

**Sorting**: newest-first by default. Click column headers to sort by name or size.

**Filtering**: the search box filters by report name or experiment name.

---

### Data Panel

Click **Data** in the sidebar to see all generated JSON and CSV artefacts.

**List view** shows:
- File name and timestamp
- File size
- Source experiment name
- Inline JSON viewer (for JSON files) — click to expand a tree view
- Download button

**JSON viewer**: the inline viewer renders nested JSON as an expandable/collapsible tree. Useful for inspecting detailed per-sign metrics without downloading the file.

---

### Report Types and Their Contents

#### PDF Reports (from PDFReportWriter)

A typical decipherment PDF report contains:

**Section 1: Corpus Summary**
- Total tokens, distinct signs, alphabet size
- H1, H2/H1, TTR, Zipf ρ, hapax count
- Reading direction and detection method
- Token-frequency bar chart (top 30 signs)

**Section 2: Structural Analysis**
- Writing system classification (abjad / syllabary / logographic)
- Confidence level and nearest known comparator
- Positional entropy profile (H per position across words)
- T/I/M profile for top signs (bar chart + table)

**Section 3: Mapping Inference Results**
- Per-condition table (k anchors → consistency, accuracy, HCI)
- Per-sign consistency table (top 30 by consistency)
- Modal assignment table (sign → proposed phoneme → consistency %)
- Posterior distribution for selected signs (top 3 candidates with probabilities)

**Section 4: Robustness Validation**
- Random corpus comparison (real vs shuffled corpus metrics)
- Cross-LM consistency test results (if multiple LMs were tested)
- Anchor holdout recovery rate

**Section 5: Conclusions**
- Summary narrative (auto-generated from metrics)
- Key findings
- Recommended next steps

#### Markdown Reports (from MarkdownReportWriter)

Markdown reports are shorter, plain-text summaries suitable for embedding in research notes or emails. They contain the main metric table and key findings in a readable format.

#### JSON Data (from JSONReportWriter)

Raw structured output. For a MappingInference run, the JSON contains:

\`\`\`json
{
  "experiment": "nw_semitic_decipher",
  "timestamp": "20260415T120000",
  "corpus_stats": { "tokens": 458, "signs": 78, "h1": 5.61 },
  "anchor_count": 6,
  "results": {
    "mean_consistency": 0.638,
    "hci75_fraction": 0.281,
    "per_sign": [
      {
        "sign": "066",
        "modal": "M",
        "consistency": 1.0,
        "anchored": true,
        "top3": [{"phoneme": "M", "prob": 1.0}]
      }
    ]
  }
}
\`\`\`

---

### Report Templates

User-defined report templates allow you to specify exactly which sections, data sources, and visualisations appear in your PDF reports.

**Accessing the template editor**: (available via the Reports panel header → **Manage Templates**).

A template defines a list of sections, each with:
- **Title** — the section heading
- **Data source** — which experiment output to draw from (e.g. the metrics from ConsistencyEvaluator)
- **Data key** — which field in the output to display
- **Chart type** — bar, line, table, or text
- **Include raw table** — whether to include a data table alongside the chart

The **ReportGenerator** node (in the Experiment Builder) takes a \`template_id\` parameter and generates a PDF according to the template, using upstream node outputs as data sources.

---

### Generating Reports via Glossa AI

You can generate reports by asking Glossa AI without opening the Report Builder:

> "Generate a PDF report for the last experiment run."

> "Create a Markdown summary of the NW Semitic decipherment results and save it to Reports."

> "Export the full per-sign consistency table as a CSV."

Glossa AI will dispatch the appropriate action and a **View Reports →** link will appear when the report is ready.

---

### Sharing Results

For sharing with collaborators:
1. Click **Download** on any report or data file — saves to your browser's download directory
2. For PDFs: include the full corpus metadata section so the reader has all context
3. For JSON data: the top-level \`experiment\` and \`timestamp\` fields provide provenance
4. For Markdown: copy from the in-browser preview for inclusion in emails or documents
    `,
  },

  // ─── 10. GLOSSA AI ─────────────────────────────────────────────────────
  {
    id: "glossa-ai",
    title: "Glossa AI",
    content: `
## Glossa AI

Glossa AI is an embedded AI research assistant that can run experiments, analyse corpora, propose hypotheses, and navigate the platform — all from a natural language conversation interface.

---

### Opening Glossa AI

Click **✨ Glossa AI** in the sidebar. The assistant panel opens on the right side of the screen. It persists across navigation — you can switch between panels while keeping your conversation open.

---

### Context Modes — Detailed Guide

The context selector at the top of the Glossa AI panel determines what background information is sent to the LLM alongside each message.

#### Global

**What it loads**: general knowledge about linguistics, epigraphy, ancient scripts, and the Glossa Lab platform. No specific corpus or experiment data.

**When to use**: asking general questions about methodology, statistical methods, or the platform itself.

**Example prompts**:
> "What is the Ashraf (2018) positional entropy method?"
> "Explain the difference between an abjad and a syllabary."
> "How do I add a new experiment to the platform?"

---

#### Corpus

**What it loads**: the selected corpus metadata (name, type, token count, alphabet size, reading direction, H1, TTR), plus the first 500 tokens for sampling.

**When to use**: questions specific to one corpus — interpretation, quality assessment, comparison.

**Example prompts**:
> "Is this corpus large enough for reliable mapping inference?"
> "The H1 is 5.6 bits. What writing system type does this suggest?"
> "Detect anomalies in this corpus — are there signs that appear in unusual positions?"

---

#### Experiment

**What it loads**: the selected experiment spec (all nodes and parameters) and the results of its most recent run (metrics, per-sign consistency, modal assignments).

**When to use**: interpreting experiment results, proposing parameter changes, running follow-up analyses.

**Example prompts**:
> "What does the consistency of 63.8% mean for this corpus?"
> "Which signs have consistency above 75%? Are any anchors among them?"
> "Rerun this experiment with 50 seeds instead of 20 and compare the results."

---

#### Study

**What it loads**: the selected study graph (all experiment nodes and connections) and the results of all experiments in the study's most recent run.

**When to use**: interpreting the results of a multi-step research workflow, identifying bottlenecks, proposing study modifications.

**Example prompts**:
> "Summarise the findings from all experiments in this study."
> "Which experiment in this study has the weakest results? Why?"
> "Generate a PDF report combining the outputs from all experiments in this study."

---

#### Research

**What it loads**: the full LEDGER (a record of all completed experiments, findings, and decisions), all notebook entries, all hypothesis records, recent corpus summaries, and recent results from the last 10 experiments.

**When to use**: deep research integration across multiple sessions. This is the most powerful mode but also the slowest due to the large context window.

**Example prompts**:
> "Based on all our previous work on the NW Semitic corpus, what would be the next logical experiment to run?"
> "Summarise the evolution of our anchor strategy across all sessions."
> "Have we ever tested a uniform language model against this corpus? What were the results?"

---

### Complete Action Reference

Glossa AI automatically detects when you are requesting an action and executes it. After execution, a **View [page] →** navigation link appears.

#### run_experiment

Runs a registered graph experiment by name or ID.

**Trigger phrases**:
> "Run the Fuls RTL corrected experiment."
> "Execute the NW Semitic decipherment with these anchors: 004=T, 066=M."
> "Run the anchor convergence benchmark on the Ge'ez corpus."

**What happens**: the experiment is queued as a background job. Results appear in the Jobs panel and, when complete, in Reports/Data.

---

#### run_pipeline

Queues a longer-running pipeline job.

**Trigger phrases**:
> "Run the full validation suite pipeline."
> "Queue a multi-seed run with 50 seeds."

---

#### create_hypothesis

Creates a structured hypothesis entry in the Hypotheses panel.

**Trigger phrases**:
> "Create a hypothesis: sign 066 in the NW Semitic corpus is the consonant M based on T-rate 0.967."
> "Save this as a hypothesis: the reading direction is RTL with high confidence."

**What happens**: a new hypothesis entry is created with status "Open" and a timestamp. You can track and update it in the Hypotheses panel.

---

#### create_notebook

Saves a research note to the Notebooks panel.

**Trigger phrases**:
> "Save this analysis to notebooks."
> "Create a notebook entry summarising today's findings."

---

#### open_view

Navigates to a specific UI panel.

**Trigger phrases**:
> "Show me the Reports panel."
> "Go to the Corpora view."
> "Open Settings."

---

#### acquire_corpus

Downloads and registers a corpus from a URL or a known source.

**Trigger phrases**:
> "Download the Ge'ez Genesis corpus."
> "Acquire the Linear B corpus from the catalogue."
> "Fetch the Proto-Sinaitic corpus."

---

#### execute_script

Runs a Python script or code snippet in the backend environment.

**Trigger phrases**:
> "Run this Python code: [code]"
> "Execute the analysis script."

---

#### query_corpus

Searches for a token pattern in a corpus and returns a concordance.

**Trigger phrases**:
> "Find all occurrences of sign 066 and their context."
> "Search for bigram 003-066 in the NW Semitic corpus."

---

#### summarize_session

Saves a structured summary of the current conversation to the Notebooks panel. Use this at the end of each research session.

**Trigger phrases**:
> "Summarise this session and save it to notebooks."
> "Save a session summary."

---

### Advanced Prompting Techniques

#### Be specific about which corpus, experiment, or parameter

Instead of: *"Run the decipherment"*

Use: *"Run the NW Semitic decipherment experiment on the Test1 corpus with 30 seeds and these anchors: 004=T, 066=M, 208=N"*

---

#### Chain multiple actions

> "Upload the Ge'ez clean corpus, run the structural analysis, then run the anchor convergence benchmark with the Fuls anchors, and generate a PDF report."

Glossa AI will queue each step and report progress for each.

---

#### Ask for interpretations of specific numbers

> "The consistency at k=10 anchors is 43.3% and the free-sign accuracy is 10.1%. Is this a statistically significant improvement over the baseline?"

> "Sign 073 has T-rate=0.002 and I-rate=1.000. What does this tell us about its grammatical function?"

---

#### Request comparisons

> "Compare the consistency results between the 0-anchor run and the 10-anchor run. Is the difference meaningful?"

> "How does our NW Semitic H1 of 5.6 bits compare to known syllabaries?"

---

### The LEDGER System

The LEDGER is a persistent structured log maintained by Glossa AI (in Research context) that records:

- All experiments run and their key results
- All hypotheses created and their current status
- All significant methodological decisions
- References to reports and data files

The LEDGER persists across sessions. When you open a new session in Research context, Glossa AI reads the LEDGER and can answer questions about work done in previous sessions.

**To update the LEDGER**: Glossa AI updates it automatically when you run experiments or create hypotheses. You can also ask it to record a specific observation:

> "Add to the LEDGER: we confirmed RTL reading direction for NW Semitic with high confidence using the Ashraf method on 101 words."

---

### Session Continuity

Within a session: Glossa AI maintains the full conversation in memory.

Across sessions (standard context): memory is reset when you reload the page.

Across sessions (Research context + LEDGER): the LEDGER provides cross-session continuity for experimental facts. Notebook summaries provide continuity for research narrative.

**Best practice**: at the end of each productive session:
1. Ask Glossa AI to summarise the session
2. Save to notebooks
3. Next session: open in Research context — LEDGER and notebooks are automatically loaded

---

### Limitations

- Glossa AI requires a configured LLM (set in **Settings**). Without an LLM, the panel is non-functional.
- Actions that involve backend compute (experiments, scripts) run asynchronously. The LLM submits the job; you watch progress in the Jobs panel.
- Glossa AI cannot directly read files from your local filesystem — only corpora already uploaded to the database are accessible.
- In Research context, very large LEDGERs (>100 experiments) may cause slow responses due to token limits.
    `,
  },

  // ─── 11. UNDERSTANDING RESULTS ─────────────────────────────────────────
  {
    id: "results",
    title: "Interpreting Results",
    content: `
## Interpreting Results

Understanding what the system's numerical outputs mean — and what they don't mean — is essential for drawing valid scientific conclusions from Glossa Lab experiments.

---

### Writing System Classification

The **WritingSystemClassifier** node uses H1 (unigram entropy) and alphabet size to classify the writing system tier.

| Type | H1 range | Alphabet size | Examples |
| Abjad | 4.1–4.7 bits | 22–30 signs | Hebrew, Ugaritic, Phoenician, Arabic |
| Syllabary | 4.7–7.5 bits | 40–120 signs | Linear B, Old Persian, Ge'ez, Cypriot |
| Logosyllabic | 5.0–7.0 bits | 100–600 signs | Sumerian, Egyptian hieroglyphs |
| Logographic | >7.5 bits | 400+ signs | Chinese, Mayan |
| Alphabetic | 3.5–4.5 bits | 26–50 signs | Greek, Latin, Cyrillic |

**Note**: H1 thresholds are empirical, not absolute. A small corpus of a logographic script may show lower H1 than expected if only common signs are attested. Always cross-reference with alphabet size.

**Nearest known comparator**: the classifier reports the most structurally similar known writing system. This is based on joint H1 + alphabet-size distance, not on linguistic relationship.

---

### Entropy Metrics — Full Interpretation

#### H1 — Unigram Entropy

H1 = −Σ p(s) log₂ p(s) over all distinct signs s.

H1 measures the **average information** in choosing the next sign, given only the unigram frequency distribution. High H1 = many equally probable signs; low H1 = a few signs dominate.

**Practical interpretation**:
- H1 < 4.0: extremely concentrated distribution. Likely a small abjad, or a noisy/filtered corpus.
- H1 4.1–4.7: abjad range. 22–30 signs with roughly Zipfian distribution.
- H1 4.7–7.5: syllabary range. 40–120 signs. This is where most undeciphered scripts of interest fall.
- H1 > 7.5: logographic. Very large alphabet.

#### H2/H1 — Sequential Compression Ratio

H2 = bigram entropy. H2/H1 measures how much entropy is reduced when you know the previous sign.

- H2/H1 ≈ 1.0: signs are statistically independent (no sequential structure)
- H2/H1 ≈ 0.7–0.9: moderate sequential structure (typical of abjads and syllabaries)
- H2/H1 < 0.7: strong sequential dependence (agglutinative morphology, heavily templatic languages)

**Use case**: corpora with H2/H1 < 0.85 have enough sequential structure to benefit from bigram-informed SA inference. Those near 1.0 may respond better to unigram-only LMs.

#### Conditional Entropy H(s|s_prev)

H(s|s_prev) = H2 − H1. Measures how much the previous sign reduces uncertainty about the current sign.

Low conditional H = strong predictability from context. High conditional H = context-free signs.

#### Type-Token Ratio (TTR)

TTR = distinct sign types / total tokens.

- TTR 0.01–0.05: large, well-attested corpus (typical for a full ancient-language text)
- TTR 0.10–0.30: small or fragmentary corpus
- TTR > 0.40: very sparse corpus (many hapax legomena; statistical analysis unreliable)

**Warning**: TTR above 0.40 combined with fewer than 500 total tokens indicates a corpus too small for reliable mapping inference. Results will be noisy.

#### Zipf ρ (Pearson correlation of log-rank vs log-frequency)

- ρ near −1.0: near-perfect power-law (Zipf's law). Consistent with natural language.
- ρ −0.9 to −0.7: approximate Zipf fit. Some deviation, may indicate sub-lexical structure or genre effects.
- ρ > −0.7: significant deviation from Zipf. May indicate a non-linguistic corpus, a mixed-genre compilation, or a formatted/encoded document.

Random corpora have ρ near 0.0 (flat log-rank vs log-freq curve).

---

### The Mapping Consistency Metric

**Consistency** for sign s = fraction of SA seeds that agree on the same modal assignment for s.

Consistency measures **statistical stability**, not accuracy. A sign with 95% consistency is one where almost all SA runs agree — but the agreed-upon phoneme could still be wrong.

#### Consistency Interpretation Guide

| Consistency | Signal strength | Recommended action |
| 90–100% | Very strong | High confidence in the modal assignment. Safe to propose as anchor candidate. |
| 75–89% | Strong | Likely signal. Cross-reference with positional profile and LM frequency. |
| 60–74% | Moderate | Plausible but uncertain. Do not anchor without external corroboration. |
| 40–59% | Weak | Multiple competing solutions. More data or additional anchors needed. |
| <40% | Very weak | Noise-dominated. The sign's assignment is underdetermined. |

#### Why Consistency ≠ Accuracy

At low corpus density (~4 tokens/sign), the SA runs often agree on the WRONG assignment. This happens because the frequency-rank mapping between cipher signs and language model phonemes is partially constrained by corpus statistics, but there are multiple solutions that are locally optimal.

**Empirical calibration**: at 4 tok/sign, consistency ≥ 75% predicts correct assignment in approximately 13–18% of cases — only marginally better than random guessing. At 20+ tok/sign, high consistency becomes a much better predictor of accuracy.

#### High Consistency Index (HCI ≥ 75%)

HCI = fraction of non-anchor signs with consistency ≥ 75%.

This is reported as a fraction (e.g. 0.186 = 18.6% of signs). As anchor count increases, HCI should increase because the anchors propagate constraints that stabilise neighbouring signs.

---

### Free-Sign Accuracy

**Free-sign accuracy** = fraction of non-anchor signs whose modal SA assignment matches the known correct phoneme value.

This metric is only computable when the ground truth is known — i.e. when testing on a deciphered script (like Ge'ez) or when using a synthetic cipher applied to known text.

For unknown scripts, free-sign accuracy is **not computable**. Only consistency and HCI are observable.

**Benchmark reference (Ge'ez, 209 signs, 80k tokens)**:

| k anchors | StructAcc (free) | Rand Acc (free) | Consistency |
| 0 | 12.2% | 9.3% | 35.4% |
| 3 | 9.4% | 8.1% | 41.6% |
| 10 | 10.1% | 9.3% | 43.3% |
| 20 | 10.0% | 9.7% | 44.8% |

The slight accuracy decrease from k=0 to k=3 at 2,000 SA iterations is explained by insufficient iterations to fully propagate anchor constraints. Consistency rises monotonically — the correct signal.

---

### Positional Profiles (T/I/M)

The **T-rate**, **I-rate**, and **M-rate** for each sign are computed from the corpus as follows:

For each occurrence of sign s:
- Count how many times s appears as the LAST sign in its word (position = word_length - 1 in LTR; position = 0 after RTL reversal)
- Count how many times s appears as the FIRST sign
- Count how many times s appears at any interior position

Rates are the fractions of occurrences at each position.

#### Reading Positional Profiles

| T-rate | Linguistic interpretation |
| 0.80–1.00 | Dominant word-final. In Semitic abjads: grammatical suffix (-m, -n, -t, -h). In syllabaries: suffix syllable. |
| 0.50–0.79 | Moderately terminal. Mixed function: core consonant + suffix use. |
| 0.20–0.49 | No dominant position. Appears across all positions. |
| 0.00–0.19 | Rarely terminal. Core, internal consonant or prefix. |

| I-rate | Linguistic interpretation |
| 0.80–1.00 | Dominant word-initial. Likely a prefix, determinative, or conjunction marker. |
| 0.50–0.79 | Moderately initial. High-frequency prefix + core use. |

#### Using T/I/M for Anchor Selection

1. Run PositionalProfiler with RTL=true (if RTL confirmed)
2. Sort by T-rate descending → these are word-final anchor candidates
3. Cross-reference with frequency (high-frequency word-final signs carry more bigram weight)
4. Identify signs where the linguistic function is plausible (does the target language have common word-final suffixes that would match this distribution?)

**Key insight from Ge'ez**: the top word-final signs (T-rate > 90%) are all second-order (−u vowel: ዩ, ሱ, ሉ, ኡ) and third-order (−i vowel: ቲ, ኒ, ቂ) Ethiopic syllabic forms — grammatical suffixes in Tigrinya. This confirms that T-rate > 0.85 reliably identifies grammatical suffix position.

---

### RTL Correction and Its Effects

Without RTL correction, all positional profiles are computed using file order. For a right-to-left script stored in LTR order in the file:

- What the file calls "position 0" (leftmost) is the LAST sign of the word in reading order
- What the file calls "position −1" (rightmost) is the FIRST sign of the word in reading order

After RTL correction (reverse all sequences before computing profiles):

- T-rate now measures occurrence at word-END in reading order (correct)
- I-rate now measures occurrence at word-START in reading order (correct)

**NW Semitic example**:

| Sign | File-order T-rate | RTL-corrected T-rate | Interpretation |
| 066 | 0.022 | 0.967 | Word-final suffix (mem) — only visible after RTL correction |
| 073 | 1.000 | 0.002 | Word-initial in file = word-FINAL in RTL! Not word-final at all. |

Without RTL correction, you would falsely identify sign 073 as a terminal sign and anchor it as a suffix — which would be wrong. RTL correction is essential before interpreting positional profiles for RTL scripts.

---

### The N_Distinct Metric (Cluster Collapse)

**N_distinct** = number of distinct complete sign-to-phoneme mappings produced by the SA seeds.

- High N_distinct (e.g. 5–10): the seeds found many different locally optimal solutions. The solution space is fragmented; no single solution dominates.
- Low N_distinct (e.g. 2–3): most seeds converged to the same family of solutions. This is the **cluster collapse** signal.

Cluster collapse at a small number of anchors (k=3 in the Ge'ez benchmark) indicates that the anchor constraints are sufficient to force the SA into a narrow region of the solution space. This is strong evidence that the method is working and that the solution space is being meaningfully constrained.

**N_distinct should fall** as anchor count increases. If it remains high even at k=10, consider:
1. The anchors may be incorrect (wrong phoneme assignments)
2. The language model may be mismatched (wrong script type)
3. The corpus may be too sparse to provide enough bigram constraints

---

### Known Limitations — Complete List

**1. Low corpus density (~4 tok/sign)**
Consistency does not predict accuracy at this density. The solution space is underdetermined. The correct assignment is in the top-3 candidates ~13% of the time (near random). Add anchors to improve.

**2. Frequency-dominated inference**
At 4 tok/sign, the SA primarily matches the cipher's sign frequency rank to the LM's phoneme frequency rank. Within-word sequential order is not reliably detected until you have ~10+ tok/sign.

**3. Fragmented solution space without anchors**
Without anchors, the SA finds many equally plausible complete mappings. Only consistency aggregation makes the aggregate result interpretable. A single seed result is meaningless.

**4. Language model mismatch**
Using an abjad LM (e.g. Old Hebrew) to decipher a syllabic corpus (e.g. Linear B) will produce incorrect results because the phoneme inventory, frequency distribution, and bigram structure do not match. Always match the LM type to the target script type (abjad → abjad LM, syllabary → syllabic LM).

**5. Incorrect anchor polarity**
An anchor that maps the wrong sign to the right phoneme (e.g. sign 073 → "M" when sign 066 is the actual "M") will distort the SA away from correct solutions. The anchor amplifier effect works in reverse: a wrong anchor propagates incorrect constraints.

**6. Corpus noise**
Punctuation, numerals, and foreign annotations mixed into the corpus inflate the alphabet size, distort frequency ranks, and break bigram statistics. Always sanitize before inference.

**7. Short word sequences**
For corpora with very short words (1–2 signs each), positional profiles are dominated by the word-start/end effect and bigram statistics are weak. Results are less reliable.
    `,
  },

  // ─── 12. RESEARCH WORKFLOWS ────────────────────────────────────────────
  {
    id: "workflow",
    title: "Research Workflows",
    content: `
## Research Workflows

This section provides end-to-end research workflow guides — step-by-step procedures for conducting real research with Glossa Lab.

---

### General Research Methodology

A rigorous decipherment study in Glossa Lab follows this sequence:

**Phase 1: Corpus Preparation**
1. Upload the cipher corpus
2. Check token count, alphabet size, TTR — assess feasibility
3. Run reading direction detection (Ashraf method)
4. Inspect token-type breakdown — sanitize if needed
5. Upload or select a reference language corpus (for LM)

**Phase 2: Structural Analysis**
1. Run EntropyAnalyzer to determine H1, H2/H1, TTR, Zipf ρ
2. Run WritingSystemClassifier — confirm tier (abjad/syllabary/logographic)
3. Run PositionalProfiler (with RTL=true if applicable)
4. Identify high-T and high-I signs as anchor candidates

**Phase 3: Baseline Inference**
1. Run MappingInference with 0 anchors, 20 seeds
2. Record mean consistency, HCI ≥ 75%, N_distinct
3. Run RandomBaselineComparator to confirm the corpus has a real statistical signal above noise

**Phase 4: Anchored Inference**
1. Create an anchor set with verified assignments (start with the 3–5 highest-confidence anchors)
2. Run MappingInference with anchors
3. Compare: consistency increase, HCI increase, N_distinct decrease
4. If N_distinct decreases significantly (cluster collapse): anchors are working
5. If no improvement: suspect incorrect anchors or LM mismatch

**Phase 5: Validation**
1. Run AnchorAccuracyEvaluator with holdout to estimate recovery rate
2. Run AnchorConvergenceBenchmark across k = 0, 3, 10, 20
3. Test with a different LM (BuiltinLM "uniform") as a control
4. Compare results across LMs — genuine signal should persist

**Phase 6: Reporting**
1. Generate PDF report via PDFReportWriter
2. Export per-sign JSON for detailed review
3. Save session summary to notebooks via Glossa AI

---

### NW Semitic Analysis — Full Case Study

This walkthrough replicates the complete analysis conducted for Dr. Andreas Fuls (TU Berlin) using a 101-inscription NW Semitic syllabic corpus.

#### 1. Corpus Upload and Assessment

Upload the corpus as a text file, one inscription per line, signs separated by hyphens.

Stats tab results:
- 458 total tokens
- 78 distinct signs (H1 = 5.61 bits)
- TTR = 0.17
- Zipf ρ = −0.94

Writing system classification: **SYLLABIC** (H1 = 5.61 bits, alphabet = 78), nearest comparator: Linear B (Mycenaean Greek, H1 = 5.58).

#### 2. Reading Direction Detection

Running the Ashraf method:
- H(position=0) = 3.91 bits
- H(position=−1) = 4.52 bits
- H(0) < H(−1) → **RTL**, high confidence

Conclusion: the corpus is a right-to-left script. All subsequent analysis uses RTL-corrected (reversed) sequences.

#### 3. Positional Profile Analysis (RTL-corrected)

Top terminal signs after RTL correction:

| Sign | T-rate | I-rate | Freq | Anchor priority |
| 066 | 0.967 | 0.016 | 82 | HIGH — word-final suffix |
| 073 | 0.005 | 1.000 | 45 | HIGH — word-initial |
| 112 | 0.002 | 0.987 | 38 | HIGH — word-initial |
| 004 | 0.22 | 0.45 | 31 | MEDIUM — mixed, external source |
| 208 | 0.43 | 0.21 | 28 | MEDIUM — confirmed by Fuls |

Sign 066 at T-rate 0.967 is an exceptional anchor candidate: it appears at word-end in 97% of its 82 occurrences. In NW Semitic morphology, the dominant word-final consonant is mem (-m), the enclitic conjunction or accusative marker.

#### 4. Baseline Decipherment (No Anchors)

MappingInference with 20 seeds, 2000 iterations, Old Hebrew LM:
- Mean consistency: 54.7%
- HCI ≥ 75%: 11 of 78 signs (14.1%)
- N_distinct: 7 distinct solutions

Baseline is above noise (random corpus gives mean consistency 35–40% for this corpus size).

#### 5. Anchored Decipherment (6 Fuls Anchors)

Anchors: 004=T, 066=M, 208=N, 128=L, 080=W, 003=B (all high confidence, from Fuls 2024 verified set)

MappingInference results:
- Mean consistency: **63.8%** (+9.2 pp vs baseline)
- HCI ≥ 75%: **22 of 78 signs** (28.2%, up from 14.1%)
- N_distinct: **3** (down from 7 — cluster collapse)

All 6 anchor signs lock to 100% consistency as expected.

#### 6. Robustness Checks

**Random corpus test**: shuffled version of the same corpus (randomise sign order within each word) gives mean consistency 38.2%. Real corpus is 25 pp above random — statistically significant.

**Cross-LM test**: running with Blended NW Semitic LM instead of Old Hebrew:
- Mean consistency: 61.1% (still above baseline; −2.7 pp vs Old Hebrew LM)
- HCI ≥ 75%: 19 of 78 signs

The signal persists across LMs, confirming it is driven by corpus structure, not LM overfitting.

**Sequence information test**: running with unigram-only LM (bigram weight = 0):
- Mean consistency: 51.2% (−2.5 pp vs baseline)
- This small decrease confirms that sequential structure is present but modest at 4 tok/sign

#### 7. Key Findings

1. The corpus is a **syllabic writing system** (H1 = 5.61 bits, 78 signs, nearest: Linear B)
2. Reading direction is **RTL** with high confidence (Ashraf method, Δ = 0.61 bits)
3. Six verified anchor assignments improve mean consistency by 9.2 pp and double the high-confidence sign count
4. Cluster collapse from 7 to 3 distinct solutions confirms that the anchors are constraining the solution space appropriately
5. The signal persists across LMs and significantly exceeds the random baseline

---

### Ge'ez Benchmark — Validation Case Study

The Ge'ez Genesis corpus provides a **known-ground-truth** benchmark for testing the anchor convergence hypothesis, since Ge'ez is a fully deciphered syllabic script.

**Setup**:
- Ge'ez Genesis corpus: 80,221 tokens, 209 distinct signs
- Apply a random bijective cipher substitution to create a synthetic "unknown" script
- Run inference on the ciphered corpus and measure how often we recover the correct syllable values

**Key results**:

| k | StructAcc (free) | Rand Acc (free) | Consistency | N_distinct |
| 0 | 12.2% | 9.3% | 35.4% | 5 |
| 3 | 9.4% | 8.1% | 41.6% | 3 |
| 10 | 10.1% | 9.3% | 43.3% | 3 |
| 20 | 10.0% | 9.7% | 44.8% | 3 |

**Conclusion**: structured anchor injection drives convergence (N_distinct: 5→3 at k=3, cluster collapse). Consistency rises monotonically. Random anchors (placebo) produce no consistent improvement. The method works when the corpus is sufficient in size (>100 tok/sign) and the LM matches the script type.

---

### Adapting to New Scripts

When starting an analysis of a new, unknown script:

**Step 1**: Upload all available inscriptions. Note the total token count and alphabet size.

**Step 2**: If total tokens < 300, the statistical basis is too thin for reliable inference. Focus on structural analysis only (H1, Zipf, TTR). Mapping inference results will be noise-dominated.

**Step 3**: Run the Ashraf reading direction test. If confidence is low (small H difference), the corpus may be too short or the script may be consistently bidirectional.

**Step 4**: Test multiple LMs. Use BuiltinLM with old_hebrew, geez, and uniform. Compare which LM produces the highest consistency with the real corpus vs a random corpus. The best LM is a clue about the target language family.

**Step 5**: Identify anchor candidates from positional profiles. Do not anchor based on speculative linguistic comparisons alone. Only anchor from strong positional evidence combined with external archaeological or comparative evidence.

**Step 6**: Run the anchor convergence benchmark. Look for cluster collapse at k=3–5 structured anchors. If you don't see it, the anchors may be wrong, or the corpus may be too small.
    `,
  },

  // ─── 13. TROUBLESHOOTING ───────────────────────────────────────────────
  {
    id: "troubleshooting",
    title: "Troubleshooting",
    content: `
## Troubleshooting

---

### Backend Issues

| Issue | Cause | Solution |
| Backend does not start | Port 8001 is already in use | Right-click tray icon → Change Port. Or kill the conflicting process: \`netstat -ano | findstr :8001\` (Windows) |
| Backend starts but UI shows "offline" | Backend started on a different port than the UI is connecting to | Check the tray icon for the current port. Navigate to \`http://localhost:<port>\` |
| Backend crashes on startup | Missing Python dependency | Run \`setup-os.cmd install\` to reinstall dependencies |
| Backend crashes after a few minutes | Memory exhaustion (large GPU inference) | Reduce n_seeds in MappingInference, or use CPU mode |
| "Address already in use" error | A previous backend instance did not exit cleanly | Kill all Python processes with \`setup-os.cmd stop\` then restart |
| "Database locked" error | Two backend instances running simultaneously | Stop all instances, then start one: \`setup-os.cmd stop && setup-os.cmd start\` |
| Backend won't stop | Process is stuck | Windows: open Task Manager → Python processes → End Task. Linux/macOS: \`pkill -f glossa_lab\` |

---

### Frontend / UI Issues

| Issue | Cause | Solution |
| Blank white screen | Frontend failed to load (bundle error) | Hard-reload the page (Ctrl+Shift+R). Check browser console for errors. |
| Sidebar items missing | UI state error | Reload the page |
| "Failed to fetch" errors | Backend is not running or is on a different port | Check the tray icon. Verify backend is running with \`setup-os.cmd status\` |
| Experiments list empty | No graph experiments loaded | Click ⟳ Refresh in the Experiments panel |
| Reports panel empty | No experiments have been run yet | Run at least one experiment with a report-writing node |
| Glossa AI panel won't open | LLM not configured | Go to Settings → configure Ollama or OpenAI API key |
| Glossa AI shows "Connection error" | LLM provider is unavailable | Check that Ollama is running (\`ollama list\`) or that the API key is valid |
| Tables in Help show blank rows | (Fixed in current version) | Clear browser cache with Ctrl+Shift+Delete |

---

### Corpus Issues

| Issue | Cause | Solution |
| Upload fails with "Encoding error" | File is not UTF-8 | Convert the file: on Windows, open in Notepad → Save As → Encoding: UTF-8 |
| Upload fails with "Empty content" | Tokenisation mode mismatch | Try a different tokenisation mode. "Line-per-token" with a space-separated file creates a single token. |
| Corpus appears with 0 tokens | Tokeniser found no valid tokens | Check that the content matches the selected tokenisation mode |
| Stats tab shows "Computing metrics…" indefinitely | Very large corpus | Wait longer. Corpora > 100,000 tokens may take 30–60 seconds |
| Token-type breakdown shows 100% Mixed | Non-standard characters in token codes | The tokens may use characters not in standard ASCII or a known Unicode block. Check the Edit tab for raw content. |
| World catalogue import fails | Local module not found | The catalogue entry may have an outdated module reference. Use the Source ↗ link to download manually. |
| Reading direction detection returns "low confidence" | Corpus is too small or characters are bidirectional | Need at least 50 words for reliable detection. Results below 50 words are indicative only. |

---

### Experiment Issues

| Issue | Cause | Solution |
| Experiment fails immediately | Missing required parameter | Open the Node Inspector for all nodes and check that required parameters are set |
| "Port type mismatch" error | Incompatible nodes connected | Check port colours match at both ends of each edge. See port type table in the Experiment Builder section. |
| Experiment runs but produces no output | Report writer node not connected | Add a JSONReportWriter or MarkdownReportWriter node and connect it to the last metrics node |
| MappingInference produces all low consistency | LM type mismatch | Switch to CorpusLM using an appropriate reference corpus, or try BuiltinLM "uniform" as a diagnostic |
| TokenFilter removes all tokens | unicode_range too narrow | Check the codepoint range for your script. Use the Stats → Token-Type Breakdown before filtering. |
| SubExperiment node shows "ports not found" | Referenced experiment has no ExperimentInput/Output nodes | Add ExperimentInput and ExperimentOutput nodes to the referenced experiment |
| AnchorSetLoader error "set not found" | Wrong anchor_set_id | Copy the anchor set ID from the Anchor Sets panel in Corpora |
| SA inference is very slow | Running on CPU with many seeds | Install CuPy for GPU acceleration. Reduce n_seeds as a temporary measure. |
| Results are identical across all runs | SA is not exploring (stuck in single optimum) | Increase temperature_start parameter in MappingInference (try 3.0 or 5.0) |

---

### GPU Issues

| Issue | Cause | Solution |
| "No GPU available, using CPU" | CuPy not installed | Run: \`pip install cupy-cuda12x\` (for CUDA 12.x) or \`cupy-cuda11x\` for CUDA 11.x |
| CuPy installed but GPU not used | CuPy cannot find CUDA | Run \`python -c "import cupy; print(cupy.cuda.is_available())"\`. If False, CUDA drivers may be missing or wrong version. |
| GPU out of memory | Corpus + LM too large for VRAM | Reduce n_seeds or n_iterations. Or set a smaller target_size parameter. |
| GPU causes different results from CPU | Floating-point precision differences | Expected and normal. Results should be statistically equivalent. |
| CUDA out of memory error | Many parallel seeds | Reduce n_seeds to a value that fits in VRAM (typically 10–20 for 8 GB VRAM) |

---

### Log Panel Issues

| Issue | Cause | Solution |
| Logs show stale old entries on reload | Log file was not purged | Click **Purge** (orange) to clear the log file and reconnect the stream |
| Logs not streaming (no new entries) | EventSource connection dropped | Click **Purge** — this disconnects and reconnects the stream |
| Logs show red ERROR entries | Backend exception | Expand the error entry. Common causes: missing corpus ID, LM load failure, disk full |
| Logs show garbled characters | Log file has non-UTF-8 content | Click **Purge** to reset the log file |
| "Purge failed" message | Log file is locked by another process | Restart the backend to release the log file lock |

---

### Performance Troubleshooting

| Symptom | Likely cause | Recommended action |
| Stats tab slow to load | Large corpus (>50k tokens) | Normal; wait up to 60 seconds |
| Experiment takes hours | Running 50+ seeds on CPU | Install CuPy for GPU, or reduce n_seeds |
| Job queue grows but jobs don't complete | Backend is single-threaded and a large job is blocking | Wait for the current job to complete. Only one compute job runs at a time. |
| Frontend freezes when expanding concordance | Too many concordance results | Search for a more specific token to reduce result count |
| Browser tab crashes | Memory exhausted by large JSON viewer | Download the JSON file instead of viewing inline |

---

### Log Level Reference

| Colour | Level | Meaning |
| Green | INFO | Normal operation messages: startup, corpus loaded, job started |
| Yellow | WARNING | Non-fatal issues: slow performance, minor data problems |
| Red | ERROR | Failures: exceptions, job errors, connection failures |
| Grey | DEBUG | Detailed diagnostic messages (only visible in debug mode) |

---

### Diagnostic Procedure

If you encounter an unexpected failure:

1. Open the **Logs** panel (Ctrl+J)
2. Look for the most recent RED (ERROR) entry
3. The error message will usually identify: the failing component, the error type, and often the cause
4. Check the **Jobs** panel — click the failed job to see the full stack trace
5. If the error is a Python exception, the last line of the traceback identifies the exact location and reason
6. Common patterns:
   - \`corpus_id not found\`: check that the corpus ID in CorpusLoader matches an existing corpus
   - \`LM not found\`: BuiltinLM name is misspelled; check valid names in the node reference
   - \`JSONDecodeError\`: a node parameter is malformed JSON; check the Node Inspector
   - \`CUDA out of memory\`: reduce n_seeds or n_iterations in MappingInference
    `,
  },
];

// ---------------------------------------------------------------------------
// Renderer
// ---------------------------------------------------------------------------

function renderSection(content: string): string {
  // Step 1: HTML-escape raw content
  let html = content
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Step 2: Protect fenced code blocks with placeholders so they survive
  //         subsequent transforms intact.
  const codeBlocks: string[] = [];
  html = html.replace(/```[\w]*\n?([\s\S]*?)```/g, (_, code) => {
    const idx = codeBlocks.length;
    codeBlocks.push(
      `<pre style='background:#1e293b;color:#e2e8f0;padding:10px 14px;border-radius:6px;font-size:11px;overflow-x:auto;margin:8px 0;line-height:1.6;white-space:pre'>${code}</pre>`
    );
    return `\x02${idx}\x03`;
  });

  // Step 3: Process tables as COMPLETE BLOCKS before any newline→<br>
  //         conversion. Walk line by line; whenever we see consecutive
  //         pipe-delimited lines, consume the entire block at once and emit
  //         a single <table> element. This prevents <br> from leaking
  //         between <tr> elements.
  const lines = html.split("\n");
  const processed: string[] = [];
  let i = 0;
  while (i < lines.length) {
    const t = lines[i].trim();
    if (t.startsWith("|") && t.endsWith("|")) {
      // Collect all consecutive table lines
      const tableLines: string[] = [];
      while (i < lines.length) {
        const tl = lines[i].trim();
        if (tl.startsWith("|") && tl.endsWith("|")) {
          tableLines.push(lines[i]);
          i++;
        } else {
          break;
        }
      }
      // Filter out separator rows (|---|---| etc.)
      const dataRows = tableLines.filter(
        (row) => !/^\s*\|[\s\-:|]+\|\s*$/.test(row)
      );
      // Build the HTML table
      const tableHtml = dataRows
        .map((row, idx) => {
          const cells = row
            .split("|")
            .slice(1, -1)
            .map((c) => c.trim());
          const isHeader = idx === 0;
          const tdStyle = isHeader
            ? "padding:6px 12px;border:1px solid #cbd5e1;font-size:12px;font-weight:700;background:#f0f4f8;color:#1e3a5f;vertical-align:top"
            : "padding:6px 12px;border:1px solid #e5e7eb;font-size:12px;vertical-align:top";
          return `<tr>${cells
            .map((c) => `<td style='${tdStyle}'>${c}</td>`)
            .join("")}</tr>`;
        })
        .join("");
      processed.push(
        `<div style='overflow-x:auto;margin:10px 0'><table style='border-collapse:collapse;font-size:12px;width:100%;border:1px solid #e5e7eb'>${tableHtml}</table></div>`
      );
    } else {
      processed.push(lines[i]);
      i++;
    }
  }
  html = processed.join("\n");

  // Step 4: Apply remaining inline markdown transforms
  html = html
    .replace(
      /`([^`]+)`/g,
      "<code style='background:#f1f5f9;padding:1px 5px;border-radius:3px;font-size:11px;font-family:monospace;color:#0f4c75'>$1</code>"
    )
    .replace(
      /^## (.+)$/gm,
      "<h2 style='font-size:16px;font-weight:700;margin:20px 0 8px;color:#1e3a5f;border-bottom:2px solid #e5e7eb;padding-bottom:6px'>$1</h2>"
    )
    .replace(
      /^### (.+)$/gm,
      "<h3 style='font-size:13px;font-weight:700;margin:16px 0 5px;color:#0f766e'>$1</h3>"
    )
    .replace(
      /^#### (.+)$/gm,
      "<h4 style='font-size:12px;font-weight:700;margin:12px 0 4px;color:#374151'>$1</h4>"
    )
    .replace(/\*\*([^*]+)\*\*/g, "<strong>$1</strong>")
    .replace(/\*([^*]+)\*/g, "<em>$1</em>")
    .replace(
      /^---$/gm,
      "<hr style='border:none;border-top:1px solid #e5e7eb;margin:16px 0'>"
    )
    .replace(
      /^> (.+)$/gm,
      "<blockquote style='border-left:3px solid #0f766e;padding:4px 12px;margin:8px 0;background:#f0fdf4;color:#1e4a3a;font-style:italic'>$1</blockquote>"
    )
    .replace(
      /^[-*] (.+)$/gm,
      "<li style='margin:4px 0;margin-left:20px;list-style-type:disc'>$1</li>"
    )
    .replace(
      /^\d+\. (.+)$/gm,
      "<li style='margin:4px 0;margin-left:20px;list-style-type:decimal'>$1</li>"
    )
    .replace(/\n\n/g, "</p><p style='margin:8px 0'>")
    .replace(/\n/g, "<br>")
    .replace(/^/, "<p style='margin:0'>")
    .replace(/$/, "</p>");

  // Step 5: Restore code block placeholders
  html = html.replace(/\x02(\d+)\x03/g, (_, idx) => codeBlocks[+idx]);

  return html;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export function HelpView() {
  const [activeId, setActiveId] = useState("quickstart");
  const section =
    MANUAL_SECTIONS.find((s) => s.id === activeId) ?? MANUAL_SECTIONS[0];

  return (
    <div
      style={{
        display: "flex",
        height: "100%",
        overflow: "hidden",
        fontFamily: "system-ui, sans-serif",
      }}
    >
      {/* Sidebar */}
      <div
        style={{
          width: 190,
          background: "#f8fafc",
          borderRight: "1px solid #e5e7eb",
          display: "flex",
          flexDirection: "column",
          flexShrink: 0,
          overflowY: "auto",
        }}
      >
        <div
          style={{
            padding: "12px 14px 8px",
            borderBottom: "1px solid #e5e7eb",
          }}
        >
          <div style={{ fontSize: 13, fontWeight: 700, color: "#1e3a5f" }}>
            📘 Help
          </div>
          <div style={{ fontSize: 10, color: "#9ca3af" }}>Glossa Lab v1.0</div>
        </div>
        {MANUAL_SECTIONS.map((s) => (
          <button
            key={s.id}
            onClick={() => setActiveId(s.id)}
            style={{
              display: "block",
              width: "100%",
              textAlign: "left",
              padding: "8px 14px",
              border: "none",
              fontSize: 12,
              background: activeId === s.id ? "#eff6ff" : "none",
              color: activeId === s.id ? "#1d4ed8" : "#374151",
              fontWeight: activeId === s.id ? 600 : 400,
              borderLeft:
                activeId === s.id
                  ? "3px solid #1d4ed8"
                  : "3px solid transparent",
              cursor: "pointer",
              lineHeight: 1.4,
            }}
          >
            {s.title}
          </button>
        ))}
        <div style={{ flex: 1 }} />
        <div
          style={{
            padding: "8px 14px",
            fontSize: 10,
            color: "#9ca3af",
            borderTop: "1px solid #e5e7eb",
          }}
        >
          <div>
            Full docs:{" "}
            <code style={{ fontSize: 9 }}>docs/user-manual.md</code>
          </div>
        </div>
      </div>

      {/* Content */}
      <div style={{ flex: 1, overflowY: "auto", padding: "20px 32px" }}>
        <div
          style={{
            maxWidth: 820,
            fontSize: 13,
            lineHeight: 1.75,
            color: "#111827",
          }}
          dangerouslySetInnerHTML={{ __html: renderSection(section.content) }}
        />
      </div>
    </div>
  );
}
