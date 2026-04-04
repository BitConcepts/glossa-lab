"""Tests for backend catalog endpoints."""


def test_catalog_endpoint_returns_expected_sections(client):
    """Aggregate catalog endpoint should expose all admin catalog sections."""
    response = client.get("/api/v1/catalog")
    assert response.status_code == 200

    data = response.json()
    assert set(data.keys()) == {"counts", "pipelines", "experiments", "reports", "providers"}
    assert data["counts"]["pipelines"] >= 17
    assert data["counts"]["experiments"] >= 8
    assert data["counts"]["providers"] == 4


def test_pipeline_catalog_matches_live_registry(client):
    """Pipeline catalog should reflect the fully loaded engine registry."""
    response = client.get("/api/v1/catalog/pipelines")
    assert response.status_code == 200

    pipelines = response.json()
    ids = {entry["id"] for entry in pipelines}
    assert len(pipelines) >= 17
    assert "positional" in ids
    assert "structural_fingerprint" in ids
    assert all(entry["registered"] for entry in pipelines)
    assert all(entry["module"].startswith("glossa_lab.pipelines.") for entry in pipelines)


def test_reports_and_providers_catalog_are_exposed(client):
    """Report and provider catalog endpoints should surface current metadata."""
    reports_response = client.get("/api/v1/catalog/reports")
    providers_response = client.get("/api/v1/catalog/providers")

    assert reports_response.status_code == 200
    assert providers_response.status_code == 200

    reports = reports_response.json()
    providers = providers_response.json()
    assert any(
        report["relative_path"] == "reports/real_indus_catalog_analysis.json" for report in reports
    )
    assert {provider["id"] for provider in providers} == {
        "openai",
        "anthropic",
        "google",
        "mistral",
    }
