# Owner decision — freeze pins are not amended to corrected bytes (2026-10-23)

**Date:** 2026-10-23
**Owner:** Tristen Pierson
**Status:** Decision recorded. This record edits no frozen record,
amends no pin, and executes no study — see the ruling and the
acceptance check below.

## Provenance of this record

On 2026-10-22 the material-audit fix commission (Spec 025 audit)
edited three literature-registry records in place to correct source
facts (proposals P2, P4, and the literature half of P8). The edits
collided with frozen whole-file pins: the records are pinned, byte
for byte, by the freeze tests of Spec 055 and Spec 057. The repair
(recorded in
`specs/025-paper-search-research-check/audit-2026-10-22/fix_repair_2026-10-22.md`)
restored all three records byte-for-byte to their pins, and the
corrections were preserved as dated `audit_correction_2026_10_22`
notes on the claims dossiers. The repair record left one question
open: whether to now amend the freeze pins to the corrected bytes.

On 2026-10-23 the owner approved the waiting-decisions plan package
(`2026-10-23-waiting-decisions-plan.md`, Item 4), whose recommendation
was NO. This entry is that ruling, recorded.

## The ruling

**The three pinned registry records stay exactly as frozen. Their
freeze pins are not amended, and the records are not corrected in
place.**

- `glossa-indus/literature/documents/ancient_writing_and_modern_technologies_51831ac9.json`
  — SHA-256 `92e19e6def7eccb42ba0e9f53f5ef3bf9dbb0b9717aa3d675cecb971f5ab0e5c`,
  pinned by `backend/tests/test_spec055_freeze.py`.
  Its correction (proposal P4) lives as the `audit_correction_2026_10_22`
  note on `glossa-indus/claims/extracted_claims/ancient_writing_and_modern_technologies_51831ac9.json`.
- `glossa-indus/literature/documents/fuls2023_catalog_of_indussigns_searchins_1dbdecdb.json`
  — SHA-256 `bb23e5e9f90c30ebebb2d45e2967fb668a54432a56692a8772753fd228316f47`,
  pinned by `backend/tests/test_spec057_freeze.py`.
  Its correction (proposal P2) lives as the `audit_correction_2026_10_22`
  note on `glossa-indus/claims/extracted_claims/fuls2023_catalog_of_indussigns_searchins_1dbdecdb.json`.
- `glossa-indus/literature/documents/positional_analysis_of_indus_signs_a2bedc93.json`
  — SHA-256 `9b95174bad62c9a4879ae3db28a03ee52bc665df4e1d9897e65f84f353baa53c`,
  pinned by `backend/tests/test_spec057_freeze.py`.
  Its correction (proposal P8, identification limb) lives as the
  `audit_correction_2026_10_22` note on
  `glossa-indus/claims/extracted_claims/positional_analysis_of_indus_signs_a2bedc93.json`.

## Reasoning (from the approved plan)

A freeze pin is an attestation — "these are the bytes the frozen
study ran against." Re-pinning to corrected bytes rewrites that
attestation after the fact and silently changes what every
downstream record citing the pins refers to; it converts a freeze
from a fixed point into a moving one. The append-only discipline
the program uses everywhere else — corrections as dated notes
riding on top of untouched frozen records — already carries the
corrected facts to any reader of the dossiers.

## Accepted cost, stated

This ruling does not establish that the registry files are correct —
they are not, in the three fields the audit found. Anyone who reads
the raw registry records without the dossier notes still sees the
uncorrected fields. That is the accepted, stated cost of keeping
freezes frozen; the notes exist precisely so the correction is
never lost.

## Acceptance

The landing of this entry is checked by TEST: this entry reads back
from merged `main`, and the Spec 055 / Spec 057 freeze tests pass
*unmodified* against the untouched pins — the check that proves no
frozen byte moved. (Executed and quoted in the landing PR.)
