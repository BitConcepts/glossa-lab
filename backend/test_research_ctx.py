import urllib.request, json
with urllib.request.urlopen("http://localhost:8001/api/v1/ai/research-context") as r:
    d = json.load(r)
s = d["summary"]
print(f"Signs assigned: {s['n_assigned_signs']}")
print(f"Token coverage: {s['token_coverage_pct']}%")
print(f"Context length: {s['context_chars']} chars")
print(f"Next step: {s['next_steps'][0][:100] if s['next_steps'] else 'N/A'}")
print(f"\nContext preview (first 500 chars):\n{d['context'][:500]}")
