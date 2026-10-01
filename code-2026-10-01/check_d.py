from ds_engine import *
import itertools
from sympy import binomial

def M_count(nu, kappa):
    """# 0-1 matrices with row sums nu, column sums kappa."""
    nu=list(nu); kappa=list(kappa)
    from functools import lru_cache
    def rec(r, cols):
        if r == len(nu): return 1 if all(c==0 for c in cols) else 0
        tot=0
        idx=[i for i,c in enumerate(cols) if c>0]
        for S in itertools.combinations(idx, nu[r]):
            nc=list(cols)
            for i in S: nc[i]-=1
            tot+=rec(r+1, tuple(nc))
        return tot
    return rec(0, tuple(kappa))

n=4; m=4; X=xs(m)
allp=[p for p in partitions(n)]
print('n=4: d_{lam,mu}(t) = [s^{n(mu)}] c_{lam,mu}, and check d(1) = M_{lam,mu\'}')
for lam in allp:
    P=eqt(lam,X); c=e_expand(P,n,m,X)
    for mu in sorted([p for p in allp if dom_geq(p,lam)], key=n_stat):
        poly=sp.Poly(sp.simplify(sp.cancel(c[mu])), s)
        v=min(mm[0] for mm in poly.monoms())
        d=sp.factor(sp.simplify(poly.coeff_monomial(s**v)))
        Mv=M_count(lam, conj(mu))
        d1=sp.simplify(d.subs(t,1))
        flag='' if sp.simplify(d1-Mv)==0 else '   <<< MISMATCH M=%s'%Mv
        print('  lam=%-12s mu=%-12s val=%d n(mu)=%d  d=%-18s d(1)=%-4s M_{lam,mu\'}=%-4s%s'
              %(str(lam),str(mu),v,n_stat(mu),str(d),d1,Mv,flag))
