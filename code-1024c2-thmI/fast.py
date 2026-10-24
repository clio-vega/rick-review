"""O(1) p=1 KLG count (my 10-23 closed form, validated against brute force), applied to
the CORRECT shape R(theta).  Replaces the 2^|theta| enumeration so m=7,8 are reachable.
Clio 2026-10-24 c2 peer review of Rick's Theorem I."""
from collections import Counter

def D(kappa, m):
    """shifted diagram: row i (0-indexed) occupies columns i .. i+kappa_{i+1}-1"""
    return frozenset((i, i + j) for i, k in enumerate(kappa) for j in range(k))

def R(rc, m):
    r, c = rc
    return (m - 1 - c, m - 1 - r)

def strict_partitions(m):
    from itertools import combinations
    out = []
    for k in range(m + 1):
        for s in combinations(range(m, 0, -1), k):
            out.append(tuple(s))
    return out

def contains(kappa, rho):
    if len(rho) > len(kappa): return False
    return all(rho[i] <= kappa[i] for i in range(len(rho)))

def forced_count(theta):
    """#KLG-tableaux of shape theta, content {1}, labels {1'<1} encoded 0=1', 1=1.
    A row or column of 2 is forced to (1',1); a diagonal box is forced unprimed (cond v);
    every unconstrained box is free.  Returns 2^f if consistent, else 0."""
    rows, cols = {}, {}
    for b in theta:
        rows.setdefault(b[0], []).append(b)
        cols.setdefault(b[1], []).append(b)
    val = {}
    def put(b, v):
        if b in val and val[b] != v: return False
        val[b] = v; return True
    for bs in list(rows.values()) + list(cols.values()):
        if len(bs) > 2: return 0
        if len(bs) == 2:
            bs.sort()
            if not put(bs[0], 0) or not put(bs[1], 1): return 0
    for b in theta:
        if b[0] == b[1] and not put(b, 1): return 0
    return 2 ** (len(theta) - len(val))

def Rset(theta, m):
    return frozenset(R(b, m) for b in theta)

def is_rim(theta):
    return all(not (b[0] > a[0] and b[1] > a[1]) for a in theta for b in theta)

def rook_strip(theta):
    rows = Counter(b[0] for b in theta); cols = Counter(b[1] for b in theta)
    return max(list(rows.values()) + [0]) <= 1 and max(list(cols.values()) + [0]) <= 1

def N_LG(theta, m):
    """Rick's N(theta) = KLG count of shape R(theta).  The R is NOT optional: the count
    is not R-invariant (rinv.py: 528/3024 pairs disagree)."""
    return forced_count(Rset(theta, m))

def r_of(kappa):
    """Lemma 0"""
    return max((k + 2 * (i + 1) - 2 for i, k in enumerate(kappa)), default=0)

def W_LG(k): return -(-r_of(k) // 2)
def W_OG(k): return r_of(k)

def rho_of_ideal(rest, m):
    """the strict partition whose shifted diagram is the order ideal `rest`.
    D(kappa,m) puts kappa_{i+1} boxes in row i (columns i..i+kappa_{i+1}-1), so the part
    for row i is the box COUNT of that row -- no offset.  (An earlier version added +i
    and manufactured 2963 spurious Lemma A failures while Lemma 0 and Ch' stayed clean;
    that asymmetry is what exposed it.)"""
    parts = [len([c for c in rest if c[0] == i]) for i in range(m)]
    return tuple(p for p in parts if p > 0)

def c_LG(kappa, rho, m, Dk=None):
    th = (Dk if Dk is not None else D(kappa, m)) - D(rho, m)
    if not th or not is_rim(th): return 0
    return (-1) ** (len(th) - 1) * N_LG(th, m)

def c_OG(kappa, rho, m, Dk=None):
    th = (Dk if Dk is not None else D(kappa, m)) - D(rho, m)
    if not th or not rook_strip(th): return 0
    return (-1) ** (len(th) - 1)
