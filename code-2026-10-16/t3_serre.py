from qsym_indep import *
from math import comb

# free braided algebra: elements = {word (tuple of letter indices): laurent}
def fmul(S, X, Y):
    out=defaultdict(lzero)
    for u,cu in X.items():
        for v,cv in Y.items():
            out[u+v]=ladd(out[u+v],lmul(cu,cv))
    return {w:c for w,c in out.items() if c}
def deg(S,w):
    d=[0]*S.n
    for a in w: d[a]+=1
    return tuple(d)
def adc(S, i, Y):
    """braided commutator ad_c(F_i)(y) = F_i y - q^{(a_i,|y|)} y F_i  (y homogeneous)"""
    out=defaultdict(lzero)
    for w,c in Y.items():
        out[(i,)+w]=ladd(out[(i,)+w],c)
        e=S.truepair(tuple(1 if k==i else 0 for k in range(S.n)), deg(S,w))
        out[w+(i,)]=ladd(out[w+(i,)],lneg(lmul(c,lmono(e))))
    return {w:c for w,c in out.items() if c}

def gauss_binom(nn,p,zexp):
    """[n,p]_z as laurent, z = q^zexp.  product formula via polynomial division-free build"""
    # [n,p]_z = prod_{k=1}^{p} (1 - z^{n-p+k}) / (1 - z^k); build by Pascal recursion instead
    # [n,p] = [n-1,p-1] + z^p [n-1,p]
    memo={}
    def B(n,p):
        if p<0 or p>n: return lzero()
        if p==0 or p==n: return lone()
        if (n,p) in memo: return memo[(n,p)]
        r=ladd(B(n-1,p-1), lmul(lmono(zexp*p), B(n-1,p)))
        memo[(n,p)]=r
        return r
    return B(nn,p)

TYPES={
 "A2":  [[2,-1],[-1,2]],
 "B2":  [[2,-2],[-2,4]],
 "G2":  [[2,-3],[-3,6]],
 "A1A1":[[2,0],[0,2]],
}
print("Thm 4(1): ad_c expansion   ad_c(F_i)^n(F_j) = sum_p (-1)^p q_ii^C(p,2) q_ij^p [n,p]_{q_ii} F_i^{n-p} F_j F_i^p")
print()
tot=ok=0
for tname,form in TYPES.items():
    S=Setup(form,[[0,0],[0,0]])
    for (i,j) in [(0,1),(1,0)]:
        aii=S.truepair(tuple(1 if k==i else 0 for k in range(2)),tuple(1 if k==i else 0 for k in range(2)))
        aij=S.truepair(tuple(1 if k==i else 0 for k in range(2)),tuple(1 if k==j else 0 for k in range(2)))
        a_ij = 2*aij//aii          # Cartan integer
        n = 1 - a_ij
        # LHS: iterate the braided commutator
        Y={(j,):lone()}
        for _ in range(n): Y=adc(S,i,Y)
        # RHS: the closed formula
        R=defaultdict(lzero)
        for p in range(n+1):
            co=lmul(lmono(aii*comb(p,2)+aij*p), gauss_binom(n,p,aii))
            if p%2: co=lneg(co)
            w=tuple([i]*(n-p))+(j,)+tuple([i]*p)
            R[w]=ladd(R[w],co)
        R={w:c for w,c in R.items() if c}
        tot+=1
        match = (Y==R)
        if match: ok+=1
        print(f"  {tname:5s} (i,j)=({i+1},{j+1})  a_ij={a_ij}  n={n}  ad_c expansion matches: {match}")
print(f"\n  TOTAL {ok}/{tot}")

print()
print("POSITIVE CONTROL: unsymmetrised Cartan used as the braiding form (B2) -> expansion must break")
S=Setup([[2,-1],[-2,2]],[[0,0],[0,0]])   # not symmetric
for (i,j) in [(0,1)]:
    aii=S.truepair((1,0),(1,0)); aij=S.truepair((1,0),(0,1))
    n=1-2*aij//aii
    Y={(j,):lone()}
    for _ in range(n): Y=adc(S,i,Y)
    R=defaultdict(lzero)
    for p in range(n+1):
        co=lmul(lmono(aii*comb(p,2)+aij*p), gauss_binom(n,p,aii))
        if p%2: co=lneg(co)
        w=tuple([i]*(n-p))+(j,)+tuple([i]*p)
        R[w]=ladd(R[w],co)
    R={w:c for w,c in R.items() if c}
    print(f"  non-symmetric form, n={n}: matches = {Y==R}  (expect False)")
