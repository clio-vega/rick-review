import sympy as sp
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

print("Sharpening the P.S. caveat.  He states the t=0 collapse for r >= k.")
print("Testing every (k,r) with k<=5, r<=k+1, in m = 2k variables (so no e_n truncates):\n")
print(" k   r   r>=k   r>=k-1   collapse holds?")
for k in range(1,6):
    for r in range(0,k+2):
        m=2*k+1
        X=symbols('X1:%d'%(m+1))
        full=sp.cancel(sp.together(sp.expand(
            sum(s**b*F(k-b,t**(r-b))*ee(b,X)*ee(r+k-b,X) for b in range(k+1)))))
        lim=sp.simplify(sp.limit(full,t,0))
        pred=sp.expand(sum((1-s)*s**b*ee(b,X)*ee(r+k-b,X) for b in range(k))+s**k*ee(k,X)*ee(r,X))
        ok=(sp.simplify(sp.expand(lim-pred))==0)
        print(f" {k}   {r}   {str(r>=k):<5}  {str(r>=k-1):<6}   {ok}")
