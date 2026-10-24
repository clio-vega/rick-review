"""Negative controls for referee33.py, done properly.

My first attempt lesioned the coefficient of C(theta-hat, p-a) in Thm 5.5 case (iv), a=1, and
the control stayed SILENT on all 1243 shapes.  Diagnosis: at p=1 and a=1 that argument is
C(theta-hat, 0), which is identically 0 because theta-hat is non-empty and p<=0.  The lesion
landed on a term that VANISHES at the evaluation point, so it could not possibly show.  The
test was fine; the control was aimed at a dead term.

At p = 1 the live arms of the recursion are exactly:
    (iii) a=1 -> -C(hat,1)                 [a>=2 collapses to 0]
    (iv)  a=1 -> -2 C(hat,1)
    (iv)  a=2 -> +C(hat,1)                 [a>=3 collapses to 0]
    (i),(ii) base cases on rows/columns
which is precisely the case list Rick's Sec. 3.3 walks through.  So each control below lesions a
coefficient that is actually multiplied by something non-zero at p=1.
Clio 2026-10-24 c2.
"""
import sys
from functools import lru_cache
import referee33 as R


def make_C(lesion):
    @lru_cache(maxsize=None)
    def C(theta, p):
        if not theta:
            return 1 if p <= 0 else 0
        if not R.is_rim(theta):
            return 0
        if p <= 0:
            return 0
        psi = R.ne_arm(theta); hat = frozenset(theta) - psi
        a = len(theta) - len(hat); n = len(theta)
        if not hat:
            if R.meets_diagonal(theta):
                if R.is_col(theta):
                    k = 0 if lesion == 'i_col_drop' else 1
                    return (1 if p == n else 0) - k * (1 if p == n - 1 else 0)
                return 1 if p == n else 0
            k = 1 if lesion == 'ii_two_to_one' else 2
            return k * (1 if p == n else 0) - (1 if p == n - 1 else 0)
        if R.connected(psi, hat):
            k = 1 if lesion == 'iii_sign_flip' else -1
            return C(hat, p - a) + k * C(hat, p - a + 1)
        if a == 1:
            k = 1 if lesion == 'iv_a1_two_to_one' else 2
            return 2 * C(hat, p - a) - k * C(hat, p - a + 1)
        k = 2 if lesion == 'iv_a2_last_coeff' else 1
        return 2 * C(hat, p - a) - 3 * C(hat, p - a + 1) + k * C(hat, p - a + 2)
    return C


if __name__ == "__main__":
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    S = [th for th in R.shapes(NMAX) if len(th) <= 13]
    truth = {th: R.T(th) for th in S}
    print(f"== Thm 5.5 recursion vs brute-force KLG count, {len(S)} shifted skew shapes "
          f"(nu_1 <= {NMAX}) ==")
    base = make_C(None)
    agree = sum(1 for th in S if base(th, 1) == truth[th])
    print(f"   UNLESIONED: {agree}/{len(S)} agree\n")
    print("== NEGATIVE CONTROLS: each lesions a coefficient that is LIVE at p=1 ==")
    for name in ('iii_sign_flip', 'iv_a1_two_to_one', 'iv_a2_last_coeff',
                 'ii_two_to_one', 'i_col_drop'):
        Cl = make_C(name)
        bad = sum(1 for th in S if Cl(th, 1) != truth[th])
        v = "FIRES" if bad else "*** SILENT -- not covered by this test ***"
        print(f"   {name:20s}: disagrees on {bad:4d}/{len(S)}  -> {v}")
    print("\n== for the record, the control that was WRONGLY silent first time ==")
    @lru_cache(maxsize=None)
    def Cdead(theta, p):
        if not theta: return 1 if p <= 0 else 0
        if not R.is_rim(theta): return 0
        if p <= 0: return 0
        psi = R.ne_arm(theta); hat = frozenset(theta) - psi
        a = len(theta) - len(hat); n = len(theta)
        if not hat:
            if R.meets_diagonal(theta):
                if R.is_col(theta): return (1 if p==n else 0) - (1 if p==n-1 else 0)
                return 1 if p==n else 0
            return 2*(1 if p==n else 0) - (1 if p==n-1 else 0)
        if R.connected(psi, hat): return Cdead(hat,p-a) - Cdead(hat,p-a+1)
        if a == 1: return 1*Cdead(hat,p-a) - 2*Cdead(hat,p-a+1)   # coeff of a VANISHING term
        return 2*Cdead(hat,p-a) - 3*Cdead(hat,p-a+1) + Cdead(hat,p-a+2)
    bad = sum(1 for th in S if Cdead(th, 1) != truth[th])
    print(f"   iv_a1_FIRST_coeff (multiplies C(hat,0) == 0 at p=1): {bad}/{len(S)}"
          f"  -> correctly silent: the lesion is on a dead term, not a gap in coverage")
