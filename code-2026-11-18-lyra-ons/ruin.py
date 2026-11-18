"""Is ONS's left tail estimation variance, or ruin (a factor hitting exactly 0 => log clamp -690.8)?
Count seeds with terminal wealth 0, and rerun with cap shrunk to 0.9/b (factor >= 0.1 always)."""
import sys, numpy as np
sys.path.insert(0, '/tmp/lyra-wip/code/evalue')
import run_equicorr_puzzle as P, run_online_weights as rw
from dgp import alt_dgp, drift_null_dgp
R = 200
for name, dgp in [("R1 g=0.25", lambda N, r: alt_dgp(N, .25, r)), ("R1 g=0.02", lambda N, r: alt_dgp(N, .02, r)),
                  ("R2 g=0.35", lambda N, r: P.alt_dgp_top_strata(N, .35, r)), ("drift null", drift_null_dgp)]:
    lw, lw9, minf, pw, pw9, lwf9 = [], [], [], [], [], []
    for r in range(R):
        rng = np.random.default_rng(1000 + r); d = dgp(P.N, rng)
        X, b = rw.build_increment_stream(d, rng)
        lon, _ = rw.ons_weights(X, b); M = rw.wealth_path(X, lon)
        lw.append(np.log(max(M[-1], 1e-300))); pw.append((M >= 20).any())
        minf.append((1 + np.einsum('ms,ms->m', lon, X)).min())
        # shrunk cap: pass b/0.9 so cap = 0.9/b  (X bound unchanged)
        lon9, _ = rw.ons_weights(X, b / 0.9); M9 = rw.wealth_path(X, lon9)
        lw9.append(np.log(max(M9[-1], 1e-300))); pw9.append((M9 >= 20).any())
        lwf9.append(np.log(rw.wealth_path(X, rw.lam_fixed(b / 0.9))[-1]))
    lw, lw9 = np.array(lw), np.array(lw9)
    ruin = lw < -600
    print(f"{name:11s} ONS: ruined seeds {ruin.sum()}/{R}, mean {lw.mean():+.2f}, mean excl. ruin {lw[~ruin].mean():+.2f}, "
          f"min factor <1e-6 in {(np.array(minf)<1e-6).sum()} | cap 0.9/b: ONS mean {lw9.mean():+.2f} med {np.median(lw9):+.2f} "
          f"pow {np.mean(pw9):.3f} (ruined {(lw9<-600).sum()}), FIXED@0.9 mean {np.mean(lwf9):+.2f}")
