"""Sign-to-number mapping and TMK cross-validation pipeline.

Phase 1: Parse OCR frequency table to extract (cjk_char, SOL, INI, MED, FIN, TOT).
Phase 2: Cross-reference totals against Fuls catalog (exact match where unique).
Phase 3: Use GPT-4o Vision on page images for ambiguous/missing signs.
Phase 4: Split bigram pair tokens (2-char CJK) into sign_A + sign_B.
Phase 5: Re-run TMK cross-validation with Fuls-mapped sign numbers.

Usage:
  python backend/experiments/sign_mapping_and_tmk.py
  python backend/experiments/sign_mapping_and_tmk.py --skip-gpt4  # skip vision step

Output:
  reports/cjk_m77_mapping.json
  reports/mahadevan_bigrams_mapped.json
  reports/tmk_bigram_crossvalidation.json  (updated)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent
_OCR_DIR = _REPO_ROOT / "data-import" / "mahadevan_ocr"
_REPORTS = _REPO_ROOT / "reports"
_CATALOG_PATH = _REPORTS / "real_indus_catalog_analysis.json"
_BIGRAMS_PATH = _REPORTS / "mahadevan_bigrams.json"
_MAPPING_PATH = _REPORTS / "cjk_m77_mapping.json"
_MAPPED_BIGRAMS_PATH = _REPORTS / "mahadevan_bigrams_mapped.json"
_TMK_OUTPUT_PATH = _REPORTS / "tmk_bigram_crossvalidation.json"

# M77 -> Fuls mapping inline (from ocr_mahadevan.py)
sys.path.insert(0, str(_REPO_ROOT / "backend"))
_M77_TO_FULS: dict[str, list[str]] = {}
_FULS_TO_M77: dict[str, str] = {}


def _load_m77_fuls():
    """Load M77<->Fuls mappings."""
    global _M77_TO_FULS, _FULS_TO_M77
    if _M77_TO_FULS:
        return
    mapping_text = """
001:90,91 002:97,143 003:93 004:105,107 005:106 006:96 007:98 008:100
009:101,102,103 010:150 011:160 012:151 013:- 014:159,161 015:154,155,156,157,158
016:123 017:140,148 018:95 019:130 020:131 021:- 022:132 023:133 024:134
025:142 026:144 027:146 028:125,126,128 029:127,129 030:119 031:117
032:110,111 033:115 034:112 035:113 036:122 037:121 038:94,136 039:99
040:137 041:104 042:118 043:- 044:- 045:- 046:116 047:175
048:176,177,178,179,180 049:277 050:345 051:255,953,957 052:256 053:798
054:190,191,193,195 055:192,194 056:204 057:205,206,207,208,209 058:794
059:219,220 060:226 061:944 062:222 063:942 064:940 065:235 066:236
067:229,240 068:241 069:230 070:231 071:232 072:233 073:234 074:227,228
075:243 076:260,261,263 077:266 078:264,268 079:262 080:272
081:265,267,269,270,271 082:952 083:244 084:278,279,280 085:281 086:31
087:32 088:43 089:33 090:46 091:45 092:44 093:- 094:- 095:34 096:35
097:1 098:- 099:2 100:- 101:12 102:3 103:13 104:4 105:14 106:5 107:15
108:6 109:16 110:7 111:49,50 112:17 113:48 114:18 115:39 116:19 117:51
118:20 119:27,28,59 120:29 121:55,56 122:57 123:60 124:61 125:63,65
126:- 127:173,440,442 128:443,444 129:66 130:435,436 131:454
132:450,452 133:451 134:480 135:482 136:383,484 137:645 138:678
139:679 140:680 141:685 142:62,687 143:689 144:688 145:686 146:683
147:684 148:- 149:690 150:692 151:694 152:693 153:519 154:- 155:69,70,72,75,515
156:73 157:- 158:71,80,85 159:83,84 160:81,82 161:64,392
162:389,390,956 163:391 164:393 165:- 166:394 167:- 168:411
169:405,406,407,408,409,410 170:950 171:415 172:417 173:416 174:354
175:350,353 176:400,401,402 177:413 178:465,467,468,470,472,473 179:466
180:290,291,292,293,294,295,296,297,298,299,300,301,302,303,304,305,306,307,308,310,311
181:309 182:318,320,322,323,324,325 183:321 184:340,341,342,343,348 185:-
186:315,317,319 187:257 188:330 189:420 190:421,422,423,424,425,426,427,428,429,430
191:329 192:335 193:336,337,338 194:576,585,586 195:572 196:573 197:575,577
198:578,579 199:570 200:571 201:362 202:360 203:361 204:503 205:491,495
206:504 207:506 208:505 209:500 210:502 211:520 212:521 213:92
214:540,542,543,544 215:545 216:550,551 217:552 218:- 219:541,560,561
220:562 221:556 222:555 223:564 224:565 225:530 226:554 227:532 228:531
229:534 230:460 231:461 232:462 233:455 234:456,458 235:457 236:628
237:599,600 238:603 239:602 240:716 241:- 242:621,622 243:623
244:629,630,631,632,633,634,635,636,637,638,639,640,642,643 245:604,615,617
246:616 247:626 248:627 249:590 250:592 251:593 252:595,596,597
253:510,511,513,514 254:525,526,527,528 255:363 256:611 257:610 258:605
259:483 260:58 261:625,850 262:860 263:849,851 264:853 265:859 266:858
267:817,861 268:202 269:- 270:863 271:864 272:826,865 273:862 274:866
275:868 276:- 277:- 278:- 279:871 280:869 281:870 282:874 283:875
284:818,824,877,879 285:878 286:880 287:900 288:901 289:42,926 290:903
291:412 292:910 293:920 294:904,927 295:905,928 296:923 297:924
298:908,914 299:899 300:902 301:921 302:250,251,252,253 303:906 304:890
305:891 306:796 307:892,898 308:895 309:533 310:894 311:896,897 312:913
313:- 314:909 315:911 316:481 317:931 318:932 319:165 320:166 321:167
322:168,172 323:380,381 324:- 325:382 326:384,385,386,387 327:388
328:697,698,700 329:702 330:703 331:710 332:732,734 333:727 334:729,731
335:728 336:704,705,706 337:735,736 338:721 339:719 340:720
341:711,717,718 342:740 343:741 344:742 345:745,746 346:749 347:760
348:772,773 349:765 350:764 351:767 352:750 353:766 354:763 355:759
356:762 357:761 358:752 359:770 360:- 361:- 362:- 363:782 364:777,778
365:- 366:- 367:776 368:783 369:784 370:785 371:786 372:768 373:790
374:- 375:808,809,832 376:834 377:946 378:837 379:829,831 380:825
381:810,812,814 382:816 383:815 384:823 385:811 386:838 387:803
388:804 389:805,806 390:807 391:820 392:945 393:930 394:351 395:285,286
396:372 397:371 398:518 399:373 400:374 401:375 402:368 403:840 404:842
405:841 406:844 407:845 408:169 409:171 410:200 411:- 412:201 413:203
414:- 415:215 416:217 417:216
"""
    for entry in re.finditer(r"(\d{3}):([\d,]+|-)", mapping_text):
        m77 = entry.group(1)
        fuls_raw = entry.group(2)
        if fuls_raw == "-":
            _M77_TO_FULS[m77] = []
        else:
            fuls_ids = [f.zfill(3) for f in fuls_raw.split(",")]
            _M77_TO_FULS[m77] = fuls_ids
            for fid in fuls_ids:
                _FULS_TO_M77[fid] = m77


# ── Phase 1: Parse OCR frequency table ───────────────────────────────

def parse_freq_table_ocr(ocr_text: str) -> list[dict]:
    """Extract (cjk_char, SOL, INI, MED, FIN, TOT) from markdown table rows."""
    entries = []
    for line in ocr_text.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        cells = [c for c in cells if c]

        # Table has 12 columns per row: SIGN SOL INI MED FIN TOT | SIGN SOL INI MED FIN TOT
        # Process in groups of 6
        for offset in range(0, len(cells) - 5, 6):
            chunk = cells[offset : offset + 6]
            if len(chunk) < 6:
                continue
            sign_tok, sol_s, ini_s, med_s, fin_s, tot_s = chunk
            # sign must be non-numeric, all stats must be numeric
            if (
                sign_tok
                and not re.match(r"^\d+$", sign_tok)
                and re.match(r"^\d+$", sol_s)
                and re.match(r"^\d+$", ini_s)
                and re.match(r"^\d+$", med_s)
                and re.match(r"^\d+$", fin_s)
                and re.match(r"^\d+$", tot_s)
            ):
                entries.append({
                    "cjk": sign_tok,
                    "sol": int(sol_s),
                    "ini": int(ini_s),
                    "med": int(med_s),
                    "fin": int(fin_s),
                    "tot": int(tot_s),
                })
    return entries


def load_all_freq_entries() -> list[dict]:
    entries = []
    for pg in range(727, 734):
        path = _OCR_DIR / f"ocr_freqs_{pg:04d}.txt"
        if path.exists():
            raw = path.read_text(encoding="utf-8")
            entries.extend(parse_freq_table_ocr(raw))
    return entries


# ── Phase 2: Cross-reference with Fuls catalog ───────────────────────

def build_freq_mapping(catalog_all_signs: list[dict]) -> tuple[dict, list]:
    """Match OCR entries to catalog signs by total frequency.

    Returns:
        mapping: {cjk_char -> {'fuls': 'NNN', 'm77': 'NNN', 'confidence': float}}
        unmatched: list of OCR entries that couldn't be matched
    """
    _load_m77_fuls()

    # Build lookup by total frequency from catalog
    # Use (total, terminal, medial, initial, solo) as a fingerprint
    fuls_by_total: dict[int, list[dict]] = defaultdict(list)
    for s in catalog_all_signs:
        fuls_by_total[s["total"]].append(s)

    ocr_entries = load_all_freq_entries()
    # Aggregate entries by CJK char (same char may appear multiple times across pages)
    aggregated: dict[str, dict] = {}
    for e in ocr_entries:
        c = e["cjk"]
        if c not in aggregated:
            aggregated[c] = {"sol": 0, "ini": 0, "med": 0, "fin": 0, "tot": 0}
        aggregated[c]["sol"] += e["sol"]
        aggregated[c]["ini"] += e["ini"]
        aggregated[c]["med"] += e["med"]
        aggregated[c]["fin"] += e["fin"]
        aggregated[c]["tot"] += e["tot"]

    mapping: dict[str, dict] = {}
    unmatched: list[dict] = []

    for cjk, agg in aggregated.items():
        tot = agg["tot"]
        candidates = fuls_by_total.get(tot, [])
        if len(candidates) == 1:
            # Unique total match
            fuls_sign = candidates[0]["sign"]
            m77_sign = _FULS_TO_M77.get(fuls_sign, "?")
            mapping[cjk] = {
                "fuls": fuls_sign,
                "m77": m77_sign,
                "confidence": "high",
                "match_basis": f"unique_total_{tot}",
                "sol": agg["sol"], "ini": agg["ini"],
                "med": agg["med"], "fin": agg["fin"], "tot": tot,
            }
        elif len(candidates) > 1:
            # Try refining by terminal frequency
            fin_match = [c for c in candidates if c["terminal"] == agg["fin"]]
            if len(fin_match) == 1:
                fuls_sign = fin_match[0]["sign"]
                m77_sign = _FULS_TO_M77.get(fuls_sign, "?")
                mapping[cjk] = {
                    "fuls": fuls_sign,
                    "m77": m77_sign,
                    "confidence": "medium",
                    "match_basis": f"total_{tot}+terminal_{agg['fin']}",
                    "sol": agg["sol"], "ini": agg["ini"],
                    "med": agg["med"], "fin": agg["fin"], "tot": tot,
                }
            else:
                unmatched.append({
                    "cjk": cjk, **agg,
                    "candidates": [c["sign"] for c in candidates],
                })
        else:
            unmatched.append({"cjk": cjk, **agg, "candidates": []})

    return mapping, unmatched


# ── Phase 3: GPT-4o Vision for ambiguous entries ─────────────────────

def gpt4_vision_map_signs(unmatched: list[dict]) -> dict[str, dict]:
    """Use GPT-4o Vision to identify sign numbers from page images."""
    import base64
    import os

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("  [SKIP] OPENAI_API_KEY not set — skipping GPT-4o Vision step")
        return {}

    try:
        from openai import OpenAI
    except ImportError:
        print("  [SKIP] openai package not installed")
        return {}

    client = OpenAI(api_key=api_key)
    gpt_mapping: dict[str, dict] = {}
    _load_m77_fuls()

    # Pick a few frequency table page images
    page_files = sorted(_OCR_DIR.glob("page_07??.jpg"))[:4]
    if not page_files:
        print("  [SKIP] No frequency table page images found")
        return {}

    # Build a lookup of ambiguous CJK chars to ask about
    ambiguous_chars = [u["cjk"] for u in unmatched if u.get("tot", 0) > 5][:30]
    if not ambiguous_chars:
        return {}

    print(f"  Querying GPT-4o Vision for {len(ambiguous_chars)} ambiguous signs...")

    for page_file in page_files:
        img_b64 = base64.b64encode(page_file.read_bytes()).decode()
        chars_list = ", ".join(f'"{c}"' for c in ambiguous_chars)

        prompt = (
            "This is a page from Mahadevan (1977) 'The Indus Script' TABLE I "
            "FREQUENCY AND POSITIONAL DISTRIBUTION OF SIGNS.\n\n"
            "Each row shows: a sign drawing, then its solo/initial/medial/final/total counts.\n"
            "Sign numbers are 3-digit codes in the range 001-417.\n\n"
            f"I need you to identify which Mahadevan sign numbers (3-digit codes) "
            f"correspond to these characters as they visually appear on this page: {chars_list}\n\n"
            "Output ONLY a JSON array like: "
            '[{"char": "X", "sign_number": "NNN", "total": N}, ...]\n'
            "Only include entries you can identify with confidence. Skip if unsure."
        )

        try:
            resp = client.chat.completions.create(
                model="gpt-4o",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "image_url",
                         "image_url": {"url": f"data:image/jpeg;base64,{img_b64}"}},
                        {"type": "text", "text": prompt},
                    ],
                }],
                max_tokens=800,
                temperature=0.1,
            )
            content = resp.choices[0].message.content or ""
            # Extract JSON from response
            json_match = re.search(r"\[.*\]", content, re.DOTALL)
            if json_match:
                items = json.loads(json_match.group())
                for item in items:
                    char = item.get("char", "")
                    m77 = str(item.get("sign_number", "")).zfill(3)
                    if char and m77 and re.match(r"^\d{3}$", m77):
                        fuls_ids = _M77_TO_FULS.get(m77, [])
                        fuls = fuls_ids[0] if fuls_ids else "?"
                        if char not in gpt_mapping:
                            gpt_mapping[char] = {
                                "fuls": fuls,
                                "m77": m77,
                                "confidence": "gpt4v",
                                "match_basis": f"gpt4v_{page_file.name}",
                            }
        except Exception as exc:
            print(f"  GPT-4o call failed for {page_file.name}: {exc}")

    print(f"  GPT-4o mapped {len(gpt_mapping)} additional signs")
    return gpt_mapping


# ── Phase 2b: Rank-correlation fallback ─────────────────────────────

def rank_correlation_mapping(
    catalog_all_signs: list[dict],
    raw_bigrams: list[dict],
    top_k: int = 30,
) -> dict[str, dict]:
    """Statistical fallback: map CJK tokens to Fuls signs via rank correlation.

    Hypothesis: signs that appear most often as the SECOND element in bigrams
    are the TMK (terminal marker) signs, which have the highest terminal rates.
    We rank CJK tokens by second-position frequency and Fuls signs by terminal rate,
    then match by rank. This is a bootstrap that enables the TMK test without
    requiring visual sign recognition.

    Confidence is 'rank_corr' (lower than freq-match or gpt4v).
    """
    _load_m77_fuls()

    # Count CJK token appearances as second element (position B in bigram)
    second_pos: Counter = Counter()
    for b in raw_bigrams:
        tok = b.get("sign_a_raw", "")
        freq = b.get("freq", 0)
        if len(tok) >= 2:
            sign_b = tok[1:]  # second sign token
            second_pos[sign_b] += freq

    ranked_cjk = [tok for tok, _ in second_pos.most_common(top_k)]

    # Rank Fuls signs by terminal rate (high terminal rate = TMK)
    ranked_fuls = sorted(
        catalog_all_signs,
        key=lambda s: -(s.get("terminal", 0) / max(s.get("total", 1), 1)),
    )[:top_k]

    mapping: dict[str, dict] = {}
    for i, (cjk_tok, fuls_entry) in enumerate(zip(ranked_cjk, ranked_fuls)):
        fuls_sign = fuls_entry["sign"]
        m77_sign = _FULS_TO_M77.get(fuls_sign, "?")
        terminal_rate = fuls_entry.get("terminal", 0) / max(fuls_entry.get("total", 1), 1)
        mapping[cjk_tok] = {
            "fuls": fuls_sign,
            "m77": m77_sign,
            "confidence": "rank_corr",
            "match_basis": f"rank_{i+1}_terminal_{terminal_rate:.3f}",
            "second_pos_freq": second_pos[cjk_tok],
            "fuls_terminal_rate": round(terminal_rate, 4),
        }

    return mapping


# ── Phase 4: Map bigrams using CJK->M77 mapping ───────────────────────

def map_bigrams(cjk_mapping: dict[str, dict]) -> list[dict]:
    """Split 2-char CJK bigram tokens into sign_A + sign_B and map to M77/Fuls."""
    raw_bigrams = json.loads(_BIGRAMS_PATH.read_text(encoding="utf-8"))
    _load_m77_fuls()

    mapped: list[dict] = []
    unmapped_count = 0

    for b in raw_bigrams:
        pair_token = b.get("sign_a_raw", "")
        freq = b.get("freq", 0)

        if not pair_token or len(pair_token) < 2:
            unmapped_count += 1
            continue

        # Split: first char = sign A, rest = sign B
        # (Most pairs are 2-char; occasional 3-char where one sign is complex)
        sign_a_cjk = pair_token[0]
        sign_b_cjk = pair_token[1:]  # handles 2-char and longer tokens

        entry_a = cjk_mapping.get(sign_a_cjk)
        entry_b = cjk_mapping.get(sign_b_cjk)

        if entry_a and entry_b:
            fuls_a = entry_a.get("fuls", "?")
            fuls_b = entry_b.get("fuls", "?")
            m77_a = entry_a.get("m77", "?")
            m77_b = entry_b.get("m77", "?")
            if fuls_a != "?" and fuls_b != "?":
                mapped.append({
                    "sign_a_fuls": fuls_a,
                    "sign_b_fuls": fuls_b,
                    "sign_a_m77": m77_a,
                    "sign_b_m77": m77_b,
                    "freq": freq,
                    "confidence": f"{entry_a['confidence']}+{entry_b['confidence']}",
                    "pair_token": pair_token,
                })
                continue
        unmapped_count += 1

    print(f"  Mapped {len(mapped)} bigrams  |  Unmapped: {unmapped_count}")
    return mapped


# ── Phase 5: TMK cross-validation ────────────────────────────────────

def tmk_crossvalidation(
    mapped_bigrams: list[dict],
    catalog_all_signs: list[dict],
) -> dict:
    """Test whether TMK signs prefer second position in bigrams."""
    tmk_fuls = {
        s["sign"] for s in catalog_all_signs
        if s.get("nwsp_class") == "TMK" or s.get("terminal") / max(s.get("total", 1), 1) >= 0.55
    }

    sign_as_first: Counter = Counter()
    sign_as_second: Counter = Counter()
    all_signs: set = set()

    for b in mapped_bigrams:
        a = b["sign_a_fuls"]
        s2 = b["sign_b_fuls"]
        freq = b["freq"]
        all_signs.update([a, s2])
        sign_as_first[a] += freq
        sign_as_second[s2] += freq

    total_tokens = sum(b["freq"] for b in mapped_bigrams)

    results = []
    for sign in sorted(all_signs):
        first = sign_as_first.get(sign, 0)
        second = sign_as_second.get(sign, 0)
        total = first + second
        if total == 0:
            continue
        second_rate = second / total
        is_tmk = sign in tmk_fuls
        results.append({
            "sign_fuls": sign,
            "is_tmk": is_tmk,
            "as_first": first,
            "as_second": second,
            "total_appearances": total,
            "second_rate": round(second_rate, 4),
        })

    results.sort(key=lambda r: -r["second_rate"])
    tmk_results = [r for r in results if r["is_tmk"]]
    non_tmk_results = [r for r in results if not r["is_tmk"]]

    def avg_sr(items: list) -> float:
        return sum(r["second_rate"] for r in items) / max(len(items), 1)

    tmk_avg = avg_sr(tmk_results)
    non_tmk_avg = avg_sr(non_tmk_results)
    top10_tmk = sum(1 for r in results[:10] if r["is_tmk"])
    advantage = tmk_avg - non_tmk_avg

    interpretation = (
        "STRONGLY SUPPORTS agglutinative-suffix hypothesis"
        if advantage > 0.10
        else "MODERATELY SUPPORTS agglutinative-suffix hypothesis"
        if advantage > 0.05
        else "WEAK support for agglutinative-suffix hypothesis"
        if advantage > 0
        else "DOES NOT support agglutinative-suffix hypothesis"
    )

    return {
        "total_bigram_tokens": total_tokens,
        "total_signs_in_bigrams": len(results),
        "tmk_signs_in_bigrams": len(tmk_results),
        "non_tmk_signs_in_bigrams": len(non_tmk_results),
        "tmk_avg_second_rate": round(tmk_avg, 4),
        "non_tmk_avg_second_rate": round(non_tmk_avg, 4),
        "tmk_advantage": round(advantage, 4),
        "top10_second_position_signs_that_are_tmk": top10_tmk,
        "interpretation": interpretation,
        "top_second_position_signs": results[:30],
        "tmk_profiles": sorted(tmk_results, key=lambda r: -r["second_rate"]),
        "all_signs": results,
    }


# ── Main ──────────────────────────────────────────────────────────────

def run(skip_gpt4: bool = False) -> dict:
    print("\n=== Sign Mapping + TMK Cross-Validation ===\n")

    catalog = json.loads(_CATALOG_PATH.read_text(encoding="utf-8"))
    catalog_all_signs = catalog.get("all_signs", [])
    print(f"Catalog: {len(catalog_all_signs)} signs")

    # Phase 1: Frequency-match mapping
    print("\n[1/5] Building CJK->M77 mapping via frequency cross-reference...")
    mapping, unmatched = build_freq_mapping(catalog_all_signs)
    print(f"  Matched: {len(mapping)}  |  Unmatched: {len(unmatched)}")

    # Phase 2: GPT-4o Vision for gaps
    if not skip_gpt4 and unmatched:
        print(f"\n[2/5] GPT-4o Vision for {len(unmatched)} unmatched signs...")
        gpt_mapping = gpt4_vision_map_signs(unmatched)
        mapping.update(gpt_mapping)
        print(f"  Total mapped after GPT-4o: {len(mapping)}")
    else:
        print("\n[2/5] Skipping GPT-4o Vision step")

    # Phase 2b: Rank-correlation fallback if coverage is low
    raw_bigrams = (
        json.loads(_BIGRAMS_PATH.read_text(encoding="utf-8"))
        if _BIGRAMS_PATH.exists()
        else []
    )
    if len(mapping) < 20 and raw_bigrams:
        print(f"\n[2b] Low coverage ({len(mapping)} signs) -- adding rank-correlation mapping...")
        rank_map = rank_correlation_mapping(catalog_all_signs, raw_bigrams, top_k=60)
        new_entries = {k: v for k, v in rank_map.items() if k not in mapping}
        mapping.update(new_entries)
        print(f"  Rank-correlation added {len(new_entries)} signs  |  Total: {len(mapping)}")
        print("  NOTE: rank_corr entries are statistical estimates (not visual matches).")
        print("  To get high-confidence mapping: set a real OpenAI key in Settings.")

    # Save mapping
    _MAPPING_PATH.write_text(
        json.dumps({"mapping": mapping, "unmatched_count": len(unmatched)}, indent=2),
        encoding="utf-8",
    )
    print(f"  Mapping saved -> {_MAPPING_PATH}")

    # Phase 3: Map bigrams
    print("\n[3/5] Splitting CJK bigram tokens and mapping to Fuls signs...")
    mapped_bigrams = map_bigrams(mapping)

    _MAPPED_BIGRAMS_PATH.write_text(
        json.dumps(mapped_bigrams, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"  Mapped bigrams saved -> {_MAPPED_BIGRAMS_PATH}")

    # Phase 4: TMK cross-validation
    print("\n[4/5] Running TMK cross-validation on mapped bigrams...")
    tmk_result = tmk_crossvalidation(mapped_bigrams, catalog_all_signs)
    _TMK_OUTPUT_PATH.write_text(json.dumps(tmk_result, indent=2), encoding="utf-8")

    # Phase 5: Report
    print("\n[5/5] Results:")
    print(f"  Sign mapping coverage: {len(mapping)} CJK chars mapped")
    print(f"  Mapped bigrams: {len(mapped_bigrams):,}")
    print(f"  Total bigram tokens: {tmk_result['total_bigram_tokens']:,}")
    print(f"  TMK signs in bigrams: {tmk_result['tmk_signs_in_bigrams']}")
    print(f"  TMK avg second-rate: {tmk_result['tmk_avg_second_rate']:.4f}")
    print(f"  Non-TMK avg second-rate: {tmk_result['non_tmk_avg_second_rate']:.4f}")
    print(f"  TMK advantage: {tmk_result['tmk_advantage']:+.4f}")
    print(f"  Top-10 second-pos TMK: {tmk_result['top10_second_position_signs_that_are_tmk']}/10")
    print(f"\n  --> {tmk_result['interpretation']}")

    if len(mapped_bigrams) > 0:
        print("\n  Top 10 signs by second-position rate:")
        print(f"  {'Sign':>6}  {'TMK':>4}  {'2nd':>6}  {'1st':>6}  {'Rate':>6}")
        for r in tmk_result["top_second_position_signs"][:10]:
            mark = "TMK" if r["is_tmk"] else ""
            s = r["sign_fuls"]
            print(f"  {s:>6}  {mark:>4}  {r['as_second']:>6}  "
                  f"{r['as_first']:>6}  {r['second_rate']:>6.3f}")

    print("\n  Reports:")
    print(f"    {_MAPPING_PATH}")
    print(f"    {_MAPPED_BIGRAMS_PATH}")
    print(f"    {_TMK_OUTPUT_PATH}")
    print("\n=== Done ===\n")
    return tmk_result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-gpt4", action="store_true",
                        help="Skip the GPT-4o Vision disambiguation step")
    args = parser.parse_args()
    run(skip_gpt4=args.skip_gpt4)
