"""Rick's side finding, tested against the RIGHT object: the raw Thm 2.5 (thm:2pt)
formula, not the closed form (which the paper restricts to y <= x).

thm:2pt, a=2 (A=B=1):
 Phi_2(g;x,y) = (1-t^x)(1-t^y) { t^{-1}[ G_{1,y-1}/(1-t)^2
                 + (1/(1-t^2)) sum_{m>=1}(t^{-m}-t^m) G_{1,y-1-m} ]
                 - (g(1,t)/(1-t^2))(1 + t^{-y}) }
 dictionary: Phi_2(P_rho;x,y) = (1-t^x)(1-t^y) X^lambda_{(x,y)}(t)/b_lambda(t), lambda = rho + 1^2
"""
import itertools, functools
import engine as E
from sympy import symbols, cancel, expand, Integer, factor, Poly, simplify
t=E.t; w=symbols('w')
exec(open('t7_green.py').read().split("print(\"=== (a)")[0])

def G1coeffs(rho):
    g=cancel(expand(HL2(rho).subs({X2[0]:1,X2[1]:w},simultaneous=True)))
    P=Poly(g,w)
    return lambda k: (Integer(0) if k<0 else cancel(P.coeff_monomial(w**k)))

def b_lam(lam):
    out=Integer(1)
    for v in set(lam):
        mv=sum(1 for p in lam if p==v)
        for i in range(1,mv+1): out*=(1-t**i)
    return out

def Phi2_raw(rho,x,y):
    G=G1coeffs(rho)
    n=sum(rho)+2
    g1t=cancel(HL2(rho).subs({X2[0]:1,X2[1]:t},simultaneous=True))
    msum=0
    for m in range(1, n+3):
        c=G(y-1-m)
        if c!=0: msum+=(t**(-m)-t**m)*c
    bracket = t**(-1)*( G(y-1)/(1-t)**2 + msum/(1-t**2) ) - g1t/(1-t**2)*(1+t**(-y))
    return cancel((1-t**x)*(1-t**y)*bracket)

def X_from_thm25(rho,x,y):
    lam=tuple(sorted((rho[0]+1, (rho[1] if len(rho)>1 else 0)+1),reverse=True))
    return cancel(Phi2_raw(rho,x,y)*b_lam(lam)/((1-t**x)*(1-t**y)))

print("=== raw Thm 2.5 vs independent Green polynomial, BOTH orderings of (x,y) ===")
for region,pred in [("y < x", lambda x,y: y<x), ("y = x", lambda x,y: y==x), ("y > x", lambda x,y: y>x)]:
    ok=bad=0; fails=[]
    for n in range(2,11):
        for l2 in range(1,n//2+1):
            l1=n-l2
            if l1<l2: continue
            rho=(l1-1,l2-1)
            for y in range(1,n):
                x=n-y
                if not pred(x,y): continue
                got=cancel(X_from_thm25(rho,x,y))
                want=cancel(green((l1,l2),(x,y)))
                if cancel(expand(got-want))==0: ok+=1
                else:
                    bad+=1
                    if len(fails)<3: fails.append(((l1,l2),(x,y),factor(got),factor(want)))
    print(f"  {region}: {ok} of {ok+bad} pass, {bad} fail")
    for f in fails: print("      FAIL lam=%s (x,y)=%s thm2.5=%s green=%s"%f)

print()
print("=== control: drop the j-sum (the step he says breaks 48 rows) -- MUST fail ===")
def Phi2_nojsum(rho,x,y):
    G=G1coeffs(rho)
    g1t=cancel(HL2(rho).subs({X2[0]:1,X2[1]:t},simultaneous=True))
    bracket = t**(-1)*( G(y-1)/(1-t)**2 ) - g1t/(1-t**2)*(1+t**(-y))
    return cancel((1-t**x)*(1-t**y)*bracket)
ok=bad=0
for n in range(2,11):
    for l2 in range(1,n//2+1):
        l1=n-l2
        if l1<l2: continue
        rho=(l1-1,l2-1)
        for y in range(1,n):
            x=n-y
            lam=(l1,l2)
            got=cancel(Phi2_nojsum(rho,x,y)*b_lam(lam)/((1-t**x)*(1-t**y)))
            if cancel(expand(got-green(lam,(x,y))))==0: ok+=1
            else: bad+=1
print(f"  dropping the j-sum: {bad} of {ok+bad} FAIL (ok={ok})")

print()
print("=== ex:tworow parity hypothesis: is 'lambda_2 >= 3 ODD' necessary? ===")
for l2 in [2,3,4,5]:
    l1=l2+2; val=cancel(green((l1,l2),(l1,l2)))
    print(f"  lambda=({l1},{l2}) diag: X={factor(val)}  t=-1: {cancel(val.subs(t,-1))}  t=0: {cancel(val.subs(t,0))}"
          f"   sign change in (-1,0): {cancel(val.subs(t,-1))*cancel(val.subs(t,0))<0}")

print()
print("=== how many of the 155 rows even HAVE a non-empty j-sum? ===")
tot=nonempty=0
for n in range(2,11):
    for l2 in range(1,n//2+1):
        l1=n-l2
        if l1<l2: continue
        for y in range(1,n):
            x=n-y; tot+=1
            rho2=l2-1
            if y-1-rho2>=1: nonempty+=1   # j-sum non-empty  <=>  y > lambda_2
print(f"  total rows enumerated: {tot}")
print(f"  rows with a non-empty j-sum (y > lambda_2): {nonempty}")
print(f"  rows where dropping it CANNOT change anything: {tot-nonempty}")
