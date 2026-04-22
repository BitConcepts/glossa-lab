"""AG2 Research Orchestrator for Glossa Lab.

Uses AG2 (AutoGen 2, package: ag2, import: autogen) to provide a multi-agent
research assistant that can:
  - Run graph experiments via python -m glossa_lab.experiments
  - Query corpus statistics from the CISI and ICIT corpora
  - Read the LEDGER for current research state
  - List and load experiment results from reports/
  - Execute analysis scripts via shell.cmd

LLM backend: Ollama (OpenAI-compatible endpoint at localhost:11434/v1).
Falls back gracefully if Ollama is not running.

Architecture:
  GlossaAssistant (AssistantAgent) — the research brain with Glossa domain knowledge
  GlossaExecutor  (UserProxyAgent) — executes tool calls, streams results back

Usage:
    async for event in run_ag2_chat(message, history, context):
        yield event  # SSE-compatible dict

Each event: {"type": "agent"|"tool"|"message"|"done", "content": str, "agent": str}
"""

from __future__ import annotations

import asyncio
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any, AsyncGenerator

_REPO_ROOT   = Path(__file__).resolve().parents[2]
_REPORTS_DIR = _REPO_ROOT / "reports"
_LEDGER_PATH = _REPO_ROOT / "LEDGER.md"
_BACKEND_DIR = Path(__file__).resolve().parent.parent

# ── AG2 system prompt ─────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """You are Glossa Research Assistant, an expert in:
- Indus Script decipherment (Parpola Dravidian hypothesis)
- Computational linguistics and information-theoretic analysis
- The Glossa Lab experiment platform

CURRENT RESEARCH STATE (key findings):
- Dravidian phonotactics: SA consistency 0.8166 vs Sanskrit 0.5602 (+25.64pp) on real CISI bigrams [VERIFIED]
- Optimal anchor set: P385=n, P324=k, P122=a, P086=m, P060=i, P332=o (peak HCI 88.4%)
- CV pair structure: P324(/k/) + P332(/o/) = 'ko' (king/chief, DEDR 2147)
- M-148A = royal title formula: 'ko-n' = 'of the king'
- 179 CISI Mohenjo-daro inscriptions available; need 3,000+ for full decipherment
- CPSC (CASModelLoader/CASProjector/CASIndusEngine) nodes available in Experiment Builder

TOOLS YOU CAN USE:
- run_experiment: run any graph experiment (e.g. indus_cisi_dravidian_vs_sanskrit)
- list_experiments: see all available experiments
- read_result: read any report file from reports/
- query_corpus: get corpus stats for indus_cisi, indus, dravidian, etc.
- read_ledger: get the latest LEDGER research summary

GUIDELINES:
- When asked to run an experiment, use run_experiment and then interpret the results
- Be precise with epistemic markers: [VERIFIED], [INFERRED], [UNCERTAIN], [BLOCKER]
- If you don't have data, use the tools to get it rather than guessing
- Keep responses focused and scientific

Reply TERMINATE when you have completed the user's research request."""


# ── Glossa Lab tools (available to the AG2 executor) ─────────────────────────

def _tool_list_experiments() -> str:
    """List all available graph experiments."""
    try:
        graphs_dir = _BACKEND_DIR / "glossa_lab" / "experiments" / "graphs"
        if not graphs_dir.exists():
            return "No experiments directory found."
        names = sorted(p.stem for p in graphs_dir.glob("*.json"))
        return "Available experiments:\n" + "\n".join(f"  - {n}" for n in names)
    except Exception as exc:  # noqa: BLE001
        return f"Error listing experiments: {exc}"


def _tool_run_experiment(experiment_id: str) -> str:
    """Run a graph experiment and return a summary of the result."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "glossa_lab.experiments", experiment_id],
            capture_output=True, text=True, timeout=600,
            cwd=str(_BACKEND_DIR),
        )
        if result.returncode != 0:
            return f"Experiment failed:\n{result.stderr[-500:]}"

        # Try to read the result from reports/
        out = _tool_read_result(f"{experiment_id}.json")
        if "not found" in out.lower():
            return f"Experiment completed. Output:\n{result.stdout[-300:]}"
        return f"Experiment '{experiment_id}' completed.\n{out}"
    except subprocess.TimeoutExpired:
        return f"Experiment '{experiment_id}' timed out after 600s."
    except Exception as exc:  # noqa: BLE001
        return f"Error running experiment: {exc}"


def _tool_read_result(filename: str) -> str:
    """Read a result file from reports/. Accepts filename or full path."""
    try:
        # Try exact name first, then with .json extension
        candidates = [
            _REPORTS_DIR / filename,
            _REPORTS_DIR / f"{filename}.json" if not filename.endswith(".json") else None,
        ]
        for p in candidates:
            if p and p.exists():
                data = json.loads(p.read_text("utf-8"))
                # Summarise: extract key numeric values
                lines = [f"File: {p.name}"]
                def _summarise(d: Any, depth: int = 0, max_depth: int = 3) -> None:
                    if depth > max_depth or len(lines) > 40:
                        return
                    if isinstance(d, dict):
                        for k, v in list(d.items())[:20]:
                            if isinstance(v, (int, float, bool, str)):
                                lines.append(f"  {'  '*depth}{k}: {v}")
                            elif isinstance(v, (dict, list)):
                                lines.append(f"  {'  '*depth}{k}:")
                                _summarise(v, depth+1, max_depth)
                    elif isinstance(d, list) and d:
                        lines.append(f"  {'  '*depth}[{len(d)} items] first: {str(d[0])[:80]}")
                _summarise(data)
                return "\n".join(lines)
        return f"Result file '{filename}' not found in reports/. Available:\n" + \
               "\n".join(f"  - {p.name}" for p in sorted(_REPORTS_DIR.glob("*.json"))[:20])
    except Exception as exc:  # noqa: BLE001
        return f"Error reading result: {exc}"


def _tool_query_corpus(corpus_name: str) -> str:
    """Get statistics for a named corpus: token count, H1 entropy, distinct signs."""
    try:
        sys.path.insert(0, str(_BACKEND_DIR))
        sys.path.insert(0, str(_BACKEND_DIR / "tests"))
        import math  # noqa: PLC0415
        from glossa_lab.experiment_graph import ATOMIC_NODES  # noqa: PLC0415

        r = ATOMIC_NODES["BuiltinCorpus"].fn({}, {"corpus": corpus_name})
        if "error" in r:
            return f"Error: {r['error']}"

        seqs = r.get("sequences", [])
        flat = [s for seq in seqs for s in seq]
        from collections import Counter  # noqa: PLC0415
        freq = Counter(flat)
        total = len(flat)
        h1 = -sum((c/total)*math.log2(c/total) for c in freq.values() if c > 0) if total else 0
        return (
            f"Corpus '{corpus_name}':\n"
            f"  Sequences: {len(seqs)}\n"
            f"  Tokens: {total}\n"
            f"  Distinct signs: {len(freq)}\n"
            f"  H1 entropy: {h1:.4f} bits\n"
            f"  Top 5 signs: {dict(freq.most_common(5))}"
        )
    except Exception as exc:  # noqa: BLE001
        return f"Error querying corpus '{corpus_name}': {exc}"


def _tool_read_ledger() -> str:
    """Return the last 400 lines of LEDGER.md (recent research state)."""
    try:
        if not _LEDGER_PATH.exists():
            return "LEDGER.md not found."
        lines = _LEDGER_PATH.read_text("utf-8").splitlines()
        return "\n".join(lines[-400:])
    except Exception as exc:  # noqa: BLE001
        return f"Error reading ledger: {exc}"


# Map tool names to functions
_TOOLS = {
    "list_experiments": (_tool_list_experiments,
        "List all available graph experiment IDs that can be run."),
    "run_experiment":   (_tool_run_experiment,
        "Run a specific graph experiment by ID and return the result summary. "
        "experiment_id: str — e.g. 'indus_cisi_dravidian_vs_sanskrit'"),
    "read_result":      (_tool_read_result,
        "Read an experiment result file from reports/. "
        "filename: str — e.g. 'indus_cisi_anchored_5.json'"),
    "query_corpus":     (_tool_query_corpus,
        "Get statistics (tokens, H1 entropy, sign count) for a named corpus. "
        "corpus_name: str — e.g. 'indus_cisi', 'indus', 'dravidian', 'sanskrit'"),
    "read_ledger":      (_tool_read_ledger,
        "Read the LEDGER.md research log to understand current state and findings. "
        "Returns the last 400 lines (recent sessions)."),
}


# ── LLM config builder ────────────────────────────────────────────

def _get_llm_config() -> dict | bool:
    """Build AG2 LLM config using the model selected in Glossa Lab Settings.

    Reads from the same provider-preference store that call_llm() uses,
    so AG2 always honours the user's Settings > Default AI selection.
    Returns False if no Ollama model is configured (tool-only mode).
    """
    try:
        from glossa_lab.ai_utils import _get_provider_prefs  # noqa: PLC0415
        prefs = _get_provider_prefs()
        ollama = prefs.get("ollama", {})
        if not (ollama.get("enabled") and ollama.get("selected_model")):
            return False
        model = ollama["selected_model"]
        return {
            "config_list": [{
                "model": model,
                "base_url": "http://localhost:11434/v1",
                "api_key": "ollama",
            }],
            "temperature": 0.3,
            "max_tokens": 2048,
            "cache_seed": None,
        }
    except Exception:  # noqa: BLE001
        return False


# ── Main chat function ────────────────────────────────────────────────────────

async def run_ag2_chat(
    message: str,
    history: list[dict] | None = None,
    context_type: str = "",
    context_id: str = "",
) -> AsyncGenerator[dict[str, Any], None]:
    """Run an AG2 research conversation and yield SSE-compatible events.

    Each event is a dict with keys:
      type: "agent_start" | "tool_call" | "tool_result" | "message" | "error" | "done"
      content: str
      agent: str  (agent name)
      metadata: dict (optional extra info)
    """
    import autogen  # noqa: PLC0415

    llm_config = _get_llm_config()

    # Yield status
    yield {
        "type": "agent_start",
        "agent": "system",
        "content": f"AG2 Research Agent starting. LLM: {'enabled (' + (llm_config['config_list'][0]['model'] if llm_config else '') + ')' if llm_config else 'offline — tool-only mode'}",
    }

    # ── Build function_map for the UserProxyAgent ─────────────────────────────
    function_map: dict[str, Any] = {}

    # Wrap each tool to emit events via a queue
    event_queue: asyncio.Queue[dict] = asyncio.Queue()
    loop = asyncio.get_event_loop()

    def _make_tool_wrapper(name: str, fn: Any) -> Any:
        def wrapper(**kwargs: Any) -> str:
            loop.call_soon_threadsafe(event_queue.put_nowait, {
                "type": "tool_call",
                "agent": "executor",
                "content": f"Calling tool `{name}`" + (f" with {kwargs}" if kwargs else ""),
            })
            try:
                result = fn(**kwargs) if kwargs else fn()
                loop.call_soon_threadsafe(event_queue.put_nowait, {
                    "type": "tool_result",
                    "agent": "executor",
                    "content": str(result)[:800],
                })
                return result
            except Exception as exc:  # noqa: BLE001
                err = f"Tool '{name}' failed: {exc}"
                loop.call_soon_threadsafe(event_queue.put_nowait, {
                    "type": "tool_result",
                    "agent": "executor",
                    "content": err,
                })
                return err
        wrapper.__name__ = name
        wrapper.__doc__ = _TOOLS[name][1]
        return wrapper

    for tool_name, (tool_fn, _) in _TOOLS.items():
        sig_args = _tool_signatures(tool_name, tool_fn)
        function_map[tool_name] = _make_tool_wrapper(tool_name, tool_fn)

    # ── Build AG2 agents ──────────────────────────────────────────────────────
    # Build functions list for the AssistantAgent (for LLM tool calling)
    functions_schema = [
        {
            "name": name,
            "description": desc,
            "parameters": _tool_signatures(name, fn),
        }
        for name, (fn, desc) in _TOOLS.items()
    ]

    assistant = autogen.AssistantAgent(
        name="GlossaResearch",
        system_message=_SYSTEM_PROMPT,
        llm_config={**llm_config, "functions": functions_schema} if llm_config else False,
        max_consecutive_auto_reply=8,
    )

    executor = autogen.UserProxyAgent(
        name="GlossaExecutor",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=6,
        is_termination_msg=lambda m: isinstance(m.get("content"), str) and "TERMINATE" in m["content"],
        code_execution_config=False,  # We use function tools, not code execution
        function_map=function_map,
    )

    # ── Register message callback ─────────────────────────────────────────────
    _original_receive = assistant.receive

    def _patched_receive(message: Any, sender: Any, request_reply: bool | None = None, silent: bool | None = False):
        content = message.get("content", "") if isinstance(message, dict) else str(message)
        if content and content.strip() and content != "None":
            loop.call_soon_threadsafe(event_queue.put_nowait, {
                "type": "message",
                "agent": "GlossaResearch",
                "content": content[:2000],
            })
        return _original_receive(message, sender, request_reply=request_reply, silent=silent)

    assistant.receive = _patched_receive

    # ── Run AG2 conversation in thread ────────────────────────────────────────
    done_flag: list[bool] = [False]
    error_flag: list[str] = [""]

    def _run_conversation():
        try:
            # Add context to the message if provided
            full_msg = message
            if context_type and context_id:
                full_msg = f"[Context: {context_type}={context_id}]\n\n{message}"
            executor.initiate_chat(
                assistant,
                message=full_msg,
                max_turns=8,
                silent=True,
            )
        except Exception as exc:  # noqa: BLE001
            error_flag[0] = str(exc)
        finally:
            done_flag[0] = True
            loop.call_soon_threadsafe(event_queue.put_nowait, {"type": "done", "agent": "system", "content": ""})

    import threading  # noqa: PLC0415
    thread = threading.Thread(target=_run_conversation, daemon=True)
    thread.start()

    # ── Yield events from queue ───────────────────────────────────────────────
    while True:
        try:
            event = await asyncio.wait_for(event_queue.get(), timeout=120.0)
            yield event
            if event.get("type") == "done":
                break
        except asyncio.TimeoutError:
            yield {"type": "error", "agent": "system",
                   "content": "AG2 conversation timed out after 120s."}
            break

    if error_flag[0]:
        yield {"type": "error", "agent": "system", "content": error_flag[0]}

    thread.join(timeout=5)


def _tool_signatures(name: str, fn: Any) -> dict:
    """Build JSON Schema parameter signatures for AG2 tool registration."""
    import inspect  # noqa: PLC0415
    sig = inspect.signature(fn)
    properties: dict = {}
    required: list = []
    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue
        properties[param_name] = {"type": "string", "description": f"Parameter: {param_name}"}
        if param.default is inspect.Parameter.empty:
            required.append(param_name)
    return {
        "type": "object",
        "properties": properties,
        "required": required,
    }
