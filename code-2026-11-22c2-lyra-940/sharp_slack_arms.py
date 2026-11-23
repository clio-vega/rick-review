"""Clio 2026-11-23: does the sharp cell slack buy power?  Same seeds/data as loo_ownseed.py.
 A  cyclic + 1/2 RiRj                (Lyra arm A)
 B  LOO    + n/(4(n-1)) RiRj         (Lyra arm B)
 As cyclic + floor(n/2)/n RiRj       (sharp cyclic, proved 11-21 c2)
 Bs LOO    + floor(n/2)ceil(n/2)/(n(n-1)) RiRj   (sharp LOO, this review sec.1; = Cov<=sigma sigma)
RiRj = 4*range_i*range_j in Lyra's convention (range = (max-min)/2).  Also prints cell-size histogram.
Usage: python3 sharp_slack_arms.py <gamma> <R> <seed0>"""
import sys, json, numpy as np
sys.path.insert(0, '/tmp/lyra940/wip/code/evalue')
from dgp import alt_dgp, null_dgp
from eprocess import assign_strata, make_within_block_pairing
from run_online_weights import lam_fixed, wealth_path
Q, BLOCK, N, TH = 10, 20, 4000, 20.0
fac = {'A': lambda n: 0.5, 'B': lambda n: n / (4 * (n - 1)),
       'As': lambda n: (n // 2) / n, 'Bs': lambda n: (n // 2) * ((n + 1) // 2) / (n * (n - 1))}
def arms(d, hist):
    Wi, Wj, pi, pj = d['W_i'], d['W_j'], d['p_i'], d['p_j']
    st = assign_strata(d['theta'], Q=Q); blk = np.arange(N) // BLOCK; M = N // BLOCK
    t = make_within_block_pairing(st, blk, Q=Q); hp = t != np.arange(N)
    U = (Wi * Wj).astype(float); Vc = (Wi * Wj[t]).astype(float); Vl = np.zeros(N)
    X = {k: np.zeros((M, Q)) for k in fac}; dmax = {k: 0.0 for k in fac}
    for m in range(M):
        for k in range(Q):
            c = np.where((blk == m) & (st == k) & hp)[0]; n = len(c)
            if n < 2: continue
            hist[min(n, 9)] += 1
            wj = Wj[c].astype(float); Vl[c] = Wi[c] * (wj.sum() - wj) / (n - 1)
            RR = (pi[c].max() - pi[c].min()) * (pj[c].max() - pj[c].min())
            for a, f in fac.items():
                dl = f(n) * RR; dmax[a] = max(dmax[a], dl)
                V = Vc[c] if a in ('A', 'As') else Vl[c]
                X[a][m, k] = (U[c] - V - dl).mean()
    return {a: wealth_path(X[a], lam_fixed(1.0 + dmax[a])).max() >= TH for a in fac}
g, R, s0 = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
hist = np.zeros(10, int); rej = {a: np.zeros(R, bool) for a in fac}
for r in range(R):
    rng = np.random.default_rng(s0 + r)
    d = null_dgp(N, rng) if g == 0 else alt_dgp(N, g, rng)
    for a, v in arms(d, hist).items(): rej[a][r] = v
f = {a: v.astype(float) for a, v in rej.items()}
out = dict(gamma=g, R=R, seed0=s0, power={a: f[a].mean() for a in fac},
           cell_size_hist={int(n): int(h) for n, h in enumerate(hist) if h})
for x, y in (('As', 'A'), ('Bs', 'B'), ('Bs', 'As')):
    dd = f[x] - f[y]; out[f'{x}-{y}'] = (round(dd.mean(), 4), round(float(dd.std(ddof=1) / np.sqrt(R)), 4))
print(json.dumps(out))
