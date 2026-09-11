"""
Independent verification of Rick's Day 180 artifact
  proofs/2026-09-08-day180-lemma-2A-proved.md
  (rick-research @ 86d0012)

Checks, from the DEFINITIONS in that file (not from his scripts, which are 404):
  (A) MVL: Pi_P^{(S)} is a polynomial (no poles at u_a=u_b), symmetric,
      of total degree <= d - (|S| - 3).
  (B) Lemma 2-A: rho( AR_k(m) mod E_{>=4} ) <= rho(m) + 1 - k.

Conventions (verbatim from §1 of the artifact):
  Delta_ij(l) = (u_i + u_j - 2 u_l + 1) / ((u_i - u_l)(u_j - u_l))
  m|_ij       = m(u + e_i + e_j)            [shift u_i, u_j by 1]
  AR_k(m)     = sum_{i<j} (u_i+u_j+1) m|_ij sum_{|L|=k, L subset [n]\{i,j}} prod_{l in L} Delta_ij(l)
  rho(E_r)    = ceil(r/2), extended multiplicatively
"""
import itertools, sys
import sympy as sp
from sympy.polys.polyfuncs import symmetrize

def setup(n):
    u = sp.symbols(f'u1:{n+1}')
    E = [sp.Integer(1)] + [sp.expand(sp.polys.specialpolys.symmetric_poly(r, u)) for r in range(1, n+1)]
    return u, E

def Delta(u, i, j, l):
    return (u[i] + u[j] - 2*u[l] + 1) / ((u[i] - u[l]) * (u[j] - u[l]))

def Pi_P(u, S, P):
    """Pi_P^{(S)} = sum_{{i,j} in S} (u_i+u_j+1) P(u_i,u_j) prod_{l in S\{i,j}} Delta_ij(l)"""
    tot = sp.Integer(0)
    for i, j in itertools.combinations(S, 2):
        term = (u[i] + u[j] + 1) * P(u[i], u[j])
        for l in S:
            if l not in (i, j):
                term *= Delta(u, i, j, l)
        tot += term
    return sp.cancel(sp.together(tot))

def rho_of_sym(expr, u, n):
    """expr: symmetric polynomial in u. Return rho( expr mod E_{>=4} ), or -oo if 0."""
    poly, sym_rem = symmetrize(sp.expand(expr), u, formal=True)[:2] if False else (None, None)
    res = symmetrize(sp.expand(expr), u, formal=True)
    # symmetrize -> (sym_part_in_s, remainder, [(s1,e1),(s2,e2),...])
    sym_part, remainder, defs = res
    assert sp.simplify(remainder) == 0, f"NOT SYMMETRIC: remainder {remainder}"
    s = [d[0] for d in defs]          # s[0]=s1 ... s[n-1]=sn
    # reduce mod E_{>=4}: set s4..sn -> 0
    reduced = sp.expand(sym_part.subs({s[r]: 0 for r in range(3, len(s))}))
    if reduced == 0:
        return -sp.oo
    p = sp.Poly(reduced, *s[:3])
    return max(b1 + b2 + 2*b3 for (b1, b2, b3) in p.monoms())

def rho_monom(a1, a2, a3):
    return a1 + a2 + 2*a3

# ---------------- (A) MVL ----------------
print("="*72)
print("(A) MASTER VANISHING LEMMA:  deg Pi_P^{(S)} <= d - (|S| - 3),  Pi polynomial")
print("="*72)
Ps = [("1",               lambda x, y: sp.Integer(1),       0),
      ("u_i+u_j",         lambda x, y: x + y,               1),
      ("u_i u_j",         lambda x, y: x*y,                 2),
      ("u_i^2+u_j^2",     lambda x, y: x**2 + y**2,         2),
      ("(u_i+u_j)^3",     lambda x, y: (x+y)**3,            3),
      ("u_iu_j(u_i+u_j)", lambda x, y: x*y*(x+y),           3),
      ("u_i^2u_j^2",      lambda x, y: x**2*y**2,           4)]
fails = 0
for N in (2, 3, 4, 5, 6):
    u, _ = setup(N)
    S = list(range(N))
    for name, P, d in Ps:
        val = Pi_P(u, S, P)
        is_poly = val.is_polynomial(*u)
        if not is_poly:
            print(f"  |S|={N} P={name:16s} *** NOT A POLYNOMIAL ***"); fails += 1; continue
        val = sp.expand(val)
        actual = -sp.oo if val == 0 else sp.Poly(val, *u).total_degree()
        bound = d - (N - 3)
        ok = (val == 0) or (actual <= bound)
        # symmetry check
        swap = {u[0]: u[1], u[1]: u[0]}
        symm = sp.expand(val.subs(swap, simultaneous=True) - val) == 0
        tight = (actual == bound) if val != 0 else (bound < 0)
        print(f"  |S|={N} P={name:16s} d={d} bound={bound:>3} actual={str(actual):>5} "
              f"sym={'Y' if symm else 'N'} {'PASS' if ok and symm else '*** FAIL ***'}"
              f"{'  [saturates]' if tight else ''}")
        if not (ok and symm): fails += 1
print(f"\nMVL: {'ALL PASS' if fails==0 else f'{fails} FAILURES'}")
