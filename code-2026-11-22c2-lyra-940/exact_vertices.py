"""Clio 2026-11-23: exact (Fraction) vertex enumeration for Lyra 940 sec.1.
Cyclic: T = (1/n) sum_r (p_i(r)-c)(p_j(r)-p_j(r+1)); LOO: d_r = p_j(r) - mean_{u!=r} p_j(u).
T is bilinear and T/(R_i R_j) is affine-invariant, so max over p in [0,1]^n x [0,1]^n is at a vertex
(vertices with R=0 give T=0). Reports exact max of T/(R_iR_j) and a witness."""
from fractions import Fraction as F
from itertools import product
def T(pi, pj, loo):
    n = len(pi); c = F(max(pi) + min(pi), 2); s = sum(pj)
    if loo: d = [pj[r] - F(s - pj[r], n - 1) for r in range(n)]
    else:   d = [pj[r] - pj[(r + 1) % n] for r in range(n)]
    return sum((pi[r] - c) * d[r] for r in range(n)) / n
for n in range(2, 9):
    V = [v for v in product((0, 1), repeat=n) if 0 < sum(v) < n]
    for loo in (False, True):
        best, wit = max(((T(a, b, loo), (a, b)) for a in V for b in V), key=lambda t: t[0])
        if loo: claim, sharp = F(n, 4 * (n - 1)), F((n // 2) * ((n + 1) // 2), n * (n - 1))
        else:   claim, sharp = F(1, 2), F(n // 2, n)
        print(f"n={n} {'LOO' if loo else 'cyc'} max={best} sharp_formula={sharp} "
              f"{'OK' if best == sharp else 'MISMATCH'} slack_used={claim} valid={best <= claim} "
              f"tight={best == claim} witness={wit}")
