#!/usr/bin/env python3
"""Cross-check against the UPSTREAM paper's own reported numbers (2609.21277),
   which is an independent source for the same matrices."""
import csv
from pathlib import Path
import numpy as np
DATA = Path("/tmp/judge-panel-article/data/raw-judge-matrix")
def load_error(s):
    rows = list(csv.reader(open(DATA/s/"error_matrix.csv")))
    jc = [k for k,h in enumerate(rows[0]) if h.startswith("j")]
    return np.array([[int(r[k]) for k in jc] for r in rows[1:]], dtype=float)

# upstream abstract: "a binary-error diagnostic credits the same panels with only
# 1.971--2.227 effective votes";  "spectral matching gives nu_H = 4.242, 6.459, 6.499"
print(f"  {'subset':8s} {'phibar':>8s} {'Kish n_eff':>11s} {'PR(err corr)':>13s}"
      f" {'1/phibar':>9s} {'1/phibar^2':>11s}")
kish=[]
for s in ["alphanli","snli","mnli_m"]:
    E = load_error(s); J = E.shape[1]
    C = np.corrcoef(E, rowvar=False)
    pb = C[~np.eye(J,dtype=bool)].mean()
    lam = np.clip(np.linalg.eigvalsh(C),0,None)
    pr = lam.sum()**2/(lam**2).sum()
    ne = J/(1+(J-1)*pb)
    kish.append(ne)
    print(f"  {s:8s} {pb:8.4f} {ne:11.4f} {pr:13.4f} {1/pb:9.4f} {1/pb**2:11.4f}")
print(f"\n  My Kish range            : {min(kish):.3f}--{max(kish):.3f}")
print(f"  Upstream abstract states : 1.971--2.227   (binary-error diagnostic)")
print(f"  Upstream nu_H states     : 4.242, 6.459, 6.499  (spectral matching)")
print(f"  -> compare PR column above to nu_H.  PR is the participation ratio of the")
print(f"     ERROR correlation matrix, which is the statistic Lyra prints as ESDOF.")
