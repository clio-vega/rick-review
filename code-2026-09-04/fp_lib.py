"""Independent reimplementation of Rick's F_P from its DEFINITION (Day 152 §1):
   F_P := Tplus(e^{T e_2} V) / V,  V = prod_{i<j}(u_i-u_j),  Tplus: u^alpha -> prod u_i^(alpha_i) rising.
Nothing here is copied from Rick's scripts; only the definition is taken from his paper.
"""
import sympy as sp

u1, u2, u3, T = sp.symbols('u1 u2 u3 T')
us = (u1, u2, u3)
V = (u1-u2)*(u1-u3)*(u2-u3)
e2sym = u1*u2 + u1*u3 + u2*u3

def rising(x, a):
    r = sp.Integer(1)
    for j in range(a):
        r *= (x + j)
    return r

def Tplus(expr):
    p = sp.Poly(sp.expand(expr), *us)
    out = sp.Integer(0)
    for mono, c in zip(p.monoms(), p.coeffs()):
        term = sp.sympify(c)
        for x, a in zip(us, mono):
            term *= rising(x, a)
        out += term
    return sp.expand(out)

def FP_coeffs(N):
    """[T^0..T^{N-1}] of F_P, each an expanded polynomial in u1,u2,u3."""
    out = []
    e2k = sp.Integer(1)
    for k in range(N):
        num = Tplus(sp.expand(e2k * V))
        q, r = sp.div(sp.Poly(num, u1, u2, u3), sp.Poly(sp.expand(V), u1, u2, u3))
        assert r.is_zero, f"V does not divide at k={k}"
        out.append(sp.expand(q.as_expr() / sp.factorial(k)))
        e2k = sp.expand(e2k * e2sym)
    return out

# ---- truncated power series arithmetic in T, coefficients = polys in u ----
def mul(A, B, N):
    C = [sp.Integer(0)]*N
    for i, a in enumerate(A):
        if a == 0: continue
        for j, b in enumerate(B):
            if i+j >= N: break
            if b == 0: continue
            C[i+j] += a*b
    return [sp.expand(c) for c in C]

def logs(A, N):
    """log of a series with A[0]==1."""
    assert sp.simplify(A[0]-1) == 0
    U = [sp.Integer(0)] + [A[i] for i in range(1, N)]   # U = A-1
    res = [sp.Integer(0)]*N
    P = [sp.Integer(1)] + [sp.Integer(0)]*(N-1)         # U^0
    P = None
    term = [sp.Integer(0)]*N
    # log(1+U) = sum_{m>=1} (-1)^{m+1} U^m/m ; U has no constant term so m<N
    Um = [sp.Integer(1)] + [sp.Integer(0)]*(N-1)
    for m in range(1, N):
        Um = mul(Um, U, N)
        s = sp.Rational((-1)**(m+1), m)
        for i in range(N):
            res[i] += s*Um[i]
    return [sp.expand(c) for c in res]

def inv(A, N):
    assert sp.simplify(A[0]-1) == 0
    B = [sp.Integer(0)]*N
    B[0] = sp.Integer(1)
    for n in range(1, N):
        s = sp.Integer(0)
        for k in range(1, n+1):
            s += A[k]*B[n-k]
        B[n] = sp.expand(-s)
    return B

def homog(expr, d, vars=us):
    """degree-d homogeneous component in the u-variables."""
    p = sp.Poly(sp.expand(expr), *vars)
    out = sp.Integer(0)
    for mono, c in zip(p.monoms(), p.coeffs()):
        if sum(mono) == d:
            t = sp.sympify(c)
            for x, a in zip(vars, mono):
                t *= x**a
            out += t
    return sp.expand(out)

def layer(series, w, vars=us):
    """ell^top_w : at [T^n] keep u-degree n+w."""
    return [homog(c, n+w, vars) if n+w >= 0 else sp.Integer(0)
            for n, c in enumerate(series)]
