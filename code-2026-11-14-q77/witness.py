import sys
from core import *

def operator(n, N, seq, C):
    """beta: v_w -> (v_w . 1_C) . a ; returns dict word->vector"""
    beta = {}
    for mu in compositions(N, n):
        if mu not in C: continue
        for w in words_of_weight(mu):
            z = apply_seq({w: 1}, seq)
            if z: beta[w] = z
    return beta

def in_B(beta, S):
    """exact: beta commutes with every phi in the S basis. phi maps word->word."""
    bad = 0
    for mu, nu, phi in S:
        for w, wimg in phi.items():
            # phi(beta(w)) vs beta(phi(w))
            lhs = defaultdict(int)
            for x, c in beta.get(w, {}).items(): lhs[phi_full(phi, x, mu)] += c
            rhs = beta.get(wimg, {})
            lhs = {k: v for k, v in lhs.items() if v and k is not None}
            if lhs != rhs: bad += 1
    return bad

def phi_full(phi, x, mu):
    return phi.get(x)   # None if x not of weight mu (phi zero there)

def pair_orbit_components(s, g, N):
    """simultaneous-move orbit of (s,g); union-find components of bipartite graph."""
    seen = {(s, g)}; dq = deque([(s, g)])
    while dq:
        a, b = dq.popleft()
        for i in range(1, N):
            p = (move(a, i), move(b, i))
            if p not in seen: seen.add(p); dq.append(p)
    parent = {}
    def f(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for a, b in seen:
        ra, rb = f((0, a)), f((1, b))
        if ra != rb: parent[ra] = rb
    return seen, f

def notin_A_certificate(zs, zg, s, g, N):
    """(zs, zg) = (s.beta, g.beta). Exists signed component functional nonzero on it?
    lambda_C = +1 on left nodes of C, -1 on right nodes; kills every orbit edge."""
    seen, f = pair_orbit_components(s, g, N)
    val = defaultdict(int)
    for w, c in zs.items():
        val[f((0, w))] += c
    for w, c in zg.items():
        val[f((1, w))] -= c
    nz = [k for k, v in val.items() if v]
    return len(seen), len(nz)
