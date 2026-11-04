"""Spec 088 — the generated program map (S1 builder, S4 page).

The whole-program picture of Spec 088, under the Spec 086
discipline (one source of truth, generated downstream, a
gate on drift) applied to the program itself:

- one node per ledger claim and one per study (spec
  directory), grouped by the curated taxonomy;
- every standing derived mechanically from the ledger under
  ``program-map-defs v1``
  (``glossa-indus/map/PROGRAM-MAP-DEFINITIONS.md``) — the
  builder reads the ledger, the taxonomy, and the spec
  tree's directory names, and nothing else (C2: no prose
  standings, ever);
- coverage is total, exact, and fail-closed: a duplicate,
  omissions, unknown ids, undeclared domains/subdomains,
  unregistered statuses, and in-flight emission are each a
  named refusal and nothing is written.

This module is the pure builder; the CLI wrapper is
``tools/map/generate_program_map.py``. The data artifacts
(``program-map.json``, ``program-map-finds.json``) landed
in Stage S2 and the Spec 086 gate's independent
recomputation (class V10) in Stage S3. Stage S4 (T401)
adds the third artifact, ``program-map.html``: a single
self-contained page that is exactly the registered
template below wrapped around the two data artifacts
embedded verbatim — the page computes no standing, class,
or count of its own (C088-8); its script only filters and
searches the generated fields, and the gate's V10 carries
its own copies of the template (the amendment recorded in
the S4 stage record).
"""

from __future__ import annotations

import json
from pathlib import Path

from glossa_lab.ledger_intake import sha256_file

DEFS_VERSION = "program-map-defs v1"
TAXONOMY_VERSION = "program-map-taxonomy v1"
LEDGER_SCHEMA_VERSION = "ledger-schema v1"

LEDGER_REL = "glossa-indus/ledger/claims.jsonl"
TAXONOMY_REL = "glossa-indus/map/program-map-taxonomy.json"
MAP_REL = "glossa-indus/map/program-map.json"
FINDS_REL = "glossa-indus/map/program-map-finds.json"
PAGE_REL = "glossa-indus/map/program-map.html"
SPECS_REL = "specs"

# program-map-defs v1 §4.2 — the derivation table (D-088-3).
# A machine copy of the registered table; the defs document
# is the registration of record, and the Stage 3 gate will
# carry its own copies. A status outside this table fails
# the build.
STATUS_TO_CLASS = {
    "strongly_supported": "positive",
    "contradicted": "negative",
    "unsupported": "negative",
    "partially_falsified": "negative",
    "superseded": "closed_other",
    "draft": "open",
    "untested": "open",
    "partially_supported": "open",
}

CLAIM_CLASSES = ("positive", "negative", "open", "closed_other")
STUDY_CLASSES = CLAIM_CLASSES + ("unjudged",)
IN_FLIGHT = "in_flight"

# program-map-defs v1 §7 — the registered name-only forms.
RESTRICTED_NAME_ONLY = {
    "072-fish-family-profiles-redesign": "executed — held under the Roif gate",
}

# program-map-defs v1 §8 — keys the taxonomy format must
# never carry, anywhere, at any depth (no standings by
# construction, C088-17).
FORBIDDEN_TAXONOMY_KEYS = frozenset(
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

# program-map-defs v1 §6 — the find kinds.
FIND_BUNDLE_LESS_STUDY = "bundle_less_study"
FIND_JUDGMENT_CALL = "judgment_call"
FIND_EXTRACTED_NULL_FALSIFIER = "extracted_null_falsifier"
FIND_RESTRICTED_NODE = "restricted_node"

_STANDING_TEMPLATE = (
    "Ledger standing: status {status} · stage {stage} · falsifier {falsifier}"
)

# ── The page (Stage S4, T401) ────────────────────────────────────────────────
#
# program-map.html is exactly these three registered template
# pieces wrapped around the two data artifacts embedded
# verbatim: _PAGE_HEAD + program-map.json text + _PAGE_MID +
# program-map-finds.json text + _PAGE_TAIL. The template
# carries no data of its own — every number, standing, and
# count the page shows is rendered by the page's script from
# the embedded artifacts' fields, and the script contains no
# derivation: it filters and searches generated fields only
# (C088-8). The Spec 086 gate's V10 class carries its own
# registered copies of these three pieces (the Stage 4
# amendment to V10's artifact list, recorded in the S4 stage
# record); a template change made in only one copy is the
# divergence the gate exists to catch.

_PAGE_HEAD = """<!DOCTYPE html>
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

_PAGE_MID = """</script>
<script type="application/json" id="program-map-finds">
"""

_PAGE_TAIL = """</script>
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


def _render_page(map_text: str, finds_text: str) -> str:
    """Assemble the page from the two artifacts' texts.

    The data is embedded verbatim; verbatim embedding inside
    a script element is only sound while the data cannot
    close the element, so a payload carrying a script close
    is a named refusal rather than an escaped rewrite (an
    escaped copy would no longer be the artifact).
    """
    for label, text in (("program-map.json", map_text),
                        ("program-map-finds.json", finds_text)):
        if "</script" in text.lower():
            raise ProgramMapBuildError(
                f"{label} carries a script-close sequence and "
                "cannot be embedded verbatim in the page "
                "(Stage S4 embedding guard)"
            )
    return _PAGE_HEAD + map_text + _PAGE_MID + finds_text + _PAGE_TAIL


class ProgramMapBuildError(Exception):
    """A named refusal: the generation cannot proceed as specified."""


# ── Inputs ───────────────────────────────────────────────────────────────────


def _read_ledger(root: Path) -> list[dict]:
    path = root / LEDGER_REL
    if not path.is_file():
        raise ProgramMapBuildError(f"ledger not found: {path}")
    rows: list[dict] = []
    for lineno, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ProgramMapBuildError(
                f"ledger line {lineno} is not JSON: {exc}"
            ) from exc
    return rows


def _spec_dirs(root: Path) -> list[str]:
    specs = root / SPECS_REL
    if not specs.is_dir():
        raise ProgramMapBuildError(f"spec tree not found: {specs}")
    return sorted(p.name for p in specs.iterdir() if p.is_dir())


def _walk_keys(value: object, trail: str = "$") -> list[str]:
    """Every mapping key in a parsed JSON value, with its path."""
    found: list[str] = []
    if isinstance(value, dict):
        for key, sub in value.items():
            found.append(f"{trail}.{key}")
            found.extend(_walk_keys(sub, f"{trail}.{key}"))
    elif isinstance(value, list):
        for i, sub in enumerate(value):
            found.extend(_walk_keys(sub, f"{trail}[{i}]"))
    return found


def _read_taxonomy(root: Path) -> dict:
    path = root / TAXONOMY_REL
    if not path.is_file():
        raise ProgramMapBuildError(f"taxonomy not found: {path}")
    try:
        tax = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ProgramMapBuildError(f"taxonomy is not JSON: {exc}") from exc
    if not isinstance(tax, dict):
        raise ProgramMapBuildError("taxonomy is not a JSON object")
    for key_path in _walk_keys(tax):
        key = key_path.rsplit(".", 1)[-1].split("[")[0]
        if key in FORBIDDEN_TAXONOMY_KEYS:
            raise ProgramMapBuildError(
                f"taxonomy carries the forbidden standing-shaped key "
                f"{key!r} at {key_path} (defs §8: the format carries "
                "no standings)"
            )
    if tax.get("version") != TAXONOMY_VERSION:
        raise ProgramMapBuildError(
            f"taxonomy version is {tax.get('version')!r}, expected "
            f"{TAXONOMY_VERSION!r}"
        )
    domains = tax.get("domains")
    if (
        not isinstance(domains, list)
        or not domains
        or len(set(domains)) != len(domains)
        or not all(isinstance(d, str) and d for d in domains)
    ):
        raise ProgramMapBuildError(
            "taxonomy 'domains' must be a non-empty list of unique names"
        )
    subdomains = tax.get("subdomains")
    if not isinstance(subdomains, dict) or set(subdomains) != set(domains):
        raise ProgramMapBuildError(
            "taxonomy 'subdomains' must declare exactly the domains"
        )
    for domain in domains:
        subs = subdomains[domain]
        if (
            not isinstance(subs, list)
            or not subs
            or len(set(subs)) != len(subs)
            or not all(isinstance(s, str) and s for s in subs)
        ):
            raise ProgramMapBuildError(
                f"taxonomy subdomains for {domain!r} must be a non-empty "
                "list of unique names"
            )

    def _assignments(kind: str, id_key: str) -> dict[str, dict]:
        raw = tax.get(kind)
        if not isinstance(raw, list):
            raise ProgramMapBuildError(f"taxonomy {kind!r} must be a list")
        out: dict[str, dict] = {}
        for entry in raw:
            if not isinstance(entry, dict) or set(entry) != {
                id_key,
                "domain",
                "subdomain",
            }:
                raise ProgramMapBuildError(
                    f"taxonomy {kind} entry must carry exactly "
                    f"{{{id_key}, domain, subdomain}}: {entry!r}"
                )
            ident = entry[id_key]
            if ident in out:
                raise ProgramMapBuildError(
                    f"taxonomy assigns {ident!r} more than once ({kind})"
                )
            if entry["domain"] not in domains:
                raise ProgramMapBuildError(
                    f"taxonomy assigns {ident!r} to the undeclared domain "
                    f"{entry['domain']!r}"
                )
            if entry["subdomain"] not in subdomains[entry["domain"]]:
                raise ProgramMapBuildError(
                    f"taxonomy assigns {ident!r} to "
                    f"{entry['subdomain']!r}, not declared under "
                    f"{entry['domain']!r}"
                )
            out[ident] = entry
        return out

    studies = _assignments("studies", "spec_dir")
    documents = _assignments("extracted_documents", "document")
    restricted = tax.get("restricted")
    if not isinstance(restricted, list) or not all(
        isinstance(r, str) for r in restricted
    ):
        raise ProgramMapBuildError("taxonomy 'restricted' must be a list")
    if len(set(restricted)) != len(restricted):
        raise ProgramMapBuildError("taxonomy 'restricted' has duplicates")
    for spec_dir in restricted:
        if spec_dir not in studies:
            raise ProgramMapBuildError(
                f"restricted study {spec_dir!r} has no taxonomy assignment"
            )
        if spec_dir not in RESTRICTED_NAME_ONLY:
            raise ProgramMapBuildError(
                f"restricted study {spec_dir!r} has no registered "
                "name-only form (defs §7)"
            )
    return {
        "domains": domains,
        "subdomains": subdomains,
        "studies": studies,
        "documents": documents,
        "restricted": list(restricted),
    }


# ── Derivation ───────────────────────────────────────────────────────────────


def _governing_entries(rows: list[dict]) -> list[dict]:
    """Claim entries with reclassification chains applied (defs §3)."""
    claims: dict[str, dict] = {}
    order: list[str] = []
    for row in rows:
        if row.get("kind") != "claim":
            continue
        cid = row.get("id")
        if cid in claims:
            raise ProgramMapBuildError(f"duplicate claim id in ledger: {cid}")
        claims[cid] = dict(row)
        order.append(cid)
    for row in rows:
        if row.get("kind") != "reclassification":
            continue
        target = row.get("supersedes")
        if target not in claims:
            raise ProgramMapBuildError(
                f"reclassification {row.get('id')!r} supersedes "
                f"{target!r}, which is not a claim entry"
            )
        for field in ("status", "stage"):
            if field in row:
                claims[target][field] = row[field]
    return [claims[cid] for cid in order]


def _falsifier_present(entry: dict) -> bool:
    return bool(entry.get("falsifier"))


def _derive_class(entry: dict) -> str:
    status = entry.get("status")
    if status not in STATUS_TO_CLASS:
        raise ProgramMapBuildError(
            f"claim {entry.get('id')!r} carries the unregistered status "
            f"{status!r} (defs §4.2: the derivation table is total over "
            "the registered vocabulary; anything else fails the build)"
        )
    cls = STATUS_TO_CLASS[status]
    if cls == IN_FLIGHT:
        raise ProgramMapBuildError(
            f"claim {entry.get('id')!r} derived the in_flight class, "
            "which has no derivation rule in v1 (defs §11)"
        )
    return cls


def _source_of_record(entry: dict) -> dict:
    sors = [
        s
        for s in entry.get("sources") or []
        if isinstance(s, dict) and s.get("role") == "source_of_record"
    ]
    if len(sors) != 1:
        raise ProgramMapBuildError(
            f"claim {entry.get('id')!r} has {len(sors)} source-of-record "
            "sources; exactly one is required to place it"
        )
    return sors[0]


def _roll_up(counts: dict[str, int]) -> tuple[str, bool]:
    """The defs §5 precedence. Returns (class, is_judgment_call)."""
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


# ── The build ────────────────────────────────────────────────────────────────


def _dump(obj: object) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=1, sort_keys=True) + "\n"


def build_artifacts(root: Path) -> dict[str, str]:
    """Build all three artifacts' text in memory, from the
    defs' inputs only (the page is the two data artifacts
    embedded verbatim in the registered template)."""
    rows = _read_ledger(root)
    tax = _read_taxonomy(root)
    spec_dirs = _spec_dirs(root)

    # Coverage over the taxonomy is exact and bidirectional (defs §8).
    assigned = set(tax["studies"])
    actual = set(spec_dirs)
    if assigned != actual:
        problems = []
        if actual - assigned:
            problems.append(
                f"spec directories with no assignment: "
                f"{sorted(actual - assigned)}"
            )
        if assigned - actual:
            problems.append(
                f"assignments naming no directory: "
                f"{sorted(assigned - actual)}"
            )
        raise ProgramMapBuildError("; ".join(problems))

    entries = _governing_entries(rows)
    dates = [str(r.get("date")) for r in rows if r.get("date")]
    stamp = {
        "ledger_latest_entry_date": max(dates) if dates else None,
        "ledger_lines": len(rows),
        "ledger_schema": LEDGER_SCHEMA_VERSION,
        "ledger_sha256": sha256_file(root / LEDGER_REL),
        "program_map_defs": DEFS_VERSION,
        "program_map_taxonomy": TAXONOMY_VERSION,
    }

    claim_nodes: list[dict] = []
    members: dict[str, list[str]] = {d: [] for d in spec_dirs}
    multi_spec_claims: list[str] = []
    null_falsifier_extracted: list[dict] = []
    falsifier_present_count = 0
    documents_seen: set[str] = set()

    for entry in entries:
        cls = _derive_class(entry)
        present = _falsifier_present(entry)
        if present:
            falsifier_present_count += 1
        standing = _STANDING_TEMPLATE.format(
            status=entry.get("status"),
            stage=entry.get("stage") if entry.get("stage") else "none",
            falsifier="present" if present else "absent",
        )
        node = {
            "class": cls,
            "document": None,
            "domain": None,
            "falsifier_present": present,
            "id": entry.get("id"),
            "kind": "claim",
            "population": entry.get("population"),
            "stage": entry.get("stage"),
            "standing": standing,
            "status": entry.get("status"),
            "study": None,
            "subdomain": None,
        }
        population = entry.get("population")
        if population == "bundle":
            home = _source_of_record(entry).get("spec")
            if not home or home not in actual:
                raise ProgramMapBuildError(
                    f"bundle claim {entry.get('id')!r} names the home "
                    f"study {home!r}, which is not a spec directory "
                    "(citation does not resolve)"
                )
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
            document = _source_of_record(entry).get("document_id")
            if not document or document not in tax["documents"]:
                raise ProgramMapBuildError(
                    f"extracted claim {entry.get('id')!r} names the "
                    f"source document {document!r}, which has no "
                    "taxonomy assignment"
                )
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
            raise ProgramMapBuildError(
                f"claim {entry.get('id')!r} has population "
                f"{population!r}, which has no registered assignment "
                "route in program-map-defs v1 (§4.1)"
            )
        claim_nodes.append(node)

    unassigned_documents = set(tax["documents"]) - documents_seen
    if unassigned_documents:
        raise ProgramMapBuildError(
            "taxonomy assigns extracted documents the ledger does not "
            f"carry: {sorted(unassigned_documents)}"
        )

    restricted = set(tax["restricted"])
    study_nodes: list[dict] = []
    finds: list[dict] = []
    unjudged_studies: list[str] = []
    judgment_calls: list[str] = []
    for spec_dir in spec_dirs:
        assignment = tax["studies"][spec_dir]
        if spec_dir in restricted:
            study_nodes.append(
                {
                    "class": None,
                    "domain": assignment["domain"],
                    "id": spec_dir,
                    "kind": "study",
                    "restricted": True,
                    "standing": RESTRICTED_NAME_ONLY[spec_dir],
                    "subdomain": assignment["subdomain"],
                }
            )
            finds.append({"kind": FIND_RESTRICTED_NODE, "subject": spec_dir})
            continue
        counts = {cls: 0 for cls in CLAIM_CLASSES}
        for cls in members[spec_dir]:
            counts[cls] += 1
        cls, is_judgment = _roll_up(counts)
        if cls == IN_FLIGHT:
            raise ProgramMapBuildError(
                f"study {spec_dir!r} derived the in_flight class, which "
                "has no derivation rule in v1 (defs §11)"
            )
        study_nodes.append(
            {
                "class": cls,
                "domain": assignment["domain"],
                "id": spec_dir,
                "judgment_call": is_judgment,
                "kind": "study",
                "member_counts": {**counts, "total": sum(counts.values())},
                "restricted": False,
                "subdomain": assignment["subdomain"],
            }
        )
        if cls == "unjudged":
            unjudged_studies.append(spec_dir)
            finds.append(
                {"kind": FIND_BUNDLE_LESS_STUDY, "subject": spec_dir}
            )
        if is_judgment:
            judgment_calls.append(spec_dir)
            finds.append(
                {
                    "kind": FIND_JUDGMENT_CALL,
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
                "kind": FIND_EXTRACTED_NULL_FALSIFIER,
                "subject": item["id"],
            }
        )
    finds.sort(key=lambda f: (f["kind"], f["subject"]))
    claim_nodes.sort(key=lambda n: n["id"])
    study_nodes.sort(key=lambda n: n["id"])

    # The coverage block (defs §9). Counts per domain only —
    # no cross-domain aggregate progress figure exists (C088-14).
    def _class_counts(nodes: list[dict], classes: tuple[str, ...]) -> dict:
        out = {cls: 0 for cls in classes}
        for node in nodes:
            if node["class"] in out:
                out[node["class"]] += 1
        return out

    domains_block: dict[str, dict] = {}
    for domain in tax["domains"]:
        d_claims = [n for n in claim_nodes if n["domain"] == domain]
        d_studies = [n for n in study_nodes if n["domain"] == domain]
        domains_block[domain] = {
            "claims": len(d_claims),
            "claims_by_class": _class_counts(d_claims, CLAIM_CLASSES),
            "restricted_studies": sum(
                1 for n in d_studies if n["restricted"]
            ),
            "studies": len(d_studies),
            "studies_by_class": _class_counts(d_studies, STUDY_CLASSES),
        }
    coverage = {
        "claims": {
            "by_class": _class_counts(claim_nodes, CLAIM_CLASSES),
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
            "by_class": _class_counts(study_nodes, STUDY_CLASSES),
            "restricted": len(restricted),
            "total": len(study_nodes),
        },
        "unjudged_studies": sorted(unjudged_studies),
    }

    program_map = {
        "coverage": coverage,
        "defs_version": DEFS_VERSION,
        "nodes": {"claims": claim_nodes, "studies": study_nodes},
        "stamp": stamp,
        "taxonomy_version": TAXONOMY_VERSION,
    }
    finds_doc = {
        "defs_version": DEFS_VERSION,
        "finds": finds,
        "stamp": stamp,
        "taxonomy_version": TAXONOMY_VERSION,
    }
    map_text = _dump(program_map)
    finds_text = _dump(finds_doc)
    return {
        MAP_REL: map_text,
        FINDS_REL: finds_text,
        PAGE_REL: _render_page(map_text, finds_text),
    }


def build_outputs(root: Path) -> dict[Path, str]:
    """Build the full new text of every generated artifact, in memory."""
    return {
        root / rel: text for rel, text in build_artifacts(root).items()
    }


def check_outputs(root: Path) -> list[str]:
    """Names of artifacts whose committed bytes differ from a fresh build."""
    drifted: list[str] = []
    for path, fresh in build_outputs(root).items():
        if not path.is_file() or path.read_bytes() != fresh.encode("utf-8"):
            drifted.append(str(path.relative_to(root)))
    return drifted


def write_outputs(root: Path) -> list[str]:
    """Write every artifact (all builds succeed first, or none is written)."""
    outputs = build_outputs(root)
    written: list[str] = []
    for path, text in outputs.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
        written.append(str(path.relative_to(root)))
    return written
