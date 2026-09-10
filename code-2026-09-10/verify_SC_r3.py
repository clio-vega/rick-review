"""Rick's numerics for (SC) itself only ran r in {1,2}.  At r=3 my check shows
SLACK.  Confirm it is real (not a small-n artefact) and locate where it starts."""
import sympy as sp
from sympy.polys.polyfuncs import symmetrize
from itertools import combinations
v1,v2,v3=sp.symbols('v1 v2 v3'); E1,E2,E3=sp.symbols('E1 E2 E3')
def esym(v,k): return sp.expand(sum(sp.prod(c) for c in combinations(v,k))) if k>0 else sp.Integer(1)
def to_E(e):
    s,rem,_=symmetrize(sp.expand(e),[v1,v2,v3],formal=True); assert sp.simplify(rem)==0
    a,b,c=sp.symbols('s1 s2 s3'); return sp.expand(sp.sympify(s).subs({a:E1,b:E2,c:E3}))
def rho_of(e):
    p=sp.Poly(sp.expand(e),E1,E2,E3); w=[m[0]+m[1]+2*m[2] for m,c in zip(p.monoms(),p.coeffs()) if c!=0]
    return max(w) if w else -1
def T(n,r,mpp):
    U=[v1,v2,v3]+[sp.Integer(0)]*(n-3); e3=esym(U,3); tot=0
    for i in range(n):
        for j in range(i+1,n):
            U2=list(U); U2[i]+=1; U2[j]+=1
            f1,f2,f3=esym(U2,1),esym(U2,2),esym(U2,3)
            tot+=(U[i]+U[j]+1)*sp.expand(f3-e3)**r*mpp(f1,f2,f3)
    return sp.expand(tot)

# instrument calibration: rho(p_r) must be r (Sub-lemma A), incl. large r
print("=== calibration: Sub-lemma A, rho(p_r) = r, top term E1^r ===")
U=[v1,v2,v3]
for r in (2,3,5,7,9):
    pr=to_E(sp.expand(sum(x**r for x in U)))
    print("   r=%d: rho(p_r)=%d  coeff of E1^r = %s" % (r,rho_of(pr), sp.Poly(pr,E1,E2,E3).coeff_monomial(E1**r)))

print()
print("=== rho(T^{X,r}(1)) vs the (SC) bound 2r, across r and n ===")
print("   n    r   bound   actual   slack")
for n in (5,6,7,8,9):
    for r in (1,2,3,4):
        if r==4 and n>7: continue
        rr=rho_of(to_E(T(n,r,lambda a,b,c:sp.Integer(1))))
        print("   %d    %d     %2d      %2d      %d %s"%(n,r,2*r,rr,2*r-rr,
              "<- tight" if rr==2*r else ""))
