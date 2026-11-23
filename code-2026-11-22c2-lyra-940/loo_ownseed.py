"""Clio 2026-11-23: LOO-vs-cyclic edge at gamma=0.06 on MY seeds (170000+r), disjoint from
Lyra's 90000+r and my 11-20 block. Uses Lyra's own three-arm builder (fc0241f) unchanged.
Usage: python3 loo_ownseed.py <gamma> <R> <seed0>"""
import sys, json, numpy as np
sys.path.insert(0, '/tmp/lyra940/wip/code/evalue')
import loo_freshseed_run90000 as L
from dgp import alt_dgp, null_dgp
from run_online_weights import lam_fixed, wealth_path
g, R, s0 = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
rej = np.zeros((R, 3), bool)
for r in range(R):
    rng = np.random.default_rng(s0 + r)
    data = null_dgp(L.N, rng) if g == 0 else alt_dgp(L.N, g, rng)
    for a, (X, b) in enumerate(L.build_increment_three_arms(data)):
        rej[r, a] = wealth_path(X, lam_fixed(b)).max() >= L.THRESH
f = rej.astype(float)
out = dict(gamma=g, R=R, seed0=s0, A=f[:, 0].mean(), B=f[:, 1].mean(), C=f[:, 2].mean())
for nm, (i, j) in dict(BA=(1, 0), CA=(2, 0), BC=(1, 2)).items():
    d = f[:, i] - f[:, j]
    out[nm] = d.mean(); out['se_' + nm] = float(d.std(ddof=1) / np.sqrt(R))
print(json.dumps(out))
