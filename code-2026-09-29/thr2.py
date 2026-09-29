"""t=0 collapse threshold, done in FREE Lambda: group the k+1 terms by the unordered
pair {b, r+k-b} (the products e_b e_{r+k-b} coincide exactly when b' = r+k-b), sum the
coefficients within each class -- individual ones have poles at t=0, class sums do not --
then take t->0 and compare with the P.S. formula grouped the same way."""
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
def Ff(n,w): return sp.cancel(sum(c(n,j)*w**j for j in range(n+1)))
print(" k   r   r>=k   r=k-1   collapse holds at t=0?", flush=True)
for k in range(1,7):
    for r in range(0,k+2):
        classes={}
        for b in range(k+1):
            key=tuple(sorted((b, r+k-b)))
            classes.setdefault(key,[I(0),I(0)])
            classes[key][0]+= s**b*Ff(k-b, t**(r-b))
            classes[key][1]+= ((1-s)*s**b if b<k else s**k)
        ok=True
        for key,(true_c,pred_c) in classes.items():
            lim=sp.simplify(sp.limit(sp.cancel(sp.together(true_c)), t, 0))
            if sp.simplify(lim-pred_c)!=0: ok=False
        mark="  <-- r=k-1" if r==k-1 else ""
        print(f" {k}   {r}   {str(r>=k):<5}  {str(r==k-1):<6}  {ok}{mark}", flush=True)
print("DONE", flush=True)
