"""(a) (SC) OUT of Rick's tested range: r=3, and n=8.
   (b) Is the cancellation in Rick's key lemma (§3.3) a REAL cancellation,
       or is M_l(f) simply too small to reach 2r+l anyway?  A vanishing that
       had nothing to cancel would be degenerate evidence."""
import sympy as sp
from sympy.polys.polyfuncs import symmetrize
from itertools import combinations
v1,v2,v3=sp.symbols('v1 v2 v3'); E1,E2,E3=sp.symbols('E1 E2 E3')
def esym(vec,k): return sp.expand(sum(sp.prod(c) for c in combinations(vec,k))) if k>0 else sp.Integer(1)
def to_E(expr):
    sym,rem,_=symmetrize(sp.expand(expr),[v1,v2,v3],formal=True)
    assert sp.simplify(rem)==0
    s1,s2,s3=sp.symbols('s1 s2 s3')
    return sp.expand(sp.sympify(sym).subs({s1:E1,s2:E2,s3:E3}))
def rho_parts(e):
    p=sp.Poly(sp.expand(e),E1,E2,E3); d={}
    for m,c in zip(p.monoms(),p.coeffs()):
        if c==0: continue
        d.setdefault(m[0]+m[1]+2*m[2],[]).append((m,c))
    return d
def rho_of(e):
    d=rho_parts(e); return max(d) if d else -1
def T(n,r,mpp):
    U=[v1,v2,v3]+[sp.Integer(0)]*(n-3); e3=esym(U,3); tot=0
    for i in range(n):
        for j in range(i+1,n):
            U2=list(U); U2[i]+=1; U2[j]+=1
            f1,f2,f3=esym(U2,1),esym(U2,2),esym(U2,3)
            tot+=(U[i]+U[j]+1)*sp.expand(f3-e3)**r*mpp(f1,f2,f3)
    return sp.expand(tot)

print("=== (a) OUT-OF-SAMPLE (SC):  r=3 at n=5,6 ; and n=8 at r=1,2 ===")
cases=[(5,3,"1",lambda a,b,c:sp.Integer(1),0),(5,3,"E1",lambda a,b,c:a,1),
       (5,3,"E3",lambda a,b,c:c,2),(6,3,"1",lambda a,b,c:sp.Integer(1),0),
       (6,3,"E2",lambda a,b,c:b,1),
       (8,1,"1",lambda a,b,c:sp.Integer(1),0),(8,1,"E3",lambda a,b,c:c,2),
       (8,1,"E2*E3",lambda a,b,c:b*c,3),(8,2,"1",lambda a,b,c:sp.Integer(1),0),
       (8,2,"E1*E3",lambda a,b,c:a*c,3)]
bad=[]
for n,r,nm,f,rm in cases:
    rr=rho_of(to_E(T(n,r,f))); bd=2*r+rm
    if rr>bd: bad.append((n,r,nm,rr,bd))
    print("  n=%d r=%d m''=%-7s rho(m'')=%d bound=%2d actual=%2d  %s%s"
          %(n,r,nm,rm,bd,rr,"OK" if rr<=bd else "*** VIOLATED ***",
            " (tight)" if rr==bd else ""))
print("  violations:", bad if bad else "NONE")

print()
print("=== (b) is Rick's §3.3 vanishing a REAL cancellation? ===")
print("    M_l(f) = sum_i u_i^l (A - B u_i + u_i^2)^r,  A=2E2+E1, B=E1+1.")
print("    Rick proves the rho = 2r+l component vanishes.  Check that M_l(f)")
print("    genuinely HAS mass just below that level (else nothing was cancelled),")
print("    and that the individual summands DO reach 2r+l before summing.")
for n in (6,):
    U=[v1,v2,v3]+[sp.Integer(0)]*(n-3)
    e1,e2,e3=esym(U,1),esym(U,2),esym(U,3)
    A=2*e2+e1; B=e1+1
    for r in (1,2,3):
        for l in (0,1,2):
            M=sp.expand(sum(U[i]**l*(A-B*U[i]+U[i]**2)**r for i in range(n)))
            ME=to_E(M); parts=rho_parts(ME)
            top=2*r+l
            has_top = top in parts
            below   = (top-1) in parts
            # one individual summand, un-summed, to show the level is populated
            single=to_E(sp.expand(U[0]**l*(A-B*U[0]+U[0]**2)**r))
            sp_parts=rho_parts(single)
            print("    r=%d l=%d : rho(M_l)=%2d ; level %d present in SUM: %-5s ;"
                  " level %d present: %-5s ; single summand reaches level %d: %s"
                  %(r,l,rho_of(ME),top,has_top,top-1,below,top,top in sp_parts))
