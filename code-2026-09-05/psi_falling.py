"""
JOB 2, part 1 — Rick's OWN frame.  Psi = FALLING frame (his Day 155 table, knob 1).
    Psi(f) = T^-(f V)/V,   T^- : u^alpha -> prod_i (u_i)_{alpha_i},
    (u)_m = u(u-1)...(u-m+1)   [falling factorial]
His stated values, to be reproduced or refuted:
    Psi(e_2)|_{n=3}   = E_2 - E_1 + 1
    Psi(e_2)|_{n=4}   = E_2 - 3E_1 + 1
    Psi(e_2^2)|_{n=3} = E_2^2 - E_1E_2 - 3E_3
    PREDICTION (Day 155, the cell he calls decisive):
    Psi(e_2^2)|_{n=4} = E_2^2 - 5E_1E_2 + 6E_1^2 - 3E_3
Clio, 2026-09-05.
"""
import sympy as sp
from sympy.polys.polyfuncs import symmetrize

def falling(x, m):
    return sp.prod([x - j for j in range(m)]) if m > 0 else sp.Integer(1)

def Psi(f, u):
    n = len(u)
    V = sp.expand(sp.prod([u[i] - u[j] for i in range(n) for j in range(i+1, n)]))
    P = sp.Poly(sp.expand(sp.expand(f) * V), *u)
    num = sp.expand(sum(c * sp.prod([falling(u[i], a[i]) for i in range(n)])
                        for a, c in P.terms()))
    q, r = sp.div(sp.Poly(num, u[0]), sp.Poly(V, u[0]))
    assert r.is_zero, "V does not divide"
    return sp.expand(q.as_expr())

def toE(poly, u, Es):
    if sp.expand(poly) == 0: return sp.Integer(0)
    s, rem, _ = symmetrize(sp.expand(poly), list(u), formal=True)
    assert sp.expand(rem) == 0, f"not symmetric: {rem}"
    return sp.expand(s.subs({sp.Symbol(f's{k}'): Es[k-1] for k in range(1, len(u)+1)}))

def psiE(n, b):
    u  = sp.symbols(f'u1:{n+1}')
    Es = sp.symbols(f'E1:{n+1}')
    e2 = sp.expand(sum(u[i]*u[j] for i in range(n) for j in range(i+1, n)))
    return sp.expand(toE(Psi(sp.expand(e2**b), u), u, Es)), Es

E1, E2, E3, E4 = sp.symbols('E1 E2 E3 E4')

print("="*80)
print("A. Reproduce his stated values in HIS frame (falling).")
print("="*80)
claims = {
    (3,1): E2 - E1 + 1,
    (4,1): E2 - 3*E1 + 1,
    (3,2): E2**2 - E1*E2 - 3*E3,
}
for (n,b), claimed in claims.items():
    got, Es = psiE(n,b)
    d = sp.expand(got - claimed)
    print(f"  n={n} b={b}:  computed = {got}")
    print(f"           his stated = {claimed}")
    print(f"           difference = {d}   -> {'MATCH' if d==0 else '*** DIFFERS ***'}")

print("\n" + "="*80)
print("B. THE DECISIVE CELL.  His Day 155 prediction for n=4, b=2:")
print("     Psi(e_2^2)|_{n=4}  =?=  E_2^2 - 5E_1E_2 + 6E_1^2 - 3E_3")
print("="*80)
got42, Es4 = psiE(4,2)
pred42 = E2**2 - 5*E1*E2 + 6*E1**2 - 3*E3
print(f"  computed Psi(e_2^2)|_{{n=4}} = {got42}")
print(f"  his prediction              = {pred42}")
diff = sp.expand(got42 - pred42)
print(f"  difference                  = {sp.expand(diff)}")
print(f"  VERDICT: {'PREDICTION CONFIRMED' if diff==0 else 'prediction differs by the above'}")
if diff != 0:
    print(f"  difference factored        : {sp.factor(diff)}")
