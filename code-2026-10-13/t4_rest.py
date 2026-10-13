import sys, time, sympy
sys.path.insert(0,'/home/clio/projects/reviews/code-2026-10-13')
import t3_star as S, t2_dmatrix as D
from t3_star import (FF,s,t,ONE,ZERO,partitions,conj,nstat,qint,qfact,
                     star_lambda_M1,star_lambda_M2,eY,expand_in_e,_scal,E_k_M2,e_lambda_poly)
ss,tt=sympy.symbols('s t')
NMAX=int(sys.argv[1]) if len(sys.argv)>1 else 5

print("="*74)
print("CHECK 4.1  Theorem H(1): E_k b_mu in  sum_nu Q[s,t] b_nu,  b_mu = s^{n(mu)} e_mu")
print("  equivalently  s^{n(nu)-n(mu)} | [e_nu] E_k e_mu  whenever n(nu) > n(mu).")
tot=ok=bites=0
for n in range(1,NMAX+1):
    for mu in partitions(n):
        co={mu:ONE}
        for k in range(1,NMAX+1-n+1):
            if k<1: continue
            m=n+k
            if m>7: continue
            out=E_k_M2(co,k,n,m)
            for nu,c in out.items():
                g=nstat(nu)-nstat(mu)
                tot+=1
                ex=sympy.expand(sympy.simplify(c.as_expr()*ss**(nstat(mu)-nstat(nu))))
                try:
                    sympy.Poly(ex,ss,tt); good=True
                except sympy.PolynomialError: good=False
                if good: ok+=1
                else: print("   H(1) FAIL  mu=%s k=%d nu=%s  coeff=%s"%(mu,k,nu,c.as_expr()))
                if g>0: bites+=1
print("  %d / %d  (nu,mu,k) triples;  of these %d have n(nu)>n(mu), where the claim BITES"%(ok,tot,bites))

print()
print("="*74)
print("CHECK 4.2  Theorem H(2):  phi o L_k = t^{-C(k,2)} e_k . phi,  phi(bbar_mu)=t^{-n(mu')}P_{mu'}(x;1/t)")
print("  P built by Gram-Schmidt (Test 2 mechanism b); e_k . P expanded back in the P-basis.")
FFt, tq = D.FF, D.t
def Pbasis(n,N,u):
    return D.HL_P(n,N,u)
ok2=tot2=0
cache={}
for n in range(1,min(NMAX,6)+1):
    for k in range(1,min(NMAX,6)+1-n+1):
        N=n+k
        if (n+k,N) not in cache: cache[(n+k,N)]=Pbasis(n+k,N,FFt.one/tq)
        if (n,N) not in cache: cache[(n,N)]=Pbasis(n,N,FFt.one/tq)
        Pbig,_=cache[(n+k,N)]; Psm,_=cache[(n,N)]
        for mu in partitions(n):
            # LHS: phi(L_k bbar_mu)
            vec=D.L_op({mu:FFt.one},k)
            lhs={}
            for nu,c in vec.items():
                key=D.conj(nu)
                lhs[key]=lhs.get(key,FFt.zero)+c*(FFt.one/tq**D.nstat(D.conj(nu)))
            # RHS: t^{-C(k,2)} e_k * phi(bbar_mu)
            mp=D.conj(mu)
            Ppoly=Psm[mp] if mp in Psm else None
            assert Ppoly is not None
            prod=D.mul(D.e_lambda((k,),N),Ppoly)
            keys=list(Pbig.keys()); basis=[Pbig[x] for x in keys]
            co=D.expand_in_basis(prod,basis,keys)
            rhs={}
            for kap,c in co.items():
                rhs[kap]=rhs.get(kap,FFt.zero)+c*(FFt.one/tq**(k*(k-1)//2))*(FFt.one/tq**D.nstat(mp))
            tot2+=1
            same=all(lhs.get(x,FFt.zero)==rhs.get(x,FFt.zero) for x in set(lhs)|set(rhs))
            if same: ok2+=1
            else:
                print("   H(2) FAIL n=%d k=%d mu=%s"%(n,k,mu))
                for x in sorted(set(lhs)|set(rhs)):
                    a,b=lhs.get(x,FFt.zero),rhs.get(x,FFt.zero)
                    if a!=b: print("      kappa=%s  lhs=%s  rhs=%s"%(x,a.as_expr(),b.as_expr()))
print("  %d / %d  (mu,k) pairs with |mu|+k <= %d"%(ok2,tot2,min(NMAX,6)+1))

print()
print("="*74)
print("CONTROL C3: L_k commute  (d_{lam,mu} independent of the order of the parts of lam)")
import itertools
c3ok=c3tot=0
for n in range(2,min(NMAX,6)+1):
    for lam in partitions(n):
        ref=D.d_by_H3(lam)
        for perm in set(itertools.permutations(lam)):
            c3tot+=1
            if D.d_by_H3(perm)==ref: c3ok+=1
            else: print("   C3 FAIL",lam,perm)
print("  %d / %d orderings"%(c3ok,c3tot))

print()
print("="*74)
print("CONTROL C4: corrupt the H(3) weight (w -> w + t); agreement with mechanism (c) MUST break")
c4break=c4tot=0
for n in range(2,min(NMAX,5)+1):
    for lam in partitions(n):
        dc=D.d_by_H3(lam,corrupt=True)
        for mu in partitions(n):
            c4tot+=1
            if dc.get(mu,D.ZERO)!=D.d_by_KK(lam,mu): c4break+=1
print("  corrupted weight disagrees on %d / %d pairs  (a control that does not fire is not a control)"%(c4break,c4tot))

print()
print("="*74)
print("CONTROL C5: t -> 1/t applied BEFORE vs AFTER the e->P expansion")
print("  (b) builds P in u=1/t then multiplies by t^{n(mu')-n(lam')};")
print("  C5 rebuilds P in u=t, expands, and substitutes t->1/t afterwards.")
c5ok=c5tot=0
for n in range(1,min(NMAX,5)+1):
    N=n
    Pu,_=D.HL_P(n,N,FFt.one/tq)      # u = 1/t
    Pt,_=D.HL_P(n,N,tq)              # u = t
    for lam in partitions(n):
        E=D.e_lambda(lam,N)
        kA=list(Pu.keys()); coA=D.expand_in_basis(E,[Pu[x] for x in kA],kA)
        kB=list(Pt.keys()); coB=D.expand_in_basis(E,[Pt[x] for x in kB],kB)
        for mu in partitions(n):
            mp=D.conj(mu)
            a=coA.get(mp,FFt.zero)*tq**(D.nstat(mp)-D.nstat(D.conj(lam)))
            bex=sympy.simplify(coB.get(mp,FFt.zero).as_expr().subs(tt,1/tt))
            b=sympy.simplify(bex*tt**(D.nstat(mp)-D.nstat(D.conj(lam))))
            c5tot+=1
            if sympy.simplify(a.as_expr()-b)==0: c5ok+=1
            else: print("   C5 FAIL",lam,mu,a.as_expr(),b)
print("  %d / %d pairs agree"%(c5ok,c5tot))
