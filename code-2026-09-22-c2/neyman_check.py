"""
Verification of two identities in Neyman, arXiv:1410.5039
  - Theorem \label{schurpols}   (line 1677 of the e-print source)  "Cylindric Cauchy Identity"
  - Corollary \label{oneschurcor} (line 1824)
Conventions follow the e-print's Section 2 (Preliminary Definitions, line 112ff):
  cylinder C_{k,n} = Z^2/(-k,n-k)Z, n > k;
  a cylindric partition lambda is weakly decreasing bi-infinite with
  lambda_m = lambda_{m+k} + (n-k).
We store lambda by its fundamental window (lambda_0,...,lambda_{k-1}).
"""
from itertools import product
from collections import defaultdict

def part_at(lam, i, k, n):
    """lambda_i for arbitrary i in Z, from the window lam=(lam_0..lam_{k-1})."""
    q, r = divmod(i, k)
    return lam[r] - q * (n - k)

def is_cylpar(lam, k, n):
    return all(part_at(lam, i, k, n) >= part_at(lam, i + 1, k, n) for i in range(k))

def contains(lam, mu, k, n):
    """mu subseteq lam  <=>  mu_m <= lam_m for all m (Def. at src line ~160)."""
    return all(mu[i] <= lam[i] for i in range(k))

def nboxes(lam, mu, k, n):
    return sum(lam[i] - mu[i] for i in range(k))

def is_hstrip(lam, mu, k, n):
    """lam/mu horizontal strip <=> lam_i >= mu_i >= lam_{i+1}  (footnote, src line ~247)."""
    if not contains(lam, mu, k, n):
        return False
    return all(mu[i] >= part_at(lam, i + 1, k, n) for i in range(k))

def cylpars_between(mu, lam, k, n):
    """all cylindric nu with mu subseteq nu subseteq lam."""
    rng = [range(mu[i], lam[i] + 1) for i in range(k)]
    return [nu for nu in product(*rng) if is_cylpar(nu, k, n)]

# ---------- generating function via the chain model ----------
def gf_chain(lam, mu, k, n, ell):
    """sum over SSCT(lam/mu) with alphabet {1..ell} of x^wt, as dict weight-tuple -> count.
    Chain model: mu = b^0 <= b^1 <= ... <= b^ell = lam, each b^t/b^{t-1} a horizontal strip."""
    if not contains(lam, mu, k, n):
        return {}
    mid = cylpars_between(mu, lam, k, n)
    cur = {mu: {(): 1}}
    for t in range(ell):
        nxt = defaultdict(lambda: defaultdict(int))
        for b, wts in cur.items():
            for c in mid:
                if not contains(c, b, k, n):
                    continue
                if not is_hstrip(c, b, k, n):
                    continue
                d = nboxes(c, b, k, n)
                for w, m in wts.items():
                    nxt[c][w + (d,)] += m
        cur = {c: dict(v) for c, v in nxt.items()}
    return cur.get(lam, {})

# ---------- generating function by brute-force filling (independent check) ----------
def gf_direct(lam, mu, k, n, ell):
    if not contains(lam, mu, k, n):
        return {}
    boxes = [(i, y) for i in range(k) for y in range(mu[i] + 1, lam[i] + 1)]
    if not boxes:
        return {(): 1} if ell == 0 else {tuple([0] * ell): 1}
    idx = {b: j for j, b in enumerate(boxes)}

    def box_of(x, y):
        """representative (i,y') in the fundamental window of the class of point (x,y)."""
        q, r = divmod(x, k)
        return (r, y + q * (n - k))

    def in_shape_point(x, y):
        return part_at(mu, x, k, n) < y <= part_at(lam, x, k, n)

    cons = []                      # (j1, j2, strict)  meaning entry[j1] < or <= entry[j2]
    for (i, y) in boxes:           # rows: weakly increasing to the right
        if (i, y + 1) in idx:
            cons.append((idx[(i, y)], idx[(i, y + 1)], False))
    # columns: strictly increasing downward, over the *points* of the cylinder
    cols = defaultdict(list)
    XLO, XHI = -4 * k - 4, 4 * k + 4
    for x in range(XLO, XHI + 1):
        for y in range(min(mu) - 2 * n - 4, max(lam) + 2 * n + 5):
            if in_shape_point(x, y):
                cols[y].append(x)
    for y, xs in cols.items():
        xs = sorted(xs)
        for a, b in zip(xs, xs[1:]):
            ja, jb = idx[box_of(a, y)], idx[box_of(b, y)]
            cons.append((ja, jb, True))

    out = defaultdict(int)
    for f in product(range(1, ell + 1), repeat=len(boxes)):
        ok = True
        for (a, b, strict) in cons:
            if (f[a] >= f[b]) if strict else (f[a] > f[b]):
                ok = False
                break
        if ok:
            w = [0] * ell
            for v in f:
                w[v - 1] += 1
            out[tuple(w)] += 1
    return dict(out)

def add_into(acc, gf):
    for w, c in gf.items():
        acc[w] = acc.get(w, 0) + c
