#!/usr/bin/env python3
"""What the residual structure IS, and the exact floor on the statistic."""
import csv, json
from pathlib import Path
import numpy as np

DATA = Path("/tmp/judge-panel-article/data/raw-judge-matrix")
STEMS = ["doubao18","doubao20pro","dsv32","dsv4flash","dsv4pro","gem25pro","gem31pro",
         "gem36flash","gem37flash","glm5","glm51","glm52","glm53","gpt41","gpt54",
         "gpt56sol","gpt56terra","grok45","grok46","haiku45","kimik25","kimik26",
         "kimik27code","kimik3","minimaxm3","o4mini","opus5","qwen35plus","qwen37plus",
         "qwen38max","qwen3max","sonnet46"]
VEND = {"doubao18":"bytedance","doubao20pro":"bytedance","dsv32":"deepseek",
  "dsv4flash":"deepseek","dsv4pro":"deepseek","gem25pro":"google","gem31pro":"google",
  "gem36flash":"google","gem37flash":"google","glm5":"zhipu","glm51":"zhipu",
  "glm52":"zhipu","glm53":"zhipu","gpt41":"openai","gpt54":"openai","gpt56sol":"openai",
  "gpt56terra":"openai","o4mini":"openai","grok45":"xai","grok46":"xai",
  "haiku45":"anthropic","opus5":"anthropic","sonnet46":"anthropic",
  "kimik25":"moonshot","kimik26":"moonshot","kimik27code":"moonshot","kimik3":"moonshot",
  "minimaxm3":"minimax","qwen35plus":"alibaba","qwen37plus":"alibaba",
  "qwen38max":"alibaba","qwen3max":"alibaba"}
vend = np.array([VEND[s] for s in STEMS])

def load_error(s):
    rows = list(csv.reader(open(DATA/s/"error_matrix.csv")))
    jc = [k for k,h in enumerate(rows[0]) if h.startswith("j")]
    return np.array([[int(r[k]) for k in jc] for r in rows[1:]], dtype=float)

print("="*78)
print("A. THE FLOOR IS EXACT:  mean off-diag Pearson of demeaned residuals >= -1/(J-1)")
print("="*78)
print("  Proof: with d_j = sqrt(G_jj), u_j = 1/d_j,")
print("    sum_{j!=j'} G_jj'/(d_j d_j') = u'Gu - J >= -J  since G = R'R is PSD.")
print("    Divide by J(J-1):  mean off-diag >= -1/(J-1).  Equality iff u in null(G),")
print("    and since G1 = 0 (rows of R sum to zero) that means all d_j equal.")
rng = np.random.default_rng(1)
worst = 0.0
for trial in range(4000):
    I = int(rng.integers(5, 60)); J = int(rng.integers(3, 20))
    X = rng.standard_normal((I,J))*rng.uniform(.1,4,size=J) + rng.standard_normal((I,1))*3
    if rng.random() < .3: X = (X > rng.standard_normal()).astype(float)   # binary too
    R = X - X.mean(axis=1, keepdims=True)
    if (R.var(axis=0) <= 0).any(): continue
    P = np.corrcoef(R, rowvar=False)
    m = P[~np.eye(J,dtype=bool)].mean()
    worst = min(worst, m + 1/(J-1))
print(f"  4000 random trials (Gaussian + binary, heteroscedastic): "
      f"min of (stat + 1/(J-1)) = {worst:+.3e}   -> floor never violated")

print()
print("="*78)
print("B. WHAT THE ESDOF DEFICIT IS MADE OF  (residual correlation spectrum)")
print("="*78)
res = {}
for s in ["alphanli","snli","mnli_m"]:
    E = load_error(s); J = E.shape[1]
    R = E - E.mean(axis=1, keepdims=True)
    P = np.corrcoef(R, rowvar=False)
    lam, V = np.linalg.eigh(P)
    order = np.argsort(lam)[::-1]; lam = lam[order]; V = V[:,order]
    print(f"\n  {s}: top 6 eigenvalues {np.round(lam[:6],3)}   "
          f"null(flat) = {J/(J-1):.4f} x {J-1}")
    for k in range(3):
        v = V[:,k]
        top = np.argsort(-np.abs(v))[:6]
        print(f"    PC{k+1} (lam={lam[k]:.3f}): " +
              ", ".join(f"{STEMS[t]}({VEND[STEMS[t]]}){v[t]:+.2f}" for t in top))
    # within- vs between-vendor mean residual correlation
    off = ~np.eye(J, dtype=bool)
    same = (vend[:,None] == vend[None,:]) & off
    diff = (vend[:,None] != vend[None,:]) & off
    w, b = P[same].mean(), P[diff].mean()
    # permutation test on the VENDOR LABELS (judges fixed, labels shuffled)
    NP = 20000
    stat = w - b
    null = np.empty(NP)
    for t in range(NP):
        pv = rng.permutation(vend)
        sm = (pv[:,None]==pv[None,:]) & off
        dm = (pv[:,None]!=pv[None,:]) & off
        null[t] = P[sm].mean() - P[dm].mean()
    p = (1 + (null >= stat).sum())/(NP+1)
    print(f"    within-vendor mean r = {w:+.4f}   between-vendor = {b:+.4f}   "
          f"gap = {stat:+.4f}   label-permutation p = {p:.5f}")
    res[s] = dict(lam=lam.tolist(), within=float(w), between=float(b),
                  gap=float(stat), p_vendor=float(p))
json.dump(res, open("structure_out.json","w"), indent=2)
