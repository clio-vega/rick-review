"""
First-hand verification of Rick's Lemma QC (UID 819 section 4) with MY engine
(proofs/code-1017-nonvanH/q484_engine.py) -- a different implementation from his.

  Lemma QC.  a<b in M.  On H_ab = {w_a w_b = 1}, for EVERY I:
      Atilde_{M,I} = g(q,w_a) * Atilde_{M\\{a,b},I},   g = (1-q)^2/((1-q x^2)(1-q x^-2)).

Strategy: exact rational values for w (with w_b = 1/w_a imposed exactly, i.e. ON H),
q kept SYMBOLIC.  So each test is an identity of rational functions in q -- exact, and
far cheaper than full multivariate symbolics.  Several w-seeds per N.

Controls, each run as a two-arm test so that a green cannot be vacuous:
  C1  the identity must FAIL off H  (w_b perturbed off the divisor)
  C2  the ratio Atilde_{M,I}/Atilde_{M'',I} must be I-INDEPENDENT on H and equal g
  C3  a PLANTED wrong multiplier (g with x^2 -> x^3) must be rejected
"""
import sympy as sp
from itertools import combinations
from fractions import Fraction
import q484_engine as E

q = E.q
SEEDS = [[sp.Rational(3), sp.Rational(5), sp.Rational(7), sp.Rational(11)],
         [sp.Rational(2), sp.Rational(1,3), sp.Rational(5,2), sp.Rational(7,4)]]

def g_of(x, power=2):
    return (1 - q)**2 / ((1 - q*x**power) * (1 - q*x**(-power)))

def run(N, seed, power=2, off_H=False):
    """returns (ok, bad, trivial, ratio_report)"""
    base = seed[:N]
    S = E.subsets(N)
    ok = bad = triv = 0
    ratio = {}
    for M in S:
        for (a, b) in combinations(M, 2):
            Mpp = tuple(m for m in M if m not in (a, b))
            w = list(base)
            x = w[a-1]
            w[b-1] = 1/x * (sp.Rational(5,4) if off_H else 1)   # ON or OFF the divisor
            for I in S:
                lhs = sp.cancel(E.Atilde(N, w, M, I, 'C'))
                r0 = sp.cancel(E.Atilde(N, w, Mpp, I, 'C'))
                rhs = sp.cancel(g_of(x, power) * r0)
                if sp.cancel(sp.together(lhs - rhs)) == 0:
                    ok += 1
                    if lhs == 0:
                        triv += 1
                    elif r0 != 0:
                        ratio.setdefault((M, a, b), []).append((I, sp.cancel(lhs / r0)))
                else:
                    bad += 1
    return ok, bad, triv, ratio

print("=" * 78)
print("LEMMA QC, my engine, q symbolic, w exact rational ON the divisor w_a w_b = 1")
print("=" * 78)
for N in (2, 3, 4):
    for si, seed in enumerate(SEEDS):
        ok, bad, triv, ratio = run(N, seed)
        print(f"N={N} seed{si}: QC holds on {ok}/{ok+bad} (M,pair,I)  "
              f"[{triv} trivial 0=0 by triangularity, {ok-triv} both sides nonzero]"
              f"{'   *** FAILURES: %d ***' % bad if bad else ''}")
    # ---- C2: I-independence of the ratio, and ratio == g ----
    ok, bad, triv, ratio = run(N, SEEDS[0])
    for (M, a, b), rs in sorted(ratio.items()):
        vals = [v for (_, v) in rs]
        same = all(sp.cancel(v - vals[0]) == 0 for v in vals)
        isg = sp.cancel(vals[0] - g_of(SEEDS[0][a-1])) == 0
        print(f"   C2  M={M} pair=({a},{b}): {len(vals)} nonzero labels, "
              f"ratio I-independent={same}, ratio==g: {isg}")
print()
print("=" * 78)
print("CONTROLS -- each must FIRE, or the green above is decoration")
print("=" * 78)
for N in (2, 3):
    ok, bad, triv, _ = run(N, SEEDS[0], off_H=True)
    print(f"C1 N={N}  identity OFF the divisor (w_b = 5/(4 w_a)): "
          f"holds {ok}, fails {bad}  ->  {'FIRES' if bad else 'DID NOT FIRE (blind)'}")
for N in (2, 3):
    ok, bad, triv, _ = run(N, SEEDS[0], power=3)
    print(f"C3 N={N}  PLANTED multiplier g with x^2 -> x^3, on the divisor: "
          f"holds {ok}, fails {bad}  ->  {'FIRES' if bad else 'DID NOT FIRE (blind)'}")
