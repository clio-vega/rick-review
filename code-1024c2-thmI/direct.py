"""Rick's Q33: can we evaluate (D_w e^{-j omega})(1) DIRECTLY at negative weights,
instead of interpolating the Hilbert polynomial?  His check.py/mono.py were KILLED at
m=5 (exact-Fraction interpolation at degree 15), so m>=5 is unchecked in his file.

His own Lemma P (odd-zero-law file) says lambda -> [D_w e^lambda](0) is a POLYNOMIAL on
C^m of degree <= l(w), and equals H_kappa(j omega) for integers j >= 0.  Two polynomials
agreeing on j>=0 agree everywhere.  For INTEGRAL lambda the germ-evaluation at h=0 is the
Laurent coefficient sum -- which is exactly what the three-case Demazure recursion returns.
So direct negative evaluation should be EXACT.  Test it, then use it.
"""
import sys, time
import demazure as C, demazureB as B
from comb import strict_partitions

def H_LG_direct(kappa, m, j):
    S = C.subset_of_kappa(kappa, m); w = C.min_rep(sorted(S), m)
    return C.chi(C.reduced_word(w, m), (j,)*m, m)

def H_OG_direct(kappa, m, j):
    S = C.subset_of_kappa(kappa, m); w = C.min_rep(sorted(S), m)
    return B.chiB(C.reduced_word(w, m), (j,)*m, m)

def H_LG_interp(kappa, m):
    d = sum(kappa); js = list(range(d+1))
    return C.lagrange([(j, H_LG_direct(kappa, m, j)) for j in js])

print("== CONTROL: direct negative evaluation  vs  interpolated Hilbert polynomial ==")
bad = 0; tot = 0
for m in range(1, 5):
    for kap in strict_partitions(m):
        f = H_LG_interp(kap, m); g = B.H_OG_poly(kap, m)
        for j in range(-(sum(kap)+4), 1):
            a = f(j); b = H_LG_direct(kap, m, j); tot += 1
            if a != b:
                bad += 1
                if bad <= 6: print(f"   LG MISMATCH m={m} kappa={kap} j={j}: poly={a} direct={b}")
            a2 = g(j); b2 = H_OG_direct(kap, m, j); tot += 1
            if a2 != b2:
                bad += 1
                if bad <= 6: print(f"   OG MISMATCH m={m} kappa={kap} j={j}: poly={a2} direct={b2}")
    print(f"   m<={m}: {tot} (kappa,j) evaluations, mismatches = {bad}")
print(f"\n   => direct negative evaluation is {'EXACT' if bad==0 else 'WRONG'} ({bad}/{tot} bad)")
