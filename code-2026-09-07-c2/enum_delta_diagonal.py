"""Clio, 2026-09-07 c2 — INDEPENDENT run of Rick's Day 174 §1 contribution rule.

Target: grandpa-rick/rick-research@7e66dca, for-collaborator/day174/...tex, §1.

I do NOT use Rick's 13-term list.  I re-derive the enumeration from
  (i) the closed forms for P_1,P_2,P_3   [proofs/scripts/day169/step15_L_closed_form.py:41-45]
  (ii) the contribution rule              [Day 174 PDF §1]
and then compare.

Calibration first: the SAME enumerator is run at delta=0 and delta=1, where the
answer is independently known (delta=0 must give the top-diagonal quadratic
R3 H^2 + R2 H + R1 = 0).  Only then delta=2.
"""
import sympy as sp

T, s, p = sp.symbols('T s p')
z = sp.symbols('z')                      # layer-grading bookkeeping variable

# ---------------------------------------------------------------- P_i, from step15
q2_x = (1 - s*T)**2 - 4*p*T**2
D = lambda k: -q2_x + T**2 + k*T
P = {3: T**2 * D(6),
     2: ((s+3)*T - 1) * D(8),
     1: (1 + s + p) * D(10) + 2}

def cells(expr):
    """{(w,d): coeff} with w = d_s + 2 d_p the u-weight, d the T-degree."""
    out = {}
    for (ds, dp, dT), c in sp.Poly(sp.expand(expr), s, p, T).terms():
        w = ds + 2*dp
        out[(w, dT)] = out.get((w, dT), sp.S(0)) + c * s**ds * p**dp
    return {k: sp.expand(v) for k, v in out.items() if sp.expand(v) != 0}

CELLS = {i: cells(P[i]) for i in (1, 2, 3)}

# ---------------------------------------------------------------- Riccati monomials
Hf, Kf, Lf, Mf = (sp.Function(n)(T) for n in ('H', 'K', 'L', 'M'))
G = Hf + z*Kf + z**2*Lf + z**3*Mf        # layer expansion, z^e = layer e
dG = sp.diff(G, T)

# (label, expression, top_X, Riccati multiplicity, parent P_i)
MONOMIALS = [
    ("G''",  sp.diff(G, T, 2), 4, 1, 3),
    ("GG'",  G*dG,             5, 3, 3),
    ("G^3",  G**3,             6, 1, 3),
    ("G'",   dG,               3, 1, 2),
    ("G^2",  G**2,             4, 1, 2),
    ("G",    G,                2, 1, 1),
]

def layer(expr, e):
    return sp.expand(sp.expand(expr).coeff(z, e))

def enumerate_delta(delta, cell_table=CELLS, emax=8):
    """All (i,w,d,X,e) firing at the given delta.  delta = 4 + d + e - w - top_X."""
    hits, total = [], sp.S(0)
    for label, X, topX, mult, i in MONOMIALS:
        for (w, d), c in sorted(cell_table[i].items()):
            e = w - d + topX + delta - 4
            if e < 0 or e > emax:
                continue
            Xe = layer(X, e)
            if Xe == 0:
                continue
            contrib = sp.expand(mult * c * T**d * Xe)
            hits.append(dict(i=i, w=w, d=d, coef=c, X=label, e=e, mult=mult, term=contrib))
            total += contrib
    return hits, sp.expand(total)


if __name__ == "__main__":
    print("=" * 78)
    print("CELL TABLES derived from step15 closed forms (w = u-weight, d = T-degree)")
    for i in (3, 2, 1):
        print(f"  P_{i}: " + ", ".join(f"({w},{d})={c}" for (w, d), c in sorted(CELLS[i].items())))
    for delta in (0, 1, 2):
        hits, total = enumerate_delta(delta)
        print(f"\ndelta={delta}: {len(hits)} tuples, max e = {max(h['e'] for h in hits)}")
        for h in hits:
            print(f"   P_{h['i']}^[{h['w']}][T^{h['d']}]={str(h['coef']):>14} x {h['mult']}*{h['X']:5s} e={h['e']}")
