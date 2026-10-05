"""Verify the INGREDIENTS of Rick's Lemma 6 (the reasons, not the conclusion).
q_n computed by explicit series division, not sp.series (too slow)."""
import sympy as sp, itertools
s, t, gam = sp.symbols('s t gamma')

def Xs(m): return list(sp.symbols(f'X1:{m+1}'))
def ee(X, k):
    if k < 0 or k > len(X): return sp.Integer(0)
    if k == 0: return sp.Integer(1)
    return sum(sp.prod(cb) for cb in itertools.combinations(X, k))
def Eser(X, a, N):
    """coeffs of prod(1 + a*X_i*y) in y, up to y^N  -> list"""
    return [sp.expand(a**n*ee(X, n)) for n in range(N+1)]
def qlist(X, N):
    """Q(y)=E(-ty)/E(-y): solve E(-y)*Q = E(-ty) by forward substitution."""
    A = Eser(X, -1, N)      # E(-y)
    B = Eser(X, -t, N)      # E(-ty)
    q = []
    for n in range(N+1):
        v = B[n] - sum(A[i]*q[n-i] for i in range(1, n+1))
        q.append(sp.expand(sp.cancel(v/A[0])))
    return q
def Epoly(X, arg): return sp.prod([1 + x*arg for x in X])
