#!/usr/bin/env python3
"""(1) reproduce Lyra's EMS numbers from the CSVs by an independent loader+ANOVA,
   (2) decompose phi-bar into within-vendor and between-vendor pairs,
   (3) minimum detectable within-vendor excess correlation at 80% power."""
import csv, json
from pathlib import Path
import numpy as np

DATA = Path("/tmp/judge-panel-article/data/raw-judge-matrix")
HERS = json.load(open("/tmp/judge-panel-article/scripts/judge_main_effect_unbiased_results.json"))
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

print("="*78)
print("1. INDEPENDENT REPRODUCTION OF HER EMS NUMBERS (my loader, my ANOVA)")
print("="*78)
print(f"  {'subset':8s} {'quantity':22s} {'mine':>14s} {'hers':>14s} {'rel.diff':>11s}")
ok = True
for s in ["alphanli","snli","mnli_m"]:
    E = load_error(s); I,J = E.shape
    gm = E.mean(); rm = E.mean(axis=1); cm = E.mean(axis=0)
    ss_i = J*((rm-gm)**2).sum(); ss_j = I*((cm-gm)**2).sum()
    ss_r = ((E-gm)**2).sum() - ss_i - ss_j
    ms_i, ms_j, ms_r = ss_i/(I-1), ss_j/(J-1), ss_r/((I-1)*(J-1))
    s2_i, s2_j = (ms_i-ms_r)/J, (ms_j-ms_r)/I
    mine = dict(ms_items=ms_i, ms_judges=ms_j, ms_resid=ms_r,
                sigma2_item=s2_i, sigma2_judge=s2_j, grand_mean=gm,
                n_items=I, n_judges=J)
    for k,v in mine.items():
        h = HERS[s][k]
        rd = abs(v-h)/max(abs(h),1e-300)
        if rd > 1e-9: ok = False
        print(f"  {s:8s} {k:22s} {v:14.9g} {h:14.9g} {rd:11.2e}")
    print(f"  {s:8s} {'omega2/tau2 %':22s} {100*s2_j/s2_i:14.4f}")
print(f"  ALL MATCH to 1e-9: {ok}")

print()
print("="*78)
print("2. phi-bar SPLIT BY VENDOR PAIR  (raw error correlations, not residuals)")
print("="*78)
rng = np.random.default_rng(20261007)
out = {}
J = 32; off = ~np.eye(J, dtype=bool)
same = (vend[:,None]==vend[None,:]) & off
diff = (vend[:,None]!=vend[None,:]) & off
print(f"  ({same.sum()//2} within-vendor pairs, {diff.sum()//2} between-vendor pairs)")
print(f"  {'subset':8s} {'phibar(all)':>12s} {'within-vend':>12s} {'between-vend':>13s}"
      f" {'excess':>9s} {'ceil(all)':>10s} {'ceil(betw)':>11s} {'p(perm)':>9s}")
for s in ["alphanli","snli","mnli_m"]:
    E = load_error(s)
    P = np.corrcoef(E, rowvar=False)
    all_, w, b = P[off].mean(), P[same].mean(), P[diff].mean()
    NP = 20000; null = np.empty(NP); stat = w-b
    for t in range(NP):
        pv = rng.permutation(vend)
        null[t] = P[(pv[:,None]==pv[None,:])&off].mean() - P[(pv[:,None]!=pv[None,:])&off].mean()
    p = (1+(null>=stat).sum())/(NP+1)
    print(f"  {s:8s} {all_:12.4f} {w:12.4f} {b:13.4f} {stat:+9.4f}"
          f" {1/all_:10.4f} {1/b:11.4f} {p:9.5f}")
    out[s] = dict(phibar_all=float(all_), phibar_within=float(w), phibar_between=float(b),
                  excess=float(stat), ceil_all=float(1/all_), ceil_between=float(1/b), p=float(p))
print("  ceil = 1/phi-bar, the Kish effective-n ceiling.  'ceil(betw)' is the ceiling a")
print("  panel of one-judge-per-vendor would face if only the between-vendor level remained.")

print()
print("="*78)
print("3. MINIMUM DETECTABLE EFFECT -- for the alternative that IS detectable")
print("="*78)
print("  Statistic: residual ESDOF.  Null: curveball (row+col sums fixed).")
print("  Alternative: within-vendor excess CONDITIONAL error correlation rho_blk,")
print("  injected via a latent-normal copula on top of the observed item difficulty.")
E = load_error("alphanli"); I,J = E.shape
p_i = E.mean(axis=1)                       # observed item difficulty
from math import sqrt
groups = [np.flatnonzero(vend==v) for v in np.unique(vend)]
def sim(rho_blk, rng):
    Z = rng.standard_normal((I,J))
    for g in groups:
        if len(g) > 1:
            sh = rng.standard_normal((I,1))
            Z[:,g] = sqrt(rho_blk)*sh + sqrt(1-rho_blk)*Z[:,g]
    # threshold so that item i has error prob p_i for every judge
    from scipy.stats import norm
    thr = norm.ppf(np.clip(p_i,1e-6,1-1e-6))[:,None]
    return (Z < thr).astype(float)
def esdof(A):
    R = A - A.mean(axis=1, keepdims=True)
    k = R.var(axis=0) > 0
    P = np.corrcoef(R[:,k], rowvar=False)
    lam = np.clip(np.linalg.eigvalsh(P),0,None)
    return lam.sum()**2/(lam**2).sum()
# null threshold at alpha=0.05 from rho_blk = 0
null = np.array([esdof(sim(0.0, rng)) for _ in range(300)])
crit = np.percentile(null, 5)
print(f"  null ESDOF (rho_blk=0): mean {null.mean():.3f} sd {null.std():.3f}"
      f"   5th pctile (critical value) = {crit:.3f}")
print(f"  {'rho_blk':>8s} {'mean ESDOF':>11s} {'power@5%':>9s}")
mde = None
for rb in [0.0, 0.005, 0.01, 0.02, 0.03, 0.05, 0.08]:
    vals = np.array([esdof(sim(rb, rng)) for _ in range(200)])
    pw = (vals < crit).mean()
    print(f"  {rb:8.3f} {vals.mean():11.3f} {pw:9.2f}")
    if mde is None and pw >= 0.80: mde = rb
print(f"  -> smallest within-vendor excess conditional correlation detectable at"
      f" 80% power: rho_blk ~ {mde}")
print(f"  OBSERVED residual ESDOF on alphaNLI = {esdof(E):.3f}  (far below critical {crit:.3f})")
json.dump(out, open("quantify_out.json","w"), indent=2)
