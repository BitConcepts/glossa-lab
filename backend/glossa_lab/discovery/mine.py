"""Mining pipeline — classify discovery items + link to project entities.

Pipeline (matches the Phase-D plan):
1. **Dedupe**     — already happens at upsert time in :mod:`store`.
2. **Classify**   — :func:`classify_item` calls the configured LLM in JSON
                    mode, asking for {kind, confidence, summary, key_claims,
                    named_entities}.
3. **Link**       — :func:`link_entities` regex-sweeps the title + summary +
                    claims for IVC sites, sign-ID references (``sign 47``,
                    ``M-410``, ``Parpola No. 234``), and DEDR cognate-set IDs.
                    Linking is deliberately conservative — heavy lifting stays
                    in the LLM call, so the regex layer only fires on
                    high-precision patterns.

Everything is persisted via :func:`store.update_classification`. The chosen
LLM provider name + model are appended to the ``links`` list as a meta-link
of kind ``"provider"`` so a downstream UI can show "classified by Mistral".
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any, Iterable

from glossa_lab.discovery import store
from glossa_lab.discovery.llm import LLMClient, LLMError, LLMResult
from glossa_lab.discovery.store import DiscoveryItem

_log = logging.getLogger("glossa_lab.discovery.mine")

# ── Classification taxonomy ─────────────────────────────────────────────────

ALLOWED_KINDS = (
    "hypothesis",  # a new theoretical claim
    "finding",     # a new empirical result
    "study",       # a methods / analysis paper
    "tablet",      # a physical seal/tablet/inscription report
    "review",      # survey or review
    "tooling",     # software / dataset release
    "other",
)


@dataclass(slots=True)
class Classification:
    kind: str
    confidence: float
    summary: str
    key_claims: list[str] = field(default_factory=list)
    named_entities: list[str] = field(default_factory=list)
    provider: str = ""
    model: str = ""

    @classmethod
    def from_response(cls, data: dict[str, Any], result: LLMResult) -> "Classification":
        kind = str(data.get("kind", "other")).strip().lower()
        if kind not in ALLOWED_KINDS:
            kind = "other"
        try:
            confidence = float(data.get("confidence", 0.0))
        except (TypeError, ValueError):
            confidence = 0.0
        confidence = max(0.0, min(1.0, confidence))
        summary = str(data.get("summary") or "").strip()
        key_claims = [
            str(x).strip() for x in (data.get("key_claims") or []) if str(x).strip()
        ]
        named_entities = [
            str(x).strip() for x in (data.get("named_entities") or []) if str(x).strip()
        ]
        return cls(
            kind=kind,
            confidence=confidence,
            summary=summary[:600],  # storage cap; matches plan's "≤80w"-ish budget
            key_claims=key_claims[:8],
            named_entities=named_entities[:16],
            provider=result.provider,
            model=result.model,
        )


# ── Prompt construction ─────────────────────────────────────────────────────

# Default system prompt — used when no research goal is configured.
_DEFAULT_SYSTEM_PROMPT = (
    "You are a research-triage assistant. You read a single news / paper / "
    "dataset item and classify it. Reply with JSON only \u2014 no prose, no markdown."
)


def _system_prompt(goal: dict | None = None) -> str:
    """Build the system prompt, injecting goal context when available."""
    if goal and goal.get("prompt_context"):
        return (
            f"{goal['prompt_context']} "
            "You read a single news / paper / dataset item and classify it. "
            "Reply with JSON only \u2014 no prose, no markdown."
        )
    return _DEFAULT_SYSTEM_PROMPT

_INSTRUCTIONS = (
    "Return a JSON object with exactly these fields:\n"
    "  kind            string, one of: hypothesis | finding | study | tablet | "
    "review | tooling | other\n"
    "  confidence      number between 0 and 1\n"
    "  summary         <= 80 words, plain English, no editorialising\n"
    "  key_claims      list of at most 6 short factual claims, each <= 25 words\n"
    "  named_entities  list of place names, people, sign ids, DEDR ids, sites\n"
    "Use \"other\" if nothing else fits. Confidence reflects how well the item "
    "fits the chosen kind, NOT how plausible the claim is."
)


def _build_messages(
    item: DiscoveryItem, *, goal: dict | None = None,
) -> list[dict[str, str]]:
    """Compose the chat messages used to classify a single item."""
    raw = item.raw_json or {}
    snippet = (
        raw.get("description")
        or raw.get("snippet")
        or raw.get("abstract")
        or raw.get("summary")
        or ""
    )
    if isinstance(snippet, str):
        snippet = snippet[:1500]
    user = (
        f"Title: {item.title}\n"
        f"URL: {item.url}\n"
        f"Source: {item.source}\n"
        f"Topic(s): {item.topic}\n"
        f"Published: {item.published_at}\n"
        f"Snippet: {snippet}\n\n"
        f"{_INSTRUCTIONS}"
    )
    return [
        {"role": "system", "content": _system_prompt(goal)},
        {"role": "user", "content": user},
    ]


# ── Classification ──────────────────────────────────────────────────────────


def classify_item(
    item: DiscoveryItem, *, client: LLMClient, goal: dict | None = None,
) -> Classification:
    """Run the LLM classifier on *item*. Raises :class:`LLMError` on failure."""
    data, result = client.chat_json(
        _build_messages(item, goal=goal), max_tokens=600, temperature=0.0,
    )
    return Classification.from_response(data, result)


# ── Entity linking ──────────────────────────────────────────────────────────

# Conservative regexes — high precision, low recall. The LLM's named_entities
# list provides the broader recall; the regex pass anchors specific resolvable
# IDs.
_RE_SIGN     = re.compile(r"\bsign\s+(\d{1,4})\b", re.IGNORECASE)
_RE_M_NUM    = re.compile(r"\bM-?(\d{2,4})\b")
_RE_PARPOLA  = re.compile(r"\bParpola\s+(?:No\.|#)\s*(\d{1,4})\b", re.IGNORECASE)
_RE_FULS     = re.compile(r"\bFuls\s+(?:No\.|#)?\s*(\d{1,4})\b", re.IGNORECASE)
_RE_DEDR     = re.compile(r"\bDEDR\s*#?\s*(\d{1,5})[a-z]?\b", re.IGNORECASE)

# Recognised IVC archaeological sites (case-insensitive whole-word match).
_IVC_SITES = (
    "Mohenjo-daro", "Mohenjo-Daro", "Mohenjo daro",
    "Harappa", "Rakhigarhi", "Dholavira", "Banawali",
    "Lothal", "Kalibangan", "Ganweriwala", "Sanauli",
    "Chanhu-daro", "Chanhudaro",
)
_RE_SITE = re.compile(
    r"\b(" + "|".join(re.escape(s) for s in _IVC_SITES) + r")\b",
    re.IGNORECASE,
)


def _haystack(item: DiscoveryItem, classification: Classification) -> str:
    parts = [item.title, classification.summary]
    parts.extend(classification.key_claims)
    parts.extend(classification.named_entities)
    return "  ".join(p for p in parts if p)


def link_entities(item: DiscoveryItem, classification: Classification) -> list[dict[str, Any]]:
    """Return a deduplicated list of project-entity links for *item*."""
    text = _haystack(item, classification)
    if not text:
        return []
    seen: set[tuple[str, str]] = set()
    links: list[dict[str, Any]] = []

    def add(kind: str, target_id: str, *, scheme: str | None = None, label: str | None = None) -> None:
        key = (kind, f"{scheme or ''}:{target_id}".lower())
        if key in seen:
            return
        seen.add(key)
        link: dict[str, Any] = {"kind": kind, "target_id": target_id}
        if scheme:
            link["scheme"] = scheme
        if label:
            link["label"] = label
        links.append(link)

    for m in _RE_SIGN.finditer(text):
        add("sign", m.group(1), scheme="generic")
    for m in _RE_M_NUM.finditer(text):
        add("sign", m.group(1), scheme="mahadevan")
    for m in _RE_PARPOLA.finditer(text):
        add("sign", m.group(1), scheme="parpola")
    for m in _RE_FULS.finditer(text):
        add("sign", m.group(1), scheme="fuls")
    for m in _RE_DEDR.finditer(text):
        add("dedr", m.group(1))
    for m in _RE_SITE.finditer(text):
        # Normalise whitespace + casing for the canonical label
        label = m.group(1)
        canonical = label.lower().replace(" ", "-")
        add("site", canonical, label=label)

    return links


def _provider_meta_link(classification: Classification) -> dict[str, Any]:
    return {
        "kind": "provider",
        "target_id": classification.provider or "unknown",
        "label": classification.model,
    }


# ── Driver ──────────────────────────────────────────────────────────────────


@dataclass(slots=True)
class MineSummary:
    item_id: str
    classified: bool
    kind: str = "other"
    confidence: float = 0.0
    n_links: int = 0
    provider: str = ""
    error: str = ""


async def mine_item(
    item: DiscoveryItem, *, client: LLMClient, goal: dict | None = None,
) -> MineSummary:
    """Classify and link one item, persisting the result via :mod:`store`."""
    try:
        classification = classify_item(item, client=client, goal=goal)
    except LLMError as exc:
        _log.warning("classify failed for %s: %s", item.id, exc)
        return MineSummary(
            item_id=item.id, classified=False, error=f"LLMError: {exc}",
        )
    except Exception as exc:  # noqa: BLE001 — surface unexpected errors per-item
        _log.warning("classify raised %s for %s: %s", type(exc).__name__, item.id, exc)
        return MineSummary(
            item_id=item.id,
            classified=False,
            error=f"{type(exc).__name__}: {exc}",
        )

    links = link_entities(item, classification)
    links.append(_provider_meta_link(classification))

    await store.update_classification(
        item.id,
        kind=classification.kind,
        confidence=classification.confidence,
        summary=classification.summary,
        links=links,
    )
    return MineSummary(
        item_id=item.id,
        classified=True,
        kind=classification.kind,
        confidence=classification.confidence,
        n_links=len(links) - 1,  # exclude the provider meta-link from the count
        provider=classification.provider,
    )


def _is_unmined(item: DiscoveryItem) -> bool:
    """An item is considered unmined when no classifier has touched it yet.

    Heuristic: kind == "other" AND summary is empty. The provider meta-link is
    only added on a successful mine, so an absent ``provider`` entry in
    ``links`` is also a strong signal.
    """
    if item.summary:
        return False
    if item.kind != "other":
        return False
    has_provider = any(l.get("kind") == "provider" for l in (item.links or []))
    return not has_provider


async def mine_pending(
    *,
    client: LLMClient,
    topic: str | None = None,
    limit: int = 20,
) -> dict[str, Any]:
    """Mine up to *limit* unmined items, optionally restricted to *topic*.

    Returns an aggregate summary suitable for embedding in a Job result.
    """
    # Look up the research goal for context-scoped classification.
    goal: dict | None = None
    try:
        from glossa_lab.database import get_db  # noqa: PLC0415
        db = get_db()
        if db:
            goal = await db.get_default_goal()
    except Exception:  # noqa: BLE001
        pass

    items = await store.list_items(topic=topic, limit=max(limit * 2, limit))
    pending = [it for it in items if _is_unmined(it)]
    pending = pending[:limit]
    summaries: list[MineSummary] = []
    for it in pending:
        # Try to find a topic-specific goal; fall back to default.
        item_goal = goal
        if it.topic and db:
            try:
                first_topic = it.topic.split(",")[0].strip()
                tg = await db.goal_for_topic(first_topic)
                if tg:
                    item_goal = tg
            except Exception:  # noqa: BLE001
                pass
        summaries.append(await mine_item(it, client=client, goal=item_goal))
    classified = [s for s in summaries if s.classified]
    failed = [s for s in summaries if not s.classified]
    by_kind: dict[str, int] = {}
    for s in classified:
        by_kind[s.kind] = by_kind.get(s.kind, 0) + 1
    return {
        "topic": topic,
        "considered": len(items),
        "pending": len(pending),
        "classified": len(classified),
        "failed": len(failed),
        "by_kind": by_kind,
        "items": [
            {
                "id": s.item_id,
                "kind": s.kind,
                "confidence": s.confidence,
                "n_links": s.n_links,
                "provider": s.provider,
                "error": s.error,
            }
            for s in summaries
        ],
        "providers_configured": client.configured_providers(),
    }


__all__ = [
    "ALLOWED_KINDS",
    "Classification",
    "MineSummary",
    "classify_item",
    "link_entities",
    "mine_item",
    "mine_pending",
]
