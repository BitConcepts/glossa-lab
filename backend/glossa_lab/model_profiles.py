"""Model capability profiles for Glossa Lab AI.

Each profile controls how the LLM is called and how the system prompt is
structured. Profiles are matched by model name prefix (longest first).

Keys
----
max_tokens       Maximum tokens to generate in a single response.
temperature      Sampling temperature. Research tasks need low variance (0.1–0.25).
ctx_budget       How many tokens of conversation history to keep (messages trimmed
                 oldest-first if over budget).  Not the same as the model's full
                 context window — we intentionally leave room for the system prompt.
action_capable   Whether the model reliably produces %%ACTIONS%%...%%END_ACTIONS%%
                 blocks. False = action addendum stripped from system prompt to save
                 tokens and reduce confusion.
prompt_style     How to format the system prompt.
                   "plain"    – single paragraph (current behaviour)
                   "sections" – ### headings + ---- separators (best for Mistral)
                   "xml"      – <context>/<instructions> tags (best for Claude)
"""

from __future__ import annotations

from typing import TypedDict


class ModelProfile(TypedDict):
    max_tokens: int
    temperature: float
    ctx_budget: int     # tokens of history to keep (system prompt is separate)
    action_capable: bool
    prompt_style: str   # "plain" | "sections" | "xml"


# ── Per-model profiles ────────────────────────────────────────────────────────
# Matched by name prefix, longest match wins.
# All sizes are approximate (GPT-4o-style: 1 token ≈ 4 chars).

_PROFILES: dict[str, ModelProfile] = {

    # ── Mistral (local via Ollama) ────────────────────────────────────────────
    # Nemo 12B: 128K context, Tekken tokenizer (efficient for non-ASCII), very
    # good instruction following, reliable structured output.
    "mistral-nemo":     {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 24000, "action_capable": True,  "prompt_style": "sections"},

    # Mistral 7B: smaller, less reliable on complex structured output
    "mistral:7b":       {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  6000, "action_capable": False, "prompt_style": "sections"},
    "mistral:latest":   {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  6000, "action_capable": False, "prompt_style": "sections"},

    # ── Qwen 2.5 (local via Ollama) ───────────────────────────────────────────
    "qwen2.5:72b":      {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 20000, "action_capable": True,  "prompt_style": "sections"},
    "qwen2.5:32b":      {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 16000, "action_capable": True,  "prompt_style": "sections"},
    "qwen2.5:14b":      {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 12000, "action_capable": True,  "prompt_style": "sections"},
    "qwen2.5:7b":       {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  6000, "action_capable": True,  "prompt_style": "sections"},
    "qwen2.5:3b":       {"max_tokens": 1024, "temperature": 0.25, "ctx_budget":  3000, "action_capable": False, "prompt_style": "plain"},
    "qwen2.5":          {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  8000, "action_capable": True,  "prompt_style": "sections"},

    # ── Llama 3 (local via Ollama) ────────────────────────────────────────────
    "llama3.3":         {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 16000, "action_capable": True,  "prompt_style": "sections"},
    "llama3.2:3b":      {"max_tokens": 1024, "temperature": 0.25, "ctx_budget":  3000, "action_capable": False, "prompt_style": "plain"},
    "llama3.2:1b":      {"max_tokens":  768, "temperature": 0.30, "ctx_budget":  2000, "action_capable": False, "prompt_style": "plain"},
    "llama3.2":         {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  8000, "action_capable": True,  "prompt_style": "sections"},
    "llama3.1":         {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  8000, "action_capable": True,  "prompt_style": "sections"},
    "llama3":           {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  8000, "action_capable": True,  "prompt_style": "sections"},

    # ── Gemma (local via Ollama) ──────────────────────────────────────────────
    "gemma3:27b":       {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 16000, "action_capable": True,  "prompt_style": "sections"},
    "gemma3:12b":       {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  8000, "action_capable": True,  "prompt_style": "sections"},
    "gemma3":           {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  8000, "action_capable": True,  "prompt_style": "sections"},

    # ── Phi (local via Ollama) ────────────────────────────────────────────────
    "phi4":             {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 12000, "action_capable": True,  "prompt_style": "sections"},
    "phi3.5":           {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  6000, "action_capable": False, "prompt_style": "plain"},

    # ── Mistral API ───────────────────────────────────────────────────────────
    "mistral-large":        {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 24000, "action_capable": True,  "prompt_style": "sections"},
    "mistral-medium":       {"max_tokens": 4096, "temperature": 0.18, "ctx_budget": 16000, "action_capable": True,  "prompt_style": "sections"},
    "mistral-small":        {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  8000, "action_capable": True,  "prompt_style": "sections"},
    "codestral":            {"max_tokens": 4096, "temperature": 0.10, "ctx_budget": 16000, "action_capable": True,  "prompt_style": "sections"},
    "open-mistral-nemo":    {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 24000, "action_capable": True,  "prompt_style": "sections"},
    "open-mistral-7b":      {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  6000, "action_capable": False, "prompt_style": "sections"},
    "pixtral":              {"max_tokens": 4096, "temperature": 0.18, "ctx_budget": 16000, "action_capable": True,  "prompt_style": "sections"},

    # ── OpenAI ────────────────────────────────────────────────────────────────
    "gpt-4o":           {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 32000, "action_capable": True,  "prompt_style": "sections"},
    "gpt-4o-mini":      {"max_tokens": 4096, "temperature": 0.18, "ctx_budget": 16000, "action_capable": True,  "prompt_style": "sections"},
    "gpt-4-turbo":      {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 32000, "action_capable": True,  "prompt_style": "sections"},
    "gpt-4":            {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 16000, "action_capable": True,  "prompt_style": "sections"},
    "gpt-3.5":          {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  8000, "action_capable": False, "prompt_style": "plain"},
    "o1":               {"max_tokens": 4096, "temperature": 1.00, "ctx_budget": 32000, "action_capable": True,  "prompt_style": "plain"},  # o1 ignores temp

    # ── Anthropic ─────────────────────────────────────────────────────────────
    "claude-3-5-sonnet":    {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 32000, "action_capable": True,  "prompt_style": "xml"},
    "claude-3-5-haiku":     {"max_tokens": 4096, "temperature": 0.18, "ctx_budget": 16000, "action_capable": True,  "prompt_style": "xml"},
    "claude-3-opus":        {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 32000, "action_capable": True,  "prompt_style": "xml"},
    "claude-3-haiku":       {"max_tokens": 2048, "temperature": 0.20, "ctx_budget":  8000, "action_capable": True,  "prompt_style": "xml"},
    "claude-3":             {"max_tokens": 4096, "temperature": 0.15, "ctx_budget": 16000, "action_capable": True,  "prompt_style": "xml"},
}

# Sensible fallback when no profile matches
_DEFAULT: ModelProfile = {
    "max_tokens": 2500,
    "temperature": 0.25,
    "ctx_budget": 6000,
    "action_capable": True,
    "prompt_style": "sections",
}


def get_profile(model: str | None) -> ModelProfile:
    """Return the capability profile for *model*, matching by prefix (longest first)."""
    if not model:
        return _DEFAULT
    # Sort by key length descending so longer (more specific) keys match first
    for key in sorted(_PROFILES, key=len, reverse=True):
        if model.lower().startswith(key.lower()):
            return _PROFILES[key]
    return _DEFAULT


def trim_history(
    messages: list[dict[str, str]],
    budget_chars: int,
) -> list[dict[str, str]]:
    """Trim conversation history to fit within budget_chars.

    When the conversation exceeds the budget, the oldest turns are collapsed
    into a single compact summary note rather than silently dropped.  This
    preserves research continuity across long sessions.

    The system message (role="system") is always kept intact.
    budget_chars approximates token count at 4 chars/token.
    """
    system = [m for m in messages if m["role"] == "system"]
    convo  = [m for m in messages if m["role"] != "system"]

    total = sum(len(m["content"]) for m in convo)
    if total <= budget_chars:
        return system + convo

    # Collect oldest messages to summarize (drop until we have headroom)
    summarized: list[str] = []
    while total > budget_chars * 0.9 and len(convo) > 2:
        removed = convo.pop(0)
        role_label = "User" if removed["role"] == "user" else "Glossa"
        # Keep first 120 chars of each dropped turn for the summary
        snippet = removed["content"][:120].replace("\n", " ")
        summarized.append(f"{role_label}: {snippet}...")
        total -= len(removed["content"])

    if summarized:
        summary_note = (
            "[Earlier conversation summary — "
            + str(len(summarized))
            + " turns condensed]\n"
            + "\n".join(summarized)
        )
        # Inject summary as first assistant message so context is preserved
        convo.insert(0, {"role": "assistant", "content": summary_note})

    return system + convo
