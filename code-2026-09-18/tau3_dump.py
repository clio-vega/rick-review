"""
Clio 2026-09-18. Compute tau_r^(3) = coeff of e_{(r+3)} in p_3(Y).e_r on my own
instrument and dump it as a string, one file per r, so the structural analysis
(Conjecture 10 fit, divisibility, factorisation) can be done separately without
recomputing.  Also dumps the full e-support.
"""
import sys, json, time
from hikita_star_clio import *

def p3Y(A, m):
    tot = {}
    for i in range(1, m+1):
        tot = add(tot, Y(i, Y(i, Y(i, A, m), m), m))
    return tot

for r in [int(x) for x in sys.argv[1:]]:
    m = r + 3
    t0 = time.time()
    co = expand_in_e(p3Y(e_poly(r, m), m), r+3, m)
    co = {k: v for k, v in co.items() if v}
    el = time.time() - t0
    out = {"r": r, "m": m, "seconds": round(el, 1),
           "coeffs": {repr(k): str(v) for k, v in sorted(co.items(), reverse=True)}}
    json.dump(out, open("tau3_r%d.json" % r, "w"), indent=1)
    print("r=%d m=%d (%.1fs) support=%s" % (r, m, el, sorted(co, reverse=True)))
    sys.stdout.flush()
