import sys, numpy as np
from core import *
P1, P2 = 2147483629, 2147483587
def rank_mod(rows, ncols, p):
    """rows: list of dict col->int. Streaming Gaussian elimination mod p (dict pivots)."""
    piv = {}  # pivot col -> row dict (normalised)
    for r in rows:
        r = {c: v % p for c, v in r.items() if v % p}
        while r:
            c = min(r)
            if c in piv:
                f = r[c]; pr = piv[c]
                for cc, vv in pr.items():
                    nv = (r.get(cc, 0) - f*vv) % p
                    if nv: r[cc] = nv
                    else: r.pop(cc, None)
            else:
                inv = pow(r[c], p-2, p)
                piv[c] = {cc: vv*inv % p for cc, vv in r.items()}
                break
    return len(piv)
def monoid(N, words):
    """all pi_x as functions on words (tuple of word-indices), BFS over generators."""
    idx = {w: k for k, w in enumerate(words)}
    gens = [tuple(idx[move(w, i)] for w in words) for i in range(1, N)]
    start = tuple(range(len(words)))
    seen = {start}; dq = deque([start])
    while dq:
        f = dq.popleft()
        for g in gens:
            h = tuple(g[f[k]] for k in range(len(words)))   # apply f then pi_i (right action)
            if h not in seen: seen.add(h); dq.append(h)
    return seen
def dimA(n, N, p):
    words = list(itertools.product(range(1, n+1), repeat=N)); W = len(words)
    fs = monoid(N, words)
    rows = [{k*W + f[k]: 1 for k in range(W)} for f in fs]
    return len(fs), rank_mod(rows, W*W, p)
def dimB(n, N, p):
    S = schur_basis(n, N)
    wts = list(compositions(N, n)); blocks = {mu: words_of_weight(mu) for mu in wts}
    var = {}
    for mu in wts:
        for a in blocks[mu]:
            for b in blocks[mu]: var[(a, b)] = len(var)   # b_mu[a<-b]: coefficient of a in b(v_b)
    rows = []
    for mu, nu, phi in S:
        inv = defaultdict(list)
        for x, y in phi.items(): inv[y].append(x)
        for w in blocks[mu]:
            # (b o phi)(w) = b_nu(phi(w)) ; (phi o b)(w) = sum_x b_mu[x<-w] phi(x)
            for t in blocks[nu]:
                r = defaultdict(int)
                r[var[(t, phi[w])]] += 1
                for x in inv[t]: r[var[(x, w)]] -= 1
                r = {k: v for k, v in r.items() if v}
                if r: rows.append(r)
    U = len(var)
    return U, U - rank_mod(rows, U, p)
if __name__ == '__main__':
    n, N = int(sys.argv[1]), int(sys.argv[2])
    for p in (P1, P2):
        print((n, N), 'p', p, '|monoid|,dimA =', dimA(n, N, p), ' U,dimB =', dimB(n, N, p) if len(sys.argv) < 4 else 'skip', flush=True)
