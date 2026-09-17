"""Clio 2026-09-17: Conjecture 7 (sharp DS) leading coefficient q^{-n(lambda)},
and exactness of the support, on lambda with |lambda| <= 6.  Independent of Rick."""
import sys
from hikita_star_clio import *
import triple_quiet as TQ
def nstat(lam): return sum(i*lam[i] for i in range(len(lam)))
allok = True
for lam in [(2,1),(2,2),(3,1),(3,2),(3,3),(4,2),(2,1,1),(2,2,1),(2,2,2),(3,2,1),
            (3,1,1),(4,1,1),(1,1,1),(1,1,1,1),(2,1,1,1),(1,1,1,1,1),(2,2,1,1)]:
    co, m = TQ.star_many(list(lam))
    got = co.get(lam, ZERO); want = (ONE/q)**nstat(lam)
    ok = (got - want) == ZERO
    nz = all(v != ZERO for v in co.values())
    allok = allok and ok and nz
    print("  lam=%-13s n(lam)=%-2d  leading %-12s  |supp|=%-2d all nonzero: %s"
          % (str(lam), nstat(lam), "q^-%d OK" % nstat(lam) if ok else "**MISMATCH**",
             len(co), nz))
    sys.stdout.flush()
print("Conj 7 diagonal + exactness:", "CONFIRMED on all 17" if allok else "FAILED")
