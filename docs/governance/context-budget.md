# Context Budget

## Context Window Management

Large governance files consume agent context rapidly. Agents MUST actively manage context window consumption.

### On session load:

* Read AGENTS.md in full (rules are authoritative, no shortcuts)
* Read only the **last ~300 lines** of LEDGER.md (recent entries + next-session block)
* Read only the **first ~200 lines** of docs/REQUIREMENTS.md and docs/TEST_SPEC.md (TOC + active items)
* Read docs/architecture.md by section header only (~first 40 lines) unless a specific section is task-relevant
* Older ledger entries and deep doc sections are loaded only when explicitly needed

### During a session:

* NEVER re-read a file already in context unless it has been modified since the last read
* Use line ranges for all reads of files longer than ~200 lines
* Prefer grep or semantic search over reading entire files when looking for specific content
* Batch file reads into a single call rather than sequential calls
* Keep responses concise — summarize rather than echoing large file contents
* Do not repeat plan or proposal contents after creating them
* After multi-step tasks, give a brief summary (2–4 sentences) rather than recapping every file

### File size guidelines (approximate):

* AGENTS.md: ~200–500 lines — read in full
* LEDGER.md: grows unbounded — read last ~300 lines
* docs/REQUIREMENTS.md: ~100–400 lines — read first ~200
* docs/TEST_SPEC.md: ~100–600 lines — read first ~200
* docs/architecture.md: ~100–400 lines — read first ~40, expand by section

Treat context window exhaustion as a **preventable defect**.

---

