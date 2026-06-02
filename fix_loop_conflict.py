"""Resolve Phase E merge conflicts in research_loop.py and ResearchLoopPanel.tsx."""
import re

# ── research_loop.py ─────────────────────────────────────────────────────
path_rl = "backend/glossa_lab/api/research_loop.py"
with open(path_rl, encoding="utf-8") as f:
    content = f.read()

if "<<<<<<< HEAD" in content:
    # The conflict is about how to count cycles and track last_experiment.
    # HEAD: simple increment + track last_experiment
    # Loop: smarter — only count on node_complete/cycle entries, stream others directly.
    # Resolution: use Loop's approach but also track last_experiment from HEAD.
    def resolve_rl(m):
        return (
            "              # Phase E: intermediate SSE events (proposal, build, verify,\n"
            "              # analysis, timeout, gap_skipped) are streamed directly.\n"
            "              # Only persist + increment on node_complete / cycle entries.\n"
            "              entry_type = entry.get(\"type\", \"\")\n"
            "              is_cycle = entry_type in (\"node_complete\", \"\") and entry.get(\"cycle\")\n"
            "              if is_cycle:\n"
            "                  cycles_done += 1\n"
            "              last_experiment = entry.get(\"experiment\", last_experiment)\n"
        )

    content = re.sub(
        r"<<<<<<< HEAD.*?>>>>>>> overhaul/loop\n",
        resolve_rl,
        content,
        flags=re.DOTALL,
    )
    with open(path_rl, "w", encoding="utf-8") as f:
        f.write(content)
    print("research_loop.py conflict resolved.")
else:
    print("research_loop.py: no conflict markers.")

# ── ResearchLoopPanel.tsx ────────────────────────────────────────────────
path_rp = "frontend/src/components/ResearchLoopPanel.tsx"
with open(path_rp, encoding="utf-8") as f:
    content = f.read()

if "<<<<<<< HEAD" not in content:
    print("ResearchLoopPanel.tsx: no conflict markers.")
else:
    # Block 1: CycleEntry type fields — keep all from both sides
    def resolve_type_block(m):
        return (
            "                  reason?: string; cycles_completed?: number;\n"
            "                  last_experiment?: string; elapsed_seconds?: number;\n"
            "                  experiment?: string; rationale?: string;\n"
            "                  summary?: string; flags?: string[];\n"
            "                  ok?: boolean; timeout_seconds?: number; gap_targeted?: string;\n"
        )

    content = re.sub(
        r"<<<<<<< HEAD\n(\s+reason\?.*?elapsed_seconds.*?)\n=======\n(.*?)>>>>>>> overhaul/loop\n",
        resolve_type_block,
        content,
        count=1,
        flags=re.DOTALL,
    )

    # Block 2: SSE event handler — keep both error handler (HEAD) AND new event types (loop)
    # Find the second conflict block
    def resolve_event_block(m):
        head_part = m.group(1)
        loop_part = m.group(2)
        # head_part contains the error event handler
        # loop_part contains proposal_selected, build_complete, etc. + node_complete handler
        # We want: loop_part's new event handlers, THEN head_part's error handler inserted in the right place,
        # THEN loop_part's final node_complete handler.
        # Actually, let's parse: head_part ends with setFailureDetail block.
        # loop_part contains all the new events plus the final `node_complete` log line.
        # Strategy: insert head_part's error block into loop_part where it fits (after gap_skipped).
        combined = loop_part
        # Find where to insert the error handler (before the final node_complete block)
        error_handler = head_part.strip()
        # Insert head error handling before the closing part of loop
        if "node_complete" in combined:
            insert_before = "                } else if (event.type === \"node_complete\" && event.cycle) {"
            if insert_before in combined:
                combined = combined.replace(
                    insert_before,
                    error_handler + "\n                " + insert_before.strip() + " {",
                    1,
                )
        return combined

    # Find the second conflict block (which is much larger)
    conflicts = list(re.finditer(
        r"<<<<<<< HEAD\n(.*?)=======\n(.*?)>>>>>>> overhaul/loop\n",
        content,
        flags=re.DOTALL,
    ))

    if len(conflicts) >= 1:
        m = conflicts[0]
        head_part = m.group(1)
        loop_part = m.group(2)
        # Simple resolution: keep loop's richer handling, but insert error handler
        # The error event: check if loop already has an error handler
        if "event.type === \"error\"" not in loop_part:
            # Insert the error handler from HEAD before the node_complete block in loop
            node_complete_pattern = "} else if (event.type === \"node_complete\" && event.cycle) {"
            if node_complete_pattern in loop_part:
                insert_part = head_part.rstrip() + "\n                "
                loop_part = loop_part.replace(
                    node_complete_pattern,
                    insert_part.rstrip() + "\n                " + node_complete_pattern,
                    1,
                )
        replacement = loop_part
        content = content[:m.start()] + replacement + content[m.end():]

    if "<<<<<<< HEAD" in content:
        print("WARNING: ResearchLoopPanel.tsx still has conflict markers — manual review needed.")
    else:
        with open(path_rp, "w", encoding="utf-8") as f:
            f.write(content)
        print("ResearchLoopPanel.tsx conflicts resolved.")
