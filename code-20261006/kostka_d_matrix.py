"""
Independent check of Rick's Theorem H Corollary (2026-10-01 PDF, UID 749).

Corollary claims, for lambda, mu |- n:
    d_{lambda mu}(t) = t^{-n(lambda')} * sum_nu K_{nu' lambda} Ktilde_{nu mu'}(t)
with consequences:
    (a) d_{lambda mu} in N[t]
    (b) d_{lambda mu}(1) = M_{lambda mu'}  (# 0-1 matrices, row sums lambda, col sums mu')
    (c) d_{lambda mu}(0) = 1 for mu |>= lambda (dominance)

Pure Python (no Sage in this container). Kostka-Foulkes computed from the
COCHARGE statistic on semistandard tableaux, independently of any
symmetric-function library.
"""
from itertools import product
from functools import lru_cache
import sympy as sp

t = sp.symbols('t')

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0:
        yield ()
        return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - k, k):
            yield (k,) + rest

def conj(lam):
    if not lam: return ()
    return tuple(sum(1 for p in lam if p > i) for i in range(lam[0]))

def n_stat(lam):
    """n(lambda) = sum (i-1) lambda_i, 1-indexed."""
    return sum(i * p for i, p in enumerate(lam))

def dominates(mu, lam):
    """mu |>= lam in dominance order (both partitions of same n)."""
    sm = sl = 0
    for i in range(max(len(mu), len(lam))):
        sm += mu[i] if i < len(mu) else 0
        sl += lam[i] if i < len(lam) else 0
        if sm < sl: return False
    return True

# ---------- semistandard Young tableaux of shape lam, content alpha ----------
def ssyt(lam, alpha):
    """Generate SSYT of shape lam with content alpha as tuple of rows."""
    cells = [(i, j) for i, r in enumerate(lam) for j in range(r)]
    letters = []
    for v, m in enumerate(alpha, start=1):
        letters += [v] * m
    if len(letters) != len(cells): return
    rows = [[None] * r for r in lam]
    lam_c = conj(lam)

    def rec(idx, remaining):
        if idx == len(cells):
            yield tuple(tuple(r) for r in rows)
            return
        i, j = cells[idx]
        for v in sorted(remaining):
            if remaining[v] == 0: continue
            # weakly increasing along rows
            if j > 0 and rows[i][j - 1] > v: continue
            # strictly increasing down columns
            if i > 0 and rows[i - 1][j] >= v: continue
            rows[i][j] = v
            remaining[v] -= 1
            yield from rec(idx + 1, remaining)
            remaining[v] += 1
            rows[i][j] = None
    from collections import Counter
    yield from rec(0, Counter(letters))

def kostka(lam, alpha):
    return sum(1 for _ in ssyt(lam, alpha))

# ---------- charge / cocharge (Lascoux-Schutzenberger) ----------
def reading_word(T):
    """Row reading word, bottom row to top row, left to right."""
    w = []
    for row in reversed(T):
        w.extend(row)
    return w

def charge_word_standard(w):
    """Charge of a standard word (each letter once, 1..n)."""
    n = len(w)
    pos = {v: i for i, v in enumerate(w)}
    # index(1)=0; index(k)= index(k-1) + (1 if k is to the RIGHT of k-1 else 0)
    idx = {1: 0}
    for k in range(2, n + 1):
        idx[k] = idx[k - 1] + (1 if pos[k] > pos[k - 1] else 0)
    return sum(idx.values())

def decompose_standard(w):
    """Standard subwords of a (partition-content) word, LS procedure."""
    from collections import Counter
    w = list(w)
    subwords = []
    while w:
        cnt = Counter(w)
        maxv = max(cnt)
        # select one of each 1..maxv by the LS right-to-left rule
        chosen = []
        # pick a 1: rightmost 1 ... LS: read right to left, pick first 1,
        # then continue cyclically picking first 2 to the left of it, etc.
        nseq = max(v for v in cnt)
        # standard selection: scan right-to-left cyclically
        taken_idx = []
        cur = 1
        i = len(w) - 1
        start = None
        # find a 1 scanning right to left
        while i >= 0 and w[i] != 1:
            i -= 1
        taken_idx.append(i); cur = 2
        while cur <= nseq:
            j = i - 1
            found = -1
            while j >= 0:
                if w[j] == cur: found = j; break
                j -= 1
            if found == -1:
                # wrap around from the right end
                j = len(w) - 1
                while j > i:
                    if w[j] == cur: found = j; break
                    j -= 1
            taken_idx.append(found)
            i = found
            cur += 1
        taken_idx_sorted = sorted(taken_idx)
        sub = [w[k] for k in taken_idx_sorted]
        subwords.append(sub)
        for k in sorted(taken_idx, reverse=True):
            del w[k]
    return subwords

def charge(T):
    w = reading_word(T)
    tot = 0
    for sub in decompose_standard(w):
        tot += charge_word_standard(sub)
    return tot

def kostka_foulkes(lam, mu):
    """K_{lam mu}(t) = sum over SSYT(lam,mu) of t^charge."""
    e = sp.Integer(0)
    for T in ssyt(lam, mu):
        e += t ** charge(T)
    return sp.expand(e)

def kostka_foulkes_tilde(lam, mu):
    """Ktilde = t^{n(mu)} K(1/t)  (cocharge version)."""
    K = kostka_foulkes(lam, mu)
    return sp.expand(sp.simplify(t ** n_stat(mu) * K.subs(t, 1 / t)))

# ---------- 0-1 matrices with prescribed row/col sums ----------
def count_01_matrices(rows, cols):
    rows = list(rows); cols = list(cols)
    if sum(rows) != sum(cols): return 0
    ncol = len(cols)
    @lru_cache(maxsize=None)
    def rec(ri, colstate):
        if ri == len(rows):
            return 1 if all(c == 0 for c in colstate) else 0
        r = rows[ri]
        total = 0
        for subset in product([0, 1], repeat=ncol):
            if sum(subset) != r: continue
            new = tuple(colstate[j] - subset[j] for j in range(ncol))
            if any(v < 0 for v in new): continue
            total += rec(ri + 1, new)
        return total
    return rec(0, tuple(cols))
