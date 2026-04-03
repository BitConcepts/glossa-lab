"""Mistral Pixtral OCR pipeline for Mahadevan (1977) and CISI corpora.

Uses Mistral's pixtral-12b vision model to extract sign sequences and
frequency tables from scanned pages of:
  - The Indus Script: Texts, Concordance and Tables (Mahadevan 1977)
  - Corpus of Indus Seals and Inscriptions Vol. 1 (India) / Vol. 2 (Pakistan)

Available on Internet Archive (public domain):
  https://archive.org/details/TheIndusScript.TextConcordanceAndTablesIravathanMahadevan

Priority targets:
  1. Pages 39-162:  "Texts in the Indus Script" - actual sign sequences
  2. Pages 724-745: Table II - Pairwise Combinations (BIGRAM FREQUENCIES)
  3. Pages 717-723: Table I  - Frequency and Positional Distribution
  4. Pages 746-775: Tables III-V - Site / Object type distributions

Usage:
  # Set API key as environment variable first:
  $env:MISTRAL_API_KEY = "your-key-here"

  python ocr_mahadevan.py --target tables    # OCR bigram/frequency tables
  python ocr_mahadevan.py --target texts     # OCR inscription sequences
  python ocr_mahadevan.py --target all       # Both (slow, ~300 pages)
  python ocr_mahadevan.py --page 724         # Single page test
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import time
from functools import lru_cache
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────
_BASE    = Path(__file__).parent
_BACKEND = _BASE / "backend"
if str(_BACKEND) not in sys.path:
    sys.path.insert(0, str(_BACKEND))
_OUTDIR  = _BASE / "data-import" / "mahadevan_ocr"
_OUTDIR.mkdir(parents=True, exist_ok=True)

OUTPUT_BIGRAMS  = _BASE / "reports" / "mahadevan_bigrams.json"
OUTPUT_TEXTS    = _BASE / "reports" / "mahadevan_texts.json"
OUTPUT_FREQS    = _BASE / "reports" / "mahadevan_frequencies.json"

MODEL_NAME = "pixtral-12b-2409"


@lru_cache(maxsize=1)
def get_model_pacer():
    from glossa_lab.ai_pacing import AIModelPacer, ModelLimit

    return AIModelPacer({
        MODEL_NAME: ModelLimit(
            rpm_limit=int(os.environ.get("MISTRAL_PIXTRAL_RPM_LIMIT", "60")),
            tpm_limit=int(os.environ.get("MISTRAL_PIXTRAL_TPM_LIMIT", "120000")),
            utilization_target=float(os.environ.get("AI_UTILIZATION_TARGET", "0.70")),
            max_concurrency=int(os.environ.get("MISTRAL_PIXTRAL_MAX_CONCURRENCY", "2")),
        )
    })

# ── Archive.org URLs ──────────────────────────────────────────────────
_ITEM_ID   = "TheIndusScript.TextConcordanceAndTablesIravathanMahadevan"
_BOOK_NAME = "The%20Indus%20Script.%20Text%2C%20Concordance%20and%20Tables%20-Iravathan%20Mahadevan"
_BASE_URL  = f"https://archive.org/download/{_ITEM_ID}/{_BOOK_NAME}_jp2"

def page_url(n: int) -> str:
    """Return the Archive.org JP2 URL for page n."""
    return f"{_BASE_URL}/{_BOOK_NAME}_{n:04d}.jp2"

# Page ranges for each target section
PAGE_RANGES = {
    "texts":        range(39,  163),   # Actual inscription sign sequences
    "concordance":  range(163, 717),   # Concordance index (less useful for sequences)
    "freq_table":   range(717, 724),   # Table I: Frequency + Positional Distribution
    "bigram_table": range(724, 746),   # Table II: Pairwise Combinations (BIGRAMS!)
    "site_tables":  range(746, 781),   # Tables III-V: Site/Object/Field distributions
}

# ── Prompts tuned for each section ────────────────────────────────────

PROMPT_TEXTS = """This is a page from Mahadevan's
'The Indus Script: Texts, Concordance and Tables' (1977).

You are looking at the 'TEXTS IN THE INDUS SCRIPT' section.
Each Indus inscription is shown as a sequence of sign drawings followed by a reference number.
Below or beside each inscription, there may be 3-digit sign numbers separated by dashes or spaces.

YOUR TASK: Extract all inscription reference numbers and their sign number sequences.

Output format (one per line):
REF:NNNN SIGNS:nnn-nnn-nnn-nnn

For example:
REF:1001 SIGNS:342-099-336
REF:1002 SIGNS:059-099

If you see 3-digit numbers that look like sign codes (001-417 range for Mahadevan),
extract them. Ignore any numbers outside this range (page numbers, dates, etc.).

Return ONLY the inscription data in the format above. No headers or explanations."""

PROMPT_BIGRAMS = """This is a page from the TABLE II 'FREQUENCY OF PAIRWISE COMBINATIONS' section of
Mahadevan (1977) 'The Indus Script: Texts, Concordance and Tables'.

This table shows how often each pair of adjacent signs (sign A followed immediately by sign B)
appears in the corpus. Sign numbers are 3-digit codes in the range 001-417.

YOUR TASK: Extract ALL sign pairs and their frequencies from this page.

Output format (one per line):
PAIR:nnn-nnn FREQ:N

For example:
PAIR:342-099 FREQ:87
PAIR:059-342 FREQ:156

Extract every row in the table. Sign numbers are in the range 001-417.
Frequencies are positive integers.

Return ONLY the pair data in the format above. Nothing else."""

PROMPT_FREQ_TABLE = """This is a page from TABLE I
'FREQUENCY AND POSITIONAL DISTRIBUTION OF SIGNS' section of
Mahadevan (1977) 'The Indus Script'.

This table shows for each sign (3-digit code 001-417):
- Total frequency in the corpus
- How often it appears at the BEGINNING of inscriptions
- How often it appears at the END of inscriptions
- How often it appears in the MIDDLE of inscriptions
- How often it appears ALONE (solo inscription)

YOUR TASK: Extract all sign statistics from this page.

Output format (one per line):
SIGN:nnn TOTAL:N BEGIN:N END:N MID:N SOLO:N

Return ONLY the data rows. No headers or explanations."""

PROMPT_SITE_TABLE = """This is a page from Mahadevan (1977) showing distribution of signs by site
(Mohenjodaro, Harappa, etc.) or by object type (seal, tablet, etc.).

Extract all sign numbers and their counts per site/type.

Output format:
SIGN:nnn SITE:name COUNT:N

Or for object types:
SIGN:nnn TYPE:name COUNT:N

Return only the data rows."""


# ── Mistral OCR client ─────────────────────────────────────────────────

def get_client():
    """Initialize Mistral client."""
    from mistralai.client import Mistral
    key = os.environ.get("MISTRAL_API_KEY")
    if not key:
        raise ValueError(
            "Set MISTRAL_API_KEY environment variable first.\n"
            "In PowerShell: $env:MISTRAL_API_KEY = 'your-key'"
        )
    return Mistral(api_key=key)


def download_page_image(page_num: int) -> bytes | None:
    """Download a JP2 page image from Archive.org."""
    import urllib.request
    url = page_url(page_num)
    cache_path = _OUTDIR / f"page_{page_num:04d}.jp2"

    if cache_path.exists():
        return cache_path.read_bytes()

    print(f"    Downloading page {page_num}...", end=" ", flush=True)
    try:
        with urllib.request.urlopen(url, timeout=30) as resp:
            data = resp.read()
        cache_path.write_bytes(data)
        print(f"OK ({len(data)//1024}KB)")
        return data
    except Exception as e:
        print(f"FAILED: {e}")
        return None


def ocr_page(client, page_num: int, prompt: str, section: str) -> str | None:
    """Send a page image to Mistral Pixtral and return the transcription."""
    # Check cache
    cache_path = _OUTDIR / f"ocr_{section}_{page_num:04d}.txt"
    if cache_path.exists():
        print(f"    [cached] page {page_num}")
        return cache_path.read_text(encoding="utf-8")

    img_data = download_page_image(page_num)
    if img_data is None:
        return None

    # Convert JP2 to base64
    b64 = base64.b64encode(img_data).decode("utf-8")
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jp2;base64,{b64}"},
                },
                {"type": "text", "text": prompt},
            ],
        }
    ]
    pacer = get_model_pacer()
    reserved_tokens = pacer.estimate_request_tokens(
        model=MODEL_NAME,
        messages=messages,
        max_output_tokens=4096,
    )

    print(f"    OCR page {page_num}...", end=" ", flush=True)
    for attempt in range(6):
        pacer.acquire(MODEL_NAME, reserved_tokens)
        try:
            response = client.chat.complete(
                model=MODEL_NAME,
                messages=messages,
                max_tokens=4096,
                temperature=0.0,
            )
            result = response.choices[0].message.content
            cache_path.write_text(result, encoding="utf-8")
            print(f"OK ({len(result)} chars)")
            return result
        except Exception as e:
            if not pacer.is_rate_limit_error(e) or attempt == 5:
                print(f"FAILED: {e}")
                return None
            delay = pacer.on_rate_limit(MODEL_NAME, e, attempt)
            print(f"RATE-LIMIT ({delay:.1f}s backoff)", end=" ", flush=True)
            time.sleep(delay)
        finally:
            pacer.release(MODEL_NAME)


# ── Result parsers ────────────────────────────────────────────────────

def parse_bigrams(ocr_text: str) -> list[dict]:
    """Parse 'PAIR:nnn-nnn FREQ:N' lines from OCR output."""
    results = []
    for line in ocr_text.splitlines():
        m = re.search(r'PAIR:(\d{3})-(\d{3})\s+FREQ:(\d+)', line)
        if m:
            a, b, freq = m.group(1), m.group(2), int(m.group(3))
            if 1 <= int(a) <= 417 and 1 <= int(b) <= 417:
                results.append({"sign_a_m77": a, "sign_b_m77": b, "freq": freq})
    return results


def parse_inscription_texts(ocr_text: str) -> list[dict]:
    """Parse 'REF:NNNN SIGNS:nnn-nnn-nnn' lines from OCR output."""
    results = []
    for line in ocr_text.splitlines():
        m = re.search(r'REF:(\d+)\s+SIGNS:([\d-]+)', line)
        if m:
            ref = m.group(1)
            signs_raw = m.group(2)
            signs = [s for s in signs_raw.split("-") if re.match(r'^\d{3}$', s)
                     and 1 <= int(s) <= 417]
            if len(signs) >= 1:
                results.append({"ref": ref, "signs_m77": signs, "length": len(signs)})
    return results


def parse_freq_table(ocr_text: str) -> list[dict]:
    """Parse 'SIGN:nnn TOTAL:N BEGIN:N END:N MID:N SOLO:N' lines."""
    results = []
    for line in ocr_text.splitlines():
        m = re.search(
            r'SIGN:(\d{3})\s+TOTAL:(\d+)\s+BEGIN:(\d+)\s+END:(\d+)\s+MID:(\d+)\s+SOLO:(\d+)',
            line
        )
        if m:
            sign = m.group(1)
            if 1 <= int(sign) <= 417:
                results.append({
                    "sign_m77":  sign,
                    "total":     int(m.group(2)),
                    "beginning": int(m.group(3)),
                    "ending":    int(m.group(4)),
                    "medial":    int(m.group(5)),
                    "solo":      int(m.group(6)),
                })
    return results


# ── M77 to Fuls conversion ─────────────────────────────────────────────

def load_m77_to_fuls_mapping() -> dict[str, list[str]]:
    """Load the M77->Fuls sign number mapping from the Catalog."""
    # Inline the mapping extracted from Fuls (2023) Chapter 2.4
    # Format: m77_number -> [fuls_id, ...]
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
    mapping: dict[str, list[str]] = {}
    for entry in re.finditer(r'(\d{3}):([\d,]+|-)', mapping_text):
        m77 = entry.group(1)
        fuls_raw = entry.group(2)
        if fuls_raw == "-":
            mapping[m77] = []
        else:
            mapping[m77] = [f.zfill(3) for f in fuls_raw.split(",")]
    return mapping


def convert_signs_m77_to_fuls(
    signs_m77: list[str],
    mapping: dict[str, list[str]],
) -> list[str]:
    """Convert a list of M77 sign numbers to Fuls sign numbers.
    When a M77 sign maps to multiple Fuls signs, use the first one.
    """
    result = []
    for s in signs_m77:
        fuls = mapping.get(s, [])
        if fuls:
            result.append(fuls[0])  # use primary Fuls sign number
        # else: unmapped sign, skip
    return result


# ── Main runner ────────────────────────────────────────────────────────

def run_ocr(target: str = "tables", max_pages: int | None = None,
            api_key: str | None = None) -> dict:
    """Run OCR on the target section and save results."""
    if api_key:
        os.environ["MISTRAL_API_KEY"] = api_key

    client = get_client()
    m77_to_fuls = load_m77_to_fuls_mapping()

    results: dict = {}

    if target in ("tables", "all"):
        # ── Table II: Bigrams (22 pages, highest value) ────────────────
        print(f"\n[Bigram Table] Pages {PAGE_RANGES['bigram_table'].start}-"
              f"{PAGE_RANGES['bigram_table'].stop - 1}")
        bigrams_all: list[dict] = []
        pages = list(PAGE_RANGES["bigram_table"])
        if max_pages:
            pages = pages[:max_pages]
        for pg in pages:
            raw = ocr_page(client, pg, PROMPT_BIGRAMS, "bigrams")
            if raw:
                parsed = parse_bigrams(raw)
                print(f"      Extracted {len(parsed)} bigrams from page {pg}")
                bigrams_all.extend(parsed)

        # Convert M77 to Fuls and deduplicate
        bigrams_fuls: dict[tuple, int] = {}
        for b in bigrams_all:
            fa = m77_to_fuls.get(b["sign_a_m77"], [])
            fb = m77_to_fuls.get(b["sign_b_m77"], [])
            if fa and fb:
                key = (fa[0], fb[0])
                bigrams_fuls[key] = bigrams_fuls.get(key, 0) + b["freq"]

        bigrams_out = [
            {"sign_a_fuls": a, "sign_b_fuls": b, "freq": f,
             "significance": "extracted by Mistral OCR from Mahadevan (1977) Table II"}
            for (a, b), f in sorted(bigrams_fuls.items(), key=lambda x: -x[1])
        ]
        results["bigrams"] = bigrams_out
        OUTPUT_BIGRAMS.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT_BIGRAMS.write_text(json.dumps(bigrams_out, indent=2), encoding="utf-8")
        print(f"\n  Saved {len(bigrams_out)} unique bigrams -> {OUTPUT_BIGRAMS}")

        # ── Table I: Frequencies ───────────────────────────────────────
        print(f"\n[Frequency Table] Pages {PAGE_RANGES['freq_table'].start}-"
              f"{PAGE_RANGES['freq_table'].stop - 1}")
        freqs_all: list[dict] = []
        for pg in PAGE_RANGES["freq_table"]:
            raw = ocr_page(client, pg, PROMPT_FREQ_TABLE, "freqs")
            if raw:
                parsed = parse_freq_table(raw)
                print(f"      Extracted {len(parsed)} sign entries from page {pg}")
                freqs_all.extend(parsed)

        # Convert M77 to Fuls
        freqs_fuls = []
        for entry in freqs_all:
            fuls_ids = m77_to_fuls.get(entry["sign_m77"], [])
            if fuls_ids:
                entry["sign_fuls"] = fuls_ids[0]
                freqs_fuls.append(entry)

        results["frequencies"] = freqs_fuls
        OUTPUT_FREQS.write_text(json.dumps(freqs_fuls, indent=2), encoding="utf-8")
        print(f"  Saved {len(freqs_fuls)} sign frequency entries -> {OUTPUT_FREQS}")

    if target in ("texts", "all"):
        # ── Inscription Texts (124 pages) ──────────────────────────────
        print(f"\n[Inscription Texts] Pages {PAGE_RANGES['texts'].start}-"
              f"{PAGE_RANGES['texts'].stop - 1}")
        texts_all: list[dict] = []
        pages = list(PAGE_RANGES["texts"])
        if max_pages:
            pages = pages[:max_pages]
        for pg in pages:
            raw = ocr_page(client, pg, PROMPT_TEXTS, "texts")
            if raw:
                parsed = parse_inscription_texts(raw)
                print(f"      Extracted {len(parsed)} inscriptions from page {pg}")
                # Convert M77 to Fuls
                for insc in parsed:
                    insc["signs_fuls"] = convert_signs_m77_to_fuls(
                        insc["signs_m77"], m77_to_fuls
                    )
                texts_all.extend(parsed)

        results["inscriptions"] = texts_all
        OUTPUT_TEXTS.write_text(json.dumps(texts_all, indent=2), encoding="utf-8")
        print(f"  Saved {len(texts_all)} inscriptions -> {OUTPUT_TEXTS}")

    return results


# ── CLI ───────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Mistral Pixtral OCR for Mahadevan (1977) Indus corpus"
    )
    parser.add_argument(
        "--target", choices=["tables", "texts", "all"], default="tables",
        help="tables=bigrams+freqs only (22 pages); texts=inscriptions (124 pages)"
    )
    parser.add_argument(
        "--page", type=int, default=None,
        help="OCR a single specific page for testing"
    )
    parser.add_argument(
        "--max-pages", type=int, default=None,
        help="Limit number of pages to process (for testing)"
    )
    parser.add_argument(
        "--api-key", type=str, default=None,
        help="Mistral API key (or set MISTRAL_API_KEY env var)"
    )
    args = parser.parse_args()

    if args.page:
        # Single page test
        if args.api_key:
            os.environ["MISTRAL_API_KEY"] = args.api_key
        client = get_client()
        # Determine which section this page is in
        section = "texts"
        prompt = PROMPT_TEXTS
        if args.page in PAGE_RANGES["bigram_table"]:
            section, prompt = "bigrams", PROMPT_BIGRAMS
        elif args.page in PAGE_RANGES["freq_table"]:
            section, prompt = "freqs", PROMPT_FREQ_TABLE

        print(f"Testing page {args.page} (section: {section})")
        result = ocr_page(client, args.page, prompt, section)
        if result:
            print("\n--- OCR RESULT ---")
            print(result[:2000])
            print("\n--- PARSED ---")
            if section == "bigrams":
                print(parse_bigrams(result)[:10])
            elif section == "texts":
                print(parse_inscription_texts(result)[:5])
            elif section == "freqs":
                print(parse_freq_table(result)[:10])
    else:
        run_ocr(
            target=args.target,
            max_pages=args.max_pages,
            api_key=args.api_key,
        )


if __name__ == "__main__":
    main()
