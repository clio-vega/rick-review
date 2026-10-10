"""
Independent spot-check of Finding 1 / Theorem 6.3 (FPSAC draft @ e44e29f):
is the printed right-hand side of Thm 6.3 the HALL pairing <T_a g, p_x p_y>
or the HL pairing <.,.>_t ?

Everything is built from the printed definitions:
  Lemma 3.9  T_k f := sum_{|A|=k} c_A X_A f(X_A),  f in Lambda_k
  Thm 6.3    Phi_a(g;x,y) := <T_a g, p_x p_y>
  Notation   <p_lam,p_mu> = delta z_lam  (Hall);
             <p_lam,p_mu>_t = delta z_lam prod_i (1-t^{lam_i})^{-1}  (HL)
"""
import sys
sys.path.insert(0, '/home/clio/projects/reviews/code-20261010')
import star
from star import *
from symfun import partitions
from fractions import Fraction
from itertools import combinations
import sympy

t = sympy.Symbol('t')
star.set_t(None)   # symbolic t

def T_k(f_on_A, k, N):
    """T_k f = sum_{|A|=k} c_A X_A f(x_A).  f_on_A(A) must return the poly f
    evaluated at the variables indexed by A, as a poly in N vars."""
    V = vandermonde(N)
    total = p_zero()
    for A in combinations(range(N), k):
        As = set(A)
        num = p_one(N)
        for i in A:
            for j in range(N):
                if j in As: continue
                num = p_mul(num, p_add(p_var(i, N), p_var(j, N, minus_t_coeff())))
        sign = 1; cof = p_one(N)
        for i in range(N):
            for j in range(i+1, N):
                ini, inj = i in As, j in As
                if ini and not inj: pass
                elif inj and not ini: sign = -sign
                else: cof = p_mul(cof, p_sub(p_var(i, N), p_var(j, N)))
        XA = p_one(N)
        for i in A: XA = p_mul(XA, p_var(i, N))
        term = p_mul(p_mul(num, cof), p_mul(XA, f_on_A(A)))
        if sign < 0: term = p_neg(term)
        total = p_add(total, term)
    return p_divide_exact(total, V)

def power_sum(r, N):
    out = {}
    for i in range(N):
        a = [0]*N; a[i] = r
        out[tuple(a)] = c_const(1)
    return out

def p_rho(rho, N):
    P = p_one(N)
    for r in rho: P = p_mul(P, power_sum(r, N))
    return P

def z_lambda(rho):
    from collections import Counter
    import math
    cnt = Counter(rho); z = 1
    for part, m in cnt.items(): z *= (part**m) * math.factorial(m)
    return z

def tosym(c):
    return sum(sympy.Rational(v.numerator, v.denominator)*t**e for e, v in c.items()) if c else sympy.Integer(0)

def mono(P, mu, N):
    return tosym(P.get(tuple(list(mu)+[0]*(N-len(mu))), {}))

def p_expand(P, n, N):
    parts = list(partitions(n))
    M = sympy.zeros(len(parts), len(parts)); rhs = sympy.zeros(len(parts), 1)
    prs = {r: p_rho(r, N) for r in parts}
    for i, mu in enumerate(parts):
        for j, r in enumerate(parts): M[i, j] = mono(prs[r], mu, N)
        rhs[i] = mono(P, mu, N)
    sol = M.solve(rhs)
    return {parts[j]: sympy.cancel(sol[j]) for j in range(len(parts))}

def printed_thm63(gfun, a, d, x, y):
    """RHS of printed Thm 6.3.  gfun(vars) -> sympy expr for g at those values."""
    n = a + d
    assert x + y == n
    w = sympy.Symbol('w')
    total = 0
    for A in range(1, a):
        B = a - A
        args = [t**i for i in range(A)] + [w*t**i for i in range(B)]
        GA = sympy.Poly(sympy.expand(gfun(args)), w)
        def Gk(k):
            if k < 0: return sympy.Integer(0)
            return GA.coeff_monomial(w**k) if k <= GA.degree() else sympy.Integer(0)
        inner = Gk(y-B)/((1-t**A)*(1-t**B))
        s2 = 0
        for m in range(1, y-B+1):
            s2 += (t**(-A*m) - t**(B*m)) * Gk(y-B-m)
        inner += s2/(1-t**a)
        total += t**(-A*B) * inner
    gdiag = gfun([t**i for i in range(a)])
    total -= gdiag/(1-t**a) * sum(t**(-j*y) for j in range(a))
    return sympy.cancel(sympy.together((-1)**a * (1-t**x)*(1-t**y) * total))

def run(a, bc, x, y, N=None):
    b, c = bc
    d = b + c; n = a + d
    N = N or n
    # g = p_b p_c  in a variables
    def f_on_A(A):
        P = p_one(N)
        for r in (b, c):
            s = {}
            for i in A:
                al = [0]*N; al[i] = r
                s[tuple(al)] = c_const(1)
            P = p_mul(P, s)
        return P
    Tg = T_k(f_on_A, a, N)
    exp = p_expand(Tg, n, N)
    mu = tuple(sorted((x, y), reverse=True))
    coeff = exp[mu]
    hall = sympy.cancel(coeff * z_lambda(mu))
    hl   = sympy.cancel(hall / ((1-t**x)*(1-t**y)))
    def gfun(args):
        return sum(v**b for v in args) * sum(v**c for v in args)
    printed = printed_thm63(gfun, a, d, x, y)
    dh  = sympy.simplify(printed - hall)
    dhl = sympy.simplify(printed - hl)
    print(f"  a={a} g=p_{b}p_{c} (x,y)=({x},{y}) | printed-Hall = {dh} | printed-HL = {sympy.factor(dhl)}")
    return dh == 0, dhl == 0

if __name__ == '__main__':
    cases = [(2,(1,1),3,1), (2,(1,1),2,2), (2,(2,1),4,1), (2,(2,1),3,2), (3,(1,1),4,1), (2,(2,2),5,1)]
    hok = hlok = 0
    for a, bc, x, y in cases:
        try:
            h, l = run(a, bc, x, y)
            hok += h; hlok += l
        except Exception as e:
            print(f"  a={a} {bc} ({x},{y}) ERROR {type(e).__name__}: {e}")
    print(f"\n  Hall matches printed Thm 6.3 : {hok}/{len(cases)}")
    print(f"  HL   matches printed Thm 6.3 : {hlok}/{len(cases)}")
