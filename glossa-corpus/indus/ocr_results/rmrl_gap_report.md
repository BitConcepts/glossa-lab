# indusscript.in Gap Report — Mahadevan 1977 OCR Analysis
**Generated:** 2026-05-15
**Method:** Tesseract OCR of 1,231 pages from the Mahadevan 1977 Internet Archive scan
**Prepared by:** Glossa-Lab / Layer1Labs Silicon

---

## Summary

We ran OCR across the full scanned copy of:

> Mahadevan, Iravatham (1977). *The Indus Script: Texts, Concordance and Tables.*
> Memoirs of the Archaeological Survey of India No. 77. New Delhi: ASI.

We compared all text numbers found in the scan against the texts currently available
in the indusscript.in database (which we accessed via the authenticated Firestore API).

| Metric | Count |
|---|---|
| Pages analyzed | 1,231 (149 TEXTS + 1,082 CONCORDANCE) |
| Unique IM77 text numbers found in scan | 3,192 |
| Text numbers in indusscript.in | 2,906 |
| **Text numbers in scan but NOT in indusscript.in** | **308** |

---

## The 308 Missing Text Numbers

These IM77 text numbers appear in the printed 1977 concordance but are not
currently accessible through the indusscript.in application:

```
1223, 1241, 1258, 1264, 1428, 1517, 1575, 1580, 1586, 1627,
1631, 1634, 1638, 1641, 1646, 1647, 1661, 1674, 1695, 1721,
1727, 1740, 1747, 1749, 1758, 1791, 1817, 1887, 1888, 1900,
1923, 1941, 1947, 1961, 1975, 1981, 2011, 2029, 2046, 2059,
2060, 2097, 2109, 2110, 2113, 2117, 2140, 2156, 2165, 2166,
...
```

(Full list in `m77_textnums_missing.json` — 308 entries total, range 1223–9989)

---

## Context and Request

We are building an open research corpus of Indus inscription texts for
computational analysis (statistical decipherment, SA-based phoneme mapping,
Zipf/entropy studies). We have already acquired the full indusarrays Firestore
collection (2,906 texts) through the normal app interface.

The 308 gaps we identified represent texts that were in Mahadevan's original 1977
concordance but appear to be missing from the current digitization. We believe this
may be due to the concordance being organized by sign rather than by text number,
and some texts appearing only once in the concordance under a sign that wasn't
fully digitized.

**We would be grateful if you could:**

1. Confirm whether these 308 text numbers are intentionally excluded or
   inadvertently missing from the indusscript.in database.

2. If they exist in your data, provide the sign sequences for these texts
   in any format (CSV, JSON, or the indusscript.in concordance format).

3. If a bulk data export of the full M77 concordance is available for
   academic research use, we would be happy to work under whatever
   attribution and usage restrictions you specify.

We will cite RMRL, the Indus Research Centre, and the original Mahadevan
publication prominently in all derivative work and publications.

---

## Technical Notes

- OCR performed using Tesseract 5.5.0 on 1800px-resolution IIIF images
- Left column extraction (text number column) with 2× upscaling
- Validation: 4-digit integers in range 1001–9999
- False positive filter: 6-digit catalog numbers and 2-digit sub-codes
  are excluded by regex pattern
- Known false positives exist (e.g. some catalog numbers misread as textnums)
  so the list should be treated as indicative, not authoritative

Contact: rmrl@rmrl.in
