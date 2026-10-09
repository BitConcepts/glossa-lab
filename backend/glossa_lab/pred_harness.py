"""Phase-119 (spec 018) — PRED-2026 evaluation harness core.

Implements the frozen spec 018: canonical sign map + CGSA
class sets (section 3), source-class evaluability gate
(section 4), deduplication (section 5), mechanical scoring
of the registered PRED-2026-001..003 criteria (section 6),
ingestion adapters with provenance (section 7), and the
labelled dry-run regime (section 8).

The scoring code path is reachable only through `evaluate`,
which enforces the section 6.1 gates (qualifying class,
complete provenance, unmapped-share guard, verdict lock,
multi-site input for PRED-2026-003) before any criterion
statistic exists. `dry_run` shares only ingestion and dedup
with `evaluate`; it computes counts and sign-set coverage
and cannot produce a rate, a conformance fraction, or a
verdict.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

UNK = "UNK"
DRY_RUN_LABEL = "HARNESS DRY RUN — NOT A PRED EVALUATION"
CAVEAT_C1 = (
    "Class features derive in part from a mayig ICIT feature "
    "extract; this corpus is the registered withheld data but "
    "is derivation-adjacent in part."
)
UNMAPPED_SHARE_LIMIT = 0.25

SOURCE_CLASSES = (
    "rmrl_concordance",
    "image_transcription",
    "future_concordance",
    "icit_full",
    "icit_lineage_derivative",
    "derivation_corpus",
)

_INDEPENDENT = ("rmrl_concordance", "image_transcription",
                "future_concordance")

# Spec section 4 evaluability matrix: prediction -> qualifying
# classes. icit_full qualifies as the registered target under
# caveat C1; lineage derivatives and the derivation corpus
# never qualify.
EVALUABILITY = {
    "PRED-2026-001": _INDEPENDENT + ("icit_full",),
    "PRED-2026-002": _INDEPENDENT + ("icit_full",),
    "PRED-2026-003": _INDEPENDENT + ("icit_full",),
}


@dataclass(frozen=True)
class Prediction:
    pid: str
    kind: str  # "rate" | "template"
    prediction_text: str
    criterion_text: str
    sign_set_name: str = ""  # "TERMINAL" | "INITIAL" (rate kind)
    rate: str = ""  # "end" | "start"
    threshold: float = 0.0
    pass_count: int = 0  # rate kind: signs that must meet it
    # Explicit sign list override (used by synthetic toy
    # predictions in tests; the registered predictions leave
    # this empty and derive their set from the frozen classes).
    sign_set: tuple = ()


PREDICTIONS = {
    "PRED-2026-001": Prediction(
        pid="PRED-2026-001", kind="rate", sign_set_name="TERMINAL",
        rate="end", threshold=0.45, pass_count=10,
        prediction_text=(
            "Signs classified as TERMINAL by the CGSA model will "
            "have end_rate ≥ 0.45 in the ICIT full corpus (6,800 "
            "inscriptions) when it becomes available."),
        criterion_text=(
            "≥ 10 of the 14 current TERMINAL signs show end_rate "
            "≥ 0.45 in ICIT data")),
    "PRED-2026-002": Prediction(
        pid="PRED-2026-002", kind="rate", sign_set_name="INITIAL",
        rate="start", threshold=0.45, pass_count=8,
        prediction_text=(
            "Signs classified as INITIAL by the CGSA model will "
            "have start_rate ≥ 0.45 in the ICIT full corpus."),
        criterion_text=(
            "≥ 8 of the 12 current INITIAL signs show start_rate "
            "≥ 0.45 in ICIT data")),
    "PRED-2026-003": Prediction(
        pid="PRED-2026-003", kind="template", threshold=0.70,
        prediction_text=(
            "The 3-slot INITIAL-MEDIAL-TERMINAL template "
            "structure will account for ≥ 70% of inscription "
            "templates in any newly acquired multi-site dataset."),
        criterion_text="Template coverage ≥ 70% in held-out corpus"),
}


# ---------------------------------------------------------------- §3 map

def load_sign_classes(inventory_csv: Path) -> dict[str, str]:
    """Frozen class rule (spec section 3): parpola_1982 rows
    with corpus_freq >= 10; TERMINAL end_rate >= 0.55, else
    INITIAL start_rate >= 0.55, else MEDIAL internal_rate
    >= 0.70, else MIXED. Returns {P sign: label}."""
    classes: dict[str, str] = {}
    with open(inventory_csv, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["numbering_system"] != "parpola_1982":
                continue
            if int(row["corpus_freq"] or 0) < 10:
                continue
            end = float(row["end_rate"] or 0)
            start = float(row["start_rate"] or 0)
            internal = float(row["internal_rate"] or 0)
            if end >= 0.55:
                label = "TERMINAL"
            elif start >= 0.55:
                label = "INITIAL"
            elif internal >= 0.70:
                label = "MEDIAL"
            else:
                label = "MIXED"
            classes[row["sign_id"]] = label
    return classes


def _resolve_claims(claims: dict[str, list[tuple[int, str]]]) -> tuple[dict[str, str], set[str]]:
    """Conflict rule (spec section 3): highest corpus_freq,
    tie -> lowest P number; residual tie -> ambiguous."""
    out: dict[str, str] = {}
    ambiguous: set[str] = set()
    for src, lst in claims.items():
        targets = {p for _, p in lst}
        if len(targets) == 1:
            out[src] = lst[0][1]
            continue
        ranked = sorted(lst, key=lambda x: (-x[0], x[1]))
        if ranked[0][0] > ranked[1][0]:
            out[src] = ranked[0][1]
        else:
            ambiguous.add(src)
    return out, ambiguous


def build_sign_maps(registry_csv: Path) -> dict:
    """Canonical M->P and W->P maps from the primary registry
    (spec section 3). Wells codes are key-normalized with
    str(int(code)) before lookup (Phase-115 lesson)."""
    m_claims: dict[str, list[tuple[int, str]]] = {}
    w_claims: dict[str, list[tuple[int, str]]] = {}
    with open(registry_csv, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            if row["numbering_system"] != "parpola_1982":
                continue
            p = row["parpola_id"]
            freq = int(row["corpus_freq"] or 0)
            for m in (row["mahadevan_ids"] or "").split("|"):
                m = m.strip()
                if m:
                    m_claims.setdefault(m, []).append((freq, p))
            for w in (row["wells_ids"] or "").split("|"):
                w = w.strip().lstrip("Ww")
                if not w:
                    continue
                key = str(int(w)) if w.isdigit() else w
                w_claims.setdefault(key, []).append((freq, p))
    m2p, m_amb = _resolve_claims(m_claims)
    w2p, w_amb = _resolve_claims(w_claims)
    return {"m2p": m2p, "w2p": w2p,
            "m_ambiguous": m_amb, "w_ambiguous": w_amb}


class SignMapper:
    """Maps source sign codes to canonical P space (spec §3).
    Unknown -> UNK (unmapped); ambiguous -> UNK (ambiguous)."""

    def __init__(self, maps: dict):
        self.m2p = maps["m2p"]
        self.w2p = maps["w2p"]
        self.m_amb = maps["m_ambiguous"]
        self.w_amb = maps["w_ambiguous"]

    def map_m(self, code: str, stats: Counter) -> str:
        if code in self.m_amb:
            stats["ambiguous"] += 1
            return UNK
        p = self.m2p.get(code)
        if p is None:
            stats["unmapped"] += 1
            return UNK
        return p

    def map_w(self, code: str, stats: Counter) -> str:
        key = str(int(code)) if str(code).isdigit() else str(code)
        if key in self.w_amb:
            stats["ambiguous"] += 1
            return UNK
        p = self.w2p.get(key)
        if p is None:
            stats["unmapped"] += 1
            return UNK
        return p


# ---------------------------------------------------------------- dataset

@dataclass
class IngestedDataset:
    name: str
    source_class: str
    records: list[dict]  # {inscription_id, site, tokens:[P|UNK]}
    provenance: dict
    stats: dict = field(default_factory=dict)

    @property
    def content_hash(self) -> str:
        canon = json.dumps(
            {"source_class": self.source_class,
             "records": [[r["inscription_id"], r["site"], r["tokens"]]
                         for r in self.records]},
            sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(canon.encode("utf-8")).hexdigest()

    @property
    def unmapped_share(self) -> float:
        tokens = self.stats.get("tokens", 0)
        if not tokens:
            return 1.0
        bad = (self.stats.get("tokens_unmapped", 0)
               + self.stats.get("tokens_ambiguous", 0))
        return bad / tokens


def _finalize(name, source_class, records, raw_stats, provenance):
    stats = {
        "inscriptions": len(records),
        "tokens": sum(len(r["tokens"]) for r in records),
        "tokens_unmapped": raw_stats["unmapped"],
        "tokens_ambiguous": raw_stats["ambiguous"],
        "distinct_signs": len({t for r in records for t in r["tokens"]
                                if t != UNK}),
    }
    prov = dict(provenance)
    prov["source_class"] = source_class
    prov["as_built"] = dict(stats)
    return IngestedDataset(name=name, source_class=source_class,
                           records=records, provenance=prov, stats=stats)


def _read_table(path: Path):
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".json":
        return json.loads(text), text
    rows = list(csv.DictReader(text.splitlines()))
    return rows, text


def adapt_rmrl_concordance(path: Path, mapper: SignMapper,
                           name: str, license_text: str,
                           source_desc: str) -> IngestedDataset:
    """RMRL-style concordance export: records with `site` and a
    whitespace-separated Mahadevan sign sequence (`signs`)."""
    data, text = _read_table(path)
    if isinstance(data, dict):
        data = data["inscriptions"]
    stats = Counter()
    records = []
    for i, row in enumerate(data):
        codes = str(row.get("signs", "")).split()
        tokens = [mapper.map_m(c, stats) for c in codes]
        records.append({"inscription_id": str(row.get("inscription_id", i)),
                        "site": row.get("site"),
                        "tokens": tokens})
    prov = {"date": None, "name": name, "source": source_desc,
            "license": license_text, "status": "ingested",
            "input_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "text_rule": "one record per inscription; signs field "
                         "split on whitespace as Mahadevan codes",
            "unit_rule": "one source record = one inscription"}
    return _finalize(name, "rmrl_concordance", records, stats, prov)


def adapt_image_transcription(path: Path, mapper: SignMapper,
                              name: str, license_text: str,
                              source_desc: str) -> IngestedDataset:
    """Image-derived transcription table: records with `site`
    and Wells sign codes (`wells_codes`, whitespace-separated,
    possibly zero-padded; optional `confidences` carried into
    provenance, unused by scoring in this version)."""
    data, text = _read_table(path)
    if isinstance(data, dict):
        data = data["inscriptions"]
    stats = Counter()
    records = []
    n_conf = 0
    for i, row in enumerate(data):
        codes = str(row.get("wells_codes", "")).split()
        tokens = [mapper.map_w(c, stats) for c in codes]
        if row.get("confidences"):
            n_conf += 1
        records.append({"inscription_id": str(row.get("inscription_id", i)),
                        "site": row.get("site"),
                        "tokens": tokens})
    prov = {"date": None, "name": name, "source": source_desc,
            "license": license_text, "status": "ingested",
            "input_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "text_rule": "one record per inscription; wells_codes "
                         "split on whitespace, key-normalized "
                         "str(int(code)) before lookup",
            "unit_rule": "one source record = one inscription",
            "records_with_confidences": n_conf}
    return _finalize(name, "image_transcription", records, stats, prov)


def adapt_future_concordance(path: Path, mapper: SignMapper,
                             name: str, license_text: str,
                             source_desc: str) -> IngestedDataset:
    """Future concordance: JSON records with `site` and
    P-number sequences (`signs` list). Unknown P -> UNK."""
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    if isinstance(data, dict):
        data = data["inscriptions"]
    known_p = set(mapper.m2p.values()) | set(mapper.w2p.values())
    stats = Counter()
    records = []
    for i, row in enumerate(data):
        tokens = []
        for code in row.get("signs", []):
            if code in known_p:
                tokens.append(code)
            else:
                stats["unmapped"] += 1
                tokens.append(UNK)
        records.append({"inscription_id": str(row.get("inscription_id", i)),
                        "site": row.get("site"),
                        "tokens": tokens})
    prov = {"date": None, "name": name, "source": source_desc,
            "license": license_text, "status": "ingested",
            "input_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "text_rule": "one record per inscription; signs taken "
                         "as Parpola numbers verbatim",
            "unit_rule": "one source record = one inscription"}
    return _finalize(name, "future_concordance", records, stats, prov)


def adapt_converted_layer(path: Path, mapper: SignMapper,
                          name: str) -> IngestedDataset:
    """Phase-115 converted layer format ({source, inscriptions:
    [[M...], ...]}). Dry-run only; class is fixed to
    icit_lineage_derivative (spec sections 4, 7)."""
    text = path.read_text(encoding="utf-8")
    data = json.loads(text)
    stats = Counter()
    records = []
    for i, seq in enumerate(data["inscriptions"]):
        tokens = [t if t == UNK else mapper.map_m(t, stats) for t in seq]
        records.append({"inscription_id": f"L{i:06d}", "site": None,
                        "tokens": tokens})
    prov = {"date": None, "name": name,
            "source": data.get("source", ""),
            "license": "ICIT via Lipi repository CSV export, "
                       "mirrored (MIT) in field-cady/"
                       "indus_valley_script_corpus",
            "status": "dry-run-only",
            "input_sha256": hashlib.sha256(text.encode()).hexdigest(),
            "text_rule": "converted layer sequences verbatim; "
                         "M codes mapped to P space per spec "
                         "section 3; UNK sentinels preserved",
            "unit_rule": "one layer entry = one inscription"}
    return _finalize(name, "icit_lineage_derivative", records, stats, prov)


# ---------------------------------------------------------------- §5 dedup
# The frozen §5 implementation lives in glossa_lab.dedup (lifted
# verbatim by Phase-130 / spec 021 so the harness and the intake
# pipeline share one implementation — no behaviour change).
# Re-exported here so existing imports (`from glossa_lab.pred_harness
# import dedup`) keep working unchanged.
from glossa_lab.dedup import dedup, levenshtein_le1  # noqa: E402,F401

_lev_le1 = levenshtein_le1


# ---------------------------------------------------------------- §6 scoring

class NotEvaluable(Exception):
    """Raised by the section 6.1 gates; carries the failed
    condition. No criterion statistic exists when this is
    raised."""

    def __init__(self, reason: str):
        super().__init__(reason)
        self.reason = reason


_PROVENANCE_REQUIRED = ("name", "source", "license", "status",
                        "input_sha256", "text_rule", "unit_rule")


def _check_gates(pred: Prediction, ds: IngestedDataset,
                 lock: set) -> None:
    # The frozen matrix binds the three registered predictions;
    # any other (synthetic) prediction defaults to the
    # independent classes only.
    qualifying = EVALUABILITY.get(pred.pid, _INDEPENDENT)
    if ds.source_class not in qualifying:
        raise NotEvaluable(
            f"source class {ds.source_class} does not qualify "
            f"for {pred.pid} (spec section 4)")
    prov = ds.provenance or {}
    missing = [k for k in _PROVENANCE_REQUIRED if not prov.get(k)]
    if missing:
        raise NotEvaluable(f"provenance incomplete: {missing}")
    if ds.unmapped_share > UNMAPPED_SHARE_LIMIT:
        raise NotEvaluable(
            f"unmapped+ambiguous token share "
            f"{ds.unmapped_share:.4f} exceeds 0.25 (spec 6.1.3)")
    if (pred.pid, ds.content_hash) in lock:
        raise NotEvaluable(
            f"verdict lock already held for {pred.pid} on this "
            f"dataset (spec 6.5)")
    if pred.kind == "template":
        sites = {r["site"] for r in ds.records if r["site"]}
        if len(sites) < 2:
            raise NotEvaluable(
                "PRED-2026-003 requires a multi-site dataset "
                "(>= 2 distinct site values; spec 6.1.5)")


def _score_rate(pred: Prediction, kept: list[dict],
                classes: dict[str, str]) -> dict:
    if pred.sign_set:
        signs = sorted(pred.sign_set)
    else:
        signs = sorted(s for s, lab in classes.items()
                       if lab == pred.sign_set_name)
    occ = Counter()
    edge = Counter()
    for r in kept:
        toks = r["tokens"]
        for t in toks:
            occ[t] += 1
        if toks:
            edge[toks[0] if pred.rate == "start" else toks[-1]] += 1
    per_sign = {}
    k = 0
    for s in signs:
        o = occ.get(s, 0)
        rate = (edge.get(s, 0) / o) if o else None
        meets = bool(o and rate is not None and rate >= pred.threshold)
        k += int(meets)
        per_sign[s] = {"occ": o,
                       "rate": rate,
                       "meets_criterion": meets}
    return {"per_sign": per_sign, "k": k,
            "verdict": "CONFIRMED" if k >= pred.pass_count else "REFUTED"}


_TEMPLATE_RE = re.compile(r"^I*M+T*$")


def _score_template(pred: Prediction, kept: list[dict],
                    classes: dict[str, str]) -> dict:
    short = {"INITIAL": "I", "MEDIAL": "M", "TERMINAL": "T",
             "MIXED": "X"}
    conforming = 0
    for r in kept:
        labels = []
        ok = True
        for t in r["tokens"]:
            lab = classes.get(t)
            if lab is None:
                ok = False
                break
            labels.append(short[lab])
        if ok and _TEMPLATE_RE.match("".join(labels)):
            conforming += 1
    total = len(kept)
    coverage = (conforming / total) if total else 0.0
    return {"conforming": conforming, "total": total,
            "coverage": coverage,
            "verdict": "CONFIRMED" if coverage >= pred.threshold
                       else "REFUTED"}


def evaluate(pred: Prediction, ds: IngestedDataset,
             classes: dict[str, str], lock: set,
             spec_sha256: str = "") -> dict:
    """The only path to a verdict (spec section 6). Gates run
    before dedup and scoring; on success the (prediction,
    dataset) pair is added to `lock`."""
    _check_gates(pred, ds, lock)
    kept, dedup_counts = dedup(ds.records)
    if pred.kind == "rate":
        scored = _score_rate(pred, kept, classes)
    else:
        scored = _score_template(pred, kept, classes)
    lock.add((pred.pid, ds.content_hash))
    report = {
        "prediction": pred.pid,
        "criterion": pred.criterion_text,
        "prediction_text": pred.prediction_text,
        "dataset": {"name": ds.name, "source_class": ds.source_class,
                    "content_hash": ds.content_hash,
                    "provenance": ds.provenance},
        "dedup": dedup_counts,
        "spec_sha256": spec_sha256,
        **scored,
    }
    if ds.source_class == "icit_full":
        report["caveat"] = CAVEAT_C1
    return report


# ---------------------------------------------------------------- §8 dry run

def dry_run(ds: IngestedDataset,
            classes: dict[str, str]) -> dict:
    """Labelled dry run (spec section 8): counts, dedup
    effects, and sign-set coverage only. This function has no
    access to the scoring path: no rates, no conformance
    fractions, no verdicts."""
    kept, dedup_counts = dedup(ds.records)

    def coverage(records):
        occ = Counter()
        for r in records:
            for t in r["tokens"]:
                occ[t] += 1
        out = {}
        for name in ("TERMINAL", "INITIAL", "MEDIAL"):
            signs = sorted(s for s, lab in classes.items()
                           if lab == name)
            out[name] = {
                "set_size": len(signs),
                "attested": sum(1 for s in signs if occ.get(s, 0) > 0),
                "per_sign_occurrences": {s: occ.get(s, 0) for s in signs},
            }
        labelled = total = 0
        for r in records:
            toks = [t for t in r["tokens"] if t != UNK]
            if toks:
                total += 1
                if all(t in classes for t in toks):
                    labelled += 1
        out["classifiability"] = {
            "inscriptions_with_mapped_signs": total,
            "all_signs_labelled": labelled,
            "fraction": (labelled / len(records)) if records else 0.0,
        }
        return out

    return {
        "label": DRY_RUN_LABEL,
        "dataset": {"name": ds.name, "source_class": ds.source_class,
                    "content_hash": ds.content_hash,
                    "stats": ds.stats},
        "dedup": dedup_counts,
        "coverage_pre_dedup": coverage(ds.records),
        "coverage_post_dedup": coverage(kept),
    }
