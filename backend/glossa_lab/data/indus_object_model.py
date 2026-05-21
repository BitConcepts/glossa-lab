"""Indus Script Corpus — Core Object Model.

Four-layer architecture (never silently collapsed):
  1. Source layer    — raw asset, fetch hash, source URL, rights class, provenance chain
  2. Diplomatic layer — lossless ICIT-compatible coded text
  3. Graphemic layer  — canonical sign IDs via M77/Parpola/Wells/Fuls crosswalk
  4. Interpretive layer — hypotheses with bibliographic attribution and confidence

Object hierarchy:
  IndusObject → IndusSurface → (IndusImageAsset + IndusTextWitness)
  IndusTextWitness → IndusSignInstance → (IndusSignType via sign ID)
  IndusSignType ↔ IndusSignRelation

ICIT Diplomatic Encoding Rules (lossless preservation):
  - Three-digit sign numbers (Wells 2006/Fuls 2014): 001–676
  - Hyphen-delimited: 740-760-033-705
  - Leading/trailing +: +NNN-NNN+ marks initial/terminal position
  - 000: one eroded sign of unknown identity
  - ++: eroded text-part of unknown length
  - Multi-part texts: separated by +

_citation:
  primary_sources: ["A.1", "A.7", "I.1", "I.2", "I.3"]
  derivation: "Schema designed for ICIT-scale reconstruction; fields derived from
               ICIT encoding documentation, CISI structure, and research report
               2026-05-14. See CITATIONS.md sections A.1 (Mahadevan 1977),
               A.7 (Wells 2015), I.1–I.8 (new sources)."
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field

# ── Enumerations ─────────────────────────────────────────────────────────────

class RightsStatus(str, Enum):
    CC0 = "CC0"
    CC_BY_4 = "CC BY 4.0"
    CC_BY_SA = "CC BY-SA"
    MIT = "MIT"
    NONCOMMERCIAL_EDUCATIONAL = "noncommercial-educational"
    INDIA_GOV_CULTURAL = "india-gov-cultural"
    RMRL_RESEARCH = "rmrl-research"
    INDIA_MUSEUM_RESTRICTED = "india-museum-restricted"
    INTERNET_ARCHIVE_DERIVATIVE = "internet-archive-derivative"
    PURCHASABLE_RESEARCH = "purchasable-research"
    PERMISSION_REQUIRED = "permission-required"
    LICENSED = "licensed"
    UNKNOWN = "unknown"


class SignIdScheme(str, Enum):
    MAHADEVAN_1977 = "Mahadevan1977"
    PARPOLA_1982 = "Parpola1982"
    WELLS_2006 = "Wells2006"
    FULS_2014 = "Fuls2014"
    GLOSSA_CANONICAL = "GlossaCanonical"


class ArtifactType(str, Enum):
    SEAL = "seal"
    SEAL_AMULET = "seal-amulet"
    TABLET = "tablet"
    POTSHERD = "potsherd"
    IMPRESSION = "impression"
    COPPER_TABLET = "copper-tablet"
    BONE = "bone"
    IVORY = "ivory"
    TERRACOTTA = "terracotta"
    UNKNOWN = "unknown"


class SurfaceId(str, Enum):
    OBVERSE = "obverse"
    REVERSE = "reverse"
    EDGE_A = "edge-a"
    EDGE_B = "edge-b"
    SINGLE_SURFACE = "single-surface"
    UNKNOWN = "unknown"


class DamageState(str, Enum):
    INTACT = "intact"
    PARTIAL = "partial"
    ERODED = "eroded"
    LOST = "lost"
    UNKNOWN = "unknown"


class ReviewState(str, Enum):
    UNREVIEWED = "unreviewed"
    SINGLE_REVIEWED = "single-reviewed"
    DOUBLE_REVIEWED = "double-reviewed"
    RELEASED = "released"


class RelationType(str, Enum):
    ALLOGRAPH_OF = "allograph_of"
    MIRRORED_VARIANT_OF = "mirrored_variant_of"
    GRAPHIC_VARIANT_OF = "graphic_variant_of"
    DISPUTED_RELATION_TO = "disputed_relation_to"
    IDENTICAL_TO = "identical_to"


class PipelineStage(str, Enum):
    SOURCE_REGISTERED = "source_registered"
    FETCHED = "fetched"
    EXTRACTED = "extracted"
    OBJECTIZED = "objectized"
    DIPLOMATIC = "diplomatic"
    NORMALIZED = "normalized"
    ANNOTATED = "annotated"
    DEDUPLICATED = "deduplicated"
    RELEASED = "released"
    QUARANTINED = "quarantined"


# ── Sub-models ────────────────────────────────────────────────────────────────

class IndusProvenanceEvent(BaseModel):
    """Single step in the provenance chain."""
    stage: PipelineStage
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    source_url: Optional[str] = None
    fetch_hash_sha256: Optional[str] = None
    agent: str = "corpus_indus_pipeline"
    note: Optional[str] = None


class IndusSignRelation(BaseModel):
    """Typed relation between sign types (allograph, mirror, variant, disputed)."""
    from_sign_id: str
    from_scheme: SignIdScheme
    to_sign_id: str
    to_scheme: SignIdScheme
    relation_type: RelationType
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    citation: Optional[str] = None
    note: Optional[str] = None


class IndusSignInstance(BaseModel):
    """A single sign token within a text witness."""
    sign_instance_id: str          # e.g. GLI-IND-0001254-S1-03
    reading_order_index: int        # position in source reading order
    source_sign_id: str             # exact source sign number, e.g. "033"
    source_scheme: SignIdScheme
    canonical_sign_id: Optional[str] = None   # after crosswalk
    damage_state: DamageState = DamageState.UNKNOWN
    damage_marker: Optional[str] = None        # e.g. "000" or "++"
    orientation_state: str = "normal"          # normal/rotated/mirror/uncertain
    confidence_model: Optional[float] = None
    confidence_human: Optional[str] = None     # high/medium/low
    review_state: ReviewState = ReviewState.UNREVIEWED
    bbox: Optional[List[float]] = None         # [x, y, w, h] in image pixels
    polygon: Optional[List[List[float]]] = None
    evidence_uris: List[str] = Field(default_factory=list)


class IndusTextWitness(BaseModel):
    """A diplomatic + graphemic text record for one surface."""
    witness_id: str                            # e.g. GLI-IND-0001254-S1-TW01
    surface_id: str                            # parent surface glossa_id
    text_code_diplomatic: Optional[str] = None  # ICIT-format: +NNN-NNN-NNN+
    text_parts_count: int = 1
    sign_count_visible: Optional[int] = None
    damage_encoding: Optional[str] = None      # "000", "++" where applicable
    sign_id_scheme: SignIdScheme = SignIdScheme.WELLS_2006
    canonical_grapheme_ids: List[str] = Field(default_factory=list)
    sign_instances: List[IndusSignInstance] = Field(default_factory=list)
    # Interpretive layer (always hypothesis, never authoritative translation)
    interpretive_notes: List[str] = Field(default_factory=list)
    review_state: ReviewState = ReviewState.UNREVIEWED


class IndusImageAsset(BaseModel):
    """A single image asset (photo, drawing, scan) for an object surface."""
    asset_id: str
    surface_id: str
    image_master_uri: Optional[str] = None
    image_derivatives: dict = Field(default_factory=dict)  # {"web": uri, "print": uri, "tiff": uri}
    rights_status: RightsStatus = RightsStatus.UNKNOWN
    source_system: str = ""
    fetch_hash_sha256: Optional[str] = None
    download_timestamp: Optional[str] = None
    note: Optional[str] = None


class IndusSurface(BaseModel):
    """One face/surface of an inscribed object."""
    surface_id: str                   # e.g. GLI-IND-0001254-S1
    object_id: str                    # parent object glossa_id
    surface_label: SurfaceId = SurfaceId.UNKNOWN
    text_witnesses: List[IndusTextWitness] = Field(default_factory=list)
    image_assets: List[IndusImageAsset] = Field(default_factory=list)
    note: Optional[str] = None


class IndusRightsRecord(BaseModel):
    """Rights and provenance tracking for an object."""
    object_id: str
    rights_status: RightsStatus = RightsStatus.UNKNOWN
    license: Optional[str] = None
    license_url: Optional[str] = None
    rights_notes: Optional[str] = None
    ml_training_cleared: bool = False
    redistribution_cleared: bool = False
    permission_contact: Optional[str] = None
    permission_requested_date: Optional[str] = None
    permission_granted_date: Optional[str] = None


class IndusObject(BaseModel):
    """
    A single inscribed Indus object — the canonical unit of the corpus.

    glossa_id is the stable internal key independent of any publisher or museum.
    Prefix: GLI-IND-XXXXXXX
    """
    # ── Identity ──────────────────────────────────────────────────────────────
    glossa_id: str                       # GLI-IND-0001254
    source_system: str                   # ICIT / CISI / Mahadevan1977 / NationalMuseumND / PennMuseum / ...
    source_object_id: str                # exact external identifier (e.g. "1254" or "L-141-176")
    source_page_ref: Optional[str] = None

    # ── Location ──────────────────────────────────────────────────────────────
    current_holding: Optional[str] = None     # Penn Museum / National Museum, New Delhi / ...
    site_name: Optional[str] = None           # Mohenjo-daro / Chanhu-Daro / Dholavira / ...
    provenience_detail: Optional[str] = None  # DK1104 / Field No SF 2428 / ...
    region: Optional[str] = None

    # ── Object type ───────────────────────────────────────────────────────────
    artifact_type: ArtifactType = ArtifactType.UNKNOWN
    material: Optional[str] = None
    dimensions_mm: Optional[str] = None

    # ── Content ───────────────────────────────────────────────────────────────
    surfaces: List[IndusSurface] = Field(default_factory=list)

    # ── Rights + provenance ───────────────────────────────────────────────────
    rights: Optional[IndusRightsRecord] = None
    provenance_chain: List[IndusProvenanceEvent] = Field(default_factory=list)

    # ── Quality ───────────────────────────────────────────────────────────────
    confidence: float = Field(ge=0.0, le=1.0, default=0.5)
    review_state: ReviewState = ReviewState.UNREVIEWED

    # ── Cross-references ──────────────────────────────────────────────────────
    cisi_id: Optional[str] = None
    mahadevan_id: Optional[str] = None
    accession_number: Optional[str] = None
    related_object_ids: List[str] = Field(default_factory=list)

    # ── Citation ──────────────────────────────────────────────────────────────
    _citation: dict = {
        "primary_sources": ["A.1", "A.7", "I.1", "I.2", "I.3", "I.4", "I.5"],
        "derivation": (
            "Object records assembled from free open sources per the ICIT-Scale "
            "Indus Corpus Reconstruction plan (2026-05-14). See CITATIONS.md."
        ),
    }

    def first_surface_diplomatic(self) -> Optional[str]:
        """Return diplomatic text of first surface with a text witness."""
        for surface in self.surfaces:
            for tw in surface.text_witnesses:
                if tw.text_code_diplomatic:
                    return tw.text_code_diplomatic
        return None

    def all_sign_ids(self, scheme: Optional[SignIdScheme] = None) -> List[str]:
        """Return all sign IDs (optionally filtered by scheme) across all surfaces."""
        result = []
        for surface in self.surfaces:
            for tw in surface.text_witnesses:
                for si in tw.sign_instances:
                    if scheme is None or si.source_scheme == scheme:
                        result.append(si.source_sign_id)
        return result

    def to_icit_format(self) -> str:
        """
        Return ICIT-format diplomatic string for the primary text witness.
        Format: +NNN-NNN-NNN+ with 000 for eroded and ++ for unknown-length eroded.
        """
        for surface in self.surfaces:
            for tw in surface.text_witnesses:
                if tw.text_code_diplomatic:
                    return tw.text_code_diplomatic
                if tw.sign_instances:
                    ids = [si.source_sign_id for si in tw.sign_instances]
                    return "+" + "-".join(ids) + "+"
        return ""


# ── Helper: parse ICIT-format diplomatic string ───────────────────────────────

def parse_diplomatic(text: str) -> List[str]:
    """
    Parse an ICIT-format diplomatic string into a list of sign ID tokens.

    Rules:
      - Strip outer + markers (initial/terminal position markers)
      - Split on hyphens
      - Preserve "000" (one eroded sign) and "++" (eroded text-part of unknown length)
      - Handle multi-part texts (multiple + clusters)

    Returns list of sign ID strings (may include "000" and "++").
    """
    if not text:
        return []
    # Remove leading/trailing whitespace
    text = text.strip()
    # Split on + to separate text parts; rejoin with placeholder if needed
    parts = []
    for chunk in text.split("++"):
        chunk = chunk.strip("+").strip("-")
        if chunk:
            tokens = [t for t in chunk.split("-") if t]
            parts.extend(tokens)
        # Preserve the ++ marker between parts
        parts.append("++")
    # Remove trailing "++" placeholder if we added an extra one
    if parts and parts[-1] == "++":
        parts.pop()
    return parts


def icit_format(sign_ids: List[str]) -> str:
    """
    Encode a list of sign ID strings to ICIT diplomatic format.
    Adds outer + markers and hyphen separators.
    """
    if not sign_ids:
        return ""
    return "+" + "-".join(sign_ids) + "+"
