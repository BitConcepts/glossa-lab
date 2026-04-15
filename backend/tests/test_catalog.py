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


def test_experiments_endpoint_returns_graph_only(client):
    """H16 regression: GET /experiments must NEVER return Python ExperimentBase compositions.

    Every item returned must have source_file ending in .json (graph spec),
    command empty string, and category='Graph Experiments'.
    This test fails if Python compositions ever leak through.
    """
    response = client.get("/api/v1/experiments")
    assert response.status_code == 200
    experiments = response.json()
    assert len(experiments) > 0

    for exp in experiments:
        assert exp.get("source_file", "").endswith(".json"), (
            f"Experiment '{exp['id']}' has non-graph source_file: {exp.get('source_file')}. "
            "Python composition leaked into /experiments response."
        )
        assert exp.get("command", "UNSET") == "", (
            f"Experiment '{exp['id']}' has command set: {exp.get('command')}. "
            "Only graph experiments (command='') should appear here."
        )
        assert exp.get("category") == "Graph Experiments", (
            f"Experiment '{exp['id']}' has wrong category: {exp.get('category')}."
        )


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
