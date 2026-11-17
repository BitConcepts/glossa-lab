"""Spec 095 Stage 1 (T105) — the twelve-case fail-closed battery.

The twelve cases of claim C095-4, as a named CI suite over the
covered loaders and the corpus identity standard
(``glossa_lab.data.corpus_identity``). Each case's defined outcome:

  1. missing corpus            — verification refuses (every
                                 registered corpus); the verified
                                 load entry points refuse.
  2. wrong content hash        — the loader refuses at load; a
                                 control with the pin set to the
                                 fixture's own digest loads, proving
                                 the refusal is the pin.
  3. same-name-different-corpus — another corpus's bytes at the
                                 strict corpus's path are refused.
  4. empty loader result       — a schema-valid file yielding zero
                                 sequences fails the identity census
                                 and the verified load refuses the
                                 empty result.
  5. duplicate identifiers     — audit flags duplicate_identifiers.
  6. contradictory mappings    — audit flags contradictory_mappings.
  7. unknown signs             — audit flags unknown_signs
                                 (foreign-numbering tokens).
  8. damaged spans             — audit flags damaged_spans
                                 (unparseable lines).
  9. reversed reading order    — the canonical export pin differs
                                 and the audit flags
                                 reversed_reading_order.
 10. partial availability      — verify-all refuses, naming the
                                 unavailable corpora.
 11. unauthorized access       — a corpus file with no read
                                 permission is refused as unauthorized,
                                 never treated as absent or empty.
 12. synthetic-presented-as-real — synthetic-prototype output placed
                                 at a covered path is refused at load
                                 and flagged by audit.

The suite is self-contained (fixtures under tmp_path) except
``TestRealTree``, which runs only where the corpora are actually
placed in the tree and skips otherwise.

_citation:
  derivation: "Spec 095 claims.md C095-4; cases enumerated there and
               in the pinnability pass (hidden_files/red-team-
               2026-11-15/pinnability-p0.md, section 4)."
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import replace
from pathlib import Path

import pytest

from glossa_lab.data import corpus_identity as ci
from glossa_lab.data import indus_corpus_v2 as v2
from glossa_lab.data import indus_corpus_v3 as v3

V3 = ci.V3_KEY


def _v3_line(dockey: int, sideline: str, texts: list) -> str:
    rec = {"dockey": dockey, "sideline": sideline, "texts": texts}
    for i in range(1, 15):
        rec[f"S{i}"] = str(texts[i - 1]) if i - 1 < len(texts) else ""
    return json.dumps(rec)


def _write_v3_fixture(path: Path, lines: list[str]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def _patch_identity(monkeypatch, key: str, **changes) -> None:
    monkeypatch.setitem(
        ci.CORPUS_IDENTITIES, key, replace(ci.CORPUS_IDENTITIES[key], **changes)
    )


def _point_v3_loader(monkeypatch, path: Path) -> None:
    monkeypatch.setattr(v3, "_FIRESTORE_JSONL", path)
    monkeypatch.setattr(v3, "_CACHE", None)
    monkeypatch.setattr(v3, "_CACHE_SEQS_BY_DOCKEY", None)


GOOD_LINES = [
    _v3_line(1001, "a", [342, 99, 267]),
    _v3_line(1002, "a", [87, 59, 89, 328]),
    _v3_line(1003, "a", [176, 344]),
]


class TestTwelveCases:
    def test_01_missing_corpus(self, tmp_path, monkeypatch):
        for key in ci.CORPUS_IDENTITIES:
            with pytest.raises(ci.CorpusIdentityError, match="missing"):
                ci.verify_corpus_identity(key, root=tmp_path)
        # The verified load entry point refuses absence too.
        monkeypatch.setattr(ci, "_REPO", tmp_path)
        with pytest.raises(ci.CorpusIdentityError):
            v3.load_corpus_verified()

    def test_02_wrong_content_hash(self, tmp_path, monkeypatch):
        fixture = _write_v3_fixture(tmp_path / "firestore_indusarrays_full.jsonl",
                                    GOOD_LINES)
        _point_v3_loader(monkeypatch, fixture)
        # The registry pin is the intake pin of record: refusal.
        with pytest.raises(ci.CorpusIdentityError, match="differs from its identity pin"):
            v3.load_corpus()
        with pytest.raises(ci.CorpusIdentityError):
            ci.enforce_file_identity(V3, fixture)
        # Control: with the pin set to the fixture's own digest and
        # the census to the fixture's basis, the same file loads.
        digest = ci.file_sha256(fixture)
        _patch_identity(monkeypatch, V3, sha256=digest,
                        census=ci.corpus_census(V3, fixture),
                        paths=(fixture.name,))
        assert len(v3.load_corpus()) == 3

    def test_03_same_name_different_corpus(self, tmp_path, monkeypatch):
        # The CISI compilation's bytes under the strict corpus's name.
        other = tmp_path / "firestore_indusarrays_full.jsonl"
        other.write_bytes(b'{"inscriptions": [{"id": "M-1", "signs": ["P121"]}]}\n')
        _point_v3_loader(monkeypatch, other)
        with pytest.raises(ci.CorpusIdentityError):
            v3.load_corpus()
        assert "content_hash_mismatch" in ci.audit_corpus_file(V3, other)

    def test_04_empty_loader_result(self, tmp_path, monkeypatch):
        lines = [_v3_line(1001, "a", []), _v3_line(1002, "a", [])]
        fixture = _write_v3_fixture(tmp_path / "firestore_indusarrays_full.jsonl",
                                    lines)
        digest = ci.file_sha256(fixture)
        # Census leg: identity census is the census of record, so a
        # zero-sequence file fails verification on counts.
        _patch_identity(monkeypatch, V3, sha256=digest, paths=(fixture.name,))
        with pytest.raises(ci.CorpusIdentityError, match="census"):
            ci.verify_corpus_identity(V3, root=tmp_path)
        # Verified-load leg: even with the identity patched to the
        # fixture's own (zero) census, the verified load refuses an
        # empty result for a claim-bearing corpus.
        _patch_identity(monkeypatch, V3,
                        census=ci.corpus_census(V3, fixture))
        monkeypatch.setattr(ci, "_REPO", tmp_path)
        _point_v3_loader(monkeypatch, fixture)
        with pytest.raises(ci.CorpusIdentityError, match="zero sequences"):
            v3.load_corpus_verified()

    def test_05_duplicate_identifiers(self):
        lines = GOOD_LINES + [GOOD_LINES[0]]
        records = [json.loads(x) for x in lines]
        assert "duplicate_identifiers" in ci.audit_v3_records(records, len(lines))

    def test_06_contradictory_mappings(self):
        lines = [
            _v3_line(1001, "a", [342, 99, 267]),
            _v3_line(1001, "a", [1, 2, 3]),
        ]
        records = [json.loads(x) for x in lines]
        assert "contradictory_mappings" in ci.audit_v3_records(records, len(lines))

    def test_07_unknown_signs(self):
        lines = [_v3_line(1001, "a", ["P121", "P202", "P99"])]
        records = [json.loads(x) for x in lines]
        assert "unknown_signs" in ci.audit_v3_records(records, len(lines))

    def test_08_damaged_spans(self, tmp_path):
        fixture = _write_v3_fixture(
            tmp_path / "firestore_indusarrays_full.jsonl",
            [GOOD_LINES[0], '{"dockey": 1002, "sideline": "a", "te', GOOD_LINES[2]],
        )
        flags = ci.audit_corpus_file(V3, fixture)
        assert "damaged_spans" in flags
        assert "content_hash_mismatch" in flags

    def test_09_reversed_reading_order(self):
        sbd = {1001: [[342, 99, 267], [87, 59]], 1002: [[176, 344, 1]]}
        reversed_sbd = {k: [list(reversed(s)) for s in v] for k, v in sbd.items()}
        assert ci.canonical_export_pin(reversed_sbd) != ci.canonical_export_pin(sbd)
        assert ci.audit_export_orientation(sbd, reversed_sbd) == [
            "reversed_reading_order"
        ]
        assert ci.audit_export_orientation(sbd, sbd) == []

    def test_10_partial_availability(self, tmp_path, monkeypatch):
        # Register fixture identities for every corpus, then make
        # only some of the files available under the fixture root.
        keys = list(ci.CORPUS_IDENTITIES)
        for key in keys:
            rel = f"{key}.bin"
            payload = f"fixture-{key}".encode()
            _patch_identity(
                monkeypatch, key,
                paths=(rel,),
                sha256=hashlib.sha256(payload).hexdigest(),
                census=None,
            )
            if key != keys[-1]:
                (tmp_path / rel).write_bytes(payload)
        with pytest.raises(ci.CorpusIdentityError, match=keys[-1]):
            ci.verify_all_identities(root=tmp_path)
        (tmp_path / f"{keys[-1]}.bin").write_bytes(f"fixture-{keys[-1]}".encode())
        assert set(ci.verify_all_identities(root=tmp_path)) == set(keys)

    def test_11_unauthorized_access(self, tmp_path, monkeypatch):
        fixture = _write_v3_fixture(tmp_path / "firestore_indusarrays_full.jsonl",
                                    GOOD_LINES)
        digest = ci.file_sha256(fixture)
        _patch_identity(monkeypatch, V3, sha256=digest, paths=(fixture.name,),
                        census=ci.corpus_census(V3, fixture))
        os.chmod(fixture, 0o000)
        try:
            with pytest.raises(ci.CorpusIdentityError, match="unauthorized"):
                ci.verify_corpus_identity(V3, root=tmp_path)
            _point_v3_loader(monkeypatch, fixture)
            with pytest.raises(ci.CorpusIdentityError, match="unauthorized"):
                v3.load_corpus()
        finally:
            os.chmod(fixture, 0o644)

    def test_12_synthetic_presented_as_real(self, tmp_path, monkeypatch):
        from glossa_lab.data import indus_public_corpus

        synthetic = indus_public_corpus.get_corpus_inscriptions()
        assert synthetic  # the prototype does generate sequences
        # Synthetic sequences dressed in the strict corpus's schema.
        lines = [
            _v3_line(1001 + i, "a", seq) for i, seq in enumerate(synthetic[:25])
        ]
        fixture = _write_v3_fixture(tmp_path / "firestore_indusarrays_full.jsonl",
                                    lines)
        _point_v3_loader(monkeypatch, fixture)
        with pytest.raises(ci.CorpusIdentityError):
            v3.load_corpus()
        assert "content_hash_mismatch" in ci.audit_corpus_file(V3, fixture)
        # Raw synthetic output (bare sign lists, no corpus schema).
        raw = tmp_path / "raw.jsonl"
        raw.write_text(
            "\n".join(json.dumps(s) for s in synthetic[:5]) + "\n",
            encoding="utf-8",
        )
        records = []
        for line in raw.read_text(encoding="utf-8").splitlines():
            records.append(json.loads(line))
        assert "schema_mismatch" in ci.audit_v3_records(records, len(records))


class TestLoaderRefusalDoesNotFallBack:
    def test_v2_refuses_corrupt_export_instead_of_falling_back(
        self, tmp_path, monkeypatch
    ):
        bad = tmp_path / "indus_research.jsonl"
        bad.write_text('{"id": 1}\n', encoding="utf-8")
        monkeypatch.setattr(v2, "_EXPORT_PATH", bad)
        monkeypatch.setattr(v2, "_CACHE", None)
        with pytest.raises(ci.CorpusIdentityError):
            v2.load_corpus()


class TestIdentityStandard:
    def test_registry_complete(self):
        for key, ident in ci.CORPUS_IDENTITIES.items():
            assert ident.sha256, key
            assert ident.source and ident.licensing, key
            assert ident.census_basis and ident.normalization, key
            assert ident.paths and ident.loaders, key

    def test_unknown_corpus_refused(self):
        with pytest.raises(ci.CorpusIdentityError, match="no corpus identity"):
            ci.verify_corpus_identity("no_such_corpus", root=Path("/tmp"))


@pytest.mark.skipif(
    not v3._FIRESTORE_JSONL.exists(),
    reason="strict corpus not placed in this tree",
)
class TestRealTree:
    def test_v3_identity_and_export_pin(self):
        rec = ci.verify_corpus_identity(V3)
        assert rec["census"] == {
            "records": 3916,
            "unique_dockeys": 2665,
            "total_sequences": 3137,
            "total_sign_instances": 12494,
        }
        sbd = v3.load_corpus_by_dockey()
        assert ci.canonical_export_pin(sbd) == (
            "e90fd7ce41121529887b51dda11640741c23db94a224e946588628802503c659"
        )

    def test_in_tree_corpora_verify(self):
        for key in ci.CORPUS_IDENTITIES:
            if key == ci.HOLDAT_KEY:
                # The downloads layer is not held in this repo tree;
                # its defined behaviour here is a missing refusal.
                with pytest.raises(ci.CorpusIdentityError, match="missing"):
                    ci.verify_corpus_identity(key)
            else:
                ci.verify_corpus_identity(key)
