#!/usr/bin/env python3
"""N2 charge table builder — Spec 068, gate 0.6 cited data.

Reads the committed blazon transcription
(n2_dering_blazons.csv: the Dering Roll, c. 1270-1280,
British Library, as transcribed by Brian Timms and
edited at bsswebsite.me.uk/History/Dering/dering-roll.html;
snapshot SHA-256
4cb6b0527d2fa482a092a848c0b93e88e0ae6ad3900f20a07bd6e982ce054739)
and writes the canonical charge table
(n2_dering_charges.csv) and the per-shield extraction
record (n2_dering_extraction.csv) under the frozen
counting rules of Spec 068 section 4, gate 0.6:

- the counting unit is one charge occurrence on one
  shield, as the roll records it;
- the canonical type is the head device noun: posture
  and form adjectives do not split types (lion
  passant / rampant / gardant are lion; torteau,
  bezant, plate, hurt are roundel);
- an explicit number word multiplies the device noun
  it governs (a / an = 1);
- strewn patterns are not counted (semy, crusilly,
  billetty, bezanty as a treatment): the number borne
  is indeterminate by design;
- field divisions and treatments are not charges
  (quarterly, party, per fess / pale / bend, checky,
  barry, bendy, lozengy, gironny, paly, vair, ermine,
  fretty as a field); a field division's own number
  (barry of six, gironny of eight) belongs to the
  field, never to a following charge;
- arrangement phrases are not charges (in chief, in
  pale, in fess, in saltire, in dexter chief);
- label, canton, bordure, chief count as devices;
- a fess of N fusils counts the numbered noun (fusil
  x N), not the carrier fess;
- an orle of X counts the orle once; the arranged
  charges are unnumbered in the blazon and are not
  counted (the semy situation).

Every shield's extraction was read against its blazon
at the freeze of this table (324 of 324); the shields
with no charge (field only) are named in the
extraction record with an empty charge list.
Deterministic: re-running reproduces both outputs
byte-identically.
"""
import csv, re, sys
from pathlib import Path
from collections import Counter

NUM = {"a": 1, "an": 1, "two": 2, "three": 3, "four": 4, "five": 5,
       "six": 6, "eight": 8, "nine": 9, "ten": 10, "twelve": 12}

# surface (singular/plural as blazoned) -> canonical type
DEVICES = {
    "lion": "lion", "lions": "lion",
    "leopard’s head": "leopard's head", "leopard's head": "leopard's head",
    "leopard’s heads": "leopard's head", "leopard's heads": "leopard's head",
    "boar’s head": "boar's head", "boar's head": "boar's head",
    "boar’s heads": "boar's head", "boar's heads": "boar's head",
    "bear’s head": "bear's head", "bear's head": "bear's head",
    "bear’s heads": "bear's head", "bear's heads": "bear's head",
    "stag’s head": "stag's head", "stag's head": "stag's head",
    "stag’s heads": "stag's head", "stag's heads": "stag's head",
    "hand": "hand", "hands": "hand",
    "bird": "bird", "birds": "bird",
    "eagle": "eagle", "eagles": "eagle",
    "martlet": "martlet", "martlets": "martlet",
    "raven": "raven", "ravens": "raven",
    "cock": "cock", "cocks": "cock",
    "wolf": "wolf", "wolves": "wolf",
    "hedgehog": "hedgehog", "hedgehogs": "hedgehog",
    "calf": "calf", "calves": "calf",
    "horse braies": "horse braies",
    "cross": "cross", "crosses": "cross",
    "fess": "fess", "chif": "chief", "chief": "chief",
    "bend": "bend", "bendlet": "bendlet", "bendlets": "bendlet",
    "chevron": "chevron", "chevrons": "chevron",
    "pale": "pale", "pallet": "pallet", "pallets": "pallet",
    "bar": "bar", "bars": "bar",
    "saltire": "saltire", "saltires": "saltire",
    "label": "label", "canton": "canton", "bordure": "bordure",
    "orle": "orle",
    "escutcheon": "escutcheon", "escutcheons": "escutcheon",
    "maunch": "maunch", "mallet": "mallet", "mallets": "mallet",
    "winnowing fan": "winnowing fan", "winnowing fans": "winnowing fan",
    "sun": "sun", "mullet": "mullet", "mullets": "mullet",
    "crescent": "crescent", "crescents": "crescent",
    "annulet": "annulet", "annulets": "annulet",
    "ring": "ring", "rings": "ring",
    "cinquefoil": "cinquefoil", "cinquefoils": "cinquefoil",
    "fleur de lis": "fleur de lis", "fleurs de lis": "fleur de lis",
    "lozenge": "lozenge", "lozenges": "lozenge",
    "fusil": "fusil", "fusils": "fusil",
    "escallop": "escallop", "escallops": "escallop",
    "bezant": "roundel", "bezants": "roundel",
    "plate": "roundel", "plates": "roundel",
    "torteau": "roundel", "torteaux": "roundel",
    "hurt": "roundel",
    "water bouget": "water bouget", "water bougets": "water bouget",
    "key": "key", "keys": "key",
    "buckle": "buckle", "buckles": "buckle",
    "sword": "sword",
    "dice": "die",
    "oak tree": "oak tree",
    "trumpet": "trumpet", "trumpets": "trumpet",
    "bugle horn": "bugle horn", "bugle horns": "bugle horn",
    "barbel": "barbel", "barbels": "barbel",
    "hake": "hake", "hakes": "hake",
    "pike": "pike",
    "herring": "herring", "herrings": "herring",
    "stocking": "stocking", "stockings": "stocking",
    "axe": "axe", "axes": "axe",
}

FIELD_STARTS = ("quarterly", "party", "per ", "checky", "barry", "bendy",
                "gironny", "lozengy", "paly", "vair", "vairy", "ermine",
                "fretty")

IGNORED = set("""gules or argent azure sable vert ermine vair vairy
passant rampant gardant displayed hauriant issuant crowned couped cabossed
addorsed eradicated queued double crossed upwards dexter sinister field
splendour his in on of the and a an per fess pale bend chief overall between
cantonned by with all first second each pilewise fesswise wavy indented
engrailed voided dancetty moline cotised counterchanged fretty checky
barry bendy gironny lozengy paly quarterly party semy de lis crusilly
billetty bezanty gemelles concentric""".split())


def extract(blazon: str):
    text = re.sub(r"\s+", " ", blazon.lower().replace("’", "'")).strip()
    counts = Counter()
    notes = []
    # strewn phrases: not counted (number indeterminate by design)
    text = re.sub(r"semy (de|of) [a-z ]+?(?=( a | an | two | three | four | five | six | eight | nine | ten | twelve | overall | and |$))", " ", text)
    text = text.replace("crusilly", " ").replace("billetty", " ")
    text = re.sub(r"\bbezanty\b", " ", text)
    # fess of N fusils: count the numbered noun, not the carrier
    def _fusil(m):
        counts["fusil"] += NUM[m.group(1)]
        notes.append(f"fusils-of-fess x{NUM[m.group(1)]}")
        return " "
    text = re.sub(r"a fess of (two|three|four|five|six) fusils", _fusil, text)
    # orle of X: the orle counts once; the arranged charges are unnumbered
    def _orle(m):
        counts["orle"] += 1
        notes.append("orle (arranged charges unnumbered, not counted)")
        return " "
    text = re.sub(r"orle of [a-z']+", _orle, text)
    # arrangement / division phrases whose nouns are not charges
    for phrase in ("in dexter chief", "per fess", "per pale", "per bend",
                   "in chief", "in pale", "in fess", "in saltire",
                   "per chevron"):
        text = text.replace(phrase, " zz ")
    tokens_pre = text
    # token scan with a phrase window
    tokens = re.findall(r"[a-z']+", text)
    FIELD_DIV = {"barry", "bendy", "gironny", "paly", "lozengy"}
    i = 0
    pending_num = None
    while i < len(tokens):
        tok = tokens[i]
        # field division "of N" (barry of six, gironny of eight, ...):
        # the number belongs to the field, never to a following charge
        if (tok in FIELD_DIV and i + 2 < len(tokens)
                and tokens[i + 1] == "of" and tokens[i + 2] in NUM):
            i += 3
            pending_num = None
            continue
        if tok in NUM and tok not in ("a", "an"):
            pending_num = NUM[tok]
            i += 1
            continue
        if tok in ("a", "an"):
            if pending_num is None:
                pending_num = 1
            i += 1
            continue
        # multi-word devices first
        matched = False
        for span in (3, 2):
            phrase = " ".join(tokens[i:i + span])
            if phrase in DEVICES:
                counts[DEVICES[phrase]] += pending_num or 1
                pending_num = None
                i += span
                matched = True
                break
        if matched:
            continue
        if tok in DEVICES:
            counts[DEVICES[tok]] += pending_num or 1
            pending_num = None
            i += 1
            continue
        i += 1
    return counts, notes


def main():
    import hashlib
    here = Path(__file__).resolve().parent
    rows = list(csv.DictReader(open(here / 'n2_dering_blazons.csv',
                                    newline='', encoding='utf-8')))
    assert len(rows) == 324
    total = Counter()
    extraction_rows = []
    for r in rows:
        c, notes = extract(r['blazon'])
        total.update(c)
        charges = '; '.join(f"{t} x{c[t]}" for t in sorted(c))
        extraction_rows.append([r['shield_no'], r['blazon'], charges,
                                '; '.join(notes)])
    charge_rows = [[t, total[t]] for t in
                   sorted(total, key=lambda t: (-total[t], t))]
    for name, header, data in (
        ('n2_dering_charges.csv', ['type', 'count'], charge_rows),
        ('n2_dering_extraction.csv',
         ['shield_no', 'blazon', 'charges', 'notes'], extraction_rows),
    ):
        p = here / name
        with open(p, 'w', newline='', encoding='utf-8') as fh:
            w = csv.writer(fh, lineterminator='\n')
            w.writerow(header)
            w.writerows(data)
        with open(p, newline='', encoding='utf-8') as fh:
            back = list(csv.reader(fh))
        assert back[0] == header and len(back) == len(data) + 1, name
        print(name, len(data), 'rows, sha256',
              hashlib.sha256(p.read_bytes()).hexdigest())
    print('N2: V', len(total), 'N', sum(total.values()))
    zero = [r[0] for r in extraction_rows if not r[2]]
    print('zero-charge shields (field only):', len(zero), zero)


if __name__ == "__main__":
    main()
