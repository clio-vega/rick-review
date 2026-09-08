"""
Independent audit of 2026-09-07-c2-Q96 Thm 4.1(2) (the two-parameter commutator).

Engine here: border strips enumerated DIRECTLY on Young diagrams (containment,
size, connectivity, no-2x2), height = (#rows occupied) - 1.  No abacus is used to
compute R_g(t); the Maya set is used only to EVALUATE the theorem's formula, which
is what is under test.
"""
import sympy as sp
from itertools import product
t, s = sp.symbols('t s')

def parts(n):
    if n == 0:
        yield ()
        return
    def rec(rem, mx):
        if rem == 0:
            yield ()
            return
        for k in range(min(rem, mx), 0, -1):
            for tail in rec(rem - k, k):
                yield (k,) + tail
    yield from rec(n, n)

def cells(lam):
    return {(i, j) for i, r in enumerate(lam) for j in range(r)}

def is_partition(mu):
    return all(mu[i] >= mu[i+1] for i in range(len(mu)-1)) and all(x > 0 for x in mu)

def border_strips(lam, g):
    """all (mu, height) with mu/lam a connected border strip of size g."""
    out = []
    L = len(lam) + g
    base = list(lam) + [0]*(L - len(lam))
    # candidate mu: increase some rows; mu_i <= mu_{i-1}
    def rec(i, prev, rem, acc):
        if i == L:
            if rem == 0:
                yield tuple(acc)
            return
        lo = base[i]
        hi = min(prev, base[i] + rem)
        for v in range(lo, hi + 1):
            yield from rec(i+1, v, rem - (v - lo), acc + [v])
    for mu in rec(0, 10**6, g, []):
        mu = tuple(x for x in mu if x > 0)
        if not is_partition(mu):
            continue
        sk = cells(mu) - cells(lam)
        if len(sk) != g:
            continue
        # no 2x2
        if any((i,j) in sk and (i+1,j) in sk and (i,j+1) in sk and (i+1,j+1) in sk for (i,j) in sk):
            continue
        # connected (edge-adjacency)
        stack = [next(iter(sk))]; seen = {stack[0]}
        while stack:
            (i,j) = stack.pop()
            for (a,b) in ((i+1,j),(i-1,j),(i,j+1),(i,j-1)):
                if (a,b) in sk and (a,b) not in seen:
                    seen.add((a,b)); stack.append((a,b))
        if len(seen) != g:
            continue
        rows = len({i for (i,j) in sk})
        out.append((mu, rows - 1))
    return out

def R(lam, g, u):
    """R_g(u) s_lam as dict mu -> coeff."""
    d = {}
    for mu, ht in border_strips(lam, g):
        d[mu] = sp.expand(d.get(mu, 0) + u**ht)
    return d

def apply_R(vec, g, u):
    out = {}
    for lam, c in vec.items():
        for mu, cc in R(lam, g, u).items():
            out[mu] = sp.expand(out.get(mu, 0) + c*cc)
    return {k: v for k, v in out.items() if sp.expand(v) != 0}

def comm(lam, e, f):
    """<mu| [R_e(t), R_f(s)] |lam> as dict mu -> coeff."""
    a = apply_R(apply_R({lam: sp.Integer(1)}, f, s), e, t)
    b = apply_R(apply_R({lam: sp.Integer(1)}, e, t), f, s)
    out = dict(a)
    for k, v in b.items():
        out[k] = sp.expand(out.get(k, 0) - v)
    return {k: sp.expand(v) for k, v in out.items() if sp.expand(v) != 0}

# ---- Maya sets, used only to evaluate the theorem's formula ----
def maya(lam, L):
    lam = list(lam) + [0]*(L - len(lam))
    return {lam[j] - (j+1) for j in range(L)}

def cnt(M, a, b):  # open interval
    return sum(1 for x in M if a < x < b)

def formula(lam, mu, e, f, L):
    M, Mp = maya(lam, L), maya(mu, L)
    diff = (M ^ Mp)
    if len(diff) == 2:
        (a,) = M - Mp
        (a2,) = Mp - M
        assert a2 - a == e + f, (a, a2, e, f)
        N = cnt(M, a, a+e+f); A = cnt(M, a, a+f); B = cnt(M, a, a+e)
        m_e = 1 if (a+e) in M else 0
        m_f = 1 if (a+f) in M else 0
        return sp.expand(s**A * t**(N-1-A) * (t - m_f*(1+t)) - t**B * s**(N-1-B) * (s - m_e*(1+s)))
    if len(diff) == 4:
        gone = sorted(M - Mp); came = set(Mp - M)
        tot = 0
        for (b, c) in [(gone[0], gone[1]), (gone[1], gone[0])]:
            if (b+e) not in came or (c+f) not in came:
                continue
            if len({b, c, b+e, c+f}) != 4:
                continue
            P = cnt(M, b, b+e); Q = cnt(M, c, c+f)
            k = (1 if b+e > c and b+e < c+f else 0) - (1 if b > c and b < c+f else 0)
            tot += t**(P-k) * s**Q * (1 - (t*s)**k)
        return sp.expand(sp.together(tot))
    return sp.Integer(0)
