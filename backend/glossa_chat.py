#!/usr/bin/env python3
"""glossa_chat.py — Backend CLI for testing Glossa AI directly.

Bypasses HTTP entirely: calls call_llm() in-process with the same system
prompt as the web UI (research context + settings + action addendum).

Usage
-----
  python glossa_chat.py                         # interactive REPL
  python glossa_chat.py "what's next?"          # single shot
  python glossa_chat.py --test                  # run built-in Indus study tests
  python glossa_chat.py --test --save           # test + save results to reports/
  python glossa_chat.py --model mistral-nemo    # use a specific model (ollama)
  python glossa_chat.py --no-context            # skip research context (faster)

Key bindings (REPL mode)
------------------------
  /r      reload research context
  /clear  new conversation
  /actions show last AI-proposed actions
  /save   save conversation to reports/chat_logs/
  /quit   exit
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
from datetime import datetime
from pathlib import Path

# ── Path setup ────────────────────────────────────────────────────────────────

_HERE = Path(__file__).parent
sys.path.insert(0, str(_HERE))

_REPORTS = _HERE.parent / "reports"
_LEDGER  = _HERE.parent / "LEDGER.md"

# ── Colour helpers (ANSI, degrade gracefully on Windows) ──────────────────────

_WIN = sys.platform == "win32"

def _c(code: str, text: str) -> str:
    if _WIN:
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleMode(  # type: ignore[attr-defined]
                ctypes.windll.kernel32.GetStdHandle(-11), 7
            )
        except Exception:
            return text
    return f"\033[{code}m{text}\033[0m"

def cyan(t: str)   -> str: return _c("36", t)
def green(t: str)  -> str: return _c("32", t)
def yellow(t: str) -> str: return _c("33", t)
def red(t: str)    -> str: return _c("31", t)
def bold(t: str)   -> str: return _c("1", t)
def dim(t: str)    -> str: return _c("2", t)
def purple(t: str) -> str: return _c("35", t)

# ── Context builders (mirrored from ai_tools.py) ──────────────────────────────

def _build_research_context() -> str:
    lines: list[str] = []
    lines.append("=== GLOSSA LAB — INDUS SCRIPT DECIPHERMENT RESEARCH CONTEXT ===")

    catalog_path = _REPORTS / "sign_expansion.json"
    if catalog_path.exists():
        try:
            data = json.loads(catalog_path.read_text("utf-8"))
            cov = data.get("token_coverage", {})
            lines.append(
                f"\nCorpus: 4,410 inscriptions | 14,213 tokens | 713 sign types"
            )
            lines.append(
                f"Token coverage: {cov.get('pct', '?')}% "
                f"({cov.get('known_tokens','?')}/{cov.get('total_tokens','?')}) "
                "with current assignments"
            )
            top100 = data.get("top100_catalog", [])
            assigned = [r for r in top100 if r.get("confidence") in ("HIGH", "MED", "LOW")]
            lines.append("\nSIGN ASSIGNMENTS (current session):")
            lines.append("  Fuls  Count   T    I    M   M77  Conf   Value       Description")
            for r in sorted(assigned, key=lambda x: x.get("rank", 999)):
                lines.append(
                    f"  {r['fuls']:>4}  {r['count']:>5}  "
                    f"{r['t_rate']:.2f}  {r['i_rate']:.2f}  {r['m_rate']:.2f}  "
                    f"{r['best_m77']:>4}  {r['confidence']:>4}  "
                    f"{r['known_value']:>10}  {r.get('m77_desc','')[:20]}"
                )
        except Exception:
            lines.append("(sign catalog unavailable)")

    synth_path = _REPORTS / "decipherment_synthesis.json"
    if synth_path.exists():
        try:
            d = json.loads(synth_path.read_text("utf-8"))
            fish = d.get("fish_ranking", [])
            if fish:
                lines.append("\nFISH SIGN RANKING:")
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
            for p in patts.get("top_patterns", [])[:6]:
                lines.append(f"  {' '.join(p['pattern'])} ({p['count']}x) = {p['reading']}")
        except Exception:
            pass

    if _LEDGER.exists():
        try:
            ledger_text = _LEDGER.read_text("utf-8", errors="replace")
            ledger_lines = ledger_text.splitlines()
            last_idx = max(
                (i for i, ln in enumerate(ledger_lines) if ln.startswith("## [")),
                default=max(0, len(ledger_lines) - 80),
            )
            snippet = "\n".join(ledger_lines[last_idx:][-80:])
            lines.append("\n=== LAST LEDGER ENTRY ===")
            lines.append(snippet)
        except Exception:
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


def _build_settings_context() -> str:
    try:
        from glossa_lab.api.settings import get_key  # noqa: PLC0415
    except ImportError:
        return ""
    lines = ["\n=== CURRENT SETTINGS ==="]
    for k, label in [("mistral_api_key","Mistral"),("openai_api_key","OpenAI"),
                     ("anthropic_api_key","Anthropic"),("google_api_key","Google")]:
        v = get_key(k)
        lines.append(f"  {label}: {'set (' + v[:4] + '…)' if v else 'not set'}")
    try:
        import urllib.request  # noqa: PLC0415
        with urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2) as r:
            data = json.loads(r.read())
        names = [m["name"] for m in data.get("models", [])]
        lines.append(f"  Ollama models: {', '.join(names) or 'none'}")
    except Exception:
        lines.append("  Ollama: not reachable")
    lines.append("=== END SETTINGS ===")
    return "\n".join(lines)


_ACTION_RE = re.compile(r"%%ACTIONS%%(.*?)%%END_ACTIONS%%", re.DOTALL)


def _parse_actions(text: str) -> tuple[str, list[dict]]:
    m = _ACTION_RE.search(text)
    if not m:
        return text, []
    try:
        actions = json.loads(m.group(1).strip())
        return text[: m.start()].rstrip(), actions if isinstance(actions, list) else []
    except Exception:
        return text, []


# ── Core chat function ────────────────────────────────────────────────────────

def chat(
    messages: list[dict[str, str]],
    model: str | None = None,
    provider: str | None = None,
) -> tuple[str, list[dict]]:
    """Send messages to the LLM and return (reply_text, actions)."""
    from glossa_lab.ai_utils import call_llm  # noqa: PLC0415
    from glossa_lab.model_profiles import get_profile, trim_history  # noqa: PLC0415

    profile = get_profile(model)
    messages = trim_history(messages, budget_chars=profile["ctx_budget"] * 4)

    raw = call_llm(
        messages,
        max_tokens=profile["max_tokens"],
        temperature=profile["temperature"],
        provider_override=provider,
        model_override=model,
    )
    return _parse_actions(raw)


def build_system(use_research: bool = True, model: str | None = None) -> str:
    from glossa_lab.model_profiles import get_profile  # noqa: PLC0415
    profile = get_profile(model)
    research_ctx = ("\n\n" + _build_research_context()) if use_research else ""
    settings_ctx = _build_settings_context()
    base = (
        "You are Glossa, an expert AI research assistant for Glossa Lab — a computational "
        "linguistics platform studying the Indus Script. You have deep knowledge of "
        "information theory, computational linguistics, ancient scripts, and the specific "
        "methodology used at Glossa Lab."
    )
    if profile["prompt_style"] == "sections":
        return (
            f"### Role\n{base}\n\n"
            f"### Context{research_ctx}{settings_ctx}\n\n"
            "### Instructions\n"
            "Be concise and scientifically rigorous. Cite specific numbers. "
            "When uncertain, say so. Reference Fuls sign numbers."
        )
    return f"{base}{research_ctx}{settings_ctx}\n\nBe concise and rigorous."


# ── Output helpers ────────────────────────────────────────────────────────────

def print_response(reply: str, actions: list[dict], elapsed: float) -> None:
    print()
    print(cyan("─" * 70))
    # Wrap long lines nicely but preserve code blocks
    in_code = False
    for line in reply.split("\n"):
        if line.startswith("```"):
            in_code = not in_code
        if in_code or len(line) <= 100:
            print(line)
        else:
            for part in textwrap.wrap(line, 100):
                print(part)
    if actions:
        print()
        print(yellow(f"⚡ {len(action)} ACTION(S) PROPOSED:" if (action := actions) else ""))
        for i, a in enumerate(actions, 1):
            req = a.get("requires_approval", True)
            tag = yellow("[APPROVAL NEEDED]") if req else green("[AUTO]")
            print(f"  {i}. {bold(a.get('label','?'))} {tag}")
            print(f"     Type: {a.get('type','?')}  Params: {a.get('params',{})}")
            print(f"     {dim(a.get('description',''))}")
    print(dim(f"\n  [{elapsed:.1f}s]"))
    print(cyan("─" * 70))


# ── Built-in Indus study test suite ──────────────────────────────────────────

INDUS_TESTS = [
    (
        "context_check",
        "Confirm you have the research context loaded. List the top 5 assigned signs "
        "by Fuls number, their values, and the current token coverage percentage.",
    ),
    (
        "tmk_assignment",
        "Based on the corpus data, what are the most likely Dravidian suffix values "
        "for the top 3 unassigned TMK (terminal) signs? Rank them by T-rate and "
        "compare their profiles to the known suffixes: 817=-um, 920=-e, 760=-il, "
        "798=-ku, 752=-in. Which suffix slots are still unoccupied?",
    ),
    (
        "initial_signs",
        "The top unassigned initial-position signs are 861, 700, 741, 740, and 690. "
        "What M77 visual types best match each based on I-rate > 0.5? Which look like "
        "determinatives vs phonetic initials? Cross-reference against sign 400 (bull "
        "head, M200) and sign 520 (arrow, M028) as reference initials.",
    ),
    (
        "locked_formula",
        "The formula [520][2][240][405][501] appears exactly 27 times at Harappa. "
        "Sign 520=arrow/initial, sign 2=common medial. Signs 240, 405, 501 are "
        "unassigned. Given Harappa is the administrative centre and 27 different seal "
        "holders used this formula, what administrative title could it encode in "
        "Proto-Dravidian? What should we check in the corpus data to verify?",
    ),
    (
        "coverage_push",
        "We are at 22.4% token coverage with 16 sign assignments. To push toward "
        "30%, which 5 signs should we prioritise next, and what are their candidate "
        "values? Suggest a testing strategy: what corpus patterns would confirm or "
        "refute each assignment?",
    ),
    (
        "action_test",
        "I want to run the sign expansion analysis to get fresh data. Can you propose "
        "the appropriate experiment to run from the backend? Also suggest creating a "
        "hypothesis entry for the PA-series (signs 465-472 = PA/PE/PI/PO).",
    ),
]


def run_tests(
    model: str | None,
    provider: str | None,
    save: bool,
    verbose: bool,
) -> None:
    print(bold(purple("\n╔══════════════════════════════════════════════════════════╗")))
    print(bold(purple(  "║         GLOSSA AI — INDUS STUDY TEST SUITE              ║")))
    print(bold(purple(  "╚══════════════════════════════════════════════════════════╝")))
    print(f"  Model: {model or 'auto'} | Provider: {provider or 'auto'}\n")

    system = build_system(use_research=True, model=model)
    results: list[dict] = []

    for i, (name, prompt) in enumerate(INDUS_TESTS, 1):
        print(f"\n{bold(yellow(f'TEST {i}/{len(INDUS_TESTS)}:'))} {cyan(name)}")
        print(dim(f"  {prompt[:100]}{'…' if len(prompt)>100 else ''}"))

        messages = [
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ]

        import time
        t0 = time.time()
        try:
            reply, actions = chat(messages, model=model, provider=provider)
            elapsed = time.time() - t0
            status = green("✓ PASS")
        except Exception as e:
            reply = f"ERROR: {e}"
            actions = []
            elapsed = time.time() - t0
            status = red("✗ FAIL")

        print(f"  Status: {status}  |  {elapsed:.1f}s  |  {len(reply)} chars  |  {len(actions)} actions")

        if verbose:
            print_response(reply, actions, elapsed)
        else:
            # Show first 3 lines of response
            preview = "\n".join(reply.split("\n")[:4])
            print(dim("  " + preview.replace("\n", "\n  ")))

        results.append({
            "test": name,
            "prompt": prompt,
            "reply": reply,
            "actions": actions,
            "elapsed": round(elapsed, 2),
            "ok": not reply.startswith("ERROR"),
        })

    # Summary
    passed = sum(1 for r in results if r["ok"])
    print(f"\n{bold('Summary:')} {green(str(passed))}/{len(results)} tests passed")

    if save:
        out = _REPORTS / f"chat_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        out.write_text(json.dumps(results, indent=2, ensure_ascii=False), "utf-8")
        print(green(f"  Saved → {out}"))


# ── Interactive REPL ──────────────────────────────────────────────────────────

def repl(
    model: str | None,
    provider: str | None,
    use_research: bool,
) -> None:
    print(bold(cyan("\n╔══════════════════════════════════════════════════════════╗")))
    print(bold(cyan(  "║             GLOSSA AI — Research Terminal               ║")))
    print(bold(cyan(  "╚══════════════════════════════════════════════════════════╝")))
    print(f"  Model: {model or 'auto'}  |  Research context: {'yes' if use_research else 'no'}")
    print(dim("  /r reload context  /clear new chat  /save save log  /quit exit"))
    print()

    system = build_system(use_research=use_research, model=model)
    history: list[dict[str, str]] = [{"role": "system", "content": system}]
    last_actions: list[dict] = []
    log: list[dict] = []

    import time

    while True:
        try:
            raw = input(green("you> ")).strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break
        if not raw:
            continue

        # REPL commands
        if raw == "/quit":
            break
        if raw == "/clear":
            history = [{"role": "system", "content": system}]
            log = []
            last_actions = []
            print(dim("  [conversation cleared]"))
            continue
        if raw == "/r":
            system = build_system(use_research=True, model=model)
            history[0] = {"role": "system", "content": system}
            print(green("  [research context reloaded]"))
            continue
        if raw == "/actions":
            if not last_actions:
                print(dim("  [no actions in last response]"))
            else:
                for a in last_actions:
                    print(f"  {a.get('label')}: {a.get('type')} {a.get('params')}")
            continue
        if raw == "/save":
            out = _REPORTS / "chat_logs"
            out.mkdir(parents=True, exist_ok=True)
            fpath = out / f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            fpath.write_text(json.dumps(log, indent=2, ensure_ascii=False), "utf-8")
            print(green(f"  Saved → {fpath}"))
            continue

        history.append({"role": "user", "content": raw})
        log.append({"role": "user", "content": raw, "ts": datetime.now().isoformat()})

        print(dim("  thinking…"), end="\r")
        t0 = time.time()
        try:
            reply, actions = chat(history, model=model, provider=provider)
            elapsed = time.time() - t0
            history.append({"role": "assistant", "content": reply})
            last_actions = actions
            log.append({"role": "assistant", "content": reply, "actions": actions,
                        "ts": datetime.now().isoformat(), "elapsed": round(elapsed, 2)})
            print_response(reply, actions, elapsed)
        except Exception as e:
            elapsed = time.time() - t0
            print(red(f"\n  Error: {e}  [{elapsed:.1f}s]"))
            history.pop()  # remove the failed user message


# ── Entry point ───────────────────────────────────────────────────────────────

def main() -> None:
    ap = argparse.ArgumentParser(description="Glossa AI backend CLI")
    ap.add_argument("prompt", nargs="?", help="Single prompt (omit for interactive REPL)")
    ap.add_argument("--model",      "-m", help="Model name (e.g. mistral-nemo, qwen2.5:14b)")
    ap.add_argument("--provider",   "-p", help="Provider override: ollama|mistral|openai|anthropic")
    ap.add_argument("--test",       "-t", action="store_true", help="Run built-in Indus study tests")
    ap.add_argument("--save",       "-s", action="store_true", help="Save test results to reports/")
    ap.add_argument("--verbose",    "-v", action="store_true", help="Show full responses in test mode")
    ap.add_argument("--no-context", "-n", action="store_true", help="Skip research context")
    args = ap.parse_args()

    use_research = not args.no_context

    if args.test:
        run_tests(args.model, args.provider, args.save, args.verbose)
        return

    if args.prompt:
        import time
        system = build_system(use_research=use_research, model=args.model)
        messages = [
            {"role": "system", "content": system},
            {"role": "user",   "content": args.prompt},
        ]
        print(dim(f"  [{args.model or 'auto'}] thinking…"))
        t0 = time.time()
        try:
            reply, actions = chat(messages, model=args.model, provider=args.provider)
            print_response(reply, actions, time.time() - t0)
        except Exception as e:
            print(red(f"Error: {e}"))
        return

    repl(args.model, args.provider, use_research)


if __name__ == "__main__":
    main()
