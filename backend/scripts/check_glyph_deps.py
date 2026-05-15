"""Verify all glyph classifier dependencies are installed."""
import sys
results = []
for mod, name in [("torch","PyTorch"),("torchvision","torchvision"),("sklearn","scikit-learn"),
                  ("scipy","scipy"),("cv2","opencv"),("PIL","Pillow"),("numpy","numpy")]:
    try:
        m = __import__(mod)
        ver = getattr(m, "__version__", "ok")
        results.append(f"  {name}: {ver}")
    except ImportError:
        results.append(f"  {name}: MISSING")
        sys.exit(1)
print("=== Glyph classifier deps ===")
for r in results: print(r)
print("All OK")
