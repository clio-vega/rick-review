"""Remaining P^infty checks at exact-rational level + Psi-level NEW cases.
Clio 2026-10-22."""
import itertools, random
from fractions import Fraction as Fr
random.seed(7)
def rho(kappa,X,w):
    e=Fr(1)
    for k in range(1,kappa): e*=(1-w[k]/X)
    return e
def Psi(kap,th,M,w):
    r=len(kap); tot=Fr(0)
    for h in itertools.permutations(M,r):
        if any(h[j]<kap[j] for j in range(r)): continue
        X=[w[m] for m in h]; e=Fr(1)
        for j in range(r):
            e*=(1-1/X[j]**2)*rho(kap[j],X[j],w)*X[j]**th[j]
        for j in range(r):
            for k in range(j+1,r): e*=(1-1/(X[j]*X[k]))/(1-X[j]/X[k])
        for t in M:
            if t in h: continue
            for j in range(r): e*=(1-1/(w[t]*X[j]))/(1-w[t]/X[j])
        tot+=e
    return tot
def det_frac(Mx):
    A=[r[:] for r in Mx]; n=len(A); d=Fr(1)
    for i in range(n):
        p=next((k for k in range(i,n) if A[k][i]!=0),None)
        if p is None: return Fr(0)
        if p!=i: A[i],A[p]=A[p],A[i]; d=-d
        d*=A[i][i]; inv=Fr(1)/A[i][i]
        for k in range(i+1,n):
            f=A[k][i]*inv
            if f:
                for j in range(i,n): A[k][j]-=f*A[i][j]
    return d
def Alt(kap,th,xs,w):
    r=len(kap)
    return det_frac([[xs[k]**(j+th[j])*rho(kap[j],xs[k],w) for j in range(r)] for k in range(r)])
def pt(N): return {k:Fr(random.randint(2,311),random.randint(2,311))+3*k for k in range(1,N+1)}

def setup(kap,p,q,t0,oth):
    r=len(kap); b=q-p+1; e=t0-(b-1); s=kap[p]
    th1=[oth.get(j,0) for j in range(r)]; th2=list(th1)
    for j in range(p,q+1): th1[j]=t0-(j-p); th2[j]=e
    return r,b,e,s,th1,th2

print("== A. ALTERNANT level, exact rational, cases too slow symbolically ==")
cases=[((2,3,6,7),(2,3),2,{0:5,1:-3},"two blocks, collapse the SECOND"),
       ((3,4,5,6),(0,3),2,{},"b=4, s=3"),
       ((1,4,5,6,7),(1,4),0,{0:3},"b=4 interior, r=5"),
       ((1,2,3,4,5),(0,4),-2,{},"b=5=r, s=1"),
       ((2,3,4,8,9),(0,2),1,{3:2,4:-1},"b=3 + untouched 2nd block")]
for kap,(p,q),t0,oth,lab in cases:
    r,b,e,s,th1,th2=setup(kap,p,q,t0,oth)
    res=[]
    for _ in range(4):
        w=pt(14); xs=[w[m] for m in random.sample(range(1,14),r)]
        C=Fr(1)
        for m in range(b-1): C*=w[s+m]**(b-1-m)
        res.append(Alt(kap,th1,xs,w)-C*Alt(kap,th2,xs,w)==0)
    print(f"   {lab:36s} kap={kap}: {sum(res)}/4")

print("\n== B. NEGATIVE CONTROLS at alternant level (must be NONZERO) ==")
def neg(kap,th1,th2,C_fn,lab):
    bad=0
    for _ in range(4):
        w=pt(14); xs=[w[m] for m in random.sample(range(1,14),len(kap))]
        bad += (Alt(kap,th1,xs,w)-C_fn(w)*Alt(kap,th2,xs,w)!=0)
    print(f"   {lab:44s}: correctly nonzero {bad}/4")
neg((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:Fr(1),                "C := 1 (constant dropped)")
neg((2,3,4),[2,0,-2],[-2,-2,-2],lambda w:w[2]**2*w[3],         "slope -2 instead of -1")
neg((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:w[3]**2*w[4],         "wrong C (s shifted by 1)")
neg((2,4,5),[1,0,-1],[-1,-1,-1],lambda w:w[2]**2*w[3],         "NON-CONSECUTIVE labels (2,4,5)")
neg((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:w[2]*w[3]**2,         "C with exponents swapped")

print("\n== C. FULL Psi level, exact rational, cases NOT in Rick's q532.py ==")
rick=[((2,3,4),(0,2),1,{}),((3,4),(0,1),2,{}),((1,3,4,5),(1,3),-1,{0:2}),
      ((2,3,4,5),(0,3),0,{}),((1,2,5,6),(2,3),3,{0:-1,1:1})]
new=[((2,3),(0,1),1,{},                 (2,3,4,5)),
     ((1,2,3),(0,2),-1,{},              (1,2,3,4)),
     ((2,3,6,7),(0,1),0,{2:1,3:-2},     (2,3,4,6,7,8)),
     ((2,3,6,7),(2,3),2,{0:5,1:-3},     (2,3,4,6,7,8)),
     ((3,4,5),(0,2),4,{},               (3,4,5,6,7)),
     ((1,4,5,6),(1,3),0,{0:3},          (1,4,5,6,7)),
     ((2,3,4),(1,2),-3,{0:4},           (2,3,4,5,6))]
tot=ok=0
for kap,(p,q),t0,oth,M in new:
    r,b,e,s,th1,th2=setup(kap,p,q,t0,oth)
    res=[]
    for _ in range(2):
        w=pt(max(M)+2)
        C=Fr(1)
        for m in range(b-1): C*=w[s+m]**(b-1-m)
        res.append(Psi(kap,th1,M,w)-C*Psi(kap,th2,M,w)==0)
    tot+=len(res); ok+=sum(res)
    print(f"   kap={str(kap):14s} block={(p,q)} t0={t0:3d} out={str(oth):18s} M={M}: {sum(res)}/2")
print(f"   Psi-level NEW cases: {ok}/{tot} exact")
