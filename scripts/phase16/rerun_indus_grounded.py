"""Phase-16: re-run multi-hypothesis ranker on M77 with empirically-grounded
CAS-YAMLs.

What this does:
  1. Load the M77 sign sequence (Mahadevan 1977: 1669 inscriptions, 5361
     signs as space-separated 3-digit codes in reports/mahadevan_corpus_flat.txt).
  2. Compute the same 8 language-signature DoFs as Phase B
     (zipf_alpha, zipf_r2, mi_gamma, mi_r2_pow, eps2/eps3, h1_norm, h1_nats).
  3. Load each of 5 CAS-YAMLs:
        dravidian_morphology
        indo_aryan_morphology
        sumerian_morphology
        akkadian_morphology
        vedic_kalyanaraman_morphology
  4. Parse each constraint expression (we support the simple forms
     "<var> >= <num>" / "<var> <= <num>" / "<var> > <num>" / "<var> < <num>").
     Each derived <score>_def expression is computed too.
  5. For each CAS-YAML, compute the per-constraint *normalized violation* of
     M77's measured DoFs, take the max as max_violation, rank hypotheses by
     ascending max_violation.
  6. Write reports/phase16_indus_grounded_rerun.json.

Run:
    py scripts/phase16/rerun_indus_grounded.py
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

# Reuse measurement functions from the Phase-B script
SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))
from measure_signature_dofs import measure_corpus  # type: ignore

ROOT = SCRIPT_DIR.parents[1]
M77_PATH = ROOT / "reports" / "mahadevan_corpus_flat.txt"
CAS_DIR = ROOT / "backend" / "glossa_lab" / "data" / "cas_models"
OUT_DIR = ROOT / "reports"
OUT_PATH = OUT_DIR / "phase16_indus_grounded_rerun.json"

CAS_YAMLS = [
    "dravidian_morphology.yaml",
    "indo_aryan_morphology.yaml",
    "sumerian_morphology.yaml",
    "akkadian_morphology.yaml",
    "vedic_kalyanaraman_morphology.yaml",
]


# ---------------------------------------------------------------------------
# YAML constraint loader (zero-dep; pyyaml is optional and we don't want to
# require it for this script to run).
# ---------------------------------------------------------------------------

CONSTRAINT_RE = re.compile(
    r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*(>=|<=|>|<|==|=)\s*([+\-]?\d+(?:\.\d+)?)\s*$"
)
DEF_RE = re.compile(
    r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)\s*$"
)
NUM_RE = re.compile(r"[+\-]?\d+(?:\.\d+)?")


def parse_yaml_constraints(path: Path) -> dict:
    """Tiny line-based YAML reader that picks up the constraints[] expressions
    and the model_id. We don't need full YAML parsing -- just to find lines
    of the form '    expression: \"<var> >= <num>\"' inside the constraints
    list and the top-level model_id."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    model_id = None
    constraints = []
    derived = []
    in_constraints = False
    cur = None
    for raw in lines:
        line = raw.rstrip()
        if line.startswith("model_id:"):
            model_id = line.split(":", 1)[1].strip()
        if line.strip() == "constraints:":
            in_constraints = True
            continue
        if in_constraints:
            if not line.startswith(" ") and line.strip():
                in_constraints = False  # next top-level key
            elif line.lstrip().startswith("- id:"):
                if cur is not None:
                    if cur.get("expression"):
                        constraints.append(cur)
                cur = {"id": line.split(":", 1)[1].strip().strip('"').strip("'")}
            elif line.lstrip().startswith("expression:"):
                expr = line.split(":", 1)[1].strip().strip('"').strip("'")
                if cur is not None:
                    cur["expression"] = expr
            elif line.lstrip().startswith("description:"):
                desc = line.split(":", 1)[1].strip().strip('"').strip("'")
                if cur is not None:
                    cur["description"] = desc
    if cur is not None and cur.get("expression"):
        constraints.append(cur)

    # Split into hard constraints vs derived-score definitions
    parsed_hard = []
    parsed_derived = []
    for c in constraints:
        expr = c["expression"]
        m = CONSTRAINT_RE.match(expr)
        if m:
            parsed_hard.append({
                "id": c["id"],
                "var": m.group(1),
                "op": m.group(2),
                "value": float(m.group(3)),
                "raw": expr,
                "description": c.get("description", ""),
            })
            continue
        m = DEF_RE.match(expr)
        if m:
            parsed_derived.append({
                "id": c["id"],
                "var": m.group(1),
                "rhs": m.group(2),
                "raw": expr,
                "description": c.get("description", ""),
            })
            continue
        # Otherwise unrecognized
        parsed_hard.append({
            "id": c["id"], "var": None, "op": None, "value": None,
            "raw": expr, "unparsed": True,
            "description": c.get("description", ""),
        })

    return {
        "model_id": model_id,
        "yaml_path": str(path),
        "constraints": parsed_hard,
        "derived": parsed_derived,
    }


# ---------------------------------------------------------------------------
# Violation computation
# ---------------------------------------------------------------------------

def violation_amount(measured: float, op: str, threshold: float) -> float:
    """Return the *normalized signed* violation magnitude for one constraint.
    0 = constraint satisfied. >0 = violated; the magnitude is how far measured
    is from the bound, divided by max(|threshold|, 1) for unit-free comparison.
    """
    denom = max(abs(threshold), 1.0)
    if op in (">=", ">"):
        if measured >= threshold:
            return 0.0
        return (threshold - measured) / denom
    if op in ("<=", "<"):
        if measured <= threshold:
            return 0.0
        return (measured - threshold) / denom
    if op in ("==", "="):
        return abs(measured - threshold) / denom
    return 0.0


def evaluate_derived(rhs: str, ctx: dict) -> float:
    """Evaluate the simple linear combinations like
        a * 0.20 + b * 0.20 + c * 1.0 + d * 1.5 + e * 0.25
    Walk numeric tokens replacing free variables with their measured values."""
    # Replace each variable name with its measured value (or 0 if missing).
    expr = rhs
    # Substitute identifiers
    def repl(match: re.Match) -> str:
        name = match.group(0)
        if name in ctx:
            return str(ctx[name])
        return name
    # Variable names are sequences of [A-Za-z_][A-Za-z0-9_]*
    expr = re.sub(r"[A-Za-z_][A-Za-z0-9_]*", repl, expr)
    # Whitelist arithmetic eval: only numbers, +-*/() and whitespace remain
    if not re.match(r"^[\s\d\.\+\-\*/\(\)]+$", expr):
        return float("nan")
    try:
        return float(eval(expr, {"__builtins__": {}}, {}))
    except Exception:
        return float("nan")


def project_hypothesis(yaml_data: dict, measured: dict) -> dict:
    """Compute per-constraint violations + max_violation + score for one CAS-YAML."""
    per_constraint = []
    max_v = 0.0
    n_violations = 0
    for c in yaml_data["constraints"]:
        if c.get("unparsed"):
            per_constraint.append({**c, "violation": None})
            continue
        var = c["var"]
        if var not in measured:
            per_constraint.append({**c, "violation": None, "reason": "var not measured"})
            continue
        v = violation_amount(measured[var], c["op"], c["value"])
        per_constraint.append({**c, "measured": measured[var], "violation": round(v, 4)})
        if v > 0:
            n_violations += 1
        if v > max_v:
            max_v = v
    score_value = None
    score_var = None
    derived_eval = []
    score_def = next((d for d in yaml_data["derived"] if d["id"].endswith("_score_def")), None)
    if score_def is not None:
        # ctx = measured + any prior derived (but we only have linear-on-DoFs)
        ctx = dict(measured)
        score_value = evaluate_derived(score_def["rhs"], ctx)
        score_var = score_def["var"]
        derived_eval.append({"id": score_def["id"], "var": score_var,
                             "value": (round(score_value, 4) if score_value == score_value else None),
                             "raw": score_def["raw"]})
    return {
        "model_id": yaml_data["model_id"],
        "max_violation": round(max_v, 4),
        "n_violations": n_violations,
        "score_var": score_var,
        "score_value": (round(score_value, 4) if (score_value is not None and score_value == score_value) else None),
        "constraints": per_constraint,
        "derived": derived_eval,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def load_m77(path: Path) -> list[str]:
    """Load M77 sign sequence: concatenate all inscriptions."""
    out: list[str] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            tokens = line.strip().split()
            out.extend(tokens)
    return out


def main() -> int:
    if not M77_PATH.exists():
        print(f"ERROR: M77 not found at {M77_PATH}", file=sys.stderr)
        return 1

    print(f"Loading M77: {M77_PATH}", file=sys.stderr)
    seq = load_m77(M77_PATH)
    print(f"  {len(seq)} signs across {len(open(M77_PATH).readlines())} inscriptions", file=sys.stderr)

    measured = measure_corpus("indus_m77", seq, note="M77 Mahadevan 1977 sign stream")
    print(f"\nM77 measured DoFs:", file=sys.stderr)
    for k in ("zipf_alpha", "zipf_r2", "mi_gamma", "mi_r2_pow",
              "epistatic_2nd_norm", "epistatic_3rd_norm", "h1_norm", "h1_nats"):
        print(f"  {k:24s} = {measured[k]}", file=sys.stderr)

    # Build a measured-vars-only dict for projection
    measured_vars = {k: measured[k] for k in (
        "zipf_alpha", "zipf_r2", "mi_gamma", "mi_r2_pow",
        "epistatic_2nd_norm", "epistatic_3rd_norm", "h1_norm", "h1_nats"
    ) if measured[k] == measured[k]}  # exclude NaN

    # Project against each CAS-YAML
    print(f"\nProjecting M77 through {len(CAS_YAMLS)} CAS-YAMLs ...", file=sys.stderr)
    projections = []
    for fname in CAS_YAMLS:
        path = CAS_DIR / fname
        if not path.exists():
            print(f"  SKIP (missing): {fname}", file=sys.stderr)
            continue
        yaml_data = parse_yaml_constraints(path)
        proj = project_hypothesis(yaml_data, measured_vars)
        projections.append(proj)
        score_str = f"score={proj['score_value']}" if proj['score_value'] is not None else "score=N/A"
        print(f"  {proj['model_id']:32s}  max_violation={proj['max_violation']:.4f}  "
              f"n_violated={proj['n_violations']}  {score_str}", file=sys.stderr)

    # Rank by max_violation (lower = better)
    ranked = sorted(projections, key=lambda p: (p["max_violation"], -1 * (p.get("score_value") or 0)))
    print("\n=== Phase-16 Hypothesis Ranking (lower max_violation = better fit) ===", file=sys.stderr)
    for i, p in enumerate(ranked, 1):
        score_str = f"score={p['score_value']}" if p['score_value'] is not None else ""
        print(f"  {i}.  {p['model_id']:32s}  max_violation={p['max_violation']:.4f}  {score_str}", file=sys.stderr)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = {
        "phase": "phase16",
        "purpose": "M77 multi-hypothesis projection with empirically-grounded CAS-YAMLs",
        "m77_measured": measured,
        "ranked_hypotheses": [
            {
                "rank": i,
                "model_id": p["model_id"],
                "max_violation": p["max_violation"],
                "n_violations": p["n_violations"],
                "score_var": p["score_var"],
                "score_value": p["score_value"],
            }
            for i, p in enumerate(ranked, 1)
        ],
        "details": projections,
    }
    with OUT_PATH.open("w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2)
    print(f"\nWrote {OUT_PATH}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
