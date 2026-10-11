"""e-basis expansion over Q[s,t], and the ground-truth 0-1 matrix count M_{nu mu}."""
from fractions import Fraction
from ring import *

def count01(rows, cols):
    """# of 0-1 matrices with row sums `rows`, column sums `cols` (Macdonald I (6.?) M_{nu mu})."""
    cols = list(cols)
    from functools import lru_cache
    def rec(i, cols):
        if i == len(rows):
            return 1 if all(c == 0 for c in cols) else 0
        r = rows[i]
        tot = 0
        idx = [j for j in range(len(cols)) if cols[j] > 0]
        for S in combinations(idx, r):
            nc = list(cols)
            for j in S: nc[j] -= 1
            tot += rec(i+1, tuple(nc))
        return tot
    return rec(0, tuple(cols))

def mat_inv_T(n):
    """returns function b_dict -> c_dict implementing c = (M^T)^{-1} b,
    M_{nu mu} = [x^mu] e_nu = count01(nu, mu)."""
    parts = list(partitions(n))
    N = len(parts)
    A = [[Fraction(count01(parts[j], parts[i])) for j in range(N)] for i in range(N)]  # A = M^T
    # augment with identity, Gauss-Jordan
    aug = [A[i] + [Fraction(1 if i == j else 0) for j in range(N)] for i in range(N)]
    for col in range(N):
        piv = next(r for r in range(col, N) if aug[r][col] != 0)
        aug[col], aug[piv] = aug[piv], aug[col]
        pv = aug[col][col]
        aug[col] = [v / pv for v in aug[col]]
        for r in range(N):
            if r != col and aug[r][col] != 0:
                f = aug[r][col]
                aug[r] = [a - f*b for a, b in zip(aug[r], aug[col])]
    Inv = [[aug[i][N+j] for j in range(N)] for i in range(N)]
    return parts, Inv

_cache = {}
def e_expand(F, n, m):
    """F a symmetric poly dict (deg n, m vars) -> {partition: Q[s,t] coeff}"""
    if n not in _cache: _cache[n] = mat_inv_T(n)
    parts, Inv = _cache[n]
    b = []
    for mu in parts:
        a = tuple(list(mu) + [0]*(m-len(mu)))
        b.append(F.get(a, {}))
    out = {}
    for i, nu in enumerate(parts):
        acc = {}
        for j in range(len(parts)):
            f = Inv[i][j]
            if f and b[j]:
                acc = cadd(acc, {k: v*f for k, v in b[j].items()})
        acc = {k: v for k, v in acc.items() if v}
        if acc: out[nu] = acc
    return out

def estar(lam, m, V=None):
    """e^star_lambda = E_{lam_1}...E_{lam_l}(1), as poly dict"""
    if V is None: V = vandermonde(m)
    F = pone(m)
    for k in lam:
        F = E_k(F, k, m, V)
    return F

def cstr(c):
    """pretty-print a Q[s,t] coefficient"""
    if not c: return "0"
    def term(k, v):
        (se, te) = k
        parts = []
        if v != 1 or (se == 0 and te == 0): parts.append(str(v))
        if se: parts.append("s" + (f"^{se}" if se > 1 else ""))
        if te: parts.append("t" + (f"^{te}" if te > 1 else ""))
        return "*".join(parts)
    return " + ".join(term(k, v) for k, v in sorted(c.items()))
