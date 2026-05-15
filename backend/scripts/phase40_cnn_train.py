"""Phase-40 EXP C: CNN augmentation training only (standalone)."""
import json, random, sys
from pathlib import Path
import torch, torch.nn as nn
import torchvision.transforms as T, torchvision.models as tvm
import cv2, numpy as np
from torch.utils.data import Dataset, DataLoader

ROOT = Path(__file__).parents[2]
REPORTS = ROOT / "reports"
TEMPLATES_DIR = ROOT / "glossa-corpus" / "indus" / "ocr_results" / "glyph_templates"
CNN_OUT = ROOT / "glossa-corpus" / "indus" / "ocr_results" / "glyph_cnn_augmented.pt"
CNN_LOG = ROOT / "glossa-corpus" / "indus" / "ocr_results" / "glyph_cnn_augmented_training.json"

GLYPH_SIZE, BATCH_SIZE, SEED, EPOCHS, LR, UNFREEZE_EPOCH, AUG_FACTOR = 64, 32, 42, 80, 1e-3, 40, 10

train_tfm = T.Compose([
    T.ToPILImage(),
    T.RandomRotation(15),
    T.RandomAffine(degrees=0, translate=(0.1,0.1), scale=(0.85,1.15)),
    T.RandomHorizontalFlip(p=0.1),
    T.ColorJitter(brightness=0.3, contrast=0.3),
    T.Resize((GLYPH_SIZE,GLYPH_SIZE)), T.ToTensor(),
    T.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5]),
])
val_tfm = T.Compose([
    T.ToPILImage(), T.Resize((GLYPH_SIZE,GLYPH_SIZE)), T.ToTensor(),
    T.Normalize([0.5,0.5,0.5],[0.5,0.5,0.5]),
])

class GlyphDS(Dataset):
    def __init__(self, samples, tfm, aug=1):
        self.samples = [(p,c) for p,c in samples for _ in range(aug)]
        self.tfm = tfm
    def __len__(self): return len(self.samples)
    def __getitem__(self, i):
        p,c = self.samples[i]
        img = cv2.imread(str(p))
        if img is None: img = np.zeros((GLYPH_SIZE,GLYPH_SIZE,3), dtype=np.uint8)
        return self.tfm(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)), c

class_dirs = sorted([d for d in TEMPLATES_DIR.iterdir() if d.is_dir()])
c2i = {d.name:i for i,d in enumerate(class_dirs)}
n_classes = len(class_dirs)
rng = random.Random(SEED)
train_s, val_s = [], []
for cd in class_dirs:
    imgs = sorted(cd.glob("*.png")); rng.shuffle(imgs)
    nv = max(1,int(len(imgs)*0.2))
    val_s += [(p,c2i[cd.name]) for p in imgs[:nv]]
    train_s += [(p,c2i[cd.name]) for p in imgs[nv:]]

print(f"Dataset: {len(train_s)+len(val_s)} images | {n_classes} classes | train={len(train_s)} val={len(val_s)}")
print(f"With {AUG_FACTOR}x aug: {len(train_s)*AUG_FACTOR} effective train samples")

# ── GPU enforcement: always use GPU; only fall back to CPU if no CUDA available ──
if torch.cuda.is_available():
    device = torch.device("cuda")
    print(f"Device: CUDA — {torch.cuda.get_device_name(0)} ({torch.cuda.get_device_properties(0).total_memory//1024**2} MB VRAM)")
else:
    import warnings
    warnings.warn(
        "CUDA not available — training on CPU will be ~20x slower. "
        "Install torch with CUDA: pip install torch torchvision --index-url https://download.pytorch.org/whl/cu126",
        stacklevel=2,
    )
    device = torch.device("cpu")
    print(f"Device: CPU (CUDA not available — install CUDA PyTorch for GPU training)")

train_dl = DataLoader(GlyphDS(train_s,train_tfm,AUG_FACTOR), batch_size=BATCH_SIZE, shuffle=True, num_workers=0)
val_dl   = DataLoader(GlyphDS(val_s,val_tfm,1),   batch_size=BATCH_SIZE, shuffle=False, num_workers=0)

model = tvm.efficientnet_b0(weights="IMAGENET1K_V1")
model.classifier = nn.Sequential(nn.Dropout(0.4,True), nn.Linear(model.classifier[1].in_features, n_classes))
for p in model.features.parameters(): p.requires_grad_(False)
model = model.to(device)

opt = torch.optim.AdamW(filter(lambda p: p.requires_grad, model.parameters()), lr=LR, weight_decay=1e-4)
sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, T_max=EPOCHS)
crit = nn.CrossEntropyLoss(label_smoothing=0.1)
history, best_val, best_ep = [], 0.0, 0

for ep in range(1, EPOCHS+1):
    if ep == UNFREEZE_EPOCH:
        for p in model.features[-3:].parameters(): p.requires_grad_(True)
        opt.add_param_group({"params": filter(lambda p: p.requires_grad, model.features.parameters()), "lr": LR*0.1})
        print(f"Epoch {ep}: backbone last 3 blocks unfrozen")

    model.train(); tl, tc, tt = 0.0, 0, 0
    for imgs,labels in train_dl:
        imgs,labels = imgs.to(device),labels.to(device)
        opt.zero_grad(); out = model(imgs); loss = crit(out,labels)
        loss.backward(); opt.step()
        tl+=loss.item()*imgs.size(0); tc+=(out.argmax(1)==labels).sum().item(); tt+=imgs.size(0)
    sched.step()
    model.eval(); vc,vt = 0,0
    with torch.no_grad():
        for imgs,labels in val_dl:
            imgs,labels = imgs.to(device),labels.to(device)
            vc+=(model(imgs).argmax(1)==labels).sum().item(); vt+=imgs.size(0)
    ta,va,tla = tc/max(tt,1),vc/max(vt,1),tl/max(tt,1)
    history.append({"epoch":ep,"train_loss":round(tla,4),"train_acc":round(ta,4),"val_acc":round(va,4)})
    if va>best_val: best_val=va; best_ep=ep; torch.save(model.state_dict(),CNN_OUT)
    if ep%10==0 or ep<=5:
        print(f"  Ep {ep:3d}: loss={tla:.4f} train={ta:.3f} val={va:.3f} {'★' if va==best_val else ''}")

imp = best_val - 0.0994
print(f"\nBest: {best_val:.4f} at epoch {best_ep} | Previous: 0.0994 | Improvement: {imp:+.4f} ({imp/0.0994*100:+.1f}%)")

result = {"best_val_accuracy":round(best_val,4),"best_epoch":best_ep,"previous_best":0.0994,
          "improvement_abs":round(imp,4),"improvement_pct":round(imp/0.0994*100,1),
          "n_classes":n_classes,"train_samples_base":len(train_s),"aug_factor":AUG_FACTOR,
          "effective_train":len(train_s)*AUG_FACTOR,"epochs":EPOCHS,"history":history,
          "_citation":{"primary":["I.8","A.1"],"phase":"Phase-40-C"}}
CNN_LOG.write_text(json.dumps(result,indent=2),"utf-8")
(REPORTS/"phase40_c_cnn_augmented.json").write_text(json.dumps(result,indent=2),"utf-8")
print(f"Saved: glyph_cnn_augmented.pt + phase40_c_cnn_augmented.json")
