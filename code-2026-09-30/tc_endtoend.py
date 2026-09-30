import sys, time
sys.path.insert(0, '/home/clio/projects/reviews/code-2026-09-30')
import sympy as sp
from tc_aha import *

print("=" * 78)
print("(TC) end-to-end:  Gamma_k == T_k  in Lambda_m (x) Q(s,t)(z,w)")
print("  Gamma_k from my own T_i/pi/Y_i implementation of Day 207b s.0;")
print("  T_k from the Day 209 s.0 closed form. Fully symbolic in X,s,t,z,w.")
print("=" * 78)
for m in [0, 1, 2, 3]:
    X = Xs(m)
    for k in [0, 1, 2, 3]:
        t0 = time.time()
        G = Gamma(X, k)
        Tc = T_closed(X, k) if m > 0 or k == 0 else T_closed(X, k)
        d = sp.cancel(sp.together(sp.expand(G) - Tc))
        ok = sp.simplify(d) == 0
        print(f"  m={m} k={k}: Gamma_k == T_k : {ok}    ({time.time()-t0:.1f}s)")
        sys.stdout.flush()
