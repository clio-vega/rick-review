"""Independent re-check of p_21 by THREE separate routes, because a
refutation of a collaborator's claim has to survive my own instrument first.
  route A: inverse-Euler recurrence (sum_{d|n} d p_d = l_n)   [integer]
  route B: Mobius-log  sum p_k t^k = sum_d (mu(d)/d) log B(t^d) [Fraction]
  route C: direct PBW  B(t) = prod (1-t^k)^{-p_k}, peel off order by order
Plus: does b_k actually satisfy the defining algebraic equation to order 25?
"""
from fractions import Fraction as Fr
from math import comb
N=26
def mul(f,g,n=N): return [sum(f[i]*g[k-i] for i in range(k+1)) for k in range(n)]
def inv(f,n=N):
    g=[Fr(1,1)/f[0]]+[Fr(0)]*(n-1)
    for k in range(1,n): g[k]=-sum(f[i]*g[k-i] for i in range(1,k+1))/f[0]
    return g
F=[Fr(0)]*N
for _ in range(N+3):
    g=[3-2*F[0]]+[-2*x for x in F[1:]]
    num=mul([Fr(0),Fr(1)]+[Fr(0)]*(N-2),mul(g,g))
    omF=[1-F[0]]+[-x for x in F[1:]]
    den=mul(mul(omF,omF),mul(omF,[3-4*F[0]]+[-4*x for x in F[1:]]))
    F=mul(num,inv(den))
b=[1]+[int(x) for x in F[1:]]

# --- does F really solve F(1-F)^3(3-4F) = theta (3-2F)^2 ? -----------------
Ff=[Fr(x) for x in [0]+b[1:]]
omF=[1-Ff[0]]+[-x for x in Ff[1:]]
lhs=mul(mul(Ff,omF),mul(omF,mul(omF,[3-4*Ff[0]]+[-4*x for x in Ff[1:]])))
g=[3-2*Ff[0]]+[-2*x for x in Ff[1:]]
rhs=mul([Fr(0),Fr(1)]+[Fr(0)]*(N-2),mul(g,g))
res=[lhs[i]-rhs[i] for i in range(N)]
print("defining-equation residual, orders 0..%d:"%(N-1), "ALL ZERO" if all(x==0 for x in res) else res)

# --- route A --------------------------------------------------------------
l=[0]*N
for n in range(1,N): l[n]=n*b[n]-sum(l[k]*b[n-k] for k in range(1,n))
pA=[0]*N
for n in range(1,N):
    s=l[n]-sum(d*pA[d] for d in range(1,n) if n%d==0); assert s%n==0; pA[n]=s//n

# --- route B : Mobius-log -------------------------------------------------
def mobius(n):
    r=1; d=2; m=n
    while d*d<=m:
        if m%d==0:
            m//=d
            if m%d==0: return 0
            r=-r
        d+=1
    if m>1: r=-r
    return r
def logser(f,n=N):          # log of series with f[0]=1
    out=[Fr(0)]*n; fp=[Fr(i*f[i]) for i in range(n)]   # t f'(t)
    # t (log f)' = t f'/f  ->  coefficients
    q=mul(fp,inv([Fr(x) for x in f],n),n)
    for k in range(1,n): out[k]=q[k]/k
    return out
S=[Fr(0)]*N
for d in range(1,N):
    mu=mobius(d)
    if mu==0: continue
    Bd=[Fr(0)]*N; Bd[0]=Fr(1)
    for k in range(1,N):
        if d*k<N: Bd[d*k]=Fr(b[k])
    lg=logser(Bd)
    for i in range(N): S[i]+=Fr(mu,d)*lg[i]
pB=[0]+[S[k] for k in range(1,N)]

# --- route C : peel PBW ---------------------------------------------------
cur=[Fr(x) for x in b]; pC=[0]*N
for d in range(1,N):
    pd=cur[d]; assert pd.denominator==1; pd=int(pd); pC[d]=pd
    fac=[Fr(0)]*N; j=0
    while d*j<N:
        fac[d*j]=Fr((-1)**j*comb(pd,j)) if pd>=0 else Fr(0); j+=1
    if pd<0:
        j=0; fac=[Fr(0)]*N
        while d*j<N: fac[d*j]=Fr(comb(-pd+j-1,j)*(-1)**0)*(-1)**0; j+=1
    cur=mul(cur,fac)

print()
print(" k :   route A (int rec)        route B (Mobius-log)     route C (PBW peel)   agree")
for k in list(range(1,14))+[19,20,21,22,25]:
    ok = (pA[k]==pB[k]==pC[k])
    print("%2d : %22d %24s %22d   %s"%(k,pA[k],str(pB[k]),pC[k],"yes" if ok else "*** NO ***"))
print()
print("all three routes agree for k=1..%d : %s"%(N-1, all(pA[k]==pB[k]==pC[k] for k in range(1,N))))
print()
print("p_21 =", pA[21])
print("p_21 mod 3 =", pA[21]%3, "   <- Rick's Sequence-3 %C predicts 2 (since 3 | 21)")
print("p_k mod 3, k=1..25:", [pA[k]%3 for k in range(1,N)])
print("first k where Rick's (0,0,2) pattern fails:",
      next(k for k in range(1,N) if pA[k]%3 != (0 if k%3 else 2)))
