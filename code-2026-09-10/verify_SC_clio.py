"""Independent check of Rick's sub-claim (SC), Day 181.

(SC)   rho( T^{X,r}(m'') mod E_{>=4} )  <=  2r + rho(m'')
       T^{X,r}(m'') = sum_{i<j} (u_i+u_j+1) X_ij^r m''|_ij,
       X_ij = E_3|_ij - E_3,  m''|_ij(u) = m''(u+e_i+e_j),  rho(E_k)=ceil(k/2).

KEY POINT (mine, not Rick's): "mod E_{>=4}" is the ring map killing e_4,...,e_n,
and that map is realised by the SUBSTITUTION u = (v1,v2,v3,0,...,0), because at
such a point e_k(u)=0 for k>=4 while e_1,e_2,e_3 stay algebraically independent.
So I never need a symmetric-function package: evaluate everything at that point
and expand the (3-variable symmetric) answer in e_1,e_2,e_3.

This shares no code and no method with Rick's verify_SC.py.
"""
import sympy as sp
from sympy.polys.polyfuncs import symmetrize

v1,v2,v3 = sp.symbols('v1 v2 v3')
E1,E2,E3 = sp.symbols('E1 E2 E3')

def esym(vec,k):
    from itertools import combinations
    return sp.expand(sum(sp.prod(c) for c in combinations(vec,k))) if k>0 else sp.Integer(1)

def rho_of(expr_in_E):
    """max over monomials E1^c1 E2^c2 E3^c3 of c1+c2+2c3."""
    p = sp.Poly(sp.expand(expr_in_E), E1,E2,E3)
    best = None
    for (c1,c2,c3),coeff in zip(p.monoms(), p.coeffs()):
        if sp.simplify(coeff)==0: continue
        w = c1+c2+2*c3
        best = w if best is None else max(best,w)
    return -1 if best is None else best   # -1 means the whole thing is 0

def to_E(expr):
    """expr symmetric in v1,v2,v3  ->  polynomial in E1,E2,E3."""
    sym, rem, _ = symmetrize(sp.expand(expr), [v1,v2,v3], formal=True)
    assert sp.simplify(rem)==0, "not symmetric! remainder=%s"%rem
    s1,s2,s3 = sp.symbols('s1 s2 s3')
    return sp.expand(sp.sympify(sym).subs({s1:E1,s2:E2,s3:E3}))

def T(n, r, mpp):
    """mpp: callable (E1v,E2v,E3v)->expr.  Returns T^{X,r}(m'') at the reduced point."""
    U = [v1,v2,v3]+[sp.Integer(0)]*(n-3)
    e1,e2,e3 = esym(U,1),esym(U,2),esym(U,3)
    tot = sp.Integer(0)
    for i in range(n):
        for j in range(i+1,n):
            U2 = list(U); U2[i]=U2[i]+1; U2[j]=U2[j]+1
            f1,f2,f3 = esym(U2,1),esym(U2,2),esym(U2,3)
            X = sp.expand(f3-e3)
            tot += (U[i]+U[j]+1)*X**r*mpp(f1,f2,f3)
    return sp.expand(tot)

# --- sanity: Rick's closed forms for E_2|_ij and X_ij, re-derived here -------
print("=== re-derivation of Rick's two closed forms (n=6) ===")
n=6; U=[v1,v2,v3]+[sp.Integer(0)]*(n-3)
e1,e2,e3=esym(U,1),esym(U,2),esym(U,3)
for (i,j) in [(0,1),(0,3),(3,4)]:
    U2=list(U); U2[i]+=1; U2[j]+=1
    f2,f3=esym(U2,2),esym(U2,3)
    claimed_E2 = e2+2*e1+1-(U[i]+U[j])
    claimed_X  = (2*e2+e1)-(U[i]+U[j])*(e1+1)+(U[i]**2+U[j]**2)
    print("  pair(%d,%d): E2|ij matches Rick: %s ; X_ij matches Rick: %s"
          % (i,j, sp.simplify(f2-claimed_E2)==0, sp.simplify(f3-e3-claimed_X)==0))

MS = [("1",       lambda a,b,c: sp.Integer(1),  0),
      ("E1",      lambda a,b,c: a,              1),
      ("E2",      lambda a,b,c: b,              1),
      ("E3",      lambda a,b,c: c,              2),
      ("E1*E3",   lambda a,b,c: a*c,            3),
      ("E2*E3",   lambda a,b,c: b*c,            3),
      ("E3**2",   lambda a,b,c: c**2,           4),
      ("E1**2*E3",lambda a,b,c: a**2*c,         4),
      ("E2**2",   lambda a,b,c: b**2,           2),
      ("E1*E2",   lambda a,b,c: a*b,            2),
      ("E3**3",   lambda a,b,c: c**3,           6)]

print()
print("=== (SC):  rho(T^{X,r}(m'') mod E>=4)  <=  2r + rho(m'') ? ===")
print(" n  r  m''        rho(m'')  bound  actual   verdict")
fails=[]
for n in (5,6,7):
    for r in (1,2):
        for nm,f,rm in MS:
            if n==7 and (r>1 or nm not in ("1","E1","E2","E3","E1*E3")): continue
            if r==2 and nm in ("E3**3",): continue
            res = T(n,r,f)
            resE = to_E(res)
            rr = rho_of(resE)
            bound = 2*r+rm
            ok = (rr<=bound)
            if not ok: fails.append((n,r,nm,rr,bound))
            print(" %d  %d  %-9s   %2d      %2d     %2d    %s%s"
                  % (n,r,nm,rm,bound,rr,"OK" if ok else "*** VIOLATED ***",
                     "  (=bound, tight)" if rr==bound else ("  (slack %d)"%(bound-rr) if ok else "")))
print()
print("violations:", fails if fails else "NONE")
