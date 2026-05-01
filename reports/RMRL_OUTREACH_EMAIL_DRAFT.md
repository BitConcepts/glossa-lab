# RMRL outreach email — draft

**Status:** Draft for user review before sending.
**Suggested recipients:**
- `info@rmrl.org` (general inquiries, primary)
- `archives@rmrl.org` (digital archives)
- `library@rmrl.org` (general library)
- Cc: any specific archivist contact you have

**Subject options:**
- Subject A (formal): "Bulk research access request — Mahadevan & Manivannan archives — Glossa-Lab Indus decipherment project"
- Subject B (concise): "Research-access request: Mahadevan personal archive + Tamil-Brahmi corpus"

---

## Email body (formal version)

> Dear RMRL Digital Archives Team,
>
> I am writing on behalf of the Glossa-Lab project, an open computational
> research effort developing statistical-linguistic methods for the analysis
> and possible decipherment of the Indus script. Project repository:
> https://github.com/layer1labs/glossa-lab.
>
> Our current work — Phases 22 through 31 — has built a reproducible
> pipeline that combines:
> 1. Mahadevan's 1977 Indus corpus (1,669 inscriptions, 5,361 sign tokens),
> 2. The CDLI Meluhha-mention tablet corpus (1,462 tablets),
> 3. The ePSD2 Sumerian/Akkadian names database (4,848 entries),
> 4. Iconographic anchors drawn from Parpola 2010, and
> 5. Mahadevan's 2003 *Early Tamil Epigraphy* (110 inscriptions, parsed
>    from the Internet Archive scan).
>
> All findings are published openly with full citation chains
> (`CITATIONS.md` in the repository) and the code is permissively
> licensed for academic use. We have just published Phase-31, which uses
> the Tamil-Brahmi corpus from Mahadevan 2003 as a parallel-script
> probe and finds (preliminary) Zipf-slope alignment with the Indus
> corpus consistent with the Dravidian-script hypothesis advocated by
> Iravatham Mahadevan, Asko Parpola, and others.
>
> I am writing to request **bulk research access** to the following RMRL
> collections, which would substantially advance Phase-32:
>
> 1. **Iravatham Mahadevan's personal notebooks** (10 items, IDs `d1`
>    through `d10`), available at
>    https://rmrl.in/en/dl/personal-archives/mahadevan/notebook?id=d1
>    through `d10`. These are flipbook scans of hand-written notebooks;
>    we would like to perform OCR + content analysis to extract any
>    sign-list updates, candidate readings, and glossary entries.
> 2. **K. Manivannan's Tamil-epigraphy manuscripts** (63 items, IDs
>    `RMRL_0001.pdf` through `RMRL_0063.pdf`), available at
>    https://rmrl.in/en/dl/personal-archives/manivannan/manuscript?id=RMRL_0001.pdf
>    through `_0063`. These appear to be PDF scans; we would parse them
>    for additional Tamil-Brahmi attestations to expand our parallel
>    corpus.
> 3. **Iravatham Mahadevan's research papers** (28+ papers, 1970-2015,
>    listed at https://rmrl.in/en/dl/research-papers/mahadevan ).
> 4. **R. Balakrishnan's research papers**, listed at
>    https://rmrl.in/en/dl/research-papers/balakrishnan .
>
> What I'm specifically hoping for is one of:
> - A bulk-download URL (zip, tar, or S3 prefix) covering these items,
> - An API key or access token for programmatic retrieval at a polite
>   rate, or
> - Confirmation that we may script-download via the existing public
>   endpoints under a stated rate limit (we already use a 1.5-second
>   minimum delay between requests and identify our project clearly in
>   the User-Agent string).
>
> We will of course cite RMRL as the digital archive source for every
> piece of content we use, link back to your collection pages from any
> publication, and abide by your `Content-Signal: search=yes,
> ai-train=no` directive in `robots.txt` — none of the content will be
> used for training generative AI models. All extracted material will be
> used solely for computational research analysis.
>
> Happy to provide additional details, our IRB / ethics statement, or
> a longer methodology document if useful. We would also welcome the
> chance to share our preliminary findings with the RMRL team or any
> Mahadevan-archive curators who might find them of interest.
>
> Thank you for your stewardship of these invaluable collections, and
> for considering this request.
>
> With warm regards,
>
> [YOUR NAME]
> Glossa-Lab Indus Decipherment Project
> [YOUR EMAIL]
> https://github.com/layer1labs/glossa-lab

---

## Email body (concise version, ~200 words)

> Dear RMRL Digital Archives Team,
>
> I lead the Glossa-Lab project (https://github.com/layer1labs/glossa-lab),
> an open computational-linguistic effort applying statistical methods to
> the Indus script and its possible Dravidian linguistic context. Our
> current phase (31) is using Mahadevan 2003 *Early Tamil Epigraphy* as a
> parallel-script probe vs the Mahadevan 1977 Indus corpus.
>
> I would like to request **bulk research access** to:
> - Iravatham Mahadevan's personal notebooks (`d1`-`d10`)
> - K. Manivannan's manuscripts (`RMRL_0001`-`RMRL_0063`)
> - Mahadevan's and R. Balakrishnan's research papers
>
> All under your `personal-archives` and `research-papers` digital
> collections.
>
> A bulk download URL, API key, or formal permission to script-download
> at a polite rate would all work for us. We honor your
> `ai-train=no` directive and will cite RMRL as the source in every use.
> All material is for computational research analysis only; nothing will
> be redistributed or used to train generative AI.
>
> Would you be open to discussing this? Happy to share more methodology
> details or our prior phase reports if useful.
>
> With thanks,
>
> [YOUR NAME]
> [YOUR EMAIL]

---

## After sending

If they reply with **YES** + bulk download:
- Use that as the canonical source going forward
- Update `CITATIONS.md` with their preferred citation format

If they reply with **conditions** (rate limit, attribution requirements):
- Adjust the scraper accordingly (already at 1.5s delay; can lower further if requested)

If they reply with **NO**:
- Stop scraping; rely on the manual-download set from Option 4
- Investigate if they have an alternative data partner (e.g. Tamil Nadu State Department of Archaeology, IRC at Chennai, or BSS Sundaram's collection)

---

*Draft maintained as part of Glossa-Lab Phase-A.*
