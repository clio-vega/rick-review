"""
Independent implementation of the affine-Hecke side, from the PRINTED conventions of
Rick's Day 207b s.0 (work-in-progress 1e92c63) -- nothing imported from scripts/day2*.

  T_i F = t s_i F + (t-1) X_{i+1} (s_i F - F)/(X_i - X_{i+1})
  pi F  = X_1 F(X_2,...,X_m, s X_1)
  Y_i   = t^{m-i} T_{i-1}...T_1 pi T_{m-1}^{-1}...T_i^{-1}
  e_k(Y) = sum_{b_1<...<b_k} Y_{b_1}...Y_{b_k}, Y_{b_k} acting FIRST
  a_ij  = (X_i - t X_j)/(X_i - X_j),  E(z) = prod(1 + X_i z)
"""
import sympy as sp
from itertools import combinations
from functools import lru_cache

s, t, z, w, x, y = sp.symbols('s t z w x y')


def Xs(m):
    return list(sp.symbols('X1:%d' % (m + 1)))


def swap(F, X, i):
    """s_i F, 1-indexed i (swap X_i, X_{i+1})."""
    a, b = X[i - 1], X[i]
    return F.subs({a: b, b: a}, simultaneous=True)


def T(F, X, i):
    m = len(X)
    assert 1 <= i <= m - 1
    sF = swap(F, X, i)
    return sp.cancel(sp.together(t * sF + (t - 1) * X[i] * (sF - F) / (X[i - 1] - X[i])))


def Tinv(F, X, i):
    """T^{-1} = (T - (t-1))/t, from (T-t)(T+1)=0."""
    return sp.cancel(sp.together((T(F, X, i) - (t - 1) * F) / t))


def pi(F, X):
    m = len(X)
    sub = {X[j]: X[j + 1] for j in range(m - 1)}
    sub[X[m - 1]] = s * X[0]
    return sp.cancel(sp.together(X[0] * F.subs(sub, simultaneous=True)))


def Y(F, X, i):
    m = len(X)
    G = F
    for j in range(i, m):            # T_i^{-1} first, up to T_{m-1}^{-1}
        G = Tinv(G, X, j)
    G = pi(G, X)
    for j in range(1, i):            # T_1 first, up to T_{i-1}
        G = T(G, X, j)
    return sp.cancel(sp.together(t ** (m - i) * G))


def ek_Y(F, X, k):
    """e_k(Y) F, with Y_{b_k} acting first."""
    m = len(X)
    if k == 0:
        return F
    tot = sp.Integer(0)
    for B in combinations(range(1, m + 1), k):
        G = F
        for b in reversed(B):        # Y_{b_k} first
            G = Y(G, X, b)
        tot += G
    return sp.cancel(sp.together(tot))


def e(X, r):
    m = len(X)
    if r < 0 or r > m:
        return sp.Integer(0)
    return sp.Add(*[sp.Mul(*c) for c in combinations(X, r)]) if r > 0 else sp.Integer(1)


def E(X, arg):
    return sp.prod([1 + Xi * arg for Xi in X])


# ---------------------------------------------------------------- Day 209 closed form
def tpoch(a, n):
    """(a;t)_n = prod_{i<n}(1 - a t^i)."""
    return sp.prod([1 - a * t ** i for i in range(n)]) if n > 0 else sp.Integer(1)


@lru_cache(maxsize=None)
def alpha(j):
    if j < 0:
        return sp.Integer(0)                       # 207b: alpha_{-1} := 0
    return sp.prod([(s - t ** i) for i in range(1, j + 1)]) / tpoch(t, j)


@lru_cache(maxsize=None)
def cnj(n, j):
    """c(n,j), 0 <= j <= n, else 0  (207b s.0)."""
    if j < 0 or n < 0 or j > n:
        return sp.Integer(0)
    return tpoch(s, n - j) / tpoch(t, n - j) * (alpha(j) - s * t ** (n - j) * alpha(j - 1))


def Nnj(n, j):
    return t ** (-n * j) * cnj(n, j)


def K_ij(i, j):
    p1 = sp.prod([(t ** p * z - s * w) / (t ** p * z - t ** j * w) for p in range(i)])
    p2 = sp.prod([(s * z - t ** r * w) / (t ** i * z - t ** r * w) for r in range(j)])
    return p1 * p2


def V(n, i, j):
    if i < 0 or j < 0 or n < 0:
        return sp.Integer(0)
    tot = sp.Integer(0)
    for n1 in range(0, n + 1):
        n2 = n - n1
        if n1 < i or n2 < j:
            continue                               # c(n,j)=0 for n<j makes this automatic
        tot += (s ** ((n1 - i) + (n2 - j)) * t ** (-(n1 - i) * j - (n2 - j) * i)
                * Nnj(n1, i) * Nnj(n2, j) * z ** (-n1) * w ** (-n2))
    return K_ij(i, j) * tot


def T_closed(X, k):
    """T_k = sum_{b,i,j} s^{2b} t^{-b(i+j)} V^{(k-b)}_{ij} e_b E(t^i z) E(t^j w)."""
    tot = sp.Integer(0)
    for b in range(0, k + 1):
        n = k - b
        for i in range(0, n + 1):
            for j in range(0, n - i + 1):
                v = V(n, i, j)
                if v == 0:
                    continue
                tot += (s ** (2 * b) * t ** (-b * (i + j)) * v
                        * e(X, b) * E(X, t ** i * z) * E(X, t ** j * w))
    return tot


def Gamma(X, k):
    """Gamma_k = sum_{a,b} z^a w^b t^{-C(k,2)} e_k(Y) . (e_a e_b)."""
    m = len(X)
    tot = sp.Integer(0)
    for a in range(0, m + 1):
        for b in range(0, m + 1):
            F = sp.expand(e(X, a) * e(X, b))
            if F == 0:
                continue
            tot += z ** a * w ** b * ek_Y(F, X, k)
    return sp.cancel(sp.together(t ** (-sp.binomial(k, 2)) * tot))
