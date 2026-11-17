"""Mechanical guard for the superseded v1 validator routines (Spec 095).

Why this module exists
----------------------
The 2026-10-26 repair package landed corrected (v2) validator routines
alongside the untouched v1 originals: ``phonotactics_v2`` succeeds the
Phase-58 phonological checker, ``site_stats_v2`` succeeds the Phase-69
chi-square routine, ``crosswalk_provenance`` succeeds the Phase-96
crosswalk construction, ``corpus_frames`` sits alongside the historical
compressed frame, and ``replay076`` wraps the frozen Spec 076 pilot.

The Stage 0 census for Spec 095 (2026-11-15) found that the v1 routines
remained executable inside the live application, unguarded, through
four experiment-graph node paths and the shared provenance-audit
library:

* ``IndusPhonologicalGap`` — executes ``phase58_phonological_gap.py``;
* ``IndusSiteStratification`` — executes
  ``phase69_site_stratification.py`` and formats its preset p-value
  into the node output text;
* ``IndusCisiCrosswalk116`` — executes ``phase96_cisi_crosswalk.py``,
  re-running the circular crosswalk construction;
* ``IndusProvenanceRecompute`` — executes
  ``phase108_provenance_recompute.py``, which calls the v1 library
  routines ``provenance_audit.phonotactic_check`` and
  ``provenance_audit.site_invariance`` (they dynamically load the
  Phase-58 / Phase-69 machinery).

Spec 095 claim C095-5 requires each of those paths to be migrated to
its corrected v2 module, retired from the node registry, or
mechanically guarded so its output cannot enter a claim-bearing record
unlabelled. Stage 2 (2026-11-16) discharges the four paths by this
guard: the node functions return a labelled refusal instead of
executing the v1 script, the two provenance-audit v1 entry points
raise :class:`LegacyValidatorRefused`, and the three v1 scripts refuse
direct execution from ``main()``. The v1 code stays in the tree for
the record, exactly as the repair left it; frozen study machinery
that loads the Phase-58 module directly (the Phase-113/115 battery
tests) is historical, is not part of the live application, and is
outside this guard's scope.

The guard is mechanical, not documentary: there is no code path from
a guarded entry point to a v1 computation. The pinning test
(``backend/tests/test_spec095_validator_pinning.py``) plants legacy
v1-rule calls in claim-bearing paths and proves they fail.
"""

from __future__ import annotations

from typing import Any, NoReturn

__all__ = [
    "GUARDED_NODE_IDS",
    "GUARDED_PATHS",
    "LegacyValidatorRefused",
    "refusal_result",
    "refuse_legacy_validator",
]


class LegacyValidatorRefused(RuntimeError):
    """A superseded v1 validator routine was invoked through a guarded path."""


# The guarded paths of record. ``v1_routine`` names what would have run;
# ``superseded_by`` names the corrected module a caller should use
# instead. Node paths carry the registry id under ``node_id``.
GUARDED_PATHS: dict[str, dict[str, str]] = {
    "phonotactics_v1_node": {
        "node_id": "IndusPhonologicalGap",
        "v1_routine": "backend/scripts/phase58_phonological_gap.py "
                      "(Phase-58 phonological checker)",
        "superseded_by": "glossa_lab.phonotactics_v2",
    },
    "site_stats_v1_node": {
        "node_id": "IndusSiteStratification",
        "v1_routine": "backend/scripts/phase69_site_stratification.py "
                      "(Phase-69 chi-square routine)",
        "superseded_by": "glossa_lab.site_stats_v2",
    },
    "crosswalk_v1_node": {
        "node_id": "IndusCisiCrosswalk116",
        "v1_routine": "backend/scripts/phase96_cisi_crosswalk.py "
                      "(Phase-96 crosswalk construction)",
        "superseded_by": "glossa_lab.crosswalk_provenance",
    },
    "provenance_recompute_v1_node": {
        "node_id": "IndusProvenanceRecompute",
        "v1_routine": "backend/scripts/phase108_provenance_recompute.py "
                      "(Phase-108 recompute over the Phase-58/Phase-69 "
                      "v1 routines)",
        "superseded_by": "glossa_lab.phonotactics_v2 and "
                         "glossa_lab.site_stats_v2",
    },
    "provenance_audit_phonotactic_check": {
        "v1_routine": "glossa_lab.pipelines.provenance_audit."
                      "phonotactic_check (Phase-58 machinery)",
        "superseded_by": "glossa_lab.phonotactics_v2",
    },
    "provenance_audit_site_invariance": {
        "v1_routine": "glossa_lab.pipelines.provenance_audit."
                      "site_invariance (Phase-69 machinery)",
        "superseded_by": "glossa_lab.site_stats_v2",
    },
}

GUARDED_NODE_IDS: tuple[str, ...] = tuple(
    path["node_id"] for path in GUARDED_PATHS.values() if "node_id" in path
)


def _message(path_id: str) -> str:
    path = GUARDED_PATHS[path_id]
    return (
        f"LegacyValidatorRefused: {path['v1_routine']} is a superseded "
        f"v1 validator routine (2026-10-26 repair) and is mechanically "
        f"guarded under Spec 095 claim C095-5: it cannot execute "
        f"through a claim-bearing path of the live application. "
        f"Use {path['superseded_by']} instead."
    )


def refuse_legacy_validator(path_id: str) -> NoReturn:
    """Raise the labelled refusal for a guarded v1 path. Never returns."""
    raise LegacyValidatorRefused(_message(path_id))


def refusal_result(path_id: str, *, gpu_device: str | None = None) -> dict[str, Any]:
    """The labelled refusal a guarded experiment node returns.

    The result carries the refusal under ``legacy_validator_refusal``
    and as its ``error``/``text``, and no v1-computed value of any
    kind, so a guarded node's output cannot enter a record unlabelled
    or be mistaken for a computed result.
    """
    path = GUARDED_PATHS[path_id]
    message = _message(path_id)
    result: dict[str, Any] = {
        "error": message,
        "text": message,
        "legacy_validator_refusal": {
            "path": path_id,
            "node_id": path.get("node_id"),
            "v1_routine": path["v1_routine"],
            "superseded_by": path["superseded_by"],
            "claim": "C095-5",
            "spec": "Spec 095 Stage 2",
        },
    }
    if gpu_device is not None:
        result["gpu_device"] = gpu_device
    return result
