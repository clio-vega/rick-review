"""Independent re-implementation of Rick's Day 206b conventions (UID 728).

NOT a copy of his scripts/day206b/check_W_r_proof.py -- written from the
conventions printed in his sect.1, so that agreement is a differential check.

Conventions (his sect.1):
  T_i F = t s_i F + (t-1) X_{i+1} (s_i F - F)/(X_i - X_{i+1})
  pi F  = X_1 F(X_2,...,X_m, s X_1),   s = 1/q
  Y_i   = t^{m-i} T_{i-1}...T_1 pi T_{m-1}^{-1}...T_i^{-1}   (rightmost acts first)
"""
import sympy as sp
from sympy import symbols, Rational, simplify, cancel, expand, together

q, t = symbols('q t')
s = 1/q

def mkvars(m):
    return symbols('X1:%d' % (m+1))

def si(F, i, X):
    """swap X_i <-> X_{i+1}, 1-indexed i."""
    a, b = X[i-1], X[i]
    tmp = symbols('__tmp')
    return F.subs({a: tmp, b: a}, simultaneous=True).subs(tmp, b)

def T(F, i, X):
    sF = si(F, i, X)
    a, b = X[i-1], X[i]
    return sp.cancel(sp.together(t*sF + (t-1)*b*(sF - F)/(a - b)))

def Tinv(F, i, X):
    # T^{-1} = t^{-1} T - (1 - t^{-1})
    return sp.cancel(T(F, i, X)/t - (1 - 1/t)*F)

def pi(F, X):
    m = len(X)
    sub = {X[k]: X[k+1] for k in range(m-1)}
    sub[X[m-1]] = s*X[0]
    return sp.cancel(X[0]*F.subs(sub, simultaneous=True))

def Y(F, i, X):
    m = len(X)
    G = F
    for k in range(m-1, i-1, -1):      # T_{m-1}^{-1} ... T_i^{-1}, rightmost first => apply T_i^{-1} first
        pass
    # rightmost factor acts first: T_i^{-1} is rightmost
    G = F
    for k in range(i, m):              # k = i, i+1, ..., m-1
        G = Tinv(G, k, X)
    G = pi(G, X)
    for k in range(1, i):              # T_1 then ... then T_{i-1}
        G = T(G, k, X)
    return sp.cancel(t**(m-i) * G)

def e(n, X):
    m = len(X)
    if n < 0 or n > m: return sp.Integer(0)
    return sp.expand(sp.symmetric_poly(n, *X)) if n > 0 else sp.Integer(1)

def bracket(n):
    """[n]_t = (1-t^n)/(1-t)"""
    return sp.cancel((1 - t**n)/(1 - t))

def W(r, X):
    return sp.expand(sp.cancel(
        s**2*e(2,X)*e(r,X)
        + s*(1-s)*bracket(r)*e(1,X)*e(r+1,X)
        + (1-s)*(bracket(r+2)/bracket(2))*(bracket(r+1) - s*(bracket(r)-1))*e(r+2,X)))

def norm(F):
    return sp.simplify(sp.cancel(sp.expand(F)))

# ---------- checks ----------
import sys
print("=== CHECK A: Claim 4 (pair formula) Y_i Y_j F = t T_{i-1}..T_1 T_{j-1}..T_2 pi^2 F ===")
for m in [2,3,4]:
    X = mkvars(m)
    tests = [e(1,X), e(min(2,m),X), e(m,X), sp.expand(e(1,X)**2)]
    for F in tests:
        for i in range(1, m+1):
            for j in range(i+1, m+1):
                lhs = Y(Y(F, j, X), i, X)
                G = pi(pi(F, X), X)
                for k in range(2, j):    # T_2 ... T_{j-1}, rightmost T_2 first
                    G = T(G, k, X)
                for k in range(1, i):    # T_1 ... T_{i-1}
                    G = T(G, k, X)
                rhs = sp.cancel(t*G)
                d = norm(lhs - rhs)
                tag = "OK " if d == 0 else "FAIL"
                if d != 0 or (m==2) or (j==i+1 and m<=3):
                    print(f"  {tag} m={m} (i,j)=({i},{j}) F={F}  diff={d}")
                assert d == 0, (m,i,j,F,d)
print("  A: all pairs m=2,3,4 pass")
