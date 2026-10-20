"""Target (a): verify Rick's 'allowed' domain definition reproduces his counts.
Definition (d-infinity file, head of section 8, added 2026-10-20):
  domain: lambda, mu, nu subset [N], {lambda,mu} unordered, nu >= lambda,mu,
          |nu| - max(|lambda|,|mu|) >= 2, 1 <= a < b <= N
  allowed iff E(lambda,mu,nu;ab) != empty.
Stated sizes: N=3 39/25, N=4 762/408, N=5 11360/5578.
|.| is OVERLOADED in this corpus: Motegi's theorem uses |I| = sum of parts,
the 'jump' language uses cardinality.  Test BOTH readings.
"""
from itertools import combinations

def subsets(N):
    out = []
    for r in range(N+1):
        out += [frozenset(c) for c in combinations(range(1, N+1), r)]
    return out

def dom_ge(M, kappa):
    """top-aligned dominance M >= kappa: injection h:[r]->M with h_j >= kappa_j.
    Greedy/Hall: align from the top."""
    Ms = sorted(M, reverse=True); ks = sorted(kappa, reverse=True)
    if len(Ms) < len(ks):
        return False
    return all(Ms[i] >= ks[i] for i in range(len(ks)))

def E(lam, mu, nu, a, b, N):
    out = []
    ground = [i for i in range(1, N+1) if i not in (a, b)]
    for r in range(len(ground)+1):
        for c in combinations(ground, r):
            Mpp = frozenset(c)
            if dom_ge(nu, Mpp | {a, b}) and dom_ge(Mpp, lam) and dom_ge(Mpp, mu):
                out.append(Mpp)
    return out

def census(N, size):
    subs = subsets(N)
    total = 0; allowed = 0
    for i, lam in enumerate(subs):
        for mu in subs[i:]:              # {lambda,mu} unordered
            for nu in subs:
                if not (dom_ge(nu, lam) and dom_ge(nu, mu)):
                    continue
                if size(nu) - max(size(lam), size(mu)) < 2:
                    continue
                for a in range(1, N+1):
                    for b in range(a+1, N+1):
                        total += 1
                        if E(lam, mu, nu, a, b, N):
                            allowed += 1
    return total, allowed

card = lambda S: len(S)
summ = lambda S: sum(S)

claimed = {3: (39, 25), 4: (762, 408), 5: (11360, 5578)}
for N in (3, 4, 5):
    print(f"N={N}  claimed cases/allowed = {claimed[N]}")
    for name, f in (("cardinality", card), ("sum-of-parts", summ)):
        t, a = census(N, f)
        mark = "  <== MATCH" if (t, a) == claimed[N] else ""
        print(f"    |.| = {name:13s} -> {t:6d} / {a:6d}{mark}")
