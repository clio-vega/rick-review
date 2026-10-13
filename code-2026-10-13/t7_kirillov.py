"""
TEST 7: the FACTORISATION that rem:H attributes to Kirillov98 (arXiv:math/9803006,
 which is NOT on disk here -- so this is a check of the STATEMENT Rick prints,
 not of the attribution).

rem:H prints:   e_lam = sum_kappa M(e,P)_{lam,kappa} P_kappa(x;t),
                M(e,P)_{lam,kappa} = sum_nu K_{nu,lam} K_{nu',kappa}(t),
and:            d_{lam,mu}(t) = t^{n(mu')-n(lam')} M(e,P)_{lam,mu'}(t^{-1}).
"""
import sys,sympy
sys.path.insert(0,'/home/clio/projects/reviews/code-2026-10-13')
import t2_dmatrix as D
from t2_dmatrix import FF,t,ONE,ZERO,partitions,conj,nstat
tt=sympy.Symbol('t')
NMAX=5
print("CHECK 7.1  M(e,P)_{lam,kappa}(t) (Gram-Schmidt, u=t) == sum_nu K_{nu,lam} K_{nu',kappa}(t)")
ok=tot=0
for n in range(1,NMAX+1):
    N=n
    P,_=D.HL_P(n,N,t)
    keys=list(P.keys()); basis=[P[x] for x in keys]
    for lam in partitions(n):
        co=D.expand_in_basis(D.e_lambda(lam,N),basis,keys)
        for kap in partitions(n):
            got=co.get(kap,ZERO)
            acc={}
            for nu in partitions(n):
                a=D.kostka(nu,lam)
                if not a: continue
                for e,c in D.kostka_foulkes_dict(conj(nu),kap).items():
                    acc[e]=acc.get(e,0)+a*c
            pred=D.dict_to_FF(acc)
            tot+=1
            if got==pred: ok+=1
            else: print("   FAIL lam=%s kappa=%s got %s pred %s"%(lam,kap,got.as_expr(),pred.as_expr()))
print("  %d / %d (lam,kappa) pairs, n <= %d"%(ok,tot,NMAX))
print()
print("CHECK 7.2  rem:H's d = t^{n(mu')-n(lam')} M(e,P)_{lam,mu'}(1/t)  ==  cor:dmatrix's d")
ok=tot=0
for n in range(1,NMAX+1):
    N=n
    P,_=D.HL_P(n,N,t)
    keys=list(P.keys()); basis=[P[x] for x in keys]
    for lam in partitions(n):
        co=D.expand_in_basis(D.e_lambda(lam,N),basis,keys)
        for mu in partitions(n):
            mp=conj(mu)
            M=co.get(mp,ZERO)
            lhs=sympy.simplify(M.as_expr().subs(tt,1/tt)*tt**(nstat(mp)-nstat(conj(lam))))
            rhs=D.d_by_KK(lam,mu).as_expr()
            tot+=1
            if sympy.simplify(lhs-rhs)==0: ok+=1
            else: print("   FAIL",lam,mu,sympy.simplify(lhs),rhs)
print("  %d / %d"%(ok,tot))
