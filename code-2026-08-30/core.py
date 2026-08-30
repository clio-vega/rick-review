"""Independent implementation of Rick's Day-131 objects, from the DEFINITIONS ONLY.
Written without consulting his scripts (which I do not have).  Clio, 2026-08-30."""
import sympy as sp
from sympy import Rational, expand, symbols, Poly, factorial

u1,u2,u3 = symbols('u1 u2 u3')
U = (u1,u2,u3)
E1s,E2s,E3s = symbols('E1 E2 E3')
Tv = symbols('T')

e1 = u1+u2+u3
e2 = u1*u2+u1*u3+u2*u3
e3 = u1*u2*u3
V  = expand((u1-u2)*(u1-u3)*(u2-u3))

def ff(x,n):
    """falling factorial (x)_n = x(x-1)...(x-n+1)"""
    r = sp.Integer(1)
    for k in range(n):
        r *= (x-k)
    return r

def Tmap(f):
    """T: u_i^n -> (u_i)_n, per variable, extended linearly."""
    f = sp.expand(f)
    p = sp.Poly(f, u1,u2,u3)
    out = sp.Integer(0)
    for mono, c in zip(p.monoms(), p.coeffs()):
        out += c*ff(u1,mono[0])*ff(u2,mono[1])*ff(u3,mono[2])
    return sp.expand(out)

def Psi_u(f):
    """Psi(f) = T(f V)/V, returned as an expanded polynomial in u."""
    q = sp.cancel(sp.together(Tmap(sp.expand(f*V))/V))
    return sp.expand(q)

def D(i,f):
    return sp.expand(U[i]*sp.diff(f,U[i]))

def sigma(f):
    """simultaneous shift u_i -> u_i - 1"""
    return sp.expand(f.subs({u1:u1-1,u2:u2-1,u3:u3-1}, simultaneous=True))

# --- symmetric -> E-basis -----------------------------------------------------
def to_E(f):
    """Express a symmetric polynomial in u as a polynomial in E1,E2,E3.
       Uses sympy's symmetrize."""
    from sympy.polys.polyfuncs import symmetrize
    sym, rem, _ = symmetrize(sp.expand(f), [u1,u2,u3], formal=True)
    assert sp.expand(rem) == 0, ("not symmetric", rem)
    s1,s2,s3 = sp.symbols('s1 s2 s3')
    return sp.expand(sym.subs({s1:E1s,s2:E2s,s3:E3s}))

def from_E(P):
    return sp.expand(P.subs({E1s:e1,E2s:e2,E3s:e3}, simultaneous=True))

# --- (1,1,2) weight -----------------------------------------------------------
def weight_parts(P):
    """dict w -> homogeneous-in-weight part of P in Q[E1,E2,E3]."""
    P = sp.expand(P)
    p = sp.Poly(P, E1s,E2s,E3s)
    d = {}
    for mono,c in zip(p.monoms(), p.coeffs()):
        a,b,cc = mono
        w = a+b+2*cc
        d[w] = d.get(w,0) + c*E1s**a*E2s**b*E3s**cc
    return {k:sp.expand(v) for k,v in d.items()}

def wmax(P):
    P = sp.expand(P)
    if P == 0: return -sp.oo
    return max(weight_parts(P))

def top(P):
    wp = weight_parts(P)
    if not wp: return sp.Integer(0)
    return wp[max(wp)]

def wslice(P,w):
    return weight_parts(P).get(w, sp.Integer(0))

def sigma_top(P):
    """ring endomorphism E1->E1, E2->E2-2E1, E3->E3"""
    return sp.expand(P.subs({E2s:E2s-2*E1s}, simultaneous=True))

def sigma_E(P):
    """full sigma acting on E-basis: E1->E1-3, E2->E2-2E1+3, E3->E3-E2+E1-1"""
    return sp.expand(P.subs({E1s:E1s-3, E2s:E2s-2*E1s+3, E3s:E3s-E2s+E1s-1},
                            simultaneous=True))
