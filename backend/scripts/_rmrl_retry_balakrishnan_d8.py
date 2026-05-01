"""Retry Balakrishnan (now with code BK) + d8 notebook."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rmrl_scrape_all import scrape_notebooks, scrape_research_papers

print("=== Retry Balakrishnan (code BK) ===")
br = scrape_research_papers("balakrishnan")
print(f"  Total: {br['n_succeeded']} OK, {br['n_failed']} failed, "
      f"{br['n_with_ocr_text']} with OCR")
print()
print("=== Retry d8 only ===")
nb = scrape_notebooks(8, 8)
print(f"  Total: {nb['n_succeeded']} OK, {nb['n_failed']} failed")
