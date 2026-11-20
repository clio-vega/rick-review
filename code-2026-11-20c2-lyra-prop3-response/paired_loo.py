"""Q(a): is the d2-LOO power edge over d2-cyclic at gamma=0.06 real?  PAIRED on the same seeds,
using Lyra's own run_online_weights (a5230bf).  Seeds 1000..1000+R-1 (her seeds, so the first
500 reproduce her 0.526/0.576), plus a disjoint block 50000.. as a fresh replicate."""
import sys, json
import numpy as np
sys.path.insert(0, sys.argv[1])
import verify_prop3_freshpair as v
from dgp import alt_dgp
from run_online_weights import build_increment_stream, lam_fixed, wealth_path
R, seed0 = int(sys.argv[2]), int(sys.argv[3])
both = only_c = only_l = neither = 0
for r in range(R):
    out = []
    for rule in ['cyclic', 'loo']:
        rng = np.random.default_rng(seed0 + r)
        data = alt_dgp(v.N, 0.06, rng)
        X, b = build_increment_stream(data, rng, pairing='within_block',
                                      slack='second_order', pairing_rule=rule)
        out.append(bool(np.any(wealth_path(X, lam_fixed(b)) >= v.THRESH)))
    c, l = out
    both += c and l; only_c += c and not l; only_l += l and not c; neither += not (c or l)
pc, pl = (both + only_c) / R, (both + only_l) / R
d = pl - pc
# paired SE of the difference from discordant counts
se = np.sqrt((only_c + only_l) / R**2 - d**2 / R)
# exact McNemar (two-sided binomial on discordant pairs)
from math import comb
nd = only_c + only_l; k = min(only_c, only_l)
p_mcn = min(1.0, 2 * sum(comb(nd, i) for i in range(k + 1)) / 2**nd) if nd else 1.0
print(json.dumps(dict(R=R, seed0=seed0, cyclic=pc, loo=pl, diff=d, paired_se=float(se),
                      both=both, only_cyclic=only_c, only_loo=only_l, neither=neither,
                      mcnemar_p=p_mcn)))
