"""
Independent verification engine for 2026-09-08-Q99-two-parameter-exchange.tex.

DELIBERATELY DISJOINT CODE PATH from scratch/q99/engine.py:
  - that engine: power-sum dictionaries, h_n = sum_{lambda |- n} p_lambda/z_lambda,
    plethystic shift by explicit subset expansion over the parts of lambda.
  - this engine: h-basis dictionaries (partition = multiset of h-indices), and the
    plethystic shift derived from   -(1-u)/z = {u/z} - {1/z}   (a difference of two
    SINGLE LETTERS), using only  sigma[a w] = 1/(1-aw)  and  sigma[-a w] = 1-aw.
    No power sums, no z_lambda, no subset expansion, no appeal to Lemma 2.1.

Derivation used here (independent of the paper's Lemma 2.1 "contraction"):
  sigma[(X - (1-u)/z) w] = sigma[Xw] * (1 - w/z) / (1 - u w/z)
  => h_n[X - (1-u)/z] = h_n - sum_{j>=1} z^{-j} u^{j-1} (1-u) h_{n-j}.
"""
import sympy as sp
from itertools import product

# A symmetric function is a dict: tuple(sorted h-indices, descending) -> coeff.
# () is h_0 = 1.  h_n for n<0 is the zero element.

def sf_zero():
    return {}

def sf_one():
    return {(): sp.Integer(1)}

def h(n):
    if n < 0:
        return {}
    if n == 0:
        return sf_one()
    return {(n,): sp.Integer(1)}

def sf_add(a, b):
    out = dict(a)
    for k, v in b.items():
        out[k] = sp.expand(out.get(k, 0) + v)
        if out[k] == 0:
            del out[k]
    return out

def sf_scale(a, c):
    c = sp.expand(c)
    if c == 0:
        return {}
    return {k: sp.expand(v * c) for k, v in a.items()}

def sf_mul(a, b):
    out = {}
    for k1, v1 in a.items():
        for k2, v2 in b.items():
            k = tuple(sorted(k1 + k2, reverse=True))
            out[k] = sp.expand(out.get(k, 0) + v1 * v2)
    return {k: v for k, v in out.items() if v != 0}

def sf_eq(a, b):
    keys = set(a) | set(b)
    return all(sp.simplify(sp.expand(a.get(k, 0) - b.get(k, 0))) == 0 for k in keys)

def sf_is_zero(a):
    return all(sp.simplify(v) == 0 for v in a.values())

# ---- plethystic shift  f -> f[X - (1-u)/z] = sum_j c_j z^{-j} ----

def shift_h(n, u, dmax):
    """h_n[X-(1-u)/z] as {j: sym func} for j = 0..dmax."""
    out = {0: h(n)}
    for j in range(1, min(n, dmax) + 1):
        out[j] = sf_scale(h(n - j), -u**(j - 1) * (1 - u))
    return out

def series_mul(A, B, dmax):
    out = {}
    for j1, f1 in A.items():
        for j2, f2 in B.items():
            if j1 + j2 > dmax:
                continue
            out[j1 + j2] = sf_add(out.get(j1 + j2, {}), sf_mul(f1, f2))
    return out

def shift(f, u):
    """f[X - (1-u)/z] as {j: sym func}, j >= 0 the power of z^{-1}."""
    dmax = max((sum(k) for k in f), default=0)
    total = {}
    for lam, coeff in f.items():
        S = {0: sf_one()}
        for part in lam:
            S = series_mul(S, shift_h(part, u, dmax), dmax)
        S = {j: sf_scale(g, coeff) for j, g in S.items()}
        for j, g in S.items():
            total[j] = sf_add(total.get(j, {}), g)
    return {j: g for j, g in total.items() if g}

def mode(f, u, m):
    """H^u_m f = sum_j c_j(f) * h_{m+j}."""
    S = shift(f, u)
    out = {}
    for j, g in S.items():
        out = sf_add(out, sf_mul(g, h(m + j)))
    return out
