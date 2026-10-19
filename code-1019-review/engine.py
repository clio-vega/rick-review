"""
Independent implementation of Rick's q=0 weight function phi^0 and his gauge F,
built ONLY from the explicit formula (2.1) of his Day-243 file
(proofs/2026-10-18-q488-converse-order-q1.md, section 2bis) --
not from any of his scripts, which are not in the repo.

(2.1)  phi^0_kappa(M) = sum_h prod_j (1-x_j^-2) prod_{k<kappa_j}(1-w_k/x_j)
                        * prod_{j<k} (1-1/(x_j x_k))/(1-x_j/x_k)
                        * prod_{t in M\h} prod_j (1-1/(w_t x_j))/(1-w_t/x_j)
       sum over INJECTIVE h:[r]->M, x_j := w_{h_j}, h_j carries label kappa_j.

F_kappa(M) := prod_{m in M} w_m^{2r} * sum_h T^0_kappa(h) * prod_j x_j^{kappa_j - 2j}
"""
import sympy as sp
from itertools import permutations, combinations

NMAX = 8
W = {i: sp.Symbol(f'w{i}') for i in range(1, NMAX + 1)}

def heads(M, r):
    """injective h:[r]->M, as tuples (h_1,...,h_r)"""
    return permutations(M, r)

def T0(kappa, M, h, subs=None):
    r = len(kappa)
    x = [W[hh] for hh in h]
    term = sp.Integer(1)
    for j in range(r):
        term *= (1 - x[j]**-2)
        for k in range(1, kappa[j]):
            term *= (1 - W[k] / x[j])
    for j in range(r):
        for k in range(j + 1, r):
            term *= (1 - 1 / (x[j] * x[k])) / (1 - x[j] / x[k])
    tails = [m for m in M if m not in h]
    for t in tails:
        for j in range(r):
            term *= (1 - 1 / (W[t] * x[j])) / (1 - W[t] / x[j])
    return term

def phi0(kappa, M):
    r = len(kappa)
    tot = sp.Integer(0)
    for h in heads(M, r):
        tot += T0(kappa, M, h)
    return sp.together(sp.simplify(tot))

def F(kappa, M):
    r = len(kappa)
    pre = sp.Integer(1)
    for m in M:
        pre *= W[m]**(2 * r)
    tot = sp.Integer(0)
    for h in heads(M, r):
        wt = sp.Integer(1)
        for j in range(r):
            wt *= W[h[j]]**(kappa[j] - 2 * (j + 1))
        tot += T0(kappa, M, h) * wt
    return sp.simplify(pre * tot)

def geq(M, I):
    s, r = len(M), len(I)
    if s < r: return False
    return all(i <= m for i, m in zip(I, M[s - r:]))

def subsets(N):
    out = []
    for k in range(N + 1): out.extend(combinations(range(1, N + 1), k))
    return out

if __name__ == '__main__':
    # TEST 1: triangularity of F (F_kappa(M) = 0 unless M >= kappa) -- D-inf section 1
    print("TEST 1  F_kappa(M) = 0 unless M >= kappa   (D-inf sec.1, via Prop 1 + (M3))")
    bad = []
    N = 4
    for kappa in subsets(N):
        for M in subsets(N):
            if len(M) < len(kappa): continue
            v = sp.simplify(F(kappa, M))
            iszero = (v == 0)
            if iszero != (not geq(M, kappa)):
                bad.append((kappa, M, geq(M, kappa), iszero))
    print(f"  N=4, all (kappa,M) with |M|>=|kappa|: mismatches = {len(bad)}  {bad[:5]}")

    # TEST 2: F_kappa(kappa) = phi0_kappa(kappa) * prod_j w_{kappa_j}^{kappa_j-2j+2r}
    print("TEST 2  F_kappa(kappa) = phi0_kappa(kappa) * prod_j w_{kappa_j}^{kappa_j-2j+2r}")
    bad2 = []
    for kappa in subsets(4):
        r = len(kappa)
        lhs = sp.simplify(F(kappa, kappa))
        rhs = phi0(kappa, kappa)
        for j in range(r):
            rhs *= W[kappa[j]]**(kappa[j] - 2 * (j + 1) + 2 * r)
        if sp.simplify(sp.together(lhs - rhs)) != 0:
            bad2.append(kappa)
    print(f"  N=4 all kappa: mismatches = {len(bad2)}  {bad2}")
