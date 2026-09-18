"""
Clio 2026-09-18.  The structural question, done correctly.

From analyze.py: q^5 tau_r^(3) = A(t^r) with A(u) = sum_{j=0}^3 A_j u^j,
A_j in Q(q,t) r-independent (fitted r=1,2,3,4, untuned PASS at r=5).

sympy factors A(u) with an EXPLICIT (t^3 u - 1) factor.  Since
t^3 u - 1 = t^{r+3} - 1 = -(1-t)[r+3]_t, the factor [r+3]_t IS present in A(u)
identically in r.  But A(u) also carries t^3 - 1 = (t-1)Phi_3(t) in its
DENOMINATOR.  So the polynomial-divisibility question in Q(q)[t] is decided by
whether Phi_3(t) survives -- and it is eaten by [n]_t exactly when 3 | n.
That is a mechanism, not a coincidence, and it predicts every row.
"""
import json, glob
import sympy as sp
from sympy import symbols
q, t, u = symbols('q t u')

DATA = {}
for f in glob.glob("tau3_r*.json"):
    d = json.load(open(f)); r = d["r"]
    DATA[r] = {eval(k): sp.sympify(v) for k, v in d["coeffs"].items()}
RS = sorted(DATA)
def tau(r): return sp.cancel(sp.together(DATA[r][(r+3,)] * q**5))

A_ = symbols('A0 A1 A2 A3')
sol = sp.solve([sp.Eq(sum(A_[j]*t**(j*r) for j in range(4)), tau(r)) for r in (1,2,3,4)], A_, dict=True)[0]
Aj = [sp.cancel(sp.together(sol[a])) for a in A_]
Au = sp.cancel(sp.together(sum(Aj[j]*u**j for j in range(4))))
Nu, Du = sp.fraction(Au)
print("A(u) = N/D with")
print("  N =", sp.factor(Nu))
print("  D =", sp.factor(Du))

# the (t^3 u - 1) factor and the cofactor Q(u)
Q_ = sp.cancel(sp.simplify(Nu / (t**3*u - 1)))
print("\n  N / (t^3 u - 1) = Q(u) =", sp.expand(Q_))
print("  check: (t^3u-1)*Q - N == 0 ?", sp.simplify(sp.expand((t**3*u-1)*Q_ - Nu)) == 0)
print("  deg_u Q =", sp.Poly(Q_, u).degree())

print("\n" + "="*72)
print("CLAUSE 1 of Prediction 1, as an identity in u:  is [r+3]_t a factor of A(u)?")
print("  t^3 u - 1 = t^{r+3} - 1 = -(1-t)[r+3]_t, and it divides N exactly. ANSWER: YES.")
print("  So q^5 tau_r^(3) = (q^3-1) [r+3]_t Q(t^r) / (q Phi_3(t))   -- check:")
lhs = sp.cancel((q**3-1)*sp.Symbol('B')*1)  # placeholder
expr = sp.cancel((q**3 - 1) * ((t**(0)) ) )  # verified numerically below instead
for r in RS:
    n = r + 3
    bn = sum(t**i for i in range(n))
    cand = sp.cancel((q**3 - 1) * bn * Q_.subs(u, t**r) / (q * sp.cyclotomic_poly(3, t)))
    print("    r=%d: closed form == computed tau ?  %s" % (r, sp.simplify(sp.cancel(cand - tau(r))) == 0))

print("\n" + "="*72)
print("The POLYNOMIAL divisibility [n]_t | q^5 tau_r in Q(q)[t], for every n --")
print("decided from A(u) alone, no further Hikita computation:")
Phi3 = sp.cyclotomic_poly(3, t)
for r in range(1, 25):
    n = r + 3
    bn = sp.Poly(sum(t**i for i in range(n)), t)
    val = sp.cancel(sp.together(Au.subs(u, t**r)))
    num, den = sp.fraction(val)
    # q^5 tau_r is a t-polynomial (den is a power of q); divide by [n]_t
    QQ, RR = sp.div(sp.Poly(sp.expand(num), t), bn)
    ok = sp.simplify(RR.as_expr()) == 0
    # and the mechanism: does Phi_3 divide Q(t^r)?
    _, r3 = sp.div(sp.Poly(sp.expand(Q_.subs(u, t**r)), t), sp.Poly(Phi3, t))
    phi3_div = sp.simplify(r3.as_expr()) == 0
    print("   n=%2d (r=%2d)  3|n:%-5s  Phi_3 | Q(t^r):%-5s  [n]_t | q^5 tau_r: %s%s"
          % (n, r, str(n % 3 == 0), str(phi3_div), "YES" if ok else "NO ",
             "" if ok else "   remainder/den = " + str(sp.factor(sp.cancel(RR.as_expr()/den)))))
