import sympy as sp, itertools
from sympy import symbols, Integer as I
q,t=symbols('q t'); s=1/q
def poch(a,n): return sp.prod([1-a*t**i for i in range(n)]) if n>0 else I(1)
def alpha(j):
    if j<0: return I(0)
    return sp.cancel(sp.prod([s-t**i for i in range(1,j+1)])/poch(t,j))
def c(n,j):
    if j<0 or j>n or n<0: return I(0)
    return sp.cancel(poch(s,n-j)/poch(t,n-j)*(alpha(j)-s*t**(n-j)*alpha(j-1)))
def F(n,w): return sp.cancel(sum(c(n,j)*w**j for j in range(n+1)))
def ee(n,X):
    m=len(X)
    if n<0 or n>m: return I(0)
    return sp.expand(sp.symmetric_poly(n,*X)) if n>0 else I(1)

print("Is the FULL right-hand side regular at t=0 when r<k, and does the P.S. collapse hold?")
print("(P.S. claim: e_k*e_r  ->  sum_{b<k}(1-s)s^b e_b e_{r+k-b} + s^k e_k e_r  at t=0, for r>=k)\n")
for (k,r,m) in [(2,0,4),(2,1,4),(3,0,5),(3,1,5),(3,2,5),(3,3,6),(4,1,6),(4,2,6),(4,4,8)]:
    X=symbols('X1:%d'%(m+1))
    full=sum(s**b*F(k-b,t**(r-b))*ee(b,X)*ee(r+k-b,X) for b in range(k+1))
    full=sp.cancel(sp.together(sp.expand(full)))
    lim=sp.simplify(sp.limit(full,t,0))
    pred=sp.expand(sum((1-s)*s**b*ee(b,X)*ee(r+k-b,X) for b in range(k))+s**k*ee(k,X)*ee(r,X))
    d=sp.simplify(sp.expand(lim-pred))
    print(f"k={k} r={r} m={m}  r>=k? {r>=k:<5}  RHS regular at t=0: {lim is not sp.nan}   P.S. collapse holds: {d==0}")
    if d!=0:
        print(f"      residual (t=0 truth  MINUS  P.S. formula) = {sp.factor(d)}")
