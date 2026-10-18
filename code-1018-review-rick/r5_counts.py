"""Debt #4 (Rick, UID 817): "tell me what your N=3 counts 58+12, 44+7, 12+1, 1 = 135
are counting."  Re-DERIVED from the engine at N=2 (the second summands), not restated
from my own prose.  Jump := |nu| - max(|lam|,|mu|); half := mu >= lam in Motegi's order.
"""
import sys, itertools
sys.path.insert(0,'/home/clio/projects/proofs/code-1018c2-gauge')
import sympy as sp
from q484_engine import Atilde, subsets, geq, q

def census(N):
    S = sorted(subsets(N), key=lambda T: (len(T), sum(T)))
    w = sp.symbols(f'w1:{N+1}')
    A = {(M,I): sp.cancel(Atilde(N, list(w), list(M), list(I), X='C')) for M in S for I in S}
    jump = {}
    for lam, mu in itertools.product(S, S):
        if not geq(mu, lam): continue          # the mu >= lam half
        c = {}
        for nu in S:
            rhs = A[nu,lam]*A[nu,mu] - sum(c[k]*A[nu,k] for k in c)
            c[nu] = sp.cancel(rhs/A[nu,nu])
        for nu in S:
            if c[nu] == 0: continue            # nonzero constants only
            j = len(nu) - max(len(lam), len(mu))
            den = sp.fraction(sp.cancel(sp.together(c[nu])))[1]
            # Laurent  <=>  the denominator is a UNIT of C(q)[w^+-], i.e. c(q) times a
            # MONOMIAL in w.  (A total-degree-0 test is wrong: it misclassifies every
            # genuine pole whose denominator happens to be inhomogeneous.)
            laurent = len(sp.Poly(den, *w).monoms()) == 1
            jump.setdefault(j, [0,0])[0 if laurent else 1] += 1
    return jump

for N in (2,):
    j = census(N)
    tot = sum(a+b for a,b in j.values())
    print(f"N={N}:  total nonzero on the mu>=lam half = {tot}")
    for k in sorted(j): print(f"   jump {k}:  Laurent {j[k][0]:3d}   poles {j[k][1]:3d}")
