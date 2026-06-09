"""Walk through Phase 5 advance flow to verify it completes."""
import json
import urllib.request

def api(method, path, body=None):
    url = f"http://localhost:8001/api/v1{path}"
    data = json.dumps(body).encode() if body else b"{}"
    req = urllib.request.Request(url, data=data, method=method,
                                headers={"Content-Type": "application/json"})
    r = urllib.request.urlopen(req, timeout=30)
    return json.loads(r.read())

# Check initial status
print("=== INITIAL STATUS ===")
s = api("GET", "/phase/status")
print(f"  Phase: {s['current_phase']} ({s['phase_label']})")
print(f"  Remaining: {s['remaining_actions']}")
print(f"  All done: {s['all_done']}")
for a in s["top_actions"]:
    print(f"    [{a['action_type']}] {a['label']}")

# Walk through each advance
for step in range(1, 8):
    print(f"\n=== ADVANCE {step} ===")
    r = api("POST", "/phase/advance")
    print(f"  ok={r['ok']}  type={r['action_type']}")
    print(f"  action: {r['action_taken']}")
    print(f"  msg: {r['message'][:120]}")
    if r["action_type"] == "no_op":
        print("  >> NO MORE ACTIONS — Phase complete!")
        break

# Final status
print("\n=== FINAL STATUS ===")
s = api("GET", "/phase/status")
print(f"  Phase: {s['current_phase']} ({s['phase_label']})")
print(f"  Remaining: {s['remaining_actions']}")
print(f"  All done: {s['all_done']}")
