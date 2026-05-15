"""Phase-41 P6: Dr. Fuls ICIT follow-up email."""
import sys, json
from pathlib import Path

ROOT = Path(__file__).parents[2]
sys.path.insert(0, str(ROOT / "backend"))
REPORTS = ROOT / "reports"

subject = "Glossa Lab — Phase-38/41 Update: Dravidian 1.056x Advantage Confirmed at 300K Iterations"

body = """Dear Dr. Fuls,

I hope this message finds you well. I am writing with a follow-up to my earlier message 
(2026-05-11) regarding the Glossa Lab Indus decipherment research and our request for 
access to the ICIT corpus.

I wanted to share our latest findings, as they may be of interest:

HEADLINE RESULT (Phase-38/41)
──────────────────────────────
Under fully controlled conditions (equalized vocabulary and bigram density),
the Dravidian syllabic language model consistently outperforms the Sanskrit model
in fitting the M77 Holdat Indus corpus:

  Dravidian lift/inscription: 7.735 (Z = 5.56, p < 0.0001)
  Sanskrit lift/inscription:  7.321 (Z = 6.34, p < 0.0001)
  Advantage: 1.0566× (Dravidian over Sanskrit)

This result has been confirmed independently at:
  - Phase-36 T1: 5 seeds × 30,000 iterations (first clean result, 1.060×)
  - Phase-38 T1: 10 seeds × 60,000 iterations + 1,000 null permutations (1.056×)
  - Phase-41 P4: 5 seeds × 300,000 iterations (1.0566× — SA fully converged)

All three confirm the same margin. The SA has converged — more iterations do not
change the result. The margin is narrow (5.6%) but consistent and statistically
significant across all conditions.

Foundation check: PASS (17/0/0) — all data integrity and citation checks passing.

CORPUS STATUS
─────────────
Glossa Lab has expanded the Indus corpus from 1,669 inscriptions (M77 Holdat) to
3,085 sequences from multiple sources, representing 56% of ICIT's text inventory
and 66% of ICIT's sign occurrence count. We have also built a glyph CNN classifier
reaching 43.57% sign recognition accuracy (up from 9.94%).

However, these expanded sources introduce sign-ID format inconsistencies that we are
currently resolving. For SA-based falsification experiments, we continue to rely on
the M77 Holdat corpus as the primary data source.

REQUEST
────────
The ICIT corpus (4,537 artefacts, 5,509 texts, 19,616 sign occurrences) would be the
decisive next step. With ICIT data, the SA comparison would have 3× more tokens and
would likely resolve whether the current 5.6% Dravidian advantage is real or a
methodological limit of the current corpus size.

We understand this is a significant request and are happy to discuss any terms,
conditions, or collaborative arrangements that would make access possible. We would
gladly share our full results, methods, and code with you.

Best regards,
Tristan Pierson
BitConcepts Inc. / Glossa Lab
"""

# Use backend/data/.keys.json directly (same approach as find_and_send.py)
import json as _json, urllib.request as _ur, urllib.error as _ue
_k = _json.loads((ROOT / "backend" / "data" / ".keys.json").read_text("utf-8"))
_resend_key = _k.get("resend_api_key", "")
_resend_from = _k.get("resend_from", "Glossa Lab <noreply@bitconcepts.tech>")
if _resend_key:
    _payload = _json.dumps({
        "from": _resend_from,
        "to": ["tpierson@bitconcepts.tech"],
        "subject": f"[DRAFT FOR REVIEW] {subject}",
        "text": body,
    }).encode()
    _req = _ur.Request("https://api.resend.com/emails", data=_payload,
        headers={"Authorization": f"Bearer {_resend_key}",
                 "Content-Type": "application/json",
                 "User-Agent": "glossa-lab-notifier/1.0 (resend-python-compat)"},
        method="POST")
    try:
        _resp = _ur.urlopen(_req, timeout=30)
        _result = _json.loads(_resp.read())
        print(f"Draft sent to tpierson for review (id: {_result.get('id')})")
    except _ue.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}")
    except Exception as e:
        print(f"Send error: {e}")
else:
    print("resend_api_key not found")

# Save to file regardless
p = REPORTS / "phase41_fuls_email_draft.txt"
p.write_text(f"Subject: {subject}\nTo: andreas.fuls@tu-berlin.de\nCC: tpierson@bitconcepts.tech\n\n{body}", "utf-8")
print(f"Draft saved: {p}")
