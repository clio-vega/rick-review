"""Meta-conjecture: e_a * e_b has exactly min(a,b)+1 nonzero e_lambda terms,
supported on two-row lambda = (a+b-k, k), k=0..min(a,b)."""
from hikita_star_clio import *
import sys, time
pairs = [tuple(int(x) for x in s.split(',')) for s in sys.argv[1:]]
for (a,b) in pairs:
    t0=time.time(); co,m = star_e(a,b); el=time.time()-t0
    pred = sorted([tuple(sorted((a+b-k,k),reverse=True)) if k>0 else (a+b,)
                   for k in range(min(a,b)+1)], reverse=True)
    got = sorted(co.keys(), reverse=True)
    print("e_%d * e_%d (m=%d, %.1fs): #nonzero=%d predicted=%d  support %s"
          % (a,b,m,el,len(co),min(a,b)+1, "MATCH" if got==pred else "MISMATCH"))
    print("   got:", got)
    if got!=pred: print("   predicted:", pred)
    for lam in got: print("     e_%s : %s" % (lam, co[lam]))
    sys.stdout.flush()
