"""Instrument check on the DISAGREE from e2clean.py.

The restatement c_n = C(n-1,2) - C(2,2) is a *relative* shift from the n=3 base,
NOT the absolute constant of the n-variable product.  e2clean.py plugged the
relative shift into the absolute product -- my error, not the claim's.

Correct test of the actual claim:
    tops^(n)[b], E_3-free  ==  tops^(3)[b] with E_2 -> E_2 + c_n E_1,  c_n = C(n-1,2)-C(2,2)
and, equivalently, the absolute product starts at C(n-1,2).
"""
import sympy as sp
E1, E2 = sp.symbols('E1 E2')

# values COMPUTED from the definition of Psi^+ by e2clean.py (untouched):
computed = {(6, 1): 10*E1 + E2,
            (5, 3): sp.expand((6*E1 + E2)*(7*E1 + E2)*(8*E1 + E2))}

def base3(b):                      # tops^(3)[b]: absolute constant is C(2,2)=1
    return sp.expand(sp.prod([E2 + (sp.binomial(2, 2) + r)*E1 for r in range(b)]))

for (n, b), val in computed.items():
    c_n = sp.binomial(n-1, 2) - sp.binomial(2, 2)          # my restatement, Rick adopted it
    via_shift = sp.expand(base3(b).subs(E2, E2 + c_n*E1))
    absolute  = sp.expand(sp.prod([E2 + (sp.binomial(n-1, 2) + r)*E1 for r in range(b)]))
    print(f"(n,b)=({n},{b})  c_n = C({n-1},2)-C(2,2) = {int(c_n)}")
    print(f"   computed from Psi^+      : {sp.factor(val)}")
    print(f"   n=3 base shifted by c_n  : {sp.factor(via_shift)}   -> {'AGREE' if sp.expand(val-via_shift)==0 else '*** DISAGREE ***'}")
    print(f"   absolute, start C(n-1,2)={int(sp.binomial(n-1,2))}: {sp.factor(absolute)}   -> {'AGREE' if sp.expand(val-absolute)==0 else '*** DISAGREE ***'}\n")
