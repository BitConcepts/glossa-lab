"""Mahadevan 1977 — Glyph CNN Classifier Training.

Fine-tunes EfficientNet-B0 (ImageNet pretrained) on Indus glyph crops.
The frozen feature backbone transfers edge/shape knowledge from ImageNet;
only the 1280→num_classes head is trained by default, making this feasible
with ~1,774 labeled pairs across 226 classes.

Two-phase training (optional via --unfreeze-epoch):
  Phase 1: frozen backbone, only head trained (fast, few epochs)
  Phase 2: last 2 MBConv blocks + head fine-tuned (slower, more epochs)

Data:
  - Exact-match texts only (glyph count == sign count) from Firestore
  - 1,774 labeled (crop, sign_id) pairs, 226 sign classes
  - 80/20 train/val split by textnum to prevent leakage

Output:
  glossa-corpus/indus/ocr_results/glyph_cnn.pt  — checkpoint
  glossa-corpus/indus/ocr_results/glyph_cnn_training.json — training log

Usage:
    shell.cmd python backend/scripts/glyph_train.py
    shell.cmd python backend/scripts/glyph_train.py --epochs 60 --unfreeze-epoch 30
"""
from __future__ import annotations
import json, re, sys, random
from datetime import datetime
from pathlib import Path

import numpy as np
import cv2
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms as T
import torchvision.models as tvm

REPO      = Path(__file__).parents[2]
FIRESTORE = (REPO / "glossa-corpus/indus/sources/rmrl/raw/indusscript-probe"
             / "firestore_indusarrays_full.json")
CROPS_DIR = REPO / "glossa-corpus/indus/ocr_results/glyph_crops"
OUT_DIR   = REPO / "glossa-corpus/indus/ocr_results"
MODEL_OUT = OUT_DIR / "glyph_cnn.pt"
LOG_OUT   = OUT_DIR / "glyph_cnn_training.json"

GLYPH_SIZE     = 64
BATCH_SIZE     = 64
DEFAULT_LR    = 3e-4
DEFAULT_EPOCHS = 60
UNFREEZE_EPOCH = 30     # epoch at which to unfreeze last 2 MBConv blocks
TRAIN_FRAC     = 0.80
SEED           = 42


# ── Model ──────────────────────────────────────────────────────────────

class GlyphCNN(nn.Module):
    """EfficientNet-B0 pretrained backbone + custom classification head.

    Phase 1 (frozen backbone): only head trains — fast, no overfitting.
    Phase 2 (partial unfreeze): last 2 MBConv blocks + head — domain adaptation.
    """

    def __init__(self, num_classes: int):
        super().__init__()
        # Load pretrained EfficientNet-B0
        weights = tvm.EfficientNet_B0_Weights.IMAGENET1K_V1
        backbone = tvm.efficientnet_b0(weights=weights)
        # Replace the classifier head
        in_features = backbone.classifier[1].in_features  # 1280
        backbone.classifier = nn.Sequential(
            nn.Dropout(p=0.4, inplace=True),
            nn.Linear(in_features, num_classes),
        )
        self.backbone = backbone
        self.freeze_backbone()

    def freeze_backbone(self):
        """Freeze all layers except classifier head."""
        for p in self.backbone.features.parameters():
            p.requires_grad = False
        for p in self.backbone.classifier.parameters():
            p.requires_grad = True

    def unfreeze_last_blocks(self, n: int = 2):
        """Unfreeze the last n MBConv blocks + head for fine-tuning."""
        blocks = list(self.backbone.features.children())
        for block in blocks[-n:]:
            for p in block.parameters():
                p.requires_grad = True
        trainable = sum(p.numel() for p in self.parameters() if p.requires_grad)
        total     = sum(p.numel() for p in self.parameters())
        print(f"  Unfroze last {n} blocks: {trainable:,}/{total:,} params trainable")

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # EfficientNet expects 3-channel input; repeat grayscale to 3 channels
        if x.shape[1] == 1:
            x = x.repeat(1, 3, 1, 1)
        return self.backbone(x)


# ── Dataset ───────────────────────────────────────────────────────────────────

def sanitize_sign(s: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '_', s.strip()).lstrip("0") or "0"


def load_labeled_pairs() -> list[tuple[Path, str]]:
    """Build (crop_path, sign_id) list from exact-match texts only."""
    from collections import defaultdict

    # Load Firestore sign sequences
    data = json.loads(FIRESTORE.read_text(encoding="utf-8"))
    by_tn: dict[int, list[list[str]]] = defaultdict(list)
    for doc in data.get("documents", []):
        tn = doc.get("textnum")
        if tn is None:
            continue
        texts = doc.get("texts") or []
        signs = [sanitize_sign(str(s)) for s in texts if str(s).strip()]
        if signs:
            by_tn[int(tn)].append(signs)
    sign_db = {tn: max(seqs, key=len) for tn, seqs in by_tn.items()}

    pairs: list[tuple[Path, str]] = []
    exact_count = 0

    for tn, signs in sorted(sign_db.items()):
        d = CROPS_DIR / str(tn)
        if not d.exists():
            continue
        files = sorted(d.glob("glyph_*.png"))
        if len(files) != len(signs):
            continue            # only exact-match texts
        exact_count += 1
        for f, sid in zip(files, signs):
            pairs.append((f, sid))

    print(f"  Exact-match texts: {exact_count}")
    print(f"  Labeled pairs: {len(pairs)}")
    return pairs


class GlyphDataset(Dataset):
    def __init__(self, pairs: list[tuple[Path, str]],
                 class_to_idx: dict[str, int],
                 augment: bool = False):
        self.pairs = pairs
        self.class_to_idx = class_to_idx
        self.augment = augment

        # Augmentation pipeline (grayscale, no H-flip — Indus signs are directional)
        if augment:
            self.transform = T.Compose([
                T.ToPILImage(),
                T.RandomAffine(degrees=10, translate=(0.05, 0.05),
                               scale=(0.90, 1.10)),
                T.ToTensor(),           # [0, 1] float, shape (1, H, W) after gray squeeze
                T.Lambda(lambda x: x.mean(0, keepdim=True) if x.shape[0] == 3 else x),
                T.Normalize(mean=[0.5], std=[0.5]),
            ])
        else:
            self.transform = T.Compose([
                T.ToPILImage(),
                T.ToTensor(),
                T.Lambda(lambda x: x.mean(0, keepdim=True) if x.shape[0] == 3 else x),
                T.Normalize(mean=[0.5], std=[0.5]),
            ])

    def __len__(self) -> int:
        return len(self.pairs)

    def __getitem__(self, idx: int):
        path, sign_id = self.pairs[idx]
        img = cv2.imread(str(path))
        if img is None:
            img = np.ones((GLYPH_SIZE, GLYPH_SIZE, 3), dtype=np.uint8) * 255
        # Convert to grayscale (keep as 3-ch for ToPILImage, then collapse in transform)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray_3ch = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
        tensor = self.transform(gray_3ch)
        label = self.class_to_idx.get(sign_id, 0)
        return tensor, label


# ── Training ──────────────────────────────────────────────────────────────────

def train_one_epoch(model, loader, optimizer, criterion, device):
    model.train()
    total_loss, correct, total = 0.0, 0, 0
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        optimizer.zero_grad()
        logits = model(X)
        loss = criterion(logits, y)
        loss.backward()
        optimizer.step()
        total_loss += loss.item() * len(y)
        correct += (logits.argmax(1) == y).sum().item()
        total += len(y)
    return total_loss / total, correct / total


@torch.no_grad()
def evaluate(model, loader, criterion, device):
    model.eval()
    total_loss, correct, total = 0.0, 0, 0
    for X, y in loader:
        X, y = X.to(device), y.to(device)
        logits = model(X)
        loss = criterion(logits, y)
        total_loss += loss.item() * len(y)
        correct += (logits.argmax(1) == y).sum().item()
        total += len(y)
    return total_loss / total, correct / total


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--epochs",         type=int,   default=DEFAULT_EPOCHS)
    parser.add_argument("--lr",             type=float, default=DEFAULT_LR)
    parser.add_argument("--batch",          type=int,   default=BATCH_SIZE)
    parser.add_argument("--unfreeze-epoch", type=int,   default=UNFREEZE_EPOCH,
                        dest="unfreeze_epoch",
                        help="Epoch at which to unfreeze last 2 backbone blocks (0=never)")
    args = parser.parse_args()

    random.seed(SEED)
    torch.manual_seed(SEED)
    np.random.seed(SEED)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"=== GlyphCNN Training (EfficientNet-B0) ===")
    print(f"Device: {device}  |  Epochs: {args.epochs}  |  LR: {args.lr}  "
          f"|  Unfreeze@{args.unfreeze_epoch}")

    if not FIRESTORE.exists():
        print(f"ERROR: {FIRESTORE} not found")
        return 1
    if not CROPS_DIR.exists():
        print(f"ERROR: {CROPS_DIR} not found — run glyph_segment.py --all first")
        return 1

    # Build dataset
    print("\nBuilding labeled dataset...")
    all_pairs = load_labeled_pairs()
    if not all_pairs:
        print("ERROR: no labeled pairs found")
        return 1

    # Build class index from all unique sign IDs in the pairs
    sign_ids = sorted(set(sid for _, sid in all_pairs))
    class_to_idx = {sid: i for i, sid in enumerate(sign_ids)}
    idx_to_class = {i: sid for sid, i in class_to_idx.items()}
    num_classes = len(sign_ids)
    print(f"  Sign classes: {num_classes}")

    # Train/val split by textnum prefix (extract textnum from path)
    textnums = sorted(set(int(p.parent.name) for p, _ in all_pairs))
    random.shuffle(textnums)
    split = int(len(textnums) * TRAIN_FRAC)
    train_tns = set(textnums[:split])
    val_tns   = set(textnums[split:])
    train_pairs = [(p, s) for p, s in all_pairs if int(p.parent.name) in train_tns]
    val_pairs   = [(p, s) for p, s in all_pairs if int(p.parent.name) in val_tns]
    print(f"  Train: {len(train_pairs)} samples ({len(train_tns)} texts)")
    print(f"  Val:   {len(val_pairs)}   samples ({len(val_tns)} texts)")

    train_ds = GlyphDataset(train_pairs, class_to_idx, augment=True)
    val_ds   = GlyphDataset(val_pairs,   class_to_idx, augment=False)
    train_ld = DataLoader(train_ds, batch_size=args.batch, shuffle=True,
                          num_workers=0, pin_memory=device.type == "cuda")
    val_ld   = DataLoader(val_ds,   batch_size=args.batch, shuffle=False,
                          num_workers=0)

    # Model, optimizer, scheduler
    print("\nLoading EfficientNet-B0 pretrained weights...")
    model = GlyphCNN(num_classes).to(device)
    total_params  = sum(p.numel() for p in model.parameters())
    train_params  = sum(p.numel() for p in model.parameters() if p.requires_grad)
    print(f"Model: EfficientNet-B0 head  |  "
          f"Trainable: {train_params:,}/{total_params:,}  "
          f"(~{total_params*4/1e6:.0f} MB total)")

    # Only pass trainable params to optimizer
    optimizer = torch.optim.Adam(
        filter(lambda p: p.requires_grad, model.parameters()),
        lr=args.lr, weight_decay=1e-4
    )
    scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
        optimizer, T_max=args.epochs, eta_min=1e-5
    )
    criterion = nn.CrossEntropyLoss()

    # Training loop
    print(f"\n{'Epoch':>5}  {'TrLoss':>7}  {'TrAcc':>6}  {'VaLoss':>7}  {'VaAcc':>6}")
    print("-" * 42)

    history = []
    best_val_acc = 0.0
    best_state = None

    for epoch in range(1, args.epochs + 1):
        # Phase 2: unfreeze last 2 blocks at the specified epoch
        if args.unfreeze_epoch > 0 and epoch == args.unfreeze_epoch:
            print(f"\n[Epoch {epoch}] Phase 2: unfreezing last 2 backbone blocks")
            model.unfreeze_last_blocks(n=2)
            # Rebuild optimizer to include newly unfrozen params at lower LR
            optimizer = torch.optim.Adam([
                {"params": filter(lambda p: p.requires_grad,
                                  model.backbone.features.parameters()),
                 "lr": args.lr * 0.1},    # 10x lower LR for backbone
                {"params": model.backbone.classifier.parameters(),
                 "lr": args.lr},
            ], weight_decay=1e-4)
            scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
                optimizer, T_max=args.epochs - epoch, eta_min=1e-5
            )

        tr_loss, tr_acc = train_one_epoch(model, train_ld, optimizer, criterion, device)
        va_loss, va_acc = evaluate(model, val_ld, criterion, device)
        scheduler.step()

        history.append({
            "epoch": epoch,
            "train_loss": round(tr_loss, 4),
            "train_acc":  round(tr_acc,  4),
            "val_loss":   round(va_loss, 4),
            "val_acc":    round(va_acc,  4),
        })

        if va_acc > best_val_acc:
            best_val_acc = va_acc
            best_state = {k: v.clone() for k, v in model.state_dict().items()}

        if epoch % 10 == 0 or epoch == 1:
            print(f"{epoch:>5}  {tr_loss:>7.4f}  {tr_acc:>6.1%}  "
                  f"{va_loss:>7.4f}  {va_acc:>6.1%}  "
                  f"{'← best' if va_acc == best_val_acc else ''}")

    print(f"\nBest val accuracy: {best_val_acc:.1%}")

    # Save model
    assert best_state is not None
    model.load_state_dict(best_state)
    checkpoint = {
        "model_state_dict": best_state,
        "class_to_idx":     class_to_idx,
        "idx_to_class":     idx_to_class,
        "num_classes":      num_classes,
        "glyph_size":       GLYPH_SIZE,
        "val_accuracy":     round(best_val_acc, 4),
        "trained_at":       datetime.utcnow().isoformat(),
        "epochs_trained":   args.epochs,
        "_citation": {
            "primary_sources": ["I.8", "A.1"],
            "derivation": (
                "GlyphCNN trained on M77 IIIF glyph crops labeled via Firestore "
                f"exact-match alignment. Val acc {best_val_acc:.1%}. "
                "Model weights are corpus artifacts derived from non-committed raw sources."
            ),
        },
    }
    torch.save(checkpoint, MODEL_OUT)
    print(f"Model saved: {MODEL_OUT}  ({MODEL_OUT.stat().st_size / 1e6:.1f} MB)")

    # Save training log
    log = {
        "_citation": {"primary_sources": ["I.8", "A.1"]},
        "generated_at": datetime.utcnow().isoformat(),
        "epochs": args.epochs,
        "lr": args.lr,
        "batch_size": args.batch,
        "num_classes": num_classes,
        "train_samples": len(train_pairs),
        "val_samples":   len(val_pairs),
        "best_val_accuracy": round(best_val_acc, 4),
        "history": history,
    }
    LOG_OUT.write_text(json.dumps(log, indent=2), encoding="utf-8")
    print(f"Log saved: {LOG_OUT}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
