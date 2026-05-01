# Notebook OCR — model + pipeline advisory

**Goal:** OCR the **3,247 image-only pages** of Iravatham Mahadevan's hand-written notebooks (d1, d2, d3, d4, d5, d6, d7, d9, d10) scraped from RMRL. The d8 notebook returned 403 and is excluded.

**The challenge:**
- Mixed Tamil + English handwriting
- Possibly some Devanagari / Sanskrit notes
- Indus sign drawings inline with text
- Variable handwriting quality (50-year span: ~1968-2018)
- High variability between notebooks (some are notes, some are draft typescripts)

**The opportunity:**
- These notebooks are likely to contain Mahadevan's **draft sign-list updates, candidate phoneme assignments, and unpublished readings** — material not in his published papers
- Even partial OCR (Tamil + English text) would give us thousands of new candidate entries for the phoneme map

This document compares OCR options across three axes: **quality**, **cost**, and **speed**.

---

## Page count + size estimates

| Notebook | Pages |
|---|---|
| d1 | 206 |
| d2 | 414 |
| d3 | 674 |
| d4 | 416 |
| d5 | 416 |
| d6 | 420 |
| d7 | 497 |
| d9 | 82 |
| d10 | 122 |
| **TOTAL** | **3,247** |

Each page is a PNG, scaled to roughly 1500×2000 px (typical Internet Archive book scan). Estimated total: ~3 GB of image data once downloaded.

**Image download budget:** 3,247 × ~3 sec polite delay = **~2.7 hours of polite scraping** before OCR even starts.

---

## Cloud-API options

### 1. Google Gemini 2.0 Flash / 2.5 Flash — RECOMMENDED for bulk

**Pricing (as of ~2026):** roughly $0.075 per 1M input tokens (image counts as ~258 tokens at the 768×768 tile size, so ~$0.000019 per image at base resolution; at high-resolution tile mode ~$0.0001 per image).

**Cost estimate:** 3,247 pages × ~$0.005 (input + output) ≈ **$16-25 total**.

**Quality on hand-written Tamil:** Strong. Gemini's multilingual coverage is excellent and it handles handwritten Tamil + Devanagari well. Indus signs would not be recognized as characters but Gemini will describe them in prose ("a fish-like sign appears here").

**Speed:** ~5-10 seconds per page via the API. 3,247 pages serial = ~5-9 hours. Parallel (10 concurrent) = ~30-60 minutes.

**Setup:**
- Get API key from [https://aistudio.google.com/](https://aistudio.google.com/) (free tier: 1500 requests/day)
- `pip install google-generativeai`
- `model.generate_content([image, "Transcribe this page verbatim..."])`

**Verdict:** Best cost/quality tradeoff for bulk. Run this first.

---

### 2. Claude Sonnet 4.5 / Opus 4.5 — RECOMMENDED for rescue runs

**Pricing:** ~$3 / 1M input tokens, ~$15 / 1M output. Image @ ~1.6K tokens. Cost per page ≈ $0.005-$0.015.

**Cost estimate:** 3,247 pages × ~$0.01 ≈ **$30-50**.

**Quality:** Best-in-class on documents and handwriting. Particularly strong on:
- Multilingual handwriting
- Layout preservation (tables, marginalia)
- Recognizing when text is illegible vs. just poorly written

**Speed:** ~6-12 sec/page; parallel-friendly.

**Setup:**
- Get API key from `https://console.anthropic.com/`
- `pip install anthropic`
- Send `image/png` content via the messages API with prompt caching enabled

**Verdict:** Use for the 5-10% of pages where Gemini struggles or returns "[unreadable]". Rescue-run pattern saves money vs running Claude on everything.

---

### 3. OpenAI GPT-4o / GPT-5 Vision

**Pricing:** $2.50 / 1M input + $10 / 1M output for GPT-4o; image-as-input at ~765 tokens/image at high detail.

**Cost estimate:** 3,247 pages × ~$0.01-0.02 ≈ **$30-65**.

**Quality:** Comparable to Claude on handwriting; slightly weaker on Tamil-specific layouts in our experience.

**Verdict:** Acceptable backup. Claude is generally a touch better on multilingual handwriting; GPT-4o's structured JSON output mode is useful if we want pre-parsed sign-list entries.

---

### 4. Mistral Pixtral Large / pixtral-12b-2409 — already used in this project

**Pricing:** Pixtral 12B small ~$0.15/1M, Pixtral Large ~$2/1M.

**Cost estimate:** 3,247 pages × Pixtral-12b ~$0.001 ≈ **$3-5** for the whole notebook set.

**Quality:** Decent on printed text; **weaker on handwriting** vs Gemini/Claude. We used it in Phase-28 for CISI Vol 3 OCR with mixed results.

**Speed:** Fast, low rate limits.

**Verdict:** Cheapest cloud option, but quality concerns. Run only on a sample first to verify.

---

## Local options — Ollama

Ollama is convenient if you want zero per-page cost and don't mind slower processing.

### 1. Qwen2.5-VL-7B / 72B — RECOMMENDED local choice

**Best open vision-LM as of late 2025.** Strongest multilingual + document OCR among open models.

**Setup:**
```bash
ollama pull qwen2.5vl:7b      # ~5 GB, runs on 16 GB VRAM
ollama pull qwen2.5vl:72b     # ~45 GB, needs 80 GB VRAM (A100 / H100 / multi-GPU)
```

**Speed:**
- 7B: ~5-15 sec/page on RTX 4090. 3,247 pages ≈ 5-15 hours.
- 72B: ~30-60 sec/page; needs serious GPU.

**Quality:** 7B is good on printed; passable on handwriting. 72B is genuinely competitive with Gemini Flash on documents.

**Verdict:** Best local option. Run 7B as a free baseline; rescue with cloud APIs.

---

### 2. MiniCPM-V 2.6 / 8B

**Setup:** `ollama pull minicpm-v:8b`

**Strengths:** Small (8 GB), fast, surprisingly good on documents.

**Weakness:** Multilingual coverage is narrower than Qwen2.5-VL.

**Verdict:** Acceptable backup for English-only pages. Less good for the Tamil sections.

---

### 3. Llama 3.2 Vision 11B / 90B

**Setup:** `ollama pull llama3.2-vision:11b`

**Strengths:** Meta's vision model, well-supported in Ollama.

**Weakness:** Notably weaker on handwriting + multilingual than Qwen2.5-VL.

**Verdict:** Skip in favor of Qwen2.5-VL.

---

### 4. InternVL2 / InternVL3

**Strengths:** Strong on scanned-document layouts, OCR-tuned variants exist.

**Setup:** Less well-supported in Ollama; you'll likely need vLLM or HuggingFace transformers directly.

**Verdict:** Worth trying if Qwen2.5-VL underperforms on a sample.

---

## Local options — vLLM (high-throughput batched inference)

vLLM is the right choice if you want to OCR all 3,247 pages locally with GPU acceleration. It batches requests and saturates the GPU.

### Recommended models for vLLM

| Model | VRAM | Throughput on H100 | Multilingual | Handwriting |
|---|---|---|---|---|
| **Qwen2.5-VL-7B** | 16 GB | ~3-5 pages/sec batched | Excellent | Good |
| **Qwen2.5-VL-72B** | 160 GB (FP16) / 80 GB (int4) | ~0.5 pages/sec | Excellent | Very Good |
| **InternVL3-8B** | 16 GB | ~3-5 pages/sec | Excellent | Very Good |
| **Pixtral-12B** | 24 GB | ~2-4 pages/sec | Good | Fair |
| **Llama-3.2-Vision-11B** | 24 GB | ~2-4 pages/sec | Fair | Fair |

**Setup (Qwen2.5-VL-7B via vLLM):**
```bash
pip install vllm
vllm serve Qwen/Qwen2.5-VL-7B-Instruct \
  --port 8001 \
  --max-model-len 32768 \
  --gpu-memory-utilization 0.9
```

Then point an OpenAI-compatible client at `http://localhost:8001/v1` and run our OCR pipeline against it.

**Speed estimate:** With batched inference on a single A100/H100, 3,247 pages should complete in **30-90 minutes** at full GPU utilization. On a consumer 4090 expect 2-4 hours.

---

## Recommended pipeline

### Tier 1: Bulk pass with Gemini 2.0 Flash (cheap + good)

```python
# Pseudo-code
for page in all_pages:
    prompt = (
        "You are looking at a page from Iravatham Mahadevan's "
        "personal notebook (Tamil epigrapher, 1930-2018). The page "
        "contains hand-written Tamil and English text and possibly "
        "drawings of Indus-script signs. Transcribe ALL legible text "
        "verbatim, preserving line structure. For Indus sign drawings, "
        "describe them in [brackets]. If a section is illegible, write "
        "[illegible]. Maintain the page's spatial structure where "
        "obvious."
    )
    text = gemini.generate_content([page_image, prompt]).text
    save_to(f"corpora/downloads/rmrl/notebooks/d{N}/text/page_{P}.txt", text)
```

**Cost:** ~$20. **Time:** ~1-3 hours with parallel requests.

### Tier 2: Rescue with Claude 3.5/4 on flagged pages

After Tier 1, flag pages where:
- Output is < 50 chars (likely missed handwriting)
- Output contains > 20% "[illegible]"
- Output is mostly drawing-description with no transcribed text

Send those (~5-15% of pages) to Claude 4 with a more detailed prompt. **Cost:** ~$5-10 additional.

### Tier 3 (optional): Local Qwen2.5-VL pass for diff comparison

Run Qwen2.5-VL-7B locally on a 100-page sample. Compare against Tier 1 + 2 output. If the local model finds text the cloud APIs missed (or vice versa), build a merged final transcript.

### Tier 4: Targeted re-OCR on key pages

After mining the Tier-1+2 transcripts for sign-list updates, identify pages that look like they contain glossary tables or sign-list updates. Re-OCR those individually with Claude in a high-detail mode + structured JSON output schema.

---

## Token / API setup checklist

For the user to acquire:

| Service | URL | Free tier | Cost for full job |
|---|---|---|---|
| **Google Gemini API** | https://aistudio.google.com/app/apikey | 1500 requests/day | $20-25 |
| **Anthropic API** | https://console.anthropic.com/ | $5 free credit | $30-50 |
| **OpenAI API** | https://platform.openai.com/api-keys | $5 free credit | $30-65 |
| **Mistral API** | https://console.mistral.ai/ | $5 free credit | $3-5 |

For local:
- **Ollama** (free) — https://ollama.com/download/windows; install + `ollama pull qwen2.5vl:7b`
- **vLLM** (free, GPU required) — `pip install vllm`; need 16+ GB VRAM for 7B models, 80+ GB for 72B

---

## Recommendation matrix

| Goal | Pick |
|---|---|
| Lowest cost, best quality | **Gemini 2.0 Flash** (Tier 1) + **Claude rescue** (Tier 2) ≈ $25-35 |
| Maximum quality regardless of cost | Claude 4 on every page ≈ $50-100 |
| Zero $ but you have a 4090+ | **Ollama + Qwen2.5-VL-7B** (5-15 hours runtime) |
| Maximum throughput, GPU available | **vLLM + Qwen2.5-VL-7B/72B** (30-90 min on H100) |
| Already have Mistral keys | Pixtral-12B as Tier 1, Claude as rescue |

**My pick for Glossa-Lab:** Gemini Flash bulk + Claude rescue. ~$25-35 total, ~2-4 hours of clock time, rescues come back in ~30 min. Net result: ~3,000 transcribed pages of Mahadevan notebook content, ready to mine for new sign readings.

---

## Next step

If you go with Gemini + Claude:
1. Acquire `GOOGLE_API_KEY` (Gemini) + `ANTHROPIC_API_KEY` (Claude rescue)
2. Drop both into a `.env` file at repo root (already gitignored)
3. I'll build `backend/scripts/notebook_ocr_pipeline.py` that:
   - Downloads all 3,247 page PNGs (polite rate)
   - Runs Tier-1 Gemini OCR with retries + caching
   - Identifies low-quality pages
   - Runs Tier-2 Claude rescue
   - Saves merged transcripts as `corpora/downloads/rmrl/notebooks/d{N}/text/page_{P}.txt`
   - Aggregates per-notebook into `notebooks/d{N}/full_text.json`

If you go with vLLM:
1. Confirm GPU + VRAM available
2. I'll add a vLLM-server setup step + a parallel client in the pipeline

---

*Phase-32 advisory document. Last updated: 2026-05-01.*
