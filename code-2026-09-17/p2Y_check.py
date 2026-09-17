"""
Clio, 2026-09-17 peer review of Rick's Day 200 PDF.

INDEPENDENT check of Rick's Lemma 9 (p_2(Y)-Pieri) and his Day-200 closed form
for tau_r(q,t), eqs (11)-(15) of
  peers/rick/proofs/2026-09-17-day200-clio-five-defects.pdf

Uses ONLY my own 2026-09-16 implementation of Hikita Def 3.4 / eq Eqn_Y_i
(hikita_star_clio.py), which is validated in selftest.py against the AHA
relations, Lem 3.3, Prop 3.6 and Hikita Thm 3.12 before use.
Rick's repo pin ca3167b is unreachable, so none of his scripts are used.
"""
import sys, time
from hikita_star_clio import *

def p2Y(A, m):
    """p_2(Y_1..Y_m) . A = sum_i Y_i^2 . A."""
    tot = {}
    for i in range(1, m+1):
        tot = add(tot, Y(i, Y(i, A, m), m))
    return tot

def rick_tau(r):
    """Rick eq (12)-(15): q^3 tau_r = A + B t^r + C t^{2r}."""
    A = -(q**2 - ONE)*(q - t - ONE) / (t**2 - ONE)
    B =  t*(q**2 - ONE)*(q - t) / (t - ONE)
    C = -q*t**3*(q**2 - ONE) / (t**2 - ONE)
    return (A + B*t**r + C*t**(2*r)) / q**3

def rick_pretty(r):
    """Rick eq (16): tau_r = K/q^3 [ (q-t-1) - (t+1)(q-t) t^{r+1} + q t^{2r+3} ]."""
    K = -(q**2 - ONE)/(t**2 - ONE)
    return K*((q - t - ONE) - (t + ONE)*(q - t)*t**(r+1) + q*t**(2*r+3)) / q**3

# Rick's three r-independent coefficients, eq (11)
COEF_r11 = ONE/q**3
COEF_r2  = -(q*t - q + t + ONE)/q**3
COEF_r1p = (q**2 - ONE)/q**3

rmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
for r in range(2, rmax+1):
    m = r + 2                      # minimal m for the degree-(r+2) e-basis to be independent
    t0 = time.time()
    A = p2Y(e_poly(r, m), m)
    co = expand_in_e(A, r+2, m)
    co = {k: v for k, v in co.items() if v}
    el = time.time() - t0
    print("r=%d  m=%d  (%.1fs)  support = %s" % (r, m, el, sorted(co, reverse=True)))
    want = {(r,1,1): COEF_r11, (r,2): COEF_r2, (r+1,1): COEF_r1p, (r+2,): rick_tau(r)}
    if r == 2:  # (2,2) and (r,2) coincide; (r,1,1)=(2,1,1)
        pass
    allok = True
    for lam in sorted(set(list(co)+list(want)), reverse=True):
        got, exp = co.get(lam, ZERO), want.get(lam, ZERO)
        ok = (got - exp) == ZERO
        allok = allok and ok
        print("    %-10s %s   Rick: %s" % (str(lam), "MATCH" if ok else "**MISMATCH**",
              "" if ok else str(exp) + "   mine: " + str(got)))
    print("    (12) vs (16) agree:", (rick_tau(r) - rick_pretty(r)) == ZERO)
    print("    Lemma 9 at r=%d: %s" % (r, "CONFIRMED" if allok else "FAILED"))
    sys.stdout.flush()
