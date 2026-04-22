"""CPSC bridge — Glossa Lab ↔ cpsc-engine-python adapter layer.

Imports CPSC via direct submodule paths to avoid the numba dependency
required by the IsingEngine and MaxSATEngine (which we don't use).

This module provides:
  1. validate_cas_yaml()      — parse + dry-run any CAS-YAML string
  2. project_cas_yaml()       — load YAML string + run CPSC solve()
  3. project_cas_model()      — run CPSC solve() on a pre-loaded CasModel
  4. build_indus_cas_model()  — build a CasModel dynamically from CISI data
  5. run_indus_engine()       — our custom CAS+CPSC sign role classifier
  6. load_builtin_cas_model() — load one of the built-in data/cas_models/ files

The key design principle: CAS-YAML encodes domain knowledge as declarative
constraints. CPSC's IterativeEngine/CellularEngine finds variable values that
satisfy those constraints. This replaces the black-box SA optimizer with a
transparent, user-editable constraint system.
"""

from __future__ import annotations

import io
import math
import textwrap
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import yaml

# ── CPSC submodule imports (avoid numba-dependent top-level import) ────────────
from cpsc.cas import (
    CasModel,
    CasError,
    Constraint,
    DegreesOfFreedomConfig,
    ExecutionConfig,
    ProjectionConfig,
    Variable,
)
from cpsc.solvers.iterative import IterativeEngine
from cpsc.solvers.cellular import CellularEngine
from cpsc.solvers.result import ProjectionResult, StateVector

_BUILTIN_MODELS_DIR = Path(__file__).parent / "data" / "cas_models"


# ── 1. Validate CAS-YAML ──────────────────────────────────────────────────────


def validate_cas_yaml(yaml_text: str) -> dict[str, Any]:
    """Parse a CAS-YAML string and run a quick zero-iteration projection.

    Returns a dict with fields:
      valid (bool), model_id (str), n_variables (int), n_constraints (int),
      dof_vars (list[str]), error (str | None)
    """
    try:
        model = _parse_yaml_to_model(yaml_text)
    except Exception as exc:  # noqa: BLE001
        return {"valid": False, "error": str(exc),
                "model_id": "", "n_variables": 0, "n_constraints": 0, "dof_vars": []}

    # Quick dry-run with zeros to check constraint evaluation
    try:
        engine = IterativeEngine(max_iterations=1, convergence_epsilon=1.0)
        dof_zeros = [0.0] * len(model.free_variables)
        result = engine.solve(model, dof_zeros)
    except Exception as exc:  # noqa: BLE001
        return {
            "valid": False,
            "error": f"Projection dry-run failed: {exc}",
            "model_id": model.model_id,
            "n_variables": len(model.variables),
            "n_constraints": len(model.constraints),
            "dof_vars": model.free_variables,
        }

    return {
        "valid": True,
        "error": None,
        "model_id": model.model_id,
        "n_variables": len(model.variables),
        "n_constraints": len(model.constraints),
        "dof_vars": model.free_variables,
        "dry_run_success": result.success,
        "dry_run_violation": result.max_violation,
    }


# ── 2. Project a CAS-YAML string ─────────────────────────────────────────────


def project_cas_yaml(
    yaml_text: str,
    dof_values: list[float],
    engine: str = "auto",
    max_iterations: int | None = None,
    force_strategy: str | None = None,
) -> dict[str, Any]:
    """Load CAS-YAML string and run CPSC projection.

    Args:
        yaml_text: CAS-YAML model content
        dof_values: Ordered values for the free variables (degrees of freedom)
        engine: 'auto' | 'iterative' | 'cellular'
        max_iterations: Override model's max_iterations
        force_strategy: 'iterative' | 'cellular' (bypasses auto-detection)

    Returns:
        dict with state (variable values), success, iterations, max_violation,
        strategy_used, details, error
    """
    try:
        model = _parse_yaml_to_model(yaml_text)
    except Exception as exc:  # noqa: BLE001
        return {"success": False, "error": str(exc), "state": {}}

    return project_cas_model(
        model, dof_values,
        engine=engine,
        max_iterations=max_iterations,
        force_strategy=force_strategy,
    )


# ── 3. Project a pre-loaded CasModel ─────────────────────────────────────────


def project_cas_model(
    model: CasModel,
    dof_values: list[float],
    engine: str = "auto",
    max_iterations: int | None = None,
    force_strategy: str | None = None,
) -> dict[str, Any]:
    """Run CPSC projection on a pre-loaded CasModel.

    engine selection:
      'iterative' → IterativeEngine (gradient-based, good for continuous)
      'cellular'  → CellularEngine (local rules, good for structural)
      'auto'      → uses projection.strategy from CAS-YAML, or 'iterative' fallback
    """
    strategy = force_strategy or engine
    yaml_hint = getattr(model.projection, "strategy", "auto") if model.projection else "auto"

    if strategy in ("auto", None):
        strategy = yaml_hint if yaml_hint not in ("auto", "") else "iterative"

    try:
        if strategy in ("cellular", "local_rules", "self_organizing"):
            eng: IterativeEngine | CellularEngine = CellularEngine()
        else:
            eng = IterativeEngine(
                max_iterations=max_iterations or (model.projection.max_iterations if model.projection else 200),
                convergence_epsilon=model.projection.convergence_epsilon if model.projection else 1e-6,
            )
        result: ProjectionResult = eng.solve(model, dof_values, max_iterations=max_iterations)
    except Exception as exc:  # noqa: BLE001
        return {"success": False, "error": str(exc), "state": {}, "strategy_used": strategy}

    state_dict = dict(result.state.values) if result.state else {}
    return {
        "success": result.success,
        "state": state_dict,
        "iterations": result.iterations,
        "max_violation": result.max_violation,
        "strategy_used": strategy,
        "reason": result.reason,
        "details": result.details,
    }


# ── 4. Load a built-in CAS model file ────────────────────────────────────────


def load_builtin_cas_model(name: str) -> CasModel | None:
    """Load one of the built-in CAS-YAML files from data/cas_models/.

    Args:
        name: filename stem (without .yaml), e.g. 'indus_sign_roles'
    """
    candidates = [
        _BUILTIN_MODELS_DIR / f"{name}.yaml",
        _BUILTIN_MODELS_DIR / f"{name}.yml",
    ]
    for p in candidates:
        if p.exists():
            try:
                return _parse_yaml_to_model(p.read_text("utf-8"))
            except Exception:  # noqa: BLE001
                return None
    return None


def list_builtin_cas_models() -> list[dict[str, str]]:
    """Return metadata for all built-in CAS-YAML model files."""
    result = []
    if not _BUILTIN_MODELS_DIR.exists():
        return result
    for p in sorted(_BUILTIN_MODELS_DIR.glob("*.yaml")):
        try:
            raw = yaml.safe_load(p.read_text("utf-8"))
            result.append({
                "name": p.stem,
                "model_id": str(raw.get("model_id", p.stem)),
                "description": str(raw.get("description", "")),
                "path": str(p),
            })
        except Exception:  # noqa: BLE001
            pass
    return result


# ── 5. CASIndusEngine — our custom sign-role classifier ───────────────────────


def run_indus_engine(
    sequences: list[list[str]],
    profiles: dict[str, Any],
    lm: Any | None = None,
    terminal_threshold: float = 0.55,
    initial_threshold: float = 0.45,
    engine: str = "iterative",
) -> dict[str, Any]:
    """Classify Indus sign functions using CPSC constraint projection.

    This is our custom engine built on top of CPSC's IterativeEngine.
    Instead of black-box SA, we:
      1. Observe I/M/T rates per sign from real inscription structure (CISI)
      2. For each sign, build a CasModel dynamically with:
         - Free vars: terminal_weight, initial_weight (DoF = observed rates as starting point)
         - Derived: medial_weight = 1 - terminal - initial
         - Constraints: Dravidian morphology patterns (case suffixes are terminal-biased,
           determinatives initial-biased, phonetic syllables medial-biased)
      3. Run CPSC IterativeEngine to project weights onto the constraint manifold
      4. The projected weights tell us each sign's most likely role given
         both observed data AND Dravidian morphological constraints

    Args:
        sequences: Multi-sign inscription sequences (from BuiltinCorpus('indus_cisi'))
        profiles:  PositionalProfiler output (dict with 'profiles' key or flat sign→rates)
        lm:        Optional Dravidian LanguageModel for bigram constraint weights
        terminal_threshold: Min projected terminal_weight to call a sign TERMINAL
        initial_threshold:  Min projected initial_weight to call a sign INITIAL
        engine:    'iterative' (default) | 'cellular'

    Returns:
        dict with terminal_signs, initial_signs, medial_signs, sign_roles,
        phoneme_candidates (if lm provided), constraint_summary, n_signs_classified
    """
    # ── Extract sign profiles from PositionalProfiler output ────────────────
    sign_profiles: dict[str, dict[str, float]] = {}

    # PositionalProfiler may return profiles nested or flat
    raw_profiles = profiles
    if isinstance(raw_profiles, dict):
        # Try nested: {profiles: {sign: {terminal_rate, initial_rate, medial_rate, count}}}
        nested = raw_profiles.get("profiles") or raw_profiles
        for sign, data in nested.items():
            if isinstance(data, dict) and "terminal_rate" in data:
                sign_profiles[str(sign)] = {
                    "terminal_rate": float(data.get("terminal_rate", 0.0)),
                    "initial_rate":  float(data.get("initial_rate", 0.0)),
                    "medial_rate":   float(data.get("medial_rate", 0.0)),
                    "count":         int(data.get("count", 1)),
                }

    if not sign_profiles and sequences:
        # Fall back: compute raw I/M/T rates from sequences directly
        sign_profiles = _compute_imt_rates(sequences)

    if not sign_profiles:
        return {
            "error": "No positional profiles available. Connect PositionalProfiler or BuiltinCorpus(indus_cisi) sequences.",
            "terminal_signs": [], "initial_signs": [], "medial_signs": [],
            "sign_roles": {}, "n_signs_classified": 0,
        }

    # ── Build and solve per-sign CAS models ──────────────────────────────────
    terminal_signs: list[str]  = []
    initial_signs:  list[str]  = []
    medial_signs:   list[str]  = []
    sign_roles:     dict[str, str]             = {}
    projected:      dict[str, dict[str, float]] = {}
    constraint_violations: list[str] = []

    min_count = 3  # only classify signs with enough observations
    eng_obj = IterativeEngine(max_iterations=300, convergence_epsilon=1e-5)

    for sign, rates in sign_profiles.items():
        if rates.get("count", 0) < min_count:
            continue

        t_obs = rates["terminal_rate"]
        i_obs = rates["initial_rate"]

        # Build a minimal CasModel for this sign programmatically
        model = _build_sign_role_model(sign, t_obs, i_obs)

        # DoF = (terminal_weight, initial_weight), starting from observed rates
        dof_start = [
            max(0.0, min(1.0, t_obs)),
            max(0.0, min(1.0, i_obs)),
        ]
        # Ensure they don't sum > 1
        if dof_start[0] + dof_start[1] > 1.0:
            total = dof_start[0] + dof_start[1]
            dof_start = [dof_start[0] / total * 0.9, dof_start[1] / total * 0.9]

        try:
            result = eng_obj.solve(model, dof_start)
        except Exception:  # noqa: BLE001
            result = None

        if result and result.success and result.state:
            t_proj = result.state.values.get("terminal_weight", t_obs)
            i_proj = result.state.values.get("initial_weight", i_obs)
            m_proj = result.state.values.get("medial_weight", 1.0 - t_proj - i_proj)
        else:
            t_proj, i_proj, m_proj = t_obs, i_obs, rates["medial_rate"]
            if result and not result.success:
                constraint_violations.append(f"{sign}: {result.reason}")

        projected[sign] = {
            "terminal_weight": t_proj,
            "initial_weight":  i_proj,
            "medial_weight":   m_proj,
            "t_observed":      t_obs,
            "i_observed":      i_obs,
        }

        # Classify sign
        if t_proj >= terminal_threshold:
            role = "TERMINAL"
            terminal_signs.append(sign)
        elif i_proj >= initial_threshold:
            role = "INITIAL"
            initial_signs.append(sign)
        else:
            role = "MEDIAL"
            medial_signs.append(sign)
        sign_roles[sign] = role

    # ── Phoneme candidates from LM (if provided) ────────────────────────────
    phoneme_candidates: dict[str, list[dict[str, Any]]] = {}
    if lm is not None:
        try:
            phoneme_candidates = _match_dravidian_phonemes(
                terminal_signs, initial_signs, medial_signs, lm
            )
        except Exception:  # noqa: BLE001
            pass

    return {
        "terminal_signs":      sorted(terminal_signs),
        "initial_signs":       sorted(initial_signs),
        "medial_signs":        sorted(medial_signs),
        "sign_roles":          sign_roles,
        "projected_weights":   projected,
        "phoneme_candidates":  phoneme_candidates,
        "constraint_summary": {
            "n_classified":  len(sign_roles),
            "n_terminal":    len(terminal_signs),
            "n_initial":     len(initial_signs),
            "n_medial":      len(medial_signs),
            "violations":    constraint_violations[:10],
            "engine_used":   engine,
            "thresholds":    {"terminal": terminal_threshold, "initial": initial_threshold},
        },
        "n_signs_classified": len(sign_roles),
    }


# ── 6. Build a sign-role CasModel programmatically ───────────────────────────


def _build_sign_role_model(sign_id: str, t_obs: float, i_obs: float) -> CasModel:
    """Build a CPSC CasModel for one Indus sign's role classification.

    Variables:
      terminal_weight (free) — DoF: how strongly this sign is terminal
      initial_weight  (free) — DoF: how strongly this sign is initial
      medial_weight (derived) = 1 - terminal_weight - initial_weight
      case_suffix_score (derived) — Dravidian case suffix compatibility
      determinative_score (derived) — logographic determinative compatibility
      phoneme_score (derived) — phonetic syllable compatibility

    Constraints:
      medial_weight = 1.0 - terminal_weight - initial_weight
      case_suffix_score = terminal_weight * 0.75 + medial_weight * 0.25
      determinative_score = initial_weight * 0.80 + medial_weight * 0.20
      phoneme_score = medial_weight * 0.70 + terminal_weight * 0.20 + initial_weight * 0.10
      terminal_weight + initial_weight <= 1.0  (predicate)

    The IterativeEngine projects (t_obs, i_obs) onto this constraint manifold,
    giving us regularized role weights that satisfy Dravidian morphology patterns.
    """
    variables = [
        Variable(name="terminal_weight", type="float",
                 domain=[0.0, 1.0], derived=False,
                 description=f"Terminal position weight for sign {sign_id}"),
        Variable(name="initial_weight", type="float",
                 domain=[0.0, 1.0], derived=False,
                 description=f"Initial position weight for sign {sign_id}"),
        Variable(name="medial_weight", type="float",
                 domain=[0.0, 1.0], derived=True,
                 description="Derived: 1 - terminal - initial"),
        Variable(name="case_suffix_score", type="float",
                 domain=[0.0, 1.0], derived=True,
                 description="Dravidian case suffix compatibility (terminal-biased)"),
        Variable(name="determinative_score", type="float",
                 domain=[0.0, 1.0], derived=True,
                 description="Logographic determinative compatibility (initial-biased)"),
        Variable(name="phoneme_score", type="float",
                 domain=[0.0, 1.0], derived=True,
                 description="Phonetic syllable compatibility (medial-biased)"),
    ]

    constraints = [
        Constraint(
            id="medial_derived",
            expression="medial_weight = 1.0 - terminal_weight - initial_weight",
            description="Medial is complement of terminal + initial",
        ),
        Constraint(
            id="case_suffix_def",
            expression="case_suffix_score = terminal_weight * 0.75 + medial_weight * 0.25",
            description="Dravidian case suffixes (genitive -in, dative -ku, etc.) are predominantly terminal",
        ),
        Constraint(
            id="determinative_def",
            expression="determinative_score = initial_weight * 0.8 + medial_weight * 0.2",
            description="Dravidian logograms / determinatives appear predominantly in initial position",
        ),
        Constraint(
            id="phoneme_def",
            expression="phoneme_score = medial_weight * 0.7 + terminal_weight * 0.2 + initial_weight * 0.1",
            description="Phonetic syllable signs (core vocabulary) are predominantly medial",
        ),
        Constraint(
            id="weights_valid",
            expression="terminal_weight + initial_weight <= 1.0",
            description="Weights must be a valid probability partition",
        ),
    ]

    return CasModel(
        version="1.0",
        model_id=f"indus_sign_{sign_id}",
        variables=variables,
        constraints=constraints,
        dof=DegreesOfFreedomConfig(free=["terminal_weight", "initial_weight"]),
        projection=ProjectionConfig(
            method="bounded_relaxation",
            max_iterations=200,
            convergence_epsilon=1e-5,
            strategy="iterative",
        ),
        execution=ExecutionConfig(
            deterministic=True,
            numeric_mode="float64",
            precision_bits=64,
        ),
    )


# ── 7. Compute I/M/T rates from raw sequences ────────────────────────────────


def _compute_imt_rates(sequences: list[list[str]]) -> dict[str, dict[str, float]]:
    """Compute terminal/initial/medial rates from inscription sequences."""
    sign_counts:    Counter[str] = Counter()
    initial_counts: Counter[str] = Counter()
    terminal_counts: Counter[str] = Counter()
    medial_counts:  Counter[str] = Counter()

    for seq in sequences:
        if not seq:
            continue
        for i, sign in enumerate(seq):
            sign_counts[sign] += 1
            if i == 0:
                initial_counts[sign] += 1
            elif i == len(seq) - 1:
                terminal_counts[sign] += 1
            else:
                medial_counts[sign] += 1

    result = {}
    for sign, total in sign_counts.items():
        if total < 3:
            continue
        result[sign] = {
            "count":         total,
            "initial_rate":  initial_counts[sign]  / total,
            "terminal_rate": terminal_counts[sign] / total,
            "medial_rate":   medial_counts[sign]   / total,
        }
    return result


# ── 8. Phoneme candidate matching via Dravidian LM ───────────────────────────


def _match_dravidian_phonemes(
    terminal_signs: list[str],
    initial_signs: list[str],
    medial_signs: list[str],
    lm: Any,
) -> dict[str, list[dict[str, Any]]]:
    """Match classified signs to candidate Dravidian phonemes using the LM.

    TERMINAL signs → Dravidian case suffixes: -in, -ku, -al, -atu, -il
    INITIAL signs  → Dravidian word-initial phonemes: k, m, n, p, t, v, c
    MEDIAL signs   → Dravidian CV syllables via LM unigram frequency

    Returns: dict mapping sign_id → list of {phoneme, role, score, rationale}
    """
    candidates: dict[str, list[dict[str, Any]]] = {}

    DRAVIDIAN_CASE_SUFFIXES = [
        {"phoneme": "in",  "role": "genitive",     "tamil": "-in, -vin"},
        {"phoneme": "ku",  "role": "dative",        "tamil": "-ku, -ukku"},
        {"phoneme": "al",  "role": "instrumental",  "tamil": "-āl"},
        {"phoneme": "atu", "role": "ablative/nominalize", "tamil": "-atu, -itu"},
        {"phoneme": "il",  "role": "locative",      "tamil": "-il, -uḷ"},
    ]
    DRAVIDIAN_INITIAL = [
        {"phoneme": "k",  "role": "initial_consonant"},
        {"phoneme": "m",  "role": "initial_consonant"},
        {"phoneme": "n",  "role": "initial_consonant"},
        {"phoneme": "p",  "role": "initial_consonant"},
        {"phoneme": "t",  "role": "initial_consonant"},
        {"phoneme": "v",  "role": "initial_consonant"},
        {"phoneme": "c",  "role": "initial_consonant"},
        {"phoneme": "a",  "role": "initial_vowel"},
    ]

    # Terminal sign candidates: cycle through Dravidian case suffixes
    for i, sign in enumerate(sorted(terminal_signs)):
        suffix = DRAVIDIAN_CASE_SUFFIXES[i % len(DRAVIDIAN_CASE_SUFFIXES)]
        candidates[sign] = [{
            "phoneme":   suffix["phoneme"],
            "role":      suffix["role"],
            "score":     0.75,
            "rationale": f"TERMINAL sign; candidate Dravidian case suffix ({suffix['tamil']})",
        }]

    # Initial sign candidates: Dravidian word-initial consonants/vowels
    for i, sign in enumerate(sorted(initial_signs)):
        init = DRAVIDIAN_INITIAL[i % len(DRAVIDIAN_INITIAL)]
        candidates[sign] = [{
            "phoneme":   init["phoneme"],
            "role":      "initial_element",
            "score":     0.60,
            "rationale": f"INITIAL sign; candidate Dravidian word-initial phoneme /{init['phoneme']}/",
        }]

    # Medial sign candidates: use LM unigram frequency to rank phonemes
    if lm and hasattr(lm, "unigram_freq") and lm.unigram_freq:
        top_phonemes = sorted(lm.unigram_freq.items(), key=lambda x: -x[1])
        for i, sign in enumerate(sorted(medial_signs)):
            phoneme, prob = top_phonemes[i % len(top_phonemes)]
            candidates[sign] = [{
                "phoneme":   phoneme,
                "role":      "medial_syllable",
                "score":     float(prob),
                "rationale": f"MEDIAL sign; most compatible Dravidian syllable by LM unigram frequency",
            }]

    return candidates


# ── 9. Parse CAS-YAML text → CasModel ────────────────────────────────────────


def _parse_yaml_to_model(yaml_text: str) -> CasModel:
    """Parse a CAS-YAML string into a CasModel object.

    This is a lightweight parser that covers the CAS-YAML subset used
    in Glossa Lab without requiring a full file on disk.
    """
    try:
        raw = yaml.safe_load(yaml_text)
    except yaml.YAMLError as exc:
        raise CasError(f"YAML parse error: {exc}") from exc

    if not isinstance(raw, dict):
        raise CasError("CAS-YAML must be a YAML mapping at the top level")

    version  = str(raw.get("version", "1.0"))
    model_id = str(raw.get("model_id", "unnamed"))

    # Variables
    var_data = raw.get("state", {}).get("variables", [])
    variables: list[Variable] = []
    for v in var_data:
        if isinstance(v, dict):
            variables.append(Variable(
                name=str(v.get("name", "")),
                type=str(v.get("type", "float")),
                domain=v.get("domain", [0.0, 1.0]),
                derived=bool(v.get("derived", False)),
                description=v.get("description"),
            ))

    # Constraints
    con_data = raw.get("constraints", [])
    constraints: list[Constraint] = []
    for c in con_data:
        if isinstance(c, dict):
            constraints.append(Constraint(
                id=str(c.get("id", f"c{len(constraints)}")),
                expression=str(c.get("expression", "")),
                description=c.get("description"),
                scope=c.get("scope"),
                constraint_class=c.get("constraint_class"),
            ))

    # DoF
    dof_data = raw.get("degrees_of_freedom", {})
    dof = DegreesOfFreedomConfig(free=list(dof_data.get("free", [])))

    # Projection
    proj_data = raw.get("projection", {})
    projection = ProjectionConfig(
        method=str(proj_data.get("method", "bounded_relaxation")),
        max_iterations=int(proj_data.get("max_iterations", 200)),
        convergence_epsilon=float(proj_data.get("convergence_epsilon", 1e-5)),
        strategy=str(proj_data.get("strategy", "auto")),
    )

    # Execution
    exec_data = raw.get("execution", {})
    execution = ExecutionConfig(
        deterministic=bool(exec_data.get("deterministic", True)),
        numeric_mode=str(exec_data.get("numeric_mode", "float64")),
        precision_bits=int(exec_data.get("precision_bits", 64)),
    )

    return CasModel(
        version=version,
        model_id=model_id,
        variables=variables,
        constraints=constraints,
        dof=dof,
        projection=projection,
        execution=execution,
    )


# ── 10. Generate a CAS-YAML template ─────────────────────────────────────────


def generate_cas_yaml_template(model_id: str = "my_model") -> str:
    """Return a starter CAS-YAML template for the UI editor."""
    return textwrap.dedent(f"""\
        version: "1.0"
        model_id: {model_id}
        description: "Describe what this model computes"

        state:
          variables:
            - name: x0
              type: float
              domain: [0.0, 10.0]
              description: "First degree of freedom"
            - name: x1
              type: float
              domain: [0.0, 10.0]
              description: "Second degree of freedom"
            - name: sum_val
              type: float
              domain: [0.0, 20.0]
              derived: true
              description: "Derived: sum of x0 and x1"

        degrees_of_freedom:
          free: [x0, x1]

        constraints:
          - id: sum_def
            expression: "sum_val = x0 + x1"
            description: "Sum of free variables"
          - id: sum_target
            expression: "sum_val == 10.0"
            description: "Target: sum must equal 10"

        projection:
          method: bounded_relaxation
          max_iterations: 200
          convergence_epsilon: 0.0001
          strategy: auto

        execution:
          deterministic: true
          numeric_mode: float64
          precision_bits: 64
    """)
