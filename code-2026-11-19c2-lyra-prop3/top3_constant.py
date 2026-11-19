"""top3_constant.py -- Regime 2 (shock only in strata 7-9): power of the CONSTANT bettor that puts
cap/3 on strata 7,8,9 (chosen before any data, hence valid), d1 vs d2 slack, R=200."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, freshpair_review as F
for g in (0.20, 0.35):
    for des in ('d1cyc', 'd2cyc'):
        rej = 0
        for r in range(200):
            rng = np.random.default_rng(1000 + r)
            _, st, pi, pj, Wi, Wj = F.gen('top3', rng, g)
            X, b, live, delta = F.stream(F.increments(st, pi, pj, Wi, Wj), des)
            lam = np.zeros((F.M, F.Q)); lam[:, 7:] = (1 / b) / 3
            rej += np.any(F.wealth(X, lam)[1] >= F.THRESH)
        print(f"top3 gamma={g:.2f} {des}: power(top-3 constant) = {rej/200:.3f}")
