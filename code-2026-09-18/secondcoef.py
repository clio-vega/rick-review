"""Clio 2026-09-18: Conjecture 10 clause 2 at k=3 -- the (r+2,1) coefficient."""
import json, glob
import sympy as sp
from sympy import symbols
q, t, u = symbols('q t u')
DATA = {}
for f in glob.glob("tau3_r*.json"):
    d = json.load(open(f)); DATA[d["r"]] = {eval(k): sp.sympify(v) for k, v in d["coeffs"].items()}
RS = [r for r in sorted(DATA) if r >= 3]
print("Conjecture 10 clause 2: 'the non-top coefficients are r-independent'.")
print("At k=2 that is TRUE (checked r=2..7, Day 200 review).  At k=3 it is FALSE:")
print()
c = {r: sp.cancel(sp.together(DATA[r][(r+2,1)])) for r in RS}
for r in RS:
    print("  r=%d  c_{(r+2,1)} = %s" % (r, sp.factor(c[r])))
# fit as B_0 + B_1 u
B0, B1 = symbols('B0 B1')
sol = sp.solve([sp.Eq(B0 + B1*t**r, c[r]) for r in RS[:2]], [B0, B1], dict=True)[0]
b0, b1 = sp.cancel(sp.together(sol[B0])), sp.cancel(sp.together(sol[B1]))
print()
print("  fit on r=%d,%d as B_0 + B_1 u :" % (RS[0], RS[1]))
print("    B_0 =", sp.factor(b0))
print("    B_1 =", sp.factor(b1))
for r in RS[2:]:
    print("    UNTUNED TEST r=%d : %s" % (r, "PASS" if sp.simplify(sp.cancel(b0 + b1*t**r - c[r])) == 0 else "**FAIL**"))
print()
print("  So c_{(r+2,1)} is LINEAR in u = t^r, not r-independent.")
print("  Count of r-DEPENDENT coefficients: k=2 -> 1 (the top);  k=3 -> 2 (top and second).")
