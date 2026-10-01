from aha import *
import itertools
fails=[]
def rep(tag,d):
    if sp.simplify(sp.cancel(sp.together(d)))!=0: fails.append(tag); print('  FAIL',tag,flush=True)

def sigma_lm(l, m, F, X):
    """sigma_{[l,m]} = sum_{a=l}^{m} T_{a-1}...T_l  (a=l gives identity)"""
    tot = 0
    for a in range(l, m+1):
        G = F
        for i in range(l, a):      # T_l first, then T_{l+1}, ..., T_{a-1}
            G = T(G, X, i)
        tot += G
    return sp.cancel(sp.together(tot))

print("=== Day205b Lemma 1 / W_r Lemma 2: sigma_m F = sum_i F^(i) prod_{j!=i} a_ij, F sym in X_2..X_m ===",flush=True)
for m in (2,3,4,5):
    X=xs(m)
    tails=[sp.Integer(1)]+[e_poly(r,X[1:]) for r in range(1,m)]
    tails.append(X[1]**2*sum(X[1:]) if m>=2 else sp.Integer(1))
    for F in tails:
        lhs=sigma_lm(1,m,F,X)
        rhs=0
        for i in range(m):
            sub={X[0]:X[i],X[i]:X[0]}
            Fi=F.subs(sub,simultaneous=True)
            pr=sp.Integer(1)
            for j in range(m):
                if j!=i: pr*=(X[i]-t*X[j])/(X[i]-X[j])
            rhs+=Fi*pr
        rep('L1 m=%d F=%s'%(m,F), lhs-rhs)
    print('  m=%d checked %d symmetric-in-tail F'%(m,len(tails)),flush=True)

print("\n=== Day205b Lemma 2 / W_r Lemma 3 (residue): (1-t) sum_i X_i^n prod_{j!=i} a_ij = q_n ===",flush=True)
for m in (2,3,4):
    X=xs(m)
    # q_n from Q(y) = E(-ty)/E(-y)
    y=symbols('y')
    E=lambda arg: sp.prod([1+X[i]*arg for i in range(m)])
    Q=sp.series(sp.cancel(E(-t*y)/E(-y)), y, 0, m+4).removeO()
    for n in range(1,m+3):
        S=0
        for i in range(m):
            pr=sp.Integer(1)
            for j in range(m):
                if j!=i: pr*=(X[i]-t*X[j])/(X[i]-X[j])
            S+=X[i]**n*pr
        qn=sp.expand(Q).coeff(y,n)
        rep('L2 m=%d n=%d'%(m,n), (1-t)*S-qn)
    print('  m=%d: n=1..%d'%(m,m+2),flush=True)

print("\n=== (C2) ordered formula ===",flush=True)
for m in (2,3,4):
    X=xs(m)
    for k in range(1,m+1):
        # G symmetric in the TAIL only: G = X_1^2 * e_r(tail) etc. Use pi^k F which is
        # sym in head+tail (a special case), plus a tail-only example.
        cands=[pi_pow(k,e_poly(r,X),X) for r in range(0,m+1)]
        if k<m: cands.append(X[0]**2*e_poly(1,X[k:]))
        for G in cands:
            lhs=G
            for l in range(k,0,-1):   # sigma_{[1,m]}...sigma_{[k,m]}: rightmost sigma_{[k,m]} first
                lhs=sigma_lm(l,m,lhs,X)
            rhs=0
            tmp=list(symbols('y1:%d'%(m+1)))
            for a in itertools.permutations(range(m),k):
                rest=[j for j in range(m) if j not in a]
                sub={}
                for idx,v in enumerate(a): sub[X[idx]]=tmp[v]
                for idx,v in enumerate(rest): sub[X[k+idx]]=tmp[v]
                GA=G.subs(sub,simultaneous=True).subs({tmp[i]:X[i] for i in range(m)},simultaneous=True)
                w=sp.Integer(1)
                for l in range(k):
                    for j in range(m):
                        if j in a[:l+1]: continue
                        w*=(X[a[l]]-t*X[j])/(X[a[l]]-X[j])
                rhs+=GA*w
            rep('C2 m=%d k=%d'%(m,k), lhs-rhs)
        print('  m=%d k=%d: %d G'%(m,k,len(cands)),flush=True)
print('\n=== FAILURES: %d ==='%len(fails),flush=True)
if fails: print(fails)
