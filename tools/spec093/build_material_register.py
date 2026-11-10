#!/usr/bin/env python3
"""Spec 093 Stage 1 — T102 material normalization register builder.

Applies the register's rules (stated in this file and serialized
into the register artifact) to every distinct raw `material`
value in the pinned corpus snapshot and writes the register:
vocabulary, rules, the disposition of every distinct value,
and the disposition counts.

Usage: python3 build_material_register.py <repo-root> <out.json>

The rules are the register. The disposition table is generated
by them, never hand-written; the companion checker
(check_material_register.py) re-applies the rules from the
register artifact itself and fails on any divergence.

Disposition kinds:
  class        — the value names exactly one material class
  composite    — the value names two or more classes (its
                 component materials, as a set)
  alternatives — a single-component value joining classes
                 with 'or' (the cataloguer's alternatives,
                 not a composite)
  non-material — the value names no material (date, period,
                 excavation-context, technique-only, or
                 medium-only strings), with a reason code
  unmapped     — no rule fires; every such value is named in
                 the register with its reason (EXPECTED_UNMAPPED
                 below is part of the frozen rules: the builder
                 fails if the unmapped set differs from it)
"""
import collections
import json
import os
import re
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------- vocabulary
# (class id, [keyword regexes]) — matched case-insensitively with
# word boundaries added by the matcher. Order is the masking
# priority for overlapping spans (longest match wins within a
# span conflict; see match_classes).
CLASSES = [
    ("steatite", ["steatite", "soapstone", "clinoenstatite", "talc"]),
    ("faience", ["faience"]),
    ("frit", ["frit", "egyptian blue"]),
    ("terracotta", ["terracotta", "earthenware"]),
    ("ceramic", ["ceramic", "pottery", "stoneware", "porcelain",
                 "stonepaste", "buffware"]),
    ("clay-unfired", ["un-baked", "unbaked", "unfired", "mud"]),
    ("clay", ["clay", "kaolin"]),
    ("agalmatolite", ["agalmatolite"]),
    ("chert", ["chert", "flint"]),
    ("quartzite", ["quartzite"]),
    ("quartz", ["quartz", "rock crystal"]),
    ("chalcedony", ["chalcedony", "plasma"]),
    ("agate", ["agate"]),
    ("carnelian", ["carnelian", "sard"]),
    ("onyx", ["onyx", "sardonyx", "nicolo"]),
    ("jasper", ["jasper", "bloodstone", "blood stone", "heliotrope"]),
    ("lapis-lazuli", ["lapis lazuli", "lapis-lazuli", "lazuli",
                      "lazurite"]),
    ("turquoise", ["turquoise"]),
    ("amazonite", ["amazonite"]),
    ("feldspar", ["feldspar", "albite"]),
    ("amphibole", ["amphibole"]),
    ("apatite", ["apatite"]),
    ("aragonite", ["aragonite"]),
    ("azurite", ["azurite"]),
    ("magnesite", ["magnesite"]),
    ("obsidian", ["obsidian"]),
    ("tuff", ["tuff"]),
    ("amethyst", ["amethyst"]),
    ("garnet", ["garnet"]),
    ("beryl", ["beryl", "emerald", "emeralds"]),
    ("corundum", ["ruby", "rubies", "sapphire"]),
    ("diamond", ["diamond", "diamonds"]),
    ("pearl", ["mother of pearl", "pearl"]),
    ("iron-oxide", ["hematite", "haematite", "haemaetite", "goethite",
                    "limonite", "magnetite", "menaccanite", "ochre"]),
    ("malachite", ["malachite"]),
    ("rhodochrosite", ["rhodochrosite"]),
    ("jade", ["jadeite", "nephrite", "jade"]),
    ("limestone", ["limestone"]),
    ("marble", ["marble"]),
    ("alabaster", ["alabaster"]),
    ("gypsum", ["plaster of paris", "gypsum"]),
    ("plaster", ["plaster", "stucco"]),
    ("calcite", ["calcite"]),
    ("travertine", ["travertine"]),
    ("serpentine", ["serpentine", "serpentinite", "marmolite",
                    "chrysotite", "chrysotile"]),
    ("chlorite", ["chlorite"]),
    ("schist", ["schist"]),
    ("slate", ["slate"]),
    ("shale", ["shale"]),
    ("basalt", ["basalt", "basanite", "diabase", "lapis lacedemonius"]),
    ("diorite", ["diorite", "metadiorite"]),
    ("granite", ["granite"]),
    ("porphyry", ["porphyry"]),
    ("conglomerate", ["conglomerate"]),
    ("siltstone", ["siltstone"]),
    ("sandstone", ["sandstone"]),
    ("stone-unspecified", ["stone", "greenstone", "lithic"]),
    ("sand", ["sand"]),
    ("mica", ["mica"]),
    ("chalk", ["chalk"]),
    ("bone", ["bone"]),
    ("ivory", ["ivory"]),
    ("shell", ["shell"]),
    ("tooth", ["tooth", "teeth"]),
    ("horn", ["horn"]),
    ("coral", ["coral"]),
    ("jet", ["jet"]),
    ("copper-alloy", ["copper alloy", "copper/bronze", "copper-bronze",
                      "copper-nickel alloy"]),
    ("copper", ["copper", "electrotype", "elecrotype"]),
    ("bronze", ["bronze"]),
    ("brass", ["brass", "latten"]),
    ("metal-unspecified", ["metal"]),
    ("steel", ["steel"]),
    ("iron", ["iron"]),
    ("silver", ["silver"]),
    ("gold", ["gold"]),
    ("electrum", ["electrum"]),
    ("lead", ["lead"]),
    ("pewter", ["pewter"]),
    ("glass", ["glass", "paste"]),
    ("enamel", ["enamel"]),
    ("paper", ["paper", "papier mache"]),
    ("parchment", ["parchment"]),
    ("leather-skin", ["leather", "hide", "sealskin", "seal gut",
                      "shagreen", "skin"]),
    ("wood", ["wood", "boxwood", "ebony", "teakwood", "rosewood",
              "walnut", "bamboo"]),
    ("plant-material", ["birch bark", "bark", "gourd", "maize",
                        "wicker"]),
    ("textile", ["linen", "cotton", "silk", "wool", "lambswool",
                 "cloth", "gauze", "thread", "cord", "fiber", "fibre",
                 "hemp", "rope", "string", "satin"]),
    ("wax", ["wax"]),
    ("lacquer", ["lacquer", "lacquered"]),
    ("bitumen", ["bitumen", "bituminous", "bitumenous", "asphaltum",
                 "grahamite"]),
    ("resin", ["resin", "mastic"]),
    ("modern-synthetic", ["sculpey", "plastic", "plasticine", "latex"]),
]

SURFACE_MEDIA = ["paint", "painted", "pigment", "ink", "slip", "glaze",
                 "glazed", "gilt", "gilded", "gilding", "whitewash",
                 "gesso", "tempera", "gouache", "watercolor", "pastel",
                 "graphite", "wash"]

# Technique phrases masked before class matching (print/drawing
# techniques are not materials). A value left with no class and
# only function words after masking is non-material (NM-TECH).
TECHNIQUE_PREMASKS = [
    "commercial color lithograph", "commercial process",
    "color lithograph", "salted paper print", "paper negative",
    "glass negative", "wood engraving", "woodblock print",
    "woodblock", "woodcut", "hand-colored", "hand-coloured",
    "lithograph", "engraving", "etching", "drypoint", "aquatint",
]

RESIDUAL_STOPWORDS = {
    "on", "of", "the", "a", "an", "from", "with", "and", "or", "in",
    "state", "proof", "first", "second", "third", "fourth", "only",
    "five", "four", "three", "two", "delteil", "chine", "collé",
    "colle", "surimono", "album", "prints", "print", "book",
    "mounted", "part", "triptych", "color", "colour", "some",
}

# Non-material whole-value patterns, checked in order.
NONMATERIAL_PATTERNS = [
    ("NM-DATE", re.compile(
        r"^[\s(\[]*(ca\.\s*)?-?\d[\d\s\-–]*(bce|ce)?[\s).\]\"]*$", re.I),
     "date or period string, not a material"),
    ("NM-PERIOD", re.compile(r"^period\b", re.I),
     "period label string, not a material"),
    ("NM-EXCAV", re.compile(
        r"\b(level|dump|test pit|surface find)\b|^(tb|ta)\b"
        r"|^[a-z]{1,3}-?\d{1,3}$", re.I),
     "excavation-context or code string, not a material"),
    ("NM-FRAGMENT", re.compile(r"^fragment\.?$", re.I),
     "fragment marker, no material named"),
]

UNCERTAIN_MARKERS = ["(?)", "(uncertain)", "?", "possibly", "probably",
                     "probable"]

# The frozen unmapped set: values no rule may disposition, each
# with its reason. The builder fails if computation disagrees.
EXPECTED_UNMAPPED = {
    " Iraq": "provenience fragment (place name) in the source data, "
             "leading space as recorded; not a material",
    " Restaurants 141": "unexplained string in the source data, "
                        "leading space as recorded; names no material",
    "Almondstone": "unresolvable stone trade name; no class assigned",
    "Andean": "geographic/cultural label, not a material",
    "Angami": "cultural label (a people of Nagaland), not a material",
    "Ao": "uninterpretable two-letter string; names no material",
    "Arctic Culture Area": "cultural-area label, not a material",
    "Assyrian": "cultural label, not a material",
    "Caribbean": "geographic label, not a material",
    "Central American": "geographic label, not a material",
    "Department of Magdalena": "geographic label, not a material",
    "Eskimo": "cultural label in the source's terms, not a material",
    "Galley": "object-form word (a tray), not a material",
    "Indian": "geographic/cultural label, not a material",
    "Indian,Hindu": "geographic/cultural labels, not a material",
    "Indian,Miri": "geographic/cultural labels, not a material",
    "Indian,Miri (uncertain)": "geographic/cultural labels, not a material",
    "India,Haryana,Rakhi Ghari": "provenience string (place names), not a material",
    "Iraq,Tepe Gawra": "provenience string (place names), not a material",
    "Kourion": "place name, not a material",
    "Magnetic Grains": "unspecified mineral grains; no class named",
    "North America,United States of America,Alaska,Lower Yukon River Valley,Kaiyuh Slough,Khotol River,Old Fish Camp":
        "provenience string (place names), not a material",
    "Rayy": "place name, not a material",
    "Thailand,Udon Thani,Ban Kham Phakkood": "provenience string (place names), not a material",
    "Thailand,Udon Thani,Ban Kham Phakkood,Ban Kham Ta Na": "provenience string (place names), not a material",
}

CLASS_PATTERNS = [
    (cid, [re.compile(r"\b" + re.escape(kw) + r"\b", re.I) for kw in kws])
    for cid, kws in CLASSES
]
SURFACE_PATTERNS = [re.compile(r"\b" + w + r"\b", re.I)
                    for w in SURFACE_MEDIA]
PREMASK_PATTERNS = [re.compile(re.escape(p), re.I)
                    for p in TECHNIQUE_PREMASKS]


def clean(value):
    return re.sub(r"\s+", " ", value.replace("\n", " ")).strip()


def match_classes(text):
    """Greedy longest-span keyword matching; returns class id set."""
    spans = []
    for cid, pats in CLASS_PATTERNS:
        for pat in pats:
            for m in pat.finditer(text):
                spans.append((m.start(), m.end(), cid))
    spans.sort(key=lambda s: (-(s[1] - s[0]), s[0]))
    taken = []
    classes = set()
    for a, b, cid in spans:
        if any(a < tb and b > ta for ta, tb in taken):
            continue
        taken.append((a, b))
        classes.add(cid)
    return classes


def disposition(raw_value):
    text = clean(raw_value)
    low = text.lower()
    uncertain = any(mk in low for mk in UNCERTAIN_MARKERS)
    for code, pat, reason in NONMATERIAL_PATTERNS:
        if pat.search(text):
            return {"kind": "non-material", "classes": [],
                    "surface_media": [], "uncertain": uncertain,
                    "reason_code": code, "reason": reason}
    # parenthetical handling: variety gloss + firing markers
    paren_contents = re.findall(r"\(([^)]*)\)", text)
    pre_classes = set()
    suppress = set()
    clay_unfired_marker = any(
        any(w in pc.lower() for w in ("unfired", "un-baked", "unbaked"))
        for pc in paren_contents)
    if any("carnelian" in pc.lower() for pc in paren_contents) and \
            re.fullmatch(r"chalcedony\s*(\([^)]*\))?", low):
        # A parenthetical variety gloss replaces the family head:
        # 'Chalcedony (carnelian)' is catalogued as carnelian.
        pre_classes.add("carnelian")
        suppress.add("chalcedony")
    text_noparen = re.sub(r"\([^)]*\)", " ", text)
    # technique pre-masking
    premask_hits = 0
    residual = text_noparen
    for pat in PREMASK_PATTERNS:
        residual, n = pat.subn(" ", residual)
        premask_hits += n
    classes = (match_classes(residual) | pre_classes) - suppress
    # Surface media are read from the full value, parenthetical
    # qualifiers included ('Steatite (glazed)' carries the glaze).
    surface = sorted({w for w, pat in zip(SURFACE_MEDIA, SURFACE_PATTERNS)
                      if pat.search(text)})
    # clay family: unfired evidence collapses clay+clay-unfired
    if "clay" in classes and "clay-unfired" in classes:
        classes.discard("clay")
    if "clay" in classes and clay_unfired_marker:
        classes.discard("clay")
        classes.add("clay-unfired")
    if not classes:
        if surface:
            return {"kind": "non-material", "classes": [],
                    "surface_media": surface, "uncertain": uncertain,
                    "reason_code": "NM-MEDIUM",
                    "reason": "surface or drawing medium only; "
                              "no substrate material named"}
        words = {w.strip(";,.:") for w in residual.lower().split()
                 if w.strip(";,.:")}
        if premask_hits and words <= RESIDUAL_STOPWORDS:
            return {"kind": "non-material", "classes": [],
                    "surface_media": surface, "uncertain": uncertain,
                    "reason_code": "NM-TECH",
                    "reason": "print or drawing technique only; "
                              "not a material"}
        return {"kind": "unmapped", "classes": [], "surface_media": surface,
                "uncertain": uncertain, "reason_code": None,
                "reason": EXPECTED_UNMAPPED.get(raw_value)}
    components = [c.strip() for c in text_noparen.split(",")]
    kind = "class" if len(classes) == 1 else "composite"
    if len(components) == 1 and " or " in (" " + components[0].lower() + " "):
        kind = "alternatives"
        uncertain = True
    return {"kind": kind, "classes": sorted(classes),
            "surface_media": surface, "uncertain": uncertain,
            "reason_code": None, "reason": None}


def main():
    root = Path(sys.argv[1])
    out_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
    summary_only = out_path is None
    snap = [json.loads(l) for l in
            open(root / "glossa-corpus/indus/exports/indus_research.jsonl",
                 encoding="utf-8") if l.strip()]
    counts = collections.Counter(
        r["material"] for r in snap
        if r["material"] not in (None, "", "None"))
    table = {}
    for value, n in sorted(counts.items()):
        d = disposition(value)
        d["records"] = n
        table[value] = d
    unmapped = {v for v, d in table.items() if d["kind"] == "unmapped"}
    if unmapped != set(EXPECTED_UNMAPPED):
        print("UNMAPPED SET DIVERGES FROM THE FROZEN SET", file=sys.stderr)
        print("  unexpected:", sorted(unmapped - set(EXPECTED_UNMAPPED)),
              file=sys.stderr)
        print("  missing:", sorted(set(EXPECTED_UNMAPPED) - unmapped),
              file=sys.stderr)
        sys.exit(1)
    kind_counts = collections.Counter()
    kind_records = collections.Counter()
    class_records = collections.Counter()
    for v, d in table.items():
        kind_counts[d["kind"]] += 1
        kind_records[d["kind"]] += d["records"]
        for c in d["classes"]:
            class_records[c] += d["records"]
    register = {
        "register": "material-normalization-register",
        "version": "v1",
        "spec": "093-material-context-channel",
        "stage": "Stage 1 (T102)",
        "population": "distinct raw `material` values in the pinned "
                      "corpus snapshot (glossa-corpus/indus/exports/"
                      "indus_research.jsonl, SHA-256 "
                      "08fc96c8dbc22a37effb65e789b22b144f4baf22be1da55dc3"
                      "d84db5dc44505e)",
        "rules": {
            "classes": [{"id": cid, "keywords": kws}
                        for cid, kws in CLASSES],
            "surface_media": SURFACE_MEDIA,
            "technique_premasks": TECHNIQUE_PREMASKS,
            "nonmaterial_patterns": [
                {"code": c, "regex": p.pattern, "reason": r}
                for c, p, r in NONMATERIAL_PATTERNS],
            "residual_stopwords": sorted(RESIDUAL_STOPWORDS),
            "uncertain_markers": UNCERTAIN_MARKERS,
            "notes": [
                "Matching is lexical: case-insensitive keyword match "
                "with word boundaries over the value with whitespace "
                "normalized, uncertainty markers read from the raw "
                "value, parenthetical spans removed before matching "
                "(their firing and variety glosses read first), and "
                "technique phrases masked before matching.",
                "Overlapping keyword spans resolve longest-first.",
                "clay + clay-unfired collapse to clay-unfired (the "
                "unfired evidence governs); a parenthetical unfired "
                "marker converts a plain clay match to clay-unfired.",
                "A single-component value joined by 'or' is "
                "alternatives, not composite, and is uncertain.",
                "A parenthetical variety gloss replaces the family "
                "head it glosses ('Chalcedony (carnelian)' is "
                "carnelian). Surface media are read from the full "
                "value, parenthetical qualifiers included.",
                "Surface-media keywords are recorded, never classes: "
                "a value naming only surface media is non-material "
                "(NM-MEDIUM).",
            ],
        },
        "counts": {
            "distinct_values": len(table),
            "records": sum(counts.values()),
            "values_by_kind": dict(kind_counts),
            "records_by_kind": dict(kind_records),
            "records_by_class": dict(class_records),
            "uncertain_values": sum(1 for d in table.values()
                                    if d["uncertain"]),
            "uncertain_records": sum(d["records"] for d in table.values()
                                     if d["uncertain"]),
        },
        "dispositions": table,
    }
    if summary_only:
        print(json.dumps(register["counts"], indent=1, sort_keys=True))
        for probe in ("Steatite (glazed)", "Steatite ?", "Chalcedony (carnelian)",
                      "Faience (?) or glazed steatite", "Clay (unfired)",
                      "Stone, probably chlorite", "1957\"", "Fragment.",
                      "Commercial color lithograph", "Ao",
                      "Pen and brown ink", "Etching and engraving; first state of four"):
            if probe in table:
                print("PROBE", repr(probe), "->", table[probe])
        return
    payload = json.dumps(register, indent=1, sort_keys=True)
    fd, tmp = tempfile.mkstemp(dir=str(out_path.parent),
                               suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(payload)
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, out_path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise
    print("distinct:", len(table), "| records:", sum(counts.values()))
    print("values by kind:", dict(kind_counts))
    print("records by kind:", dict(kind_records))


if __name__ == "__main__":
    main()
