"""Independent computation of Xi = top-u-weight layer of log F_P in THREE variables,
and of d^2/du_3^2 Xi |_{u_3=0}.  From the Day-131 definitions only.  Clio 2026-09-06 c2."""
import sympy as sp
from sympy import Poly

u1, u2, u3 = sp.symbols('u1 u2 u3')
s, p = sp.symbols('s p')
e2_3 = u1*u2 + u1*u3 + u2*u3
V3 = sp.expand((u1-u2)*(u1-u3)*(u2-u3))

def ff(x, n):
    r = sp.Integer(1)
    for k in range(n): r *= (x-k)
    return r

def Psi3(b):
    """Psi(e_2^b) as a polynomial in u1,u2,u3."""
    f = sp.expand(e2_3**b * V3)
    P = Poly(f, u1, u2, u3)
    out = sp.Integer(0)
    for mono, c in zip(P.monoms(), P.coeffs()):
        a1, a2, a3 = mono
        out += c*ff(u1, a1)*ff(u2, a2)*ff(u3, a3)
    quo = sp.cancel(sp.together(sp.expand(out)/V3))
    return sp.expand(quo)

def logFP_coeffs(N):
    """[T^n] log F_P, n = 0..N, as polynomials in u1,u2,u3 (P_b = phi(Psi_b))."""
    c = []
    for b in range(N+1):
        P = sp.expand(Psi3(b).subs({u1:-u1, u2:-u2, u3:-u3}, simultaneous=True))
        c.append(sp.expand(P/sp.factorial(b)))
    # log of the series c
    lg = [sp.Integer(0)]*(N+1)
    for n in range(1, N+1):
        acc = c[n]
        for k in range(1, n):
            acc -= sp.Rational(k, n)*lg[k]*c[n-k]
        lg[n] = sp.expand(acc)
    return lg

def top_layer(poly, deg):
    """homogeneous part of total degree `deg` in u1,u2,u3"""
    poly = sp.expand(poly)
    P = Poly(poly, u1, u2, u3)
    out = sp.Integer(0)
    for mono, c in zip(P.monoms(), P.coeffs()):
        if sum(mono) == deg:
            out += c*u1**mono[0]*u2**mono[1]*u3**mono[2]
    return sp.expand(out)

def to_sp(f):
    from sympy.polys.polyfuncs import symmetrize
    sym, rem, _ = symmetrize(sp.expand(f), [u1, u2], formal=True)
    assert sp.expand(rem) == 0, ("not symmetric in u1,u2", rem)
    s1, s2 = sp.symbols('s1 s2')
    return sp.expand(sym.subs({s1: s, s2: p}))

def d2_Xi_at_0(N):
    """[T^n] of  d^2/du_3^2 Xi |_{u_3=0},  n = 0..N, in s,p."""
    lg = logFP_coeffs(N)
    out = []
    for n in range(N+1):
        Xi_n = top_layer(lg[n], n+1) if n >= 1 else sp.Integer(0)
        d2 = sp.expand(sp.diff(Xi_n, u3, 2).subs(u3, 0))
        out.append(to_sp(d2))
    return out

if __name__ == '__main__':
    import sys, time
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    t0 = time.time()
    r = d2_Xi_at_0(N)
    for n, v in enumerate(r):
        print(f"[T^{n}] d^2_u3 Xi|_0 =", sp.factor(v))
    print(f"({time.time()-t0:.1f}s)")
