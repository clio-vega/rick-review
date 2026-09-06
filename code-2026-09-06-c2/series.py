"""Truncated power series over Q[s,p], for the Day 170 audit.  Clio 2026-09-06 c2."""
import sympy as sp
s, p, T = sp.symbols('s p T')

def trim(a, N):
    a = list(a[:N+1]) + [sp.Integer(0)]*(N+1-len(a))
    return [sp.expand(x) for x in a]

def add(a, b): return [sp.expand(x+y) for x, y in zip(a, b)]
def sub(a, b): return [sp.expand(x-y) for x, y in zip(a, b)]
def smul(c, a): return [sp.expand(c*x) for x in a]

def mul(a, b):
    N = len(a)-1
    out = [sp.Integer(0)]*(N+1)
    for i, x in enumerate(a):
        if x == 0: continue
        for j, y in enumerate(b):
            if i+j > N: break
            if y == 0: continue
            out[i+j] += x*y
    return [sp.expand(v) for v in out]

def inv(a):
    """1/a, requires a[0] != 0"""
    N = len(a)-1
    a0 = a[0]
    assert sp.expand(a0) != 0
    out = [sp.Integer(0)]*(N+1)
    out[0] = sp.cancel(1/a0)
    for n in range(1, N+1):
        acc = sp.Integer(0)
        for k in range(1, n+1):
            acc += a[k]*out[n-k]
        out[n] = sp.cancel(sp.expand(-acc/a0))
    return [sp.expand(v) for v in out]

def div(a, b): return mul(a, inv(b))

def deriv(a):
    N = len(a)-1
    return [sp.expand((k+1)*a[k+1]) if k+1 <= N else sp.Integer(0) for k in range(N+1)]

def integ(a):
    """antiderivative with zero constant term"""
    N = len(a)-1
    out = [sp.Integer(0)]*(N+1)
    for k in range(1, N+1):
        out[k] = sp.expand(sp.Rational(1, k)*a[k-1])
    return out

def const(c, N): return [sp.expand(c)] + [sp.Integer(0)]*N

def Tser(N):
    out = [sp.Integer(0)]*(N+1)
    if N >= 1: out[1] = sp.Integer(1)
    return out

def powr(a, n):
    N = len(a)-1
    out = const(1, N)
    for _ in range(n): out = mul(out, a)
    return out

def Y_series(N):
    """Y = T(1 + sY + pY^2)"""
    Y = [sp.Integer(0)]*(N+1)
    for it in range(N+2):
        rhs = add(add(const(1, N), smul(s, Y)), smul(p, mul(Y, Y)))
        Y = mul(Tser(N), rhs)
    return Y

def q_series(N):
    Y = Y_series(N)
    return sub(sub(const(1, N), smul(s, Tser(N))), smul(2*p, mul(Tser(N), Y)))

def shift_down(a, k=1):
    """divide by T^k (requires first k coeffs zero)"""
    for i in range(k):
        assert sp.expand(a[i]) == 0, ("not divisible by T", i, a[i])
    N = len(a)-1
    return a[k:] + [sp.Integer(0)]*k

def wdeg_parts(f):
    """split poly in s,p by u-weight (deg s = 1, deg p = 2) -> dict w -> part"""
    f = sp.expand(f)
    P = sp.Poly(f, s, p)
    out = {}
    for (i, j), c in zip(P.monoms(), P.coeffs()):
        w = i + 2*j
        out[w] = sp.expand(out.get(w, 0) + c*s**i*p**j)
    return out
