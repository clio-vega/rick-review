"""Independent engine for T0 / Psi_{kappa,theta}(M), built from the DEFINITIONS in
proofs/2026-10-18-q488-d-infinity.md section 1 and the certifier file section 2 --
NOT from Rick's scripts.  Exact rational arithmetic.

T0_kappa(h) = prod_j (1-x_j^-2) * prod_j prod_{k<kappa_j}(1-w_k/x_j)
            * prod_{j<k} (1-1/(x_j x_k))/(1-x_j/x_k)
            * prod_{t in tails, j} (1-1/(w_t x_j))/(1-w_t/x_j)
Psi_{kappa,theta}(M) = sum_h T0_kappa(h) prod_j x_j^{theta_j}
"""
from fractions import Fraction as F
from itertools import permutations, combinations
import random

def Psi(kappa, theta, M, w):
    """kappa: increasing tuple of labels; theta: tuple same length; M: tuple; w: dict i->Fraction"""
    r = len(kappa); M = tuple(sorted(M))
    assert len(theta) == r
    tot = F(0)
    for h in permutations(M, r):            # injective [r] -> M
        x = [w[hj] for hj in h]
        tails = [t for t in M if t not in h]
        term = F(1)
        for j in range(r):
            term *= (1 - 1/x[j]**2)
            for k in range(1, kappa[j]):    # rho_{kappa_j}(x_j)
                term *= (1 - w[k]/x[j])
            if term == 0: break
        if term == 0: continue
        for j in range(r):
            for k in range(j+1, r):
                term *= (1 - 1/(x[j]*x[k])) / (1 - x[j]/x[k])
        for t in tails:
            for j in range(r):
                term *= (1 - 1/(w[t]*x[j])) / (1 - w[t]/x[j])
        for j in range(r):
            term *= x[j]**theta[j]
        tot += term
    return tot

def S0(H, M, w):
    """S0^M(H) from the Day 248 file section 1"""
    H = tuple(sorted(H)); tails = [t for t in M if t not in H]
    v = F(1)
    for j in H: v *= (1 - 1/w[j]**2)
    for j, k in combinations(H, 2): v *= (1 - 1/(w[j]*w[k]))
    for j in H:
        for t in tails: v *= (w[j] - 1/w[t]) / (w[j] - w[t])
    return v

def rho(k, x, w):
    v = F(1)
    for i in range(1, k): v *= (1 - w[i]/x)
    return v

def V(xs):
    v = F(1)
    for i in range(len(xs)):
        for j in range(i+1, len(xs)): v *= (xs[j] - xs[i])
    return v

def A_alt(kappa, theta, xs, w):
    """A_{kappa,theta}(x) = Alt[prod_j x_j^{j-1+theta_j} rho_{kappa_j}(x_j)] / V(x)"""
    r = len(kappa); tot = F(0)
    for p in permutations(range(r)):
        sgn = 1
        pl = list(p)
        for i in range(r):
            for j in range(i+1, r):
                if pl[i] > pl[j]: sgn = -sgn
        term = F(1)
        for j in range(r):
            xj = xs[p[j]]
            term *= xj**(j + theta[j]) * rho(kappa[j], xj, w)   # x^{j-1+theta}, j 0-indexed
        tot += sgn * term
    return tot / V(xs)

def Psi_alt(kappa, theta, M, w):
    """Lemma A: Psi = sum_{H subset M, |H|=r} S0^M(H) * A_{kappa,theta}(x_H)"""
    r = len(kappa); tot = F(0)
    for H in combinations(sorted(M), r):
        xs = [w[h] for h in H]
        tot += S0(H, M, w) * A_alt(kappa, theta, xs, w)
    return tot

def randw(N, seed):
    rnd = random.Random(seed)
    while True:
        w = {i: F(rnd.randint(2, 200), rnd.randint(1, 31)) for i in range(1, N+1)}
        vals = list(w.values())
        ok = len(set(vals)) == N and all(v != 1 for v in vals)
        ok = ok and all(vals[i]*vals[j] != 1 for i in range(N) for j in range(N))
        if ok: return w
