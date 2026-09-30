import sys, time
sys.path.insert(0, '/home/clio/projects/reviews/code-2026-09-30')
import sympy as sp
from tc_aha import *
for m, k in [(4,1),(4,2),(5,1),(4,3)]:
    X = Xs(m); t0 = time.time()
    d = sp.cancel(sp.together(sp.expand(Gamma(X,k)) - T_closed(X,k)))
    print(f"  m={m} k={k}: Gamma_k == T_k : {sp.simplify(d)==0}   ({time.time()-t0:.0f}s)")
    sys.stdout.flush()
