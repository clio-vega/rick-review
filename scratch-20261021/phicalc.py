"""Independent reimplementation of Rick's Phi-calculus from
proofs/2026-10-20-dual-block-identity.md section 1 ONLY (his scripts are unpublished).

Definitions transcribed verbatim from his text:
  S0^M(H) = prod_{j in H}(1 - x_j^{-2}) * prod_{{j,k} subset H}(1 - 1/(x_j x_k))
            * prod_{j in H, t in M\H} (x_j - 1/w_t)/(x_j - w_t)
  Phi_r^M[f] = sum_{|H|=r} S0^M(H) f(x_H)
  V(x_1..x_r) = prod_{j<k}(x_k - x_j),  Alt[F] = sum_sigma sgn(sigma) F(x_sigma)
  g_S(u) = prod_{t in S}(u - 1/w_t)/(u - w_t)
  G_S(z) = prod_{t in S}(z - 1/w_t)/(z - w_t)      (same function, his two names)
  e_M = prod_{m in M} w_m
Targets: Lemma H (exact peel), Lemma P1, the Lagrange step, Lemma Lambda.
"""
import sympy as sp
from itertools import combinations, permutations

def wvars(M):
    return {m: sp.Symbol('w%d' % m, positive=True) for m in M}

def S0(M, H, w):
    """S0^M(H); H a tuple of labels, w a dict label->symbol."""
    H = tuple(H)
    out = sp.Integer(1)
    for j in H:
        out *= (1 - w[j]**-2)
    for j, k in combinations(H, 2):
        out *= (1 - 1/(w[j]*w[k]))
    for j in H:
        for t in M:
            if t in H:
                continue
            out *= (w[j] - 1/w[t])/(w[j] - w[t])
    return out

def Phi(M, r, f, w):
    """Phi_r^M[f]; f takes a tuple of sympy exprs (the x_H), must be symmetric."""
    if r > len(M):
        return sp.Integer(0)
    tot = sp.Integer(0)
    for H in combinations(sorted(M), r):
        tot += S0(M, H, w) * f(tuple(w[j] for j in H))
    return sp.together(sp.simplify(tot))

def gS(S, u, w):
    out = sp.Integer(1)
    for t in S:
        out *= (u - 1/w[t])/(u - w[t])
    return out

def e_of(M, w):
    out = sp.Integer(1)
    for m in M:
        out *= w[m]
    return out

def zero(expr):
    return sp.simplify(sp.together(expr)) == 0

