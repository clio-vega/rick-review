"""
Clio, 2026-09-18 peer review of Rick's Day 204 PDF (email UID 720).

INDEPENDENT recomputation of tau_r^(3) := coefficient of e_{(r+3)} in p_3(Y) . e_r,
the object of Rick's S5 "Prediction 1 REFUTED" table, using ONLY my own
implementation of Hikita Def 3.4 / eq Eqn_Y_i (hikita_star_clio.py, built
2026-09-16 from arXiv:2503.23597 LaTeX source; self-tests in
../code-2026-09-16/selftest.py all pass).  Shares no code with his
scripts/day204/conj10_divisibility_test.py.

Three jobs:
  (1) r=3: is q^5 tau_r^(3) divisible by [6]_t, and if not is the remainder
      exactly his 3 q^2 (q^3-1)(t^3+1)?
  (2) the u-degree of the quotient where divisibility holds.
  (3) the DISCRIMINATING cases his sample never ran: r=6 (n=9=3^2, one prime,
      3|n) and r=9 (n=12=2^2.3, two primes, 3|n).  His sample n=4,5,6,7,8 has
      "3|n" and "n has two distinct prime factors" true on exactly the same
      single row (n=6), so it cannot separate the two explanations.
"""
import sys, time
from hikita_star_clio import *
from sympy import symbols, Poly, simplify, factor_list, div, together, cancel
import sympy as sp

def p3Y(A, m):
    """p_3(Y_1..Y_m) . A = sum_i Y_i^3 . A."""
    tot = {}
    for i in range(1, m+1):
        tot = add(tot, Y(i, Y(i, Y(i, A, m), m), m))
    return tot

def to_sympy(f):
    """FF element (q,t fraction field) -> sympy expression."""
    qs, ts = symbols('q t')
    return sp.sympify(str(f)).subs({symbols('q'): qs, symbols('t'): ts})

def brack(n, ts):
    """[n]_t = 1 + t + ... + t^{n-1}."""
    return sum(ts**i for i in range(n))

def run(r):
    m = r + 3                      # minimal m for the degree-(r+3) e-basis to be independent
    t0 = time.time()
    A = p3Y(e_poly(r, m), m)
    co = expand_in_e(A, r+3, m)
    el = time.time() - t0
    tau = co.get((r+3,), ZERO)
    print("r=%d  m=%d  (%.1fs)  support = %s" % (r, m, el, sorted([k for k,v in co.items() if v], reverse=True)))
    sys.stdout.flush()
    return tau, co

if __name__ == "__main__":
    rs = [int(x) for x in sys.argv[1:]] or [3]
    qs, ts = symbols('q t')
    for r in rs:
        tau, co = run(r)
        expr = sp.cancel(sp.together(to_sympy(tau) * qs**5))
        n = r + 3
        num, den = sp.fraction(expr)
        print("  q^5 tau_r^(3), r=%d:" % r)
        print("    denominator:", sp.factor(den))
        Bn = brack(n, ts)
        # polynomial division of numerator by [n]_t in t over Q(q)
        Q_, R_ = sp.div(sp.Poly(sp.expand(num), ts), sp.Poly(sp.expand(Bn), ts))
        R_ = sp.simplify(R_.as_expr())
        print("    [%d]_t divides numerator? %s" % (n, R_ == 0))
        if R_ != 0:
            print("    remainder (over den %s): %s" % (sp.factor(den), sp.factor(R_)))
            rick = 3*qs**2*(qs**3-1)*(ts**3+1)
            print("    remainder / den  =", sp.factor(sp.cancel(R_/den)))
            print("    Rick's stated remainder 3q^2(q^3-1)(t^3+1) matches R/den? ",
                  sp.simplify(sp.cancel(R_/den) - rick) == 0)
            print("    ... matches R itself? ", sp.simplify(R_ - rick) == 0)
            # numeric check at q=1.7, t=primitive cube root
            w = sp.Rational(-1,2) + sp.I*sp.sqrt(3)/2
            print("    R/den at q=1.7, t=exp(2pi i/3):",
                  sp.N(sp.cancel(R_/den).subs({qs: sp.Rational(17,10), ts: w}), 6))
            print("    full q^5 tau at q=1.7, t=exp(2pi i/3):",
                  sp.N(expr.subs({qs: sp.Rational(17,10), ts: w}), 6))
        else:
            quo = sp.cancel(Q_.as_expr()/den)
            print("    quotient:", sp.factor(quo))
        sys.stdout.flush()
