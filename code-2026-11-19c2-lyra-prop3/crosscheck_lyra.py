"""
crosscheck_lyra.py -- run Lyra's OWN build_increment_stream (branch fix/prop3-fresh-pair-eprocess,
commit dbc1b9d) on her own null_dgp data, and compare its X with my independent d1cyc stream.
Her directory is inserted into sys.path EXPLICITLY (run with python3 -I, so nothing else is
picked up implicitly). Usage: python3 -I crosscheck_lyra.py /tmp/lyra-wip/code/evalue
"""
import sys, os
lyra_dir = os.path.abspath(sys.argv[1])
here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import freshpair_review as mine          # noqa: E402
sys.path.insert(0, lyra_dir)
import numpy as np                      # noqa: E402
import run_online_weights as rw         # noqa: E402
import dgp                              # noqa: E402
from eprocess import assign_strata      # noqa: E402

rw.Q, rw.BLOCK = 10, 20
maxdiff, bdiff = 0.0, 0.0
for r in range(50):
    rng = np.random.default_rng(1000 + r)
    for fn in (dgp.null_dgp, dgp.drift_null_dgp):
        data = fn(4000, rng)
        X_l, b_l = rw.build_increment_stream(data, rng, pairing='within_block')
        stratum = assign_strata(data['theta'], Q=10)
        inc = mine.increments(stratum, data['p_i'], data['p_j'], data['W_i'], data['W_j'])
        X_m, b_m, _, _ = mine.stream(inc, 'd1cyc')
        maxdiff = max(maxdiff, float(np.abs(X_l - X_m).max()))
        bdiff = max(bdiff, abs(b_l - b_m))
print(f"100 streams (50 static + 50 drift null): max |X_lyra - X_clio| = {maxdiff:.3e}, "
      f"max |b_lyra - b_clio| = {bdiff:.3e}")
# negative control: a planted error in my stream must be seen
X_bad = X_m.copy(); X_bad[3, 4] += 1e-6
print(f"planted 1e-6 perturbation seen: {np.abs(X_l - X_bad).max():.3e}")
