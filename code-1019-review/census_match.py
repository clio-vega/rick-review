"""Pin down Rick's 'allowed' counts (N=3: 39, N=4: 408, N=5: 5578) and
characterise the Theorem-6-but-E-empty gap set."""
from itertools import combinations

def geq(M, I):
    s, r = len(M), len(I)
    if s < r: return False
    return all(i <= m for i, m in zip(I, M[s-r:]))

def subsets(N):
    out=[]
    for k in range(N+1): out.extend(combinations(range(1,N+1),k))
    return out

def Eset(lam,mu,nu,a,b,N):
    ground=[x for x in range(1,N+1) if x not in (a,b)]
    res=[]
    for k in range(len(ground)+1):
        for Mpp in combinations(ground,k):
            if geq(nu, tuple(sorted(Mpp+(a,b)))) and geq(Mpp,lam) and geq(Mpp,mu):
                res.append(Mpp)
    return res

def thm6(lam,mu,a,b,N):
    """Theorem 6 aggregate condition: exists M'' subset [N]\\{a,b} with M''>=lam,mu.
       (no reference to nu)"""
    ground=[x for x in range(1,N+1) if x not in (a,b)]
    for k in range(len(ground)+1):
        for Mpp in combinations(ground,k):
            if geq(Mpp,lam) and geq(Mpp,mu): return True
    return False

for N in (3,4,5):
    S=subsets(N); pairs=list(combinations(range(1,N+1),2))
    cases=[(l,m,n,a,b) for l in S for m in S for n in S
           if geq(n,l) and geq(n,m) for (a,b) in pairs]
    c_thm6 = [c for c in cases if thm6(c[0],c[1],c[3],c[4],N)]
    c_E    = [c for c in cases if Eset(*c,N)]
    gap    = [c for c in c_thm6 if not Eset(*c,N)]
    print(f"N={N}  (triple,pair) with nu>=lam,mu : {len(cases)}")
    print(f"      Theorem 6 condition holds      : {len(c_thm6)}   <-- candidate 'allowed'")
    print(f"      E != empty                     : {len(c_E)}")
    print(f"      GAP (Thm6 yes, E empty)        : {len(gap)}")
    gap_not12 = [c for c in gap if (c[3],c[4])!=(1,2)]
    print(f"      GAP on pairs != (1,2)          : {len(gap_not12)}")
    e12 = [c for c in c_E if (c[3],c[4])==(1,2)]
    t12 = [c for c in c_thm6 if (c[3],c[4])==(1,2)]
    print(f"      Thm6 on pair (1,2)             : {len(t12)}   E!=0 on (1,2): {len(e12)}")
    print()
