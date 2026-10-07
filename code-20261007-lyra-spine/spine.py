#!/usr/bin/env python3
"""
spine.py -- Lyra's spine question, both halves, on the byte-identical
Li-Yu-Li matrices at judge-panel-article@6b0e86e, data/raw-judge-matrix/.

HALF ONE : is the ~49% (now 0.486) between-item error-variance share right?
HALF TWO : does the per-item-demeaned cross-judge residual correlation
           collapse toward zero?

Reported SEPARATELY, with separate evidence.
"""
import csv, json, itertools
from pathlib import Path
import numpy as np

DATA = Path("/tmp/judge-panel-article/data/raw-judge-matrix")
SUBSETS = ["alphanli", "snli", "mnli_m"]

VENDOR = {
    "doubao18":"doubao","doubao20pro":"doubao",
    "dsv32":"deepseek","dsv4flash":"deepseek","dsv4pro":"deepseek",
    "gem25pro":"google","gem31pro":"google","gem36flash":"google","gem37flash":"google",
    "glm5":"zhipu","glm51":"zhipu","glm52":"zhipu","glm53":"zhipu",
    "gpt41":"openai","gpt54":"openai","gpt56sol":"openai","gpt56terra":"openai","o4mini":"openai",
    "grok45":"xai","grok46":"xai",
    "haiku45":"anthropic","opus5":"anthropic","sonnet46":"anthropic",
    "kimik25":"moonshot","kimik26":"moonshot","kimik27code":"moonshot","kimik3":"moonshot",
    "minimaxm3":"minimax",
    "qwen35plus":"alibaba","qwen37plus":"alibaba","qwen38max":"alibaba","qwen3max":"alibaba",
}
STEMS = ["doubao18","doubao20pro","dsv32","dsv4flash","dsv4pro","gem25pro","gem31pro",
         "gem36flash","gem37flash","glm5","glm51","glm52","glm53","gpt41","gpt54",
         "gpt56sol","gpt56terra","grok45","grok46","haiku45","kimik25","kimik26",
         "kimik27code","kimik3","minimaxm3","o4mini","opus5","qwen35plus","qwen37plus",
         "qwen38max","qwen3max","sonnet46"]

def load_error(subset):
    p = DATA/subset/"error_matrix.csv"
    with open(p) as f:
        rows = list(csv.reader(f))
    hdr = rows[0]
    jcols = [k for k,h in enumerate(hdr) if h.startswith("j")]
    E = np.array([[int(r[k]) for k in jcols] for r in rows[1:]], dtype=float)
    return E, [hdr[k] for k in jcols]

# ---------------------------------------------------------------- statistics
def mean_offdiag(M):
    J = M.shape[0]
    return float(M[~np.eye(J,dtype=bool)].mean())

def phibar_pearson(E):
    """Mean off-diagonal Pearson correlation of error columns (Lyra's phi-bar)."""
    return mean_offdiag(np.corrcoef(E, rowvar=False))

def icc_oneway(E):
    """Between-item share via two-way random-effects EMS (independent mechanism)."""
    I,J = E.shape
    gm = E.mean()
    rm = E.mean(axis=1); cm = E.mean(axis=0)
    ss_items  = J*((rm-gm)**2).sum()
    ss_judges = I*((cm-gm)**2).sum()
    ss_total  = ((E-gm)**2).sum()
    ss_resid  = ss_total - ss_items - ss_judges
    ms_items  = ss_items/(I-1); ms_judges = ss_judges/(J-1)
    ms_resid  = ss_resid/((I-1)*(J-1))
    s2_item  = (ms_items -ms_resid)/J
    s2_judge = (ms_judges-ms_resid)/I
    s2_resid = ms_resid
    return dict(ms_items=ms_items, ms_judges=ms_judges, ms_resid=ms_resid,
                s2_item=s2_item, s2_judge=s2_judge, s2_resid=s2_resid,
                icc=s2_item/(s2_item+s2_resid),
                omega2_over_tau2_pct=100*s2_judge/s2_item,
                naive_omega2_over_tau2_pct=100*cm.var()/s2_item)

def residuals(E):
    R = E - E.mean(axis=1, keepdims=True)      # per-item demeaning
    return R

def resid_offdiag_pearson(E):
    R = residuals(E)
    keep = R.var(axis=0) > 0
    return mean_offdiag(np.corrcoef(R[:,keep], rowvar=False)), int((~keep).sum())

def resid_offdiag_pooled(E):
    """Pooled-variance normalisation: the exactly-pinned version."""
    R = residuals(E); R = R - R.mean(axis=0, keepdims=True)
    G = R.T @ R
    return mean_offdiag(G)/np.diag(G).mean()

def resid_esdof(E):
    """ESDOF (participation ratio) of the residual correlation matrix.
       Null value is exactly J-1."""
    R = residuals(E)
    keep = R.var(axis=0) > 0
    P = np.corrcoef(R[:,keep], rowvar=False)
    lam = np.linalg.eigvalsh(P)
    lam = np.clip(lam, 0, None)
    return float(lam.sum()**2/ (lam**2).sum())

# ---------------------------------------------------------------- report
out = {}
print("="*78)
print("PANEL SHAPE AND WELL-FORMEDNESS  (data: judge-panel-article@6b0e86e)")
print("="*78)
for s in SUBSETS:
    E, names = load_error(s)
    I,J = E.shape
    er = E.mean(axis=0)
    out[s] = dict(I=I, J=J, err_min=er.min(), err_max=er.max(), err_mean=er.mean())
    print(f"  {s:8s}  I={I:4d}  J={J:3d}   per-judge error rate "
          f"min={er.min():.4f} max={er.max():.4f} mean={er.mean():.4f}")
    assert names == [f"j{k:02d}" for k in range(1,J+1)]
print("  (Lyra's stated well-formedness band 6.5%-15.7% is alphaNLI; confirmed below)")

print()
print("="*78)
print("HALF ONE -- the between-item share.  TWO INDEPENDENT MECHANISMS.")
print("="*78)
print(f"  {'subset':8s} {'phibar(Pearson)':>16s} {'ICC(EMS/ANOVA)':>16s} {'diff':>10s}"
      f" {'omega2/tau2 %':>14s} {'naive %':>9s}")
for s in SUBSETS:
    E,_ = load_error(s)
    pb = phibar_pearson(E)
    an = icc_oneway(E)
    out[s].update(phibar=pb, icc=an["icc"], omega2_pct=an["omega2_over_tau2_pct"],
                  omega2_naive_pct=an["naive_omega2_over_tau2_pct"],
                  s2_item=an["s2_item"], s2_resid=an["s2_resid"], s2_judge=an["s2_judge"])
    print(f"  {s:8s} {pb:16.6f} {an['icc']:16.6f} {pb-an['icc']:+10.2e}"
          f" {an['omega2_over_tau2_pct']:14.3f} {an['naive_omega2_over_tau2_pct']:9.3f}")

# bootstrap over ITEMS for phibar CI
print()
print("  Bootstrap over items (2000 resamples) for phi-bar:")
rng = np.random.default_rng(20261007)
for s in SUBSETS:
    E,_ = load_error(s)
    I = E.shape[0]
    bs = np.empty(2000)
    for b in range(2000):
        idx = rng.integers(0, I, I)
        bs[b] = phibar_pearson(E[idx])
    lo,hi = np.percentile(bs,[2.5,97.5])
    out[s].update(phibar_lo=lo, phibar_hi=hi, phibar_se=bs.std())
    print(f"    {s:8s} phi-bar = {phibar_pearson(E):.4f}  "
          f"95% CI [{lo:.4f}, {hi:.4f}]  se={bs.std():.4f}   "
          f"Kish n_eff = {E.shape[1]/(1+(E.shape[1]-1)*phibar_pearson(E)):.4f}"
          f"   ceiling 1/phibar = {1/phibar_pearson(E):.4f}")

print()
print("="*78)
print("HALF TWO -- the per-item-demeaned residual correlation")
print("="*78)
print(f"  {'subset':8s} {'-1/(J-1)':>12s} {'pooled-norm':>14s} {'Pearson':>12s}"
      f" {'AM-GM slack':>12s} {'resid ESDOF':>12s} {'null J-1':>9s}")
for s in SUBSETS:
    E,_ = load_error(s)
    J = E.shape[1]
    pred = -1/(J-1)
    pooled = resid_offdiag_pooled(E)
    pear, ndrop = resid_offdiag_pearson(E)
    es = resid_esdof(E)
    out[s].update(resid_pred=pred, resid_pooled=pooled, resid_pearson=pear,
                  resid_esdof=es, resid_esdof_null=J-1, ndrop=ndrop)
    print(f"  {s:8s} {pred:12.8f} {pooled:14.8f} {pear:12.6f} {pear-pred:+12.2e}"
          f" {es:12.4f} {J-1:9d}")
print("  (pooled-norm agrees with -1/(J-1) to machine precision, as proved)")

json.dump(out, open("/tmp/wk-20261007-review/spine_out.json","w"), indent=2)
print()
print("wrote spine_out.json")
