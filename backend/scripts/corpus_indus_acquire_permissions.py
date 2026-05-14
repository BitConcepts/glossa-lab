"""Indus Corpus — Permissions Batch (STUB — CONTACT REQUIRED).

STUB: Tracks and generates outreach templates for institutions requiring
formal permissions before data can be ingested or published.

Priority contact list (from deep-research-report.md, 2026-05-14):

1. RMRL / Indus Research Centre — HIGHEST PRIORITY
   Contact: https://rmrl.in/en/irc  |  indusscript.in
   Ask for:
     - Concordance cooperation and portal export possibilities
     - Mahadevan crosswalk guidance
     - Bulletin reuse permission
     - Access to the new expanded concordance (in development)
   Why: Only institution with a live Mahadevan-1977-based digital portal
   and an active new concordance project.

2. National Museum, New Delhi
   Contact: https://nationalmuseumindia.gov.in/en/contact-us
   Ask for:
     - High-res object images for Indus-script objects (batch request by accession)
     - Object metadata verification
     - Permission for corpus use (internal research)
     - Gallery catalog support
   Priority: Batch request after baseline inventory from open sources.

3. ASI Archive and Central Archaeological Library
   Contact: https://asi.nic.in/pages/archive
   Ask for:
     - High-res historical photos (glass negatives, excavation photos)
     - Permission to reproduce/report for corpus use
     - Access to excavation documentation and D-forms
     - Bulk metadata reconciliation
   Priority: After open-source baseline.

4. Penn Museum (high-res images)
   Current status: CC BY 4.0 metadata acquired. Images are noncommercial-educational.
   Contact: https://www.penn.museum/collections/permission-to-reproduce.php
   Ask for: Publication-quality images for identified Indus objects.

5. British Museum / BM Images
   Contact: https://britishmuseumimages.com/
   Ask for: Licensing package for targeted high-value Indus seals.

6. Finnish Academy / Tiedekirja / CISI editors
   Contact: https://tiedekirja.fi
   Ask for: Digital rights status and scan/use permission for internal research.

_citation:
  primary_sources: ["I.1", "I.2", "I.3", "I.7", "I.8"]
  derivation: "Permissions tracking stub for Indus corpus reconstruction."
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parents[2]
LOG_PATH = REPO / "glossa-corpus" / "indus" / "sources" / "permissions_log.json"

CONTACTS = [
    {
        "institution": "RMRL / Indus Research Centre",
        "priority": 1,
        "contact_url": "https://rmrl.in/en/irc",
        "ask": "Concordance cooperation, portal export, Mahadevan crosswalk guidance, new expanded concordance access",
        "status": "not_contacted",
        "date_contacted": None,
        "response": None,
    },
    {
        "institution": "National Museum, New Delhi",
        "priority": 2,
        "contact_url": "https://nationalmuseumindia.gov.in/en/contact-us",
        "ask": "Batch high-res object images, metadata verification, corpus-use permission",
        "status": "not_contacted",
        "date_contacted": None,
        "response": None,
    },
    {
        "institution": "ASI Archive and Central Archaeological Library",
        "priority": 3,
        "contact_url": "https://asi.nic.in/pages/archive",
        "ask": "Glass negatives, excavation photos, D-forms, permission to reproduce",
        "status": "not_contacted",
        "date_contacted": None,
        "response": None,
    },
    {
        "institution": "Penn Museum (high-res images)",
        "priority": 4,
        "contact_url": "https://www.penn.museum/collections/permission-to-reproduce.php",
        "ask": "Publication-quality images for Indus objects (batch by accession)",
        "status": "not_contacted",
        "date_contacted": None,
        "response": None,
    },
    {
        "institution": "British Museum / BM Images",
        "priority": 5,
        "contact_url": "https://britishmuseumimages.com/",
        "ask": "Licensing package for targeted high-value Indus seals",
        "status": "not_contacted",
        "date_contacted": None,
        "response": None,
    },
    {
        "institution": "Finnish Academy / Tiedekirja / CISI editors",
        "priority": 6,
        "contact_url": "https://tiedekirja.fi",
        "ask": "Digital rights status and scan/use permission for internal research",
        "status": "not_contacted",
        "date_contacted": None,
        "response": None,
    },
]


def main() -> int:
    print("=== Indus Corpus — Permissions Batch Status ===")
    print()

    # Load existing log if any
    existing = {}
    if LOG_PATH.exists():
        try:
            existing = {c["institution"]: c for c in json.loads(LOG_PATH.read_text(encoding="utf-8"))}
        except Exception:
            pass

    contacts = []
    for c in CONTACTS:
        existing_entry = existing.get(c["institution"], {})
        merged = {**c, **{k: v for k, v in existing_entry.items() if v is not None}}
        contacts.append(merged)
        status = merged.get("status", "not_contacted")
        contacted = merged.get("date_contacted") or "-"
        print(f"  [{merged['priority']}] {merged['institution']}")
        print(f"      Status: {status}  |  Contacted: {contacted}")
        print(f"      URL: {merged['contact_url']}")
        print(f"      Ask: {merged['ask'][:80]}")
        print()

    # Save log
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    LOG_PATH.write_text(json.dumps(contacts, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Log saved: {LOG_PATH}")
    print()
    print("To update a contact status, edit the log file directly:")
    print(f"  {LOG_PATH}")
    print('  Set "status" to: contacted / awaiting_response / granted / denied / in_negotiation')
    return 0


if __name__ == "__main__":
    sys.exit(main())
