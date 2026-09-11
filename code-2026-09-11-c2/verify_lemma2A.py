"""(B) Lemma 2-A: rho( AR_k(m) mod E_{>=4} ) <= rho(m) + 1 - k.
Definitions taken verbatim from §1 of Rick's 2026-09-08-day180-lemma-2A-proved.md.
Records ACTUAL rho as well as the bound, so that a degenerate (always-zero) test
cannot masquerade as confirmation."""
import itertools
import sympy as sp
from sympy.polys.polyfuncs import symmetrize

def Delta(u, i, j, l):
    return (u[i] + u[j] - 2*u[l] + 1) / ((u[i] - u[l]) * (u[j] - u[l]))

def AR_k(u, n, m_expr, k):
    """m_expr: a callable taking the tuple of u-variables -> expression."""
    tot = sp.Integer(0)
    for i, j in itertools.combinations(range(n), 2):
        shifted = list(u)
        shifted[i] = u[i] + 1
        shifted[j] = u[j] + 1
        m_ij = m_expr(shifted)
        rest = [l for l in range(n) if l not in (i, j)]
        inner = sp.Integer(0)
        for L in itertools.combinations(rest, k):
            prod = sp.Integer(1)
            for l in L:
                prod *= Delta(u, i, j, l)
            inner += prod
        tot += (u[i] + u[j] + 1) * m_ij * inner
    return sp.cancel(sp.together(tot))

def rho_mod_E4(expr, u):
    expr = sp.expand(expr)
    if expr == 0:
        return -sp.oo, True
    sym_part, remainder, defs = symmetrize(expr, u, formal=True)
    if sp.simplify(remainder) != 0:
        return None, False          # not symmetric
    s = [d[0] for d in defs]
    reduced = sp.expand(sym_part.subs({s[r]: 0 for r in range(3, len(s))}))
    if reduced == 0:
        return -sp.oo, True
    p = sp.Poly(reduced, *s[:3])
    return max(b1 + b2 + 2*b3 for (b1, b2, b3) in p.monoms()), True

def E(u, r):
    return sp.expand(sp.polys.specialpolys.symmetric_poly(r, u))

# monomials m = E1^a1 E2^a2 E3^a3 ; rho(m) = a1 + a2 + 2 a3
MONOMS = [(0,0,0), (1,0,0), (0,1,0), (2,0,0), (1,1,0), (0,0,1),
          (0,2,0), (3,0,0), (1,0,1), (2,1,0)]

print("="*84)
print("(B) LEMMA 2-A:  rho( AR_k(m) mod E_{>=4} )  <=  rho(m) + 1 - k")
print("="*84)
print(f"{'n':>2} {'m = E1^a1 E2^a2 E3^a3':22} {'rho(m)':>6} {'k':>2} {'bound':>6} {'actual':>7}  {'status':10}")
print("-"*84)
fails, tight, total = 0, 0, 0
for n in (3, 4, 5):
    u = sp.symbols(f'u1:{n+1}')
    for (a1, a2, a3) in MONOMS:
        if a3 > 0 and n < 3:
            continue
        rho_m = a1 + a2 + 2*a3
        m_expr = lambda uu, a1=a1, a2=a2, a3=a3: (E(uu,1)**a1) * (E(uu,2)**a2) * (E(uu,3)**a3)
        for k in range(0, n - 1):
            val = AR_k(u, n, m_expr, k)
            if not val.is_polynomial(*u):
                print(f"{n:>2} E1^{a1}E2^{a2}E3^{a3}{'':13} {rho_m:>6} {k:>2} *** AR_k NOT POLYNOMIAL ***")
                fails += 1; total += 1; continue
            actual, is_sym = rho_mod_E4(val, u)
            total += 1
            if not is_sym:
                print(f"{n:>2} E1^{a1}E2^{a2}E3^{a3}{'':13} {rho_m:>6} {k:>2} *** NOT SYMMETRIC ***")
                fails += 1; continue
            bound = rho_m + 1 - k
            ok = (actual == -sp.oo) or (actual <= bound)
            if actual == bound: tight += 1
            if not ok: fails += 1
            print(f"{n:>2} E1^{a1}E2^{a2}E3^{a3}{'':13} {rho_m:>6} {k:>2} {bound:>6} {str(actual):>7}  "
                  f"{'PASS' if ok else '*** FAIL ***':10}{' <-- TIGHT' if actual==bound else ''}")
print("-"*84)
print(f"{total} cases, {fails} failures, {tight} saturate the bound exactly.")
print("A bound that is NEVER saturated would be evidence of a degenerate test;")
print(f"here it is attained in {tight}/{total} cases, so the test has live variation.")
