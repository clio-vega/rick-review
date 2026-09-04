"""Instrument check BEFORE any disagreement is believed.
Hand-computable values, compared against RICK's published numbers."""
import sys; sys.path.insert(0,'/home/clio/projects/reviews/code-2026-09-04')
import sympy as sp
from fp_lib import *

N = 10
F = FP_coeffs(N)
E1,E2,E3 = sp.symbols('E1 E2 E3')

def to_E(expr):
    """rewrite a symmetric poly in u1,u2,u3 into E1,E2,E3."""
    from sympy.polys.polyfuncs import symmetrize
    s, rem, _ = symmetrize(sp.expand(expr), us, formal=True, symbols=[E1,E2,E3])
    assert sp.simplify(rem) == 0, f"not symmetric: rem={rem}"
    return sp.expand(s)

print("--- instrument check 0: [T^1] F_P  (Rick Day161 §0: 1+E1+E2) ---")
print("  mine:", sp.factor(to_E(F[1])))

print("--- instrument check 1: hand value.  [T^1]F_P = Tplus(e2*V)/V ---")
# by hand: e2*V, apply Tplus, divide.  Do it a totally different way: evaluate numerically.
import itertools
def FP_numeric_T1(a,b,c):
    ex = sp.expand(e2sym*V)
    return sp.simplify(Tplus(ex).subs({u1:a,u2:b,u3:c})/V.subs({u1:a,u2:b,u3:c}))
for (a,b,c) in [(5,3,2),(7,2,-1),(4,-3,11)]:
    lhs = FP_numeric_T1(a,b,c)
    rhs = (1 + (a+b+c) + (a*b+a*c+b*c))
    print(f"  u={(a,b,c)}: Tplus(e2 V)/V = {lhs},  1+E1+E2 = {rhs},  match={lhs==rhs}")
