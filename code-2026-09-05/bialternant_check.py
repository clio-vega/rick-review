"""
Independent re-derivation of Psi(e_2^b) via the BIALTERNANT, not via term-by-term T^-.
Rationale: Psi(s_mu) = det[(u_i)_{mu_j+n-j}]/V = the factorial Schur function s*_mu.
So  Psi(e_2^b) = sum_mu c_mu s*_mu  where e_2^b = sum_mu c_mu s_mu  (Littlewood-Richardson).
If this reproduces the term-by-term T^- computation, both are right.
Clio, 2026-09-05.
"""
import sympy as sp
from sympy.polys.polyfuncs import symmetrize
from itertools import permutations

def falling(x, m):
    return sp.prod([x - j for j in range(m)]) if m > 0 else sp.Integer(1)

def V_of(u):
    n = len(u)
    return sp.expand(sp.prod([u[i]-u[j] for i in range(n) for j in range(i+1,n)]))

def star_schur(mu, u):
    """s*_mu = det[(u_i)_{mu_j + n - j}] / V"""
    n = len(u)
    mu = list(mu) + [0]*(n-len(mu))
    if len(mu) > n: return sp.Integer(0)
    alpha = [mu[j] + n - 1 - j for j in range(n)]
    M = sp.Matrix(n, n, lambda i, j: falling(u[i], alpha[j]))
    num = sp.expand(M.det())
    V = V_of(u)
    q, r = sp.div(sp.Poly(num, u[0]), sp.Poly(V, u[0]))
    assert r.is_zero, "V does not divide the bialternant"
    return sp.expand(q.as_expr()), alpha

def Psi_direct(f, u):
    n = len(u); V = V_of(u)
    P = sp.Poly(sp.expand(f)*V, *u)
    num = sp.expand(sum(c*sp.prod([falling(u[i], a[i]) for i in range(n)]) for a,c in P.terms()))
    q, r = sp.div(sp.Poly(num, u[0]), sp.Poly(V, u[0]))
    assert r.is_zero
    return sp.expand(q.as_expr())

def toE(poly, u, Es):
    if sp.expand(poly)==0: return sp.Integer(0)
    s, rem, _ = symmetrize(sp.expand(poly), list(u), formal=True)
    assert sp.expand(rem)==0
    return sp.expand(s.subs({sp.Symbol(f's{k}'): Es[k-1] for k in range(1,len(u)+1)}))

print("="*80)
print("A. Psi(s_mu) = s*_mu  (bialternant)  vs  Psi applied termwise to s_mu")
print("="*80)
for n in (3,4):
    u = sp.symbols(f'u1:{n+1}')
    for mu in [(1,1),(2,2),(2,1,1),(1,1,1,1)]:
        if len(mu) > n: continue
        sm, alpha = star_schur(mu, u)
        # ordinary Schur via bialternant, then Psi termwise
        nn=n; mul=list(mu)+[0]*(n-len(mu))
        A=[mul[j]+n-1-j for j in range(n)]
        Mo=sp.Matrix(n,n,lambda i,j: u[i]**A[j])
        q,r=sp.div(sp.Poly(sp.expand(Mo.det()),u[0]),sp.Poly(V_of(u),u[0])); assert r.is_zero
        s_ord=sp.expand(q.as_expr())
        direct=Psi_direct(s_ord,u)
        print(f"  n={n} mu={mu}: alpha={A}  agree={sp.expand(sm-direct)==0}")

print("\n"+"="*80)
print("B. e_2^2 = s_22 + s_211 + s_1111 (LR).  Check, then rebuild Psi(e_2^2).")
print("="*80)
for n in (3,4):
    u  = sp.symbols(f'u1:{n+1}')
    Es = sp.symbols(f'E1:{n+1}')
    e2 = sp.expand(sum(u[i]*u[j] for i in range(n) for j in range(i+1,n)))
    # ordinary Schur check
    def ord_schur(mu):
        mul=list(mu)+[0]*(n-len(mu))
        if len(mu)>n: return sp.Integer(0)
        A=[mul[j]+n-1-j for j in range(n)]
        Mo=sp.Matrix(n,n,lambda i,j: u[i]**A[j])
        q,r=sp.div(sp.Poly(sp.expand(Mo.det()),u[0]),sp.Poly(V_of(u),u[0])); assert r.is_zero
        return sp.expand(q.as_expr())
    lhs = sp.expand(e2**2)
    rhs = sp.expand(ord_schur((2,2))+ord_schur((2,1,1))+ord_schur((1,1,1,1)))
    print(f"  n={n}: e_2^2 = s22+s211+s1111 ? {sp.expand(lhs-rhs)==0}")
    tot = sp.Integer(0)
    for mu in [(2,2),(2,1,1),(1,1,1,1)]:
        if len(mu)>n: continue
        sm,_ = star_schur(mu,u); tot = sp.expand(tot+sm)
    direct = Psi_direct(sp.expand(e2**2), u)
    print(f"       sum of s*_mu == Psi(e_2^2) directly ? {sp.expand(tot-direct)==0}")
    print(f"       Psi(e_2^2)|_(n={n}) in E-basis = {toE(direct,u,Es)}")
