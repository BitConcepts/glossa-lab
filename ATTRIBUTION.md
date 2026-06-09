# Attribution, Data Sources & Contact

**Glossa-Lab** is an open-source AI-assisted research platform for the computational
analysis of ancient and undeciphered writing systems. This project depends on the
work of many scholars and data providers whose contributions we are committed to
crediting accurately.

---

## If a citation or credit is missing — contact us immediately

If you are a researcher, data provider, or rights-holder and you believe your work
has been used without proper attribution, or if you have any concern about how your
material appears in this project:

**Please contact Tristen Kyle Pierson directly:**

> **Email:** tpierson@bitconcepts.tech  
> **Subject line:** "Attribution concern — Glossa-Lab"

We treat attribution concerns as urgent. You will receive a response within 48 hours.
If the concern is valid, we will correct the attribution, update the repository, and
update any published outputs immediately.

You may also open a GitHub issue at:
https://github.com/BitConcepts/glossa-lab/issues

---

## Primary data sources

All data sources used in this project are documented in detail in
[CITATIONS.md](./CITATIONS.md). Key sources include:

| Source | Authors | License | Used for |
|--------|---------|---------|---------|
| Holdat LLC Indus Corpus v3 | Miller 2025 | Proprietary — statistical derivatives only, no raw data redistributed | Primary inscription corpus |
| Mahadevan 1977 (M77) | Iravatham Mahadevan | Public domain (ASI / Govt. of India) | Sign numbering (M001–M397) |
| DEDR | Burrow & Emeneau 1984 | © Clarendon Press — reference use | Dravidian etymological evidence |
| Parpola 1994 / 2010 | Asko Parpola | © CUP / open conference paper | Decipherment framework, phoneme map |
| ePSD2 | Tinney et al. / Penn | CC BY-SA | Sumerian/Akkadian name corpus |
| CDLI | Englund et al. | CC BY-NC-SA 3.0 | Bibliographic reference only (no data committed) |
| CISI Vols 1–3 | Joshi, Shah, Parpola et al. | © Suomalainen Tiedeakatemia | Reference only (no data redistributed) |
| Wells 2006 / 2015 | Bryan K. Wells | Open access / © Archaeopress | Sign list cross-reference |
| Fuls 2022/2023 | Andreas Fuls | © independently published | Sign catalog cross-reference |
| ICIT | Wells & Fuls | Restricted (TU Berlin) | API reference; no data committed |
| Nair 2026 | Ashish Nair | CC BY (arXiv) | Independent replication study cited |
| Laursen 2010 | Steffen Terp Laursen | © Wiley / AAE | Gulf seal catalog, fish-sign validation |
| Crawford 2001 | Harriet Crawford | © Archaeology International | Dilmun/Saar seal reference |
| ePSD2 names subset | Penn Babylonian Section | CC BY-SA | Meluhhan name matching (null results) |
| Tamburini 2025 | Fabio Tamburini | CC BY (Frontiers) | SA algorithm methodology reference |

For the complete bibliography with BibTeX entries, license analysis, and per-file
attribution, see [CITATIONS.md](./CITATIONS.md) and
[research/indus/DATA_LICENSES.md](./research/indus/DATA_LICENSES.md).

---

## License compliance summary

- **Holdat LLC corpus (proprietary):** Not redistributed. Only statistical
  derivatives (positional frequencies, bigram counts, candidate readings) appear
  in outputs.
- **ePSD2 (CC BY-SA):** Used only for Meluhhan name matching experiments that
  produced null results. Not incorporated into released research outputs.
  The CC BY 4.0 licence on `research/indus/` outputs is unaffected.
- **CDLI (CC BY-NC-SA):** No CDLI tablet text committed to this repository.
  All CDLI references are bibliographic only.
- **Copyrighted academic sources (CISI, Parpola 1994, Mahadevan 2003):** Used
  as structured analytical references (sign numbers, phoneme assignments, crosswalk
  mappings). No verbatim text reproduced. Defensible as academic fair use / fair
  dealing.
- **PyMuPDF (AGPL):** Used only in standalone research scripts, not in the
  deployed backend. AGPL network-use provisions do not apply.

Released research outputs (`research/indus/`, anchor tables, phase reports,
supplemental datasets) are original analysis released under **CC BY 4.0**.

---

## Acknowledgements

This project is indebted to the following scholars and institutions
(see [CITATIONS.md §Acknowledgements](./CITATIONS.md) for full details):

Iravatham Mahadevan (1930–2018) · Asko Parpola · Bryan K. Wells ·
Andreas Fuls · William Miller Sr (Holdat LLC) · Ashish Nair ·
Steffen Terp Laursen · Harriet Crawford · Petteri Koskikallio ·
Roja Muthiah Research Library (Chennai) · University of Pennsylvania Museum ·
TIFR (Rao, Yadav, Vahia, Joglekar, Adhikari) · Tamburini (Frontiers AI)

---

## How to cite Glossa-Lab

```bibtex
@software{glossalab2026,
  author = {Pierson, Tristen Kyle},
  title  = {Glossa-Lab: An agentic computational linguistics research platform
            for statistical analysis and decipherment of ancient writing systems},
  year   = {2026},
  url    = {https://github.com/BitConcepts/glossa-lab},
  note   = {BitConcepts LLC. MIT licence (source); CC BY 4.0 (research outputs).}
}
```

---

*Last reviewed: June 2026. Contact tpierson@bitconcepts.tech for any attribution
concern — we respond within 48 hours.*
