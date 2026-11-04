"""Spec 087 Stage S3, PR-F (final batch: F2 + F10 + F11 + F12 + F13 +
F15, plus the four retire-candidate flags): equivalence proofs.

The fixtures in tests/fixtures/spec087_s3_conv_f/expected.json were
captured from the PRE-change implementations, family by family (each
family's capture commit precedes that family's conversion in this
PR). Each case replays its node's registered fn against the recorded
inputs/params and compares the entire result by canonical-JSON
equality ("full" mode), except the DravidianSyllableLM cases, whose
result carries a LanguageModel object and are compared by a pinned
field set plus a canonical digest of the model ("lm" mode).

Setup kinds:
  plain          — inputs/params exactly as recorded.
  evidence_dirs  — the indus-evidence module's _LIT_DOCS / _CLAIMS_DIR
                   constants are pointed at the pinned fixture dirs.
  loader_stubs   — phase29's F1 loader fns are replaced by stubs
                   returning the case's pinned outputs.
  meluhha_stage  — the case's pinned corpus-audit file is staged at
                   the real backend/reports/ path for the call and
                   removed afterwards (the file is absent from the
                   repo; the absence case is kind "plain" and asserts
                   the path does not exist).
  ocr_run        — glossa_lab.ai_utils.call_llm_vision is stubbed
                   with the case's pinned transcript; a two-page PDF
                   is generated in a tmp dir; tmp-dir and repo-root
                   path strings in the result are normalized before
                   comparison.
  kalyan_files   — the kalyanaraman module's lexicon/anchors path
                   constants are pointed at the case's fixture files.

Placement rationale per case lives in
specs/087-node-system-tightening/records/stage-s3-conversions.md.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from glossa_lab import experiment_graph as eg

FIXTURE_DIR = Path(__file__).parent / "fixtures" / "spec087_s3_conv_f"
FIXTURE_PATH = FIXTURE_DIR / "expected.json"
BUNDLE = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
CASES = BUNDLE["cases"]

CONVERTED_IDS = {
    "IndusLiteratureLoader": "glossa_lab.experiment_graph_indus_evidence",
    "IndusClaimsLoader": "glossa_lab.experiment_graph_indus_evidence",
    "IndusClaimTester": "glossa_lab.experiment_graph_indus_evidence",
    "IndusSealsAtMesopotamiaSummary": "glossa_lab.experiment_graph_phase22",
    "MeluhhaCorpusReporter": "glossa_lab.experiment_graph_phase22",
    "SealSignAuditor": "glossa_lab.experiment_graph_phase23",
    "LaursenTable1Auditor": "glossa_lab.experiment_graph_phase24",
    "SealSignUpgradeAuditor": "glossa_lab.experiment_graph_phase24",
    "Phase29CorpusStats": "glossa_lab.experiment_graph_phase29",
    "CISIFindspotReporter": "glossa_lab.experiment_graph_phase26",
    "ShuIlishuContactZoneFilter": "glossa_lab.experiment_graph_phase27",
    "MeluhhaCooccurrenceCheck": "glossa_lab.experiment_graph_phase30",
    "Phase20Verdict": "glossa_lab.experiment_graph_phase20",
    "Phase21Verdict": "glossa_lab.experiment_graph_phase21",
    "CISIVol3OCRNode": "glossa_lab.experiment_graph_phase28",
    "CMCatalogParser": "glossa_lab.experiment_graph_phase20",
    "DravidianSyllableLM": "glossa_lab.experiment_graph_phase30",
    "KalyanCrossValidation": "glossa_lab.experiment_graph_kalyanaraman",
}

RETIRE_IDS = {
    "ShuIlishuCandidateFilter": "glossa_lab.experiment_graph_phase26",
    "Phase22Verdict": "glossa_lab.experiment_graph_phase22",
    "Phase23Verdict": "glossa_lab.experiment_graph_phase23",
    "Phase24Verdict": "glossa_lab.experiment_graph_phase24",
}

PRIMITIVE_IDS = [
    "JsonRecordDirLoader",
    "PositionalClaimTester",
    "RecordGroupSummary",
    "CorpusComparisonStats",
    "PrefixFindspotAssigner",
    "CorpusCooccurrenceCheck",
    "PredictionVerdictAggregator",
    "VisionOCRNode",
    "CatalogTextParser",
    "SyllableLMLoader",
    "LexiconCrossValidator",
]


def _key(k):
    if isinstance(k, str):
        return k
    if k is None:
        return "null"
    if isinstance(k, bool):
        return "true" if k else "false"
    return str(k)


def _norm(o):
    if isinstance(o, dict):
        return {_key(k): _norm(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [_norm(v) for v in o]
    return o


def _canon(obj) -> str:
    return json.dumps(_norm(obj), sort_keys=True, ensure_ascii=False, default=str)


def _norm_paths(obj, replacements):
    if isinstance(obj, dict):
        return {k: _norm_paths(v, replacements) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_norm_paths(v, replacements) for v in obj]
    if isinstance(obj, str):
        for src, dst in replacements:
            obj = obj.replace(src, dst)
        return obj
    return obj


def _run_case(case, monkeypatch, tmp_path):
    fn = eg.ATOMIC_NODES[case["node"]].fn
    setup = case["setup"]
    kind = setup["kind"]
    if kind == "plain":
        return fn(case["inputs"], case["params"])
    if kind == "evidence_dirs":
        from glossa_lab import experiment_graph_indus_evidence as ev

        monkeypatch.setattr(ev, "_LIT_DOCS", FIXTURE_DIR / "f2_lit_docs")
        monkeypatch.setattr(ev, "_CLAIMS_DIR", FIXTURE_DIR / "f2_claims")
        return fn(case["inputs"], case["params"])
    if kind == "loader_stubs":
        from glossa_lab import experiment_graph_phase29 as p29

        monkeypatch.setattr(
            p29, "_mathematica_epigraphica_loader",
            lambda inputs, params: setup["fuls"])
        monkeypatch.setattr(
            p29, "_icit_corpus_loader",
            lambda inputs, params: setup["icit"])
        return fn(case["inputs"], case["params"])
    if kind == "meluhha_stage":
        import shutil

        target = (
            Path(eg.__file__).resolve().parent.parent
            / "reports" / "meluhha_corpus_audit.json"
        )
        assert not target.exists(), (
            "named pin: backend/reports/meluhha_corpus_audit.json is "
            "absent from the repo; the stage setup requires that state"
        )
        shutil.copyfile(FIXTURE_DIR / setup["file"], target)
        try:
            return fn(case["inputs"], case["params"])
        finally:
            target.unlink(missing_ok=True)
    if kind == "root_normalize":
        result = fn(case["inputs"], case["params"])
        root = str(Path(eg.__file__).resolve().parent.parent.parent)
        return _norm_paths(result, [(root, "<ROOT>")])
    if kind == "ocr_run":
        import fitz

        from glossa_lab import ai_utils

        pdf = tmp_path / "catalog.pdf"
        doc = fitz.open()
        for i in range(2):
            page = doc.new_page()
            page.insert_text((72, 72), f"synthetic page {i + 1}")
        doc.save(str(pdf))
        doc.close()
        params = {
            k: (v.replace("{TMP}", str(tmp_path)) if isinstance(v, str) else v)
            for k, v in case["params"].items()
        }
        prompts: list[str] = []
        state = {"n": 0}
        transcripts = setup["transcripts"]
        fails = {int(k): v for k, v in setup["fail_calls"].items()}

        def stub(prompt, data_uri):
            prompts.append(prompt)
            state["n"] += 1
            if state["n"] in fails:
                raise RuntimeError(fails[state["n"]])
            return transcripts[state["n"] - 1]

        monkeypatch.setattr(ai_utils, "call_llm_vision", stub)
        result = fn(case["inputs"], params)
        merged = dict(result)
        merged["written_records"] = json.loads(
            Path(params["output_path"]).read_text("utf-8"))
        merged["prompts_seen"] = prompts
        return _norm_paths(merged, [(str(tmp_path), "{TMP}")])
    if kind == "kalyan_files":
        from glossa_lab import experiment_graph_kalyanaraman as kal

        absent = FIXTURE_DIR / "f15_absent.json"
        monkeypatch.setattr(
            kal, "_LEXICON_PATH",
            FIXTURE_DIR / setup["lexicon"] if setup["lexicon"] else absent)
        monkeypatch.setattr(
            kal, "_ANCHORS_PATH",
            FIXTURE_DIR / setup["anchors"] if setup["anchors"] else absent)
        return fn(case["inputs"], case["params"])
    raise AssertionError(f"unknown setup kind {kind!r}")


def _lm_digest(lm) -> str:
    import hashlib

    payload = {
        "symbols": lm.symbols, "alphabet": lm.alphabet, "size": lm.size,
        "ranked": lm.ranked, "unigram_freq": lm.unigram_freq,
        "bigram_freq": {f"{a}|{b}": p for (a, b), p in lm.bigram_freq.items()},
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True, default=str).encode()
    ).hexdigest()


@pytest.mark.parametrize("case", CASES, ids=[c["id"] for c in CASES])
def test_converted_node_replays_prechange_output(case, monkeypatch, tmp_path):
    result = _run_case(case, monkeypatch, tmp_path)
    if case["mode"] == "lm":
        got = {
            "language": result["language"],
            "n_bigrams": result["n_bigrams"],
            "n_syllables": result["n_syllables"],
            "verdict": result["verdict"],
            "lm_digest": _lm_digest(result["lm"]),
        }
        assert got == case["expected"]
    else:
        assert _canon(result) == _canon(case["expected"])


def test_converted_ids_are_legacy_and_keep_their_fn_module():
    data = json.loads(
        (
            Path(eg.__file__).parent / "spec087_s2_legacy_ids.json"
        ).read_text(encoding="utf-8")
    )
    assert set(data["s3_additions"]["PR-F (F2+F10+F11+F12+F13+F15)"]) == set(
        CONVERTED_IDS
    )
    assert set(data["s3_additions"]["PR-F retire-candidates"]) == set(RETIRE_IDS)
    for node_id, module in {**CONVERTED_IDS, **RETIRE_IDS}.items():
        node = eg.ATOMIC_NODES[node_id]
        assert node.legacy is True, node_id
        assert node.fn.__module__ == module, node_id


def test_new_primitives_are_in_the_default_palette(client):
    default_ids = {
        entry["id"] for entry in client.get("/api/v1/experiment-graphs/catalog").json()
    }
    full_ids = {
        entry["id"]
        for entry in client.get(
            "/api/v1/experiment-graphs/catalog?include_legacy=true"
        ).json()
    }
    for primitive_id in PRIMITIVE_IDS:
        assert primitive_id in default_ids, primitive_id
        assert eg.ATOMIC_NODES[primitive_id].legacy is False
    for node_id in {**CONVERTED_IDS, **RETIRE_IDS}:
        assert node_id not in default_ids, node_id
        assert node_id in full_ids, node_id
