"""Reconcile Rick's census domain. Hypothesis: he reduces by the symmetry
c^nu_{lam mu} = c^nu_{mu lam} (lam <= mu as sorted tuples) and restricts to
jump >= 2 (jump<=1 being settled by Thm 10 / q488-d-jump-le-1)."""
from itertools import combinations, chain
def geq(M,I):
    s,r=len(M),len(I)
    if s<r: return False
    return all(i<=m for i,m in zip(I,M[s-r:]))
def subsets(N): return list(chain.from_iterable(combinations(range(1,N+1),k) for k in range(N+1)))
def Enz(lam,mu,nu,a,b,N):
    g=[x for x in range(1,N+1) if x not in (a,b)]
    for k in range(len(g)+1):
        for M in combinations(g,k):
            if geq(nu,tuple(sorted(M+(a,b)))) and geq(M,lam) and geq(M,mu): return True
    return False
print("domain: nu>=lam,mu AND lam<=mu (unordered pairs) AND jump>=2")
for N in (3,4,5):
    S=subsets(N); tot=0; allowed=0
    for lam in S:
        for mu in S:
            if lam>mu: continue
            for nu in S:
                if not(geq(nu,lam) and geq(nu,mu)): continue
                if len(nu)-max(len(lam),len(mu))<2: continue
                for a,b in combinations(range(1,N+1),2):
                    tot+=1
                    if Enz(lam,mu,nu,a,b,N): allowed+=1
    print(f"  N={N}: total={tot}  allowed(E!=0)={allowed}  non-allowed(E=0)={tot-allowed}")
print("  Rick: N=3 total 39 / 14 zeros;  N=4 allowed 408, non-allowed 354 (total 762);  N=5 allowed 5578")
