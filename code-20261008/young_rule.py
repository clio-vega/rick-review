"""Rick's Young's-rule derivation (WIP 0798053, 2026-10-08-two-row-green-is-young.pdf),
checked against the independent engine -- and against Jing-Liu.

    X^{(n-k,k)}_rho(t) = pi_k(rho) + (t-1) sum_{j<k} t^{k-1-j} pi_j(rho)

pi_j(rho) = # of j-subsets of {1..n} fixed by a permutation of cycle type rho
          = # of sub-multisets of the parts of rho summing to j.
"""
import sympy as sp
from fractions import Fraction as F
from itertools import product
from hl_orthogonality import GreenEngine, partitions
from jingliu import X_jingliu
t = sp.Symbol('t')

def pi_coeffs(rho, jmax):
    """pi_j(rho) via sub-multisets of parts: gen fn prod_i (1 + u^{rho_i})."""
    poly = sp.Poly(sp.expand(sp.prod([(1 + t**r) for r in rho])), t)
    return [poly.coeff_monomial(t**j) or 0 for j in range(jmax + 1)]

def X_young(lam, rho):
    n_k, k = lam
    pi = pi_coeffs(rho, max(k, sum(rho)))
    return sp.expand(pi[k] + (t-1)*sum(t**(k-1-j)*pi[j] for j in range(k)))

if __name__ == '__main__':
    # (0) pi_j == Jing-Liu's D^{(j)}?  (prod over parts vs prod over multiplicities)
    same = all(sp.expand(sp.prod([(1+t**r) for r in rho])
                         - sp.prod([(1+t**i)**rho.count(i) for i in set(rho)])) == 0
               for n in range(1, 9) for rho in partitions(n))
    print('pi_j(rho) == Jing-Liu D^{(j)}(rho) as generating functions : %s' % same)

    # (1) Rick's Young's-rule form vs the independent engine, two-row lambda, ARBITRARY rho
    TV = [F(2), F(3), F(5), F(-2), F(1,2), F(7,3)]
    bad = tot = 0; rows = 0; badJ = 0
    for n in range(2, 10):
        eng = {tv: GreenEngine(n, tv) for tv in TV}
        for k in range(0, n//2 + 1):
            lam = (n-k, k) if k > 0 else (n,)
            if k > 0 and n-k < k: continue
            for rho in partitions(n):
                rows += 1
                XY = X_young((n-k, k), rho)
                if sp.expand(XY - X_jingliu((n-k, k), rho)) != 0: badJ += 1
                for tv in TV:
                    tot += 1
                    lhs = sp.Rational(XY.subs(t, sp.Rational(tv)))
                    rhs = sp.Rational(eng[tv].X(lam, rho).numerator, eng[tv].X(lam, rho).denominator)
                    if sp.simplify(lhs - rhs) != 0:
                        bad += 1
                        if bad <= 4: print('  FAIL', lam, rho, tv, lhs, rhs)
    print()
    print("Rick's Young's-rule formula, two-row lambda x ARBITRARY rho, n=2..9")
    print('  (lambda, rho) rows                      : %d' % rows)
    print('  symbolic mismatches vs Jing-Liu sec 2   : %d' % badJ)
    print('  numeric  mismatches vs engine (%d evals): %d' % (tot, bad))

    # (2) does it reproduce Theorem C?  (his explicit ask)
    from compare_rick_day228 import X_clio_thmC, X_rick
    badC = badR = nC = 0
    for n in range(2, 11):
        for l2 in range(1, n//2 + 1):
            lam = (n-l2, l2)
            for y in range(1, n):
                x = n - y; rho = tuple(sorted((x, y), reverse=True)); nC += 1
                XY = X_young(lam, rho)
                if sp.expand(XY - sp.expand(X_clio_thmC(lam, x, y, t))) != 0: badC += 1
                if sp.expand(XY - sp.expand(X_rick(lam, x, y, t))) != 0: badR += 1
    print()
    print("  vs Clio Thm C, symbolic, %d rows        : %d mismatches" % (nC, badC))
    print("  vs Rick Day 228, symbolic, %d rows      : %d mismatches" % (nC, badR))
