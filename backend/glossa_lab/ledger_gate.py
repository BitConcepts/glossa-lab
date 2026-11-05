"""Spec 086 Stage 3 — the verification gate over the
ledger → matrix → map chain (spec.md Point 4).

The gate recomputes every downstream layer from the ledger
by an **independent route**: the matrix definitions below are
the gate's own registered copies of `matrix-defs v1`
(`glossa-indus/matrix/DEFINITIONS.md`), deliberately not
imported from the generator (`matrix_generate.py`). A
deliberate definitions change is made in all copies in the
same motion (DEFINITIONS.md §12); a change made in only one
copy is exactly the divergence this gate exists to catch.

Check classes (spec.md Point 4(c)): V1 ledger validity
(including the recorded-source-hash arm: every `sources[]`
and annotation-sidecar hash recorded in the ledger verifies
against the canonical hash of the named file — the Stage 1
gap this stage closes), V2 count equivalence, V3 matrix
recomputation, V4 relation-carrying citations (tie rules
T1–T4 plus the numeric arm of harmonization adoption 3,
item 2), V5 map recomputation, V6 anchor shares, V7 lossless
regeneration (checked mode, `--regen`), V8 settling
canonicals (Stage 4: the canonical scenarios and comparison
registered in `glossa-indus/ledger/settling-canonical.json`
reproduced under the gate's own glossa-settle-1 route — the
settle definitions below are the gate's registered copies,
not imported from the engine — plus the settling layer's
scenario/verdict separation check), V9 no write path,
V10 program-map equivalence (Spec 088 Stage 3: the
program map recomputed from the ledger + taxonomy under
the gate's own program-map-defs v1 copies — not imported
from the builder — and byte-compared against the
published artifacts, with taxonomy coverage checked
bidirectionally and the stamp checked against the
current ledger; Stage 4 adds the generated page to the
byte-compared artifact list, rendered from the
recomputed data under the gate's own template copies),
V11 run-binding (Spec 089 Stage 5: the run stores, their
indexes, the junction store, and the run-produced
artifacts checked under the gate's own registered copies
of run-defs v2 — not imported from the run tooling —
for resolving producing bindings, quarantined citations,
store census and index integrity, and junction
completeness; the gate verifies junction reports and
index acts, it never originates an analysis, an act, or
an adjudication).

**The gate never writes.** It calls only pure builders and
read paths; it imports no write entry point (V9 audits this
in the gate's own source). Publication lives in
`gated_publish.py`, which writes candidates, runs this gate
against them, and replaces the published artifacts only on
ALL PASS (C086-11).
"""

from __future__ import annotations

import ast
import hashlib
import json
import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from glossa_lab import ledger_intake as li

# ---------------------------------------------------------------------------
# Registered definitions — the gate's own copies of
# matrix-defs v1 (glossa-indus/matrix/DEFINITIONS.md).
# NOT imported from the generator: this is the independent
# recomputation route (spec.md Point 4, V3).

GATE_MATRIX_DEFS_VERSION = "matrix-defs v1"
MATRIX_REL_DIR = "glossa-indus/matrix"
MAP_REL = "glossa-indus/map/map-data.json"
ANCHORS_REL = "backend/reports/INDUS_FINAL_ANCHORS.json"
PROVENANCE_REGISTER_REL = "reports/phase108_provenance_register.json"
CORPUS_REL = "glossa-corpus/indus/exports/indus_research.jsonl"

RELATIONS = ("supports", "opposes", "constrains")
COLUMN_CLASSES = (
    "studies",
    "documents",
    "research_checks",
    "anchors",
    "corpus_texts",
)
RULES = {
    "R1": "evidence instance (documents, supports)",
    "R2": "bundle evidence direction (documents, per stored direction)",
    "R3": "study outcome (studies, per the outcome table)",
    "R4": "anchor assignment (anchors, constrains)",
    "R5": "research-check verdict (research checks; verdict table empty in v1)",
    "R6": "settling instrument (constrains; instrument register empty in v1)",
}
DIRECTION_RELATIONS = {
    "supports": "supports",
    "opposes": "opposes",
    "constrains": "constrains",
}
# The outcome table (DEFINITIONS.md §6): no outcome maps to
# supports in v1; an unexecuted or null outcome carries
# neither relation.
BEARING_OUTCOMES = {
    "NOT SUPPORTED": "opposes",
    "INCONSISTENT": "opposes",
    "NOT NUMERAL-LIKE": "opposes",
}
VERDICT_RELATIONS: dict[str, str] = {}
COOCCURRENCE_PARAMS = {"window": 2, "min_freq": 3, "min_edge_weight": 2}
COOCCURRENCE_PIPELINE = "glossa_lab.pipelines.cooccurrence.build_cooccurrence_network"

# The strict-anchor rule as recorded in the anchors file
# itself (metadata.spec029_phase_h_annotation.strict_set_rule,
# Spec 029 Phase H / D-A): confidence in {HIGH, MEDIUM} AND
# the Phase-108 register category not in the SA-lineage set
# AND the register's sa_in_chain is false.
STRICT_RULE_ID = "strict_sa_independent_hm"
STRICT_CONFIDENCES = ("HIGH", "MEDIUM")
SA_LINEAGE_CATEGORIES = ("SA_DERIVED", "SA_CONFIRMED_ONLY")

# ---------------------------------------------------------------------------
# Registered definitions — the gate's own copies of
# glossa-settle-1 (`glossa-indus/ledger/SETTLING-SEMANTICS.md`),
# for V8. NOT imported from the engine (`settling.py`):
# the same independent-route discipline as the matrix
# definitions above. A deliberate semantics change is made
# in all copies in the same motion (a new semantics
# version); a change in only one copy is the divergence
# V8 exists to catch.

SETTLE_SEMANTICS_VERSION = "glossa-settle-1"
SETTLING_CANONICAL_REL = "glossa-indus/ledger/settling-canonical.json"
# Sign identity is by (frame, number) under glossa-settle-1
# §2 — the register key is the frame's prefix plus the
# number zero-padded to three digits. This is the settling
# identity rule, deliberately NOT matrix-defs v1 R4's
# literal key construction (the divergence is registered
# in the semantics and stands).
SETTLE_FRAME_PREFIXES = {"mahadevan": "M"}
# The outcome table (SETTLING-SEMANTICS.md §5, carrying
# matrix-defs v1 §6): tallies are keyed supporting /
# opposing / constraining; no recorded outcome maps to
# supporting in v1.
SETTLE_BEARING_OUTCOMES = {
    "NOT SUPPORTED": "opposing",
    "INCONSISTENT": "opposing",
    "NOT NUMERAL-LIKE": "opposing",
}
SETTLE_TALLY_KEYS = ("supporting", "opposing", "constraining")

# The numeric arm's registered comparator vocabulary
# (harmonization adoption 3, item 2 — the Atlas's
# claim.measurement shape: value / comparator / bound).
NUMERIC_COMPARATORS = ("<=", ">=", "=", "in")

# ---------------------------------------------------------------------------
# Registered definitions — the gate's own copies of
# map-defs v1 (glossa-indus/map/DEFINITIONS.md), for V5's
# map recomputation (Stage 5). NOT imported from the
# builder (map_generate.py): the same independent-route
# discipline as the matrix and settling definitions above.
# A deliberate definitions change is made in all copies in
# the same motion (DEFINITIONS.md §11).

GATE_MAP_DEFS_VERSION = "map-defs v1"
ASSIGNMENT_SETS_REL = "glossa-indus/ledger/assignment-sets.json"
RUNS_REL_DIR = "glossa-indus/ledger/runs"
COMPARISON_REL = (
    "specs/086-winning-combination-adoption/records/"
    "stage-4-dual-run-comparison.json"
)
PENDING_VALIDATION_STATUS = "pending_non_sa_validation"
PENDING_VALIDATIONS_REASON = (
    "the anchors register records no review dates for the "
    "pending validations, so they appear as a count, not as "
    "dated items (decision Q4)"
)
SETTLING_LABEL = (
    "Computation over ledgered relations under "
    "glossa-settle-1 semantics. Establishes what the ledger "
    "implies under these rules, not what the script says."
)
MAP_RUN_RESULT_FIELDS = (
    "scope_signs",
    "assigned_count",
    "assigned_share",
    "contexts_touched",
    "strict_contexts",
    "consistent",
    "non_strict_contexts",
    "conflicts",
    "strict_agreement_share",
    "claims_touched",
    "forced",
    "s_r3",
)
MAP_S_R3_NOTE = (
    "no positional-class table exists in the "
    "record; the rule is registered but inert "
    "and reports a determinate zero in every "
    "run record"
)

# ---------------------------------------------------------------------------
# Registered definitions — the gate's own copies of
# program-map-defs v1
# (glossa-indus/map/PROGRAM-MAP-DEFINITIONS.md), for V10
# (Spec 088 Stage 3). NOT imported from the builder
# (program_map_generate.py): the same independent-route
# discipline as the matrix, settling, and map definitions
# above. A deliberate definitions change is made in all
# copies in the same motion
# (PROGRAM-MAP-DEFINITIONS.md §12); a change in only one
# copy is the divergence V10 exists to catch.

GATE_PROGRAM_MAP_DEFS_VERSION = "program-map-defs v1"
PROGRAM_MAP_TAXONOMY_VERSION = "program-map-taxonomy v1"
PROGRAM_MAP_REL = "glossa-indus/map/program-map.json"
PROGRAM_MAP_FINDS_REL = "glossa-indus/map/program-map-finds.json"
PROGRAM_MAP_HTML_REL = "glossa-indus/map/program-map.html"
PROGRAM_MAP_TAXONOMY_REL = "glossa-indus/map/program-map-taxonomy.json"
PROGRAM_MAP_SPECS_REL = "specs"

# The derivation table (PROGRAM-MAP-DEFINITIONS.md §4.2,
# D-088-3): ledger status → node class, applied to the
# governing entry. A status outside this table is a
# recomputation refusal — the table is total over the
# registered vocabulary because the route refuses the
# unregistered, not because it guesses at it.
PM_STATUS_TO_CLASS = {
    "strongly_supported": "positive",
    "contradicted": "negative",
    "unsupported": "negative",
    "partially_falsified": "negative",
    "superseded": "closed_other",
    "draft": "open",
    "untested": "open",
    "partially_supported": "open",
}
PM_CLAIM_CLASSES = ("positive", "negative", "open", "closed_other")
PM_STUDY_CLASSES = PM_CLAIM_CLASSES + ("unjudged",)
PM_IN_FLIGHT = "in_flight"
# The standing-text template (§4.3): a mechanical rendering
# over the governing entry's verbatim fields.
PM_STANDING_TEMPLATE = (
    "Ledger standing: status {status} · stage {stage} · "
    "falsifier {falsifier}"
)
# The registered name-only forms (§7): a restricted study
# renders exactly this standing, no class, no member data.
PM_RESTRICTED_NAME_ONLY = {
    "072-fish-family-profiles-redesign":
        "executed — held under the Roif gate",
}
# Keys the taxonomy format must never carry, anywhere, at
# any depth (§8): no standings by construction (C088-17).
PM_FORBIDDEN_TAXONOMY_KEYS = frozenset(
    {
        "standing",
        "standing_text",
        "status",
        "class",
        "verdict",
        "score",
        "curated",
    }
)
# The find kinds (§6) — exactly four exist in v1.
PM_FIND_KINDS = (
    "bundle_less_study",
    "extracted_null_falsifier",
    "judgment_call",
    "restricted_node",
)

# The page template (Spec 088 Stage 4 amendment to V10's
# artifact list, recorded in the S4 stage record): the
# published page is exactly the registered template
# wrapped around the two data artifacts embedded
# verbatim. The gate carries its own copies of the three
# pieces, as it carries the tables above; the builder's
# copies live in program_map_generate.py, the agreement
# test pins the two sets byte-equal, and a change made in
# only one copy is the divergence V10 exists to catch.
PM_PAGE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Program map — Glossa-Lab Indus program (Spec 088)</title>
<style>
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { margin: 0; padding: 0 16px 48px; background: #f7f7f4;
  color: #1c1e21; font: 15px/1.45 -apple-system, "Segoe UI", Roboto,
  Helvetica, Arial, sans-serif; }
.pm-header { max-width: 1080px; margin: 0 auto; padding: 24px 0 8px; }
.pm-header h1 { font-size: 26px; margin: 0 0 6px; }
.pm-sub { color: #44484d; max-width: 72ch; margin: 0 0 10px; }
.pm-stamp { font: 12px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace;
  color: #33363a; word-break: break-all; margin: 0 0 8px; }
.pm-domain-counts { list-style: none; margin: 0 0 14px; padding: 0;
  display: flex; flex-wrap: wrap; gap: 6px; }
.pm-domain-count { background: #eceee9; border: 1px solid #d4d8d0;
  border-radius: 999px; padding: 2px 10px; font-size: 13px; }
.pm-controls { display: flex; flex-wrap: wrap; gap: 10px 18px;
  align-items: center; margin-bottom: 6px; }
.pm-filters { display: flex; flex-wrap: wrap; gap: 6px; }
.pm-filter { border: 1px solid #b9beb4; background: #fff; color: #1c1e21;
  border-radius: 999px; padding: 3px 12px; font-size: 13px; cursor: pointer; }
.pm-filter.active { background: #1c1e21; color: #fff; border-color: #1c1e21; }
.pm-search-label { font-size: 13px; color: #44484d; }
.pm-search-label input { margin-left: 6px; padding: 4px 8px; width: 300px;
  max-width: 70vw; border: 1px solid #b9beb4; border-radius: 6px;
  font-size: 14px; }
main, .pm-finds { max-width: 1080px; margin: 0 auto; }
details.domain { background: #fff; border: 1px solid #dcded8;
  border-radius: 8px; margin: 12px 0; padding: 6px 14px 10px; }
summary { cursor: pointer; }
.domain-head { font-size: 18px; font-weight: 650; padding: 6px 0; }
.domain-head .counts, .study-head .counts { font-weight: 400;
  font-size: 13px; color: #55585d; margin-left: 8px; }
details.subdomain { margin: 4px 0 8px 10px; border-left: 3px solid #e3e5df;
  padding-left: 12px; }
.subdomain-head { font-size: 15px; font-weight: 600; padding: 4px 0; }
details.study { margin: 2px 0 2px 6px; }
.study-head { font-size: 14px; padding: 2px 0; }
.sname, .dname { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 13.5px; }
.claim-list { margin: 2px 0 6px 18px; }
.claim-row { display: flex; flex-wrap: wrap; gap: 4px 8px; align-items: baseline;
  padding: 2.5px 0; border-bottom: 1px dotted #e6e8e2; font-size: 13.5px; }
.cid { font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 12.5px; word-break: break-all; }
.standing { color: #33363a; }
.chip { border-radius: 999px; padding: 0 8px; font-size: 11.5px;
  line-height: 1.7; white-space: nowrap; }
.chip.positive { background: #dff2e1; color: #14532d; }
.chip.negative { background: #fbe3e0; color: #7f1d1d; }
.chip.open { background: #e2e9f7; color: #1e3a5f; }
.chip.closed_other { background: #e8e8e6; color: #3f4348; }
.chip.unjudged { background: #fdf0d3; color: #713f12; }
.chip.in_flight { background: #efe3f7; color: #4c1d95; }
.badge { background: #fdf0d3; color: #713f12; border-radius: 4px;
  padding: 0 6px; font-size: 11.5px; line-height: 1.7; }
.restricted-flag { background: #1c1e21; color: #fff; border-radius: 4px;
  padding: 0 6px; font-size: 11.5px; line-height: 1.7; }
.name-only { margin: 2px 0 4px 18px; color: #33363a; font-style: italic; }
.pm-finds { margin-top: 26px; background: #fff; border: 1px solid #dcded8;
  border-radius: 8px; padding: 10px 18px 16px; }
.pm-finds h2 { font-size: 19px; margin: 6px 0 4px; }
.finds-note { color: #44484d; max-width: 72ch; margin: 0 0 8px; }
.find-kind h3 { font-size: 15px; margin: 14px 0 4px; }
.find-list { margin: 0; padding-left: 20px; font-size: 13.5px; }
.find-list li { padding: 1.5px 0; word-break: break-all; }
.empty { color: #55585d; font-style: italic; margin: 2px 0; }
[hidden] { display: none !important; }
@media (max-width: 700px) {
  body { padding: 0 10px 36px; font-size: 14px; }
  .pm-header h1 { font-size: 22px; }
  .pm-search-label input { width: 100%; max-width: none; margin: 4px 0 0; }
  .pm-controls { flex-direction: column; align-items: stretch; }
  .claim-list { margin-left: 8px; }
  details.subdomain { margin-left: 2px; padding-left: 8px; }
}
</style>
</head>
<body>
<header class="pm-header">
<h1>Program map</h1>
<p class="pm-sub">Every claim and every study in the Glossa-Lab Indus
decipherment program, grouped by the program-map taxonomy, with
standings derived mechanically from the claims ledger. This page is
generated from the ledger by the program-map builder and verified by
the ledger gate (class V10); it is never hand-edited, and it carries
no aggregate score: counts are per domain only.</p>
<p class="pm-stamp" id="pm-stamp"></p>
<ul class="pm-domain-counts" id="pm-domain-counts"></ul>
<div class="pm-controls">
<div class="pm-filters" id="pm-filters" role="group" aria-label="Filter by class"></div>
<label class="pm-search-label">Search<input id="pm-search" type="search"
autocomplete="off" placeholder="claim id, standing, status, study, document"></label>
</div>
</header>
<main id="pm-tree"></main>
<section class="pm-finds" id="pm-finds"></section>
<script type="application/json" id="program-map-data">
"""
PM_PAGE_MID = """</script>
<script type="application/json" id="program-map-finds">
"""
PM_PAGE_TAIL = """</script>
<script>
(function () {
  "use strict";
  var pm = JSON.parse(document.getElementById("program-map-data").textContent);
  var fd = JSON.parse(document.getElementById("program-map-finds").textContent);
  var CLASS_LABELS = {
    positive: "positive", negative: "negative", open: "open",
    closed_other: "closed\\u2013other", unjudged: "unjudged",
    in_flight: "in flight"
  };
  var FILTERS = [
    ["all", "All"], ["positive", "Positive"], ["negative", "Negative"],
    ["open", "Open"], ["in_flight", "In flight"],
    ["closed_other", "Closed\\u2013other"], ["unjudged", "Unjudged"]
  ];
  var FIND_LABELS = {
    bundle_less_study: "Bundle-less studies (unjudged)",
    judgment_call: "Judgment calls",
    extracted_null_falsifier: "Extracted claims with no falsifier",
    restricted_node: "Restricted nodes (name-only)"
  };
  var FIND_ORDER = ["bundle_less_study", "judgment_call",
    "extracted_null_falsifier", "restricted_node"];

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text !== undefined && text !== null) n.textContent = text;
    return n;
  }
  function chip(cls) {
    var c = el("span", "chip " + cls, CLASS_LABELS[cls]);
    return c;
  }
  function searchText(parts) {
    return parts.filter(Boolean).join(" ").toLowerCase();
  }

  // Header: the stamp and the per-domain counts, copied from the
  // generated coverage block's own fields (never recomputed here).
  var stamp = pm.stamp;
  document.getElementById("pm-stamp").textContent =
    "As of the ledger: " + stamp.ledger_lines + " lines \\u00b7 sha256 " +
    stamp.ledger_sha256 + " \\u00b7 latest entry " +
    stamp.ledger_latest_entry_date + " \\u00b7 " + stamp.ledger_schema +
    " \\u00b7 " + stamp.program_map_defs + " \\u00b7 " +
    stamp.program_map_taxonomy;
  var countsList = document.getElementById("pm-domain-counts");
  Object.keys(pm.coverage.domains).sort().forEach(function (d) {
    var b = pm.coverage.domains[d];
    countsList.appendChild(el("li", "pm-domain-count",
      d + " \\u2014 " + b.studies + " studies \\u00b7 " + b.claims +
      " claims"));
  });

  // Filters and search operate only on generated fields (C088-8):
  // each row and group carries its node's own fields, and the
  // controls below only show or hide what the data already says.
  var state = { cls: "all", q: "" };
  var filtersBox = document.getElementById("pm-filters");
  FILTERS.forEach(function (pair) {
    var b = el("button", "pm-filter", pair[1]);
    b.type = "button";
    b.dataset.value = pair[0];
    if (pair[0] === "all") b.classList.add("active");
    b.addEventListener("click", function () {
      state.cls = pair[0];
      var kids = filtersBox.children;
      for (var i = 0; i < kids.length; i++) {
        kids[i].classList.toggle("active", kids[i] === b);
      }
      apply();
    });
    filtersBox.appendChild(b);
  });
  document.getElementById("pm-search").addEventListener("input",
    function (e) {
      state.q = e.target.value.trim().toLowerCase();
      apply();
    });

  var claimsByStudy = {}, claimsByDoc = {};
  pm.nodes.claims.forEach(function (c) {
    if (c.study) {
      (claimsByStudy[c.study] = claimsByStudy[c.study] || []).push(c);
    } else {
      (claimsByDoc[c.document] = claimsByDoc[c.document] || []).push(c);
    }
  });
  var studiesByGroup = {}, docsByGroup = {};
  pm.nodes.studies.forEach(function (s) {
    var k = s.domain + "|" + s.subdomain;
    (studiesByGroup[k] = studiesByGroup[k] || []).push(s);
  });
  pm.nodes.claims.forEach(function (c) {
    if (!c.study) {
      var k = c.domain + "|" + c.subdomain;
      (docsByGroup[k] = docsByGroup[k] || {})[c.document] = true;
    }
  });

  function claimRow(c) {
    var row = el("div", "claim-row");
    row.dataset.class = c.class;
    row.dataset.search = searchText([c.id, c.standing, c.status,
      c.class, c.domain, c.subdomain, c.study, c.document]);
    row.appendChild(el("span", "cid", c.id));
    row.appendChild(chip(c.class));
    row.appendChild(el("span", "standing", c.standing));
    return row;
  }
  function studyGroup(s) {
    var box = el("details", "study" + (s.restricted ? " restricted" : ""));
    box.dataset.class = s.class || "";
    box.dataset.search = searchText([s.id, s.class, s.domain,
      s.subdomain, s.standing]);
    var head = el("summary", "study-head");
    head.appendChild(el("span", "sname", s.id));
    if (s.restricted) {
      head.appendChild(el("span", "restricted-flag", "restricted"));
    } else {
      head.appendChild(chip(s.class));
      var mc = s.member_counts;
      var bits = [];
      ["positive", "negative", "open", "closed_other"].forEach(
        function (k) {
          if (mc[k]) bits.push(mc[k] + " " + CLASS_LABELS[k]);
        });
      head.appendChild(el("span", "counts",
        mc.total + (mc.total === 1 ? " claim" : " claims") +
        (bits.length ? " \\u00b7 " + bits.join(" \\u00b7 ") : "")));
      if (s.judgment_call) {
        head.appendChild(el("span", "badge", "judgment call"));
      }
    }
    box.appendChild(head);
    if (s.restricted) {
      box.appendChild(el("p", "name-only", s.standing));
    }
    var list = el("div", "claim-list");
    (claimsByStudy[s.id] || []).forEach(function (c) {
      list.appendChild(claimRow(c));
    });
    box.appendChild(list);
    return box;
  }
  function docGroup(docId) {
    var box = el("details", "study doc-group");
    box.dataset.class = "";
    box.dataset.search = searchText([docId]);
    var head = el("summary", "study-head");
    head.appendChild(el("span", "sname",
      "Extracted document \\u2014 " + docId));
    box.appendChild(head);
    var list = el("div", "claim-list");
    (claimsByDoc[docId] || []).forEach(function (c) {
      list.appendChild(claimRow(c));
    });
    box.appendChild(list);
    return box;
  }

  var tree = document.getElementById("pm-tree");
  Object.keys(pm.coverage.domains).sort().forEach(function (domain) {
    var dsec = el("details", "domain");
    dsec.open = true;
    var b = pm.coverage.domains[domain];
    var dh = el("summary", "domain-head");
    dh.appendChild(el("span", "dname", domain));
    dh.appendChild(el("span", "counts",
      b.studies + " studies \\u00b7 " + b.claims + " claims"));
    dsec.appendChild(dh);
    var subs = {};
    pm.nodes.studies.forEach(function (s) {
      if (s.domain === domain) subs[s.subdomain] = true;
    });
    pm.nodes.claims.forEach(function (c) {
      if (c.domain === domain) subs[c.subdomain] = true;
    });
    Object.keys(subs).sort().forEach(function (sub) {
      var ssec = el("details", "subdomain");
      ssec.open = true;
      var sh = el("summary", "subdomain-head");
      sh.appendChild(el("span", "sname", sub));
      ssec.appendChild(sh);
      var key = domain + "|" + sub;
      (studiesByGroup[key] || []).forEach(function (s) {
        ssec.appendChild(studyGroup(s));
      });
      var docs = docsByGroup[key] || {};
      Object.keys(docs).sort().forEach(function (docId) {
        ssec.appendChild(docGroup(docId));
      });
      dsec.appendChild(ssec);
    });
    tree.appendChild(dsec);
  });

  // The finds panel: the machine find list, grouped by its four
  // registered kinds. An empty kind is shown as an empty kind.
  var findsBox = document.getElementById("pm-finds");
  findsBox.appendChild(el("h2", null,
    "Finds \\u2014 where the picture is thin"));
  findsBox.appendChild(el("p", "finds-note",
    "The builder's machine find list, embedded verbatim from " +
    "program-map-finds.json. These shortfalls are what the gap " +
    "register is built from."));
  var byKind = {};
  fd.finds.forEach(function (f) {
    (byKind[f.kind] = byKind[f.kind] || []).push(f);
  });
  FIND_ORDER.forEach(function (kind) {
    var items = byKind[kind] || [];
    var sec = el("div", "find-kind");
    sec.appendChild(el("h3", null,
      FIND_LABELS[kind] + " \\u2014 " + items.length));
    if (!items.length) {
      sec.appendChild(el("p", "empty", "None on the current ledger."));
    } else {
      var ul = el("ul", "find-list");
      items.forEach(function (f) {
        var text = f.subject;
        if (f.document) text += " \\u00b7 document " + f.document;
        if (kind === "judgment_call") {
          text += " \\u00b7 positive " + f.positive +
            " \\u00b7 negative " + f.negative +
            " \\u00b7 total " + f.total;
        }
        ul.appendChild(el("li", null, text));
      });
      sec.appendChild(ul);
    }
    findsBox.appendChild(sec);
  });

  function matches(node) {
    if (state.cls !== "all" && node.dataset.class !== state.cls) {
      return false;
    }
    if (state.q &&
        (node.dataset.search || "").indexOf(state.q) === -1) {
      return false;
    }
    return true;
  }
  function apply() {
    var active = state.cls !== "all" || state.q !== "";
    var i, j;
    var rows = document.querySelectorAll(".claim-row");
    for (i = 0; i < rows.length; i++) {
      rows[i].hidden = !matches(rows[i]);
    }
    var groups = document.querySelectorAll("details.study");
    for (i = 0; i < groups.length; i++) {
      var anyClaim = false;
      var inner = groups[i].querySelectorAll(".claim-row");
      for (j = 0; j < inner.length; j++) {
        if (!inner[j].hidden) anyClaim = true;
      }
      groups[i].hidden = !(matches(groups[i]) || anyClaim);
      if (active && !groups[i].hidden) groups[i].open = true;
    }
    var subs = document.querySelectorAll("details.subdomain");
    for (i = 0; i < subs.length; i++) {
      var vis = false;
      var sg = subs[i].querySelectorAll("details.study");
      for (j = 0; j < sg.length; j++) {
        if (!sg[j].hidden) vis = true;
      }
      subs[i].hidden = !vis;
      if (active && vis) subs[i].open = true;
    }
    var doms = document.querySelectorAll("details.domain");
    for (i = 0; i < doms.length; i++) {
      var dvis = false;
      var ds = doms[i].querySelectorAll("details.subdomain");
      for (j = 0; j < ds.length; j++) {
        if (!ds[j].hidden) dvis = true;
      }
      doms[i].hidden = !dvis;
      if (active && dvis) doms[i].open = true;
    }
  }
})();
</script>
</body>
</html>
"""

WRITE_ENTRY_POINTS = ("append_entry", "write_ledger", "write_matrix")
REGISTERED_WRITERS = {
    "backend/glossa_lab/matrix_generate.py",
    "backend/glossa_lab/map_generate.py",
    # Spec 088: the program-map generator is a registered writer
    # from its first landing (Stage S1) — V9's census flags it
    # from the moment it exists, so T303's registration rides
    # with S1; the V10 recompute class itself lands in S3.
    "backend/glossa_lab/program_map_generate.py",
    "backend/glossa_lab/gated_publish.py",
    # Spec 089 Stage 5 (T502): the run machinery's writers
    # join the census in the same motion that extends the
    # artifact patterns to the run stores, the indexes, and
    # the junction store below — the run-record library
    # (records + index acts), the junction tool (reports +
    # quarantine acts through the library), and the settling
    # engine's store writer (run records + the bound
    # assignment-sets artifact). The tools/ CLIs write only
    # through these modules and carry no write call of their
    # own, so the census reads them as readers, exactly as
    # it reads the gated-publication CLIs' library.
    "backend/glossa_lab/run_records.py",
    "backend/glossa_lab/run_junction.py",
    "backend/glossa_lab/settling.py",
    "tools/ledger/generate_matrix.py",
    "tools/ledger/generate_map.py",
}
ARTIFACT_PATH_PATTERNS = (
    re.compile(r"glossa-indus/matrix"),
    re.compile(r"glossa-indus/map"),
    re.compile(r"(?<![\w.-])matrix\.json(?![\w-])"),
    re.compile(r"(?<![\w.-])matrix\.md(?![\w-])"),
    re.compile(r"(?<![\w.-])map-data\.json(?![\w-])"),
    # Spec 089 Stage 5: the run layer's artifacts — the
    # settling runs store, the junction store, every store's
    # run index, and the run-produced assignment-sets
    # artifact — join the census patterns, so an
    # unregistered write to any of them is a gate failure.
    re.compile(r"glossa-indus/ledger/runs"),
    re.compile(r"glossa-indus/ledger/junctions"),
    re.compile(r"run-index\.jsonl"),
    re.compile(r"assignment-sets\.json"),
)


# ---------------------------------------------------------------------------
# Result model


@dataclass
class Check:
    name: str
    status: str  # "PASS" | "FAIL" | "NOT-RUN"
    evidence: list[str] = field(default_factory=list)


@dataclass
class GateReport:
    root: Path
    mode: str
    checks: list[Check] = field(default_factory=list)
    header: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return all(c.status != "FAIL" for c in self.checks)

    def counts(self) -> dict[str, int]:
        out = {"PASS": 0, "FAIL": 0, "NOT-RUN": 0}
        for c in self.checks:
            out[c.status] = out.get(c.status, 0) + 1
        return out

    def render(self) -> str:
        lines = list(self.header)
        lines.append("checks:")
        for c in self.checks:
            lines.append(f"{c.status} {c.name}")
            for ev in c.evidence:
                lines.append(f"  {ev}")
        n = self.counts()
        lines.append(
            f"summary: {n['PASS']} PASS / {n['FAIL']} FAIL / "
            f"{n['NOT-RUN']} NOT-RUN"
        )
        lines.append("RESULT: " + ("PASS" if self.ok else "FAIL"))
        return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Register access for the gate's own derivation (hash-verified
# through the ledger's pointers, like the generator's route
# but independently coded here).


def _records_of(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if isinstance(data, dict):
        if isinstance(data.get("claims"), list):
            return [r for r in data["claims"] if isinstance(r, dict)]
        return [r for r in data.values() if isinstance(r, dict)]
    return []


class _GateRegisters:
    """Source records named by ledger entries, parsed only
    after their canonical hash verifies. Mismatches are
    collected, not raised, so the gate can name them under
    the check classes they belong to."""

    def __init__(self, root: Path):
        self.root = root
        self._parsed: dict[str, Any] = {}
        self.mismatches: list[str] = []

    def verify(self, rel_path: str, recorded_sha256: str) -> None:
        if rel_path in self._parsed or rel_path in self.mismatches:
            return
        target = self.root / rel_path
        if not target.is_file():
            self.mismatches.append(f"{rel_path}: file not found")
            return
        actual = li.sha256_file(target)
        if actual != recorded_sha256:
            self.mismatches.append(
                f"{rel_path}: recorded sha256 {recorded_sha256} "
                f"does not match the file on disk ({actual})"
            )
            return
        try:
            self._parsed[rel_path] = json.loads(
                target.read_text(encoding="utf-8")
            )
        except (OSError, json.JSONDecodeError) as exc:
            self.mismatches.append(f"{rel_path}: cannot parse: {exc}")

    def record(self, rel_path: str, claim_id: str) -> Optional[dict[str, Any]]:
        data = self._parsed.get(rel_path)
        if data is None:
            return None
        for record in _records_of(data):
            if record.get("claim_id") == claim_id or record.get("id") == claim_id:
                return record
        return None

    def records(self, rel_path: str) -> list[dict[str, Any]]:
        data = self._parsed.get(rel_path)
        return _records_of(data) if data is not None else []


def _load_registers(root: Path, entries: list[dict[str, Any]]) -> _GateRegisters:
    registers = _GateRegisters(root)
    for entry in entries:
        for source in entry.get("sources", []):
            registers.verify(source["path"], source["sha256"])
        if entry.get("kind") == "annotation":
            sidecar = entry.get("sidecar") or {}
            if sidecar.get("path") and sidecar.get("sha256"):
                registers.verify(sidecar["path"], sidecar["sha256"])
    return registers


def _source_record(
    registers: _GateRegisters, entry: dict[str, Any], role: str
) -> Optional[dict[str, Any]]:
    for source in entry.get("sources", []):
        if source.get("role") == role:
            return registers.record(source["path"], source["claim_id"])
    return None


def _outcome_blocks(
    registers: _GateRegisters, entry: dict[str, Any]
) -> dict[str, list[dict[str, Any]]]:
    """All stored outcome blocks of an entry's records,
    grouped by spec: {spec: [{outcome, date, pointer}]} —
    the gate's own scan, per DEFINITIONS.md §5 R3."""
    blocks_by_spec: dict[str, list[dict[str, Any]]] = {}
    for source in entry.get("sources", []):
        record = registers.record(source["path"], source["claim_id"])
        if record is None:
            continue
        for key, value in record.items():
            if (
                isinstance(value, dict)
                and "spec" in value
                and "outcome" in value
            ):
                spec = str(value["spec"])
                blocks_by_spec.setdefault(spec, []).append(
                    {
                        "spec": spec,
                        "outcome": str(value["outcome"]),
                        "date": value.get("date"),
                        "pointer": (
                            f"{source['path']}:{source['claim_id']}#{key}"
                        ),
                    }
                )
    return blocks_by_spec


def _governing(blocks: list[dict[str, Any]]) -> dict[str, Any]:
    """The governing block: latest dated governs; a block
    without a date sorts before dated blocks; ties break by
    pointer (DEFINITIONS.md §5 R3 total order)."""
    return sorted(blocks, key=lambda b: (str(b["date"] or ""), b["pointer"]))[-1]


# ---------------------------------------------------------------------------
# The gate's independent matrix recomputation (V3's route,
# and the derivation V4's tie rules read from).


@dataclass
class _Derivation:
    rows: list[dict[str, Any]]
    columns: list[dict[str, Any]]
    cells: list[dict[str, Any]]
    coverage: dict[str, Any]
    as_of: dict[str, Any]
    sign_block: Optional[dict[str, Any]]
    registers: _GateRegisters
    blocks: dict[str, dict[str, list[dict[str, Any]]]]  # entry id -> spec -> blocks


def _derive(
    root: Path,
    entries: list[dict[str, Any]],
    *,
    with_sign_block: bool,
) -> _Derivation:
    claims = [e for e in entries if e.get("kind") == "claim"]
    annotations = [e for e in entries if e.get("kind") == "annotation"]
    claim_ids = {e["id"] for e in claims}
    registers = _load_registers(root, entries)

    anchors_path = root / ANCHORS_REL
    anchors: dict[str, Any] = {}
    if anchors_path.is_file():
        anchors = json.loads(
            anchors_path.read_text(encoding="utf-8")
        ).get("anchors", {})

    cells: dict[tuple[str, str, str], dict[str, Any]] = {}
    study_columns: set[str] = set()
    document_columns: set[str] = set()
    non_bearing: list[dict[str, Any]] = []
    unresolved_anchor_refs: list[dict[str, Any]] = []
    blocks_by_entry: dict[str, dict[str, list[dict[str, Any]]]] = {}
    derivation_conflicts: list[str] = []

    def put(cell: dict[str, Any]) -> None:
        key = (cell["row"], cell["column_class"], cell["column"])
        existing = cells.get(key)
        if existing is None:
            cells[key] = cell
            return
        if (
            existing["relation"] != cell["relation"]
            or existing["rule"] != cell["rule"]
        ):
            derivation_conflicts.append(
                f"conflicting derivations for ({cell['row']} x "
                f"{cell['column']}): {existing['rule']}/"
                f"{existing['relation']} vs {cell['rule']}/"
                f"{cell['relation']}"
            )
            return
        for citation in cell["citations"]:
            if citation not in existing["citations"]:
                existing["citations"].append(citation)

    for entry in claims:
        eid = entry["id"]
        sor = _source_record(registers, entry, "source_of_record")

        # R1 — evidence instances (extracted population).
        if entry.get("population") == "extracted" and sor is not None:
            for instance in sor.get("evidence_instances") or []:
                if not isinstance(instance, dict):
                    continue
                doc = instance.get("source_document_id")
                inst_id = instance.get("claim_id")
                if not doc:
                    continue
                document_columns.add(str(doc))
                put(
                    {
                        "row": eid,
                        "column": str(doc),
                        "column_class": "documents",
                        "relation": "supports",
                        "rule": "R1",
                        "citations": [eid, str(inst_id)] if inst_id else [eid],
                    }
                )

        # R2 — bundle evidence direction (bundle population).
        if entry.get("population") == "bundle" and sor is not None:
            by_ref: dict[str, dict[str, Any]] = {}
            for item in sor.get("evidence") or []:
                if not isinstance(item, dict) or not item.get("ref"):
                    continue
                ref = str(item["ref"])
                relation = DIRECTION_RELATIONS.get(str(item.get("direction")))
                if relation is None:
                    derivation_conflicts.append(
                        f"{eid}: evidence item {ref} carries "
                        f"unregistered direction {item.get('direction')!r}"
                    )
                    continue
                document_columns.add(ref)
                cell = by_ref.get(ref)
                if cell is None:
                    by_ref[ref] = {
                        "row": eid,
                        "column": ref,
                        "column_class": "documents",
                        "relation": relation,
                        "rule": "R2",
                        "citations": [eid, ref],
                    }
                elif cell["relation"] != relation:
                    derivation_conflicts.append(
                        f"{eid}: conflicting stored directions for "
                        f"evidence ref {ref}"
                    )
            for cell in by_ref.values():
                put(cell)

        # R3 — study outcomes (any population).
        blocks_by_spec = _outcome_blocks(registers, entry)
        blocks_by_entry[eid] = blocks_by_spec
        for spec in sorted(blocks_by_spec):
            study_columns.add(spec)
            blocks = blocks_by_spec[spec]
            ordered = sorted(
                blocks, key=lambda b: (str(b["date"] or ""), b["pointer"])
            )
            governing = ordered[-1]
            relation = BEARING_OUTCOMES.get(governing["outcome"])
            if relation is not None:
                put(
                    {
                        "row": eid,
                        "column": spec,
                        "column_class": "studies",
                        "relation": relation,
                        "rule": "R3",
                        "citations": [eid] + [b["pointer"] for b in ordered],
                    }
                )
                for block in ordered[:-1]:
                    non_bearing.append(
                        {
                            "row": eid,
                            "study": spec,
                            "outcome": block["outcome"],
                            "date": block["date"],
                            "pointer": block["pointer"],
                            "reason": (
                                "superseded by a later outcome block "
                                "from the same study"
                            ),
                        }
                    )
            else:
                for block in ordered:
                    non_bearing.append(
                        {
                            "row": eid,
                            "study": spec,
                            "outcome": block["outcome"],
                            "date": block["date"],
                            "pointer": block["pointer"],
                            "reason": (
                                "governing outcome is non-bearing"
                                if block is governing
                                else "superseded by a later outcome "
                                "block from the same study"
                            ),
                        }
                    )

        # R4 — anchor assignment (constrains).
        for sign_ref in entry.get("sign_refs") or []:
            frame, _, value = str(sign_ref).partition(":")
            anchor_key = f"M{value}" if frame == "mahadevan" else None
            anchor = anchors.get(anchor_key) if anchor_key else None
            if anchor is not None and anchor.get("reading"):
                put(
                    {
                        "row": eid,
                        "column": anchor_key,
                        "column_class": "anchors",
                        "relation": "constrains",
                        "rule": "R4",
                        "citations": [eid, anchor_key],
                    }
                )
            else:
                if frame != "mahadevan":
                    reason = (
                        f"frame {frame!r} has no anchor-register "
                        "mapping in matrix-defs v1"
                    )
                elif anchor is None:
                    reason = "no anchor record under this key"
                else:
                    reason = "anchor record carries no recorded reading"
                unresolved_anchor_refs.append(
                    {"row": eid, "sign_ref": str(sign_ref), "reason": reason}
                )

    # R5 — research-check verdicts (verdict table empty in v1).
    research_check_columns: set[str] = set()
    for annotation in annotations:
        sidecar = (annotation.get("sidecar") or {}).get("path")
        if not sidecar:
            continue
        research_check_columns.add(str(sidecar))
        verdict = (annotation.get("bearing") or {}).get("verdict")
        relation = VERDICT_RELATIONS.get(verdict) if verdict else None
        target = annotation.get("canonical_claim_id")
        if relation is not None and target in claim_ids:
            put(
                {
                    "row": str(target),
                    "column": str(sidecar),
                    "column_class": "research_checks",
                    "relation": relation,
                    "rule": "R5",
                    "citations": [str(target), annotation["id"]],
                }
            )

    # R6 — settling instruments: register empty in v1.

    cell_list = sorted(
        cells.values(), key=lambda c: (c["row"], c["column_class"], c["column"])
    )
    rows_with_cells = {c["row"] for c in cell_list}
    columns_by_class: dict[str, list[str]] = {
        "studies": sorted(study_columns),
        "documents": sorted(document_columns),
        "research_checks": sorted(research_check_columns),
        "anchors": sorted(anchors.keys()),
        "corpus_texts": [],
    }
    borne = {(c["column_class"], c["column"]) for c in cell_list}
    unused_columns = {
        cls: [c for c in cols if (cls, c) not in borne]
        for cls, cols in columns_by_class.items()
    }
    falsifier_by_population: dict[str, dict[str, int]] = {}
    for entry in claims:
        bucket = falsifier_by_population.setdefault(
            str(entry.get("population")), {"covered": 0, "total": 0}
        )
        bucket["total"] += 1
        if entry.get("falsifier"):
            bucket["covered"] += 1
    falsifier_coverage = {
        "covered": sum(b["covered"] for b in falsifier_by_population.values()),
        "total": len(claims),
        "by_population": falsifier_by_population,
    }
    unresolved_mentions: list[dict[str, Any]] = []
    seen_store_records: set[tuple[str, str]] = set()
    for entry in claims:
        if entry.get("population") != "extracted":
            continue
        for source in entry.get("sources", []):
            for record in registers.records(source["path"]):
                marker = (source["path"], str(record.get("claim_id")))
                if marker in seen_store_records:
                    continue
                seen_store_records.add(marker)
                for mention in record.get("signs_involved") or []:
                    unresolved_mentions.append(
                        {
                            "record": str(record.get("claim_id")),
                            "source": source["path"],
                            "mention": str(mention),
                        }
                    )
    unresolved_mentions.sort(key=lambda m: (m["record"], m["mention"]))
    dependency_pairs: list[dict[str, str]] = []
    for entry in claims:
        spec_prefix = (
            entry["id"].rsplit("/", 1)[0] if "/" in entry["id"] else None
        )
        for ref in entry.get("evidence_refs") or []:
            target = None
            if ref in claim_ids:
                target = ref
            elif spec_prefix and f"{spec_prefix}/{ref}" in claim_ids:
                target = f"{spec_prefix}/{ref}"
            if target and target != entry["id"]:
                dependency_pairs.append({"from": entry["id"], "to": target})
    dependency_pairs.sort(key=lambda p: (p["from"], p["to"]))
    non_bearing.sort(
        key=lambda b: (b["row"], b["study"], str(b["date"] or ""), b["pointer"])
    )
    unresolved_anchor_refs.sort(key=lambda u: (u["row"], u["sign_ref"]))

    coverage = {
        "rows_total": len(claims),
        "rows_with_cells": len(rows_with_cells),
        "empty_rows": [e["id"] for e in claims if e["id"] not in rows_with_cells],
        "columns_by_class": {
            cls: len(cols) for cls, cols in columns_by_class.items()
        },
        "unused_columns": unused_columns,
        "cells_total": len(cell_list),
        "cells_by_relation": {
            rel: sum(1 for c in cell_list if c["relation"] == rel)
            for rel in RELATIONS
        },
        "cells_by_class": {
            cls: sum(1 for c in cell_list if c["column_class"] == cls)
            for cls in COLUMN_CLASSES
        },
        "falsifier_coverage": falsifier_coverage,
        "unresolved_sign_mentions": unresolved_mentions,
        "sign_refs_without_anchor_record": unresolved_anchor_refs,
        "study_outcome_blocks_not_bearing": non_bearing,
        "dependency_pairs_not_cells": dependency_pairs,
    }
    if derivation_conflicts:
        coverage["derivation_conflicts"] = sorted(set(derivation_conflicts))

    sign_block = _sign_sign_block(root) if with_sign_block else None

    ledger_bytes = (root / li.LEDGER_REL).read_bytes()
    as_of = {
        "ledger_sha256": li.canonical_sha256_bytes(ledger_bytes),
        "ledger_lines": len(entries),
        "ledger_date": max((str(e.get("date")) for e in entries), default=None),
        "ledger_schema": li.SCHEMA_VERSION,
        "matrix_defs": GATE_MATRIX_DEFS_VERSION,
    }
    return _Derivation(
        rows=[
            {
                "id": e["id"],
                "population": e.get("population"),
                "status": e.get("status"),
                "stage": e.get("stage"),
            }
            for e in claims
        ],
        columns=[
            {"id": column, "class": cls}
            for cls in COLUMN_CLASSES
            for column in columns_by_class[cls]
        ],
        cells=cell_list,
        coverage=coverage,
        as_of=as_of,
        sign_block=sign_block,
        registers=registers,
        blocks=blocks_by_entry,
    )


def _sign_sign_block(root: Path) -> dict[str, Any]:
    """The gate's own run of the registered co-occurrence
    pipeline over the corpus snapshot, with the gate's
    registered parameters (DEFINITIONS.md §8)."""
    corpus_path = root / CORPUS_REL
    corpus_hash = li.sha256_file(corpus_path)

    from glossa_lab.data import indus_corpus_v2
    from glossa_lab.pipelines.cooccurrence import build_cooccurrence_network

    status = indus_corpus_v2.corpus_status()
    tier = str(status.get("tier", ""))
    if not tier.startswith("real-corpus"):
        raise RuntimeError(
            f"corpus loader tier is {tier!r}, not the real corpus"
        )
    sequences = indus_corpus_v2.load_corpus()
    symbols = [f"sign-int:{n}" for seq in sequences for n in seq]
    network = build_cooccurrence_network(symbols, **COOCCURRENCE_PARAMS)
    return {
        "source": {
            "pipeline": COOCCURRENCE_PIPELINE,
            "parameters": dict(COOCCURRENCE_PARAMS),
            "parameter_note": (
                "window/min_freq/min_edge_weight as at the "
                "analyze_script.py §6 call site; remaining "
                "parameters at the pipeline's defaults, "
                "including its node selection and edge "
                "emission caps — the block is the pipeline "
                "output as emitted"
            ),
            "corpus": CORPUS_REL,
            "corpus_sha256": corpus_hash,
            "corpus_tier": tier,
            "sequences": len(sequences),
            "sign_tokens": len(symbols),
            "sign_id_form": (
                "sign-int:<n> — the corpus loader's integer sign "
                "ids, not relabeled with a frame name (the loader "
                "converts to Mahadevan integers where its "
                "crosswalk maps and otherwise preserves "
                "source-frame integers)"
            ),
        },
        "node_count": network["node_count"],
        "edge_count": network["edge_count"],
        "edges_emitted": len(network["edges"]),
        "community_count": network["community_count"],
        "nodes": network["nodes"],
        "edges": network["edges"],
        "communities": network["communities"],
    }


# ---------------------------------------------------------------------------
# V4 — relation-carrying citations (tie rules T1–T4 + the
# numeric arm)


def numeric_arm_check(
    relation: str, value: float, comparator: str, bound: Any
) -> Optional[str]:
    """The numeric arm (adoption 3, item 2): where a cited
    evidence entry carries a measurement and the citing claim
    carries a machine-readable bound, a supports citation
    whose value violates the bound is refused, and the
    symmetric opposes case. Returns a failure reason, or
    None when the citation carries its relation."""
    if comparator == "<=":
        satisfies = value <= bound
    elif comparator == ">=":
        satisfies = value >= bound
    elif comparator == "=":
        satisfies = value == bound
    elif comparator == "in":
        lo, hi = bound
        satisfies = lo <= value <= hi
    else:
        return f"unregistered numeric comparator {comparator!r}"
    if relation == "supports" and not satisfies:
        return (
            f"measurement value {value} violates the claim's bound "
            f"{comparator} {bound} — a supports citation the number "
            "does not carry"
        )
    if relation == "opposes" and satisfies:
        return (
            f"measurement value {value} satisfies the claim's bound "
            f"{comparator} {bound} — an opposes citation the number "
            "does not carry"
        )
    return None


def _measurement_shape(record: Any) -> Optional[dict[str, Any]]:
    """A record's machine-readable measurement value, in
    the registered shape {value, comparator, bound} — the
    cited evidence entry carries the value (and may carry
    the whole shape)."""
    if not isinstance(record, dict):
        return None
    m = record.get("measurement")
    if isinstance(m, dict) and "value" in m:
        return m
    return None


def _bound_shape(record: Any) -> Optional[dict[str, Any]]:
    """A record's machine-readable bound {comparator,
    bound} — the citing claim carries the bound; no value
    is required on this half of the shape."""
    if not isinstance(record, dict):
        return None
    m = record.get("measurement")
    if isinstance(m, dict) and "comparator" in m and "bound" in m:
        return m
    return None


_POINTER_RE = re.compile(r"^(?P<path>.+):(?P<claim>[^:#]+)#(?P<field>[^#]+)$")


class _TieContext:
    """Everything V4 reads: the ledger entries, the verified
    source registers, the anchors register, and each claim's
    stored outcome blocks."""

    def __init__(self, root: Path, entries: list[dict[str, Any]]):
        self.root = root
        self.entries = {e["id"]: e for e in entries}
        self.claims = {
            e["id"]: e for e in entries if e.get("kind") == "claim"
        }
        self.registers = _load_registers(root, entries)
        anchors_path = root / ANCHORS_REL
        self.anchors: dict[str, Any] = {}
        if anchors_path.is_file():
            self.anchors = json.loads(
                anchors_path.read_text(encoding="utf-8")
            ).get("anchors", {})
        self.blocks = {
            e["id"]: _outcome_blocks(self.registers, e)
            for e in entries
            if e.get("kind") == "claim"
        }
        self.numeric_exercised = 0

    def source_record(self, entry: dict[str, Any]) -> Optional[dict[str, Any]]:
        return _source_record(self.registers, entry, "source_of_record")

    def resolve_pointer(self, pointer: str) -> Optional[dict[str, Any]]:
        m = _POINTER_RE.match(pointer)
        if not m:
            return None
        record = self.registers.record(m.group("path"), m.group("claim"))
        if record is None:
            return None
        block = record.get(m.group("field"))
        if isinstance(block, dict) and "spec" in block and "outcome" in block:
            return {
                "spec": str(block["spec"]),
                "outcome": str(block["outcome"]),
                "date": block.get("date"),
                "pointer": pointer,
            }
        return None


def _tie_failures_for_cell(
    ctx: _TieContext, cell: dict[str, Any]
) -> list[str]:
    """V4 over one matrix cell. Every citation after the
    entry id must carry the cell's relation under a
    registered tie; the entry id itself is T1 (the claim
    itself)."""
    row = cell["row"]
    relation = cell["relation"]
    rule = cell.get("rule")
    column = cell["column"]
    entry = ctx.claims.get(row)
    if entry is None:
        return [f"row {row!r} is not a ledger claim entry"]
    citations = cell.get("citations") or []
    if not citations or citations[0] != row:
        return [
            f"citation list does not open with the ledger entry id "
            f"{row!r} (got {citations[:1]})"
        ]
    sor = ctx.source_record(entry)
    failures: list[str] = []
    extras = citations[1:]

    if rule == "R1":
        instances = (sor or {}).get("evidence_instances") or []
        for citation in extras:
            tied = any(
                isinstance(inst, dict)
                and inst.get("source_document_id") == column
                and inst.get("claim_id") == citation
                for inst in instances
            )
            if not tied:
                failures.append(
                    f"citation {citation!r} is not an evidence "
                    f"instance of the claim naming document "
                    f"{column!r} (T1: no stored membership)"
                )
        if not extras:
            tied = any(
                isinstance(inst, dict)
                and inst.get("source_document_id") == column
                and not inst.get("claim_id")
                for inst in instances
            )
            if not tied:
                failures.append(
                    "R1 cell cites no instance and no stored "
                    "instance without a claim id names the column (T1)"
                )
    elif rule == "R2":
        items = (sor or {}).get("evidence") or []
        for citation in extras:
            tied = any(
                isinstance(item, dict)
                and str(item.get("ref")) == citation
                and DIRECTION_RELATIONS.get(str(item.get("direction")))
                == relation
                for item in items
            )
            if not tied:
                failures.append(
                    f"citation {citation!r}: no stored evidence "
                    f"item with this ref carries direction "
                    f"{relation!r} (T1: stored direction governs)"
                )
    elif rule == "R3":
        failures.extend(_tie_failures_study(ctx, row, column, relation, extras))
    elif rule == "R4":
        for citation in extras:
            anchor = ctx.anchors.get(citation)
            sign_ref = (
                f"mahadevan:{citation[1:]}"
                if citation.startswith("M")
                else None
            )
            tied = (
                anchor is not None
                and bool(anchor.get("reading"))
                and sign_ref in (entry.get("sign_refs") or [])
                and citation == column
            )
            if not tied:
                failures.append(
                    f"citation {citation!r}: no registered anchor "
                    "record whose frame-qualified sign intersects "
                    "the claim's sign_refs with a recorded reading "
                    "(T3)"
                )
    elif rule == "R5":
        failures.append(
            "R5 cell exists but the v1 verdict table is empty — "
            "no research-check verdict can carry a relation in v1"
        )
    elif rule == "R6":
        failures.append(
            "R6 cell exists but the settling-instrument register "
            "is empty in matrix-defs v1 (T4: no registered "
            "instrument record)"
        )
    else:
        failures.append(f"unregistered derivation rule {rule!r}")

    failures.extend(_numeric_arm_failures(ctx, entry, relation, extras))
    return failures


def _tie_failures_study(
    ctx: _TieContext,
    row: str,
    study: str,
    relation: str,
    pointers: list[str],
) -> list[str]:
    """T2, the dated-test tie — the Atlas failure mode's
    home. A study citation ties only if the study's
    governing stored outcome block for the claim is among
    the cited pointers and its recorded outcome maps to the
    asserted relation under the outcome table. An unexecuted
    or null outcome carries neither relation."""
    failures: list[str] = []
    stored = ctx.blocks.get(row, {}).get(study, [])
    if not stored:
        return [
            f"no stored outcome record names study {study!r} for "
            "this claim (T2: the study did not test the claim "
            "in the record)"
        ]
    governing = _governing(stored)
    cited_blocks = []
    for pointer in pointers:
        block = ctx.resolve_pointer(pointer)
        if block is None or block["spec"] != study:
            failures.append(
                f"citation {pointer!r} does not resolve to a "
                f"stored outcome block of study {study!r} for "
                "this claim (T2)"
            )
        else:
            cited_blocks.append(block)
    if failures:
        return failures
    if governing["pointer"] not in pointers:
        cited_desc = "; ".join(
            f"{b['outcome']} ({b['date']})" for b in cited_blocks
        )
        failures.append(
            f"the cited outcome block(s) [{cited_desc}] do not "
            f"include the study's governing block "
            f"({governing['outcome']}, {governing['date']}) — a "
            "superseded or non-bearing outcome carries no "
            "relation (T2). This is the named Atlas failure "
            "mode: a citation can exist, be relevant, and still "
            "not carry the relation"
        )
        return failures
    mapped = BEARING_OUTCOMES.get(governing["outcome"])
    if mapped != relation:
        failures.append(
            f"governing outcome {governing['outcome']!r} "
            f"({governing['date']}) maps to "
            f"{mapped or 'no relation (non-bearing)'} under the "
            f"outcome table, not {relation!r} (T2)"
        )
    return failures


def _numeric_arm_failures(
    ctx: _TieContext,
    entry: dict[str, Any],
    relation: str,
    citations: list[str],
) -> list[str]:
    """The numeric arm over a citation set: fires only where
    a cited record carries a measurement value and a
    machine-readable bound is carried on the cited record or
    the citing claim (registered shape {value, comparator,
    bound}). Counts exercises so the gate can state whether
    the live population exercised the arm."""
    failures: list[str] = []
    claim_shape = _bound_shape(entry) or _measurement_shape(entry)
    for citation in citations:
        cited_record: Any = None
        if citation in ctx.entries:
            cited_record = ctx.entries[citation]
        else:
            m = _POINTER_RE.match(citation)
            if m:
                cited_record = ctx.registers.record(
                    m.group("path"), m.group("claim")
                )
        cited_shape = _measurement_shape(cited_record)
        value = None
        comparator = None
        bound = None
        if cited_shape is not None:
            value = cited_shape.get("value")
            comparator = cited_shape.get("comparator")
            bound = cited_shape.get("bound")
        if value is None and isinstance(cited_record, dict) \
                and cited_record.get("kind") == "measurement":
            value = cited_record.get("value")
        if comparator is None and claim_shape is not None:
            comparator = claim_shape.get("comparator")
            bound = claim_shape.get("bound")
        if value is None or comparator is None or bound is None:
            continue
        ctx.numeric_exercised += 1
        reason = numeric_arm_check(relation, value, comparator, bound)
        if reason:
            failures.append(f"numeric arm: {reason}")
    return failures


def _tie_failures_for_edge(
    ctx: _TieContext, edge: dict[str, Any]
) -> list[str]:
    """V4 over one candidate-map edge {from, to, rel,
    citations}: the same tie rules as for matrix cells,
    resolved by citation kind (the map's edges are authored
    downstream, so no derivation rule vouches for them —
    each citation must tie on its own)."""
    claim_id = edge.get("to")
    relation = edge.get("rel")
    entry = ctx.claims.get(claim_id)
    label = f"edge {edge.get('from')!r} -> {claim_id!r} ({relation})"
    if entry is None:
        return [f"{label}: target is not a ledger claim entry"]
    if relation not in RELATIONS:
        return [f"{label}: unregistered relation {relation!r}"]
    citations = edge.get("citations") or []
    body = [c for c in citations if c != claim_id]
    failures: list[str] = []
    sor = ctx.source_record(entry)
    for citation in body:
        tied = False
        reasons: list[str] = []
        # T2 — a stored outcome-block pointer.
        block = ctx.resolve_pointer(citation)
        if block is not None:
            sub = _tie_failures_study(
                ctx, claim_id, block["spec"], relation, [citation]
            )
            if not sub:
                tied = True
            else:
                reasons.extend(sub)
        # T1 — an evidence instance claim id (supports).
        if not tied and sor is not None:
            instances = sor.get("evidence_instances") or []
            if any(
                isinstance(inst, dict)
                and inst.get("claim_id") == citation
                for inst in instances
            ):
                if relation == "supports":
                    tied = True
                else:
                    reasons.append(
                        "an evidence instance stands behind the "
                        "claim; it carries supports, not "
                        f"{relation!r} (T1)"
                    )
            # T1 — a bundle evidence ref with stored direction.
            items = sor.get("evidence") or []
            if any(
                isinstance(item, dict)
                and str(item.get("ref")) == citation
                and DIRECTION_RELATIONS.get(str(item.get("direction")))
                == relation
                for item in items
            ):
                tied = True
        # T3 — a registered anchor key.
        if not tied and citation in ctx.anchors:
            anchor = ctx.anchors[citation]
            sign_ref = (
                f"mahadevan:{citation[1:]}"
                if citation.startswith("M")
                else None
            )
            if (
                anchor.get("reading")
                and sign_ref in (entry.get("sign_refs") or [])
                and relation == "constrains"
            ):
                tied = True
            else:
                reasons.append(
                    "anchor record does not tie: the sign does "
                    "not intersect the claim's sign_refs, or "
                    "carries no reading, or the relation is not "
                    "constrains (T3)"
                )
        if not tied:
            detail = "; ".join(reasons) if reasons else (
                "the cited record is not named in the claim's "
                "stored relation fields, is not a governing "
                "study outcome, and is not a registered anchor "
                "or instrument (T1–T4). Existence and topical "
                "relevance are not ties"
            )
            failures.append(
                f"{label}: citation {citation!r} carries no "
                f"tie: {detail}"
            )
    failures.extend(
        f"{label}: {f}"
        for f in _numeric_arm_failures(ctx, entry, relation, body)
    )
    return failures


# ---------------------------------------------------------------------------
# V6 — anchor shares


def _anchor_shares(root: Path) -> dict[str, Any]:
    """Recompute the strict set and shares from the
    canonical anchors file under the rule version recorded
    in the file itself, with the Phase-108 provenance
    register the rule reads."""
    anchors_data = json.loads((root / ANCHORS_REL).read_text(encoding="utf-8"))
    anchors = anchors_data.get("anchors", {})
    annotation = (
        anchors_data.get("metadata", {}).get(
            "spec029_phase_h_annotation", {}
        )
    )
    rule = annotation.get("strict_set_rule", {})
    register_data = json.loads(
        (root / PROVENANCE_REGISTER_REL).read_text(encoding="utf-8")
    )
    records = register_data.get("records", register_data)
    if not isinstance(records, dict):
        records = {}
    recomputed: set[str] = set()
    for sign, record in anchors.items():
        if (record.get("confidence") or "").upper() not in STRICT_CONFIDENCES:
            continue
        reg = records.get(sign)
        if reg is None:
            continue
        if reg.get("category") in SA_LINEAGE_CATEGORIES:
            continue
        if reg.get("sa_in_chain"):
            continue
        recomputed.add(sign)
    stored = {s for s, r in anchors.items() if r.get("strict_set")}
    total = len(anchors)
    return {
        "total": total,
        "recomputed_strict": recomputed,
        "stored_strict": stored,
        "recorded_rule_id": rule.get("rule_id"),
        "recorded_rule_version": rule.get("rule_version"),
        "recorded_strict_count": rule.get("strict_count"),
        "vocabulary": annotation.get("validation_status_vocabulary", []),
        "validation_statuses": {
            r.get("validation_status") for r in anchors.values()
        },
        "strict_share": (len(recomputed) / total) if total else 0.0,
    }


# ---------------------------------------------------------------------------
# V8 — settling canonicals under the gate's own
# glossa-settle-1 route, and the settling layer's
# scenario/verdict separation check.


def _settle_identity(ref: Any) -> Optional[tuple[str, int]]:
    frame, sep, value = str(ref).partition(":")
    if not sep or not frame:
        return None
    try:
        return (frame, int(value))
    except ValueError:
        return None


def _settle_anchor_key(identity: tuple[str, int]) -> Optional[str]:
    prefix = SETTLE_FRAME_PREFIXES.get(identity[0])
    if prefix is None:
        return None
    return f"{prefix}{identity[1]:03d}"


def _settle_falsifier_count(entry: dict[str, Any]) -> int:
    falsifier = entry.get("falsifier")
    if isinstance(falsifier, list):
        return sum(1 for f in falsifier if isinstance(f, str) and f)
    if isinstance(falsifier, str) and falsifier:
        return 1
    return 0


def _gate_settle(
    claims: list[dict[str, Any]],
    registers: _GateRegisters,
    anchors: dict[str, Any],
    strict_set: set[str],
    candidate: dict[str, Any],
    scope: list[Any],
) -> dict[str, Any]:
    """The gate's own S-R1…S-R4 evaluation of one candidate
    over one scope (glossa-settle-1, the gate's registered
    copies above). Independent of the engine's route: the
    same registered rules, separately implemented."""
    by_identity: dict[tuple[str, int], str] = {}
    for item in candidate.get("assignments") or []:
        identity = _settle_identity(item.get("sign"))
        if identity is not None:
            by_identity[identity] = str(item.get("value"))
    scope_pairs: list[tuple[str, tuple[str, int]]] = []
    for ref in scope:
        identity = _settle_identity(ref)
        if identity is not None:
            scope_pairs.append((str(ref), identity))

    assigned = [
        {"sign": sign_str, "value": by_identity[identity]}
        for sign_str, identity in scope_pairs
        if identity in by_identity
    ]
    assigned_ids = set(by_identity) & {
        identity for _, identity in scope_pairs
    }

    contexts: list[dict[str, Any]] = []
    uncontexted: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    n_strict = 0
    n_consistent = 0
    n_non_strict = 0
    for item in assigned:
        identity = _settle_identity(item["sign"])
        key = _settle_anchor_key(identity) if identity else None
        record = anchors.get(key) if key else None
        if record is None:
            uncontexted.append(
                {"sign": item["sign"], "value": item["value"]}
            )
            continue
        is_strict = key in strict_set
        reading = record.get("reading")
        if is_strict:
            n_strict += 1
            if item["value"] == reading:
                outcome = "consistent"
                n_consistent += 1
            else:
                outcome = "conflict"
                conflicts.append(
                    {
                        "sign": item["sign"],
                        "anchor": key,
                        "assigned_value": item["value"],
                        "anchor_reading": reading,
                    }
                )
        else:
            outcome = "non_strict"
            n_non_strict += 1
        contexts.append(
            {
                "sign": item["sign"],
                "anchor": key,
                "assigned_value": item["value"],
                "anchor_reading": reading,
                "confidence": record.get("confidence"),
                "strict": is_strict,
                "result": outcome,
            }
        )

    touched: list[dict[str, Any]] = []
    for entry in claims:
        refs = entry.get("sign_refs") or []
        via = [r for r in refs if _settle_identity(r) in assigned_ids]
        if not via:
            continue
        tallies = {key: 0 for key in SETTLE_TALLY_KEYS}
        for blocks in _outcome_blocks(registers, entry).values():
            relation = SETTLE_BEARING_OUTCOMES.get(
                _governing(blocks)["outcome"]
            )
            if relation:
                tallies[relation] += 1
        touched.append(
            {
                "claim": entry["id"],
                "via_signs": via,
                "tallies": tallies,
                "falsifiers_present": _settle_falsifier_count(entry),
                "falsifiers_evaluable": 0,
            }
        )

    forced: list[dict[str, Any]] = []
    for sign_str, identity in scope_pairs:
        if identity in assigned_ids:
            continue
        key = _settle_anchor_key(identity)
        if key and key in strict_set and key in anchors:
            forced.append(
                {"sign": sign_str, "value": anchors[key].get("reading")}
            )

    return {
        "scope": [sign_str for sign_str, _ in scope_pairs],
        "scope_signs": len(scope_pairs),
        "assigned": assigned,
        "assigned_count": len(assigned),
        "assigned_share": (
            len(assigned) / len(scope_pairs) if scope_pairs else None
        ),
        "uncontexted_assignments": uncontexted,
        "contexts": contexts,
        "contexts_touched": len(contexts),
        "strict_contexts": n_strict,
        "consistent": n_consistent,
        "non_strict_contexts": n_non_strict,
        "conflicts": conflicts,
        "strict_agreement_share": (
            n_consistent / n_strict if n_strict else None
        ),
        "contexted_share": (
            len(contexts) / len(assigned) if assigned else None
        ),
        "claims_touched": touched,
        "claims_touched_count": len(touched),
        "s_r3": {"class_table": None, "violations": []},
        "forced": forced,
    }


def _gate_compare(
    candidate_a: str,
    result_a: dict[str, Any],
    candidate_b: str,
    result_b: dict[str, Any],
) -> dict[str, Any]:
    """The gate's own dual-run comparison over two settled
    result blocks (semantics §7): tallies over every claim
    either run touches, divergences named, coverage deltas,
    signs assigned by one only, and the expectations
    absence statement in its mechanically derivable form."""
    side_a = candidate_a.replace("-", "_")
    side_b = candidate_b.replace("-", "_")
    tallies_a = {t["claim"]: t["tallies"] for t in result_a["claims_touched"]}
    tallies_b = {t["claim"]: t["tallies"] for t in result_b["claims_touched"]}
    zero = {key: 0 for key in SETTLE_TALLY_KEYS}
    order: list[str] = []
    for claim_id in list(tallies_a) + list(tallies_b):
        if claim_id not in order:
            order.append(claim_id)
    compared: list[dict[str, Any]] = []
    divergences: list[dict[str, Any]] = []
    for claim_id in order:
        ta = tallies_a.get(claim_id, dict(zero))
        tb = tallies_b.get(claim_id, dict(zero))
        compared.append(
            {
                "claim": claim_id,
                f"{side_a}_tallies": ta,
                f"{side_b}_tallies": tb,
                "divergent": ta != tb,
            }
        )
        if ta != tb:
            divergences.append(
                {
                    "claim": claim_id,
                    f"{side_a}_tallies": ta,
                    f"{side_b}_tallies": tb,
                }
            )

    def delta(value_a: Any, value_b: Any) -> dict[str, Any]:
        return {side_a: value_a, side_b: value_b}

    assigned_a = [item["sign"] for item in result_a["assigned"]]
    assigned_b = [item["sign"] for item in result_b["assigned"]]
    ids_a = {_settle_identity(s) for s in assigned_a}
    ids_b = {_settle_identity(s) for s in assigned_b}
    if len(order) == 1:
        note = (
            "No pre-registered expectation exists in the "
            "program's record for the one touched claim."
        )
    elif order:
        note = (
            "No pre-registered expectation exists in the "
            f"program's record for the {len(order)} touched "
            "claims."
        )
    else:
        note = (
            "No pre-registered expectation exists in the "
            "program's record for a touched claim; neither "
            "run touches a claim."
        )
    return {
        "claims_compared": compared,
        "per_claim_divergences": divergences,
        "coverage_deltas": {
            "assigned_count": delta(
                result_a["assigned_count"], result_b["assigned_count"]
            ),
            "contexts_touched": delta(
                result_a["contexts_touched"], result_b["contexts_touched"]
            ),
            "strict_contexts": delta(
                result_a["strict_contexts"], result_b["strict_contexts"]
            ),
            "consistent": delta(
                result_a["consistent"], result_b["consistent"]
            ),
            "conflicts": delta(
                len(result_a["conflicts"]), len(result_b["conflicts"])
            ),
            "forced_count": delta(
                len(result_a["forced"]), len(result_b["forced"])
            ),
        },
        "signs_assigned_by_one_only": {
            f"{side_b}_only": [
                s for s in assigned_b if _settle_identity(s) not in ids_a
            ],
            f"{side_a}_only": [
                s for s in assigned_a if _settle_identity(s) not in ids_b
            ],
        },
        "pre_registered_expectations": [],
        "pre_registered_expectations_note": note,
    }


def _map_matrix_key(ref: Any) -> Optional[str]:
    """matrix-defs v1 R4's key construction (map-defs v1
    §7): the frame prefix + the number as written in the
    sign_ref — no zero-padding."""
    frame, sep, value = str(ref).partition(":")
    if not sep or frame not in SETTLE_FRAME_PREFIXES:
        return None
    return f"{SETTLE_FRAME_PREFIXES[frame]}{value}"


def _map_anchor_summary(
    anchors: dict[str, Any], strict_set: set[str], key: Optional[str]
) -> Optional[dict[str, Any]]:
    if key is None:
        return None
    record = anchors.get(key)
    if record is None:
        return None
    return {
        "key": key,
        "reading": record.get("reading"),
        "confidence": record.get("confidence"),
        "validation_status": record.get("validation_status"),
        "strict": key in strict_set,
    }


def _map_census_lines(expected_map: dict[str, Any]) -> list[str]:
    """The census rule (map-defs v1 §10): every map check
    class states the live instance count behind it; a class
    or named sub-population with zero live instances is
    reported UNPROVEN on the live population, never silently
    counted as passing."""
    elements = expected_map.get("elements", [])
    by_kind = Counter(e.get("kind") for e in elements)
    edges = expected_map.get("edges", [])
    by_rel = Counter(e.get("rel") for e in edges)
    lines = [
        f"census: {by_kind.get('claim', 0)} claim elements; "
        "column elements by class: "
        + ", ".join(
            f"{cls} {by_kind.get(cls, 0)}" for cls in COLUMN_CLASSES
        ),
        f"census: {len(edges)} map edges by relation: "
        + ", ".join(f"{rel} {by_rel.get(rel, 0)}" for rel in RELATIONS)
        + f"; {len(expected_map.get('claims', {}))} per-claim "
        "records; "
        f"{len((expected_map.get('settling') or {}).get('runs', []))} "
        "stored settling runs recomputed",
    ]
    for cls in COLUMN_CLASSES:
        if not by_kind.get(cls):
            lines.append(
                f"UNPROVEN on the live population: {cls} "
                "elements — 0 live instances (the class exists "
                "in the definitions and carries no columns "
                "in v1; its teeth are fixtures in the battery)"
            )
    if not by_rel.get("constrains"):
        lines.append(
            "UNPROVEN on the live population: constrains "
            "edges — 0 live instances (the relation class is "
            "empty in the generated matrix and the artifact "
            "says so; its teeth are fixtures in the battery)"
        )
    return lines


def _derive_map(
    root: Path,
    entries: list[dict[str, Any]],
    claims: list[dict[str, Any]],
    deriv: _Derivation,
    shares: dict[str, Any],
    ledger_sha: str,
) -> tuple[dict[str, Any], list[str]]:
    """The gate's own map recomputation (V5's full leg):
    the expected map artifact, built from the ledger by
    the gate's routes — its matrix derivation, its anchor
    shares, its settling route — under its registered
    map-defs v1 copies. Returns (expected, failures):
    failures names defects in the records of record
    themselves (a stored run record the gate's route does
    not reproduce, a pin that names another build), which
    fail V5 however faithfully the map copied them."""
    failures: list[str] = []
    coverage = deriv.coverage
    anchors_path = root / ANCHORS_REL
    anchors_raw = anchors_path.read_bytes()
    anchors = json.loads(anchors_raw.decode("utf-8")).get("anchors", {})
    anchors_raw_sha = hashlib.sha256(anchors_raw).hexdigest()
    strict_set = shares["recomputed_strict"]

    # -- header ---------------------------------------------------------------
    by_status = Counter(str(e.get("status")) for e in claims)
    bearing_groups: dict[tuple[str, str, str], dict[str, Any]] = {}
    for entry in claims:
        for spec, blocks in deriv.blocks.get(entry["id"], {}).items():
            governing = _governing(blocks)
            relation = BEARING_OUTCOMES.get(governing["outcome"])
            if relation is None or governing["date"] is None:
                continue
            key = (str(governing["date"]), spec, governing["outcome"])
            group = bearing_groups.setdefault(
                key,
                {
                    "date": str(governing["date"]),
                    "study": spec,
                    "outcome": governing["outcome"],
                    "relation": relation,
                    "claims": [],
                },
            )
            group["claims"].append(entry["id"])
    nearest = sorted(
        bearing_groups.values(), key=lambda g: (g["study"], g["outcome"])
    )
    nearest = sorted(nearest, key=lambda g: g["date"], reverse=True)[:3]
    for group in nearest:
        group["claims"] = sorted(group["claims"])
    pending = sum(
        1
        for r in anchors.values()
        if r.get("validation_status") == PENDING_VALIDATION_STATUS
    )

    matrix_path = root / MATRIX_REL_DIR / "matrix.json"
    as_of = {
        "ledger_sha256": ledger_sha,
        "ledger_lines": len(entries),
        "ledger_date": max(
            (str(e.get("date")) for e in entries), default=None
        ),
        "ledger_schema": li.SCHEMA_VERSION,
        "matrix_defs": GATE_MATRIX_DEFS_VERSION,
        "map_defs": GATE_MAP_DEFS_VERSION,
        "settle_semantics": SETTLE_SEMANTICS_VERSION,
        "matrix_sha256": li.sha256_file(matrix_path),
        "anchors_register_sha256_raw_bytes": anchors_raw_sha,
    }
    header = {
        "claims_total": len(claims),
        "claims_by_status": {k: by_status[k] for k in sorted(by_status)},
        "validated_anchor_share": shares["strict_share"],
        "strict_anchor_share": shares["strict_share"],
        "anchors_strict": len(strict_set),
        "anchors_total": shares["total"],
        "nearest_dated_items": nearest,
        "pending_validations": {
            "count": pending,
            "reason": PENDING_VALIDATIONS_REASON,
        },
        "as_of": as_of,
    }

    # -- elements + loads ------------------------------------------------------
    elements: list[dict[str, Any]] = [
        {
            "kind": "claim",
            "id": e["id"],
            "statement": e.get("statement"),
            "status": e.get("status"),
            "stage": e.get("stage"),
            "population": e.get("population"),
        }
        for e in claims
    ] + [
        {"kind": c["class"], "id": c["id"]} for c in deriv.columns
    ]
    loads: dict[str, dict[str, int]] = {
        row["id"]: {rel: 0 for rel in RELATIONS} for row in deriv.rows
    }
    cells_by_row: dict[str, list[dict[str, Any]]] = {}
    for cell in deriv.cells:
        if cell["row"] in loads:
            loads[cell["row"]][cell["relation"]] += 1
        cells_by_row.setdefault(cell["row"], []).append(cell)

    # -- edges (map-defs §5: citations that carry) -----------------------------
    edges: list[dict[str, Any]] = []
    for cell in deriv.cells:
        citations = list(cell.get("citations") or [])
        if cell.get("rule") == "R3":
            blocks = deriv.blocks.get(cell["row"], {}).get(
                cell["column"], []
            )
            if blocks:
                governing = _governing(blocks)
                citations = [
                    c
                    for c in citations
                    if c == cell["row"] or c == governing["pointer"]
                ]
        edges.append(
            {
                "from": cell["column"],
                "to": cell["row"],
                "rel": cell["relation"],
                "rule": cell.get("rule"),
                "column_class": cell["column_class"],
                "citations": citations,
            }
        )

    # -- the settling records, re-derived by the gate's own route ---------------
    sets_path = root / ASSIGNMENT_SETS_REL
    if not sets_path.is_file():
        raise FileNotFoundError(
            f"assignment sets of record not found: {ASSIGNMENT_SETS_REL}"
        )
    assignment_sets = json.loads(sets_path.read_text(encoding="utf-8"))
    as_of["assignment_sets_sha256"] = li.sha256_file(sets_path)
    register_pin = (assignment_sets.get("register") or {}).get(
        "sha256_raw_bytes"
    )
    if register_pin != anchors_raw_sha:
        failures.append(
            f"the assignment-sets record pins anchors register "
            f"{register_pin}, but the register on disk hashes "
            f"{anchors_raw_sha}"
        )
    sets_by_id = {
        s.get("id"): s for s in assignment_sets.get("sets", [])
    }
    out_of_frame = list(assignment_sets.get("out_of_frame_records") or [])
    in_frame = len(anchors) - len(out_of_frame)
    sets_summary = []
    for s in assignment_sets.get("sets", []):
        item = {
            "id": s.get("id"),
            "frame": s.get("frame"),
            "assignments": len(s.get("assignments") or []),
            "provenance": s.get("provenance"),
        }
        item["frame_scope"] = in_frame
        item["share"] = (
            item["assignments"] / in_frame if in_frame else None
        )
        sets_summary.append(item)

    runs_dir = root / RUNS_REL_DIR
    run_files = sorted(runs_dir.glob("*.json")) if runs_dir.is_dir() else []
    loaded_runs = []
    for run_path in run_files:
        record = json.loads(run_path.read_text(encoding="utf-8"))
        # The gate's own copy of the builder's enumeration
        # rule: the map carries scenario evaluation records.
        # Since Spec 089 the run store also holds
        # materialization records (no candidate/scenario)
        # and absence records (no result block) — store
        # records under the run definitions, not
        # settling evaluations, and never map-carried (Spec 089
        # Stage 5, both copies filtered in the same motion).
        if not (
            isinstance(record.get("candidate"), str)
            and isinstance(record.get("scenario"), str)
            and isinstance(record.get("result"), dict)
        ):
            continue
        loaded_runs.append((run_path, record))
    loaded_runs.sort(
        key=lambda pair: (
            0 if pair[1].get("candidate") == "incumbent" else 1,
            pair[0].stem,
        )
    )
    runs: list[dict[str, Any]] = []
    settled_results: list[tuple[str, dict[str, Any]]] = []
    touched_by_claim: dict[str, list[dict[str, Any]]] = {}
    for run_path, record in loaded_runs:
        pins = record.get("pins") or {}
        pin_sha = (pins.get("ledger") or {}).get("sha256")
        if pin_sha != ledger_sha:
            failures.append(
                f"run record {run_path.stem} is pinned to ledger "
                f"{pin_sha}, but the current ledger is "
                f"{ledger_sha} — it cannot be carried by the map"
            )
        candidate_id = record.get("candidate")
        candidate_set = sets_by_id.get(candidate_id)
        if candidate_set is None:
            failures.append(
                f"run record {run_path.stem} names candidate "
                f"{candidate_id!r}, which is not a set of record"
            )
            continue
        result = _gate_settle(
            claims,
            deriv.registers,
            anchors,
            strict_set,
            {"assignments": candidate_set.get("assignments") or []},
            record.get("scope") or [],
        )
        stored_result = record.get("result") or {}
        record_divs: list[str] = []
        _first_divergences(
            result, stored_result, f"run record {run_path.stem}",
            record_divs, limit=6,
        )
        failures.extend(
            f"the gate's settling route does not reproduce {d}"
            for d in record_divs
        )
        settled_results.append((str(candidate_id), result))
        run_summary = {
            "record": run_path.stem,
            "scenario": record.get("scenario"),
            "candidate": candidate_id,
            "semantics": record.get("semantics"),
            "pins": pins,
        }
        for field_name in MAP_RUN_RESULT_FIELDS:
            run_summary[field_name] = result.get(field_name)
        runs.append(run_summary)
        for touched in result.get("claims_touched") or []:
            touched_by_claim.setdefault(touched["claim"], []).append(
                {
                    "candidate": candidate_id,
                    "record": run_path.stem,
                    "via_signs": touched.get("via_signs"),
                    "tallies": touched.get("tallies"),
                    "falsifiers_present": touched.get(
                        "falsifiers_present"
                    ),
                    "falsifiers_evaluable": touched.get(
                        "falsifiers_evaluable"
                    ),
                }
            )

    comparison_path = root / COMPARISON_REL
    if not comparison_path.is_file():
        raise FileNotFoundError(
            f"comparison record not found: {COMPARISON_REL}"
        )
    comparison_record = json.loads(
        comparison_path.read_text(encoding="utf-8")
    )
    comp_pin_sha = (
        (comparison_record.get("pins") or {}).get("ledger") or {}
    ).get("sha256")
    if comp_pin_sha != ledger_sha:
        failures.append(
            f"the filed comparison record is pinned to ledger "
            f"{comp_pin_sha}, but the current ledger is {ledger_sha}"
        )
    if len(settled_results) == 2:
        computed_comparison = _gate_compare(
            settled_results[0][0],
            settled_results[0][1],
            settled_results[1][0],
            settled_results[1][1],
        )
    else:
        failures.append(
            f"the run store carries {len(settled_results)} "
            "reproducible runs, not the stored pair the "
            "comparison names"
        )
        computed_comparison = comparison_record.get("result")
    comparison = {
        "record": COMPARISON_REL,
        "sha256": li.sha256_file(comparison_path),
        "result": computed_comparison,
    }
    as_of["comparison_sha256"] = comparison["sha256"]
    divergent_by_claim = {
        row["claim"]: row.get("divergent")
        for row in (computed_comparison or {}).get(
            "claims_compared", []
        )
    }

    canonical_path = root / SETTLING_CANONICAL_REL
    canonical = json.loads(canonical_path.read_text(encoding="utf-8"))
    canonicals = {
        "record": SETTLING_CANONICAL_REL,
        "sha256": li.sha256_file(canonical_path),
        "scenarios": [
            {
                "id": s.get("id"),
                "title": s.get("title"),
                "expected": s.get("expected"),
            }
            for s in canonical.get("scenarios", [])
        ],
    }
    as_of["settling_canonical_sha256"] = canonicals["sha256"]

    # -- system view --------------------------------------------------------------
    frame = sets_summary[0]["frame"] if sets_summary else None
    hotspots = [
        {
            "row": c["row"],
            "column": c["column"],
            "column_class": c["column_class"],
            "rule": c.get("rule"),
            "relation": c["relation"],
        }
        for c in deriv.cells
        if c["relation"] == "opposes"
    ]
    by_stage = Counter(
        str(e.get("stage")) for e in claims if e.get("stage")
    )
    by_population = Counter(str(e.get("population")) for e in claims)
    system = {
        "sign_inventory": {
            "frame": frame,
            "register_records": len(anchors),
            "out_of_frame_records": out_of_frame,
            "out_of_frame_note": assignment_sets.get("out_of_frame_note"),
            "frame_scope": in_frame,
            "assignment_sets": sets_summary,
            "register": {
                "path": ANCHORS_REL,
                "sha256_raw_bytes": anchors_raw_sha,
            },
        },
        "matrix_coverage": {
            "rows_total": coverage.get("rows_total"),
            "rows_with_cells": coverage.get("rows_with_cells"),
            "empty_rows": coverage.get("empty_rows"),
            "columns_by_class": coverage.get("columns_by_class"),
            "unused_columns": coverage.get("unused_columns"),
            "cells_total": coverage.get("cells_total"),
            "cells_by_relation": coverage.get("cells_by_relation"),
            "cells_by_class": coverage.get("cells_by_class"),
            "conflict_hotspots": hotspots,
            "study_columns_without_cells": (
                (coverage.get("unused_columns") or {}).get("studies", [])
            ),
            "dependency_pairs_not_cells": len(
                coverage.get("dependency_pairs_not_cells") or []
            ),
        },
        "claim_population": {
            "by_status": {k: by_status[k] for k in sorted(by_status)},
            "by_stage": {k: by_stage[k] for k in sorted(by_stage)},
            "no_stage_recorded": sum(
                1 for e in claims if not e.get("stage")
            ),
            "by_population": {
                k: by_population[k] for k in sorted(by_population)
            },
        },
        "falsifier_census": {
            "covered": (coverage.get("falsifier_coverage") or {}).get(
                "covered"
            ),
            "total": (coverage.get("falsifier_coverage") or {}).get(
                "total"
            ),
            "by_population": (
                coverage.get("falsifier_coverage") or {}
            ).get("by_population"),
            "gap_claims": [
                e["id"] for e in claims if not e.get("falsifier")
            ],
        },
        "aee_state_census": {
            "with_state": sum(
                1 for e in claims if e.get("aee_state") is not None
            ),
            "without_state": sum(
                1 for e in claims if e.get("aee_state") is None
            ),
            "total": len(claims),
        },
        "unresolved": {
            "sign_mentions": coverage.get("unresolved_sign_mentions"),
            "sign_refs_without_anchor_record": coverage.get(
                "sign_refs_without_anchor_record"
            ),
        },
        "sign_sign_block_summary": {
            "node_count": (deriv.sign_block or {}).get("node_count"),
            "edge_count": (deriv.sign_block or {}).get("edge_count"),
            "edges_emitted": (deriv.sign_block or {}).get(
                "edges_emitted"
            ),
            "community_count": (deriv.sign_block or {}).get(
                "community_count"
            ),
            "corpus_sha256": (
                (deriv.sign_block or {}).get("source") or {}
            ).get("corpus_sha256"),
        },
    }

    # -- per-claim records ---------------------------------------------------------
    annotations = [e for e in entries if e.get("kind") == "annotation"]
    annotations_by_target: dict[str, list[dict[str, Any]]] = {}
    for annotation in annotations:
        target = annotation.get("target_claim_id")
        if target:
            annotations_by_target.setdefault(target, []).append(
                {
                    "id": annotation.get("id"),
                    "canonical_claim_id": annotation.get(
                        "canonical_claim_id"
                    ),
                    "sidecar": annotation.get("sidecar"),
                    "bearing": annotation.get("bearing"),
                }
            )
    columns_by_class = coverage.get("columns_by_class") or {}
    claim_records: dict[str, Any] = {}
    for entry in claims:
        eid = entry["id"]
        row_cells = cells_by_row.get(eid, [])
        touched = touched_by_claim.get(eid)
        bearing = None
        if touched:
            bearing = {
                "runs": touched,
                "divergent": divergent_by_claim.get(eid),
            }
        evaluable = (
            touched[0].get("falsifiers_evaluable") if touched else None
        )
        sign_records = []
        for ref in entry.get("sign_refs") or []:
            m_key = _map_matrix_key(ref)
            identity = _settle_identity(ref)
            s_key = _settle_anchor_key(identity) if identity else None
            matrix_record = _map_anchor_summary(
                anchors, strict_set, m_key
            )
            settle_record = _map_anchor_summary(
                anchors, strict_set, s_key
            )
            sign_records.append(
                {
                    "sign_ref": ref,
                    "matrix_key": m_key,
                    "matrix_record": matrix_record,
                    "settle_key": s_key,
                    "settle_record": settle_record,
                    "divergence": (matrix_record is None)
                    != (settle_record is None)
                    or (
                        matrix_record is not None
                        and settle_record is not None
                        and m_key != s_key
                    ),
                }
            )
        sor = next(
            (
                s
                for s in entry.get("sources", [])
                if s.get("role") == "source_of_record"
            ),
            None,
        )
        claim_records[eid] = {
            "id": eid,
            "statement": entry.get("statement"),
            "status": entry.get("status"),
            "stage": entry.get("stage"),
            "population": entry.get("population"),
            "author": entry.get("author"),
            "author_kind": entry.get("author_kind"),
            "as_of": entry.get("as_of"),
            "date": entry.get("date"),
            "falsifier": entry.get("falsifier"),
            "falsifier_counts": {
                "present": _settle_falsifier_count(entry),
                "evaluable": evaluable,
            },
            "does_not_establish": entry.get("does_not_establish"),
            "aee_state": entry.get("aee_state"),
            "displayed_score": (
                {"state": "recorded", "aee_state": entry.get("aee_state")}
                if entry.get("aee_state") is not None
                else {"state": "empty"}
            ),
            "sign_refs": entry.get("sign_refs") or [],
            "sources": entry.get("sources") or [],
            "matrix_row": {
                "cells": row_cells,
                "empty": not row_cells,
            },
            "settling_bearing": bearing,
            "annotations": annotations_by_target.get(eid, []),
            "evidence": {
                "column_summary": {
                    cls: {
                        "columns": columns_by_class.get(cls, 0),
                        "cells": sum(
                            1
                            for c in row_cells
                            if c["column_class"] == cls
                        ),
                    }
                    for cls in COLUMN_CLASSES
                },
                "source_document": sor,
                "sign_records": sign_records,
            },
        }

    settling = {
        "label": SETTLING_LABEL,
        "semantics": SETTLE_SEMANTICS_VERSION,
        "assignment_sets": {
            "record": ASSIGNMENT_SETS_REL,
            "sha256": as_of["assignment_sets_sha256"],
            "register": assignment_sets.get("register"),
            "sets": sets_summary,
            "out_of_frame_records": out_of_frame,
            "out_of_frame_note": assignment_sets.get("out_of_frame_note"),
        },
        "runs": runs,
        "comparison": comparison,
        "canonicals": canonicals,
        "reach": {
            "claims_with_sign_refs": sum(
                1 for e in claims if e.get("sign_refs")
            ),
            "claims_total": len(claims),
            "claims_untouched_by_any_run": len(claims)
            - len(touched_by_claim),
            "s_r3": {
                "status": "UNMEASURED",
                "class_table": None,
                "note": MAP_S_R3_NOTE,
            },
        },
    }

    expected = {
        "artifact": "glossa-indus layered map data",
        "generated_from": (
            f"{li.LEDGER_REL} through "
            f"{MATRIX_REL_DIR}/matrix.json and the "
            "settling records of record"
        ),
        "generated_by": (
            "tools/ledger/generate_map.py "
            "(backend/glossa_lab/map_generate.py)"
        ),
        "header": header,
        "elements": elements,
        "edges": edges,
        "loads": loads,
        "matrix": {
            "rows": deriv.rows,
            "columns": deriv.columns,
            "cells": deriv.cells,
            "coverage": coverage,
            "sign_sign_block": deriv.sign_block,
        },
        "system": system,
        "claims": claim_records,
        "settling": settling,
    }
    return expected, failures


def _v8_checks(
    root: Path,
    entries: list[dict[str, Any]],
    claims: list[dict[str, Any]],
) -> list[Check]:
    names = (
        "V8 settling canonicals — scenarios reproduce under "
        "the gate's own glossa-settle-1 route",
        "V8 settling canonicals — the registered comparison "
        "reproduces",
        "V8 scenario/verdict separation — the settling layer "
        "carries no reachable ledger write path",
    )
    canonical_path = root / SETTLING_CANONICAL_REL
    anchors_path = root / ANCHORS_REL
    register_path = root / PROVENANCE_REGISTER_REL
    corpus_path = root / CORPUS_REL
    absent = [
        rel
        for rel, path in (
            (SETTLING_CANONICAL_REL, canonical_path),
            (ANCHORS_REL, anchors_path),
            (PROVENANCE_REGISTER_REL, register_path),
            (CORPUS_REL, corpus_path),
        )
        if not path.is_file()
    ]
    if absent:
        return [
            Check(
                name,
                "NOT-RUN",
                [
                    "the settling layer is not present in this "
                    f"tree (absent: {', '.join(absent)}) — V8 "
                    "runs where the settling layer is present"
                ],
            )
            for name in names
        ]
    try:
        canonical = json.loads(
            canonical_path.read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        return [
            Check(
                names[0],
                "FAIL",
                [f"cannot parse {SETTLING_CANONICAL_REL}: {exc}"],
            ),
            Check(names[1], "NOT-RUN", ["the canonical artifact does not parse"]),
            Check(names[2], "NOT-RUN", ["the canonical artifact does not parse"]),
        ]

    # The provenance pins first: the canonicals govern one
    # pinned build; a tree they do not describe fails here,
    # naming the pin, before any scenario is settled.
    pin_failures: list[str] = []
    prov = canonical.get("provenance", {})
    ledger_pin = prov.get("ledger", {})
    ledger_path = root / li.LEDGER_REL
    actual_ledger_sha = (
        li.canonical_sha256_bytes(ledger_path.read_bytes())
        if ledger_path.is_file()
        else "MISSING"
    )
    if ledger_pin.get("sha256_canonical") != actual_ledger_sha:
        pin_failures.append(
            f"ledger pin: the canonicals were derived over "
            f"ledger sha256 {ledger_pin.get('sha256_canonical')}, "
            f"this tree's ledger hashes {actual_ledger_sha}"
        )
    if ledger_pin.get("lines") != len(entries):
        pin_failures.append(
            f"ledger pin: the canonicals record "
            f"{ledger_pin.get('lines')} ledger lines, this "
            f"tree carries {len(entries)}"
        )
    anchors_bytes = anchors_path.read_bytes()
    anchors_raw_sha = hashlib.sha256(anchors_bytes).hexdigest()
    anchors_pin = prov.get("anchors_register", {})
    if anchors_pin.get("sha256_raw_bytes") != anchors_raw_sha:
        pin_failures.append(
            "anchors register pin: the canonicals were "
            f"derived over register raw sha256 "
            f"{anchors_pin.get('sha256_raw_bytes')}, this "
            f"tree's register hashes {anchors_raw_sha}"
        )
    corpus_pin = prov.get("corpus_snapshot", {})
    if corpus_pin.get("sha256_canonical") != li.sha256_file(corpus_path):
        pin_failures.append(
            "corpus pin: the canonicals were derived over "
            f"corpus sha256 {corpus_pin.get('sha256_canonical')}, "
            f"this tree's corpus hashes "
            f"{li.sha256_file(corpus_path)}"
        )
    shares = _anchor_shares(root)
    if shares["recorded_rule_id"] != STRICT_RULE_ID:
        pin_failures.append(
            f"strict rule pin: the anchors file records rule "
            f"{shares['recorded_rule_id']!r}; glossa-settle-1 "
            f"is registered against {STRICT_RULE_ID!r}"
        )
    if shares["recomputed_strict"] != shares["stored_strict"]:
        pin_failures.append(
            "strict set: the recomputation disagrees with "
            "the stored strict_set flags — a settling run "
            "refuses over this register (semantics §1)"
        )
    if anchors_pin.get("strict") != len(shares["recomputed_strict"]):
        pin_failures.append(
            f"strict count pin: the canonicals record "
            f"{anchors_pin.get('strict')} strict anchors, "
            f"recomputed {len(shares['recomputed_strict'])}"
        )
    registers = _load_registers(root, entries)
    if registers.mismatches:
        pin_failures.append(
            "source records do not verify against the "
            "ledger's recorded hashes (the settling route "
            "reads outcome blocks from verified records "
            f"only): {registers.mismatches[:3]}"
        )
    if pin_failures:
        return [
            Check(names[0], "FAIL", pin_failures),
            Check(
                names[1],
                "NOT-RUN",
                ["the canonicals' pins do not hold over this tree"],
            ),
            *_v8_separation_checks(root, names[2]),
        ]

    anchors = json.loads(anchors_bytes.decode("utf-8")).get("anchors", {})
    strict_set = shares["recomputed_strict"]

    # (a) The scenarios, settled by the gate's own route.
    divergences: list[str] = []
    settled: dict[str, dict[str, Any]] = {}
    candidates: dict[str, str] = {}
    for scenario in canonical.get("scenarios", []):
        result = _gate_settle(
            claims,
            registers,
            anchors,
            strict_set,
            scenario["inputs"]["candidate"],
            scenario["inputs"]["scope"],
        )
        settled[scenario["id"]] = result
        candidates[scenario["id"]] = scenario["inputs"]["candidate"].get(
            "id", scenario["id"]
        )
        _first_divergences(
            result,
            scenario["expected"],
            f"scenario {scenario['id']}",
            divergences,
            limit=12,
        )
    scenario_check = Check(
        names[0],
        "FAIL" if divergences else "PASS",
        divergences
        or [
            f"{len(settled)} registered canonical scenarios "
            "reproduced exactly under the gate's own "
            "glossa-settle-1 route (S-R4 result blocks, "
            "field-for-field), over provenance pins that "
            "verify against this tree"
        ],
    )

    # (b) The registered comparison, compared by the gate's
    # own comparison. The expectations note is checked on
    # its mechanically derivable part (FINDING-S4-1).
    comparison_checks: list[Check] = []
    for comparison in canonical.get("comparisons", []):
        run_ids = comparison["inputs"]["runs"]
        if len(run_ids) != 2 or any(r not in settled for r in run_ids):
            comparison_checks.append(
                Check(
                    names[1],
                    "FAIL",
                    [
                        f"comparison {comparison['id']} names "
                        f"runs {run_ids}, which are not both "
                        "registered scenarios"
                    ],
                )
            )
            continue
        computed = _gate_compare(
            candidates[run_ids[0]],
            settled[run_ids[0]],
            candidates[run_ids[1]],
            settled[run_ids[1]],
        )
        expected = dict(comparison["expected"])
        registered_note = expected.pop(
            "pre_registered_expectations_note", None
        )
        gate_note = computed.pop("pre_registered_expectations_note")
        comp_divergences: list[str] = []
        _first_divergences(
            computed, expected, f"comparison {comparison['id']}",
            comp_divergences, limit=12,
        )
        note_ok = (
            registered_note is not None
            and gate_note == registered_note.split(";")[0] + "."
        )
        if comp_divergences or not note_ok:
            evidence = list(comp_divergences)
            if not note_ok:
                evidence.append(
                    "pre_registered_expectations_note: the "
                    "gate's absence clause does not match the "
                    "registered note's first clause"
                )
            comparison_checks.append(Check(names[1], "FAIL", evidence))
        else:
            comparison_checks.append(
                Check(
                    names[1],
                    "PASS",
                    [
                        f"comparison {comparison['id']} "
                        "reproduced exactly (claims compared, "
                        "per-claim divergences, coverage "
                        "deltas, signs assigned by one only, "
                        "expectations named); the expectations "
                        "note is checked on its mechanically "
                        "derivable part — the absence clause "
                        "matches verbatim; the registered "
                        "note's remainder is brief-specific "
                        "prose (FINDING-S4-1, stage record)"
                    ],
                )
            )
    if not comparison_checks:
        comparison_checks.append(
            Check(
                names[1],
                "FAIL",
                ["the canonical artifact registers no comparison"],
            )
        )

    return [scenario_check, *comparison_checks, *_v8_separation_checks(root, names[2])]


def _v8_separation_checks(root: Path, name: str) -> list[Check]:
    """The settling layer's separation arm: no settling or
    scenario module may import **or reach** a ledger write
    entry point. V9.2 audits imports; this arm extends the
    audit to reachability — an attribute use such as
    `li.append_entry(...)` or a bare name reference is a
    reachable write path even where the import itself names
    only the module (harmonization adoption 3, item 3: the
    computed layer and the verdict layer stay distinct by
    construction, not by import style)."""
    pkg_dir = root / "backend" / "glossa_lab"
    modules: list[Path] = []
    if pkg_dir.is_dir():
        modules = sorted(
            p
            for p in pkg_dir.rglob("*.py")
            if re.search(r"settling|scenario", p.name)
        )
    if not modules:
        return [
            Check(
                name,
                "FAIL",
                [
                    "the canonical artifact is present but no "
                    "settling/scenario module exists under "
                    "backend/glossa_lab — the layer the "
                    "canonicals govern is missing"
                ],
            )
        ]
    failures: list[str] = []
    for path in modules:
        rel = str(path.relative_to(root))
        tree = ast.parse(path.read_text(encoding="utf-8"))
        bad_imports = _imported_names(tree) & set(WRITE_ENTRY_POINTS)
        if bad_imports:
            failures.append(
                f"{rel} imports ledger write entry points "
                f"{sorted(bad_imports)}"
            )
        reached: set[str] = set()
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Attribute)
                and node.attr in WRITE_ENTRY_POINTS
            ):
                reached.add(node.attr)
            elif (
                isinstance(node, ast.Name)
                and node.id in WRITE_ENTRY_POINTS
            ):
                reached.add(node.id)
        if reached:
            failures.append(
                f"{rel} reaches ledger write entry points "
                f"{sorted(reached)} (attribute or name use — "
                "a reachable write path, not only an import)"
            )
    return [
        Check(
            name,
            "FAIL" if failures else "PASS",
            failures
            or [
                f"{len(modules)} settling/scenario module(s) "
                "scanned; none imports or reaches a ledger "
                f"write path ({', '.join(WRITE_ENTRY_POINTS)}) "
                "— the settling layer's outputs are computed "
                "records, never ledger verdicts"
            ],
        )
    ]


# ---------------------------------------------------------------------------
# V9 — no write path


def _imported_names(tree: ast.AST) -> set[str]:
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            for alias in node.names:
                names.add(alias.name)
                if alias.asname:
                    names.add(alias.asname)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
    return names


def _has_write_call(tree: ast.AST) -> bool:
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr in (
                "write_bytes",
                "write_text",
            ):
                return True
            if isinstance(func, ast.Name) and func.id == "open" and any(
                isinstance(a, ast.Constant)
                and isinstance(a.value, str)
                and ("w" in a.value or "a" in a.value)
                for a in node.args[1:]
            ):
                return True
            if (
                isinstance(func, ast.Attribute)
                and func.attr == "replace"
                and isinstance(func.value, ast.Name)
                and func.value.id == "os"
            ):
                return True
    return False


def _v9_checks(root: Path) -> list[Check]:
    checks: list[Check] = []

    # V9.1 — the gate's own import hygiene.
    gate_files = [
        Path(__file__),
        root / "tools" / "ledger" / "check_ledger_gate.py",
    ]
    hygiene_failures: list[str] = []
    for path in gate_files:
        if not path.is_file():
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        bad = _imported_names(tree) & set(WRITE_ENTRY_POINTS)
        if bad:
            hygiene_failures.append(
                f"{path.name} imports write entry points {sorted(bad)}"
            )
        if path == Path(__file__) and _has_write_call(tree):
            hygiene_failures.append(
                "ledger_gate.py contains a write call — the gate "
                "must never write"
            )
    checks.append(
        Check(
            "V9 no write path — gate import hygiene",
            "FAIL" if hygiene_failures else "PASS",
            hygiene_failures
            or [
                "the gate modules import no write entry point "
                f"({', '.join(WRITE_ENTRY_POINTS)}) and contain "
                "no write call"
            ],
        )
    )

    # V9.2 — settling/scenario package audit.
    pkg_dir = root / "backend" / "glossa_lab"
    settling_modules = []
    if pkg_dir.is_dir():
        settling_modules = sorted(
            p
            for p in pkg_dir.rglob("*.py")
            if re.search(r"settling|scenario", p.name)
        )
    audit_failures: list[str] = []
    for path in settling_modules:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        bad = _imported_names(tree) & set(WRITE_ENTRY_POINTS)
        if bad:
            audit_failures.append(
                f"{path.relative_to(root)} imports write entry "
                f"points {sorted(bad)}"
            )
    if settling_modules:
        evidence = audit_failures or [
            f"{len(settling_modules)} settling/scenario module(s) "
            "audited; none imports a ledger write path"
        ]
    else:
        evidence = [
            "no settling/scenario package exists yet (Stage 4); "
            "the audit is armed and scans for one on every run"
        ]
    checks.append(
        Check(
            "V9 no write path — settling/scenario import audit",
            "FAIL" if audit_failures else "PASS",
            evidence,
        )
    )

    # V9.3 — writer census over the repo's production python
    # sources (backend/glossa_lab, backend/scripts, tools).
    # Test code is out of the census: it writes fixtures
    # under tmp dirs by design and is not a publication path.
    writers_found: set[str] = set()
    readers: set[str] = set()
    for base in (
        root / "backend" / "glossa_lab",
        root / "backend" / "scripts",
        root / "tools",
    ):
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.py")):
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            if not any(p.search(text) for p in ARTIFACT_PATH_PATTERNS):
                continue
            rel = str(path.relative_to(root))
            if _has_write_call(ast.parse(text)):
                writers_found.add(rel)
            else:
                readers.add(rel)
    unregistered = writers_found - REGISTERED_WRITERS
    checks.append(
        Check(
            "V9 no write path — matrix/map writer census",
            "FAIL" if unregistered else "PASS",
            [
                f"writers of the gated artifacts: "
                f"{sorted(writers_found) or 'none found'}",
                f"readers (no write call): {len(readers)} module(s)",
                "census scope: backend/glossa_lab, "
                "backend/scripts, tools (test code writes "
                "fixtures under tmp dirs by design and is not "
                "a publication path)",
            ]
            + (
                [
                    f"UNREGISTERED WRITER: {w} — the generators, "
                    "the gated-publication path, and the "
                    "registered run machinery are the only "
                    "writers (V9)"
                    for w in sorted(unregistered)
                ]
                if unregistered
                else []
            ),
        )
    )
    return checks


# ---------------------------------------------------------------------------
# V10 — program-map equivalence (Spec 088 Stage 3). The
# gate's independent route to the program map: the ledger
# + taxonomy recomputed under the gate's registered
# program-map-defs v1 copies above, never imported from
# the builder. The builder and the gate agreeing is
# consistency; the defs' semantics were the owner's call
# at T003/T101 (C088-7's own limit). Stage 4 (T401) amends
# V10's artifact list to include the generated page
# (program-map.html), rendered by this route from the
# recomputed data under the gate's template copies —
# the amendment is recorded in the S4 stage record, per
# the defs discipline.


def _pm_key_paths(value: Any, trail: str = "$") -> list[str]:
    """Every mapping key in a parsed JSON value, with its
    path — the taxonomy format audit (§8)."""
    found: list[str] = []
    if isinstance(value, dict):
        for key, sub in value.items():
            found.append(f"{trail}.{key}")
            found.extend(_pm_key_paths(sub, f"{trail}.{key}"))
    elif isinstance(value, list):
        for i, sub in enumerate(value):
            found.extend(_pm_key_paths(sub, f"{trail}[{i}]"))
    return found


def _pm_taxonomy(
    root: Path,
) -> tuple[Optional[dict[str, Any]], list[str]]:
    """Parse and validate the taxonomy under the gate's
    own §8 rules. Returns (structure, failures); the
    structure is None when the file cannot be read at
    all."""
    path = root / PROGRAM_MAP_TAXONOMY_REL
    if not path.is_file():
        return None, [f"taxonomy not found: {path}"]
    try:
        tax = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, [f"taxonomy is not readable JSON: {exc}"]
    if not isinstance(tax, dict):
        return None, ["taxonomy is not a JSON object"]
    failures: list[str] = []
    for key_path in _pm_key_paths(tax):
        key = key_path.rsplit(".", 1)[-1].split("[")[0]
        if key in PM_FORBIDDEN_TAXONOMY_KEYS:
            failures.append(
                f"taxonomy carries the forbidden standing-"
                f"shaped key {key!r} at {key_path} (defs §8: "
                "the format carries no standings)"
            )
    if tax.get("version") != PROGRAM_MAP_TAXONOMY_VERSION:
        failures.append(
            f"taxonomy version is {tax.get('version')!r}, "
            f"the gate's registered copy is "
            f"{PROGRAM_MAP_TAXONOMY_VERSION!r}"
        )
    domains = tax.get("domains")
    if (
        not isinstance(domains, list)
        or not domains
        or len(set(domains)) != len(domains)
        or not all(isinstance(d, str) and d for d in domains)
    ):
        failures.append(
            "taxonomy 'domains' must be a non-empty list of "
            "unique names"
        )
        domains = []
    subdomains = tax.get("subdomains")
    if not isinstance(subdomains, dict) or set(subdomains) != set(domains):
        failures.append(
            "taxonomy 'subdomains' must declare exactly the "
            "domains"
        )
        subdomains = {}
    for domain in domains:
        subs = subdomains.get(domain)
        if (
            not isinstance(subs, list)
            or not subs
            or len(set(subs)) != len(subs)
            or not all(isinstance(s, str) and s for s in subs)
        ):
            failures.append(
                f"taxonomy subdomains for {domain!r} must be "
                "a non-empty list of unique names"
            )

    def _assignments(kind: str, id_key: str) -> dict[str, Any]:
        raw = tax.get(kind)
        if not isinstance(raw, list):
            failures.append(f"taxonomy {kind!r} must be a list")
            return {}
        out: dict[str, Any] = {}
        for entry in raw:
            if not isinstance(entry, dict) or set(entry) != {
                id_key,
                "domain",
                "subdomain",
            }:
                failures.append(
                    f"taxonomy {kind} entry must carry exactly "
                    f"{{{id_key}, domain, subdomain}}: {entry!r}"
                )
                continue
            ident = entry[id_key]
            if ident in out:
                failures.append(
                    f"taxonomy assigns {ident!r} more than "
                    f"once ({kind})"
                )
            if entry["domain"] not in domains:
                failures.append(
                    f"taxonomy assigns {ident!r} to the "
                    f"undeclared domain {entry['domain']!r}"
                )
            elif entry["subdomain"] not in subdomains.get(
                entry["domain"], ()
            ):
                failures.append(
                    f"taxonomy assigns {ident!r} to "
                    f"{entry['subdomain']!r}, not declared "
                    f"under {entry['domain']!r}"
                )
            out[ident] = entry
        return out

    studies = _assignments("studies", "spec_dir")
    documents = _assignments("extracted_documents", "document")
    restricted = tax.get("restricted")
    if not isinstance(restricted, list) or not all(
        isinstance(r, str) for r in restricted
    ):
        failures.append("taxonomy 'restricted' must be a list")
        restricted = []
    if len(set(restricted)) != len(restricted):
        failures.append("taxonomy 'restricted' has duplicates")
    for spec_dir in restricted:
        if spec_dir not in studies:
            failures.append(
                f"restricted study {spec_dir!r} has no "
                "taxonomy assignment"
            )
        if spec_dir not in PM_RESTRICTED_NAME_ONLY:
            failures.append(
                f"restricted study {spec_dir!r} has no "
                "registered name-only form in the gate's "
                "copies (defs §7)"
            )
    structure = {
        "domains": domains,
        "subdomains": subdomains,
        "studies": studies,
        "documents": documents,
        "restricted": list(restricted),
        "version": tax.get("version"),
    }
    return structure, failures


def _pm_roll_up(counts: dict[str, int]) -> tuple[str, bool]:
    """The study roll-up precedence (defs §5). Returns
    (class, is_judgment_call); first matching rule wins."""
    total = sum(counts.values())
    if total == 0:
        return "unjudged", False
    if counts["positive"] > 0 and counts["negative"] > 0:
        return "open", True
    if counts["closed_other"] == total:
        return "closed_other", False
    if counts["negative"] > 0:
        return "negative", False
    if counts["positive"] > 0:
        return "positive", False
    return "open", False


def _pm_dump(obj: Any) -> bytes:
    """The published artifacts' byte format, as the gate
    reproduces it for the byte-equality legs."""
    return (
        json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True)
        + "\n"
    ).encode("utf-8")


def _pm_render_page(map_bytes: bytes, finds_bytes: bytes) -> bytes:
    """The gate's own rendering of the page (Stage 4): the
    gate's registered template copies wrapped around the
    gate's recomputed data artifacts. The page carries no
    derivation of its own — it is the two artifacts embedded
    verbatim — so recomputing it from the recomputed data
    under the gate's template copies is the whole route."""
    return (
        PM_PAGE_HEAD.encode("utf-8")
        + map_bytes
        + PM_PAGE_MID.encode("utf-8")
        + finds_bytes
        + PM_PAGE_TAIL.encode("utf-8")
    )


def _pm_page_divergences(
    committed: bytes, artifacts: dict[str, bytes]
) -> list[str]:
    """Name the segment(s) in which a published page
    diverges from the gate's recomputation: the embedded
    program-map payload, the embedded finds payload, or the
    template chrome around them — enough to repair from,
    never a silent 'differs'."""
    out: list[str] = []
    try:
        text = committed.decode("utf-8")
    except UnicodeDecodeError as exc:
        return [f"page is not readable UTF-8: {exc}"]
    map_marker = 'id="program-map-data">\n'
    finds_marker = 'id="program-map-finds">\n'
    if map_marker not in text or finds_marker not in text:
        out.append(
            "page does not carry the registered embedded-data "
            "markers (the verbatim embedding is absent or "
            "reshaped)"
        )
        return out
    head, rest = text.split(map_marker, 1)
    map_payload, rest = rest.split("</script>", 1)
    if finds_marker not in rest:
        out.append("page's finds payload marker is missing")
        return out
    mid, rest = rest.split(finds_marker, 1)
    finds_payload, tail = rest.split("</script>", 1)
    tail = "</script>" + tail
    if head + map_marker != PM_PAGE_HEAD:
        out.append(
            "page chrome before the embedded program-map data "
            "diverges from the gate's registered template copy"
        )
    if map_payload.encode("utf-8") != artifacts[PROGRAM_MAP_REL]:
        out.append(
            "embedded program-map payload is not the gate's "
            "recomputed program-map.json, byte for byte"
        )
    if "</script>" + mid != PM_PAGE_MID:
        out.append(
            "page chrome between the embedded payloads "
            "diverges from the gate's registered template copy"
        )
    if finds_payload.encode("utf-8") != artifacts[PROGRAM_MAP_FINDS_REL]:
        out.append(
            "embedded finds payload is not the gate's "
            "recomputed program-map-finds.json, byte for byte"
        )
    if tail != PM_PAGE_TAIL:
        out.append(
            "page chrome after the embedded finds payload "
            "diverges from the gate's registered template copy"
        )
    if not out:
        out.append(
            "page bytes differ but no segment divergence was "
            "isolated (serialization-level drift)"
        )
    return out


def _derive_program_map(
    root: Path,
    entries: list[dict[str, Any]],
    tax: dict[str, Any],
) -> tuple[Optional[dict[str, bytes]], list[str], list[str]]:
    """Recompute the program-map artifacts from the
    ledger entries + taxonomy under the gate's registered
    copies (the two data artifacts, and the page rendered
    from them under the gate's template copies). Returns
    (artifact bytes by rel path, refusal failures, coverage
    failures): any refusal means no artifacts — the route
    fails closed exactly where the builder does, by its
    own code."""
    failures: list[str] = []
    coverage_failures: list[str] = []
    specs_dir = root / PROGRAM_MAP_SPECS_REL
    if not specs_dir.is_dir():
        return None, [f"spec tree not found: {specs_dir}"], []
    spec_dirs = sorted(p.name for p in specs_dir.iterdir() if p.is_dir())

    # Taxonomy coverage is exact and bidirectional (§8).
    assigned = set(tax["studies"])
    actual = set(spec_dirs)
    if assigned != actual:
        if actual - assigned:
            coverage_failures.append(
                "spec directories with no assignment: "
                f"{sorted(actual - assigned)}"
            )
        if assigned - actual:
            coverage_failures.append(
                "assignments naming no directory: "
                f"{sorted(assigned - actual)}"
            )

    # Governing entries (§3): claims in ledger order, then
    # every reclassification applied in ledger order.
    claims: dict[str, dict[str, Any]] = {}
    order: list[str] = []
    for row in entries:
        if row.get("kind") != "claim":
            continue
        cid = row.get("id")
        if cid in claims:
            failures.append(f"duplicate claim id in ledger: {cid}")
            continue
        claims[cid] = dict(row)
        order.append(cid)
    for row in entries:
        if row.get("kind") != "reclassification":
            continue
        target = row.get("supersedes")
        if target not in claims:
            failures.append(
                f"reclassification {row.get('id')!r} supersedes "
                f"{target!r}, which is not a claim entry"
            )
            continue
        for field_name in ("status", "stage"):
            if field_name in row:
                claims[target][field_name] = row[field_name]
    governing = [claims[cid] for cid in order]

    ledger_path = root / li.LEDGER_REL
    dates = [str(r.get("date")) for r in entries if r.get("date")]
    stamp = {
        "ledger_latest_entry_date": max(dates) if dates else None,
        "ledger_lines": len(entries),
        "ledger_schema": li.SCHEMA_VERSION,
        "ledger_sha256": (
            li.sha256_file(ledger_path) if ledger_path.is_file() else None
        ),
        "program_map_defs": GATE_PROGRAM_MAP_DEFS_VERSION,
        "program_map_taxonomy": PROGRAM_MAP_TAXONOMY_VERSION,
    }

    def _source_of_record(
        entry: dict[str, Any],
    ) -> Optional[dict[str, Any]]:
        sors = [
            s
            for s in entry.get("sources") or []
            if isinstance(s, dict) and s.get("role") == "source_of_record"
        ]
        if len(sors) != 1:
            failures.append(
                f"claim {entry.get('id')!r} has {len(sors)} "
                "source-of-record sources; exactly one is "
                "required to place it"
            )
            return None
        return sors[0]

    claim_nodes: list[dict[str, Any]] = []
    members: dict[str, list[str]] = {d: [] for d in spec_dirs}
    multi_spec_claims: list[str] = []
    null_falsifier_extracted: list[dict[str, Any]] = []
    falsifier_present_count = 0
    documents_seen: set[str] = set()
    for entry in governing:
        status = entry.get("status")
        if status not in PM_STATUS_TO_CLASS:
            failures.append(
                f"claim {entry.get('id')!r} carries the "
                f"unregistered status {status!r} (defs §4.2)"
            )
            continue
        cls = PM_STATUS_TO_CLASS[status]
        if cls == PM_IN_FLIGHT:
            failures.append(
                f"claim {entry.get('id')!r} derived the "
                "in_flight class, which has no derivation "
                "rule in v1 (defs §11)"
            )
            continue
        present = bool(entry.get("falsifier"))
        if present:
            falsifier_present_count += 1
        node: dict[str, Any] = {
            "class": cls,
            "document": None,
            "domain": None,
            "falsifier_present": present,
            "id": entry.get("id"),
            "kind": "claim",
            "population": entry.get("population"),
            "stage": entry.get("stage"),
            "standing": PM_STANDING_TEMPLATE.format(
                status=status,
                stage=entry.get("stage") if entry.get("stage") else "none",
                falsifier="present" if present else "absent",
            ),
            "status": status,
            "study": None,
            "subdomain": None,
        }
        population = entry.get("population")
        if population == "bundle":
            sor = _source_of_record(entry)
            home = sor.get("spec") if sor else None
            if not home or home not in actual:
                failures.append(
                    f"bundle claim {entry.get('id')!r} names "
                    f"the home study {home!r}, which is not a "
                    "spec directory (citation does not resolve)"
                )
                continue
            specs_named = {
                s.get("spec")
                for s in entry.get("sources") or []
                if isinstance(s, dict) and s.get("spec")
            }
            if len(specs_named) > 1:
                multi_spec_claims.append(entry["id"])
            assignment = tax["studies"][home]
            node["study"] = home
            node["domain"] = assignment["domain"]
            node["subdomain"] = assignment["subdomain"]
            members[home].append(cls)
        elif population == "extracted":
            sor = _source_of_record(entry)
            document = sor.get("document_id") if sor else None
            if not document or document not in tax["documents"]:
                failures.append(
                    f"extracted claim {entry.get('id')!r} names "
                    f"the source document {document!r}, which "
                    "has no taxonomy assignment"
                )
                continue
            documents_seen.add(document)
            assignment = tax["documents"][document]
            node["document"] = document
            node["domain"] = assignment["domain"]
            node["subdomain"] = assignment["subdomain"]
            if not present:
                null_falsifier_extracted.append(
                    {"document": document, "id": entry["id"]}
                )
        else:
            failures.append(
                f"claim {entry.get('id')!r} has population "
                f"{population!r}, which has no registered "
                "assignment route in program-map-defs v1 (§4.1)"
            )
            continue
        claim_nodes.append(node)
    unassigned_documents = set(tax["documents"]) - documents_seen
    if unassigned_documents:
        coverage_failures.append(
            "taxonomy assigns extracted documents the ledger "
            f"does not carry: {sorted(unassigned_documents)}"
        )
    uncarried = documents_seen - set(tax["documents"])
    if uncarried:  # unreachable given the placement refusal; stated anyway
        coverage_failures.append(
            "ledger documents with no taxonomy assignment: "
            f"{sorted(uncarried)}"
        )

    restricted = set(tax["restricted"])
    study_nodes: list[dict[str, Any]] = []
    finds: list[dict[str, Any]] = []
    unjudged_studies: list[str] = []
    judgment_calls: list[str] = []
    for spec_dir in spec_dirs:
        assignment = tax["studies"].get(spec_dir)
        if assignment is None:
            continue  # the coverage leg names it; no node is derivable
        if spec_dir in restricted:
            study_nodes.append(
                {
                    "class": None,
                    "domain": assignment["domain"],
                    "id": spec_dir,
                    "kind": "study",
                    "restricted": True,
                    "standing": PM_RESTRICTED_NAME_ONLY[spec_dir],
                    "subdomain": assignment["subdomain"],
                }
            )
            finds.append({"kind": "restricted_node", "subject": spec_dir})
            continue
        counts = {c: 0 for c in PM_CLAIM_CLASSES}
        for member_cls in members[spec_dir]:
            counts[member_cls] += 1
        cls, is_judgment = _pm_roll_up(counts)
        if cls == PM_IN_FLIGHT:
            failures.append(
                f"study {spec_dir!r} derived the in_flight "
                "class, which has no derivation rule in v1 "
                "(defs §11)"
            )
            continue
        study_nodes.append(
            {
                "class": cls,
                "domain": assignment["domain"],
                "id": spec_dir,
                "judgment_call": is_judgment,
                "kind": "study",
                "member_counts": {
                    **counts,
                    "total": sum(counts.values()),
                },
                "restricted": False,
                "subdomain": assignment["subdomain"],
            }
        )
        if cls == "unjudged":
            unjudged_studies.append(spec_dir)
            finds.append(
                {"kind": "bundle_less_study", "subject": spec_dir}
            )
        if is_judgment:
            judgment_calls.append(spec_dir)
            finds.append(
                {
                    "kind": "judgment_call",
                    "negative": counts["negative"],
                    "positive": counts["positive"],
                    "subject": spec_dir,
                    "total": sum(counts.values()),
                }
            )
    for item in null_falsifier_extracted:
        finds.append(
            {
                "document": item["document"],
                "kind": "extracted_null_falsifier",
                "subject": item["id"],
            }
        )
    finds.sort(key=lambda f: (f["kind"], f["subject"]))
    claim_nodes.sort(key=lambda n: n["id"])
    study_nodes.sort(key=lambda n: n["id"])

    def _class_counts(
        nodes: list[dict[str, Any]], classes: tuple[str, ...]
    ) -> dict[str, int]:
        out = {c: 0 for c in classes}
        for node in nodes:
            if node["class"] in out:
                out[node["class"]] += 1
        return out

    domains_block: dict[str, Any] = {}
    for domain in tax["domains"]:
        d_claims = [n for n in claim_nodes if n["domain"] == domain]
        d_studies = [n for n in study_nodes if n["domain"] == domain]
        domains_block[domain] = {
            "claims": len(d_claims),
            "claims_by_class": _class_counts(d_claims, PM_CLAIM_CLASSES),
            "restricted_studies": sum(
                1 for n in d_studies if n["restricted"]
            ),
            "studies": len(d_studies),
            "studies_by_class": _class_counts(d_studies, PM_STUDY_CLASSES),
        }
    coverage = {
        "claims": {
            "by_class": _class_counts(claim_nodes, PM_CLAIM_CLASSES),
            "by_population": {
                pop: sum(
                    1 for n in claim_nodes if n["population"] == pop
                )
                for pop in sorted({n["population"] for n in claim_nodes})
            },
            "total": len(claim_nodes),
        },
        "domains": domains_block,
        "falsifier_coverage": {
            "null_extracted_claims": sorted(
                item["id"] for item in null_falsifier_extracted
            ),
            "present": falsifier_present_count,
            "total": len(claim_nodes),
        },
        "judgment_call_studies": sorted(judgment_calls),
        "multi_spec_claims": sorted(multi_spec_claims),
        "studies": {
            "by_class": _class_counts(study_nodes, PM_STUDY_CLASSES),
            "restricted": len(restricted),
            "total": len(study_nodes),
        },
        "unjudged_studies": sorted(unjudged_studies),
    }
    program_map = {
        "coverage": coverage,
        "defs_version": GATE_PROGRAM_MAP_DEFS_VERSION,
        "nodes": {"claims": claim_nodes, "studies": study_nodes},
        "stamp": stamp,
        "taxonomy_version": PROGRAM_MAP_TAXONOMY_VERSION,
    }
    finds_doc = {
        "defs_version": GATE_PROGRAM_MAP_DEFS_VERSION,
        "finds": finds,
        "stamp": stamp,
        "taxonomy_version": PROGRAM_MAP_TAXONOMY_VERSION,
    }
    if failures or coverage_failures:
        return None, failures, coverage_failures
    artifacts = {
        PROGRAM_MAP_REL: _pm_dump(program_map),
        PROGRAM_MAP_FINDS_REL: _pm_dump(finds_doc),
    }
    artifacts[PROGRAM_MAP_HTML_REL] = _pm_render_page(
        artifacts[PROGRAM_MAP_REL], artifacts[PROGRAM_MAP_FINDS_REL]
    )
    return artifacts, failures, coverage_failures


def _pm_census_lines(program_map: dict[str, Any]) -> list[str]:
    coverage = program_map.get("coverage", {})
    claims = coverage.get("claims", {})
    studies = coverage.get("studies", {})
    fc = coverage.get("falsifier_coverage", {})
    lines = [
        "census: "
        f"{claims.get('total')} claim nodes by class "
        f"{claims.get('by_class')}; {studies.get('total')} "
        f"study nodes by class {studies.get('by_class')} "
        f"(+{studies.get('restricted')} restricted, name-only)",
        "census: judgment calls "
        f"{len(coverage.get('judgment_call_studies', []))}; "
        f"unjudged studies "
        f"{len(coverage.get('unjudged_studies', []))}; "
        "falsifier coverage "
        f"{fc.get('present')} of {fc.get('total')} claims",
    ]
    for domain, block in sorted(
        (coverage.get("domains") or {}).items()
    ):
        lines.append(
            f"census: domain {domain!r}: {block.get('studies')} "
            f"studies, {block.get('claims')} claims (per-domain "
            "counts only; no cross-domain aggregate, C088-14)"
        )
    return lines


def _v10_checks(
    root: Path, entries: list[dict[str, Any]]
) -> list[Check]:
    """V10's legs. Where the program-map layer has not
    landed at all (no taxonomy and no published artifacts —
    a pre-Spec-088 tree, or a scratch tree carrying only
    the older chain), V10 enumerates a single NOT-RUN, the
    V5 posture toward a layer that did not exist yet. Once
    any part of the layer is present, every leg runs and
    absence is a named failure."""
    checks: list[Check] = []
    taxonomy_path = root / PROGRAM_MAP_TAXONOMY_REL
    map_path = root / PROGRAM_MAP_REL
    finds_path = root / PROGRAM_MAP_FINDS_REL
    page_path = root / PROGRAM_MAP_HTML_REL
    if (
        not taxonomy_path.is_file()
        and not map_path.is_file()
        and not finds_path.is_file()
        and not page_path.is_file()
    ):
        return [
            Check(
                "V10 program-map equivalence",
                "NOT-RUN",
                [
                    "no program-map layer in this tree (no "
                    "taxonomy, no published artifacts); the "
                    "layer lands with Spec 088 S1/S2"
                ],
            )
        ]

    tax, tax_failures = _pm_taxonomy(root)
    artifacts: Optional[dict[str, bytes]] = None
    derive_failures: list[str] = []
    coverage_failures: list[str] = list(tax_failures)
    expected_map: Optional[dict[str, Any]] = None
    expected_finds: Optional[dict[str, Any]] = None
    if tax is not None:
        artifacts, derive_failures, cov_failures = _derive_program_map(
            root, entries, tax
        )
        coverage_failures.extend(cov_failures)
        if artifacts is not None:
            expected_map = json.loads(artifacts[PROGRAM_MAP_REL])
            expected_finds = json.loads(artifacts[PROGRAM_MAP_FINDS_REL])

    # -- Leg 1: taxonomy coverage and format, bidirectional.
    leg1_evidence = list(coverage_failures)
    if tax is not None and not coverage_failures:
        leg1_evidence = [
            f"taxonomy assigns all {len(tax['studies'])} spec "
            "directories exactly once (set equality both "
            "directions); every extracted document the ledger "
            f"carries is assigned ({len(tax['documents'])}) and "
            "every assignment is carried; the format carries "
            "no standing-shaped key (defs §8)"
        ]
    checks.append(
        Check(
            "V10 program-map equivalence — taxonomy coverage "
            "and format (bidirectional)",
            "FAIL" if coverage_failures else "PASS",
            leg1_evidence,
        )
    )

    # -- Leg 2: program-map.json byte-equality + citations.
    if not map_path.is_file():
        checks.append(
            Check(
                "V10 program-map equivalence — program-map.json",
                "FAIL",
                [f"published artifact missing: {map_path}"],
            )
        )
    elif artifacts is None:
        checks.append(
            Check(
                "V10 program-map equivalence — program-map.json",
                "FAIL",
                [
                    "the gate's recomputation refused, so no "
                    "equality can be established: "
                    + "; ".join(
                        (derive_failures or coverage_failures)[:4]
                    )
                ],
            )
        )
    else:
        committed_bytes = map_path.read_bytes()
        if committed_bytes == artifacts[PROGRAM_MAP_REL]:
            checks.append(
                Check(
                    "V10 program-map equivalence — "
                    "program-map.json byte-equals the gate's "
                    "recomputation (program-map-defs v1 copies)",
                    "PASS",
                    [
                        "every claim node cites its governing "
                        "ledger entry, every study node its "
                        "spec directory, every extracted "
                        "document its taxonomy assignment — "
                        "the recomputation is built only from "
                        "resolving citations, and the published "
                        "bytes equal it exactly"
                    ]
                    + _pm_census_lines(expected_map or {}),
                )
            )
        else:
            divs: list[str] = []
            try:
                committed_map = json.loads(
                    committed_bytes.decode("utf-8")
                )
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                divs.append(f"artifact is not readable JSON: {exc}")
                committed_map = None
            if committed_map is not None and expected_map is not None:
                for section in (
                    "defs_version",
                    "taxonomy_version",
                    "stamp",
                    "coverage",
                    "nodes",
                ):
                    _first_divergences(
                        expected_map.get(section),
                        committed_map.get(section),
                        section,
                        divs,
                        limit=10,
                    )
            checks.append(
                Check(
                    "V10 program-map equivalence — "
                    "program-map.json byte-equals the gate's "
                    "recomputation (program-map-defs v1 copies)",
                    "FAIL",
                    divs[:40]
                    or [
                        "bytes differ but no section divergence "
                        "was isolated (serialization-level drift)"
                    ],
                )
            )

    # -- Leg 3: program-map-finds.json byte-equality (find list).
    if not finds_path.is_file():
        checks.append(
            Check(
                "V10 program-map equivalence — program-map-finds.json",
                "FAIL",
                [f"published artifact missing: {finds_path}"],
            )
        )
    elif artifacts is None:
        checks.append(
            Check(
                "V10 program-map equivalence — program-map-finds.json",
                "FAIL",
                [
                    "the gate's recomputation refused, so no "
                    "equality can be established: "
                    + "; ".join(
                        (derive_failures or coverage_failures)[:4]
                    )
                ],
            )
        )
    else:
        committed_bytes = finds_path.read_bytes()
        if committed_bytes == artifacts[PROGRAM_MAP_FINDS_REL]:
            find_counts = Counter(
                f["kind"] for f in (expected_finds or {}).get("finds", [])
            )
            checks.append(
                Check(
                    "V10 program-map equivalence — "
                    "program-map-finds.json byte-equals the "
                    "gate's recomputation (find-list equality)",
                    "PASS",
                    [
                        "find list equal: "
                        + ", ".join(
                            f"{kind} {n}"
                            for kind, n in sorted(find_counts.items())
                        )
                    ],
                )
            )
        else:
            divs = []
            try:
                committed_finds = json.loads(
                    committed_bytes.decode("utf-8")
                )
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                divs.append(f"artifact is not readable JSON: {exc}")
                committed_finds = None
            if committed_finds is not None and expected_finds is not None:
                for section in (
                    "defs_version",
                    "taxonomy_version",
                    "stamp",
                    "finds",
                ):
                    _first_divergences(
                        expected_finds.get(section),
                        committed_finds.get(section),
                        section,
                        divs,
                        limit=10,
                    )
            checks.append(
                Check(
                    "V10 program-map equivalence — "
                    "program-map-finds.json byte-equals the "
                    "gate's recomputation (find-list equality)",
                    "FAIL",
                    divs[:40]
                    or [
                        "bytes differ but no section divergence "
                        "was isolated (serialization-level drift)"
                    ],
                )
            )

    # -- Leg 4: stamp freshness against the current ledger.
    stamp_failures: list[str] = []
    stamp: Optional[dict[str, Any]] = None
    if map_path.is_file():
        try:
            stamp = json.loads(
                map_path.read_text(encoding="utf-8")
            ).get("stamp")
        except (OSError, json.JSONDecodeError) as exc:
            stamp_failures.append(
                f"cannot read the artifact's stamp: {exc}"
            )
    else:
        stamp_failures.append(
            "no published program-map.json, so no stamp to check"
        )
    if stamp is not None:
        ledger_path = root / li.LEDGER_REL
        current = {
            "ledger_sha256": (
                li.sha256_file(ledger_path)
                if ledger_path.is_file()
                else None
            ),
            "ledger_lines": len(entries),
            "ledger_latest_entry_date": (
                max(str(r.get("date")) for r in entries if r.get("date"))
                if any(r.get("date") for r in entries)
                else None
            ),
            "ledger_schema": li.SCHEMA_VERSION,
            "program_map_defs": GATE_PROGRAM_MAP_DEFS_VERSION,
            "program_map_taxonomy": (
                tax.get("version") if tax is not None else None
            ),
        }
        for field_name, current_value in current.items():
            if stamp.get(field_name) != current_value:
                stamp_failures.append(
                    f"stamp {field_name}: artifact carries "
                    f"{stamp.get(field_name)!r}, current value "
                    f"is {current_value!r} (stale artifact, "
                    "defs §10)"
                )
    checks.append(
        Check(
            "V10 program-map equivalence — stamp freshness "
            "against the current ledger",
            "FAIL" if stamp_failures else "PASS",
            stamp_failures
            or [
                "stamp ledger hash, line count, latest entry "
                "date, and versions all equal the current "
                "ledger's"
            ],
        )
    )

    # -- Leg 5: program-map.html byte-equality (Stage 4: the
    # page joins V10's artifact list). The page is the gate's
    # recomputed data artifacts embedded verbatim in the
    # gate's registered template copies, so byte-equality
    # carries both the data and the template.
    if not page_path.is_file():
        checks.append(
            Check(
                "V10 program-map equivalence — program-map.html",
                "FAIL",
                [f"published artifact missing: {page_path}"],
            )
        )
    elif artifacts is None:
        checks.append(
            Check(
                "V10 program-map equivalence — program-map.html",
                "FAIL",
                [
                    "the gate's recomputation refused, so no "
                    "equality can be established: "
                    + "; ".join(
                        (derive_failures or coverage_failures)[:4]
                    )
                ],
            )
        )
    else:
        committed_page = page_path.read_bytes()
        if committed_page == artifacts[PROGRAM_MAP_HTML_REL]:
            checks.append(
                Check(
                    "V10 program-map equivalence — "
                    "program-map.html byte-equals the gate's "
                    "recomputation (registered template copies)",
                    "PASS",
                    [
                        "the page is the gate's recomputed "
                        "program-map.json and "
                        "program-map-finds.json embedded "
                        "verbatim in the gate's registered "
                        "template copies; the published bytes "
                        "equal that recomputation exactly, so "
                        "the page can show nothing the "
                        "recomputed data does not carry"
                    ],
                )
            )
        else:
            checks.append(
                Check(
                    "V10 program-map equivalence — "
                    "program-map.html byte-equals the gate's "
                    "recomputation (registered template copies)",
                    "FAIL",
                    _pm_page_divergences(committed_page, artifacts),
                )
            )
    return checks


# ---------------------------------------------------------------------------
# V11 — run-binding (Spec 089 Stage 5, T502). The gate's
# own registered copies of run-defs v2's checkable rules
# (glossa-indus/ledger/RUN-DEFINITIONS.md), deliberately
# NOT imported from the run tooling (run_records,
# run_junction): the header required-fields list, the
# key's component and constitutive sets, the disposition
# vocabulary, the absence kinds, the index act forms and
# fold refusals, and the legacy label. A deliberate
# run-defs change is made in every copy in the same
# motion (run-defs v2 §9); a change made in the tooling's
# copy only is exactly the divergence this class exists
# to catch (C089-15). The gate verifies bindings,
# citations, censuses, and junction completeness; it
# never originates a junction analysis, appends an act,
# or lifts a quarantine (D-089-2, C089-16).

GATE_RUN_DEFS_VERSION = "run-defs v2"
RUN_JUNCTIONS_REL = "glossa-indus/ledger/junctions"
RUN_INDEX_NAME = "run-index.jsonl"
RUN_SURFACES = ("settling", "experiment", "study", "suite")
RUN_HEADER_FIELDS = (
    "run_id",
    "surface",
    "tool",
    "tool_version",
    "started",
    "key",
    "determinism_class",
)
RUN_KEY_COMPONENTS = (
    "surface",
    "command",
    "tool_version",
    "input_pins",
    "seed",
    "code_version",
    "environment_class",
)
RUN_CONSTITUTIVE_COMPONENTS = (
    "surface",
    "command",
    "tool_version",
    "input_pins",
    "seed",
)
RUN_DETERMINISM_CLASSES = ("deterministic", "named-nondeterministic")
RUN_DISPOSITIONS = (
    "explained-by-named-difference",
    "not-comparable",
    "identical-after-all",
    "unexplained",
)
RUN_ABSENCE_KINDS = ("empty", "refused", "crashed")
RUN_ACT_KINDS = (
    "entry",
    "supersedes",
    "quarantine",
    "adjudication",
    "departure",
)
RUN_ADJUDICATION_STATES = (
    "quarantine-lifted",
    "quarantine-confirmed",
)
RUN_LEGACY_LABEL = "legacy — key partial"
_RUN_ID_RE = re.compile(
    r"^(settling|experiment|study|suite)-\d{8}T\d{6}Z-[0-9a-f]{6}$"
)
_RUN_TOKEN_RE = re.compile(
    r"(?<![\w-])(?:settling|experiment|study|suite)"
    r"-\d{8}T\d{6}Z-[0-9a-f]{6}(?![\w-])"
)
_JUNCTION_ID_RE = re.compile(r"^junction-\d{8}T\d{6}Z-[0-9a-f]{6}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
_EVENT_RE = re.compile(r"^re_derivations\[(\d+)\]$")


class _V11Store:
    """One guarded run store as the gate reads it: its
    index acts, the gate's own fold of them, and its
    record files parsed once for every leg."""

    def __init__(self, label: str, store_dir: Path):
        self.label = label
        self.dir = store_dir
        self.index_path = store_dir / RUN_INDEX_NAME
        self.acts: list[Any] = []
        self.index_failures: list[str] = []
        if self.index_path.is_file():
            for line_no, line in enumerate(
                self.index_path.read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if not line.strip():
                    continue
                try:
                    self.acts.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    self.index_failures.append(
                        f"{label}: index line {line_no} is not "
                        f"readable JSON: {exc}"
                    )
        self.entries: dict[str, dict[str, Any]] = {}
        self.superseded_by: dict[str, str] = {}
        self.junctions: dict[str, dict[str, Any]] = {}
        self.departed: dict[str, dict[str, Any]] = {}
        self.fold_failures: list[str] = []
        self._fold()
        self.records: dict[str, Optional[dict[str, Any]]] = {}
        if store_dir.is_dir():
            for path in sorted(store_dir.glob("*.json")):
                try:
                    parsed = json.loads(
                        path.read_text(encoding="utf-8")
                    )
                    self.records[path.name] = (
                        parsed if isinstance(parsed, dict) else None
                    )
                except (OSError, UnicodeDecodeError, json.JSONDecodeError):
                    self.records[path.name] = None

    def _fold(self) -> None:
        """The gate's own fold of the index acts, under
        run-defs v2 §7.1's refusal rules (registered
        copies): refusals are collected as named failures,
        never raised, and a refused act changes no state —
        the same order the tooling's fold enforces."""
        for pos, act in enumerate(self.acts, start=1):
            where = f"{self.label} index act {pos}"
            if not isinstance(act, dict):
                self.fold_failures.append(
                    f"{where}: act is not an object"
                )
                continue
            kind = act.get("act")
            if kind not in RUN_ACT_KINDS:
                self.fold_failures.append(
                    f"{where}: unknown index act kind {kind!r}; "
                    f"the acts are {list(RUN_ACT_KINDS)}"
                )
                continue
            if kind == "entry":
                self._fold_entry(where, act)
            elif kind == "supersedes":
                self._fold_supersedes(where, act)
            elif kind == "quarantine":
                self._fold_quarantine(where, act)
            elif kind == "adjudication":
                self._fold_adjudication(where, act)
            else:
                self._fold_departure(where, act)

    def _fold_entry(self, where: str, act: dict[str, Any]) -> None:
        for name in ("run_id", "record", "key"):
            if name not in act:
                self.fold_failures.append(
                    f"{where}: entry act is missing field {name!r}"
                )
                return
        run_id = act["run_id"]
        if not isinstance(run_id, str) or not run_id:
            self.fold_failures.append(
                f"{where}: entry act run_id must be a string"
            )
            return
        legacy_id = run_id.startswith("legacy:")
        if not legacy_id and not _RUN_ID_RE.match(run_id):
            self.fold_failures.append(
                f"{where}: entry act run id {run_id!r} is "
                "neither a run-defs v2 run id nor a legacy id"
            )
            return
        if not isinstance(act["record"], str) or not act["record"]:
            self.fold_failures.append(
                f"{where}: entry act 'record' must be a "
                "non-empty path string"
            )
            return
        if not isinstance(act["key"], dict):
            self.fold_failures.append(
                f"{where}: entry act 'key' must be an object"
            )
            return
        if run_id in self.entries:
            self.fold_failures.append(
                f"{where}: duplicate entry act for run id "
                f"{run_id!r} — an id is one execution, "
                "entered once"
            )
            return
        if act.get("legacy"):
            if not legacy_id:
                self.fold_failures.append(
                    f"{where}: legacy entry act carries "
                    f"non-legacy run id {run_id!r}"
                )
                return
            if act.get("label") != RUN_LEGACY_LABEL or not act.get(
                "key_partial"
            ):
                self.fold_failures.append(
                    f"{where}: legacy entry {run_id!r} must "
                    f"carry the label {RUN_LEGACY_LABEL!r} "
                    "and key_partial: true"
                )
                return
            if not act.get("missing"):
                self.fold_failures.append(
                    f"{where}: legacy entry {run_id!r} must "
                    "name the components that do not exist "
                    "to recover ('missing')"
                )
                return
        elif legacy_id:
            self.fold_failures.append(
                f"{where}: entry act for legacy id "
                f"{run_id!r} is not marked legacy — legacy "
                "ids exist only under the partial label"
            )
            return
        else:
            # A non-legacy entry's key is a full run-key v1
            # key (the tooling's fold validates it the same
            # way): every registered component present, the
            # string components non-empty strings, the pins
            # an object.
            key = act["key"]
            for component in RUN_KEY_COMPONENTS:
                if component not in key:
                    self.fold_failures.append(
                        f"{where}: entry act key omits "
                        f"registered component {component!r}"
                    )
                    return
            for component in (
                "command",
                "tool_version",
                "code_version",
                "environment_class",
            ):
                if not isinstance(key[component], str) or not key[
                    component
                ]:
                    self.fold_failures.append(
                        f"{where}: entry act key component "
                        f"{component!r} must be a non-empty "
                        "string"
                    )
                    return
            if not isinstance(key["input_pins"], dict):
                self.fold_failures.append(
                    f"{where}: entry act key component "
                    "'input_pins' must be an object"
                )
                return
        self.entries[run_id] = act

    def _fold_supersedes(self, where: str, act: dict[str, Any]) -> None:
        for name in ("run_id", "supersedes", "ref"):
            if name not in act:
                self.fold_failures.append(
                    f"{where}: supersedes act is missing "
                    f"field {name!r}"
                )
                return
        new_id, old_id = act["run_id"], act["supersedes"]
        for named in (new_id, old_id):
            if named not in self.entries:
                self.fold_failures.append(
                    f"{where}: supersedes act names unknown "
                    f"run id {named!r}"
                )
                return
        if new_id == old_id:
            self.fold_failures.append(
                f"{where}: a run may not supersede itself"
            )
            return
        if not isinstance(act["ref"], str) or not act["ref"]:
            self.fold_failures.append(
                f"{where}: supersedes act must carry the "
                "act reference ('ref') that ordered the "
                "supersession"
            )
            return
        if old_id in self.superseded_by:
            self.fold_failures.append(
                f"{where}: run {old_id!r} is already "
                f"superseded by {self.superseded_by[old_id]!r} "
                "— a record's successor is single"
            )
            return
        self.superseded_by[old_id] = new_id

    def _fold_quarantine(self, where: str, act: dict[str, Any]) -> None:
        for name in ("junction_id", "run_ids"):
            if name not in act:
                self.fold_failures.append(
                    f"{where}: quarantine act is missing "
                    f"field {name!r}"
                )
                return
        junction_id = act["junction_id"]
        if not isinstance(junction_id, str) or not _JUNCTION_ID_RE.match(
            junction_id
        ):
            self.fold_failures.append(
                f"{where}: quarantine act junction id "
                f"{junction_id!r} is malformed"
            )
            return
        run_ids = act["run_ids"]
        if not isinstance(run_ids, list) or not run_ids:
            self.fold_failures.append(
                f"{where}: quarantine act 'run_ids' must be "
                "a non-empty list"
            )
            return
        for run_id in run_ids:
            if run_id not in self.entries:
                self.fold_failures.append(
                    f"{where}: quarantine act names unknown "
                    f"run id {run_id!r}"
                )
                return
        junction = self.junctions.setdefault(
            junction_id, {"run_ids": [], "lifted": False}
        )
        for run_id in run_ids:
            if run_id not in junction["run_ids"]:
                junction["run_ids"].append(run_id)

    def _fold_adjudication(self, where: str, act: dict[str, Any]) -> None:
        for name in ("junction_id", "ruling", "actor", "resulting_state"):
            if name not in act:
                self.fold_failures.append(
                    f"{where}: adjudication act is missing "
                    f"field {name!r}"
                )
                return
        junction_id = act["junction_id"]
        if junction_id not in self.junctions:
            self.fold_failures.append(
                f"{where}: adjudication act names unknown "
                f"junction id {junction_id!r} (no quarantine "
                "act introduced it)"
            )
            return
        if act["resulting_state"] not in RUN_ADJUDICATION_STATES:
            self.fold_failures.append(
                f"{where}: adjudication resulting_state "
                f"{act['resulting_state']!r} is not "
                f"registered; the states are "
                f"{list(RUN_ADJUDICATION_STATES)}"
            )
            return
        for name in ("ruling", "actor"):
            if not isinstance(act[name], str) or not act[name]:
                self.fold_failures.append(
                    f"{where}: adjudication act {name!r} "
                    "must be a non-empty string"
                )
                return
        self.junctions[junction_id]["lifted"] = (
            act["resulting_state"] == "quarantine-lifted"
        )

    def _fold_departure(self, where: str, act: dict[str, Any]) -> None:
        """The gate's own fold of a departure act (run-defs
        v2 §7.1, registered copy of the tooling's fold):
        the departed-generation accounting — an appended
        act carrying, for an entered generation whose
        record no longer stands in the store, the
        superseding commit, the record's final git blob,
        and the blob's SHA-256."""
        for name in (
            "run_id",
            "record",
            "superseded_by_commit",
            "git_blob",
            "blob_sha256",
            "ref",
        ):
            if name not in act:
                self.fold_failures.append(
                    f"{where}: departure act is missing "
                    f"field {name!r}"
                )
                return
        run_id = act["run_id"]
        if run_id not in self.entries:
            self.fold_failures.append(
                f"{where}: departure act names unknown "
                f"run id {run_id!r}"
            )
            return
        if act["record"] != self.entries[run_id]["record"]:
            self.fold_failures.append(
                f"{where}: departure act for run {run_id!r} "
                f"names record {act['record']!r}, which "
                "differs from its entry's record "
                f"{self.entries[run_id]['record']!r}"
            )
            return
        if run_id in self.departed:
            self.fold_failures.append(
                f"{where}: run {run_id!r} already stands "
                "accounted as departed — a generation's "
                "departure is accounted once"
            )
            return
        if not _COMMIT_RE.match(str(act["superseded_by_commit"])):
            self.fold_failures.append(
                f"{where}: departure act "
                "'superseded_by_commit' must be a commit "
                f"id, got {act['superseded_by_commit']!r}"
            )
            return
        if not isinstance(act["git_blob"], str) or not act["git_blob"]:
            self.fold_failures.append(
                f"{where}: departure act 'git_blob' must "
                "be a non-empty string"
            )
            return
        if not _SHA256_RE.match(str(act["blob_sha256"])):
            self.fold_failures.append(
                f"{where}: departure act 'blob_sha256' "
                f"must be a SHA-256, got {act['blob_sha256']!r}"
            )
            return
        if not isinstance(act["ref"], str) or not act["ref"]:
            self.fold_failures.append(
                f"{where}: departure act must carry the "
                "act reference ('ref') that ordered the "
                "accounting"
            )
            return
        self.departed[run_id] = act

    @property
    def open_quarantine(self) -> dict[str, set[str]]:
        """run id -> the junction ids under which it
        stands quarantined (an adjudication lifting the
        quarantine closes it; the latest act governs)."""
        out: dict[str, set[str]] = {}
        for junction_id, junction in self.junctions.items():
            if junction["lifted"]:
                continue
            for run_id in junction["run_ids"]:
                out.setdefault(run_id, set()).add(junction_id)
        return out


def _v11_discover_stores(root: Path) -> list[_V11Store]:
    """The guarded stores: the settling runs store, and
    every citation store — a spec's records/ directory
    carrying a run index (run-defs v2 §1: the citing
    spec's records/ is the suite/experiment surfaces'
    store of record)."""
    stores: list[_V11Store] = []
    settling = root / RUNS_REL_DIR
    if settling.is_dir():
        stores.append(_V11Store("the settling runs store", settling))
    specs = root / "specs"
    if specs.is_dir():
        for records_dir in sorted(specs.glob("*/records")):
            if (records_dir / RUN_INDEX_NAME).is_file():
                label = (
                    "citation store "
                    + records_dir.relative_to(root).as_posix()
                )
                stores.append(_V11Store(label, records_dir))
    return stores


def _v11_header_failures(
    record: dict[str, Any], where: str
) -> list[str]:
    """Validate one run record's header under the gate's
    registered copies of run-defs v2 §3.1/§4: the
    required fields, a registered surface, the run-id
    form, the key's full component set, a registered
    determinism class, and exactly one outcome (a result
    block, or an absence block of a registered kind)."""
    failures: list[str] = []
    header = record.get("run")
    if not isinstance(header, dict):
        return [f"{where}: record carries no run header object"]
    for name in RUN_HEADER_FIELDS:
        if name not in header:
            failures.append(
                f"{where}: run header is missing field {name!r}"
            )
    surface = header.get("surface")
    if surface not in RUN_SURFACES:
        failures.append(
            f"{where}: header names unregistered surface "
            f"{surface!r}; the surfaces are {list(RUN_SURFACES)}"
        )
    run_id = header.get("run_id")
    if not isinstance(run_id, str) or not _RUN_ID_RE.match(run_id):
        failures.append(
            f"{where}: header run id {run_id!r} is not in "
            "the run-defs v2 form "
            "<surface>-<yyyymmddThhmmssZ>-<6 lowercase hex>"
        )
    elif isinstance(surface, str) and run_id.split("-", 1)[0] != surface:
        failures.append(
            f"{where}: header run id {run_id!r} belongs to "
            f"surface {run_id.split('-', 1)[0]!r}, not "
            f"{surface!r}"
        )
    key = header.get("key")
    if not isinstance(key, dict):
        failures.append(f"{where}: header key is not an object")
    else:
        for component in RUN_KEY_COMPONENTS:
            if component not in key:
                failures.append(
                    f"{where}: comparability key omits "
                    f"registered component {component!r}"
                )
        if "surface" in key and key["surface"] != surface:
            failures.append(
                f"{where}: key surface {key['surface']!r} "
                f"does not match the header surface {surface!r}"
            )
    if header.get("determinism_class") not in RUN_DETERMINISM_CLASSES:
        failures.append(
            f"{where}: determinism class "
            f"{header.get('determinism_class')!r} is not "
            f"registered; the classes are "
            f"{list(RUN_DETERMINISM_CLASSES)}"
        )
    has_result = isinstance(record.get("result"), dict)
    has_absence = isinstance(record.get("absence"), dict)
    if has_result == has_absence:
        failures.append(
            f"{where}: a run record carries exactly one "
            "outcome — a result block or an absence block"
        )
    elif has_absence:
        absence = record["absence"]
        if absence.get("kind") not in RUN_ABSENCE_KINDS:
            failures.append(
                f"{where}: absence kind "
                f"{absence.get('kind')!r} is not registered; "
                f"the kinds are {list(RUN_ABSENCE_KINDS)}"
            )
        if not isinstance(absence.get("detail"), str) or not absence.get(
            "detail"
        ):
            failures.append(
                f"{where}: absence block must carry a "
                "non-empty 'detail' string"
            )
    return failures


def _v11_checks(root: Path) -> list[Check]:
    """V11's legs. Where the run layer has not landed at
    all (no run store, no junction store, no run-produced
    artifact — a pre-Spec-089 tree, or a scratch tree
    carrying only the older chain), V11 enumerates a
    single NOT-RUN, the V10 posture toward a layer that
    did not exist yet. Once any part of the layer is
    present, every leg runs and absence is a named
    failure."""
    junctions_dir = root / RUN_JUNCTIONS_REL
    stores = _v11_discover_stores(root)
    sets_path = root / ASSIGNMENT_SETS_REL
    if not stores and not junctions_dir.is_dir() and not sets_path.is_file():
        return [
            Check(
                "V11 run-binding",
                "NOT-RUN",
                [
                    "no run layer in this tree (no run "
                    "store, no junction store, no "
                    "run-produced artifact); the layer "
                    "lands with Spec 089 S1–S4"
                ],
            )
        ]
    checks: list[Check] = []
    ledger_path = root / li.LEDGER_REL
    ledger_sha = (
        li.canonical_sha256_bytes(ledger_path.read_bytes())
        if ledger_path.is_file()
        else None
    )
    settling_store = next(
        (s for s in stores if s.dir == root / RUNS_REL_DIR), None
    )

    # -- Leg (a): producing bindings resolve. -----------------------------
    a_failures: list[str] = []
    a_checked: list[str] = []
    if sets_path.is_file():
        try:
            artifact = json.loads(sets_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
            artifact = None
            a_failures.append(
                f"the assignment-sets artifact is not readable "
                f"JSON: {exc}"
            )
        if isinstance(artifact, dict):
            binding = artifact.get("producing_run")
            if not isinstance(binding, dict) or not binding.get("run_id"):
                a_failures.append(
                    "the assignment-sets artifact carries no "
                    "producing-run binding — a regenerated "
                    "artifact with no binding and no unbound "
                    "label cannot ground a verdict (C089-7)"
                )
            else:
                run_id = binding["run_id"]
                entry = (
                    settling_store.entries.get(run_id)
                    if settling_store is not None
                    else None
                )
                if entry is None:
                    a_failures.append(
                        f"the assignment-sets artifact names "
                        f"producing run {run_id!r}, which is "
                        "not entered in the settling runs "
                        "store's index — the binding does not "
                        "resolve (C089-15a)"
                    )
                else:
                    record = (
                        settling_store.records.get(entry["record"])
                        if settling_store is not None
                        else None
                    )
                    result = (
                        record.get("result")
                        if isinstance(record, dict)
                        else None
                    )
                    if not isinstance(result, dict) or result.get(
                        "materialized"
                    ) != ASSIGNMENT_SETS_REL:
                        a_failures.append(
                            f"producing run {run_id!r} is "
                            "entered, but its record is not a "
                            "materialization record for "
                            f"{ASSIGNMENT_SETS_REL}"
                        )
                    elif result.get("artifact_sha256") != li.sha256_file(
                        sets_path
                    ):
                        a_failures.append(
                            f"producing run {run_id!r} names "
                            "artifact sha256 "
                            f"{result.get('artifact_sha256')}, "
                            "but the published artifact hashes "
                            f"{li.sha256_file(sets_path)} — "
                            "the binding names a different "
                            "artifact than the one published"
                        )
                    else:
                        a_checked.append(
                            f"assignment-sets.json → run "
                            f"{run_id} (its materialization "
                            "record names this artifact and "
                            "its current sha256)"
                        )
    elif stores:
        a_failures.append(
            "the run layer is present but the run-produced "
            f"artifact {ASSIGNMENT_SETS_REL} is missing — "
            "no binding can resolve for it"
        )
    # The generated layers' build bindings: each layer's
    # stamp names the ledger build it was derived over;
    # the binding resolves iff that build is the ledger
    # of record.
    layer_bindings = (
        (MATRIX_REL_DIR + "/matrix.json", ("as_of", "ledger_sha256")),
        (MAP_REL, ("header", "as_of", "ledger_sha256")),
        (PROGRAM_MAP_REL, ("stamp", "ledger_sha256")),
    )
    for rel, path_keys in layer_bindings:
        layer_path = root / rel
        if not layer_path.is_file() or ledger_sha is None:
            continue
        try:
            layer = json.loads(layer_path.read_text(encoding="utf-8"))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            continue  # unreadable layers are V3/V5/V10 findings
        node: Any = layer
        for key in path_keys:
            node = node.get(key) if isinstance(node, dict) else None
        if not isinstance(node, str):
            a_failures.append(
                f"{rel} carries no ledger build binding at "
                f"{'.'.join(path_keys)} — a published "
                "artifact in the guarded set with no "
                "producing build named (C089-15a)"
            )
        elif node != ledger_sha:
            a_failures.append(
                f"{rel} names ledger build {node}, which "
                f"is not the ledger of record ({ledger_sha}) "
                "— the binding does not resolve"
            )
        else:
            a_checked.append(f"{rel} → ledger build {node[:12]}…")
    # Citation records and store records carrying the
    # header format validate under the registered copies.
    header_records = 0
    for store in stores:
        for name, record in sorted(store.records.items()):
            if record is None:
                a_failures.append(
                    f"{store.label}: record file {name} is "
                    "not readable JSON"
                )
                continue
            if "run" not in record:
                continue  # a pre-spec record: leg (c) covers its entry
            header_records += 1
            a_failures.extend(
                _v11_header_failures(
                    record, f"{store.label} record {name}"
                )
            )
    if header_records:
        a_checked.append(
            f"{header_records} run record(s) carrying the "
            "run-defs v2 header validate under the gate's "
            "registered copies"
        )
    checks.append(
        Check(
            "V11 run-binding — producing bindings resolve "
            "(run-defs v2 copies)",
            "FAIL" if a_failures else "PASS",
            a_failures
            or a_checked
            or ["no producing binding stands in the guarded set"],
        )
    )

    # -- Leg (b): no quarantined citation as verdict support. -------------
    open_quarantine: dict[str, set[str]] = {}
    entered_ids: set[str] = set()
    for store in stores:
        entered_ids.update(store.entries)
        for run_id, junction_ids in store.open_quarantine.items():
            open_quarantine.setdefault(run_id, set()).update(junction_ids)
    b_failures: list[str] = []
    cited_resolved: set[str] = set()
    cited_unresolved: set[str] = set()
    files_scanned = 0
    scan_texts: list[tuple[str, str]] = []
    specs_dir = root / "specs"
    if specs_dir.is_dir():
        for records_dir in sorted(specs_dir.glob("*/records")):
            for path in sorted(records_dir.rglob("*")):
                if path.is_file() and path.name != RUN_INDEX_NAME:
                    scan_texts.append(
                        (
                            path.relative_to(root).as_posix(),
                            path.read_bytes().decode(
                                "utf-8", errors="replace"
                            ),
                        )
                    )
    for store in stores:
        for name in sorted(store.records):
            path = store.dir / name
            if path.is_file():
                scan_texts.append(
                    (
                        path.relative_to(root).as_posix(),
                        path.read_bytes().decode(
                            "utf-8", errors="replace"
                        ),
                    )
                )
    for label, text in scan_texts:
        files_scanned += 1
        for token in _RUN_TOKEN_RE.findall(text):
            if token in open_quarantine:
                b_failures.append(
                    f"{label} cites run {token}, which "
                    "stands under open unexplained "
                    f"quarantine (junction "
                    f"{sorted(open_quarantine[token])[0]}) — "
                    "a quarantined run may be cited only "
                    "as quarantined, never as verdict "
                    "support (C089-13)"
                )
            elif token in entered_ids:
                cited_resolved.add(token)
            else:
                cited_unresolved.add(token)
    b_evidence = [
        f"{files_scanned} record file(s) scanned for run "
        f"citations; {len(cited_resolved)} cited run(s) "
        "resolve to entered runs, none under quarantine"
        if not b_failures
        else f"{files_scanned} record file(s) scanned for "
        "run citations",
        f"{len(open_quarantine)} run(s) stand under open "
        "unexplained quarantine in the guarded indexes",
    ]
    if cited_unresolved:
        shown = ", ".join(sorted(cited_unresolved)[:3])
        more = (
            f" (+{len(cited_unresolved) - 3} more)"
            if len(cited_unresolved) > 3
            else ""
        )
        b_evidence.append(
            f"{len(cited_unresolved)} run-id-shaped token(s) "
            "resolve to no entered run (named in test "
            "fixtures and stage records of the machinery's "
            f"own tests): {shown}{more} — reported, not "
            "failed: the gate fails quarantined citations; "
            "a citation's existence in a store is leg (a)'s "
            "and the reviewer's office"
        )
    checks.append(
        Check(
            "V11 run-binding — no quarantined citation as "
            "verdict support",
            "FAIL" if b_failures else "PASS",
            b_failures + b_evidence if b_failures else b_evidence,
        )
    )

    # -- Leg (c): store census and index integrity. ------------------------
    c_failures: list[str] = []
    c_evidence: list[str] = []
    canonical_events: Optional[int] = None
    canonical_path = root / SETTLING_CANONICAL_REL
    if canonical_path.is_file():
        try:
            canonical = json.loads(
                canonical_path.read_text(encoding="utf-8")
            )
            canonical_events = len(canonical.get("re_derivations") or [])
        except (OSError, UnicodeDecodeError, json.JSONDecodeError):
            canonical_events = None
    for store in stores:
        c_failures.extend(store.index_failures)
        c_failures.extend(store.fold_failures)
        standing = 0
        historical = 0
        departed_count = 0
        events = 0
        entered_records: dict[str, str] = {}
        for run_id, entry in sorted(store.entries.items()):
            record_name = entry["record"]
            event_match = _EVENT_RE.match(str(entry.get("event", "")))
            if event_match:
                events += 1
                idx = int(event_match.group(1))
                if canonical_events is None or idx >= canonical_events:
                    c_failures.append(
                        f"{store.label}: entry {run_id!r} "
                        f"points at re_derivations[{idx}] of "
                        f"{SETTLING_CANONICAL_REL}, which "
                        "does not stand in that file"
                    )
                continue
            if record_name in store.records:
                standing += 1
                entered_records[record_name] = run_id
            elif (
                entry.get("legacy")
                and _COMMIT_RE.match(
                    str(entry.get("superseded_by_commit", ""))
                )
                and isinstance(entry.get("git_blob"), str)
                and entry.get("git_blob")
                and _SHA256_RE.match(str(entry.get("blob_sha256", "")))
            ):
                historical += 1
            elif run_id in store.departed:
                # The run-defs v2 form: a generation that
                # entered standing and later departed is
                # accounted by its folded departure act,
                # whose three accounting fields the fold
                # shape-checked (the entry itself is
                # immutable and carries none).
                departed_count += 1
            else:
                c_failures.append(
                    f"{store.label}: entry {run_id!r} names "
                    f"record {record_name!r}, which neither "
                    "stands in the store nor is accounted "
                    "as a superseded legacy record (a "
                    "superseding commit and the record's "
                    "blob hash named, on the entry or on a "
                    "departure act)"
                )
        # The census population is the store's run
        # records. The settling store is a dedicated run
        # store: every record file in it is a run record,
        # pre-spec ones included (their headerlessness is
        # what the legacy entry covers). A citation store
        # is a spec's general records directory: a file is
        # a run record there iff it carries the run-defs
        # v1 header — the directory's other records
        # (assessments, notes) are not run population and
        # no census covers them.
        dedicated = store.dir == root / RUNS_REL_DIR
        for name in sorted(store.records):
            record = store.records[name]
            header = (
                record.get("run") if isinstance(record, dict) else None
            )
            is_run_record = dedicated or isinstance(header, dict)
            if not is_run_record:
                continue
            if name not in entered_records:
                c_failures.append(
                    f"{store.label}: record file {name} "
                    "stands in the store with no index entry "
                    "— the index's folded census does not "
                    "cover the store (C089-17)"
                )
            elif isinstance(header, dict):
                entered_as = entered_records[name]
                if header.get("run_id") != entered_as:
                    c_failures.append(
                        f"{store.label}: record file {name} "
                        f"carries header run id "
                        f"{header.get('run_id')!r} but is "
                        f"entered as {entered_as!r}"
                    )
        c_evidence.append(
            f"{store.label}: folded census "
            f"{len(store.entries)} entries = {standing} "
            f"standing record(s) + {historical} superseded "
            f"legacy record(s) + {departed_count} departed "
            f"generation(s) accounted by departure act + "
            f"{events} canonical "
            "re-derivation event(s); every supersedes / "
            "quarantine / adjudication / departure act "
            "names run ids that resolve (the fold refuses "
            "otherwise)"
        )
    checks.append(
        Check(
            "V11 run-binding — store census and index "
            "integrity",
            "FAIL" if c_failures else "PASS",
            c_failures or c_evidence,
        )
    )

    # -- Leg (d): junction completeness. -----------------------------------
    d_failures: list[str] = []
    reports: list[dict[str, Any]] = []
    if junctions_dir.is_dir():
        for path in sorted(junctions_dir.glob("*.json")):
            try:
                report = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
                d_failures.append(
                    f"junction report {path.name} is not "
                    f"readable JSON: {exc}"
                )
                continue
            if isinstance(report, dict):
                reports.append(report)
            else:
                d_failures.append(
                    f"junction report {path.name} is not a "
                    "JSON object"
                )
    report_pairs: dict[frozenset, dict[str, Any]] = {}
    disposition_counts: Counter = Counter()
    for report in reports:
        junction_id = report.get("junction_id")
        if not isinstance(junction_id, str) or not _JUNCTION_ID_RE.match(
            junction_id
        ):
            d_failures.append(
                f"junction report names malformed junction "
                f"id {junction_id!r}"
            )
            continue
        disposition = report.get("disposition")
        disposition_counts[disposition] += 1
        if disposition not in RUN_DISPOSITIONS:
            d_failures.append(
                f"junction report {junction_id} carries "
                f"disposition {disposition!r}, which is "
                "outside the registered vocabulary "
                f"{list(RUN_DISPOSITIONS)} (C089-12)"
            )
            continue
        runs = report.get("runs")
        run_ids = (
            [r.get("run_id") for r in runs if isinstance(r, dict)]
            if isinstance(runs, list)
            else []
        )
        if len(run_ids) != 2 or not all(
            isinstance(r, str) for r in run_ids
        ):
            d_failures.append(
                f"junction report {junction_id} does not "
                "name exactly two runs by id"
            )
            continue
        report_pairs[frozenset(run_ids)] = report
    comparable_pairs = 0
    divergent_pairs = 0
    key_partial_entries = 0
    for store in stores:
        full_key_entries: dict[str, dict[str, Any]] = {}
        for run_id, entry in store.entries.items():
            key = entry.get("key") or {}
            if entry.get("legacy") or any(
                component not in key
                for component in RUN_CONSTITUTIVE_COMPONENTS
            ):
                key_partial_entries += 1
                continue
            full_key_entries[run_id] = entry
        run_ids = sorted(full_key_entries)
        for i, run_id_a in enumerate(run_ids):
            for run_id_b in run_ids[i + 1 :]:
                key_a = full_key_entries[run_id_a]["key"]
                key_b = full_key_entries[run_id_b]["key"]
                if any(
                    key_a.get(component) != key_b.get(component)
                    for component in RUN_CONSTITUTIVE_COMPONENTS
                ):
                    continue
                comparable_pairs += 1
                record_a = store.records.get(
                    full_key_entries[run_id_a]["record"]
                )
                record_b = store.records.get(
                    full_key_entries[run_id_b]["record"]
                )
                if record_a is None or record_b is None:
                    continue  # leg (c) names the missing record
                outcome_a = record_a.get(
                    "result", record_a.get("absence")
                )
                outcome_b = record_b.get(
                    "result", record_b.get("absence")
                )
                if outcome_a == outcome_b:
                    continue
                divergent_pairs += 1
                if frozenset((run_id_a, run_id_b)) not in report_pairs:
                    d_failures.append(
                        f"{store.label}: comparable runs "
                        f"{run_id_a} and {run_id_b} diverge "
                        "with no junction report naming the "
                        "pair (C089-11, C089-14)"
                    )
    for report in reports:
        if report.get("disposition") != "unexplained":
            continue
        junction_id = report.get("junction_id")
        run_ids = {
            r.get("run_id")
            for r in report.get("runs", [])
            if isinstance(r, dict)
        }
        quarantined = any(
            junction_id in store.junctions
            and run_ids <= set(store.junctions[junction_id]["run_ids"])
            for store in stores
        )
        if not quarantined:
            d_failures.append(
                f"junction report {junction_id} is "
                "unexplained, but its runs are not "
                "quarantined in any guarded index "
                "(C089-13)"
            )
    d_evidence = [
        f"{comparable_pairs} comparable pair(s) examined "
        f"across the guarded stores ({divergent_pairs} "
        "divergent); "
        f"{key_partial_entries} entered run(s) are "
        "key-partial (legacy) and pair with nothing, per "
        "run-defs v2 §7.2",
        f"junction store: {len(reports)} report(s) on "
        "file"
        + (
            " — by disposition: "
            + ", ".join(
                f"{name} {count}"
                for name, count in sorted(
                    disposition_counts.items(), key=lambda kv: str(kv[0])
                )
            )
            if reports
            else " (no junction has occurred under the "
            "machinery yet; the store comes into existence "
            "with the first filed report)"
        ),
    ]
    checks.append(
        Check(
            "V11 run-binding — junction completeness",
            "FAIL" if d_failures else "PASS",
            d_failures + d_evidence if d_failures else d_evidence,
        )
    )
    return checks


# ---------------------------------------------------------------------------
# The gate run


def _first_divergences(expected: Any, actual: Any, path: str, out: list[str],
                       limit: int = 8) -> None:
    """Enumerate the first divergences between two JSON
    structures, with paths — enough to repair from, never a
    silent 'differs'."""
    if len(out) >= limit:
        return
    if type(expected) is not type(actual):
        out.append(
            f"{path}: expected {type(expected).__name__} "
            f"{str(expected)[:80]!r}, found {type(actual).__name__} "
            f"{str(actual)[:80]!r}"
        )
        return
    if isinstance(expected, dict):
        for key in sorted(set(expected) | set(actual), key=str):
            if len(out) >= limit:
                return
            if key not in actual:
                out.append(f"{path}.{key}: missing from the artifact")
            elif key not in expected:
                out.append(f"{path}.{key}: present in the artifact, not recomputed")
            else:
                _first_divergences(expected[key], actual[key], f"{path}.{key}", out, limit)
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            out.append(
                f"{path}: recomputed {len(expected)} items, "
                f"artifact carries {len(actual)}"
            )
        for i, (e, a) in enumerate(zip(expected, actual)):
            if len(out) >= limit:
                return
            label = f"{path}[{i}]"
            if isinstance(e, dict) and "row" in e and "column" in e:
                label = f"{path}[{e['row']} × {e['column']}]"
            elif isinstance(e, dict) and "id" in e:
                label = f"{path}[{e['id']}]"
            _first_divergences(e, a, label, out, limit)
    elif expected != actual:
        out.append(f"{path}: recomputed {expected!r}, artifact carries {actual!r}")


def run_gate(
    root: Path,
    *,
    mode: str = "full",
    scope: Optional[set[str]] = None,
    candidate_matrix: Optional[Path] = None,
    candidate_map: Optional[Path] = None,
    regen: bool = False,
    intended_change: Optional[str] = None,
) -> GateReport:
    """Run the gate over the tree at ``root``. ``scope`` is
    the set of check classes to run (None = all); classes
    out of scope are enumerated NOT-RUN. Never writes."""
    root = Path(root)
    report = GateReport(root=root, mode=mode)

    def in_scope(cls: str) -> bool:
        return scope is None or cls in scope

    ledger_path = root / li.LEDGER_REL
    entries: list[dict[str, Any]] = []
    if ledger_path.is_file():
        entries = li.read_ledger(ledger_path)
    claims = [e for e in entries if e.get("kind") == "claim"]

    # -- header -------------------------------------------------------------
    validator = li.validate_ledger(root)
    ledger_sha = (
        li.canonical_sha256_bytes(ledger_path.read_bytes())
        if ledger_path.is_file()
        else "MISSING"
    )
    report.header = [
        "Ledger gate — glossa-indus chain (Spec 086, Point 4)",
        f"mode: {mode}",
        f"root: {root}",
        f"ledger: {li.LEDGER_REL} — {len(entries)} lines, "
        f"canonical sha256 {ledger_sha}",
        f"definitions: {GATE_MATRIX_DEFS_VERSION} (the gate's "
        "registered copies); ledger schema: "
        f"{li.SCHEMA_VERSION}",
        f"map definitions: {GATE_MAP_DEFS_VERSION} (the gate's "
        "registered copies)",
        "program-map definitions: "
        f"{GATE_PROGRAM_MAP_DEFS_VERSION} "
        "(the gate's registered copies)",
        f"settling semantics: {SETTLE_SEMANTICS_VERSION} (the "
        f"gate's registered copies); canonicals: "
        f"{SETTLING_CANONICAL_REL}",
        f"run definitions: {GATE_RUN_DEFS_VERSION} (the "
        "gate's registered copies)",
        "falsifier coverage: "
        f"{validator.falsifier_covered} of {validator.falsifier_total} "
        "claim entries carry a falsifier (published on every "
        "gate run, C086-5)"
        + (
            " — by population: "
            + ", ".join(
                f"{k} {c}/{t}"
                for k, (c, t) in sorted(
                    validator.falsifier_by_population.items()
                )
            )
            if validator.falsifier_by_population
            else ""
        ),
    ]

    # -- the matrix under check ----------------------------------------------
    matrix_path = candidate_matrix or (root / MATRIX_REL_DIR / "matrix.json")
    matrix: Optional[dict[str, Any]] = None
    matrix_error: Optional[str] = None
    if matrix_path.is_file():
        try:
            matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            matrix_error = f"cannot parse {matrix_path}: {exc}"
    else:
        matrix_error = f"matrix artifact not found: {matrix_path}"
    if candidate_matrix is not None:
        report.header.append(
            f"candidate matrix under check: {matrix_path} "
            "(the published artifact is not read)"
        )

    map_data: Optional[dict[str, Any]] = None
    map_error: Optional[str] = None
    committed_map = root / MAP_REL
    if candidate_map is not None:
        if candidate_map.is_file():
            try:
                map_data = json.loads(
                    candidate_map.read_text(encoding="utf-8")
                )
            except (OSError, json.JSONDecodeError) as exc:
                map_error = f"cannot parse {candidate_map}: {exc}"
        else:
            map_error = f"candidate map not found: {candidate_map}"
    elif committed_map.is_file():
        try:
            map_data = json.loads(committed_map.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            map_error = f"cannot parse {committed_map}: {exc}"

    # -- derivations (lazy: the expensive routes run once) --------------------
    _derivation: dict[str, Optional[_Derivation]] = {}

    def derivation(with_sign_block: bool) -> Optional[_Derivation]:
        key = "full" if with_sign_block else "plain"
        if key not in _derivation:
            try:
                _derivation[key] = _derive(
                    root, entries, with_sign_block=with_sign_block
                )
            except Exception as exc:  # derivation refusal = a named failure
                _derivation[key] = None
                _derivation[f"{key}_error"] = exc  # type: ignore[assignment]
        return _derivation[key]

    # -- V1 -------------------------------------------------------------------
    if in_scope("V1"):
        errors = list(validator.errors)
        report.checks.append(
            Check(
                "V1 ledger validity — pinned schema, fingerprints "
                "(spec029-phase-i-v1), D-B uniqueness, field "
                "provenance, pointers (Stage 1 validator)",
                "FAIL" if errors else "PASS",
                [f"validator error: {e}" for e in errors]
                or [
                    f"{validator.lines} lines validate against "
                    f"{li.SCHEMA_VERSION}; every fingerprint "
                    "recomputes; no duplicates"
                ],
            )
        )
        # The recorded-source-hash arm (spec.md V1's last
        # clause, extended to every entry: the Stage 1 gap).
        hash_failures: list[str] = []
        checked = 0
        for entry in entries:
            for source in entry.get("sources", []):
                checked += 1
                target = root / source["path"]
                if not target.is_file():
                    hash_failures.append(
                        f"{entry['id']}: source {source['path']} "
                        "not found"
                    )
                elif li.sha256_file(target) != source["sha256"]:
                    hash_failures.append(
                        f"{entry['id']}: recorded sha256 for "
                        f"{source['path']} does not match the "
                        "file on disk under the canonical hash"
                    )
            if entry.get("kind") == "annotation":
                sidecar = entry.get("sidecar") or {}
                if sidecar.get("path") and sidecar.get("sha256"):
                    checked += 1
                    target = root / sidecar["path"]
                    if not target.is_file():
                        hash_failures.append(
                            f"{entry['id']}: sidecar "
                            f"{sidecar['path']} not found"
                        )
                    elif li.sha256_file(target) != sidecar["sha256"]:
                        hash_failures.append(
                            f"{entry['id']}: recorded sidecar "
                            f"sha256 for {sidecar['path']} does "
                            "not match the file on disk"
                        )
        report.checks.append(
            Check(
                "V1 recorded source hashes — every sources[] and "
                "sidecar hash verifies (canonical hash)",
                "FAIL" if hash_failures else "PASS",
                hash_failures
                or [
                    f"{checked} recorded hashes verified against "
                    "the files on disk via "
                    "ledger_intake.sha256_file"
                ],
            )
        )
    else:
        report.checks.append(
            Check("V1 ledger validity", "NOT-RUN",
                  ["out of scope for this run"])
        )
        report.checks.append(
            Check("V1 recorded source hashes", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V2 -------------------------------------------------------------------
    if in_scope("V2"):
        if matrix is None:
            report.checks.append(
                Check("V2 count equivalence", "FAIL",
                      [matrix_error or "matrix unavailable"])
            )
        else:
            rows = matrix.get("rows", [])
            for label, field_name in (
                ("by status", "status"),
                ("by stage", "stage"),
                ("by population", "population"),
            ):
                recomputed = Counter(
                    str(e.get(field_name)) for e in claims
                )
                carried = Counter(str(r.get(field_name)) for r in rows)
                report.checks.append(
                    Check(
                        f"V2 count equivalence — claims {label}: "
                        "ledger == matrix",
                        "PASS" if recomputed == carried else "FAIL",
                        [
                            f"{sum(recomputed.values())} claims; "
                            + (
                                "counts equal"
                                if recomputed == carried
                                else f"ledger {dict(recomputed)} != "
                                f"matrix {dict(carried)}"
                            )
                        ],
                    )
                )
            deriv = derivation(False)
            fc_carried = (matrix.get("coverage") or {}).get(
                "falsifier_coverage"
            )
            fc_recomputed = (
                deriv.coverage["falsifier_coverage"] if deriv else None
            )
            report.checks.append(
                Check(
                    "V2 count equivalence — falsifier coverage "
                    "block: ledger == matrix",
                    "PASS"
                    if fc_recomputed is not None
                    and fc_carried == fc_recomputed
                    else "FAIL",
                    [
                        f"matrix carries {fc_carried}; recomputed "
                        f"{fc_recomputed}"
                    ],
                )
            )
            if map_data is not None:
                header = map_data.get("header", {})
                by_status = Counter(str(e.get("status")) for e in claims)
                carried_status = header.get("claims_by_status")
                report.checks.append(
                    Check(
                        "V2 count equivalence — claims by status: "
                        "ledger == map header",
                        "PASS"
                        if carried_status
                        == {k: v for k, v in by_status.items()}
                        else "FAIL",
                        [
                            f"map header carries {carried_status}",
                            f"census: {len(claims)} claims "
                            f"counted across {len(by_status)} "
                            "statuses in the map header",
                        ],
                    )
                )
            else:
                report.checks.append(
                    Check(
                        "V2 count equivalence — map header leg",
                        "NOT-RUN",
                        [
                            "no map artifact (the map is Stage "
                            "5) and no --candidate-map supplied"
                        ]
                        + ([map_error] if map_error else []),
                    )
                )
    else:
        report.checks.append(
            Check("V2 count equivalence", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V3 -------------------------------------------------------------------
    if in_scope("V3"):
        if matrix is None:
            report.checks.append(
                Check("V3 matrix recomputation", "FAIL",
                      [matrix_error or "matrix unavailable"])
            )
        else:
            deriv = derivation(True)
            if deriv is None:
                exc = _derivation.get("full_error")
                report.checks.append(
                    Check(
                        "V3 matrix recomputation — independent route",
                        "FAIL",
                        [f"the gate's recomputation refused: {exc}"],
                    )
                )
            else:
                reg_failures = list(deriv.registers.mismatches)
                cell_divs: list[str] = []
                _first_divergences(
                    deriv.cells, matrix.get("cells", []), "cells", cell_divs
                )
                report.checks.append(
                    Check(
                        "V3 matrix recomputation — cells "
                        "cell-for-cell (relation, citation ids, "
                        "derivation rule id)",
                        "FAIL" if (cell_divs or reg_failures) else "PASS",
                        [f"register mismatch: {m}" for m in reg_failures]
                        + cell_divs
                        or [
                            f"{len(deriv.cells)} cells recomputed "
                            "from the ledger by the gate's own "
                            "route; every cell equal"
                        ],
                    )
                )
                struct_divs: list[str] = []
                for key, expected in (
                    ("rows", deriv.rows),
                    ("columns", deriv.columns),
                    ("coverage", deriv.coverage),
                    ("as_of", deriv.as_of),
                    ("sign_sign_block", deriv.sign_block),
                ):
                    _first_divergences(
                        expected, matrix.get(key), key, struct_divs
                    )
                report.checks.append(
                    Check(
                        "V3 matrix recomputation — rows, columns, "
                        "coverage, as-of stamp, sign×sign block",
                        "FAIL" if struct_divs else "PASS",
                        struct_divs
                        or [
                            "rows, columns, coverage, the as-of "
                            "stamp and the sign×sign block all "
                            "equal the gate's recomputation"
                        ],
                    )
                )
    else:
        report.checks.append(
            Check("V3 matrix recomputation", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V4 -------------------------------------------------------------------
    if in_scope("V4"):
        ctx = _TieContext(root, entries)
        v4_failures: list[str] = []
        cells_checked = 0
        citations_checked = 0
        if matrix is None:
            v4_failures.append(matrix_error or "matrix unavailable")
        else:
            for cell in matrix.get("cells", []):
                cells_checked += 1
                citations_checked += max(
                    0, len(cell.get("citations") or []) - 1
                )
                for failure in _tie_failures_for_cell(ctx, cell):
                    v4_failures.append(
                        f"cell ({cell['row']} × {cell['column']}, "
                        f"{cell['relation']}, {cell.get('rule')}): "
                        f"{failure}"
                    )
        edges_checked = 0
        if map_data is not None:
            for edge in map_data.get("edges", []):
                edges_checked += 1
                citations_checked += len(edge.get("citations") or [])
                v4_failures.extend(_tie_failures_for_edge(ctx, edge))
        evidence = [
            f"{cells_checked} matrix cells and {edges_checked} "
            f"map edges checked; {citations_checked} citations "
            "required to carry their relation under T1–T4"
        ]
        if ctx.numeric_exercised:
            evidence.append(
                f"numeric arm exercised on {ctx.numeric_exercised} "
                "citation(s) carrying a measurement and a bound"
            )
        else:
            evidence.append(
                "numeric arm: 0 citations in the live population "
                "carry a measurement with a machine-readable "
                "bound (the arm is exercised on fixtures in the "
                "teeth battery)"
            )
        if map_data is not None:
            edge_rels = Counter(
                e.get("rel") for e in map_data.get("edges", [])
            )
            evidence.append(
                "map edge census: "
                + ", ".join(
                    f"{rel} {edge_rels.get(rel, 0)}"
                    for rel in RELATIONS
                )
            )
            if not edge_rels.get("constrains"):
                evidence.append(
                    "UNPROVEN on the live population: "
                    "constrains map edges — 0 live instances "
                    "(the class is empty in the artifact and "
                    "says so; its teeth are fixtures in the "
                    "battery)"
                )
        if ctx.registers.mismatches:
            v4_failures.extend(
                f"register mismatch: {m}"
                for m in ctx.registers.mismatches
            )
        report.checks.append(
            Check(
                "V4 relation-carrying citations — every citation "
                "ties under T1–T4 (incl. the numeric arm)",
                "FAIL" if v4_failures else "PASS",
                v4_failures[:40] + evidence,
            )
        )
    else:
        report.checks.append(
            Check("V4 relation-carrying citations", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V5 -------------------------------------------------------------------
    if in_scope("V5"):
        if map_data is None:
            report.checks.append(
                Check(
                    "V5 map recomputation",
                    "NOT-RUN",
                    [
                        "no map artifact (the map is Stage 5) "
                        "and no --candidate-map supplied"
                    ]
                    + ([map_error] if map_error else []),
                )
            )
        else:
            v5_failures: list[str] = []
            by_id = {e["id"]: e for e in claims}
            column_ids = {
                (c["class"], c["id"])
                for c in (matrix or {}).get("columns", [])
            }
            anchor_keys = set()
            anchors_path = root / ANCHORS_REL
            if anchors_path.is_file():
                anchor_keys = set(
                    json.loads(
                        anchors_path.read_text(encoding="utf-8")
                    ).get("anchors", {})
                )
            for element in map_data.get("elements", []):
                eid = element.get("id")
                kind = element.get("kind")
                if kind == "claim":
                    entry = by_id.get(eid)
                    if entry is None:
                        v5_failures.append(
                            f"element {eid!r}: not a ledger claim"
                        )
                        continue
                    for field_name in (
                        "statement",
                        "status",
                        "stage",
                        "population",
                    ):
                        if field_name in element and element[
                            field_name
                        ] != entry.get(field_name):
                            v5_failures.append(
                                f"element {eid!r}: embedded "
                                f"{field_name} {element[field_name]!r} "
                                f"!= ledger {entry.get(field_name)!r}"
                            )
                elif kind in COLUMN_CLASSES:
                    if (kind, eid) not in column_ids and eid not in anchor_keys:
                        v5_failures.append(
                            f"element {eid!r} ({kind}): traces to "
                            "no matrix column or anchor record"
                        )
                else:
                    v5_failures.append(
                        f"element {eid!r}: unregistered element "
                        f"kind {kind!r}"
                    )
            # The loads block deep-equals the matrix's.
            expected_loads: dict[str, dict[str, int]] = {}
            for row in (matrix or {}).get("rows", []):
                expected_loads[row["id"]] = {
                    rel: 0 for rel in RELATIONS
                }
            for cell in (matrix or {}).get("cells", []):
                if cell["row"] in expected_loads:
                    expected_loads[cell["row"]][cell["relation"]] += 1
            carried_loads = map_data.get("loads")
            if carried_loads != expected_loads:
                divs: list[str] = []
                _first_divergences(
                    expected_loads, carried_loads, "loads", divs
                )
                v5_failures.extend(divs or ["loads block differs"])
            header = map_data.get("header", {})
            stamp = (header.get("as_of") or {}).get("ledger_sha256")
            if stamp != ledger_sha:
                v5_failures.append(
                    f"map header as-of stamp names ledger "
                    f"{stamp}, current ledger is {ledger_sha} "
                    "(stale artifact, D-D)"
                )
            report.checks.append(
                Check(
                    "V5 map recomputation — elements trace, "
                    "embedded fields equal, loads block "
                    "deep-equals the matrix's",
                    "FAIL" if v5_failures else "PASS",
                    v5_failures[:40]
                    or [
                        f"{len(map_data.get('elements', []))} "
                        "elements trace to ledger ids; loads "
                        "block equal"
                    ],
                )
            )
            # The full leg (Stage 5): the whole artifact
            # recomputed by the gate's own route under its
            # registered map-defs v1 copies, section by
            # section — the V3 idiom applied to the map.
            deriv = derivation(True)
            if deriv is None:
                exc = _derivation.get("full_error")
                report.checks.append(
                    Check(
                        "V5 map recomputation — full artifact, "
                        "the gate's own route (map-defs v1 "
                        "copies)",
                        "FAIL",
                        [f"the gate's recomputation refused: {exc}"],
                    )
                )
            else:
                try:
                    shares_for_map = _anchor_shares(root)
                    expected_map, map_failures = _derive_map(
                        root, entries, claims, deriv,
                        shares_for_map, ledger_sha,
                    )
                except (OSError, json.JSONDecodeError,
                        FileNotFoundError) as exc:
                    expected_map, map_failures = None, [str(exc)]
                if expected_map is None:
                    report.checks.append(
                        Check(
                            "V5 map recomputation — full "
                            "artifact, the gate's own route "
                            "(map-defs v1 copies)",
                            "FAIL",
                            [
                                "the gate's map recomputation "
                                f"could not run: {map_failures[0]}"
                            ],
                        )
                    )
                else:
                    divs: list[str] = list(map_failures)
                    for section in (
                        "artifact", "generated_from",
                        "generated_by", "header", "elements",
                        "edges", "loads", "matrix", "system",
                        "claims", "settling",
                    ):
                        _first_divergences(
                            expected_map.get(section),
                            map_data.get(section),
                            section,
                            divs,
                            limit=6,
                        )
                    census = _map_census_lines(expected_map)
                    report.checks.append(
                        Check(
                            "V5 map recomputation — full "
                            "artifact, the gate's own route "
                            "(map-defs v1 copies)",
                            "FAIL" if divs else "PASS",
                            divs[:40] + census
                            if divs
                            else [
                                "every section of the map "
                                "artifact equals the gate's "
                                "recomputation from the ledger "
                                "(header, elements, edges, "
                                "loads, matrix, system, claims, "
                                "settling)"
                            ]
                            + census,
                        )
                    )
    else:
        report.checks.append(
            Check("V5 map recomputation", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V6 -------------------------------------------------------------------
    if in_scope("V6"):
        try:
            shares = _anchor_shares(root)
        except (OSError, json.JSONDecodeError) as exc:
            shares = None
            report.checks.append(
                Check("V6 anchor shares", "FAIL",
                      [f"cannot recompute anchor shares: {exc}"])
            )
        if shares is not None:
            v6_failures: list[str] = []
            if shares["recorded_rule_id"] != STRICT_RULE_ID:
                v6_failures.append(
                    f"anchors file records strict rule "
                    f"{shares['recorded_rule_id']!r}, the gate's "
                    f"registered copy is {STRICT_RULE_ID!r}"
                )
            if shares["recomputed_strict"] != shares["stored_strict"]:
                only_recomputed = sorted(
                    shares["recomputed_strict"] - shares["stored_strict"]
                )
                only_stored = sorted(
                    shares["stored_strict"] - shares["recomputed_strict"]
                )
                v6_failures.append(
                    f"strict set recomputation disagrees with "
                    f"the stored strict_set flags: recomputed-"
                    f"only {only_recomputed[:8]}; stored-only "
                    f"{only_stored[:8]}"
                )
            if shares["recorded_strict_count"] is not None and (
                shares["recorded_strict_count"]
                != len(shares["recomputed_strict"])
            ):
                v6_failures.append(
                    f"recorded strict_count "
                    f"{shares['recorded_strict_count']} != "
                    f"recomputed {len(shares['recomputed_strict'])}"
                )
            out_of_vocab = (
                shares["validation_statuses"] - set(shares["vocabulary"])
                - {None}
            )
            if out_of_vocab:
                v6_failures.append(
                    f"validation_status values outside the "
                    f"recorded vocabulary: {sorted(out_of_vocab)}"
                )
            share = shares["strict_share"]
            report.checks.append(
                Check(
                    "V6 anchor shares — strict set recomputes "
                    "under the recorded D-A rule "
                    f"({STRICT_RULE_ID})",
                    "FAIL" if v6_failures else "PASS",
                    v6_failures
                    or [
                        f"strict anchors: "
                        f"{len(shares['recomputed_strict'])} of "
                        f"{shares['total']}; strict share "
                        f"{share:.4f}; validated-anchor share "
                        f"(the strict share, spec.md Point 5) "
                        f"{share:.4f}; rule version as recorded: "
                        f"{shares['recorded_rule_version']}"
                    ],
                )
            )
            if map_data is not None:
                header = map_data.get("header", {})
                header_failures: list[str] = []
                for field_name in (
                    "validated_anchor_share",
                    "strict_anchor_share",
                ):
                    carried = header.get(field_name)
                    if carried is None or abs(carried - share) > 1e-6:
                        header_failures.append(
                            f"map header {field_name} = "
                            f"{carried}, recomputed {share:.6f}"
                        )
                report.checks.append(
                    Check(
                        "V6 anchor shares — map header leg",
                        "FAIL" if header_failures else "PASS",
                        header_failures
                        or [
                            "map header shares equal the "
                            "recomputation",
                            f"census: the share is computed "
                            f"over {shares['total']} register "
                            f"records, {len(shares['recomputed_strict'])} "
                            "of them strict",
                        ],
                    )
                )
            else:
                report.checks.append(
                    Check(
                        "V6 anchor shares — map header leg",
                        "NOT-RUN",
                        ["no map artifact (Stage 5) and no "
                         "--candidate-map supplied"],
                    )
                )
    else:
        report.checks.append(
            Check("V6 anchor shares", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V7 -------------------------------------------------------------------
    if regen:
        report.checks.extend(
            _regen_checks(
                root, entries, intended_change=intended_change
            )
        )
    elif in_scope("V7"):
        report.checks.append(
            Check(
                "V7 lossless regeneration",
                "NOT-RUN",
                ["runs under --regen (the push CI job runs it)"],
            )
        )
    else:
        report.checks.append(
            Check("V7 lossless regeneration", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V8 -------------------------------------------------------------------
    if in_scope("V8"):
        report.checks.extend(_v8_checks(root, entries, claims))
    else:
        report.checks.append(
            Check("V8 settling canonicals", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V9 -------------------------------------------------------------------
    if in_scope("V9"):
        report.checks.extend(_v9_checks(root))
    else:
        report.checks.append(
            Check("V9 no write path", "NOT-RUN",
                  ["out of scope for this run"])
        )

    # -- V10 ------------------------------------------------------------------
    if in_scope("V10"):
        report.checks.extend(_v10_checks(root, entries))
    else:
        report.checks.append(
            Check(
                "V10 program-map equivalence",
                "NOT-RUN",
                ["out of scope for this run"],
            )
        )

    # -- V11 ------------------------------------------------------------------
    if in_scope("V11"):
        report.checks.extend(_v11_checks(root))
    else:
        report.checks.append(
            Check(
                "V11 run-binding",
                "NOT-RUN",
                ["out of scope for this run"],
            )
        )

    return report


def _regen_checks(
    root: Path,
    entries: list[dict[str, Any]],
    *,
    intended_change: Optional[str],
) -> list[Check]:
    """V7 — hash, regenerate with the pure builders only,
    byte-compare, classify. The regeneration route is the
    generator's pure builder (that is what regeneration
    means); V3 above is the independent route."""
    from glossa_lab import matrix_generate as mg

    checks: list[Check] = []
    try:
        build = mg.build_matrix(root)
    except Exception as exc:
        return [
            Check(
                "V7 lossless regeneration — matrix",
                "FAIL",
                [f"regeneration refused: {exc}"],
            )
        ]
    fresh = {"matrix.json": build.json_bytes, "matrix.md": build.md_bytes}
    for name, data in fresh.items():
        target = root / MATRIX_REL_DIR / name
        if not target.is_file():
            checks.append(
                Check(
                    f"V7 lossless regeneration — {name}",
                    "FAIL",
                    [f"published artifact missing: {target}"],
                )
            )
            continue
        before = target.read_bytes()
        before_sha = li.canonical_sha256_bytes(before)
        after_sha = li.canonical_sha256_bytes(data)
        if before == data:
            checks.append(
                Check(
                    f"V7 lossless regeneration — {name}",
                    "PASS",
                    [
                        f"byte-identical after regeneration "
                        f"(sha256 {before_sha})"
                    ],
                )
            )
        elif intended_change:
            checks.append(
                Check(
                    f"V7 lossless regeneration — {name}",
                    "PASS",
                    [
                        f"diff classified: intended-change-named "
                        f"({intended_change}); published sha256 "
                        f"{before_sha}, regenerated {after_sha} "
                        "— republish through the gated path"
                    ],
                )
            )
        else:
            checks.append(
                Check(
                    f"V7 lossless regeneration — {name}",
                    "FAIL",
                    [
                        f"diff classified: downstream-defect — "
                        f"the published artifact is not what the "
                        f"ledger generates (published sha256 "
                        f"{before_sha}, regenerated {after_sha}); "
                        "fixed by regeneration through the gated "
                        "path, never by editing the artifact"
                    ],
                )
            )
    map_path = root / MAP_REL
    if not map_path.is_file():
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "FAIL",
                [f"published artifact missing: {map_path}"],
            )
        )
        return checks
    from glossa_lab import map_generate as mp

    try:
        map_build = mp.build_map(root)
    except Exception as exc:
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "FAIL",
                [f"regeneration refused: {exc}"],
            )
        )
        return checks
    before = map_path.read_bytes()
    before_sha = li.canonical_sha256_bytes(before)
    after_sha = li.canonical_sha256_bytes(map_build.json_bytes)
    if before == map_build.json_bytes:
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "PASS",
                [
                    f"byte-identical after regeneration "
                    f"(sha256 {before_sha})"
                ],
            )
        )
    elif intended_change:
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "PASS",
                [
                    f"diff classified: intended-change-named "
                    f"({intended_change}); published sha256 "
                    f"{before_sha}, regenerated {after_sha} "
                    "— republish through the gated path"
                ],
            )
        )
    else:
        checks.append(
            Check(
                "V7 lossless regeneration — map data",
                "FAIL",
                [
                    f"diff classified: downstream-defect — "
                    f"the published artifact is not what the "
                    f"ledger generates (published sha256 "
                    f"{before_sha}, regenerated {after_sha}); "
                    "fixed by regeneration through the gated "
                    "path, never by editing the artifact"
                ],
            )
        )
    return checks
