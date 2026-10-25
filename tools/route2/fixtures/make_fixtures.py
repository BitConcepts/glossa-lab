#!/usr/bin/env python3
"""Generate the Route 2 tooling fixtures (deterministic; re-runnable).

Writes, beside this file:
  rest_pages/page1.json, rest_pages/page2.json  - mock Firestore REST pages
  badpage/page1.json                            - a mis-shaped page 1
  fixture_records.jsonl                         - 12 handcrafted records
  fixture_expect.json                           - hand-computed census
                                                  expectations for them
  roundtrip_expect.json                         - expectations for the
                                                  census of the read
                                                  script's fixture output
"""
import json
from pathlib import Path

HERE = Path(__file__).parent
S_FIELDS = [f"S{i}" for i in range(1, 15)]


def sv(v):
    return {"stringValue": v}


def iv(v):
    return {"integerValue": str(v)}


def doc(name_id, dockey, sideline, texts, svals, extra=None):
    fields = {"dockey": iv(dockey), "sideline": sv(sideline)}
    fields["texts"] = {"arrayValue": {"values": [sv(t) for t in texts]}} if texts \
        else {"arrayValue": {}}
    for i, sf in enumerate(S_FIELDS):
        fields[sf] = sv(svals[i] if i < len(svals) else "0")
    if extra:
        fields.update(extra)
    return {"name": f"projects/theindusscript/databases/(default)"
                    f"/documents/indusarrays/{name_id}", "fields": fields}


def write(name, obj):
    (HERE / name).write_text(json.dumps(obj, indent=1), encoding="utf-8")


# --- REST pages -------------------------------------------------------------
page1 = {"documents": [
    doc("doc001", 1001, "a", ["342", "99"], ["342", "99"], {"textnum": iv(1)}),
    doc("doc002", 1002, "b", ["267", "72"], ["267", "72"]),
    doc("doc003", 1003, "a", [], ["59", "89"]),
], "nextPageToken": "tok2"}
page2 = {"documents": [
    doc("doc004", 1004, "a", ["342", "342"], ["342", "342"], {"fs80": sv("x")}),
    doc("doc005", 1005, "x", ["72", "342"], ["72", "342"]),
]}
(HERE / "rest_pages").mkdir(exist_ok=True)
write("rest_pages/page1.json", page1)
write("rest_pages/page2.json", page2)

bad = doc("bad001", 1001, "a", ["342", "99"], ["342", "99"])
del bad["fields"]["dockey"]
write("badpage/page1.json", {"documents": [bad]})

# --- Handcrafted census fixture (12 records; see run_route2_tests.py) -------
def rec(dockey, sideline, texts, svals):
    r = {}
    if dockey is not None:
        r["dockey"] = dockey
    if sideline is not None:
        r["sideline"] = sideline
    r["texts"] = texts
    for i, v in enumerate(svals):
        r[S_FIELDS[i]] = v
    return r


records = [
    rec(1001, "a", ["342", "99", "342"], ["342", "99", "342", "0"]),   # R1
    rec(1001, "a", ["342"], ["99", "87"]),                             # R2
    rec(1001, "b", ["*12", "267", "0", "72"], ["*12", "267", "0", "72"]),  # R3
    rec(1002, "a", [], ["59", "*5", "89", "0"]),                       # R4
    rec("1002", "a", ["59", "89", "328"], ["59", "89", "328"]),       # R5
    rec(1003, None, ["72"], ["72"]),                                  # R6
    rec("abc", "a", [], ["342", "*9"]),                                # R7
    rec(1004, "a", ["342", "342"], ["342", "342"]),                    # R8
    rec(1004, "a", ["99"], ["99", "99", "99"]),                        # R9
    rec(1005, "x", ["267", "99", "267", "99"], ["267", "99", "267", "99"]),  # R10
    rec(1005, "y", ["72", "342"], ["72", "342"]),                      # R11
    rec(1006, "a", ["59"], ["0", ""]),                                # R12
]
with open(HERE / "fixture_records.jsonl", "w", encoding="utf-8") as fh:
    for r in records:
        fh.write(json.dumps(r) + "\n")

# Hand-computed from the loader's rules (see test driver for the derivation):
# sequences: [342,99,342] [267,72] [59,89,328] [99,99,99] [267,99,267,99] [72,342]
write("fixture_expect.json", {
    "lines": 12, "parsed_records": 12, "unique_dockeys": 4,
    "total_sequences": 6, "total_sign_instances": 17,
    "mean_inscription_length": 2.83, "numeric_mahadevan": 25,
    "star_nnn_filtered": 3, "dockey_range": [1001, 1005],
    "top_20": [[99, 6], [342, 3], [267, 3], [72, 2], [59, 1], [89, 1], [328, 1]],
    "terminal_frac": {},
})

# Census of the read script's fixture output (5 docs, all reconstruct):
write("roundtrip_expect.json", {
    "lines": 5, "parsed_records": 5, "unique_dockeys": 5,
    "total_sequences": 5, "total_sign_instances": 10,
    "mean_inscription_length": 2.0, "numeric_mahadevan": 10,
    "star_nnn_filtered": 0, "dockey_range": [1001, 1005],
    "top_20": [[342, 4], [72, 2], [99, 1], [267, 1], [59, 1], [89, 1]],
    "terminal_frac": {},
})
print("fixtures written")
