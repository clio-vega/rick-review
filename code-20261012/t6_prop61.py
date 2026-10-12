"""Prop 6.1 (fpsac prop:reduce): if (a,b,c) is ANY ordering of lambda and kappa(lambda,mu)=1,
   [(s-1)^2] c_{lambda mu} = [e_mu]( Gamma_a(e_b,e_c) + D_a D_b(e_c) ).
Independent engine: E_k from the printed subset formula, Taylor pieces by expanding s=1+eps."""
import itertools, functools
import engine as E
from sympy import symbols, cancel, expand, Integer, Poly, series, simplify
s,t=E.s,E.t
eps=symbols('eps')

# ---------- Taylor pieces of E_k in (s-1) ----------
def Ek_taylor(f, X, k, order):
    """returns [E_k^{(0)}f, ..., E_k^{(order)}f] where E_k = sum_p (s-1)^p E_k^{(p)}"""
    g = E.E_k(f, X, k)
    g = cancel(expand(g.subs(s, 1+eps)))
    P = Poly(g, eps)
    out=[]
    for p in range(order+1):
        out.append(expand(P.coeff_monomial(eps**p)))
    return out

def Ekp(f,X,k,p):  return Ek_taylor(f,X,k,p)[p]

# ---------- e_mu basis expansion ----------
@functools.lru_cache(maxsize=None)
def ebasis(m,d):
    X=E.xs(m)
    mus=[tuple(p) for p in E.partitions(d,maxlen=None,maxpart=m)]
    tab={}
    for mu in mus:
        poly=Integer(1)
        for p in mu: poly*=E.e_sym(p,X)
        tab[mu]=E.to_mono_dict(expand(poly),X,d)
    return tuple(mus),tab

def expand_in_e(f,m,d):
    X=E.xs(m)
    mus,tab=ebasis(m,d)
    target=E.to_mono_dict(expand(cancel(f)),X,d)
    # solve linear system
    from sympy import Matrix
    lams=[tuple(p) for p in E.partitions(d,maxlen=m)]
    A=Matrix([[tab[mu].get(lam,0) for mu in mus] for lam in lams])
    b=Matrix([[target.get(lam,0)] for lam in lams])
    sol=A.solve_least_squares(b) if A.rows!=A.cols else A.solve(b)
    return {mu: cancel(sol[i]) for i,mu in enumerate(mus)}

# ---------- kappa(lambda,mu) ----------
def setparts(lst):
    if not lst: yield []; return
    first,rest=lst[0],lst[1:]
    for p in setparts(rest):
        for i in range(len(p)):
            yield p[:i]+[[first]+p[i]]+p[i+1:]
        yield [[first]]+p

def kappa(lam,mu):
    if not E.dominates(mu,lam): return float('-inf')
    best=0
    for pl in setparts(list(range(len(lam)))):
        for pm in setparts(list(range(len(mu)))):
            if len(pl)!=len(pm): continue
            r=len(pl)
            # try all bijections between blocks
            for perm in itertools.permutations(range(r)):
                good=True
                for i in range(r):
                    lb=tuple(sorted((lam[j] for j in pl[i]),reverse=True))
                    mb=tuple(sorted((mu[j] for j in pm[perm[i]]),reverse=True))
                    if sum(lb)!=sum(mb) or not E.dominates(mb,lb): good=False;break
                if good: best=max(best,r);break
    return best

def Gamma(a,b,c,X):
    eb=E.e_sym(b,X); ec=E.e_sym(c,X)
    return expand(Ekp(expand(eb*ec),X,a,2) - eb*Ekp(ec,X,a,2) - ec*Ekp(eb,X,a,2))

print("=== Prop 6.1, all orderings, kappa=1 ===")
rows=[]
for lam in [(2,1,1),(2,2,1),(3,1,1),(2,2,2),(3,2,1),(3,2,2),(4,2,1),(3,3,1)]:
    n=sum(lam); m=n; X=E.xs(m)
    # e^star_lambda = E_{l1}E_{l2}E_{l3}(1)
    f=Integer(1)
    for p in reversed(lam): f=E.E_k(f,X,p)
    cs=expand_in_e(f,m,n)
    for mu,cval in sorted(cs.items()):
        if cval==0: continue
        kp=kappa(lam,mu)
        # [(s-1)^2] c_{lam mu}
        cc=cancel(cval.subs(s,1+eps))
        lhs=Poly(expand(cc),eps).coeff_monomial(eps**2) if cc!=0 else 0
        vals=[]
        for (a,b,c) in set(itertools.permutations(lam)):
            rhs_poly=expand(Gamma(a,b,c,X)+Ekp(Ekp(E.e_sym(c,X),X,b,1),X,a,1))
            rr=expand_in_e(rhs_poly,m,n).get(mu,0)
            vals.append(((a,b,c),cancel(rr)))
        rows.append((lam,mu,kp,cancel(lhs),vals))

ok=bad=0; ordok=ordbad=0; k2seen=0; k2match=0
for lam,mu,kp,lhs,vals in rows:
    agree_all = all(cancel(v-vals[0][1])==0 for _,v in vals)
    if kp==1:
        hit = all(cancel(v-lhs)==0 for _,v in vals)
        if hit: ok+=1
        else:
            bad+=1
            print(f"  FAIL kappa=1 lam={lam} mu={mu} lhs={lhs}")
            for o,v in vals: print(f"        ordering {o}: {v}")
        if agree_all: ordok+=1
        else: ordbad+=1
    else:
        k2seen+=1
        if all(cancel(v-lhs)==0 for _,v in vals): k2match+=1
print(f"\n  kappa=1 cases: {ok} of {ok+bad} satisfy Prop 6.1 in ALL orderings, {bad} fail")
print(f"  kappa=1 cases: {ordok} of {ordok+ordbad} have the RHS equal across all orderings")
print(f"  CONTROL (kappa>=2 pairs, where Prop 6.1 does NOT claim anything):")
print(f"        {k2seen} such pairs, of which {k2match} happen to satisfy the identity anyway")
print(f"        -> the kappa=1 hypothesis is load-bearing iff k2match < k2seen")
