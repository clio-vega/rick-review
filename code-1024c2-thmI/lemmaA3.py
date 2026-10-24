"""A shorter proof of Lemma A(iii), offered to Rick.

His Lemma A(iii) proves N(T_{t*}) >= 1 by EXHIBITING a KLG-tableau (and the r-even case
needs a half-page of case analysis on which image box lands left/top).  But his own new
Theorem Q30 (crownF file) gives the vanishing criterion intrinsically on theta:

    V(theta) = 0  iff  theta has a 3-chain, or some diagonal box (c,c) in theta
                       has (c-1,c) in theta.

Both conditions are IMMEDIATE for T_{t*} from the antidiagonal structure:

 * No 3-chain.  Along a chain a+b strictly increases, and T_t occupies at most two
   antidiagonals, so no chain in T_t has 3 boxes.   (Works for t=1 and t=2 alike.)

 * No non-minimal diagonal box.  A diagonal box (c,c) has even coordinate sum 2c; its
   lower neighbour (c-1,c) has sum 2c-1, which is ODD.  So the two sit on antidiagonals of
   opposite parity, one apart.
     - r odd,  t*=1: T_1 is the single antidiagonal a+b = r-1 (EVEN).  (c-1,c) has odd sum
       r-2, so it is not in T_1.
     - r even, t*=2: T_2 = {r-2, r-1}.  r-2 is even, r-1 is odd, so a diagonal box must have
       2c = r-2; then (c-1,c) has sum r-3, which is not in {r-2, r-1}.
   Either way V(T_{t*}) = 2^i >= 1.

And the SAME criterion explains the negative control.  For r ODD with t=2, T_2 = {r-2, r-1}
and r-1 is EVEN, so a diagonal box can sit on the OUTER antidiagonal with 2c = r-1; then
(c-1,c) has sum r-2, which IS in T_2.  So V = 0 exactly when such a box exists -- which is
Rick's "forced prime on a diagonal box", now read off the intrinsic criterion.

This script verifies all three statements.  Clio 2026-10-24 c2.
"""
import sys
from fast import D, strict_partitions, r_of, N_LG
from q30thm import V_rick


def T_strip(Dk, r, t):
    return frozenset(b for b in Dk if b[0] + b[1] >= r - t)


def has_3chain(theta):
    bs = sorted(theta)
    for x in bs:
        for y in bs:
            if y != x and x[0] <= y[0] and x[1] <= y[1]:
                for z in bs:
                    if z != y and y[0] <= z[0] and y[1] <= z[1]:
                        return True
    return False


def nonmin_diag(theta):
    return [(c, c) for (c, d) in theta if c == d and (c - 1, c) in theta]


if __name__ == "__main__":
    MM = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    print("== CLAIM 1: T_{t*} has no 3-chain and no non-minimal diagonal box ==")
    c1 = c2 = tot = 0
    for m in range(1, MM + 1):
        for kap in strict_partitions(m):
            if not kap: continue
            Dk = D(kap, m); r = r_of(kap); t = 1 if r % 2 else 2
            T = T_strip(Dk, r, t); tot += 1
            if has_3chain(T): c1 += 1
            if nonmin_diag(T): c2 += 1
    print(f"   m<={MM}: {tot} nonempty kappa | with a 3-chain: {c1} | "
          f"with a non-minimal diagonal box: {c2}   (both must be 0)")

    print("\n== CLAIM 2: hence V(T_{t*}) >= 1, matching Lemma A(iii) and the KLG count ==")
    bad = mism = tot = 0
    for m in range(1, MM + 1):
        for kap in strict_partitions(m):
            if not kap: continue
            Dk = D(kap, m); r = r_of(kap); t = 1 if r % 2 else 2
            T = T_strip(Dk, r, t); tot += 1
            v = V_rick(T); n = N_LG(T, m)
            if v < 1: bad += 1
            if v != n: mism += 1
    print(f"   m<={MM}: {tot} kappa | V(T_t*) < 1 : {bad} | V != KLG count on R(T_t*) : {mism}")

    print("\n== CLAIM 3: for r ODD and t=2, V=0 EXACTLY when an outer diagonal box exists ==")
    agree = dis = tot = 0
    for m in range(1, MM + 1):
        for kap in strict_partitions(m):
            if not kap: continue
            r = r_of(kap)
            if r % 2 == 0: continue
            Dk = D(kap, m); T = T_strip(Dk, r, 2); tot += 1
            predicted_zero = bool(nonmin_diag(T)) or has_3chain(T)
            actual_zero = (N_LG(T, m) == 0)
            if predicted_zero == actual_zero: agree += 1
            else: dis += 1
    print(f"   r-odd kappa, m<={MM}: {tot} | criterion agrees with the KLG count: {agree}/{tot}"
          f" | disagreements: {dis}")
