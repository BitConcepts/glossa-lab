"""Phase-40: SA with expanded Indus corpus + CNN augmentation + gap analysis.

Three experiments:
  A. Corpus status audit — how many usable sequences from indus_corpus_v2?
  B. SA T1 confirmation with expanded corpus (3,085 seqs vs 1,669 M77 Holdat)
     Uses indus_corpus_v2.py as drop-in corpus loader.
     Expected: more signs with freq>=3, higher Z-scores, larger Dravidian advantage.
  C. CNN augmentation — use torchvision transforms to 10x training data,
     retrain EfficientNet-B0. Should go from 9.94% to ~30-50% val accuracy.

Citations: A.1 (M77), C.2 (Parpola), E.1 (DEDR), I.1-I.5 (museum sources)
"""
from __future__ import annotations
import json, math, random, re, sys, time, unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))
REPORTS = ROOT / "reports"
BACKEND_REPORTS = ROOT / "backend" / "reports"
DATA = ROOT / "backend" / "glossa_lab" / "data"
SMOOTHING = math.log(1e-8)

# ── Helpers ───────────────────────────────────────────────────────────────────
_D = {"ā":"a","ī":"i","ū":"u","ṉ":"n","ṟ":"r","ḷ":"l","ḻ":"l","ṛ":"r",
      "ṭ":"t","ḍ":"d","ṅ":"n","ṇ":"n","ñ":"n","ś":"s","ṣ":"s","ḥ":"h"}
def _sd(s):
    o=[]
    for c in unicodedata.normalize("NFD",s):
        p=_D.get(c)
        if p: o.append(p)
        elif unicodedata.category(c)!="Mn": o.append(c)
    return "".join(o)
def _sylls(w):
    V=set("aeiou"); C=set("bcdfghjklmnpqrstvwxyz")
    r=[]; i=0; cur=""
    while i<len(w):
        c=w[i]; cur+=c
        if c in V:
            if i+1<len(w) and w[i+1] in C and (i+2>=len(w) or w[i+2] in V): i+=1; cur+=w[i]
            r.append(cur); cur=""
        elif len(cur)>=3: r.append(cur); cur=""
        i+=1
    if cur:
        if r: r[-1]+=cur
        else: r.append(cur)
    return [s for s in r if s]
def _to_syl(reading, vocab):
    reading=reading.split("/")[0].strip()
    reading=re.sub(r"\(.*?\)","",reading).strip().rstrip("?")
    if re.match(r"(term|med|init|ctx|role|boundary|suffix|uncertain)[-:]?",reading.lower()): return None
    if not reading or reading in("?","-") or "uncertain" in reading.lower(): return None
    clean=_sd(reading); clean=re.sub(r"[^a-z]","",clean.lower())
    if not clean: return None
    if clean in vocab: return clean
    for s in _sylls(clean):
        if s in vocab: return s
    for l in(2,3,1):
        if len(clean)>=l:
            c=clean[:l]
            if c in vocab: return c
    return clean[:3] if len(clean)>3 else clean

def load_lm(name):
    raw=json.loads((DATA/name).read_text("utf-8"))
    braw=raw.get("bigrams",raw.get("bigram_freq",{}))
    bigs={}
    for k,lp in braw.items():
        ps=k.split("|") if "|" in k else k.split(",") if "," in k else [k]
        if len(ps)==2:
            try: bigs[(ps[0].strip(),ps[1].strip())]=float(lp)
            except: pass
    freq=Counter()
    for(a,b) in bigs: freq[a]+=1; freq[b]+=1
    ranked=raw.get("vocab",[]) or [s for s,_ in freq.most_common()]
    return bigs, ranked

def score(m, inscs, bigs):
    t=0.0
    for insc in inscs:
        for i in range(len(insc)-1):
            a=m.get(insc[i]); b=m.get(insc[i+1])
            if a and b: t+=bigs.get((a,b),SMOOTHING)
    return t

def run_sa(fixed, free, vocab, inscs, bigs, n=30_000, seed=42):
    rng=random.Random(seed)
    if not vocab: return dict(fixed),score(fixed,inscs,bigs)
    ft=[v for v in vocab if v not in fixed.values()]
    while len(ft)<len(free): ft.append(rng.choice(vocab))
    rng.shuffle(ft)
    m=dict(fixed)
    for i,s in enumerate(free): m[s]=ft[i%len(ft)]
    cur=score(m,inscs,bigs); best=dict(m); bs=cur
    T0,T1=2.0,0.01
    for it in range(n):
        T=T0*((T1/T0)**(it/n))
        if len(free)<2: break
        i,j=rng.sample(range(len(free)),2)
        si,sj=free[i],free[j]; vi,vj=m[si],m[sj]
        m[si],m[sj]=vj,vi; nw=score(m,inscs,bigs); d=nw-cur
        if d>0 or rng.random()<math.exp(d/max(T,1e-10)):
            cur=nw
            if nw>bs: bs=nw; best=dict(m)
        else: m[si],m[sj]=vi,vj
    return best,bs

def null_test(m, inscs, bigs, n=1000, seed=99):
    rng=random.Random(seed); obs=score(m,inscs,bigs)
    ks=list(m.keys()); vs=list(m.values()); ns=[]
    for _ in range(n):
        sh=vs[:]; rng.shuffle(sh)
        ns.append(score(dict(zip(ks,sh)),inscs,bigs))
    nm=sum(ns)/len(ns); nstd=math.sqrt(sum((s-nm)**2 for s in ns)/len(ns))
    z=(obs-nm)/nstd if nstd else 0.0
    p=sum(1 for s in ns if s>=obs)/n
    ci_lo=sorted(ns)[int(0.025*n)]; ci_hi=sorted(ns)[int(0.975*n)]
    return nm,nstd,z,p,ci_lo,ci_hi

def build_anchors(vocab):
    anchors={}
    pp=json.loads((DATA/"parpola_phonemes.json").read_text("utf-8"))
    for sid,info in pp.get("phoneme_map",{}).items():
        if not isinstance(info,dict): continue
        pv=info.get("phoneme",info.get("phoneme_value",""))
        if pv and info.get("confidence","low") in("high","medium") and "?" not in pv:
            s=_to_syl(pv,vocab)
            if s:
                anchors[sid]=s
                if sid.isdigit(): anchors[sid.zfill(3)]=s
    fa_p=BACKEND_REPORTS/"INDUS_FINAL_ANCHORS.json"
    if fa_p.exists():
        for m_id,info in json.loads(fa_p.read_text("utf-8")).get("anchors",{}).items():
            if info.get("confidence") not in("HIGH","MEDIUM"): continue
            r=info.get("reading","")
            if "?" in r: continue
            s=_to_syl(r,vocab)
            if not s: continue
            anchors[m_id]=s
            if m_id.startswith("M") and m_id[1:].isdigit(): anchors[m_id[1:]]=s
    xw_p=DATA/"mahadevan_parpola_crosswalk_v2.json"
    if xw_p.exists():
        for m_id,entry in json.loads(xw_p.read_text("utf-8")).get("crosswalk",{}).items():
            ph=entry.get("phoneme",""); conf=entry.get("confidence","LOW")
            if conf.upper() not in("HIGH","MEDIUM") or "?" in ph: continue
            s=_to_syl(ph,vocab)
            if not s: continue
            anchors[m_id]=s
            bare=m_id[1:] if m_id.startswith("M") and m_id[1:].isdigit() else m_id
            if bare not in anchors: anchors[bare]=s
    return anchors

# ════════════════════════════════════════════════════════════════════════════════
print("="*65); print("Phase-40: Loading data...")

# Load equalized LMs
skt_b, skt_r = load_lm("sanskrit_syllable_lm.json")
N_SYL, N_BIG = len(skt_r), len(skt_b)  # 424, 651
drav_b_full, drav_r_full = load_lm("dravidian_syllable_lm.json")
drav_r_eq = drav_r_full[:N_SYL]
drav_vocab_eq = set(drav_r_eq)
drav_b_all = {(a,b):lp for(a,b),lp in drav_b_full.items() if a in drav_vocab_eq and b in drav_vocab_eq}
drav_b_eq = dict(sorted(drav_b_all.items(),key=lambda x:-x[1])[:N_BIG])
print(f"Equalized LMs: Dravidian {N_SYL} syl/{N_BIG} bg | Sanskrit {N_SYL} syl/{N_BIG} bg")

# ════════════════════════════════════════════════════════════════════════════════
# EXP A — Corpus status audit
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65); print("EXP A: Corpus status audit")

# Load M77 baseline (for comparison)
from glossa_lab.data.indus_m77 import get_corpus_inscriptions as m77_inscs, get_corpus_symbols as m77_syms
m77_inscriptions = m77_inscs()
m77_sf = Counter(m77_syms())
m77_cipher = [s for s,c in m77_sf.items() if c>=3]
print(f"M77 baseline:  {len(m77_inscriptions)} inscriptions | {sum(len(i) for i in m77_inscriptions)} tokens | {len(m77_cipher)} signs (freq>=3)")

# Load expanded corpus v2
from glossa_lab.data.indus_corpus_v2 import load_corpus as load_v2, corpus_status
v2_raw = load_v2()  # list[list[int]]
# Convert int IDs to zero-padded strings (matching M77 format "047")
v2_inscriptions = [[str(s).zfill(3) for s in seq if s > 0] for seq in v2_raw if len(seq) >= 2]
v2_sf = Counter(s for insc in v2_inscriptions for s in insc)
v2_cipher = [s for s,c in v2_sf.items() if c>=3]
status = corpus_status()
print(f"V2 corpus:     {len(v2_inscriptions)} inscriptions | {sum(len(i) for i in v2_inscriptions)} tokens | {len(v2_cipher)} signs (freq>=3)")
print(f"  Tier: {status.get('tier','?')[:80]}")
print(f"  Coverage: {status.get('coverage_texts_pct','?')}% texts, {status.get('coverage_tokens_pct','?')}% tokens")
print(f"  Multiplier vs M77: {len(v2_inscriptions)/max(len(m77_inscriptions),1):.2f}x inscriptions, {sum(len(i) for i in v2_inscriptions)/max(sum(len(i) for i in m77_inscriptions),1):.2f}x tokens")

exp_a = {
    "experiment": "Phase-40 A: Corpus status audit",
    "m77_baseline": {"inscriptions": len(m77_inscriptions), "tokens": sum(len(i) for i in m77_inscriptions),
                     "signs_freq3": len(m77_cipher)},
    "v2_expanded": {"inscriptions": len(v2_inscriptions), "tokens": sum(len(i) for i in v2_inscriptions),
                    "signs_freq3": len(v2_cipher), "tier": status.get("tier","?")[:100]},
    "multiplier_inscriptions": round(len(v2_inscriptions)/max(len(m77_inscriptions),1),2),
    "multiplier_tokens": round(sum(len(i) for i in v2_inscriptions)/max(sum(len(i) for i in m77_inscriptions),1),2),
    "coverage_texts_pct": status.get("coverage_texts_pct",0),
    "_citation": {"primary":["A.1","I.1","I.2","I.3","I.4","I.5"],"phase":"Phase-40-A"},
}
(REPORTS/"phase40_a_corpus_audit.json").write_text(json.dumps(exp_a,indent=2,ensure_ascii=False),"utf-8")
print(f"Saved phase40_a_corpus_audit.json")

# ════════════════════════════════════════════════════════════════════════════════
# EXP B — SA T1 with expanded corpus (10 seeds × 60K iters, 1000 null)
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65); print("EXP B: SA T1 with expanded corpus (Phase-36 T1 conditions)")
t0=time.time()

# Use V2 expanded corpus
inscs = v2_inscriptions
sf = v2_sf

drav_anch = build_anchors(drav_vocab_eq)
drav_fixed = {s:r for s,r in drav_anch.items() if s in sf and r in drav_vocab_eq}
drav_free = [s for s in v2_cipher if s not in drav_fixed]
skt_anch = build_anchors(set(skt_r))
skt_fixed = {s:r for s,r in skt_anch.items() if s in sf and r in set(skt_r)}
skt_free = [s for s in v2_cipher if s not in skt_fixed]

print(f"V2 corpus: {len(inscs)} inscriptions | {len(v2_cipher)} signs (freq>=3)")
print(f"Dravidian: {len(drav_fixed)} anchors, {len(drav_free)} free")
print(f"Sanskrit:  {len(skt_fixed)} anchors, {len(skt_free)} free")

N_SEEDS=10; N_ITERS=60_000
print(f"\nRunning Dravidian SA: {N_SEEDS}×{N_ITERS}...")
dr_res=[]
for seed in range(N_SEEDS):
    m,s=run_sa(drav_fixed,drav_free,drav_r_eq,inscs,drav_b_eq,N_ITERS,seed)
    dr_res.append((s,m)); print(f"  Drav seed {seed}: {s:.1f}")
dr_bs,dr_bm=max(dr_res,key=lambda x:x[0])
dr_nm,dr_nstd,dr_z,dr_p,dr_ci_lo,dr_ci_hi=null_test(dr_bm,inscs,drav_b_eq,n=1000)
dr_lift=(dr_bs-dr_nm)/max(1,len(inscs))
print(f"Dravidian: Z={dr_z:.2f}, p={dr_p:.4f}, lift={dr_lift:.4f}, 95%CI=[{dr_ci_lo:.1f},{dr_ci_hi:.1f}]")

print(f"\nRunning Sanskrit SA: {N_SEEDS}×{N_ITERS}...")
sk_res=[]
for seed in range(N_SEEDS):
    m,s=run_sa(skt_fixed,skt_free,skt_r,inscs,skt_b,N_ITERS,seed)
    sk_res.append((s,m)); print(f"  Skt  seed {seed}: {s:.1f}")
sk_bs,sk_bm=max(sk_res,key=lambda x:x[0])
sk_nm,sk_nstd,sk_z,sk_p,sk_ci_lo,sk_ci_hi=null_test(sk_bm,inscs,skt_b,n=1000)
sk_lift=(sk_bs-sk_nm)/max(1,len(inscs))
print(f"Sanskrit:  Z={sk_z:.2f}, p={sk_p:.4f}, lift={sk_lift:.4f}, 95%CI=[{sk_ci_lo:.1f},{sk_ci_hi:.1f}]")

dw=dr_lift>sk_lift; ratio=dr_lift/max(abs(sk_lift),0.001)
print(f"\nDravidian wins: {dw} (ratio {ratio:.4f}x) | Runtime {time.time()-t0:.0f}s")

exp_b = {
    "experiment": "Phase-40 B: SA with expanded corpus (V2, 10x60K, 1000null)",
    "corpus_size": len(inscs), "corpus_tokens": sum(len(i) for i in inscs),
    "n_cipher_signs": len(v2_cipher), "n_seeds": N_SEEDS, "n_iters": N_ITERS,
    "dravidian": {"n_anchors":len(drav_fixed),"best_score":round(dr_bs,3),
                  "null_mean":round(dr_nm,3),"null_std":round(dr_nstd,3),
                  "z_score":round(dr_z,3),"p_value":round(dr_p,4),
                  "nll_lift":round(dr_lift,4),"ci95":[round(dr_ci_lo,1),round(dr_ci_hi,1)],
                  "seed_scores":[round(s,1) for s,_ in dr_res]},
    "sanskrit":  {"n_anchors":len(skt_fixed),"best_score":round(sk_bs,3),
                  "null_mean":round(sk_nm,3),"null_std":round(sk_nstd,3),
                  "z_score":round(sk_z,3),"p_value":round(sk_p,4),
                  "nll_lift":round(sk_lift,4),"ci95":[round(sk_ci_lo,1),round(sk_ci_hi,1)],
                  "seed_scores":[round(s,1) for s,_ in sk_res]},
    "dravidian_wins": dw, "lift_ratio": round(ratio,4),
    "m77_comparison": {"inscriptions":len(m77_inscriptions),"signs_freq3":len(m77_cipher)},
    "verdict": (
        f"Phase-40 B SA with {len(inscs)} inscriptions ({len(inscs)/len(m77_inscriptions):.1f}x M77): "
        f"Dravidian lift={dr_lift:.4f} (Z={dr_z:.2f}) vs Sanskrit lift={sk_lift:.4f} (Z={sk_z:.2f}). "
        f"Dravidian {'WINS' if dw else 'loses'} ({ratio:.3f}x). "
        f"Runtime={time.time()-t0:.0f}s."
    ),
    "_citation": {"primary":["A.1","E.1","C.2","I.1","I.2","I.3","I.4","I.5"],"phase":"Phase-40-B"},
}
(REPORTS/"phase40_b_sa_expanded_corpus.json").write_text(json.dumps(exp_b,indent=2,ensure_ascii=False),"utf-8")
print(f"Saved phase40_b_sa_expanded_corpus.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# EXP C — CNN Augmentation: retrain with 10x data augmentation
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65); print("EXP C: CNN augmentation (10x data augmentation, retrain)")
t0=time.time()

TEMPLATES_DIR = ROOT / "glossa-corpus" / "indus" / "ocr_results" / "glyph_templates"
CNN_OUT = ROOT / "glossa-corpus" / "indus" / "ocr_results" / "glyph_cnn_augmented.pt"
CNN_LOG = ROOT / "glossa-corpus" / "indus" / "ocr_results" / "glyph_cnn_augmented_training.json"

try:
    import torch
    import torch.nn as nn
    import torchvision.transforms as T
    import torchvision.models as tvm
    import cv2, numpy as np
    from torch.utils.data import Dataset, DataLoader

    GLYPH_SIZE = 64
    BATCH_SIZE = 32
    SEED = 42
    EPOCHS = 80
    LR = 1e-3
    UNFREEZE_EPOCH = 40
    AUG_FACTOR = 10  # 10x augmentation via transforms

    # ── Data augmentation pipeline ──────────────────────────────────────────
    train_transform = T.Compose([
        T.ToPILImage(),
        T.RandomRotation(15),
        T.RandomAffine(degrees=0, translate=(0.1,0.1), scale=(0.85,1.15)),
        T.RandomHorizontalFlip(p=0.1),  # light flip (Indus signs are mostly directional)
        T.ColorJitter(brightness=0.3, contrast=0.3),
        T.Resize((GLYPH_SIZE, GLYPH_SIZE)),
        T.ToTensor(),
        T.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5]),
    ])
    val_transform = T.Compose([
        T.ToPILImage(),
        T.Resize((GLYPH_SIZE, GLYPH_SIZE)),
        T.ToTensor(),
        T.Normalize(mean=[0.5,0.5,0.5], std=[0.5,0.5,0.5]),
    ])

    # ── Load glyph templates as training data ──────────────────────────────
    class GlyphTemplateDataset(Dataset):
        def __init__(self, samples, transform, aug_factor=1):
            self.samples = []
            for img_path, class_idx in samples:
                for _ in range(aug_factor):
                    self.samples.append((img_path, class_idx))
            self.transform = transform

        def __len__(self): return len(self.samples)

        def __getitem__(self, idx):
            img_path, class_idx = self.samples[idx]
            img = cv2.imread(str(img_path))
            if img is None:
                img = np.zeros((GLYPH_SIZE, GLYPH_SIZE, 3), dtype=np.uint8)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            return self.transform(img), class_idx

    # Collect all samples (canonical + sample_*.png)
    all_samples = []
    class_dirs = [d for d in TEMPLATES_DIR.iterdir() if d.is_dir()]
    class_to_idx = {d.name: i for i, d in enumerate(sorted(class_dirs))}
    for class_dir in class_dirs:
        idx = class_to_idx[class_dir.name]
        for img_file in class_dir.glob("*.png"):
            all_samples.append((img_file, idx))

    n_classes = len(class_dirs)
    print(f"  Glyph dataset: {len(all_samples)} images, {n_classes} classes")

    if len(all_samples) < 10:
        raise RuntimeError(f"Too few images: {len(all_samples)}")

    # Train/val split by class (80/20 of canonical+samples per class)
    rng = random.Random(SEED)
    train_samples, val_samples = [], []
    for class_dir in class_dirs:
        idx = class_to_idx[class_dir.name]
        imgs = sorted(class_dir.glob("*.png"))
        rng.shuffle(imgs)
        n_val = max(1, int(len(imgs) * 0.2))
        val_samples.extend([(p, idx) for p in imgs[:n_val]])
        train_samples.extend([(p, idx) for p in imgs[n_val:]])

    print(f"  Train: {len(train_samples)} images | Val: {len(val_samples)} images")
    print(f"  With {AUG_FACTOR}x augmentation: {len(train_samples)*AUG_FACTOR} effective training samples")

    train_ds = GlyphTemplateDataset(train_samples, train_transform, aug_factor=AUG_FACTOR)
    val_ds = GlyphTemplateDataset(val_samples, val_transform, aug_factor=1)
    train_dl = DataLoader(train_ds, batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
    val_dl = DataLoader(val_ds, batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

    # ── Model: EfficientNet-B0 with custom head ─────────────────────────────
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"  Device: {device}")

    model = tvm.efficientnet_b0(weights="IMAGENET1K_V1")
    # Replace classifier
    in_features = model.classifier[1].in_features
    model.classifier = nn.Sequential(
        nn.Dropout(p=0.4, inplace=True),
        nn.Linear(in_features, n_classes),
    )
    # Phase 1: freeze backbone
    for param in model.features.parameters():
        param.requires_grad_(False)
    model = model.to(device)

    optimizer = torch.optim.AdamW(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=LR, weight_decay=1e-4
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=EPOCHS)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.1)

    history = []
    best_val_acc = 0.0
    best_epoch = 0

    print(f"  Training {EPOCHS} epochs...")
    for epoch in range(1, EPOCHS + 1):
        # Unfreeze last 2 MBConv blocks at epoch UNFREEZE_EPOCH
        if epoch == UNFREEZE_EPOCH:
            for param in model.features[-3:].parameters():
                param.requires_grad_(True)
            optimizer.add_param_group({
                "params": filter(lambda p: p.requires_grad, model.features.parameters()),
                "lr": LR * 0.1
            })
            print(f"  Epoch {epoch}: unfroze last 3 feature blocks")

        # Train
        model.train()
        train_loss, train_correct, train_total = 0.0, 0, 0
        for imgs, labels in train_dl:
            imgs, labels = imgs.to(device), labels.to(device)
            optimizer.zero_grad()
            out = model(imgs)
            loss = criterion(out, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * imgs.size(0)
            train_correct += (out.argmax(1) == labels).sum().item()
            train_total += imgs.size(0)
        scheduler.step()

        # Validate
        model.eval()
        val_correct, val_total = 0, 0
        with torch.no_grad():
            for imgs, labels in val_dl:
                imgs, labels = imgs.to(device), labels.to(device)
                out = model(imgs)
                val_correct += (out.argmax(1) == labels).sum().item()
                val_total += imgs.size(0)

        train_acc = train_correct / max(train_total, 1)
        val_acc = val_correct / max(val_total, 1)
        train_loss_avg = train_loss / max(train_total, 1)

        h = {"epoch":epoch,"train_loss":round(train_loss_avg,4),
             "train_acc":round(train_acc,4),"val_acc":round(val_acc,4)}
        history.append(h)

        if val_acc > best_val_acc:
            best_val_acc = val_acc
            best_epoch = epoch
            torch.save(model.state_dict(), CNN_OUT)

        if epoch % 10 == 0 or epoch <= 5:
            print(f"  Epoch {epoch:3d}: train_loss={train_loss_avg:.4f} "
                  f"train_acc={train_acc:.3f} val_acc={val_acc:.3f} "
                  f"{'★BEST' if val_acc==best_val_acc else ''}")

    print(f"\n  Best val accuracy: {best_val_acc:.4f} at epoch {best_epoch}")
    print(f"  Previous best (unaugmented): 0.0994")
    improvement = best_val_acc - 0.0994
    print(f"  Improvement: {improvement:+.4f} ({improvement/0.0994*100:+.1f}%)")

    cnn_result = {
        "best_val_accuracy": round(best_val_acc, 4),
        "best_epoch": best_epoch,
        "previous_best": 0.0994,
        "improvement_abs": round(improvement, 4),
        "improvement_pct": round(improvement/0.0994*100, 1),
        "n_classes": n_classes,
        "train_samples_base": len(train_samples),
        "aug_factor": AUG_FACTOR,
        "effective_train_samples": len(train_samples) * AUG_FACTOR,
        "epochs": EPOCHS,
        "unfreeze_epoch": UNFREEZE_EPOCH,
        "history": history,
        "model_path": str(CNN_OUT),
        "_citation": {"primary":["I.8","A.1"],"phase":"Phase-40-C"},
    }

except Exception as exc:
    import traceback
    print(f"  CNN training error: {exc}")
    traceback.print_exc()
    cnn_result = {"error": str(exc), "history": [],
                  "_citation": {"primary":["I.8","A.1"],"phase":"Phase-40-C"}}

CNN_LOG.write_text(json.dumps(cnn_result, indent=2, ensure_ascii=False), "utf-8")
(REPORTS/"phase40_c_cnn_augmented.json").write_text(json.dumps(cnn_result, indent=2, ensure_ascii=False), "utf-8")
print(f"Saved phase40_c_cnn_augmented.json ({time.time()-t0:.1f}s)")

# ════════════════════════════════════════════════════════════════════════════════
# SUMMARY
# ════════════════════════════════════════════════════════════════════════════════
print("\n"+"="*65); print("Phase-40 complete:")
for fn in ["phase40_a_corpus_audit.json","phase40_b_sa_expanded_corpus.json","phase40_c_cnn_augmented.json"]:
    p=REPORTS/fn; sz=p.stat().st_size if p.exists() else 0
    print(f"  {'OK' if p.exists() else 'MISSING'} {fn} ({sz//1024}KB)")

print(f"\nA: V2 corpus {len(v2_inscriptions)} inscriptions ({len(v2_inscriptions)/len(m77_inscriptions):.1f}x M77) | {len(v2_cipher)} signs (freq>=3)")
print(f"B: Dravidian lift={dr_lift:.4f} (Z={dr_z:.2f}) vs Sanskrit lift={sk_lift:.4f} (Z={sk_z:.2f}) | Wins={dw} ratio={ratio:.3f}x")
print(f"C: CNN best val_acc={cnn_result.get('best_val_accuracy','?')} (was 0.0994)")
