import itertools, functools
from sympy import symbols, Rational, cancel, expand, Integer, Poly, Matrix
import engine as E
s=E.s; eps=symbols('eps'); tv=Rational(3)

def setparts(lst):
    if not lst: yield []; return
    f,rest=lst[0],lst[1:]
    for p in setparts(rest):
        for i in range(len(p)): yield p[:i]+[[f]+p[i]]+p[i+1:]
        yield [[f]]+p

def kappa(lam,mu):
    if not E.dominates(mu,lam): return -1
    best=0
    for pl in setparts(list(range(len(lam)))):
        for pm in setparts(list(range(len(mu)))):
            if len(pl)!=len(pm) or len(pl)<=best: continue
            r=len(pl)
            for perm in itertools.permutations(range(r)):
                good=True
                for i in range(r):
                    lb=tuple(sorted((lam[j] for j in pl[i]),reverse=True))
                    mb=tuple(sorted((mu[j] for j in pm[perm[i]]),reverse=True))
                    if sum(lb)!=sum(mb) or not E.dominates(mb,lb): good=False;break
                if good: best=r;break
    return best

def Ek(f,X,k,m):
    tot=0
    for A in itertools.combinations(range(m),k):
        cA=Integer(1)
        for i in A:
            for j in range(m):
                if j not in A: cA*=(X[i]-tv*X[j])/(X[i]-X[j])
        xA=Integer(1)
        for i in A: xA*=X[i]
        tot+=cA*xA*f.subs({X[i]:s*X[i] for i in A},simultaneous=True)
    return cancel(expand(cancel(tot)))

def Ekp(f,X,k,p,m):
    g=expand(cancel(Ek(f,X,k,m).subs(s,1+eps)))
    return expand(Poly(g,eps).coeff_monomial(eps**p))

@functools.lru_cache(maxsize=None)
def ebas(m,d):
    X=E.xs(m)
    mus=[tuple(p) for p in E.partitions(d,maxpart=m)]
    lams=[tuple(p) for p in E.partitions(d,maxlen=m)]
    tab={mu: E.to_mono_dict(expand(functools.reduce(lambda u,v:u*v,[E.e_sym(p,X) for p in mu],Integer(1))),X,d) for mu in mus}
    A=Matrix([[tab[mu].get(l,0) for mu in mus] for l in lams])
    return tuple(mus),tuple(lams),A.inv()

def in_e(f,m,d):
    X=E.xs(m); mus,lams,Ai=ebas(m,d)
    tgt=E.to_mono_dict(expand(cancel(f)),X,d)
    sol=Ai*Matrix([[tgt.get(l,0)] for l in lams])
    return {mu:cancel(sol[i]) for i,mu in enumerate(mus)}

k1ok=k1bad=0; same_n=diff_n=0; k2=0; k2hit=0
for lam in [(2,1,1),(3,1,1),(2,2,1),(2,2,2),(3,2,1)]:
    n=sum(lam); m=n; X=E.xs(m)
    f=Integer(1)
    for p in reversed(lam): f=Ek(f,X,p,m)
    cs=in_e(f,m,n)
    lhs={}
    for mu,cv in cs.items():
        cc=cancel(cv.subs(s,1+eps))
        lhs[mu]=expand(Poly(expand(cc),eps).coeff_monomial(eps**2)) if cc!=0 else Integer(0)
    rhs={}
    for (a,b,c) in sorted(set(itertools.permutations(lam))):
        eb=E.e_sym(b,X); ec=E.e_sym(c,X)
        Gam=expand(Ekp(expand(eb*ec),X,a,2,m)-eb*Ekp(ec,X,a,2,m)-ec*Ekp(eb,X,a,2,m))
        DD=Ekp(Ekp(ec,X,b,1,m),X,a,1,m)
        rhs[(a,b,c)]=in_e(expand(Gam+DD),m,n)
    norders=len(rhs)
    for mu in sorted(cs):
        kp=kappa(lam,mu)
        if kp<1: continue
        L=cancel(lhs.get(mu,0))
        vals=[(o,cancel(rhs[o].get(mu,0))) for o in rhs]
        same=all(cancel(v-vals[0][1])==0 for _,v in vals)
        hit=all(cancel(v-L)==0 for _,v in vals)
        if kp==1:
            if hit: k1ok+=1
            else:
                k1bad+=1; print(f"  FAIL lam={lam} mu={mu} lhs={L}")
                for o,v in vals: print(f"      {o}: {v}")
            if same: same_n+=1
            else: diff_n+=1
        else:
            k2+=1
            if hit: k2hit+=1
    print(f"  lam={lam}: {norders} distinct orderings, done", flush=True)

print()
print(f"kappa=1 : {k1ok} of {k1ok+k1bad} (lam,mu) pairs satisfy Prop 6.1 in EVERY ordering; {k1bad} fail")
print(f"kappa=1 : RHS identical across all orderings in {same_n} of {same_n+diff_n} pairs")
print(f"CONTROL kappa>=2 (Prop 6.1 asserts nothing there): {k2} pairs, {k2hit} satisfy it anyway,"
      f" {k2-k2hit} break")
print(f"  -> the kappa=1 hypothesis is load-bearing: {k2hit<k2}")
