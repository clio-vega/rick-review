"""
Task 2: independent combinatorics for Rick's Theorem D-infinity (2026-10-19 review).

Order convention read FIRST-HAND from Motegi arXiv:2610.15344,
Prop at L3247-3259 (eq:typeC-shifted-dominance):
  for M = {m_1<...<m_s}, I = {i_1<...<i_r}, s >= r,
  "M >= I"  <=>  i_j <= m_{s-r+j} for j=1..r  <=>  lambda(I) subset lambda(M),
i.e. the top r elements of M dominate I elementwise.
Nothing here is taken from Rick's prose.
"""
from itertools import combinations

def geq(M, I):
    """M >= I in the shifted-dominance order (M, I are sorted tuples)."""
    s, r = len(M), len(I)
    if s < r:
        return False
    top = M[s - r:]          # top r elements of M, increasing
    return all(i <= m for i, m in zip(I, top))

def subsets(N):
    out = []
    for k in range(N + 1):
        out.extend(combinations(range(1, N + 1), k))
    return out

def E(lam, mu, nu, a, b):
    """E(lam,mu,nu;ab) = {M'' subset [N]\\{a,b} : M''u{a,b} <= nu, M''>=lam, M''>=mu}."""
    ground = [x for x in nu_ground if x not in (a, b)]
    res = []
    for k in range(len(ground) + 1):
        for Mpp in combinations(ground, k):
            M = tuple(sorted(Mpp + (a, b)))
            if geq(nu, M) and geq(Mpp, lam) and geq(Mpp, mu):
                res.append(Mpp)
    return res

def jump(lam, mu, nu):
    return len(nu) - max(len(lam), len(mu))

for N in (3, 4, 5):
    nu_ground = tuple(range(1, N + 1))
    S = subsets(N)
    pairs = list(combinations(range(1, N + 1), 2))
    allowed = [(l, m, n) for l in S for m in S for n in S if geq(n, l) and geq(n, m)]
    print(f"N={N}: allowed triples (nu>=lam, nu>=mu) = {len(allowed)}")

    # pair-level census: (triple,pair) cases with E != empty
    pair_nonempty = 0
    pair_total = 0
    for (l, m, n) in allowed:
        for (a, b) in pairs:
            pair_total += 1
            if E(l, m, n, a, b):
                pair_nonempty += 1
    print(f"   (triple,pair) cases = {pair_total}, E!=0 on {pair_nonempty}, E=0 on {pair_total-pair_nonempty}")

    # TRIPLE-level criterion comparison, reported as a SET
    only_E, only_J = [], []
    for (l, m, n) in allowed:
        hasE = any(E(l, m, n, a, b) for (a, b) in pairs)
        hasJ = jump(l, m, n) >= 2
        if hasE and not hasJ:
            only_E.append((l, m, n))
        if hasJ and not hasE:
            only_J.append((l, m, n))
    print(f"   SYMMETRIC DIFFERENCE {{exists ab: E!=0}} vs {{jump>=2}}:")
    print(f"     in E-side only ({len(only_E)}): {only_E[:12]}{' ...' if len(only_E)>12 else ''}")
    print(f"     in J-side only ({len(only_J)}): {only_J[:12]}{' ...' if len(only_J)>12 else ''}")

    # Rick's named witness: a<b the two smallest elements of nu
    wit_fail = []
    for (l, m, n) in allowed:
        if jump(l, m, n) >= 2:
            if len(n) < 2:
                wit_fail.append(((l, m, n), "nu too small"))
                continue
            a, b = n[0], n[1]
            if not E(l, m, n, a, b):
                wit_fail.append(((l, m, n), (a, b)))
    print(f"   Rick's named witness pair (two smallest of nu) FAILS on {len(wit_fail)}: {wit_fail[:8]}")
    print()
