"""Tests for text corpus update/delete endpoints."""


def test_update_and_delete_text(client):
    """Texts can be updated and deleted through the API."""
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
