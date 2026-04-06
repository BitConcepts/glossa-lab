"""Catalog endpoints for pipelines, experiments, reports, and providers."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from glossa_lab.catalog import (
    get_catalog_summary,
    list_experiment_catalog,
    list_pipeline_catalog,
    list_provider_catalog,
    list_report_catalog,
)

router = APIRouter()


class PipelineCatalogEntry(BaseModel):
    """Pipeline catalog entry."""

    id: str
    label: str
    group: str
    description: str
    inputs: str
    outputs: str
    default_params: dict[str, Any]
    needs_lm: bool
    registered: bool
    module: str


class ExperimentCatalogEntry(BaseModel):
    """Experiment catalog entry."""

    id: str
    name: str
    category: str
    description: str
    command: str
    results_file: str | None = None
    requires_key: str | None = None
    estimated_time: str


class ModelDetailEntry(BaseModel):
    """Per-model description and use-case tag."""

    id: str
    description: str = ""
    use_for: str = ""


class ProviderCatalogEntry(BaseModel):
    """Provider catalog entry."""

    id: str
    label: str
    api_key_setting: str
    supports_live_model_discovery: bool
    recommended_models: list[str]
    model_details: list[ModelDetailEntry] = []
    ocr_preferred_models: list[str]


class ReportCatalogEntry(BaseModel):
    """Report catalog entry."""

    id: str
    name: str
    kind: str
    relative_path: str
    size_bytes: int
    updated_at: str


class CatalogResponse(BaseModel):
    """Aggregate catalog response."""

    counts: dict[str, int]
    pipelines: list[PipelineCatalogEntry]
    experiments: list[ExperimentCatalogEntry]
    reports: list[ReportCatalogEntry]
    providers: list[ProviderCatalogEntry]


@router.get("/catalog")
async def get_catalog() -> CatalogResponse:
    """Return the aggregate backend catalog."""
    return CatalogResponse(
        counts=get_catalog_summary(),
        pipelines=[PipelineCatalogEntry(**entry) for entry in list_pipeline_catalog()],
        experiments=[ExperimentCatalogEntry(**entry) for entry in list_experiment_catalog()],
        reports=[ReportCatalogEntry(**entry) for entry in list_report_catalog()],
        providers=[
            ProviderCatalogEntry(
                **{
                    **entry,
                    "model_details": [
                        ModelDetailEntry(**m) for m in entry.get("model_details", [])
                    ],
                }
            )
            for entry in list_provider_catalog()
        ],
    )


@router.get("/catalog/pipelines")
async def get_pipeline_catalog() -> list[PipelineCatalogEntry]:
    """Return live pipeline metadata."""
    return [PipelineCatalogEntry(**entry) for entry in list_pipeline_catalog()]


@router.get("/catalog/experiments")
async def get_experiment_catalog() -> list[ExperimentCatalogEntry]:
    """Return experiment metadata."""
    return [ExperimentCatalogEntry(**entry) for entry in list_experiment_catalog()]


@router.get("/catalog/reports")
async def get_report_catalog() -> list[ReportCatalogEntry]:
    """Return discovered report artifacts."""
    return [ReportCatalogEntry(**entry) for entry in list_report_catalog()]


@router.get("/catalog/providers")
async def get_provider_catalog() -> list[ProviderCatalogEntry]:
    """Return provider metadata."""
    return [
        ProviderCatalogEntry(
            **{
                **entry,
                "model_details": [
                    ModelDetailEntry(**m) for m in entry.get("model_details", [])
                ],
            }
        )
        for entry in list_provider_catalog()
    ]
