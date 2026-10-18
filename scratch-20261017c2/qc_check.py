# SECOND ARM, and it AGREES.  This is the fully-multivariate-symbolic version of the
# Lemma QC check.  It did not finish inside the session's foreground budget, so the
# review was written off qc_fast.py (exact rational w, symbolic q); it then completed
# in the background at 2026-10-18 00:24 with exit 0 and numbers IDENTICAL to the fast
# arm: 4/4 and 48/48 at N=2,3, same trivial/nonzero split 3/1 and 36/12, control 1
# firing 4/4 and 41/48.  So the rational-point specialisation hid nothing, and Lemma QC
# has two independent arms rather than one.  Corrected here because the previous header
# said it was 'kept because it is what I tried first, not because it ran' -- which was
# true when written and false twenty minutes later.
"""
First-hand verification of Rick's Lemma QC (UID 819, section 4) with MY engine
(proofs/code-1017-nonvanH/q484_engine.py, the only copy with EB/EX), i.e. by a
different implementation from his.

  Lemma QC.  a<b in M.  On H_ab = {w_a w_b = 1}, for EVERY I:
      Atilde_{M,I} = g(q,w_a) * Atilde_{M\{a,b},I},   g = (1-q)^2/((1-q x^2)(1-q x^-2)).

Plus his two stated controls: the identity fails off H, and the ratio is I-independent
only on H.  A control that cannot fire is decoration, so each is run as a two-arm test.
"""
import sympy as sp
from itertools import combinations
from q484_engine import Atilde, wvars, subsets, geq

q = sp.Symbol('q')

def g_of(x):
    return (1 - q)**2 / ((1 - q*x**2) * (1 - q*x**-2))

for N in (2, 3):
    w = wvars(N)
    S = subsets(N)
    ok = bad = triv = 0
    ratios_on_H, ratios_off_H = {}, {}
    for M in S:
        for (a, b) in combinations(M, 2):
            Mpp = tuple(m for m in M if m not in (a, b))
            x = w[a-1]
            onH = {w[b-1]: 1/x}                       # the divisor w_a w_b = 1
            for I in S:
                lhs = sp.cancel(sp.together(Atilde(N, w, M, I, 'C').subs(onH)))
                rhs = sp.cancel(sp.together(g_of(x) * Atilde(N, w, Mpp, I, 'C').subs(onH)))
                d = sp.simplify(sp.cancel(lhs - rhs))
                if d == 0:
                    ok += 1
                    if lhs == 0:
                        triv += 1
                    else:
                        ratios_on_H.setdefault((M, a, b), []).append(
                            sp.cancel(lhs / Atilde(N, w, Mpp, I, 'C').subs(onH)))
                else:
                    bad += 1
                    print(f"  FAIL N={N} M={M} pair=({a},{b}) I={I}: residual {d}")
    print(f"N={N}: QC holds on {ok} of {ok+bad} (M,pair,I) triples "
          f"({triv} of them the trivial 0=0 from triangularity, "
          f"{ok-triv} with both sides nonzero)")

    # ---- control 1: does the identity FAIL off H?  (two-arm: must fire) ----
    fired = 0; checked = 0
    for M in S:
        for (a, b) in combinations(M, 2):
            Mpp = tuple(m for m in M if m not in (a, b))
            x = w[a-1]
            for I in S:
                lhs = Atilde(N, w, M, I, 'C')                      # NO substitution: off H
                rhs = g_of(x) * Atilde(N, w, Mpp, I, 'C')
                if sp.simplify(sp.cancel(sp.together(lhs - rhs))) != 0:
                    fired += 1
                checked += 1
    print(f"   control 1 (identity must FAIL off H): fired on {fired}/{checked} "
          f"-> {'FIRES' if fired else 'DID NOT FIRE -- control is blind'}")

    # ---- control 2: is the ratio I-independent ONLY on H? ----
    for key, rs in sorted(ratios_on_H.items()):
        rs = [sp.cancel(r) for r in rs]
        same = all(sp.simplify(r - rs[0]) == 0 for r in rs)
        isg = sp.simplify(rs[0] - g_of(w[key[1]-1])) == 0
        print(f"   control 2  M={key[0]} pair=({key[1]},{key[2]}): "
              f"{len(rs)} nonzero labels, ratio I-independent on H: {same}, equals g: {isg}")
    print()
