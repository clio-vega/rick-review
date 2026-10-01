"""Independent implementation of Rick's (0.1) and checks of DS / Theorem 2.
Written from the formula in 2026-10-01-DS-all-lengths.tex, NOT from scripts/day214/.
"""
import itertools, sympy as sp
from sympy import Rational, symbols, simplify, cancel, together, factor, Poly

s, t, u = symbols('s t u')

def xs(m): return symbols('x1:%d' % (m+1))

def E_k(k, F, X, sval=s, tval=t):
    """E_k F = sum_{|A|=k} prod_{i in A, j notin A} (x_i - t x_j)/(x_i - x_j) * prod_A x_a * F(x_a -> s x_a)"""
    m = len(X)
    tot = 0
    for A in itertools.combinations(range(m), k):
        Aset = set(A)
        ker = sp.Integer(1)
        for i in A:
            for j in range(m):
                if j in Aset: continue
                ker *= (X[i] - tval*X[j])/(X[i] - X[j])
        mon = sp.Integer(1)
        for a in A: mon *= X[a]
        sub = {X[a]: sval*X[a] for a in A}
        tot += ker*mon*F.subs(sub, simultaneous=True)
    return sp.cancel(sp.together(tot))

def e_poly(r, X):
    if r == 0: return sp.Integer(1)
    return sum(sp.prod(c) for c in itertools.combinations(X, r))

def e_lambda(lam, X):
    out = sp.Integer(1)
    for p in lam: out *= e_poly(p, X)
    return sp.expand(out)

def eqt(lam, X, sval=s, tval=t, order=None):
    """e_lambda^{(q,t)} = E_{lam_1} ... E_{lam_l} (1), applied right to left."""
    seq = list(lam) if order is None else list(order)
    F = sp.Integer(1)
    for k in reversed(seq):
        F = E_k(k, F, X, sval, tval)
        F = sp.expand(sp.cancel(F))
    return F

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for p in range(min(n, maxpart), 0, -1):
        for rest in partitions(n-p, p): yield (p,)+rest

def e_expand(P, n, m, X):
    """Expand symmetric homogeneous P of degree n in the e_nu basis (nu |- n). Uses
    linear solve against monomial coefficients."""
    parts = list(partitions(n))
    if any(len(p) > m for p in parts):
        parts = [p for p in parts if len(p) <= m]
    basis = [sp.expand(e_lambda(p, X)) for p in parts]
    # collect on monomials
    Pp = sp.Poly(sp.expand(P), *X)
    Bp = [sp.Poly(b, *X) for b in basis]
    mons = sorted(set(Pp.monoms()) | set(m0 for b in Bp for m0 in b.monoms()))
    coeffs = symbols('c1:%d' % (len(parts)+1))
    eqs = []
    for mo in mons:
        lhs = Pp.coeff_monomial(mo)
        rhs = sum(coeffs[i]*Bp[i].coeff_monomial(mo) for i in range(len(parts)))
        eqs.append(sp.Eq(lhs, rhs))
    sol = sp.solve(eqs, coeffs, dict=True)
    assert sol, "e-expansion failed (not symmetric or wrong degree?)"
    sol = sol[0]
    return {parts[i]: sp.simplify(sol.get(coeffs[i], 0)) for i in range(len(parts))}

def dom_geq(mu, lam):
    """mu dominates lam (mu >= lam), same size."""
    assert sum(mu) == sum(lam)
    a = b = 0
    for i in range(max(len(mu), len(lam))):
        a += mu[i] if i < len(mu) else 0
        b += lam[i] if i < len(lam) else 0
        if a < b: return False
    return True

def n_stat(lam): return sum(i*p for i, p in enumerate(lam))

def conj(lam):
    if not lam: return ()
    return tuple(sum(1 for p in lam if p > c) for c in range(lam[0]))
