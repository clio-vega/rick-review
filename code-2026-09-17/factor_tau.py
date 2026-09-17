"""Clio 2026-09-17: does Rick's tau_r bracket factor as a quadratic in u = t^r?
Conjecture 10 makes q^{2k-1} tau^{(k)}_r a degree-k polynomial in u.  At k=1 it is
linear (Hikita Thm 3.12).  If at k=2 it splits into Baxterised linear forms, that
predicts the k=3 shape and is a far sharper target than the fit."""
import sympy as sp
q,t,u = sp.symbols('q t u')
A = -(q**2-1)*(q-t-1)/(t**2-1)
B =  t*(q**2-1)*(q-t)/(t-1)
C = -q*t**3*(q**2-1)/(t**2-1)
P = sp.simplify(A + B*u + C*u**2)
print("q^3 tau_r, with u = t^r:"); sp.pprint(sp.factor(P))
print()
print("factor over Q(q,t)[u]:"); print(sp.factor(P, u))
print()
disc = sp.simplify(sp.discriminant(sp.expand(P*(t**2-1)/(q**2-1)), u))
print("discriminant of the bracket in u:"); print(sp.factor(disc))
print("is it a perfect square in Q(q,t)?:", sp.simplify(sp.sqrt(sp.factor(disc))))
print()
# k=1 comparison: q*tau^{(1)}_r from Hikita Thm 3.12
P1 = sp.expand(q*(1-1/q)*(1-t*u)/(1-t))
print("k=1 (Hikita Thm 3.12), q*tau^(1)_r in u:"); print(sp.factor(P1))
