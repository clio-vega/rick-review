exec(open('rick_Wr_check.py').read().split('# ---------- checks ----------')[0])
import sympy as sp, itertools
from sympy import Integer as I

def poch(a,n):           # (a;t)_n
    return sp.prod([1 - a*t**i for i in range(n)]) if n>0 else I(1)
def alpha(j):
    if j<0: return I(0)
    return sp.cancel(sp.prod([s - t**i for i in range(1,j+1)])/poch(t,j))
def c(n,j):
    if j<0 or j>n or n<0: return I(0)
    return sp.cancel(poch(s,n-j)/poch(t,n-j)*(alpha(j) - s*t**(n-j)*alpha(j-1)))
def F(n,w):
    return sp.cancel(sum(c(n,j)*w**j for j in range(0,n+1)))

print("=== CHECK E: Lemma 7 (star), the one-index q-series identity ===")
bad=0
for n in range(0,14):
    for j in range(0,n+3):
        lhs=(1-t**n)*c(n,j)
        r1=(1-s*t**(-j))*sum((s*t**(-j))**p*c(n-1-p,j) for p in range(0,n+2))
        r2=t**n*(1-s*t**(1-j))*sum((s*t**(1-j))**p*c(n-1-p,j-1) for p in range(0,n+2))
        d=sp.simplify(sp.cancel(lhs-(r1-r2)))
        if d!=0: print(f"  FAIL n={n} j={j} diff={d}"); bad+=1
print(f"  (star) verified for 0<=n<=13, 0<=j<=n+2  (includes n=0 and j>n, both outside his stated n>=1): {bad} failures")

print()
print("=== CHECK F: Theorem 1 of UID 732 vs direct AHA computation ===")
def ekY_dot(k, r, X):
    m=len(X)
    if k>m: return I(0)
    Fr=e(r,X) if r<=m else I(0)
    tot=I(0)
    for combo in itertools.combinations(range(1,m+1),k):
        G=Fr
        for i in reversed(combo):     # Y_{b1}...Y_{bk}, rightmost acts first
            G=Y(G,i,X)
        tot+=G
    return sp.cancel(tot/t**sp.binomial(k,2))
def rhs_thm(k,r,X):
    return sp.expand(sp.cancel(sum(s**b*F(k-b,t**(r-b))*e(b,X)*e(r+k-b,X) for b in range(0,k+1))))

for m in [1,2,3]:
    X=mkvars(m)
    for k in range(1,m+3):
        for r in range(0,m+3):
            d=sp.simplify(sp.cancel(ekY_dot(k,r,X)-rhs_thm(k,r,X)))
            flag="OK " if d==0 else "FAIL"
            note=" [k>m]" if k>m else ("" if r>=k else " [r<k]")
            print(f"  {flag} m={m} k={k} r={r}{note}")
            assert d==0,(m,k,r,d)
print("  F: all pass, INCLUDING k>m and r<k")
