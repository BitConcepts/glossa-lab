"""AI Tools API — advanced AI-powered research assistance.

Endpoints:
  POST /ai/chat                    -- freeform Q&A with optional corpus/experiment context
  POST /ai/decipher                -- Indus sign sequence decipherment assistant
  POST /ai/draft-section           -- experiment result → academic paper paragraph
  POST /ai/hypotheses/generate     -- generate hypotheses from study results
  POST /ai/experiment-chain        -- plan a sequence of experiments for a hypothesis
  POST /ai/synthesize              -- cross-study synthesis
  POST /ai/sign-reading            -- probabilistic sign reading suggestions
"""

from __future__ import annotations

import asyncio
import json
import re
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["ai-tools"])


# ── Action helpers ─────────────────────────────────────────────────────────────

_ACTION_RE = re.compile(r"%%ACTIONS%%(.*?)%%END_ACTIONS%%", re.DOTALL)


def _parse_actions(text: str) -> tuple[str, list[dict[str, Any]]]:
    """Extract %%ACTIONS%%...%%END_ACTIONS%% block from LLM response.

    Handles models that emit multiple separate [...] arrays instead of one.
    Filters to only items that are dicts with a 'type' key (action objects),
    so sign-sequence numbers like [520] in the text never cause parse errors.
    Returns (clean_text, actions_list).
    """
    match = _ACTION_RE.search(text)
    if not match:
        return text, []
    raw = match.group(1).strip()
    # Collect all [...] array blocks, keep only dict items with 'type'
    arrays = re.findall(r"\[.*?\]", raw, re.DOTALL)
    actions: list[dict[str, Any]] = []
    for arr in arrays:
        try:
            parsed = json.loads(arr)
            if isinstance(parsed, list):
                for item in parsed:
                    if isinstance(item, dict) and "type" in item:
                        actions.append(item)
        except (json.JSONDecodeError, ValueError):
            pass
    if not actions:
        try:
            parsed_whole = json.loads(raw)
            if isinstance(parsed_whole, list):
                actions = [a for a in parsed_whole if isinstance(a, dict) and "type" in a]
        except (json.JSONDecodeError, ValueError):
            return text, []
    return text[: match.start()].rstrip(), actions


def _build_settings_context() -> str:
    """Return a compact summary of current AI provider / key status."""
    from glossa_lab.api.settings import get_key  # noqa: PLC0415

    lines = ["\n=== CURRENT SETTINGS ==="]
    providers = [
        ("mistral_api_key",   "Mistral"),
        ("openai_api_key",    "OpenAI"),
        ("anthropic_api_key", "Anthropic"),
        ("google_api_key",    "Google"),
    ]
    for key_name, label in providers:
        val = get_key(key_name)
        status = f"set ({val[:4]}…)" if val else "not set"
        lines.append(f"  {label}: {status}")
    # Ollama installed models
    try:
        import urllib.request  # noqa: PLC0415
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as r:
            data = json.loads(r.read())
        names = [m["name"] for m in data.get("models", [])]
        lines.append(f"  Ollama models installed: {', '.join(names) or 'none'}")
    except Exception:  # noqa: BLE001
        lines.append("  Ollama: not reachable")
    lines.append("=== END SETTINGS ===")
    return "\n".join(lines)


_ACTION_SYSTEM_ADDENDUM = """

=== GLOSSA LAB ACTIONS ===
You can propose actions for the user to approve. After your response text, if you want to
propose one or more actions include a block formatted EXACTLY as shown:

%%ACTIONS%%
[{"type": "run_experiment", "params": {"id": "contact_zone_analysis"}, "label": "Run Contact Zone Analysis", "description": "Runs KL divergence on contact-zone vs heartland sites (~30 seconds)."}]
%%END_ACTIONS%%

Available action types and their params:
  run_experiment      {"id": "<experiment_id>"}              — requires approval
  run_pipeline        {"pipeline": "<id>", "params": {}, "name": "<job_name>"}  — requires approval
  change_setting      {"key": "<setting_key>", "value": "<value>"}  — requires approval; never suggest actual key values
  generate_report     {"script": "<script_name.py>"}         — requires approval
  create_hypothesis   {"title": "...", "statement": "..."}   — no approval needed
  create_notebook     {"title": "...", "content": "..."}     — no approval needed
  open_view           {"view": "<view_id>"}                  — no approval; navigates to a view
  clear_jobs          {}                                      — requires approval

View IDs for open_view: studies, builder, experiments, corpora, reports, entropy, signs,
  timeline, hypotheses, notebooks, citations, ai-tools, status, pipelines, jobs, settings

Rules:
- Only propose actions when the user explicitly asks you to DO something.
- NEVER propose actions unsolicited.
- Always explain what you're proposing and why, BEFORE the %%ACTIONS%% block.
- One %%ACTIONS%% block per response, containing a JSON array (even for a single action).
- NEVER ask for or suggest API key values in change_setting actions.
=== END GLOSSA LAB ACTIONS ==="""

_REPORTS = Path(__file__).resolve().parent.parent.parent.parent / "reports"
_LEDGER  = Path(__file__).resolve().parent.parent.parent.parent / "LEDGER.md"


def _build_research_context() -> str:
    """Assemble current Indus decipherment research state into a compact context block.

    Loads from reports/sign_expansion.json and the last ~80 lines of LEDGER.md
    so any AI model has the full current state without needing file uploads.
    """
    lines: list[str] = []
    lines.append("=== GLOSSA LAB — INDUS SCRIPT DECIPHERMENT RESEARCH CONTEXT ===")

    # ---- Sign assignments from sign_expansion.json --------------------------
    catalog_path = _REPORTS / "sign_expansion.json"
    if catalog_path.exists():
        try:
            data = json.loads(catalog_path.read_text(encoding="utf-8"))
            cov = data.get("token_coverage", {})
            lines.append(
                "\nCorpus: 4,410 inscriptions | 14,213 tokens | 713 sign types"
            )
            lines.append(
                f"Token coverage: {cov.get('pct', '?')}% "
                f"({cov.get('known_tokens','?')}/{cov.get('total_tokens','?')}) "
                "with current assignments"
            )

            # Sign catalog table
            top100 = data.get("top100_catalog", [])
            assigned = [r for r in top100 if r.get("confidence") in ("HIGH","MED","LOW")]
            lines.append("\nSIGN ASSIGNMENTS (current session):")
            lines.append("  Fuls  Count   T    I    M   M77  Conf   Value       Description")
            for r in sorted(assigned, key=lambda x: x.get("rank", 999)):
                lines.append(
                    f"  {r['fuls']:>4}  {r['count']:>5}  "
                    f"{r['t_rate']:.2f}  {r['i_rate']:.2f}  {r['m_rate']:.2f}  "
                    f"{r['best_m77']:>4}  {r['confidence']:>4}  "
                    f"{r['known_value']:>10}  {r.get('m77_desc','')[:20]}"
                )
        except Exception:  # noqa: BLE001
            lines.append("(sign catalog unavailable)")

    # ---- Key findings from decipherment_synthesis.json ----------------------
    synth_path = _REPORTS / "decipherment_synthesis.json"
    if synth_path.exists():
        try:
            d = json.loads(synth_path.read_text(encoding="utf-8"))
            fish = d.get("fish_ranking", [])
            if fish:
                lines.append("\nFISH SIGN RANKING (M77 profile distance):")
                for f in fish:
                    lines.append(
                        f"  Fuls {f['fuls']:>3} → M059 dist={f['m77_dist']:.3f}  "
                        f"M-rate={f['m_rate']:.3f}  n={f['total']}"
                    )
            patts = d.get("readable_inscriptions", {})
            lines.append(
                f"\nReadable inscriptions: "
                f"{patts.get('total_100pct',0)} fully known, "
                f"{patts.get('total_50pct',0)} at >50%"
            )
            top = patts.get("top_patterns", [])[:8]
            if top:
                lines.append("Top patterns:")
                for p in top:
                    lines.append(
                        f"  {' '.join(p['pattern'])} ({p['count']}x) = {p['reading']}"
                    )
        except Exception:  # noqa: BLE001
            pass

    # ---- Last LEDGER entry (open TODOs + next step) -------------------------
    if _LEDGER.exists():
        try:
            ledger_text = _LEDGER.read_text(encoding="utf-8", errors="replace")
            ledger_lines = ledger_text.splitlines()
            # Find the last '## [' heading
            last_entry_idx = max(
                (i for i, ln in enumerate(ledger_lines) if ln.startswith("## [")),
                default=max(0, len(ledger_lines) - 80),
            )
            snippet = "\n".join(ledger_lines[last_entry_idx:][-80:])
            lines.append("\n=== LAST LEDGER ENTRY (current state + open TODOs) ===")
            lines.append(snippet)
        except Exception:  # noqa: BLE001
            pass

    lines.append("\n=== END RESEARCH CONTEXT ===")
    lines.append(
        "You are acting as a decipherment research collaborator. "
        "Reason from the evidence above. Propose hypotheses with explicit "
        "confidence levels (HIGH/MED/LOW). When suggesting analysis, describe "
        "what a Python script would do so the team can implement it. "
        "Reference Fuls sign numbers (e.g. 'sign 817') not abstract descriptions."
    )
    return "\n".join(lines)


# ── Request models ─────────────────────────────────────────────────────────────


class ChatMessage(BaseModel):
    role: str = "user"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    context_type: str | None = None  # "corpus" | "experiment" | "study" | "research"
    context_id: str | None = None
    stream: bool = False
    provider: str | None = None   # model picker override: "ollama"|"mistral"|"openai"|"anthropic"
    model: str | None = None      # model name override


class ActionExecuteRequest(BaseModel):
    type: str
    params: dict[str, Any] = {}


class DecipherRequest(BaseModel):
    sign_sequence: list[str]
    theory: str = "linguistic"  # linguistic | logo-syllabic | acrophonic | dravidian
    corpus_id: str | None = None


class DraftSectionRequest(BaseModel):
    experiment_id: str
    section_type: str = "results"  # abstract | introduction | methods | results | discussion
    result_json: dict[str, Any] = {}


class HypothesisGenRequest(BaseModel):
    study_id: str | None = None
    context: str = ""  # free-form context if no study_id


class ExperimentChainRequest(BaseModel):
    hypothesis: str
    available_experiment_ids: list[str] = []


class SynthesisRequest(BaseModel):
    study_ids: list[str]
    question: str = ""


class SignReadingRequest(BaseModel):
    sign_ids: list[str]  # e.g. ["740", "400", "700"]
    theory: str = "dravidian"
    context: str = ""


# ── Shared helper ─────────────────────────────────────────────────────────────


def _build_system_prompt(
    base: str,
    context_block: str,
    settings_ctx: str,
    action_addendum: str,
    style: str,
) -> str:
    """Assemble the system prompt in the style best suited to the model."""
    if style == "xml":
        # Claude responds well to explicit XML structure
        return (
            f"<role>\n{base}\n</role>\n"
            f"<context>{context_block}{settings_ctx}\n</context>\n"
            "<instructions>\n"
            "Be concise, precise, and scientifically rigorous. "
            "Cite specific numbers. Say so when uncertain."
            f"\n{action_addendum}\n</instructions>"
        )
    if style == "sections":
        # Mistral / Qwen / Llama prefer clear section headers
        return (
            f"### Role\n{base}\n\n"
            f"### Context{context_block}{settings_ctx}\n\n"
            "### Instructions\n"
            "Be concise, precise, and scientifically rigorous. "
            "Cite specific numbers. Say so when uncertain."
            f"{action_addendum}"
        )
    # "plain" — single paragraph (smallest models, o1)
    return (
        f"{base}"
        f"{context_block}"
        f"{settings_ctx}\n\n"
        "Be concise, precise, and scientifically rigorous. "
        "Cite specific numbers. When uncertain, say so."
        f"{action_addendum}"
    )


async def _run_llm(
    messages: list[dict[str, str]],
    json_mode: bool = False,
    provider: str | None = None,
    model: str | None = None,
) -> str:
    from glossa_lab.ai_utils import call_llm  # noqa: PLC0415
    from glossa_lab.model_profiles import get_profile, trim_history  # noqa: PLC0415

    profile = get_profile(model)
    # Trim history to model's context budget (chars = tokens * 4)
    messages = trim_history(messages, budget_chars=profile["ctx_budget"] * 4)

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: call_llm(
            messages,
            json_mode=json_mode,
            max_tokens=profile["max_tokens"],
            temperature=profile["temperature"],
            provider_override=provider,
            model_override=model,
        ),
    )


# ── Endpoints ──────────────────────────────────────────────────────────────────


@router.post("/chat")
async def ai_chat(body: ChatRequest) -> dict[str, Any]:
    """Conversational AI with optional corpus / experiment / study context.

    Pass context_type + context_id to inject relevant data into the system prompt.
    """
    from glossa_lab.database import get_db
    from glossa_lab.experiment_base import get_experiment

    context_block = ""

    # ── Research context: load full decipherment state from reports + LEDGER ──
    if body.context_type == "research":
        context_block = "\n\n" + _build_research_context()

    elif body.context_type and body.context_id:
        db = get_db()
        if db:
            if body.context_type == "corpus":
                text = await db.get_text(body.context_id)
                if text:
                    from collections import Counter

                    freq = Counter(text["content"])
                    top10 = ", ".join(f"{t}={c}" for t, c in freq.most_common(10))
                    context_block = (
                        f"\n\n[Active corpus: {text['name']} | "
                        f"{len(text['content'])} tokens | alphabet {text['alphabet_size']} | "
                        f"top tokens: {top10}]"
                    )
            elif body.context_type == "study":
                study = await db.get_study(body.context_id)
                if study:
                    context_block = (
                        f"\n\n[Active study: {study['name']} — {study.get('description', '')} | "
                        f"{len(study.get('graph', {}).get('nodes', []))} experiments]"
                    )
        if body.context_type == "experiment" and body.context_id:
            cls = get_experiment(body.context_id)
            if cls:
                m = cls.to_dict()
                context_block = (
                    f"\n\n[Active experiment: {m['name']} ({m['category']}) — {m['description']}]"
                )

    from glossa_lab.model_profiles import get_profile  # noqa: PLC0415

    profile = get_profile(body.model)
    settings_ctx = _build_settings_context()
    action_addendum = _ACTION_SYSTEM_ADDENDUM if profile["action_capable"] else ""

    base_role = (
        "You are Glossa, an expert AI research assistant for Glossa Lab — a computational "
        "linguistics platform studying the Indus Script. You have deep knowledge of "
        "information theory, computational linguistics, ancient scripts, and the specific "
        "methodology used at Glossa Lab (entropy analysis, n-gram statistics, Zipf law, "
        "comparative linguistics with Sumerian, Proto-Elamite, Luwian, Linear A, etc.)."
    )

    system = _build_system_prompt(
        base=base_role,
        context_block=context_block,
        settings_ctx=settings_ctx,
        action_addendum=action_addendum,
        style=profile["prompt_style"],
    )

    messages = [{"role": "system", "content": system}] + [
        {"role": m.role, "content": m.content} for m in body.messages
    ]

    try:
        raw_reply = await _run_llm(messages, provider=body.provider, model=body.model)
        clean_reply, actions = _parse_actions(raw_reply)
        return {
            "role": "assistant",
            "content": clean_reply,
            "actions": actions,
            "context_type": body.context_type,
            "context_id": body.context_id,
        }
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/execute-action")
async def execute_action(body: ActionExecuteRequest) -> dict[str, Any]:
    """Execute an AI-proposed action that the user has approved."""
    t = body.type
    p = body.params

    # ── open_view — client-side navigation, nothing to do on server ────────────
    if t == "open_view":
        return {"ok": True, "navigate": p.get("view"), "summary": f"Navigating to {p.get('view', '?')}"}

    # ── run_experiment ──────────────────────────────────────────────────────────
    if t == "run_experiment":
        from glossa_lab.experiment_base import get_experiment  # noqa: PLC0415
        exp_id = p.get("id", "")
        cls = get_experiment(exp_id)
        if cls is None:
            raise HTTPException(404, f"Experiment '{exp_id}' not found")
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, cls().run)
        n = len(result) if isinstance(result, dict) else "?"
        return {"ok": True, "summary": f"Experiment '{exp_id}' completed ({n} result keys).", "result": result}

    # ── run_pipeline ────────────────────────────────────────────────────────────
    if t == "run_pipeline":
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db is None:
            raise HTTPException(503, "Database unavailable")
        job = await db.create_job({
            "name": p.get("name", p.get("pipeline", "ai-job")),
            "pipeline": p.get("pipeline", ""),
            "params": p.get("params", {}),
            "status": "pending",
        })
        return {"ok": True, "summary": f"Pipeline job queued (id={job['id']}).", "job_id": job["id"]}

    # ── change_setting ──────────────────────────────────────────────────────────
    if t == "change_setting":
        from glossa_lab.api.settings import set_key  # noqa: PLC0415
        key = p.get("key", "")
        value = p.get("value", "")
        if not key:
            raise HTTPException(400, "Missing setting key")
        set_key(key, str(value))
        return {"ok": True, "summary": f"Setting '{key}' updated."}

    # ── generate_report ─────────────────────────────────────────────────────────
    if t == "generate_report":
        script = p.get("script", "")
        if not script:
            raise HTTPException(400, "Missing script name")
        import subprocess  # noqa: PLC0415, S404
        import sys
        backend_dir = Path(__file__).resolve().parent.parent.parent
        script_path = backend_dir / script
        if not script_path.exists():
            raise HTTPException(404, f"Script {script} not found")
        proc = subprocess.run(  # noqa: S603
            [sys.executable, str(script_path)],
            capture_output=True, text=True, timeout=300,
        )
        ok = proc.returncode == 0
        return {"ok": ok, "summary": f"Report script finished (exit {proc.returncode}).",
                "stdout": proc.stdout[-500:], "stderr": proc.stderr[-200:]}

    # ── create_hypothesis ───────────────────────────────────────────────────────
    if t == "create_hypothesis":
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db is None:
            raise HTTPException(503, "Database unavailable")
        h = await db.create_hypothesis({
            "title": p.get("title", "AI-generated hypothesis"),
            "statement": p.get("statement", ""),
            "status": "active", "evidence": [], "study_ids": [], "exp_ids": [],
        })
        return {"ok": True, "summary": f"Hypothesis '{h['title']}' created.", "id": h["id"]}

    # ── create_notebook ─────────────────────────────────────────────────────────
    if t == "create_notebook":
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db is None:
            raise HTTPException(503, "Database unavailable")
        nb = await db.create_notebook({
            "title": p.get("title", "AI note"),
            "content": p.get("content", ""),
            "study_id": None, "tags": ["ai-generated"],
        })
        return {"ok": True, "summary": f"Notebook entry '{nb['title']}' created.", "id": nb["id"]}

    # ── clear_jobs ──────────────────────────────────────────────────────────────
    if t == "clear_jobs":
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db is None:
            raise HTTPException(503, "Database unavailable")
        n = await db.clear_jobs()
        return {"ok": True, "summary": f"Cleared {n} jobs."}

    raise HTTPException(400, f"Unknown action type: '{t}'")


@router.post("/decipher")
async def ai_decipher(body: DecipherRequest) -> dict[str, Any]:
    """Indus Script decipherment assistant — apply a theory to a sign sequence."""
    theory_descriptions = {
        "linguistic": "general linguistic analysis treating signs as syllabic or logographic units",
        "logo-syllabic": "logo-syllabic hypothesis: leading sign is logographic, rest syllabic",
        "acrophonic": "acrophonic principle: each sign represents the first sound of its name in a Dravidian language",
        "dravidian": "Dravidian proto-language hypothesis: signs map to Proto-Tamil/Dravidian morphemes",
    }
    theory_desc = theory_descriptions.get(body.theory, body.theory)
    seq = " → ".join(body.sign_sequence)

    system = (
        "You are an expert in ancient script decipherment, specialising in the Indus Script. "
        "Return ONLY valid JSON:\n"
        '{"reading": "proposed phonetic/semantic reading", '
        '"confidence": "low|medium|high", '
        '"reasoning": "step-by-step reasoning", '
        '"alternative_readings": ["alt 1", "alt 2"], '
        '"parallels": ["parallel in other scripts"], '
        '"caveats": ["caveat 1"]}'
    )
    user = (
        f"Apply the {body.theory} theory ({theory_desc}) to interpret this Indus sign sequence:\n"
        f"Signs: {seq}\n"
        f"Sign IDs: {body.sign_sequence}"
    )

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        result = json.loads(raw)
        result["sign_sequence"] = body.sign_sequence
        result["theory"] = body.theory
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/draft-section")
async def ai_draft_section(body: DraftSectionRequest) -> dict[str, Any]:
    """Turn an experiment result into a draft academic paper section."""
    from glossa_lab.experiment_base import get_experiment

    cls = get_experiment(body.experiment_id)
    meta = cls.to_dict() if cls else {"name": body.experiment_id, "description": "", "category": ""}

    section_instructions = {
        "abstract": "Write a 150-word abstract summarising the experiment and its key finding.",
        "introduction": "Write an Introduction paragraph (200 words) motivating this experiment.",
        "methods": "Write a Methods paragraph (200 words) describing how the experiment was conducted.",
        "results": "Write a Results paragraph (200 words) reporting the numerical findings.",
        "discussion": "Write a Discussion paragraph (250 words) interpreting the results in the context of Indus Script research.",
    }
    instr = section_instructions.get(body.section_type, section_instructions["results"])

    system = (
        "You are an academic writer specialising in computational linguistics and ancient script research. "
        "Write formal, journal-quality prose. Return ONLY valid JSON:\n"
        '{"section_type": "...", "text": "the paragraph text", '
        '"suggested_title": "...", "keywords": ["kw1", "kw2"]}'
    )
    user = (
        f"Experiment: {meta['name']}\n"
        f"Category: {meta.get('category', '')}\n"
        f"Description: {meta.get('description', '')}\n"
        f"Results: {json.dumps(body.result_json, indent=2)[:1500]}\n\n"
        f"{instr}"
    )

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        result = json.loads(raw)
        result["experiment_id"] = body.experiment_id
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/hypotheses/generate")
async def ai_generate_hypotheses(body: HypothesisGenRequest) -> dict[str, Any]:
    """Generate testable hypotheses from study results or a free-text context."""
    from glossa_lab.database import get_db
    from glossa_lab.experiment_base import get_experiment

    context = body.context
    if body.study_id:
        db = get_db()
        if db:
            study = await db.get_study(body.study_id)
            if study:
                graph = study.get("graph", {})
                exp_descs = []
                for node in graph.get("nodes", []):
                    cls = get_experiment(node.get("ref_id", ""))
                    if cls:
                        m = cls.to_dict()
                        exp_descs.append(f"- {m['name']}: {m['description']}")
                context = (
                    f"Study: {study['name']}\n"
                    f"Description: {study.get('description', '')}\n"
                    f"Experiments:\n" + "\n".join(exp_descs)
                ) + ("\n\n" + body.context if body.context else "")

    system = (
        "You are a research hypothesis generator for Indus Script computational linguistics. "
        "Return ONLY valid JSON:\n"
        '{"hypotheses": [{"title": "H1: ...", "statement": "full statement", '
        '"testability": "how to test this", "priority": "high|medium|low", '
        '"related_experiments": ["exp_id_hint"]}], '
        '"research_gaps": ["gap 1", "gap 2"]}'
    )
    user = f"Generate 3-5 testable research hypotheses based on:\n{context}"

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        result = json.loads(raw)
        if body.study_id:
            result["study_id"] = body.study_id
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/experiment-chain")
async def ai_experiment_chain(body: ExperimentChainRequest) -> dict[str, Any]:
    """Plan a sequence of experiments to test a research hypothesis."""
    from glossa_lab.experiment_base import list_discovered_experiments

    exps = list_discovered_experiments()
    exp_list = "\n".join(
        f"  id={e['id']!r}, name={e['name']!r}, desc={e['description'][:60]!r}" for e in exps[:25]
    )

    system = (
        "You are an experimental research planner for Indus Script linguistics. "
        "Return ONLY valid JSON:\n"
        '{"chain": [{"step": 1, "experiment_id": "...", "experiment_name": "...", '
        '"purpose": "why this step", "expected_output": "what this step produces", '
        '"depends_on": []}], '
        '"rationale": "overall experimental strategy", '
        '"success_criteria": "how to know the hypothesis is confirmed/refuted"}'
    )
    user = (
        f"Plan an experiment chain to test:\n{body.hypothesis}\n\n"
        f"Available experiments:\n{exp_list}"
    )

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        result = json.loads(raw)
        result["hypothesis"] = body.hypothesis
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/synthesize")
async def ai_synthesize(body: SynthesisRequest) -> dict[str, Any]:
    """Cross-study synthesis: find patterns and insights across multiple studies."""
    from glossa_lab.database import get_db
    from glossa_lab.experiment_base import get_experiment

    db = get_db()
    if db is None:
        raise HTTPException(status_code=503, detail="Database not available")

    study_summaries = []
    for sid in body.study_ids[:6]:
        study = await db.get_study(sid)
        if not study:
            continue
        nodes = study.get("graph", {}).get("nodes", [])
        exp_names = []
        for node in nodes:
            cls = get_experiment(node.get("ref_id", ""))
            if cls:
                exp_names.append(cls.to_dict()["name"])
        study_summaries.append(
            f"Study '{study['name']}': {study.get('description', '')} | "
            f"experiments: {', '.join(exp_names) or 'none'}"
        )

    system = (
        "You are a meta-researcher synthesising findings across multiple Indus Script studies. "
        "Return ONLY valid JSON:\n"
        '{"synthesis": "narrative synthesis of key cross-study findings", '
        '"convergent_findings": ["finding 1"], '
        '"contradictions": ["contradiction 1"], '
        '"emerging_patterns": ["pattern 1"], '
        '"recommended_next_studies": [{"name": "...", "rationale": "..."}], '
        '"overall_assessment": "where does the research stand?"}'
    )
    question_block = f"\nResearch question: {body.question}" if body.question else ""
    user = f"Synthesise these studies:{question_block}\n\n" + "\n".join(study_summaries)

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        result = json.loads(raw)
        result["study_ids"] = body.study_ids
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.post("/sign-reading")
async def ai_sign_reading(body: SignReadingRequest) -> dict[str, Any]:
    """Probabilistic sign reading suggestions for Indus Script sign IDs."""
    system = (
        "You are an Indus Script specialist with knowledge of all major decipherment theories. "
        "Return ONLY valid JSON:\n"
        '{"readings": [{"sign_id": "...", "theory": "...", '
        '"phonetic_reading": "...", "semantic_reading": "...", "confidence": 0.0-1.0, '
        '"notes": ""}], '
        '"sequence_reading": "overall sequence interpretation", '
        '"parallels": ["parallel in Sumerian/Elamite/Dravidian"]}'
    )
    user = (
        f"Apply the {body.theory} theory to give readings for these Indus signs:\n"
        f"Sign IDs: {', '.join(body.sign_ids)}\n"
        + (f"Context: {body.context}" if body.context else "")
    )

    try:
        raw = await _run_llm(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            json_mode=True,
        )
        result = json.loads(raw)
        result["sign_ids"] = body.sign_ids
        result["theory"] = body.theory
        return result
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/research-context")
async def get_research_context() -> dict[str, Any]:
    """Return the current Indus decipherment research context as a plain-text block.

    The frontend uses this to show a preview and to inject research state
    into the AI chat when context_type='research' is selected.
    """
    context = _build_research_context()
    # Count how many sign assignments are loaded
    catalog_path = _REPORTS / "sign_expansion.json"
    n_assigned = 0
    coverage_pct = 0.0
    next_steps: list[str] = []
    if catalog_path.exists():
        try:
            data = json.loads(catalog_path.read_text(encoding="utf-8"))
            top100 = data.get("top100_catalog", [])
            n_assigned = sum(
                1 for r in top100 if r.get("confidence") in ("HIGH", "MED", "LOW")
            )
            cov = data.get("token_coverage", {})
            coverage_pct = cov.get("pct", 0.0)
        except Exception:  # noqa: BLE001
            pass
    # Pull next step from LEDGER
    if _LEDGER.exists():
        try:
            text = _LEDGER.read_text(encoding="utf-8", errors="replace")
            for line in reversed(text.splitlines()):
                line = line.strip()
                if line.startswith("Next step:"):
                    next_steps = [line[len("Next step:"):].strip()]
                    break
        except Exception:  # noqa: BLE001
            pass
    return {
        "context": context,
        "summary": {
            "n_assigned_signs": n_assigned,
            "token_coverage_pct": coverage_pct,
            "next_steps": next_steps,
            "context_chars": len(context),
        },
    }
