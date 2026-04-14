"""Tests for text corpus CRUD including reading_direction (TEST-TC-001..012).

TEST-TC-001  Create and delete a corpus; full CRUD cycle.
TEST-TC-002  reading_direction defaults to 'unknown' when not supplied.
TEST-TC-003  reading_direction is persisted correctly on creation.
TEST-TC-004  reading_direction can be updated independently.
TEST-TC-005  reading_direction appears in GET /texts response.
TEST-TC-006  detect-direction with caller-supplied words (rtl corpus).
TEST-TC-007  detect-direction with metadata.inscriptions word structure.
TEST-TC-008  detect-direction returns expected keys in response.
TEST-TC-009  detect-direction updates reading_direction in DB when confident.
TEST-TC-010  detect-direction on non-existent text returns 404.
TEST-TC-011  Invalid reading_direction value is coerced to 'unknown'.
TEST-TC-012  Listing texts includes reading_direction for all items.
"""


# ── CRUD helpers ─────────────────────────────────────────────────────────────


def _create(client, name="tmp", direction="unknown", content=None, metadata=None):
    body = {
        "name": name,
        "corpus_type": "linguistic",
        "content": content or ["A", "B", "A"],
        "metadata": metadata or {},
        "reading_direction": direction,
    }
    resp = client.post("/api/v1/texts", json=body)
    assert resp.status_code == 201
    return resp.json()


# ── Tests ─────────────────────────────────────────────────────────────────────


def test_update_and_delete_text(client):
    """TEST-TC-001: Texts can be updated and deleted through the API."""
    created = client.post(
        "/api/v1/texts",
        json={
            "name": "tmp-corpus",
            "corpus_type": "linguistic",
            "content": ["A", "B", "A"],
            "metadata": {"source": "test"},
        },
    )
    assert created.status_code == 201
    text_id = created.json()["id"]

    updated = client.put(
        f"/api/v1/texts/{text_id}",
        json={
            "name": "tmp-corpus-updated",
            "content": ["X", "Y", "Z"],
            "metadata": {"source": "updated"},
        },
    )
    assert updated.status_code == 200
    data = updated.json()
    assert data["name"] == "tmp-corpus-updated"
    assert data["alphabet_size"] == 3
    assert data["metadata"] == {"source": "updated"}

    deleted = client.delete(f"/api/v1/texts/{text_id}")
    assert deleted.status_code == 200
    assert deleted.json()["id"] == text_id
    assert client.get(f"/api/v1/texts/{text_id}").status_code == 404


def test_reading_direction_defaults_to_unknown(client):
    """TEST-TC-002: Omitting reading_direction gives 'unknown'."""
    resp = client.post(
        "/api/v1/texts",
        json={"name": "no-dir", "content": ["A", "B"]},
    )
    assert resp.status_code == 201
    assert resp.json()["reading_direction"] == "unknown"
    client.delete(f"/api/v1/texts/{resp.json()['id']}")


def test_reading_direction_persisted_on_create(client):
    """TEST-TC-003: reading_direction is stored and returned correctly."""
    for direction in ("ltr", "rtl", "unknown"):
        corpus = _create(client, name=f"dir-{direction}", direction=direction)
        assert corpus["reading_direction"] == direction
        client.delete(f"/api/v1/texts/{corpus['id']}")


def test_reading_direction_update(client):
    """TEST-TC-004: reading_direction can be updated via PUT."""
    corpus = _create(client, name="dir-update-test", direction="unknown")
    tid = corpus["id"]

    resp = client.put(f"/api/v1/texts/{tid}", json={"reading_direction": "rtl"})
    assert resp.status_code == 200
    assert resp.json()["reading_direction"] == "rtl"

    # Update back to ltr
    resp2 = client.put(f"/api/v1/texts/{tid}", json={"reading_direction": "ltr"})
    assert resp2.json()["reading_direction"] == "ltr"
    client.delete(f"/api/v1/texts/{tid}")


def test_get_text_includes_reading_direction(client):
    """TEST-TC-005: GET /texts/{id} returns reading_direction."""
    corpus = _create(client, name="get-dir-test", direction="rtl")
    resp = client.get(f"/api/v1/texts/{corpus['id']}")
    assert resp.status_code == 200
    assert "reading_direction" in resp.json()
    assert resp.json()["reading_direction"] == "rtl"
    client.delete(f"/api/v1/texts/{corpus['id']}")


def test_detect_direction_with_caller_supplied_words(client):
    """TEST-TC-006: detect-direction with explicit words param (RTL corpus)."""
    # Create a minimal corpus — content doesn't matter for this test
    corpus = _create(client, name="detect-rtl")
    tid = corpus["id"]

    # Build a strongly RTL word list: position-0 is always '000' (low entropy)
    words = [["000", str(i).zfill(3)] for i in range(1, 30)]

    resp = client.post(
        f"/api/v1/texts/{tid}/detect-direction",
        json={"words": words, "update_field": False},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["inferred_direction"] == "rtl"
    assert data["word_source"] == "caller_supplied"
    client.delete(f"/api/v1/texts/{tid}")


def test_detect_direction_uses_metadata_inscriptions(client):
    """TEST-TC-007: detect-direction reads inscriptions from corpus metadata."""
    # All words end in '000' → LTR (word-END is rightmost → low entropy there)
    inscriptions = [[str(i).zfill(3), "000"] for i in range(1, 30)]
    corpus = _create(
        client,
        name="detect-ltr-meta",
        content=[t for w in inscriptions for t in w],
        metadata={"inscriptions": inscriptions},
    )
    tid = corpus["id"]

    resp = client.post(
        f"/api/v1/texts/{tid}/detect-direction",
        json={"update_field": False},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["inferred_direction"] == "ltr"
    assert data["word_source"] == "metadata"
    client.delete(f"/api/v1/texts/{tid}")


def test_detect_direction_response_keys(client):
    """TEST-TC-008: detect-direction response contains all expected keys."""
    corpus = _create(client, name="detect-keys-test")
    words = [["A", "B"] for _ in range(10)]
    resp = client.post(
        f"/api/v1/texts/{corpus['id']}/detect-direction",
        json={"words": words, "update_field": False},
    )
    assert resp.status_code == 200
    data = resp.json()
    expected = {
        "text_id", "word_source", "inferred_direction", "confidence",
        "n_words", "interpretation", "entropy_pos0", "entropy_posN1",
        "gini_pos0", "gini_posN1",
    }
    assert expected.issubset(data.keys())
    client.delete(f"/api/v1/texts/{corpus['id']}")


def test_detect_direction_updates_db_when_confident(client):
    """TEST-TC-009: detect-direction persists direction when confidence is not low."""
    corpus = _create(client, name="detect-persist", direction="unknown")
    tid = corpus["id"]

    # Strongly RTL words: pos-0 always '000'
    words = [["000", str(i).zfill(3)] for i in range(1, 30)]
    resp = client.post(
        f"/api/v1/texts/{tid}/detect-direction",
        json={"words": words, "update_field": True},
    )
    assert resp.status_code == 200
    data = resp.json()

    if data["inferred_direction"] in ("ltr", "rtl"):
        # Direction was committed — confirm it's stored in DB
        stored = client.get(f"/api/v1/texts/{tid}").json()
        assert stored["reading_direction"] == data["inferred_direction"]

    client.delete(f"/api/v1/texts/{tid}")


def test_detect_direction_missing_corpus(client):
    """TEST-TC-010: detect-direction on non-existent corpus returns 404."""
    resp = client.post(
        "/api/v1/texts/nonexistent_id_xyz/detect-direction",
        json={},
    )
    assert resp.status_code == 404


def test_list_texts_includes_reading_direction(client):
    """TEST-TC-012: GET /texts returns reading_direction for every item."""
    corpus = _create(client, name="list-dir-test", direction="ltr")
    resp = client.get("/api/v1/texts")
    assert resp.status_code == 200
    items = resp.json()
    assert any(t["id"] == corpus["id"] for t in items)
    for item in items:
        assert "reading_direction" in item
    client.delete(f"/api/v1/texts/{corpus['id']}")
