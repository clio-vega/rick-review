"""Independent construction of Rick's F_P at u_3 = 0 and u_3 = -1, from the
Day-131/Day-148 DEFINITIONS ONLY (T umbral map, Psi = T(fV)/V, P_b = phi(Psi_b),
F_P = sum_b P_b T^b/b!).  Clio, 2026-09-06 c2 peer review.

Note phi: u_i -> -u_i acts on ALL THREE variables, so
    P_b|_{u_3 = c}  =  Psi_b(-u_1, -u_2, -c).
Hence F_{-1} needs Psi_b evaluated at u_3 = +1.
"""
import sympy as sp
from sympy import expand, Poly, Rational

u1, u2, u3 = sp.symbols('u1 u2 u3')
s, p = sp.symbols('s p')          # s = E_1 = u1+u2, p = E_2 = u1 u2  (at u3 = 0 level)
T = sp.symbols('T')

e2_3 = u1*u2 + u1*u3 + u2*u3
V3 = sp.expand((u1-u2)*(u1-u3)*(u2-u3))

def ff(x, n):
    r = sp.Integer(1)
    for k in range(n):
        r *= (x - k)
    return r

def Psi_at_u3(b, u3val):
    """Psi(e_2^b) evaluated at u_3 = u3val, as a polynomial in u1,u2."""
    f = sp.expand(e2_3**b * V3)
    P = Poly(f, u1, u2, u3)
    out = sp.Integer(0)
    for mono, c in zip(P.monoms(), P.coeffs()):
        a1, a2, a3 = mono
        out += c * ff(u1, a1) * ff(u2, a2) * ff(sp.Integer(u3val), a3)
    out = sp.expand(out)
    Vc = sp.expand(V3.subs(u3, u3val))
    quo = sp.cancel(sp.together(out / Vc))
    quo = sp.expand(quo)
    # must be a polynomial
    assert sp.simplify(sp.expand(quo*Vc - out)) == 0
    return quo

def to_sp(f):
    """symmetric polynomial in u1,u2  ->  polynomial in s,p"""
    from sympy.polys.polyfuncs import symmetrize
    sym, rem, _ = symmetrize(sp.expand(f), [u1, u2], formal=True)
    assert sp.expand(rem) == 0, ("not symmetric", rem)
    s1, s2 = sp.symbols('s1 s2')
    return sp.expand(sym.subs({s1: s, s2: p}))

def P_coeffs(u3val, N):
    """[P_0, ..., P_N] at u_3 = u3val, in s,p."""
    out = []
    for b in range(N+1):
        psi = Psi_at_u3(b, -u3val)          # phi negates u_3 too
        Pb = sp.expand(psi.subs({u1: -u1, u2: -u2}, simultaneous=True))
        out.append(to_sp(Pb))
    return out

def FP_series(u3val, N):
    """coefficients c_k = P_k / k! of F_P|_{u3=u3val}, k = 0..N"""
    return [sp.expand(P / sp.factorial(k)) for k, P in enumerate(P_coeffs(u3val, N))]

if __name__ == '__main__':
    import sys
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    print("=== F_0 = F_P|_{u3=0} from the definition ===")
    c0 = FP_series(0, N)
    for k, c in enumerate(c0):
        print(f"  c_{k} =", sp.factor(c))
    print("\n  Rick's Day-158 claim: c_k = prod_{j=1}^k (p + j s + j^2)/k!")
    for k in range(N+1):
        pred = sp.expand(sp.prod([p + j*s + j**2 for j in range(1, k+1)])/sp.factorial(k))
        ok = sp.expand(pred - c0[k]) == 0
        print(f"   k={k}: {'MATCH' if ok else 'MISMATCH ' + str(sp.expand(pred-c0[k]))}")

    print("\n=== F_{-1} = F_P|_{u3=-1} from the definition ===")
    cm = FP_series(-1, N)
    for k, c in enumerate(cm):
        print(f"  c_{k} =", sp.factor(c))
