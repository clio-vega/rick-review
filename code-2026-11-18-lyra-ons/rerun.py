"""Rerun Lyra's equicorr puzzle cells (commit 44e1f1d) at reduced R, report next to her numbers.
Also: hindsight-oracle vs (Q/2) ln M parametric price; 1-D scale-mixture alternative."""
import sys, time, numpy as np
sys.path.insert(0, '/tmp/lyra-wip/code/evalue')
import run_equicorr_puzzle as P
import run_online_weights as rw
from dgp import alt_dgp, drift_null_dgp
R = int(sys.argv[1]) if len(sys.argv) > 1 else 50
cells = [("R1 g=0.25", lambda N, rng: alt_dgp(N, 0.25, rng)),
         ("R1 g=0.15", lambda N, rng: alt_dgp(N, 0.15, rng)),
         ("R1 g=0.02", lambda N, rng: alt_dgp(N, 0.02, rng)),
         ("R2 g=0.35", lambda N, rng: P.alt_dgp_top_strata(N, 0.35, rng)),
         ("drift null", drift_null_dgp),
         ("latent null", P.latent_factor_null_dgp)]
GRID = np.linspace(0, 1, 11)          # scale grid c_k * cap, uniform direction
for name, dgp in cells:
    t0 = time.time(); out = []
    for r in range(R):
        rng = np.random.default_rng(1000 + r)
        data = dgp(P.N, rng)
        X, b = rw.build_increment_stream(data, rng)
        cap = 1 / b
        lf = rw.lam_fixed(b); lon, _ = rw.ons_weights(X, b); lo = rw.oracle_weights(X, b)
        Mf, Mo, Mr = rw.wealth_path(X, lf), rw.wealth_path(X, lon), rw.wealth_path(X, lo)
        xbar = X.mean(axis=1)                       # <uniform/Q, X>, times cap*c below
        paths = np.cumprod(1 + np.outer(xbar, GRID * cap), axis=0)   # (M, K)
        Mmix = paths.mean(axis=1)                  # average of e-processes: valid
        f = lambda M: (np.log(max(M[-1], 1e-300)), bool((M >= 20).any()))
        out.append([*f(Mf), *f(Mo), *f(Mr), *f(Mmix), b])
    a = np.array(out, float)
    M = X.shape[0]
    print(f"{name:12s} R={R} M={M} b~{a[:,8].mean():.3f}  "
          f"W/pow  FIX {a[:,0].mean():+.2f}/{a[:,1].mean():.3f} (med {np.median(a[:,0]):+.2f})  "
          f"ONS {a[:,2].mean():+.2f}/{a[:,3].mean():.3f} (med {np.median(a[:,2]):+.2f})  "
          f"HIND {a[:,4].mean():+.2f}/{a[:,5].mean():.3f}  "
          f"MIX1D {a[:,6].mean():+.2f}/{a[:,7].mean():.3f}  "
          f"HIND-ONS {np.mean(a[:,4]-a[:,2]):.1f} vs (Q/2)lnM={5*np.log(M):.1f}  [{time.time()-t0:.0f}s]", flush=True)
