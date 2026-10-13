#!/usr/bin/env python3
"""Regenerate drafts-review.md (and the README index table) from drafts.json.

The JSON file is the single source of the draft texts. Run after any edit:

    python3 build_review.py

The script rewrites drafts-review.md in full and replaces the marked index
block in README.md. It never touches drafts.json or any live record.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

KIND_TITLES = {
    "extracted_claim": "Extracted claims (canonical store, post-Phase-I)",
    "study_headline_claim": "Study headline claims",
    "registered_prediction": "Registered predictions with recorded partial checks",
}
KIND_ORDER = ["extracted_claim", "study_headline_claim", "registered_prediction"]


def load():
    with open(HERE / "drafts.json") as f:
        return json.load(f)


def index_table(doc):
    lines = [
        "| Claim | Stage today | One-line gist |",
        "|---|---|---|",
    ]
    for d in doc["drafts"]:
        lines.append(
            "| `{}` | {} | {} |".format(d["claim_id"], d["stage"], d["gist"]))
    return "\n".join(lines)


def review_md(doc):
    out = []
    out.append("# Lane-2 drafts — readable copy")
    out.append("")
    out.append(
        "**DRAFT — AI-drafted 2026-10-13, unauthored, no stage effect.** "
        "This file is generated from `drafts.json` by `build_review.py`; edit "
        "the JSON and re-run the script rather than editing this file. The "
        "status that governs these drafts is stated in `README.md`.")
    out.append("")
    out.append("## Index")
    out.append("")
    out.append(index_table(doc))
    out.append("")
    for kind in KIND_ORDER:
        group = [d for d in doc["drafts"] if d["record_kind"] == kind]
        if not group:
            continue
        out.append("## " + KIND_TITLES[kind])
        out.append("")
        for d in group:
            er = d["explanation_record"]
            out.append("### `{}`".format(d["claim_id"]))
            out.append("")
            out.append("- **Stage today:** {} · **Recorded status/verdict:** {}"
                       .format(d["stage"], d["lane1_status"]))
            if d.get("verified_unexplained"):
                out.append("- **Flag:** verified but unexplained "
                           "(checked, with no authored explanation on record)")
            out.append("- **Source record:** {}".format(d["source_record"]))
            if d.get("evidence_instances"):
                out.append("- **Evidence instances (same proposition, merged "
                           "in Phase I):** " + ", ".join(
                               "`{}`".format(i) for i in d["evidence_instances"]))
            out.append("")
            out.append("**The claim, in plain words**")
            out.append("")
            out.append(d["claim_plain"])
            out.append("")
            out.append("**Explanation draft** *(would become the explanation "
                       "record's artifact text on human authorship; the record "
                       "fields `author`, `artifact_uri`, `content_hash` and "
                       "`challenge_venue` are empty in the draft on purpose — "
                       "only the authoring human can complete them)*")
            out.append("")
            out.append(er["explanation_text"])
            out.append("")
            out.append("**What remains not understood — draft for the "
                       "`not_understood` field**")
            out.append("")
            out.append(d["not_understood"])
            out.append("")
            out.append("**Evidence on the record:** " + "; ".join(
                "`{}`".format(r) for r in d["evidence_refs"]))
            out.append("")
    return "\n".join(out).rstrip() + "\n"


def main():
    doc = load()
    (HERE / "drafts-review.md").write_text(review_md(doc))
    readme_path = HERE / "README.md"
    readme = readme_path.read_text()
    begin = "<!-- BEGIN GENERATED INDEX -->"
    end = "<!-- END GENERATED INDEX -->"
    if begin in readme and end in readme:
        head, rest = readme.split(begin, 1)
        _, tail = rest.split(end, 1)
        readme = (head + begin + "\n\n" + index_table(doc) + "\n\n" + end + tail)
        readme_path.write_text(readme)
    print("drafts-review.md regenerated; README index refreshed ({} drafts)"
          .format(len(doc["drafts"])))


if __name__ == "__main__":
    main()
