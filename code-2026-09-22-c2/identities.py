from neyman_check import *
from itertools import product

def mus_below(alpha, k, n, d):
    """cylindric mu with mu subseteq alpha and |alpha/mu| = d."""
    out=[]
    for delta in product(range(0,d+1), repeat=k):
        if sum(delta)!=d: continue
        mu = tuple(alpha[i]-delta[i] for i in range(k))
        if is_cylpar(mu,k,n): out.append(mu)
    return out

def lams_above(alpha, k, n, d):
    out=[]
    for delta in product(range(0,d+1), repeat=k):
        if sum(delta)!=d: continue
        lam = tuple(alpha[i]+delta[i] for i in range(k))
        if is_cylpar(lam,k,n): out.append(lam)
    return out

def mus_below_two(alpha, beta, k, n, dx):
    """cylindric mu <= alpha and <= beta with |alpha/mu| = dx."""
    out=[]
    for delta in product(range(0,dx+1), repeat=k):
        if sum(delta)!=dx: continue
        mu = tuple(alpha[i]-delta[i] for i in range(k))
        if is_cylpar(mu,k,n) and contains(beta,mu,k,n): out.append(mu)
    return out

def lams_above_two(alpha, beta, k, n, dx):
    """cylindric lam >= alpha and >= beta with |lam/beta| = dx."""
    out=[]
    M = tuple(max(alpha[i],beta[i]) for i in range(k))
    for delta in product(range(0,dx+1), repeat=k):
        lam = tuple(beta[i]+delta[i] for i in range(k))
        if sum(lam[i]-beta[i] for i in range(k))!=dx: continue
        if not contains(lam,M,k,n): continue
        if is_cylpar(lam,k,n): out.append(lam)
    return out

print("=== Corollary \\label{oneschurcor} (Neyman src line 1824, = Cor 5.21) ===")
tot=badc=0
for (k,n) in [(1,3),(2,4),(2,5),(3,5),(3,6),(2,6)]:
    cands=[t for t in product(range(0,3), repeat=k) if is_cylpar(t,k,n)]
    for alpha in cands:
        for d in range(0,5):
            ell=max(d,1)
            L={}; R={}
            for mu in mus_below(alpha,k,n,d): add_into(L, gf_chain(alpha,mu,k,n,ell))
            for lam in lams_above(alpha,k,n,d): add_into(R, gf_chain(lam,alpha,k,n,ell))
            L={w:c for w,c in L.items() if c}; R={w:c for w,c in R.items() if c}
            tot+=1
            if L!=R:
                badc+=1
                if badc<4: print("  FAIL",k,n,alpha,d,L,R)
print(f"  {tot} (k,n,alpha,degree) instances checked, {badc} failures")

print("=== Theorem \\label{schurpols} (Neyman src line 1677, = Thm 5.14, cylindric Cauchy) ===")
tot=badt=0
for (k,n) in [(1,3),(2,4),(2,5),(3,5)]:
    cands=[t for t in product(range(0,3), repeat=k) if is_cylpar(t,k,n)]
    for alpha in cands:
        for beta in cands:
            shift=sum(alpha)-sum(beta)
            for dx in range(0,4):
                dy=dx-shift
                if dy<0 or dy>4: continue
                ellx=max(dx,1); elly=max(dy,1)
                L={}; R={}
                for mu in mus_below_two(alpha,beta,k,n,dx):
                    if nboxes(beta,mu,k,n)!=dy: continue
                    A=gf_chain(alpha,mu,k,n,ellx); B=gf_chain(beta,mu,k,n,elly)
                    for w1,c1 in A.items():
                        for w2,c2 in B.items(): L[(w1,w2)]=L.get((w1,w2),0)+c1*c2
                for lam in lams_above_two(alpha,beta,k,n,dx):
                    if nboxes(lam,alpha,k,n)!=dy: continue
                    A=gf_chain(lam,beta,k,n,ellx); B=gf_chain(lam,alpha,k,n,elly)
                    for w1,c1 in A.items():
                        for w2,c2 in B.items(): R[(w1,w2)]=R.get((w1,w2),0)+c1*c2
                L={w:c for w,c in L.items() if c}; R={w:c for w,c in R.items() if c}
                tot+=1
                if L!=R:
                    badt+=1
                    if badt<4: print("  FAIL",k,n,alpha,beta,dx,dy,"L-R keys",set(L)^set(R))
print(f"  {tot} (k,n,alpha,beta,bidegree) instances checked, {badt} failures")
