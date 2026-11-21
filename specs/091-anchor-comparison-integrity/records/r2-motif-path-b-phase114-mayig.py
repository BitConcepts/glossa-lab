"""Path B (independent): parse outputs/phase114_full_seal_translations.json all_translations (dict keyed by cisi id)
plus the mayig-CISI layer (data/corpus_layers/mayig_cisi_layer_v1.json, P-numbers) via the empirical
P->M mapping derived from glossa-corpus/indus/exports/indus_open.jsonl (canonical_grapheme_ids vs text_code)."""
import json, collections
d=json.load(open("outputs/phase114_full_seal_translations.json"))
at=d["all_translations"]
seals=list(at.values())
print("phase114 n_seals", len(seals))
targets=["M006","M013","M016","M039","M045","M057","M060","M062","M063","M067","M068","M073","M080","M012","M059","M391"]
out={}
for t in targets:
    ss=[s for s in seals if t in s["signs"]]
    out[t]={"seals_with_sign":len(ss),"tokens":sum(s["signs"].count(t) for s in seals),
            "sites":dict(collections.Counter(s["site"] for s in ss))}
    if t in ("M012","M059","M391"):
        out[t]["len_dist"]=dict(sorted(collections.Counter(s["n_signs"] for s in ss).items()))
        out[t]["pos_first_frac"]=[round(sum(1 for s in ss if s["signs"][0]==t)/len(ss),4) if ss else None]
        out[t]["pos_last_frac"]=[round(sum(1 for s in ss if s["signs"][-1]==t)/len(ss),4) if ss else None]
        out[t]["max_repeat_in_seal"]=max((s["signs"].count(t) for s in ss), default=0)
        out[t]["seals_with_repeat"]=sum(1 for s in ss if s["signs"].count(t)>=2)
out["_pop"]={"n_seals":len(seals),"sites_all":dict(collections.Counter(s["site"] for s in seals))}
# mayig independent representation
rows=[json.loads(l) for l in open("glossa-corpus/indus/exports/indus_open.jsonl")]
p2m={}
for r in rows:
    nums=(r["text_code_diplomatic"] or "").strip("+").split("-")
    for n,g in zip(nums, r["canonical_grapheme_ids"]):
        if g: p2m.setdefault("P"+n.zfill(3), set()).add(g)
may=json.load(open("data/corpus_layers/mayig_cisi_layer_v1.json"))["inscriptions"]
mres={}
for t in ("M012","M059","M391"):
    ps=[p for p,s in p2m.items() if t in s]
    mres[t]={"parpola_ids":sorted(ps),"mayig_seals_with":sum(1 for i in may if any(x in ps for x in i["tokens"])),
             "mayig_tokens":sum(i["tokens"].count(p) for i in may for p in ps),"mayig_n":len(may)}
out["_mayig"]=mres
json.dump(out, open("/tmp/r2motif/path_b.json","w"), indent=1)
print(json.dumps({k:(v["seals_with_sign"],v["tokens"]) for k,v in out.items() if not k.startswith("_")}))
print("mayig", json.dumps(mres))
print("EXIT_OK")
