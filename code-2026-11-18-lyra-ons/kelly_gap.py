"""Q1 heuristic check. Population Kelly optimum lam* from pooled blocks (cap 0.9/b, no ruin);
D(lam_F) = l(lam*) - l(lam_F) per block.  Fixed's cost = M*D; learner's cost = M*l(lam*) - E[W_on].
Puzzle inequality: Fixed beats learner iff M*D < learner cost (predicted <= (k/2) ln M, k = active dims)."""
import sys, numpy as np
sys.path.insert(0, '/tmp/lyra-wip/code/evalue')
import run_equicorr_puzzle as P, run_online_weights as rw
from dgp import alt_dgp
M = 200
for g in [0.10, 0.15, 0.20, 0.25, 0.30, 0.35]:
    Xs, bs = [], []
    for r in range(300):                      # pool seeds 50000+ (disjoint from evaluation seeds)
        rng = np.random.default_rng(50000 + r); X, b = rw.build_increment_stream(alt_dgp(P.N, g, rng), rng)
        Xs.append(X); bs.append(b)
    Xp = np.vstack(Xs); b9 = np.mean(bs) / 0.9
    lstar = rw.oracle_weights(Xp, b9, iters=400)
    l = lambda lam: np.mean(np.log(1 + Xp @ lam))
    D = l(lstar) - l(rw.lam_fixed(b9))
    WF, WO = [], []
    for r in range(200):
        rng = np.random.default_rng(1000 + r); X, b = rw.build_increment_stream(alt_dgp(P.N, g, rng), rng)
        WF.append(np.log(rw.wealth_path(X, rw.lam_fixed(b / .9))[-1])); WO.append(np.log(rw.wealth_path(X, rw.ons_weights(X, b / .9)[0])[-1]))
    k = int((lstar > 1e-6).sum()); cap_bind = lstar.sum() / (1 / b9)
    print(f"g={g:.2f} M*l*={M*l(lstar):+6.2f} | Fixed cost M*D={M*D:5.2f} (obs {M*l(lstar)-np.mean(WF):5.2f}) | "
          f"ONS cost obs {M*l(lstar)-np.mean(WO):5.2f} | active k={k}, sum/cap={cap_bind:.2f}, (k/2)lnM={k/2*np.log(M):.1f} | "
          f"lam*/cap range [{lstar.min()*b9:.3f},{lstar.max()*b9:.3f}]", flush=True)
