"""Owed from UID 841: Rick's Theorem B (odd-zero-law file, line 127), which my 10-23
review recorded as "not verified, not endorsed".

**Theorem B.** Let M = 2a+1 with a >= m.  Then
   (-1)^{|kappa|} * 2^m * H_kappa(-M/2) = sum_{S subset [m]} h^0(Y, O_Y(-dY) (x) L_{lam_S}) >= 1.
In particular H_kappa has no zero at any half-integer j <= -m-1/2, and the sign is (-1)^{|kappa|}.

I cannot check the PROOF (Serre duality on a CM variety, (G2)/(G4), Lie-Kolchin filtration,
h^0 of line bundles on the P/B-bundle Y) by computation.  What I CAN check is the numeric
conclusion, with my own type-C Demazure engine, plus the integrality claim 2^m H in Z.
Clio 2026-10-24 c2.
"""
import sys
from fractions import Fraction
import demazure as C


def H_poly(kappa, m):
    S = C.subset_of_kappa(kappa, m)
    word = C.reduced_word(C.min_rep(sorted(S), m), m)
    d = sum(kappa)
    return C.lagrange([(j, C.chi(word, (j,) * m, m)) for j in range(d + 1)])


def run(MMAX, AEXTRA=4):
    print("== THEOREM B (conclusion only): M=2a+1, a >= m  =>  (-1)^|k| 2^m H(-M/2) >= 1 ==")
    for m in range(1, MMAX + 1):
        pos = bad = integ = integ_bad = tot = 0
        sign_bad = 0
        for kap in C.strict_partitions(m):
            f = H_poly(kap, m); sgn = (-1) ** sum(kap)
            for a in range(m, m + AEXTRA + 1):
                M = 2 * a + 1
                v = f(Fraction(-M, 2))
                q = sgn * (2 ** m) * v
                tot += 1
                if q >= 1: pos += 1
                else:
                    bad += 1
                    if bad <= 4: print(f"     FAIL m={m} kappa={kap} a={a}: (-1)^|k| 2^m H = {q}")
                if q.denominator == 1: integ += 1
                else: integ_bad += 1
                if v != 0 and (v > 0) != (sgn > 0): sign_bad += 1
        print(f"   m={m}: {tot} (kappa,a) points | >=1 : {pos}/{tot} | 2^m H in Z : {integ}/{tot}"
              f" | sign (-1)^|kappa| : {tot-sign_bad}/{tot}")
    return


def negctl(MMAX):
    """NEGATIVE CONTROL: Theorem B needs a >= m.  Below that bound the odd-zero law says
    there ARE zeros, so the SAME test must fail for a < m.  Otherwise 'a >= m' is decoration."""
    print("\n== NEGATIVE CONTROL: drop the hypothesis a >= m and test a < m ==")
    for m in range(2, MMAX + 1):
        zeros = tot = 0
        for kap in C.strict_partitions(m):
            f = H_poly(kap, m); sgn = (-1) ** sum(kap)
            for a in range(1, m):
                v = f(Fraction(-(2 * a + 1), 2)); tot += 1
                if sgn * (2 ** m) * v < 1: zeros += 1
        v = "FIRES -> 'a >= m' is load-bearing" if zeros else "*** SILENT -> hypothesis idle ***"
        print(f"   m={m}, a < m: {tot} points, {zeros} violate '>= 1'  -> {v}")


if __name__ == "__main__":
    MM = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    run(MM)
    negctl(MM)
