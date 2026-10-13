"""
TEST 5: Section 9 (sec:box) -- Box Complement, Column Lemma, Pieri-all-s,
plethystic linear coefficient -- plus the printed Lead example of cor:column
and thm:G.
"""
import sys, time, sympy
sys.path.insert(0,'/home/clio/projects/reviews/code-2026-10-13')
from t3_star import (FF,s,t,ONE,ZERO,partitions,conj,nstat,qint,qfact,
                     star_lambda_M1,star_lambda_M2)
ss,tt=sympy.symbols('s t')
def sh(c): return sympy.factor(sympy.simplify(c.as_expr()))

CACHE={}
def cstar(lam,engine='M2'):
    lam=tuple(p for p in lam if p>0)
    key=(lam,engine)
    if key in CACHE: return CACHE[key]
    f = star_lambda_M2 if engine=='M2' else star_lambda_M1
    CACHE[key]=f(lam)
    return CACHE[key]

def comp(N,ell,lam):
    lam=list(lam)+[0]*(ell-len(lam))
    v=sorted([N-a for a in lam],reverse=True)
    return tuple(p for p in v if p>0)   # partitions are keyed WITHOUT zero parts

print("="*74)
print("CHECK 5.1  thm:box   c_{N^l-lam, N^l-mu} = s^{N C(l,2) - (l-1)|lam|} c_{lam,mu}")
cases=[(2,2,(1,0)),(2,3,(1,1)),(3,2,(1,1,0)),(3,2,(1,0,0)),(2,3,(1,0)),
       (3,2,(2,1,0)),(2,4,(2,1)),(2,3,(2,1))]
ok=tot=0; t0=time.time()
for ell,N,lam in cases:
    lamc=comp(N,ell,lam)
    if sum(lamc)>6: print("  skip (degree %d too big): l=%d N=%d lam=%s"%(sum(lamc),ell,N,lam)); continue
    A=cstar(lam); B=cstar(lamc)
    sig=N*(ell*(ell-1)//2)-(ell-1)*sum(lam)
    for mu,c in A.items():
        muc=comp(N,ell,mu)
        if max(mu)>N or len(mu)>ell:
            print("   (mu=%s outside the box, skipped)"%(mu,)); continue
        got=B.get(muc,ZERO)
        pred=c*s**sig
        tot+=1
        if got==pred: ok+=1
        else: print("   FAIL l=%d N=%d lam=%s mu=%s: c_{%s,%s}=%s  vs  s^%d c=%s"%(
            ell,N,lam,mu,lamc,muc,sh(got),sig,sh(pred)))
    print("  l=%d N=%d  lam=%s -> %s   sigma=%d   (%.1fs)"%(ell,N,lam,lamc,sig,time.time()-t0))
print("  %d / %d (lam,mu) instances"%(ok,tot))

print()
print("="*74)
print("CHECK 5.2  cor:column   c_{lam+1^l, mu+1^l} = s^{C(l,2)} c_{lam,mu}")
ok=tot=0
for lam,ell in [((1,),1),((1,1),2),((2,1),2),((1,0),2),((2,2),2),((1,1,1),3)]:
    lamp=tuple(a+1 for a in list(lam)+[0]*(ell-len(lam)))
    if sum(lamp)>6: print("  skip degree %d: lam=%s l=%d"%(sum(lamp),lam,ell)); continue
    A=cstar(lam); B=cstar(lamp)
    sig=ell*(ell-1)//2
    for mu,c in A.items():
        if len(mu)>ell: continue
        mup=tuple(a+1 for a in list(mu)+[0]*(ell-len(mu)))
        got=B.get(mup,ZERO); pred=c*s**sig
        tot+=1
        if got==pred: ok+=1
        else: print("   FAIL lam=%s l=%d mu=%s: got %s pred %s"%(lam,ell,mu,sh(got),sh(pred)))
    print("  lam=%s l=%d -> %s  sigma=%d"%(lam,ell,lamp,sig))
print("  %d / %d"%(ok,tot))

print()
print("="*74)
print("CHECK 5.3  cor:pieri   e_k * e_r = sum_y s^y C_{k-y,r-y} e_{k+r-y} e_y")
def pi_a(a,j):
    u=sympy.Symbol('u')
    f=1
    for mm in range(a): f*= (1+ss*u*tt**mm)/(1+u*tt**mm)
    return sympy.simplify(sympy.series(f,u,0,j+1).removeO().coeff(u,j))
def Ccal(a,b):
    if b==0 or a==0: return sympy.Integer(1)
    A=sum(tt**i for i in range(a)); AB=sum(tt**i for i in range(a+b))
    return sympy.simplify((-1)**b*AB/A*pi_a(a,b))
ok=tot=0
for k in range(1,4):
    for r in range(1,4):
        if k+r>6: continue
        A=cstar((k,r)) if k>=r else cstar((r,k))
        pred={}
        for y in range(0,min(k,r)+1):
            nu=tuple(sorted([k+r-y,y],reverse=True))
            nu=tuple(p for p in nu if p>0)
            pred[nu]=pred.get(nu,sympy.Integer(0))+ss**y*Ccal(k-y,r-y)
        for nu in set(list(A)+list(pred)):
            got=sympy.simplify(A.get(nu,ZERO).as_expr())
            pr=sympy.simplify(pred.get(nu,sympy.Integer(0)))
            tot+=1
            if sympy.simplify(got-pr)==0: ok+=1
            else: print("   FAIL k=%d r=%d nu=%s got %s pred %s"%(k,r,nu,got,pr))
print("  %d / %d coefficients, (k,r) with 1<=k,r<=3, k+r<=6"%(ok,tot))

print()
print("="*74)
print("CHECK 5.4  thm:lin   lin(e_k*G) = (-1)^d [k+d]/[k] G[(s-1)[k]_t],  p_r -> (s^r-1)[k]_{t^r}")
import itertools
def plethG(J,k):
    """G = e_{j1}..e_{jp};  apply the ring map p_r -> (s^r-1)[k]_{t^r} to G."""
    # e_j in p-basis then substitute
    def e_in_p(j):
        out={}
        for l in partitions(j):
            eps=(-1)**(j-len(l))
            import math
            z=1
            mm={}
            for p_ in l: mm[p_]=mm.get(p_,0)+1
            for v,c in mm.items(): z*= (v**c)*math.factorial(c)
            out[l]=sympy.Rational(eps,z)
        return out
    cur={():sympy.Integer(1)}
    for j in J:
        nxt={}
        for l1,c1 in cur.items():
            for l2,c2 in e_in_p(j).items():
                key=tuple(sorted(l1+l2,reverse=True))
                nxt[key]=nxt.get(key,0)+c1*c2
        cur=nxt
    tot=sympy.Integer(0)
    for l,c in cur.items():
        pr=c
        for r in l: pr*= (ss**r-1)*sum(tt**(r*i) for i in range(k))
        tot+=pr
    return sympy.simplify(tot)
from t3_star import E_k_M2
ok=tot=0
for k in range(1,4):
    for J in [(1,),(2,),(1,1),(3,),(2,1),(1,1,1)]:
        d=sum(J); n=k+d
        if n>6: continue
        # thm:lin is about e_k * G with G an ORDINARY product e_{j1}...e_{jp}
        A=E_k_M2({tuple(sorted(J,reverse=True)):ONE},k,d,n)
        got=sympy.simplify(A.get((n,),ZERO).as_expr())
        pred=sympy.simplify((-1)**d*sum(tt**i for i in range(k+d))/sum(tt**i for i in range(k))*plethG(J,k))
        tot+=1
        if sympy.simplify(sympy.together(got-pred))==0: ok+=1
        else: print("   FAIL k=%d J=%s  got %s  pred %s"%(k,J,sympy.factor(got),sympy.factor(pred)))
print("  %d / %d  (k,J) pairs with k+|J| <= 6"%(ok,tot))

print()
print("="*74)
print("CHECK 5.5  the printed Lead example of cor:column / thm:G")
print("  claim: (1,1,1)->(3), (2,2,2)->(3,3) and (2,2,2)->(4,1,1) all have lead [3]_t(t+2)")
def lead(lam,mu):
    A=cstar(lam); c=A.get(mu,ZERO)
    ex=sympy.expand(c.as_expr())
    ser=sympy.Poly(ex.subs(ss,1+sympy.Symbol('w')),sympy.Symbol('w'))
    co=ser.all_coeffs()[::-1]
    for i,cc in enumerate(co):
        if sympy.simplify(cc)!=0: return i, sympy.factor(sympy.simplify(cc))
    return None,0
target=sympy.factor(sympy.simplify(sum(tt**i for i in range(3))*(tt+2)))
print("  target [3]_t(t+2) =",sympy.expand(target))
for lam,mu in [((1,1,1),(3,)),((2,2,2),(3,3)),((2,2,2),(4,1,1))]:
    if sum(lam)>6: continue
    v,L=lead(lam,mu)
    good = sympy.simplify(sympy.expand(L)-sympy.expand(target))==0
    print("   %s -> %s :  val=%s  Lead=%s   %s"%(lam,mu,v,sympy.expand(L),"MATCH" if good else "DIFFERS"))
