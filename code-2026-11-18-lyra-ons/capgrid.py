"""R1 grid: ruin counts at cap 1/b (Lyra's), and FIXED vs ONS at cap 0.9/b (no ruin possible)."""
import sys, numpy as np
sys.path.insert(0, '/tmp/lyra-wip/code/evalue')
import run_equicorr_puzzle as P, run_online_weights as rw
from dgp import alt_dgp
R = 200
print("gamma | ruin@1/b | @0.9/b: FIX W/med/pow | ONS W/med/pow | ONS>FIX seeds")
for g in [0.10, 0.15, 0.20, 0.25, 0.30, 0.35]:
    ru = 0; F = []; O = []
    for r in range(R):
        rng = np.random.default_rng(1000 + r); d = alt_dgp(P.N, g, rng)
        X, b = rw.build_increment_stream(d, rng)
        l1, _ = rw.ons_weights(X, b); ru += rw.wealth_path(X, l1)[-1] == 0
        b9 = b / 0.9
        Mf = rw.wealth_path(X, rw.lam_fixed(b9)); l9, _ = rw.ons_weights(X, b9); Mo = rw.wealth_path(X, l9)
        F.append((np.log(Mf[-1]), (Mf >= 20).any())); O.append((np.log(Mo[-1]), (Mo >= 20).any()))
    F, O = np.array(F), np.array(O)
    print(f"{g:.2f} | {ru:3d}/{R} | {F[:,0].mean():+6.2f} {np.median(F[:,0]):+6.2f} {F[:,1].mean():.3f} | "
          f"{O[:,0].mean():+6.2f} {np.median(O[:,0]):+6.2f} {O[:,1].mean():.3f} | {np.mean(O[:,0]>F[:,0]):.3f}")
