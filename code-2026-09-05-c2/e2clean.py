"""Reciprocal spot-check of Rick's Day-169 26/26 on the E_2-shift.

UNTUNED cells: (n,b) with n>=5 that my own 2026-09-03 review never ran
(E2_shift_table.py ran only (3,1),(3,2),(3,3),(4,1),(4,2),(4,3),(5,1),(5,2)).
The rule under test is MY OWN derivation, so this is an independent recompute
from the definition of Psi^+, not a confirmation of his pipeline by his pipeline.

   tops^(n)[b], E_3-free part  =  (-1)^b prod_{r=0}^{b-1} (E_2 - (c_n + r) E_1),
   c_n = C(n-1,2) - C(2,2).
"""
import math
import sympy as sp
from sympy.polys.polyfuncs import symmetrize


def tops(n, b):
    u = sp.symbols(f'u1:{n+1}')
    V = sp.expand(sp.prod([u[i] - u[j] for i in range(n) for j in range(i + 1, n)]))
    e2 = sp.expand(sum(u[i] * u[j] for i in range(n) for j in range(i + 1, n)))
    rising = lambda x, m: sp.prod([x + j for j in range(m)]) if m > 0 else sp.Integer(1)
    P = sp.Poly(sp.expand(sp.expand(e2 ** b) * V), *u)
    num = sp.expand(sum(c * sp.prod([rising(u[i], a[i]) for i in range(n)]) for a, c in P.terms()))
    q, r = sp.div(sp.Poly(num, u[0]), sp.Poly(V, u[0]))
    assert r.is_zero, "V does not divide"
    s, rem, _ = symmetrize(sp.expand(q.as_expr()), list(u), formal=True)
    assert sp.expand(rem) == 0, "not symmetric"
    Es = sp.symbols(f'E1:{n+1}')
    expr = sp.expand(s.subs({sp.Symbol(f's{k}'): Es[k - 1] for k in range(1, n + 1)}))
    top = sp.Integer(0)
    for a, c in sp.Poly(expr, *Es).terms():
        if sum(a[k] * math.ceil((k + 1) / 2) for k in range(n)) == b:
            top += c * sp.prod([Es[k] ** a[k] for k in range(n)])
    return sp.expand(top), Es


for (n, b) in [(6, 1), (5, 3), (6, 2), (7, 1)]:
    top, Es = tops(n, b)
    free = sp.expand(top.subs({Es[k]: 0 for k in range(2, n)}))
    c_n = sp.binomial(n - 1, 2) - sp.binomial(2, 2)
    pred = sp.expand((-1) ** b * sp.prod([Es[1] - (c_n + r) * Es[0] for r in range(b)]))
    print(f"(n,b)=({n},{b})  c_n = C({n-1},2)-C(2,2) = {int(c_n)}")
    print(f"   computed  E3-free tops: {sp.factor(free)}")
    print(f"   predicted             : {sp.factor(pred)}")
    print(f"   -> {'AGREE' if sp.expand(free - pred) == 0 else '*** DISAGREE ***'}\n", flush=True)
