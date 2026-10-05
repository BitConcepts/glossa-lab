"""Tests for the GDELT Web Ngrams fetcher (gdelt_ngrams.py).

All fixtures are small synthetic .gz payloads built in-test; the
download layer is monkeypatched — no network access in any test.
"""
from __future__ import annotations

import gzip
import io
import json
from datetime import datetime, timezone

import pytest

from glossa_lab.discovery.fetchers import gdelt_ngrams as gn
from glossa_lab.discovery.fetchers.base import TopicProfile


def _gz(text: str) -> bytes:
    buf = io.BytesIO()
    with gzip.GzipFile(fileobj=buf, mode="wb") as gz:
        gz.write(text.encode("utf-8"))
    return buf.getvalue()


def _topic(**kw) -> TopicProfile:
    base = dict(
        id="indus_script",
        label="Indus Script",
        description="test",
        keywords=["Indus script", "Harappan"],
        exclusions=["stock market"],
        languages=["en"],
    )
    base.update(kw)
    return TopicProfile(**base)


NGRAMS = (
    "doc1\tthe indus script remains undeciphered\t3\n"
    "doc1\tindus script seals were found\t2\n"
    "doc2\tharappan cities and indus script\t1\n"
    "doc3\tquarterly stock market results today\t9\n"
    "doc4\tnothing relevant in this phrase\t5\n"
)

TOC = json.dumps([
    {"docid": "doc1", "url": "https://example.org/a", "title": "New Indus Script Study",
     "date": "20261005T120000Z", "lang": "en", "img": "https://example.org/a.png"},
    {"docid": "doc2", "url": "https://example.org/b", "title": "Harappan Cities Revisited",
     "date": "2026-10-05", "lang": "en", "img": ""},
    {"docid": "doc3", "url": "https://example.org/c", "title": "Stock Market Weekly",
     "date": "2026-10-05", "lang": "en", "img": ""},
    {"docid": "doc4", "url": "https://example.org/d", "title": "Unrelated",
     "date": "2026-10-05", "lang": "en", "img": ""},
])


# ── Matching ─────────────────────────────────────────────────────────────

def test_quadgram_phrase_matching():
    items = gn.items_from_pair(NGRAMS, gn.parse_toc(TOC), _topic(), stem="20261005120000")
    by_url = {i.url: i for i in items}
    assert "https://example.org/a" in by_url
    assert "https://example.org/b" in by_url
    a = by_url["https://example.org/a"]
    assert a.source == "gdelt_ngrams"
    assert a.topic == "indus_script"
    assert a.published_at == "2026-10-05"
    assert a.raw["matched_keywords"] == ["Indus script"]
    assert a.raw["match_count"] == 5  # 3 + 2 across two quadgrams
    assert a.raw["docid"] == "doc1"


def test_unigram_keyword_matches_containing_quadgram():
    items = gn.items_from_pair(NGRAMS, gn.parse_toc(TOC), _topic())
    b = next(i for i in items if i.url.endswith("/b"))
    assert "Harappan" in b.raw["matched_keywords"]


def test_unmatched_doc_produces_no_item():
    items = gn.items_from_pair(NGRAMS, gn.parse_toc(TOC), _topic())
    assert all(i.url != "https://example.org/d" for i in items)


def test_exclusion_filtering():
    # doc3's quadgram matches no keyword, so also verify exclusion on a
    # keyword-matching doc whose TITLE trips the exclusion list.
    ngrams = "doc9\tindus script stock market hype\t4\n"
    toc = json.dumps([{"docid": "doc9", "url": "https://example.org/x",
                       "title": "Indus Script Stock Market Hype", "date": "2026-10-05",
                       "lang": "en"}])
    items = gn.items_from_pair(ngrams, gn.parse_toc(toc), _topic())
    assert items == []


def test_missing_toc_entry_skips_doc():
    ngrams = "docZ\tindus script appears here now\t1\n"
    items = gn.items_from_pair(ngrams, gn.parse_toc(TOC), _topic())
    assert items == []


def test_long_keyword_windows_and_reductions():
    topic = _topic(keywords=["ancient Indus Valley script decipherment claims"])
    # 4-gram window hit
    n1 = "doc1\tindus valley script decipherment\t1\n"
    # trigram reduction hit
    n2 = "doc1\tvalley script decipherment\t1\n"  # only 3 tokens in line value? quadgram below
    n2 = "doc1\tthe valley script decipherment continues\t1\n"
    # bigram reduction hit
    n3 = "doc1\tscript decipherment in the news\t1\n"
    for text in (n1, n2, n3):
        items = gn.items_from_pair(text, gn.parse_toc(TOC), topic)
        assert len(items) == 1, text
        assert items[0].raw["matched_keywords"] == [
            "ancient Indus Valley script decipherment claims"
        ]
    # unrelated text does not match
    items = gn.items_from_pair(
        "doc1\tcompletely different words appear here\t1\n", gn.parse_toc(TOC), topic,
    )
    assert items == []


# ── TOC parsing variants ─────────────────────────────────────────────────

def test_toc_json_lines_and_dict_shapes():
    lines = "\n".join([
        json.dumps({"DOCID": "d1", "URL": "https://x/1", "Title": "T1",
                    "Date": "20261005T000000Z", "Lang": "en"}),
        json.dumps({"docid": "d2", "url": "https://x/2", "title": "T2",
                    "date": "2026-10-05", "lang": "fr"}),
    ])
    toc = gn.parse_toc(lines)
    assert toc["d1"]["url"] == "https://x/1"
    assert toc["d2"]["lang"] == "fr"
    as_dict = gn.parse_toc(json.dumps({"d9": {"url": "https://x/9", "title": "T9"}}))
    assert as_dict["d9"]["title"] == "T9"


# ── Candidate marks / heartbeat walk-back ────────────────────────────────

def test_candidate_stems_bounded_and_heartbeat_aligned():
    now = datetime(2026, 10, 5, 12, 7, tzinfo=timezone.utc)
    stems = gn.candidate_stems(now, max_marks=24)
    assert stems[0] == "20261005120200"  # now - 5 min, exact minute first
    assert len(stems) <= 25
    marks = [gn.stem_datetime(s) for s in stems[1:]]
    assert all(m.minute in (0, 15, 30, 45) for m in marks)
    assert marks == sorted(marks, reverse=True)  # newest → oldest


@pytest.mark.asyncio
async def test_fetch_walks_back_over_heartbeat_gaps(monkeypatch, tmp_path):
    state = tmp_path / "gdelt_ngrams.json"
    monkeypatch.setattr(gn, "_state_path", lambda: state)

    calls: list[str] = []

    def fake_pair(stem: str):
        calls.append(stem)
        if stem == "20261005120000":  # only the 12:00 mark exists
            return NGRAMS, TOC
        return None

    monkeypatch.setattr(gn, "download_pair", fake_pair)
    now = datetime(2026, 10, 5, 12, 20, tzinfo=timezone.utc)
    monkeypatch.setattr(gn, "datetime", _FrozenDateTime(now))

    fetcher = gn.GDELTNgramsFetcher()
    items = list(await fetcher.fetch(_topic()))
    assert {i.url for i in items} == {"https://example.org/a", "https://example.org/b"}
    assert "20261005120000" in calls
    saved = json.loads(state.read_text(encoding="utf-8"))
    assert saved["last_processed_stem"] == "20261005120000"

    # Second run: watermark suppresses rescanning the same minutes.
    calls.clear()
    items2 = list(await fetcher.fetch(_topic()))
    assert items2 == []
    assert "20261005120000" not in calls


@pytest.mark.asyncio
async def test_fetch_no_files_returns_empty(monkeypatch, tmp_path):
    monkeypatch.setattr(gn, "_state_path", lambda: tmp_path / "s.json")
    monkeypatch.setattr(gn, "download_pair", lambda stem: None)
    fetcher = gn.GDELTNgramsFetcher()
    assert list(await fetcher.fetch(_topic())) == []


def _make_frozen(now: datetime):
    return type("Frozen", (datetime,), {"now": classmethod(lambda c, tz=None: now)})


def _FrozenDateTime(now: datetime):  # noqa: N802 — test helper factory
    return _make_frozen(now)


def test_gz_roundtrip_helper():
    payload = _gz("doc1\ta b c d\t1\n")
    assert gzip.decompress(payload).decode() == "doc1\ta b c d\t1\n"
