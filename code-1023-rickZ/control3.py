"""Negative controls for TEST 3, plus a direct measurement of the 'multiplicity 2'.
Clio 2026-10-23."""
from fractions import Fraction
from testZ import H_poly, c_BR, dual, klg_count_p1
from demazure import strict_partitions
from comb import D, rprime, contains
import sys

for m in (2, 3):
    print(f"\n===== m={m} =====")
    ks = strict_partitions(m)
    POLY = {k: H_poly(k, m)[0] for k in ks}
    PTS = [Fraction(t, 2) for t in range(-8, 9)]

    def holds(k, terms):
        for jj in PTS:
            lhs = POLY[k](jj) - POLY[k](jj-1)
            rhs = sum(Fraction(c)*POLY[r](jj) for r, c in terms)
            if lhs != rhs: return False
        return True

    print("-- NEGATIVE CONTROL A: drop one nonzero term -> identity MUST fail")
    tested = failed = 0
    for k in ks:
        lam = dual(k, m)
        terms = [(r, c_BR(lam, dual(r, m), m)) for r in ks if c_BR(lam, dual(r, m), m)]
        if not terms: continue
        for d in range(len(terms)):
            t2 = terms[:d]+terms[d+1:]
            tested += 1
            if not holds(k, t2): failed += 1
    print(f"   {failed}/{tested} perturbations correctly FAIL  (want all)")

    print("-- NEGATIVE CONTROL B: bump one coefficient by +1 -> identity MUST fail")
    tested = failed = 0
    for k in ks:
        lam = dual(k, m)
        terms = [(r, c_BR(lam, dual(r, m), m)) for r in ks if c_BR(lam, dual(r, m), m)]
        if not terms: continue
        for d in range(len(terms)):
            t2 = list(terms); t2[d] = (t2[d][0], t2[d][1]+1)
            tested += 1
            if not holds(k, t2): failed += 1
    print(f"   {failed}/{tested} perturbations correctly FAIL  (want all)")

    print("-- NEGATIVE CONTROL C: 'reduced boundary' -- force every multiplicity to 1")
    print("   (Rick: 'Using the reduced boundary instead is wrong: off-diagonal components")
    print("    have multiplicity 2.'  So setting all |theta|=1 coefficients to 1 must fail.)")
    tested = failed = 0
    for k in ks:
        lam = dual(k, m)
        terms = [(r, c_BR(lam, dual(r, m), m)) for r in ks if c_BR(lam, dual(r, m), m)]
        if not terms: continue
        t2 = [(r, (1 if c > 0 else c)) for r, c in terms]
        if t2 == terms: continue
        tested += 1
        if not holds(k, t2): failed += 1
    print(f"   {failed}/{tested} reduced-boundary substitutions correctly FAIL  (want all)")

print("\n===== the 'multiplicity 2', measured: single-box theta =====")
print("BR Cor 5.6 at p=1 with |theta|=1 gives c = (-1)^0 * #KLG-tableaux:")
for box, name in (((0, 0), "DIAGONAL box (r,r)"), ((0, 1), "OFF-DIAGONAL box (r,c), c>r")):
    th = frozenset({box})
    print(f"  theta = {{{box}}}  {name:26s} -> #KLG-tableaux = {klg_count_p1(th)}  => c = {klg_count_p1(th)}")
print("  Condition (v) 'no diagonal box contains a primed integer' kills the 1' labelling")
print("  on the diagonal; off the diagonal both 1' and 1 are allowed. Hence 2.")

print("\n  Census of true single-box coefficients over all (kappa,rho), m<=4:")
for m in (2, 3, 4):
    ks = strict_partitions(m)
    from collections import Counter
    cc = Counter()
    for k in ks:
        lam = dual(k, m)
        for r in ks:
            nu = dual(r, m)
            c = c_BR(lam, nu, m)
            if c and len(D(nu, m)-D(lam, m)) == 1:
                th = next(iter(D(nu, m)-D(lam, m)))
                cc[(c, "diag" if th[0] == th[1] else "offdiag")] += 1
    print(f"   m={m}: {dict(cc)}")
