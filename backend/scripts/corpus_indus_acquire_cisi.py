"""Indus Corpus — CISI Volume Acquisition (STUB — PURCHASE REQUIRED).

STUB: This script is a placeholder for when the CISI volumes are purchased.

Acquisition plan:
  1. Purchase CISI bundle 1+2+3.1+3.2 (€300) + CISI 3.3 (€220) from:
     https://tiedekirja.fi/en/corpus-of-indus-seals-and-inscriptions-1
  2. Obtain digital/scan rights for internal research use (contact Tiedekirja).
  3. Place scanned PDFs in:
     glossa-corpus/indus/sources/cisi/raw/{date}/vol1.pdf, vol2.pdf, ...
  4. Uncomment and complete the ingest functions below.

Volume scope:
  CISI 1: Collections in India
  CISI 2: Collections in Pakistan
  CISI 3.1: Mohenjo-daro + Harappa (outside India/Pakistan) + new material
  CISI 3.2: Kalibangan, Ahar, Balathal, Gilund, Rojdi, etc.
  CISI 3.3: Indo-Iranian Borderlands

Sign encoding in CISI: Parpola 1982 (P-numbers, same as mayig-cisi corpus).
Crosswalk: use IndusSignCrosswalk.parpola_to_m77() and .parpola_to_fuls()

_citation:
  primary_sources: ["C.1"]
  derivation: "Stub for CISI volume acquisition. See CITATIONS.md C.1 for full reference."
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).parents[2]
CORPUS = REPO / "glossa-corpus" / "indus" / "sources" / "cisi"


def main() -> int:
    print("=" * 60)
    print("STUB: CISI acquisition not yet implemented.")
    print()
    print("PURCHASE REQUIRED:")
    print("  CISI bundle 1+2+3.1+3.2: €300")
    print("  CISI 3.3:                 €220")
    print("  Total:                    €520")
    print()
    print("Purchase URL: https://tiedekirja.fi/en/corpus-of-indus-seals-and-inscriptions-1")
    print()
    print("After purchase:")
    print("  1. Obtain scan/internal-use rights from Tiedekirja")
    print("  2. Place PDFs in glossa-corpus/indus/sources/cisi/raw/{date}/")
    print("  3. Update provenance.yaml with download_date and checksum_sha256")
    print("  4. Implement PDF parsing / OCR pipeline in this script")
    print("  5. Run: shell.cmd python backend/scripts/corpus_indus_acquire_cisi.py")
    print("=" * 60)

    # TODO: implement after purchase
    # from glossa_lab.data.indus_sign_crosswalk import get_crosswalk
    # xw = get_crosswalk()
    # ... parse CISI PDFs, extract inscription sequences (P-numbers),
    # ... convert to ICIT format, write to staging
    return 1  # stub returns non-zero until implemented


if __name__ == "__main__":
    sys.exit(main())
