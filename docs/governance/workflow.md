# Workflow

## Required: Ledger.Md

A file named `LEDGER.md` MUST exist at repo root.

### Rules

- Every meaningful task MUST be recorded
- Every session MUST append an entry
- All TODOs MUST live in the ledger
- No work is considered complete without a ledger entry

### Entry format

```md

## Session Lifecycle

Agents MUST follow structured session flows.

### Session boundary rules

- A new conversation is a new session, NOT a new project.
- All governance rules in AGENTS.md persist across sessions and conversations.
- Agents MUST NOT reset or ignore project rules across conversation boundaries.
- Past chat messages from previous conversations are not available; agents MUST rely on on-disk documents (ledger, requirements, tests, architecture) as the source of truth for continuity.
- LEDGER.md is the ONLY authoritative source for session continuity. Do NOT create `NEXT_SESSION.md`, `STATUS.md`, `SESSION_SUMMARY.md`, or similar files — all continuity lives in the ledger.

### Conversation summarization recovery

Whenever the conversation is optimized, summarized, or truncated by the platform (e.g. a "CONVERSATION SUMMARY" block is inserted), agents MUST **immediately re-read AGENTS.md in full** before performing ANY further actions. Summarization loses nuance from project rules; the only way to restore it is to re-read the authoritative source. **No exceptions.**

---

## 🔵 New Session Prompt

When starting fresh:

```text
Load AGENTS.md, README.md, docs/architecture.md, docs/workflow.md, docs/services.md, and LEDGER.md.

Output:
1. Current system understanding
2. Current known state from ledger
3. Open TODOs
4. Suggested next task

Then produce a Proposal.
```

---

## 🟡 Resume Session Prompt

```text
Load AGENTS.md and LEDGER.md.

Summarize:
- last completed task
- current objective
- open TODOs
- risks

Then propose next bounded task.
```

---

## 🟢 Save Session Prompt

```text
Prepare LEDGER.md entry for this session.

Include:
- what changed
- what was verified
- what remains incomplete
- next recommended step

Do not invent results.
```

---

## 🔴 Git Commit Prompt

```text
Prepare commit summary:

- what changed
- why
- files touched
- checks performed

Generate commit message.

Then list commands to run:
git add .
git commit -m "<message>"
git push
```

---

## 🔵 Git Update Prompt

```text
Update local repo safely:

1. git status
2. git pull
3. summarize changes
4. identify conflicts or risks
```

---

## Quick Commands

Agents should use these short commands:

| Command  | Meaning             |
| -------- | ------------------- |
| `start`  | new session         |
| `resume` | resume from ledger  |
| `save`   | write ledger entry  |
| `commit` | prepare git commit  |
| `sync`   | pull latest changes |

---

