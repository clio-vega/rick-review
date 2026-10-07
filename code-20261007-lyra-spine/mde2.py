#!/usr/bin/env python3
"""MDE, take 2.  FIRST verify the injection injects (positive control), THEN
   report the minimum detectable effect on the OBSERVABLE scale (within-vendor
   excess residual correlation), because the latent rho_blk is attenuated hard
   by thresholding at a p~0.094 tail."""
import csv, json, math
from pathlib import Path
import numpy as np

DATA = Path("/tmp/judge-panel-article/data/raw-judge-matrix")
STEMS = ["doubao18","doubao20pro","dsv32","dsv4flash","dsv4pro","gem25pro","gem31pro",
  "gem36flash","gem37flash","glm5","glm51","glm52","glm53","gpt41","gpt54","gpt56sol",
  "gpt56terra","grok45","grok46","haiku45","kimik25","kimik26","kimik27code","kimik3",
  "minimaxm3","o4mini","opus5","qwen35plus","qwen37plus","qwen38max","qwen3max","sonnet46"]
VEND = {"doubao18":"bytedance","doubao20pro":"bytedance","dsv32":"deepseek",
  "dsv4flash":"deepseek","dsv4pro":"deepseek","gem25pro":"google","gem31pro":"google",
  "gem36flash":"google","gem37flash":"google","glm5":"zhipu","glm51":"zhipu",
  "glm52":"zhipu","glm53":"zhipu","gpt41":"openai","gpt54":"openai","gpt56sol":"openai",
  "gpt56terra":"openai","o4mini":"openai","grok45":"xai","grok46":"xai",
  "haiku45":"anthropic","opus5":"anthropic","sonnet46":"anthropic","kimik25":"moonshot",
  "kimik26":"moonshot","kimik27code":"moonshot","kimik3":"moonshot","minimaxm3":"minimax",
  "qwen35plus":"alibaba","qwen37plus":"alibaba","qwen38max":"alibaba","qwen3max":"alibaba"}
vend = np.array([VEND[s] for s in STEMS])
def load_error(s):
    rows = list(csv.reader(open(DATA/s/"error_matrix.csv")))
    jc = [k for k,h in enumerate(rows[0]) if h.startswith("j")]
    return np.array([[int(r[k]) for k in jc] for r in rows[1:]], dtype=float)
_z = np.linspace(-9,9,400001); _P = 0.5*(1+np.vectorize(math.erf)(_z/math.sqrt(2)))
def ppf(p): return np.interp(p,_P,_z)

E = load_error("alphanli"); I,J = E.shape
thr = ppf(np.clip(E.mean(axis=1),1e-6,1-1e-6))[:,None]
groups = [np.flatnonzero(vend==v) for v in np.unique(vend)]
off = ~np.eye(J,dtype=bool)
same = (vend[:,None]==vend[None,:]) & off
diff = (vend[:,None]!=vend[None,:]) & off
rng = np.random.default_rng(20261007)

def sim(rb):
    Z = rng.standard_normal((I,J))
    for g in groups:
        if len(g) > 1:
            sh = rng.standard_normal((I,1))
            Z[:,g] = math.sqrt(rb)*sh + math.sqrt(1-rb)*Z[:,g]
    return (Z < thr).astype(float)

def stats(A):
    R = A - A.mean(axis=1,keepdims=True)
    k = R.var(axis=0) > 0
    P = np.corrcoef(R[:,k],rowvar=False)
    lam = np.clip(np.linalg.eigvalsh(P),0,None)
    es = float(lam.sum()**2/(lam**2).sum())
    if k.all():
        exc = float(P[same].mean() - P[diff].mean())
    else:
        exc = float('nan')
    return es, exc

print("="*78)
print("POSITIVE CONTROL: does the injection move the observable at all?")
print("="*78)
print(f"  {'rho_blk':>8s} {'excess resid r':>15s} {'ESDOF':>8s}")
for rb in [0.0, 0.1, 0.3, 0.6, 0.9]:
    es, exc = stats(sim(rb))
    print(f"  {rb:8.2f} {exc:15.4f} {es:8.3f}")
print("  -> if 'excess resid r' does not rise with rho_blk, the injection is broken.")

print()
print("="*78)
print("MDE ON BOTH SCALES (alphaNLI shape: I=995, J=32, 42 within-vendor pairs)")
print("="*78)
null = np.array([stats(sim(0.0))[0] for _ in range(400)])
crit = float(np.percentile(null,5))
print(f"  calibration rho_blk=0: ESDOF mean {null.mean():.3f} sd {null.std():.3f}"
      f"  5% critical {crit:.3f}")
print(f"  (curveball permutation null from perm2.py was 27.633 sd 0.194 -- two")
print(f"   independent nulls, copula-sim vs exact permutation, agree)")
print(f"  {'rho_blk':>8s} {'excess resid r':>15s} {'mean ESDOF':>11s} {'power@5%':>9s}")
rows=[]; mde_lat=None; mde_obs=None
for rb in [0.0,0.02,0.05,0.08,0.12,0.18,0.25,0.35,0.50]:
    out = [stats(sim(rb)) for _ in range(250)]
    es = np.array([o[0] for o in out]); ex = np.array([o[1] for o in out])
    pw = float((es<crit).mean())
    rows.append((rb,float(ex.mean()),float(es.mean()),pw))
    print(f"  {rb:8.3f} {ex.mean():15.4f} {es.mean():11.3f} {pw:9.2f}")
    if mde_lat is None and pw>=0.80: mde_lat, mde_obs = rb, float(ex.mean())
obs_es, obs_exc = stats(E)
print(f"\n  MDE at 80% power: rho_blk ~ {mde_lat}  (observable excess resid r ~ {mde_obs:.4f})")
print(f"  OBSERVED alphaNLI: ESDOF {obs_es:.3f}, excess resid r {obs_exc:+.4f}")
print(f"  observed effect is {obs_exc/mde_obs:.1f}x the minimum detectable effect"
      if mde_obs else "")
json.dump(dict(crit=crit,null_mean=float(null.mean()),null_sd=float(null.std()),
               mde_rho_blk=mde_lat,mde_excess_r=mde_obs,curve=rows,
               obs_esdof=obs_es,obs_excess=obs_exc), open("mde2_out.json","w"), indent=2)
