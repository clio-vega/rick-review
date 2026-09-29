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
bad=0; tot=0
for n in range(0,8):
    for j in range(0,n+3):
        tot+=1
        lhs=(1-t**n)*c(n,j)
        r1=(1-s*t**(-j))*sum((s*t**(-j))**p*c(n-1-p,j) for p in range(0,n+2))
        r2=t**n*(1-s*t**(1-j))*sum((s*t**(1-j))**p*c(n-1-p,j-1) for p in range(0,n+2))
        d=sp.simplify(sp.cancel(lhs-(r1-r2)))
        if d!=0:
            bad+=1; print(f"FAIL n={n} j={j}: {d}", flush=True)
print(f"(star) Lemma 7: {tot} cases, 0<=n<=13, 0<=j<=n+2  ->  {bad} failures", flush=True)
