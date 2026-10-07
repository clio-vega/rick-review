#!/usr/bin/env python3
"""EXACT permutation nulls for half two; warm-chain curveball (single chain, thinned).

Lyra's null is "judges are exchangeable given the item".  If judge labels carry
no information beyond the item, every within-row permutation of the error matrix
is equally likely -> an EXACT finite-sample null, no model, no fitted difficulty.
That null CONTAINS both conditional independence AND exchangeable conditional
dependence of any strength, so the test is blind to exactly the distinction that
is unidentifiable and sensitive to exactly the one that is not.

  N1  fixed ROW sums            -> judge main effect + judge clustering
  N2  fixed ROW and COLUMN sums -> judge clustering BEYOND the main effect
"""
import csv, json
from pathlib import Path
import numpy as np

DATA = Path("/tmp/judge-panel-article/data/raw-judge-matrix")
SUBSETS = ["alphanli","snli","mnli_m"]
NPERM, BURN, THIN = 1000, 20000, 2000

def load_error(s):
    rows = list(csv.reader(open(DATA/s/"error_matrix.csv")))
    jc = [k for k,h in enumerate(rows[0]) if h.startswith("j")]
    return np.array([[int(r[k]) for k in jc] for r in rows[1:]], dtype=float)

def resid_stats(E):
    R = E - E.mean(axis=1, keepdims=True)
    keep = R.var(axis=0) > 0
    P = np.corrcoef(R[:,keep], rowvar=False)
    off = P[~np.eye(P.shape[0],dtype=bool)].mean()
    lam = np.clip(np.linalg.eigvalsh(P), 0, None)
    return float(off), float(lam.sum()**2/(lam**2).sum())

def perm_rows(E, rng):
    idx = np.argsort(rng.random(E.shape), axis=1)
    return np.take_along_axis(E, idx, axis=1)

class Curveball:
    def __init__(self, E, rng):
        self.I, self.J = E.shape
        self.sets = [set(np.flatnonzero(E[i] > .5).tolist()) for i in range(self.I)]
        self.rng = rng
    def trades(self, n):
        rng = self.rng; I = self.I; sets = self.sets
        aa = rng.integers(0, I, n); bb = rng.integers(0, I, n)
        for t in range(n):
            a = aa[t]; b = bb[t]
            if a == b: continue
            A = sets[a]; B = sets[b]
            shared = A & B
            ex_a = A - shared; ex_b = B - shared
            na = len(ex_a)
            if na == 0 or len(ex_b) == 0: continue
            pool = list(ex_a) + list(ex_b)
            rng.shuffle(pool)
            sets[a] = shared.union(pool[:na]); sets[b] = shared.union(pool[na:])
    def matrix(self):
        out = np.zeros((self.I, self.J))
        for i in range(self.I): out[i, list(self.sets[i])] = 1.0
        return out

rng = np.random.default_rng(20261007)
report = {}
for s in SUBSETS:
    E = load_error(s); I, J = E.shape
    off_obs, es_obs = resid_stats(E)
    print("="*78, flush=True)
    print(f"{s}  I={I} J={J}   OBSERVED  off-diag residual r={off_obs:+.6f}   "
          f"residual ESDOF={es_obs:.4f}   (theory null = J-1 = {J-1})", flush=True)
    rec = dict(I=I, J=J, off_obs=off_obs, esdof_obs=es_obs, esdof_null_theory=J-1)

    def summarise(tag, offs, ess):
        d = dict(off_mean=float(offs.mean()), off_sd=float(offs.std()),
                 es_mean=float(ess.mean()), es_sd=float(ess.std()),
                 p_es=float((1+(ess<=es_obs).sum())/(NPERM+1)),
                 es_z=float((es_obs-ess.mean())/ess.std()),
                 off_z=float((off_obs-offs.mean())/offs.std()),
                 p_off=float(min(1.0, 2*min((1+(offs<=off_obs).sum())/(NPERM+1),
                                            (1+(offs>=off_obs).sum())/(NPERM+1)))))
        print(f"  {tag}: off-diag null {d['off_mean']:+.6f} sd {d['off_sd']:.2e} "
              f"z={d['off_z']:+8.2f} p={d['p_off']:.4f}  |  ESDOF null {d['es_mean']:.4f} "
              f"sd {d['es_sd']:.4f} z={d['es_z']:+8.2f} p={d['p_es']:.4f}", flush=True)
        return d

    offs = np.empty(NPERM); ess = np.empty(NPERM)
    for b in range(NPERM):
        offs[b], ess[b] = resid_stats(perm_rows(E, rng))
    rec["N1"] = summarise("N1 rows     ", offs, ess)

    cb = Curveball(E, rng); cb.trades(BURN)
    offs = np.empty(NPERM); ess = np.empty(NPERM)
    for b in range(NPERM):
        cb.trades(THIN)
        offs[b], ess[b] = resid_stats(cb.matrix())
    rec["N2"] = summarise("N2 rows+cols", offs, ess)
    report[s] = rec

json.dump(report, open("perm_out.json","w"), indent=2)
print("wrote perm_out.json", flush=True)
