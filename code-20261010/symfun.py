"""Symmetric function helpers: e_mu, monomial extraction, e-basis expansion, kappa."""
from fractions import Fraction
from itertools import combinations
from star import *

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n-k, k):
            yield (k,) + rest

def e_poly(k, N):
    """elementary symmetric e_k in N vars"""
    out = {}
    for A in combinations(range(N), k):
        a = [0]*N
        for i in A: a[i] = 1
        out[tuple(a)] = c_const(1)
    return out

def e_mu(mu, N):
    P = p_one(N)
    for k in mu: P = p_mul(P, e_poly(k, N))
    return P

def mono_coeff(P, mu, N):
    """coefficient of x^mu (mu padded to length N) in P"""
    a = tuple(list(mu) + [0]*(N-len(mu)))
    return P.get(a, {})

def e_expand(P, n, N):
    """Expand symmetric P (homogeneous degree n) in the e-basis.
    Solve M c = p where rows indexed by partitions mu of n:
    M[mu][nu] = coeff of x^mu in e_nu ; p[mu] = coeff of x^mu in P."""
    parts = list(partitions(n))
    import sympy
    t = sympy.Symbol('t')
    def tosym(c): return sum(sympy.Rational(v.numerator, v.denominator)*t**e for e, v in c.items()) if c else sympy.Integer(0)
    M = sympy.zeros(len(parts), len(parts))
    rhs = sympy.zeros(len(parts), 1)
    enus = {nu: e_mu(nu, N) for nu in parts}
    for i, mu in enumerate(parts):
        for j, nu in enumerate(parts):
            M[i, j] = tosym(mono_coeff(enus[nu], mu, N))
        rhs[i] = tosym(mono_coeff(P, mu, N))
    sol = M.solve(rhs)
    return {parts[j]: sympy.simplify(sympy.cancel(sol[j])) for j in range(len(parts))}

# ---------- dominance and kappa ----------
def dominates(mu, lam):
    """mu >= lam in dominance (same size).  mu, lam sorted decreasing tuples."""
    if sum(mu) != sum(lam): return False
    a = b = 0
    for i in range(max(len(mu), len(lam))):
        a += mu[i] if i < len(mu) else 0
        b += lam[i] if i < len(lam) else 0
        if a < b: return False
    return True

def set_partitions(lst, r):
    """all set partitions of list positions into exactly r nonempty blocks"""
    n = len(lst)
    if r > n or r < 1: return
    def rec(i, blocks):
        if i == n:
            if len(blocks) == r: yield [tuple(b) for b in blocks]
            return
        for bi in range(len(blocks)):
            blocks[bi].append(lst[i])
            yield from rec(i+1, blocks)
            blocks[bi].pop()
        if len(blocks) < r:
            blocks.append([lst[i]])
            yield from rec(i+1, blocks)
            blocks.pop()
    yield from rec(0, [])

def kappa(lam, mu):
    """largest r with lam = lam^1 u..u lam^r, mu = mu^1 u..u mu^r (multisets of
    parts), blocks nonempty, mu^i >= lam^i in dominance.  -inf (here: 0) if
    mu does not dominate lam."""
    if not dominates(mu, lam): return 0
    best = 0
    for r in range(min(len(lam), len(mu)), 0, -1):
        for pl in set_partitions(list(lam), r):
            for pm in set_partitions(list(mu), r):
                # try to match blocks of pl to blocks of pm
                used = [False]*r
                def match(i):
                    if i == r: return True
                    lb = tuple(sorted(pl[i], reverse=True))
                    for j in range(r):
                        if used[j]: continue
                        mb = tuple(sorted(pm[j], reverse=True))
                        if sum(mb) == sum(lb) and dominates(mb, lb):
                            used[j] = True
                            if match(i+1): return True
                            used[j] = False
                    return False
                if match(0):
                    return r
    return best
