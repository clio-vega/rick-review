"""Hunt for Rick's 'allowed' counts: N=3 -> 39, N=4 -> 408, N=5 -> 5578."""
from itertools import combinations
TARGET={3:39,4:408,5:5578}

def geq(M,I):
    s,r=len(M),len(I)
    if s<r: return False
    return all(i<=m for i,m in zip(I,M[s-r:]))
def subsets(N):
    out=[]
    for k in range(N+1): out.extend(combinations(range(1,N+1),k))
    return out
def Eset(lam,mu,nu,a,b,N):
    g=[x for x in range(1,N+1) if x not in (a,b)]
    r=[]
    for k in range(len(g)+1):
        for M in combinations(g,k):
            if geq(nu,tuple(sorted(M+(a,b)))) and geq(M,lam) and geq(M,mu): r.append(M)
    return r

cands={}
for N in (3,4,5):
    S=subsets(N); pairs=list(combinations(range(1,N+1),2))
    tri=[(l,m,n) for l in S for m in S for n in S if geq(n,l) and geq(n,m)]
    c={}
    c['triples nu>=lam,mu']=len(tri)
    c['triples jump>=2']=sum(1 for l,m,n in tri if len(n)-max(len(l),len(m))>=2)
    c['triples jump>=1']=sum(1 for l,m,n in tri if len(n)-max(len(l),len(m))>=1)
    c['triples lam,mu nonempty']=sum(1 for l,m,n in tri if l and m)
    c['triples |n|<=|l|+|m|']=sum(1 for l,m,n in tri if len(n)<=len(l)+len(m))
    c['triples nonempty & |n|<=|l|+|m|']=sum(1 for l,m,n in tri if l and m and len(n)<=len(l)+len(m))
    c['triples sum: |nu|_s <= |lam|_s+|mu|_s']=sum(1 for l,m,n in tri if sum(n)<=sum(l)+sum(m))
    c['(t,p) E!=0']=sum(1 for l,m,n in tri for a,b in pairs if Eset(l,m,n,a,b,N))
    c['(t,p) jump>=2']=sum(1 for l,m,n in tri for a,b in pairs if len(n)-max(len(l),len(m))>=2)
    # pair-level: a,b in nu
    c['(t,p) a,b in nu']=sum(1 for l,m,n in tri for a,b in pairs if a in n and b in n)
    c['(t,p) a,b in nu & jump>=2']=sum(1 for l,m,n in tri for a,b in pairs if a in n and b in n and len(n)-max(len(l),len(m))>=2)
    # H12 only
    c['H12 only, nu>=lam,mu']=len(tri)
    c['(t, H12) E!=0']=sum(1 for l,m,n in tri if Eset(l,m,n,1,2,N))
    cands[N]=c

keys=cands[3].keys()
print(f"{'candidate':46s} {'N=3':>7s} {'N=4':>7s} {'N=5':>8s}  match?")
for k in keys:
    v=[cands[N][k] for N in (3,4,5)]
    hit=''.join('*' if v[i]==TARGET[N] else '.' for i,N in enumerate((3,4,5)))
    print(f"{k:46s} {v[0]:7d} {v[1]:7d} {v[2]:8d}  {hit}")
print(f"{'TARGET (Rick)':46s} {39:7d} {408:7d} {5578:8d}")
