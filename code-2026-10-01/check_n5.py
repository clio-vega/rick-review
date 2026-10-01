from ds_engine import *
import itertools
def conj_full(lam):
    if not lam or lam[0]==0: return ()
    return tuple(sum(1 for p in lam if p>c) for c in range(lam[0]))
n=5;m=5;X=xs(m)
allp=list(partitions(n))
for lam in allp:
    P=eqt(lam,X,sval=s,tval=t)
    c=e_expand(P,n,m,X)
    nz={mu:v for mu,v in c.items() if sp.simplify(v)!=0}
    upset=[mu for mu in allp if dom_geq(mu,lam)]
    bad=[mu for mu in nz if not dom_geq(mu,lam)]
    missing=[mu for mu in upset if mu not in nz]
    lead=sp.simplify(nz.get(lam,0)-s**n_stat(lam))
    van=[mu for mu in nz if mu!=lam and sp.simplify(sp.cancel(nz[mu].subs(s,1)))!=0]
    vb=[];lb=[]
    for mu in nz:
        pol=sp.Poly(sp.simplify(sp.cancel(nz[mu])),s)
        v=min(mm[0] for mm in pol.monoms())
        if v!=n_stat(mu): vb.append((mu,v,n_stat(mu)))
        low=sp.simplify(pol.coeff_monomial(s**v).subs(t,0))
        if sp.simplify(low-1)!=0: lb.append((mu,low))
    print('lam=%-15s supp=%d upset=%d S_viol=%s missing=%s lead=%s s1=%s val=%s d0=%s'%(
        str(lam),len(nz),len(upset),bad or 'none',missing or 'none',lead==0,van or 'none',not vb,not lb),flush=True)
    if vb: print('   VALBAD',vb,flush=True)
    if lb: print('   LOWBAD',lb,flush=True)
print('N5 DONE')
