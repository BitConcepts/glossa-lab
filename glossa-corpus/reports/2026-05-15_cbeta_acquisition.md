# CBETA Acquisition Report

**Date:** 2026-05-15  
**Result:** 4/5 OK, 50,892 total files

## Key Finding: Why Batch 1 Failed

- We tried `cbeta-org/xml-p5a` → **WRONG**: `p5a` is the internal version under `cbeta-git` user account, not the `cbeta-org` organization
- We tried `cbeta-git/cbeta-open-data` → **WRONG**: this repo never existed

**Correct public version:** `https://github.com/cbeta-org/xml-p5`  
(the `cbeta-org` GitHub organization was only created on 2026-02-21)

## CBETA Repository Map

| Repository | Purpose | License |
|---|---|---|
| `cbeta-org/xml-p5` | Official TEI P5 (public) | CC BY-NC-SA 3.0 TW |
| `cbeta-git/xml-p5a` | Internal editing version | not public |
| `DILA-edu/cbeta-normal-text` | Plain text, 一卷一檔 | CC BY-NC-SA 3.0 TW |
| `DILA-edu/CBETA-txt` | TAF plain text (T/X/J) | CC BY-NC-SA 3.0 TW |
| `mahawu/BM_u8` | Basic Markup UTF-8 | CC BY-NC-SA 3.0 TW |
| `cbeta-org/cbeta_gaiji` | Missing characters DB | CC BY-NC-SA 3.0 TW |

## License Note
CC BY-NC-SA 3.0 Taiwan: **non-commercial research use permitted**.  
Commercial use requires permission from CBETA Foundation + original copyright holders.

## Acquisition Results

- **cbeta-normal-text (DILA-edu)**: OK (21,961 files) — Plain text 一卷一檔, CC BY-NC-SA 3.0
- **BM_u8 (mahawu)**: OK (1,763 files) — Basic Markup UTF-8, simple format
- **xml-p5 (cbeta-org)**: FAIL (3,707 files) — Official TEI P5 (T+X sparse), CC BY-NC-SA 3.0
- **CBETA-txt (DILA-edu)**: OK (23,420 files) — TAF plain text T/X/J canons
- **cbeta_gaiji (cbeta-org)**: OK (41 files) — Gaiji (missing characters + Sanskrit characters) DB