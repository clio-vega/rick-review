"""Clio 2026-09-18 -- final structural statement and its untuned tests."""
import json, glob
import sympy as sp
from sympy import symbols
q, t, u = symbols('q t u')
DATA = {}
for f in glob.glob("tau3_r*.json"):
    d = json.load(open(f)); DATA[d["r"]] = {eval(k): sp.sympify(v) for k, v in d["coeffs"].items()}
RS = sorted(DATA)
def tau(r): return sp.cancel(sp.together(DATA[r][(r+3,)] * q**5))
A_ = symbols('A0 A1 A2 A3')
sol = sp.solve([sp.Eq(sum(A_[j]*t**(j*r) for j in range(4)), tau(r)) for r in (1,2,3,4)], A_, dict=True)[0]
Aj = [sp.cancel(sp.together(sol[a])) for a in A_]
Au = sp.cancel(sp.together(sum(Aj[j]*u**j for j in range(4))))
Nu, Du = sp.fraction(Au)
Q_ = sp.cancel(sp.simplify(Nu/(t**3*u - 1)))          # includes the (q^3-1)
Phi3 = sp.cyclotomic_poly(3, t)

print("="*72)
print("THE CLOSED FORM.   [n]_t := 1+t+...+t^{n-1},  n = r+3,  u = t^r,  Phi_3 = 1+t+t^2")
print()
print("   q^5 tau_r^(3)  =  [r+3]_t * Q(t^r) / ( q * Phi_3(t) ),     Q(u) = (q^3-1) * C(u),")
C_ = sp.cancel(sp.simplify(Q_/(q**3 - 1)))
print()
print("   C(u) =", sp.collect(sp.expand(C_), u))
print()
for r in RS:
    n = r+3
    bn = sum(t**i for i in range(n))
    cand = sp.cancel(bn * Q_.subs(u, t**r) / (q * Phi3))
    tag = "  <-- UNTUNED (fit used r=1,2,3,4 only)" if r not in (1,2,3,4) else ""
    print("   r=%d: closed form == tau computed on the Hikita instrument (m=%d)?  %s%s"
          % (r, r+3, sp.simplify(sp.cancel(cand - tau(r))) == 0, tag))

print()
print("="*72)
print("PREDICTION 1, CLAUSE 1 -- 'q^5 tau_r^(3) is divisible by [r+3]_t'")
print("  As an identity in u over Q(q,t): the factor IS there, exactly. (t^3 u - 1) | A(u).")
qq, rr = sp.div(sp.Poly(Nu, u), sp.Poly(sp.expand(t**3*u - 1), u))
print("    remainder of A(u) by (t^3 u - 1):", sp.simplify(rr.as_expr()))
print("  As polynomial divisibility in Q(q)[t] at fixed r: holds iff 3 does NOT divide r+3,")
print("  because Phi_3(t) sits in the DENOMINATOR and is cancelled by [r+3]_t exactly when 3|r+3.")
print("    verified for n = 4..27 in analyze2.py; two full independent Hikita computes agree:")
print("      n=6  (r=3, m=6) remainder 3q^2(q^3-1)(t^3+1)      -- matches Rick's S5 value")
print("      n=9  (r=6, m=9) remainder 3q^2(q^3-1)(t^6+t^3+1)  -- predicted from A(u) first, then computed")

print()
print("="*72)
print("PREDICTION 1, CLAUSE 2 -- 'splits into three linear forms in u'")
print("  A(u) = (t^3u-1) * C(u) * (q^3-1) / (q(t^3-1)); C is a quadratic in u.")
P = sp.Poly(sp.expand(C_), u)
a2, a1, a0 = P.all_coeffs()
disc = sp.factor(sp.expand(a1**2 - 4*a2*a0))
print("  C(u) = (%s) u^2 + (%s) u + (%s)" % (sp.factor(a2), sp.factor(a1), sp.factor(a0)))
print("  discriminant =", disc)
sq = sp.sqrt(sp.expand(a1**2 - 4*a2*a0))
print("  is the discriminant a square in Q(q,t)?  ", sp.simplify(sq - sp.nsimplify(sq)) == 0 and sq.is_polynomial(q, t))
fl = sp.factor_list(sp.expand(a1**2 - 4*a2*a0))
print("  factor_list of the discriminant:", fl)
allsq = all(e % 2 == 0 for _, e in fl[1]) and sp.simplify(fl[0] - sp.Integer(fl[0])) == 0
print("  every irreducible factor to an EVEN power (=> perfect square)?", all(e % 2 == 0 for _, e in fl[1]), " unit:", fl[0])
print("  => C(u) splits into two linear forms over Q(q,t)?", allsq)
print()
print("  CONTRAST, k=2 (my Day 200 result): discriminant t^2(qt-q-t^2-t)^2, a perfect square,")
print("  which is exactly why tau_r^(2) factors completely into linear forms.")
