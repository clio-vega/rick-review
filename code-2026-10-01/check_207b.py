from aha import *
import itertools

fails=[]
def rep(tag, d):
    if sp.simplify(sp.cancel(sp.together(d)))!=0:
        fails.append(tag); print('  FAIL', tag, flush=True); return False
    return True

print("=== (C3) Poincare: sum_{w in S_k} prod_{l<l'} a_{w_l w_l'} = [k]_t! ===",flush=True)
for k in range(1,6):
    X=xs(k); tot=0
    for w in itertools.permutations(range(k)):
        p=sp.Integer(1)
        for l in range(k):
            for l2 in range(l+1,k):
                p*=(X[w[l]]-t*X[w[l2]])/(X[w[l]]-X[w[l2]])
        tot+=p
    f=sp.Integer(1)
    for i in range(1,k+1): f*=sum(t**j for j in range(i))
    print('  k=%d %s'%(k,'OK' if rep('C3 k=%d'%k, tot-f) else ''),flush=True)

print("\n=== (A_k) Prop 3: Y_{b1}..Y_{bk}F = t^C(k,2) T_{w(b)} pi^k F ===",flush=True)
for m in (2,3,4):
    n=0
    X=xs(m)
    for r in range(0,m+1):
        F=e_poly(r,X)
        for k in range(1,m+1):
            for b in itertools.combinations(range(1,m+1),k):
                G=F
                for i in reversed(b): G=Y(G,X,i)
                rhs=t**sp.binomial(k,2)*T_word(pi_pow(k,F,X),X,w_of_D(list(b),m))
                rep('Ak m=%d r=%d b=%s'%(m,r,b), G-rhs); n+=1
    print('  m=%d: %d (r,k,b) cases'%(m,n),flush=True)

print("\n=== e_k(Y)F = t^C(k,2) sigma^(k) pi^k F ===",flush=True)
for m in (2,3,4):
    X=xs(m); n=0
    for r in range(0,m+1):
        F=e_poly(r,X)
        for k in range(1,m+1):
            rep('ekY-sigma m=%d r=%d k=%d'%(m,r,k), ek_Y(k,F,X)-t**sp.binomial(k,2)*sigma_k(k,pi_pow(k,F,X),X)); n+=1
    print('  m=%d: %d cases'%(m,n),flush=True)

print("\n=== (K_k) Prop 4: sigma^(k) G = sum_{|A|=k} G^(A) prodx_A ===",flush=True)
for m in (2,3,4):
    X=xs(m); n=0
    for k in range(1,m+1):
        for r in range(0,m+1):
            G=pi_pow(k,e_poly(r,X),X)
            rhs=0
            tmp=list(symbols('y1:%d'%(m+1)))
            for A in itertools.combinations(range(m),k):
                Ac=[j for j in range(m) if j not in A]
                sub={}
                for idx,a in enumerate(A): sub[X[idx]]=tmp[a]
                for idx,a in enumerate(Ac): sub[X[k+idx]]=tmp[a]
                GA=G.subs(sub,simultaneous=True).subs({tmp[i]:X[i] for i in range(m)},simultaneous=True)
                rhs+=GA*kernel_A(A,X)
            rep('Kk m=%d k=%d r=%d'%(m,k,r), sigma_k(k,G,X)-rhs); n+=1
    print('  m=%d: %d cases'%(m,n),flush=True)

print("\n=== (0.1) END-TO-END: t^{-C(k,2)} e_k(Y).F == subset formula ===",flush=True)
for m in (2,3,4):
    X=xs(m); n=0
    for k in range(1,m+1):
        for r in range(0,m+1):
            F=e_poly(r,X)
            rep('(0.1) m=%d k=%d r=%d'%(m,k,r), t**(-sp.binomial(k,2))*ek_Y(k,F,X)-subset_formula(k,F,X)); n+=1
    # also e_mu for 2-row mu
    for k in range(1,m+1):
        for mu in [(2,1),(1,1),(2,2),(3,1)]:
            if sum(mu)>m: continue
            F=sp.expand(sp.prod([e_poly(p,X) for p in mu]))
            rep('(0.1) m=%d k=%d mu=%s'%(m,k,mu), t**(-sp.binomial(k,2))*ek_Y(k,F,X)-subset_formula(k,F,X)); n+=1
    print('  m=%d: %d cases'%(m,n),flush=True)

print('\n==== TOTAL FAILURES: %d ===='%len(fails),flush=True)
if fails: print(fails)
