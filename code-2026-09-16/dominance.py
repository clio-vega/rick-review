"""CLIO'S CONJECTURE (Day 193 review, 2026-09-16).

  supp_e( e_{l_1} * e_{l_2} * ... * e_{l_k} )  =  { mu |- n : mu  |>  lambda }

i.e. the e-support of a star-product of elementary symmetric functions is exactly
the DOMINANCE UPPER-INTERVAL of lambda = sort(l_1..l_k).

This CONTAINS Rick's min(a,b)+1 meta-conjecture as the two-factor case:
  { mu |> (a,b) } = { (a+b-k, k) : 0 <= k <= min(a,b) },  cardinality min(a,b)+1.

It also explains the 'conjugate of the classical Schur support' coincidence:
Schur supp(e_lambda) = { nu : nu' |> lambda }  (Kostka positivity K_{nu' lambda}>0
<=> nu' |> lambda), so conjugating gives exactly the same set.  Same rule, not a
collision.
"""
from hikita_star_clio import *
from triple import star_many, dominates
import itertools, sys, time

def all_lams(n, minparts=2):
    return [l for l in partitions(n) if len(l) >= minparts]

ok = True
for n in range(2, 8):
    for lam in all_lams(n):
        t0 = time.time()
        try:
            co, m = star_many(list(lam))
        except AssertionError as e:
            print("  n=%d lam=%s: EXPANSION FAILED: %s" % (n, lam, e)); ok=False; continue
        truth = sorted(co.keys(), reverse=True)
        pred  = sorted([mu for mu in partitions(n) if dominates(mu, lam)], reverse=True)
        good = truth == pred
        ok = ok and good
        print("  lam=%-14s n=%d m=%d  |supp|=%-3d pred=%-3d  %s  (%.1fs)"
              % (str(lam), n, m, len(truth), len(pred),
                 "OK" if good else "*** MISMATCH ***", time.time()-t0))
        if not good:
            print("      truth:", truth); print("      pred :", pred)
        sys.stdout.flush()
print("\nDOMINANCE CONJECTURE: %s" % ("ALL CASES PASS" if ok else "FAILED somewhere"))
