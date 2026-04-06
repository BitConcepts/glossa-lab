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
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["ai-tools"])


# ── Request models ─────────────────────────────────────────────────────────────


class ChatMessage(BaseModel):
    role: str = "user"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    context_type: str | None = None  # "corpus" | "experiment" | "study"
    context_id: str | None = None
    stream: bool = False


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


async def _run_llm(messages: list[dict[str, str]], json_mode: bool = False) -> str:
    from glossa_lab.ai_utils import call_llm

    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(
        None,
        lambda: call_llm(messages, json_mode=json_mode, max_tokens=2500),
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
    if body.context_type and body.context_id:
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

    system = (
        "You are Glossa, an expert AI research assistant for Glossa Lab — a computational "
        "linguistics platform studying the Indus Script. You have deep knowledge of "
        "information theory, computational linguistics, ancient scripts, and the specific "
        "methodology used at Glossa Lab (entropy analysis, n-gram statistics, Zipf law, "
        "comparative linguistics with Sumerian, Proto-Elamite, Luwian, Linear A, etc.)."
        f"{context_block}\n\n"
        "Be concise, precise, and scientifically rigorous. When you reference specific numbers "
        "cite what you know. When uncertain, say so."
    )

    messages = [{"role": "system", "content": system}] + [
        {"role": m.role, "content": m.content} for m in body.messages
    ]

    try:
        reply = await _run_llm(messages)
        return {
            "role": "assistant",
            "content": reply,
            "context_type": body.context_type,
            "context_id": body.context_id,
        }
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


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
