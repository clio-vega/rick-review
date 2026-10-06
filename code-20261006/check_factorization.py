"""
Is Rick's Corollary formula a composite of two CLASSICAL transition matrices?

Claim to test:  e_lambda = sum_nu K_{nu' lambda} s_nu          (leg 1, classical)
and             s_nu     = sum_mu Ktilde_{nu mu}(t) P_mu(x;t)  (leg 2, Macdonald III.6)
=> composite   e_lambda = sum_mu [ sum_nu K_{nu' lambda} Ktilde_{nu mu}(t) ] P_mu(x;t)
which is exactly Rick's bracket. Here we verify LEG 1 from scratch in N variables.
"""
import sympy as sp
from itertools import permutations
from kostka_d_matrix import partitions, conj, kostka

N = 6
xs = sp.symbols(f'x0:{N}')

def e_poly(k):
    from itertools import combinations
    return sp.expand(sum(sp.prod(c) for c in combinations(xs, k))) if k>0 else sp.Integer(1)

def e_lambda(lam):
    r = sp.Integer(1)
    for p in lam: r *= e_poly(p)
    return sp.expand(r)

def schur(lam):
    """Bialternant: s_lam = det(x_i^{lam_j + N - j}) / Vandermonde."""
    l = list(lam) + [0]*(N-len(lam))
    if len(l) > N: return None
    M = sp.Matrix(N, N, lambda i, j: xs[i]**(l[j] + N - 1 - j))
    V = sp.Matrix(N, N, lambda i, j: xs[i]**(N - 1 - j))
    return sp.simplify(sp.expand(M.det()) / sp.expand(V.det()))

print(f"LEG 1 check: e_lambda == sum_nu K_{{nu' lambda}} s_nu   in N={N} variables")
ok=fail=0
cache={}
for n in range(1, 6):
    for lam in partitions(n):
        lhs = e_lambda(lam)
        rhs = sp.Integer(0)
        for nu in partitions(n):
            if len(nu) > N: continue
            c = kostka(conj(nu), lam)
            if not c: continue
            if nu not in cache: cache[nu] = schur(nu)
            rhs += c * cache[nu]
        good = sp.simplify(sp.expand(lhs - sp.expand(rhs))) == 0
        ok += good; fail += (not good)
        if not good: print("   FAIL", lam)
print(f"  LEG 1: OK {ok}  FAIL {fail}")

print("\nNEGATIVE CONTROL: use K_{nu lambda} (no conjugate) instead")
ok2=fail2=0
for n in range(2, 5):
    for lam in partitions(n):
        lhs = e_lambda(lam)
        rhs = sp.Integer(0)
        for nu in partitions(n):
            if len(nu) > N: continue
            c = kostka(nu, lam)
            if not c: continue
            if nu not in cache: cache[nu] = schur(nu)
            rhs += c * cache[nu]
        good = sp.simplify(sp.expand(lhs - sp.expand(rhs))) == 0
        ok2 += good; fail2 += (not good)
print(f"  wrong-conjugate variant: matches {ok2}, mismatches {fail2} (want mismatches>0 => control fired)")
