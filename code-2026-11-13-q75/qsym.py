"""Independent QSym/NSym engine for reviewing Rick's Q75 (2026-11-13, Clio).

Mechanism: fundamental quasisymmetric products by SHUFFLES of permutations,
F_alpha dual to R_alpha. Nothing here uses Rick's Key Identity, generating
functions, or S-basis engine.

Encoding: a composition of d is encoded by its descent set as a bitmask on
positions 1..d-1 (bit p-1 <-> descent at p).  The binary string s of length
L=d-1 in Rick's convention: s[p-1]=='1' iff descent at p.
"""
from fractions import Fraction
from itertools import combinations
from functools import lru_cache

def comp_to_mask(alpha):
    m, p = 0, 0
    for a in alpha[:-1]:
        p += a
        m |= 1 << (p - 1)
    return m

def mask_to_comp(mask, d):
    parts, last = [], 0
    for p in range(1, d):
        if mask >> (p - 1) & 1:
            parts.append(p - last); last = p
    parts.append(d - last)
    return tuple(parts)

def str_to_mask(s):
    return sum(1 << p for p, c in enumerate(s) if c == '1')

def rep_perm(mask, n, offset=0):
    """A permutation of offset+1..offset+n with descent set exactly `mask`:
    increasing runs, each later run taking SMALLER values."""
    comp = mask_to_comp(mask, n) if n > 0 else ()
    vals, out, hi = [], [], offset + n
    for a in comp:
        out.append(list(range(hi - a + 1, hi + 1))); hi -= a
    return [v for run in out for v in run]

def desc_mask(w):
    m = 0
    for p in range(len(w) - 1):
        if w[p] > w[p + 1]:
            m |= 1 << p
    return m

@lru_cache(maxsize=None)
def F_product(ma, i, mb, j):
    """F_alpha * F_beta as dict mask->coeff (degree i+j). i,j>=1."""
    sig = rep_perm(ma, i, 0)
    tau = rep_perm(mb, j, i)
    d = i + j
    out = {}
    for pos in combinations(range(d), i):
        w = [0] * d
        ps = set(pos)
        a = b = 0
        for t in range(d):
            if t in ps:
                w[t] = sig[a]; a += 1
            else:
                w[t] = tau[b]; b += 1
        m = desc_mask(w)
        out[m] = out.get(m, 0) + 1
    return out

def rank(rows):
    """Exact rank over Q of a list of lists."""
    M = [[Fraction(x) for x in r] for r in rows if any(r)]
    if not M: return 0
    ncol = len(M[0]); r = 0
    for c in range(ncol):
        piv = next((k for k in range(r, len(M)) if M[k][c] != 0), None)
        if piv is None: continue
        M[r], M[piv] = M[piv], M[r]
        for k in range(len(M)):
            if k != r and M[k][c] != 0:
                f = M[k][c] / M[r][c]
                M[k] = [x - f * y for x, y in zip(M[k], M[r])]
        r += 1
        if r == len(M): break
    return r

def pairing_matrix(smask, d, i):
    """B_s on F-bases: rows F_alpha (|alpha|=i), cols F_beta (|beta|=d-i),
    entry = [F_s](F_alpha F_beta)."""
    if i == 0 or i == d:
        return [[1]]
    j = d - i
    return [[F_product(ma, i, mb, j).get(smask, 0) for mb in range(1 << (j - 1))]
            for ma in range(1 << (i - 1))]

def r_vector(s):
    d = len(s) + 1
    sm = str_to_mask(s)
    return [rank(pairing_matrix(sm, d, i)) for i in range(d + 1)]

# ---- M basis in terms of F:  M_alpha = sum_{beta refines alpha} (-1)^{l(beta)-l(alpha)} F_beta
def M_in_F(mask, n):
    """refinements of alpha = supersets of its descent set."""
    free = [p for p in range(n - 1) if not mask >> p & 1]
    out = {}
    for r in range(len(free) + 1):
        for sub in combinations(free, r):
            m = mask | sum(1 << p for p in sub)
            out[m] = out.get(m, 0) + (-1) ** r
    return out

def qsym_mul(f, i, g, j):
    """f,g dicts mask->coeff in F-basis of degrees i,j."""
    if i == 0: return {k: v * f.get(0, 0) for k, v in g.items()} if True else None
    if j == 0: return {k: v * g.get(0, 0) for k, v in f.items()}
    out = {}
    for ma, ca in f.items():
        for mb, cb in g.items():
            for m, c in F_product(ma, i, mb, j).items():
                out[m] = out.get(m, 0) + ca * cb * c
    return {k: v for k, v in out.items() if v}
