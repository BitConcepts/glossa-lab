# Fine-Tuning Mistral NeMo 12B for Glossa Lab

> **Purpose**: This guide documents how to create a Glossa-Lab-specific
> fine-tuned version of `mistral-nemo:12b` that performs better on the
> domain tasks identified through systematic evaluation.

---

## Why Fine-Tune?

Our evaluation of `mistral-nemo:12b` against 20 prompts across research
reasoning, code generation, domain knowledge, and long-form synthesis
identified several **persistent gaps** that context injection alone cannot fix:

| Gap | Root Cause | Fine-tune benefit |
|---|---|---|
| M77 L1 arithmetic errors | 12B arithmetic ceiling | Training on M77 worked examples |
| Corpus load pattern drift | Inconsistent few-shot recall | Repeated pattern reinforcement |
| Wrong experiment import paths | No module-structure knowledge | Inject codebase structure |
| Short synthesis responses | Temperature/length bias | Preference tuning on length |
| Confusing Fuls IDs with M77 IDs | Two numbering systems in context | Explicit disambiguation pairs |

A fine-tuned model would:
1. **Always use correct import paths** for `glossa_lab.*` modules
2. **Always use correct corpus load pattern** (`json.loads(path.read_text(...))`)
3. **Correctly compute M77 L1 distances** with the right reference values
4. **Write complete long-form responses** without premature action blocks
5. **Cite benchmark numbers verbatim** from the known results table

---

## Overview of Approach

We use **LoRA (Low-Rank Adaptation)** — a parameter-efficient fine-tuning
method that adds small trainable matrices alongside frozen base weights.
This allows fine-tuning Mistral NeMo 12B on a single GPU (≥ 12 GB VRAM)
without modifying the base model.

**Toolchain**:
- **[Unsloth](https://github.com/unslothai/unsloth)** — 2–3× faster than
  vanilla HuggingFace fine-tuning, same memory; recommended for most cases
- **[Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl)** — more
  flexible dataset formats, better for multi-turn conversations; use when
  training on full conversation histories

---

## Step 1 — Build the Training Dataset

### 1.1 Dataset format

Mistral NeMo uses the **ChatML format** (also compatible with ShareGPT):

```json
{
  "conversations": [
    {"from": "system", "value": "<system_prompt>"},
    {"from": "human", "value": "<user_question>"},
    {"from": "gpt", "value": "<ideal_answer>"}
  ]
}
```

Multi-turn conversations simply add more `human`/`gpt` pairs.

### 1.2 Sources for training pairs

**Source A — Evaluation harness Q&A pairs**
The eval scripts in `backend/_glossa_ai_eval.py` and `backend/_eval_round2.py`
define 20 prompts with expected criteria. Convert each into a training pair
by writing the *ideal* answer (Oz's reference answer from the evaluation):

```python
# Example training pair structure
pair = {
    "conversations": [
        {"from": "system", "value": GLOSSA_SYSTEM_PROMPT},
        {"from": "human", "value": prompt["prompt"]},
        {"from": "gpt", "value": ideal_answer}  # our reference answer
    ]
}
```

**Source B — Benchmark result interpretation pairs**
For each of the 6 benchmark results in `reports/`, generate:
- A question asking about the result
- The ideal answer citing exact numbers

**Source C — Code generation pairs**
For each `glossa_lab.*` function, generate input/output pairs:
- Input: "Write a function that does X"
- Output: Correct code using only `glossa_lab.pipelines.*` imports

**Source D — M77 arithmetic pairs**
For each of the 12 M77 profiles, generate:
- Input: "What M77 profile is closest to T=X, I=Y, M=Z?"
- Output: Correct L1 distance computation with the right profile ID

### 1.3 Dataset generation script

```python
# backend/scripts/generate_training_data.py
"""Generate Glossa Lab LoRA fine-tuning dataset from eval Q&A pairs."""
import json
from pathlib import Path

SYSTEM_PROMPT = """You are Glossa, the AI research assistant for Glossa Lab.
You have expert knowledge of:
- Indus Script decipherment methodology (Fuls 2023, ICIT corpus)
- Computational linguistics: entropy, Zipf, n-gram statistics
- The glossa_lab Python codebase (pipelines, experiments, data modules)
- Benchmark results from Tier 1a through Tier 5 experiments
- M77 positional profiles (12 comparison signs, L1 distance computation)
- Kandles phoneme-colour validation system

When writing Python code, use ONLY these imports:
  from glossa_lab.pipelines.decipher import LanguageModel, decipher, score_accuracy
  from glossa_lab.pipelines.beam_decipher import beam_decipher, UGARITIC_PHONO_GROUPS_TIGHT
  from glossa_lab.experiments.<module> import <ClassName>

Benchmark scores (cite exactly):
  Tier 1a: 30/30 = 100% (beam + tight phono + 10 anchors)
  Tier 1a SA no anchors: 2/30 = 6.7%
  Tier 1f Meroitic→Coptic oracle delta: -3972
  Transparency T3: 30/30 = 100%, attribution: 90% human anchors
"""

# M77 reference pairs (generated exhaustively for all 12 profiles)
M77_PROFILES = {
    "M088": (0.056, 0.333, 0.611, "Figure+staff"),
    "M200": (0.038, 0.811, 0.151, "Bull head"),
    "M028": (0.044, 0.923, 0.033, "Arrow"),
    "M059": (0.047, 0.094, 0.812, "Fish"),
    "M012": (0.863, 0.013, 0.125, "Small circle TMK"),
    "M282": (0.730, 0.016, 0.254, "Bracket TMK"),
    "M500": (0.125, 0.250, 0.625, "Plant/tree"),
    "M342": (0.138, 0.241, 0.517, "Short stroke"),
    "M086": (0.060, 0.360, 0.540, "Standing figure"),
    "M083": (0.059, 0.588, 0.353, "Kneeling figure"),
    "M029": (0.030, 0.101, 0.869, "Comb/rake"),
    "M005": (0.000, 0.019, 0.981, "Six strokes"),
}

def l1(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1]) + abs(a[2]-b[2])

def generate_m77_pairs():
    pairs = []
    import random; rng = random.Random(42)
    # Generate 50 queries with known answers
    profile_list = list(M77_PROFILES.items())
    for _ in range(50):
        # Pick a profile and add noise
        name, (t, i, m, desc) = rng.choice(profile_list)
        noise = lambda x: round(max(0, min(1, x + rng.uniform(-0.05, 0.05))), 3)
        qt, qi, qm = noise(t), noise(i), noise(m)
        # normalize
        s = qt + qi + qm
        qt, qi, qm = round(qt/s, 3), round(qi/s, 3), round(qm/s, 3)

        dists = sorted(
            [(k, round(l1((qt,qi,qm), v[:3]), 3), v[3]) for k, v in M77_PROFILES.items()],
            key=lambda x: x[1]
        )
        top3 = dists[:3]
        answer = f"""Based on the positional profile T={qt}, I={qi}, M={qm}, here are the top 3 closest M77 profiles:

1. **{top3[0][0]}** ({top3[0][2]}): L1 = |{qt}-{M77_PROFILES[top3[0][0]][0]}| + |{qi}-{M77_PROFILES[top3[0][0]][1]}| + |{qm}-{M77_PROFILES[top3[0][0]][2]}| = {top3[0][1]} ← CLOSEST
2. **{top3[1][0]}** ({top3[1][2]}): L1 = {top3[1][1]}
3. **{top3[2][0]}** ({top3[2][2]}): L1 = {top3[2][1]}

The sign is closest to **{top3[0][0]} ({top3[0][2]})** with L1 distance {top3[0][1]}.
{"This sign has a very high M-rate, suggesting it functions as a medial/syllabic core in inscriptions." if qm > 0.7
 else "This sign has a high I-rate, suggesting it appears predominantly word-initially." if qi > 0.6
 else "This sign has a high T-rate, suggesting it is a terminal marker (TMK) or grammatical suffix."}"""

        pairs.append({
            "conversations": [
                {"from": "system", "value": SYSTEM_PROMPT},
                {"from": "human", "value": f"A sign has positional profile T={qt}, I={qi}, M={qm}. Which M77 profile is most similar? Show L1 distances."},
                {"from": "gpt", "value": answer}
            ]
        })
    return pairs

# Run this script to generate training_data.jsonl
if __name__ == "__main__":
    out = Path("backend/data/glossa_training_data.jsonl")
    pairs = generate_m77_pairs()
    # Add more pair generators here...
    with open(out, "w") as f:
        for p in pairs:
            f.write(json.dumps(p) + "\n")
    print(f"Generated {len(pairs)} training pairs → {out}")
```

### 1.4 Recommended dataset size

| Category | Pairs | Priority |
|---|---|---|
| M77 arithmetic | 200 | Critical |
| Code generation (imports) | 100 | Critical |
| Benchmark citation | 60 | High |
| Decipherment theory | 40 | High |
| Multi-turn research Q&A | 80 | Medium |
| Corpus analysis scripts | 60 | Medium |
| Long-form synthesis | 30 | Low |
| **Total** | **~570** | — |

570 high-quality pairs is sufficient for LoRA on a 12B model. More is better
up to ~2,000 pairs, but diminishing returns beyond that for domain adaptation.

---

## Step 2 — Environment Setup

### Hardware requirements

| Config | VRAM | Training time (570 pairs, 3 epochs) |
|---|---|---|
| RTX 3090 / 4090 (24 GB) | 24 GB | ~45 min |
| RTX 3080 (10 GB) + CPU offload | 10 GB | ~2 hours |
| A100 80 GB | 80 GB | ~20 min |
| 2× RTX 3090 (multi-GPU) | 48 GB | ~25 min |

### Install Unsloth (fastest, recommended)

```bash
# Create a new venv for fine-tuning (separate from glossa-lab venv)
python -m venv glossa-finetune
source glossa-finetune/bin/activate  # Linux/macOS
# glossa-finetune\Scripts\activate  # Windows

# Install Unsloth with CUDA 12.1
pip install "unsloth[colab-new] @ git+https://github.com/unslothai/unsloth.git"
pip install --no-deps trl peft accelerate bitsandbytes
```

### Install Axolotl (alternative, better multi-turn)

```bash
git clone https://github.com/OpenAccess-AI-Collective/axolotl
cd axolotl
pip install packaging ninja
pip install -e '.[flash-attn,deepspeed]'
```

---

## Step 3 — Fine-Tuning with Unsloth

### 3.1 Training script

```python
# backend/scripts/finetune_glossa.py
"""LoRA fine-tuning of mistral-nemo-12b for Glossa Lab."""
from unsloth import FastLanguageModel
from trl import SFTTrainer
from transformers import TrainingArguments
from datasets import load_dataset
import torch

# ── Model loading ─────────────────────────────────────────────
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/mistral-nemo-bnb-4bit",  # 4-bit quantized base
    max_seq_length=8192,       # NeMo supports 128K; 8K sufficient for our prompts
    dtype=None,                # auto-detect (float16 on most GPUs)
    load_in_4bit=True,         # 4-bit quantization for VRAM efficiency
)

# ── LoRA configuration ─────────────────────────────────────────
model = FastLanguageModel.get_peft_model(
    model,
    r=32,                      # rank: 16–64 for domain adaptation
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_alpha=64,             # scaling factor (= 2 * r is typical)
    lora_dropout=0.05,
    bias="none",
    use_gradient_checkpointing="unsloth",
    random_state=42,
    use_rslora=False,
    loftq_config=None,
)

# ── Dataset ────────────────────────────────────────────────────
# Format: ChatML / ShareGPT JSON lines
dataset = load_dataset(
    "json",
    data_files="backend/data/glossa_training_data.jsonl",
    split="train",
)

def format_chat(example):
    """Convert conversation to Mistral NeMo ChatML tokens."""
    messages = example["conversations"]
    # Unsloth handles the ChatML template automatically
    return {"text": tokenizer.apply_chat_template(
        [{"role": "system" if m["from"] == "system" else
                  "user" if m["from"] == "human" else "assistant",
          "content": m["value"]} for m in messages],
        tokenize=False,
        add_generation_prompt=False,
    )}

dataset = dataset.map(format_chat)

# ── Training arguments ─────────────────────────────────────────
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    max_seq_length=8192,
    dataset_num_proc=4,
    packing=True,              # pack short examples together for efficiency
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=8,   # effective batch = 16
        warmup_steps=30,
        num_train_epochs=3,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=10,
        optim="adamw_8bit",
        weight_decay=0.01,
        lr_scheduler_type="cosine",
        seed=42,
        output_dir="glossa-nemo-lora",
        save_steps=100,
        save_total_limit=2,
    ),
)

trainer.train()

# ── Save ──────────────────────────────────────────────────────
model.save_pretrained("glossa-nemo-lora-final")
tokenizer.save_pretrained("glossa-nemo-lora-final")
print("LoRA adapters saved to glossa-nemo-lora-final/")
```

### 3.2 Key hyperparameters to tune

| Parameter | Starting value | Notes |
|---|---|---|
| `r` (LoRA rank) | 32 | 16 if VRAM is tight, 64 for more capacity |
| `lora_alpha` | 64 | Keep = 2×r |
| `learning_rate` | 2e-4 | Lower to 1e-4 if loss diverges |
| `num_train_epochs` | 3 | 2–4 for domain adaptation; more → overfitting |
| `max_seq_length` | 8192 | 4096 if VRAM limited |
| `lora_dropout` | 0.05 | 0.1 if overfitting |

---

## Step 4 — Convert and Deploy to Ollama

After training, the LoRA adapters are merged into the base model and converted
to GGUF format for Ollama.

### 4.1 Merge adapters into base model

```python
# Merge LoRA into full model (in fine-tuning venv)
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    "glossa-nemo-lora-final",
    max_seq_length=8192,
    dtype=None,
    load_in_4bit=True,
)
model.save_pretrained_merged(
    "glossa-nemo-merged",
    tokenizer,
    save_method="merged_4bit_forced",  # keeps 4-bit quantization
)
print("Merged model saved to glossa-nemo-merged/")
```

### 4.2 Convert to GGUF

```bash
# Install llama.cpp (for GGUF conversion)
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make -j8

# Convert to GGUF Q4_K_M (best quality/size tradeoff)
python convert_hf_to_gguf.py glossa-nemo-merged \
    --outfile glossa-nemo-12b-q4_k_m.gguf \
    --outtype q4_k_m
```

### 4.3 Create Ollama Modelfile and push

```dockerfile
# Modelfile
FROM ./glossa-nemo-12b-q4_k_m.gguf

SYSTEM """You are Glossa, the AI research assistant for Glossa Lab — a computational
linguistics platform studying the Indus Script using methods developed by Dr. Andreas Fuls.
You have deep knowledge of entropy analysis, decipherment benchmarks, and the
glossa_lab Python codebase. Always cite benchmark numbers from the provided context.
When writing code, use only glossa_lab.pipelines.* and glossa_lab.experiments.* imports."""

PARAMETER temperature 0.15
PARAMETER num_ctx 8192
PARAMETER num_predict 4096
```

```bash
# Register and run in Ollama
ollama create glossa-nemo:12b-glossa -f Modelfile
ollama run glossa-nemo:12b-glossa

# Update Glossa Lab settings to use the fine-tuned model:
# In Settings → AI → Ollama → select "glossa-nemo:12b-glossa"
```

---

## Step 5 — Evaluation After Fine-Tuning

Re-run the eval harnesses against the fine-tuned model to measure improvement:

```bash
# Update the backend to point to the new model temporarily:
# In Settings → Ollama → select "glossa-nemo:12b-glossa"

cd backend
python _glossa_ai_eval.py      # Round 1 (8 prompts)
python _eval_round2.py         # Round 2 (12 prompts)
```

**Target improvements vs base model:**

| Metric | Base `mistral-nemo:12b` | Target after fine-tune |
|---|---|---|
| Round 1 pass rate | 6/8 (75%) | 8/8 (100%) |
| Round 2 pass rate | 11/12 (92%) | 12/12 (100%) |
| M77 L1 arithmetic | IDs correct, values wrong | IDs + values correct |
| Code imports | ~80% correct | >98% correct |
| Benchmark citation | Numbers correct | Numbers + tier correct |
| Long-form word count | 190 avg (vs 250 target) | >250 consistently |

---

## Step 6 — Axolotl Configuration (Alternative)

For multi-turn conversation training, Axolotl with the `sharegpt` format is
more flexible. Example config:

```yaml
# backend/scripts/axolotl_glossa.yml
base_model: mistralai/Mistral-Nemo-Instruct-2407
model_type: MistralForCausalLM
tokenizer_type: LlamaTokenizer

load_in_4bit: true
adapter: lora
lora_r: 32
lora_alpha: 64
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj

datasets:
  - path: backend/data/glossa_training_data.jsonl
    type: sharegpt
    conversation: chatml

dataset_prepared_path: /tmp/glossa-axolotl-prep
val_set_size: 0.05
sequence_len: 8192
sample_packing: true

gradient_accumulation_steps: 8
micro_batch_size: 2
num_epochs: 3
optimizer: adamw_bnb_8bit
lr_scheduler: cosine
learning_rate: 0.0002
warmup_steps: 30

output_dir: ./glossa-nemo-axolotl-out
logging_steps: 10
save_steps: 100
save_total_limit: 2
```

```bash
# Train with Axolotl
accelerate launch -m axolotl.cli.train backend/scripts/axolotl_glossa.yml
```

---

## Gap-Specific Training Pairs

### Pair type: M77 arithmetic (sample)

**Human**: A sign has T=0.03, I=0.10, M=0.87. Which M77 profile is closest?

**Gpt**:
```
Computing L1 distances against all 12 M77 profiles:

  M029 (Comb/rake):  |0.03-0.030| + |0.10-0.101| + |0.87-0.869| = 0.000+0.001+0.001 = 0.002 ← CLOSEST
  M059 (Fish):       |0.03-0.047| + |0.10-0.094| + |0.87-0.812| = 0.017+0.006+0.058 = 0.081
  M005 (Six strks):  |0.03-0.000| + |0.10-0.019| + |0.87-0.981| = 0.030+0.081+0.111 = 0.222

Closest: M029 (Comb/rake), L1=0.002. This is an almost pure MEDIAL sign
(M=0.869 in the reference), suggesting it functions as a syllabic core or
medial consonant. With M-rate 0.87, it very rarely appears word-initially or
word-terminally.
```

### Pair type: correct import (sample)

**Human**: How do I import and run the TransparencyBenchmark?

**Gpt**:
```python
from glossa_lab.experiments.transparency_benchmark import TransparencyBenchmark

result = TransparencyBenchmark().run()
# result contains: {'tiers': [...], 'conclusion': '...'}
# tiers[0] = T0 (freq-rank floor), tiers[3] = T3 (full stack)
print(result['tiers'][3]['accuracy'])  # → 30
print(result['conclusion'])
```

### Pair type: corpus load (sample)

**Human**: Write code to load the Indus corpus and count total tokens.

**Gpt**:
```python
import json
from pathlib import Path
from collections import Counter

R = Path(__file__).parent.parent / "reports"
data = json.loads((R / "icit_extracted_corpus.json").read_text("utf-8"))
inscriptions = [i["sequence"] for i in data["inscriptions"] if i.get("sequence")]

total_c = Counter(s for ins in inscriptions for s in ins)
print(f"Total tokens: {sum(total_c.values())}")
print(f"Distinct signs: {len(total_c)}")
print(f"Inscriptions: {len(inscriptions)}")
# Expected: ~14,213 tokens, 713 sign types, 4,410 inscriptions
```

---

## Notes on the Base Model

**Mistral NeMo 12B** (mistral-nemo-instruct-2407) characteristics relevant
to fine-tuning:

- **Tokenizer**: Tekken (tiktoken-compatible) — efficient for multilingual and
  technical text; handles Unicode sign sequences well
- **Context window**: 128K tokens — far more than we need (8K is sufficient)
- **Architecture**: Standard Mistral with grouped-query attention (GQA)
- **Instruction format**: ChatML (`<|im_start|>system\n...<|im_end|>` etc.)
- **Strengths**: Excellent instruction following, clean JSON output, good at
  structured tasks; already ranked 10/10 on Glossa score in our library
- **Weaknesses identified**: Arithmetic on unfamiliar reference tables (M77),
  domain-specific import paths, response length consistency

The fine-tuning adds ~50–200M trainable parameters via LoRA on top of the
~12B frozen base parameters. The resulting model remains fully compatible with
Ollama and all existing Glossa Lab infrastructure.

---

*Last updated: 2026-04-10. Run `python backend/scripts/generate_training_data.py`
to regenerate the training dataset after adding new benchmark results.*
