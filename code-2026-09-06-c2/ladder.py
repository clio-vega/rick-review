"""CAVEAT (Clio, 2026-09-06 c2): the linear fit below is UNDER-DETERMINED at the
truncation order used -- it returns a spurious solution that does not even reproduce the
known m=1 answer (Day 168 Result 2).  The STRUCTURAL observation in the docstring is a
one-line fact and stands; the closed-form consequence is a CONJECTURE, not verified here.
Do not cite this script as evidence for anything.

Prop 2's pin u_3=-1 works because u_3^{(c)} = u_3(u_3+1)...(u_3+c-1) vanishes at
u_3=-1 for c >= 2.  But a rising factorial vanishes on the whole ladder {0,-1,-2,...}:
at u_3 = -m it kills c >= m+1.  So a Prop-2-style constructive formula should exist at
EVERY negative integer, with m+1 surviving powers.  Test: is F_{-m} in the
Q(T,s,p)-span of {1, I, F_0, F_0'} (I = int F_0)?"""
import sympy as sp
from series import *
from build_FP import FP_series
N = 7
Tv = Tser(N)
F0 = trim(FP_series(0, N), N)
I0 = integ(F0); F0p = deriv(F0)
one = const(1, N)
basis = [one, I0, F0, F0p]
for m in [1, 2, 3]:
    Fm = trim(FP_series(-m, N), N)
    a = sp.symbols(f'a0:4')
    # allow coefficients rational in T: try polynomial in T of degree <= 3
    deg = 2
    cs = sp.symbols(f'c0:{4*(deg+1)}')
    comb = [sp.Integer(0)]*(N+1)
    for bi, B in enumerate(basis):
        for d in range(deg+1):
            comb = add(comb, smul(cs[bi*(deg+1)+d]*sp.Symbol('T')**0, mul(powr(Tv, d), B)))
    eqs = []
    for n in range(N-1):
        eqs.append(sp.expand(Fm[n] - comb[n]))
    sol = sp.solve(eqs, cs, dict=True)
    if not sol:
        print(f"u_3 = -{m}:  NO fit in span{{1,I,F_0,F_0'}} with deg<=3 T-coefficients")
        continue
    sol = sol[0]
    got = {k: sp.simplify(v) for k, v in sol.items() if sp.simplify(v) != 0}
    names = ['1', 'I', 'F0', "F0'"]
    out = []
    for bi in range(4):
        poly = sum(sol.get(cs[bi*(deg+1)+d], cs[bi*(deg+1)+d])*sp.Symbol('T')**d for d in range(deg+1))
        poly = sp.simplify(poly.subs({c: 0 for c in cs if c not in sol}))
        if poly != 0: out.append(f"({sp.factor(poly)})*{names[bi]}")
    print(f"u_3 = -{m}:  F_{{-{m}}} = " + " + ".join(out))
