"""Path A: parse outputs/phase100_full_corpus.json translations (list, with formula_type)."""
import json, collections, sys
d=json.load(open("outputs/phase100_full_corpus.json"))
tr=d["translations"]
print("n_seals_total_field", d["n_seals_total"], "n_translations", len(tr))
targets=["M006","M013","M016","M039","M045","M057","M060","M062","M063","M067","M068","M073","M080","M012","M059","M391"]
out={}
for t in targets:
    seals=[s for s in tr if t in s["signs"]]
    out[t]={"seals_with_sign":len(seals),"tokens":sum(s["signs"].count(t) for s in tr),
            "sites":dict(collections.Counter(s["site"] for s in seals))}
    if t in ("M012","M059","M391"):
        out[t]["len_dist"]=dict(sorted(collections.Counter(s["n_signs"] for s in seals).items()))
        out[t]["formula"]=dict(collections.Counter(s.get("formula_type","?") for s in seals))
        out[t]["pos_first_frac"]=[round(sum(1 for s in seals if s["signs"][0]==t)/len(seals),4) if seals else None]
        out[t]["pos_last_frac"]=[round(sum(1 for s in seals if s["signs"][-1]==t)/len(seals),4) if seals else None]
        out[t]["max_repeat_in_seal"]=max((s["signs"].count(t) for s in seals), default=0)
        out[t]["seals_with_repeat"]=sum(1 for s in seals if s["signs"].count(t)>=2)
# population marginals
out["_pop"]={"n_seals":len(tr),"len_dist_all":dict(sorted(collections.Counter(s["n_signs"] for s in tr).items())),
             "formula_all":dict(collections.Counter(s.get("formula_type","?") for s in tr)),
             "sites_all":dict(collections.Counter(s["site"] for s in tr))}
json.dump(out, open("/tmp/r2motif/path_a.json","w"), indent=1)
print(json.dumps({k:(v["seals_with_sign"],v["tokens"]) for k,v in out.items() if k!="_pop"}))
print("EXIT_OK")
