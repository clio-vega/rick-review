"""Broader sweep: conjunctions of simple predicates, (triple,pair) and triple level."""
from itertools import combinations, chain
TARGET={3:39,4:408,5:5578}
def geq(M,I):
    s,r=len(M),len(I)
    if s<r: return False
    return all(i<=m for i,m in zip(I,M[s-r:]))
def subsets(N):
    return list(chain.from_iterable(combinations(range(1,N+1),k) for k in range(N+1)))
def Eset(lam,mu,nu,a,b,N):
    g=[x for x in range(1,N+1) if x not in (a,b)]
    for k in range(len(g)+1):
        for M in combinations(g,k):
            if geq(nu,tuple(sorted(M+(a,b)))) and geq(M,lam) and geq(M,mu): return True
    return False

PREDS = {
 'ab_in_nu'   : lambda l,m,n,a,b,N: a in n and b in n,
 'lam_ne'     : lambda l,m,n,a,b,N: len(l)>0,
 'mu_ne'      : lambda l,m,n,a,b,N: len(m)>0,
 'both_ne'    : lambda l,m,n,a,b,N: len(l)>0 and len(m)>0,
 'lam_le_mu'  : lambda l,m,n,a,b,N: l<=m,
 'card_sum'   : lambda l,m,n,a,b,N: len(n)<=len(l)+len(m),
 'jump2'      : lambda l,m,n,a,b,N: len(n)-max(len(l),len(m))>=2,
 'jump1'      : lambda l,m,n,a,b,N: len(n)-max(len(l),len(m))>=1,
 'E'          : lambda l,m,n,a,b,N: Eset(l,m,n,a,b,N),
 'b_eq_a1'    : lambda l,m,n,a,b,N: b==a+1,
 'nu_full'    : lambda l,m,n,a,b,N: len(n)==N,
 'ab_smallest': lambda l,m,n,a,b,N: len(n)>=2 and (a,b)==(n[0],n[1]),
}
import itertools
res={}
for N in (3,4,5):
    S=subsets(N); pairs=list(combinations(range(1,N+1),2))
    cases=[(l,m,n,a,b) for l in S for m in S for n in S
           if geq(n,l) and geq(n,m) for (a,b) in pairs]
    res[N]=cases
names=list(PREDS)
found=[]
for k in range(1,4):
    for combo in itertools.combinations(names,k):
        counts=[]
        for N in (3,4,5):
            c=0
            for cs in res[N]:
                if all(PREDS[p](*cs,N) for p in combo): c+=1
            counts.append(c)
            if counts[-1]!=TARGET[N]: break
        if len(counts)==3 and counts==[39,408,5578]:
            found.append((combo,counts))
        elif counts and counts[0]==39:
            print("  partial (N=3 hits):",combo,counts)
print("FULL MATCHES:",found if found else "NONE")
# also at triple level
print("--- triple level sweep ---")
tri={}
for N in (3,4,5):
    S=subsets(N)
    tri[N]=[(l,m,n) for l in S for m in S for n in S if geq(n,l) and geq(n,m)]
tnames=['lam_ne','mu_ne','both_ne','card_sum','jump2','jump1','lam_le_mu','nu_full']
for k in range(1,4):
    for combo in itertools.combinations(tnames,k):
        counts=[]
        for N in (3,4,5):
            c=sum(1 for l,m,n in tri[N] if all(PREDS[p](l,m,n,1,2,N) for p in combo))
            counts.append(c)
            if c!=TARGET[N]: break
        if len(counts)==3: print("TRIPLE FULL MATCH:",combo,counts)
        elif counts and counts[0]==39: print("  triple partial:",combo,counts)
