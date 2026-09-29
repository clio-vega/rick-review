exec(open('rick_Wr_check.py').read().split('# ---------- checks ----------')[0])
import sympy as sp
from sympy import Integer as I
def e1Y(F,X):
    m=len(X); return sp.cancel(sum(Y(F,i,X) for i in range(1,m+1)))
def br(n): return sp.cancel((1-t**n)/(1-t)) if n>0 else I(0)   # his [n]=0 for n<=0
print("UID 731 Theorem 1:  C_r = e1 * e1 * e_r  (operator reading e1(Y).(e1(Y).e_r))")
for m in [2,3,4]:
    X=mkvars(m)
    for r in range(1,m+3):
        Fr = e(r,X) if r<=m else I(0)
        lhs = e1Y(e1Y(Fr,X),X)
        rhs = (s**3*e(r,X)*e(1,X)**2
             + s**2*(1-s)*br(2)*e(r,X)*e(2,X)
             + s*(1-s)*(br(r+1)+t*br(r)+s)*e(r+1,X)*e(1,X)
             + (1-s)**2*br(r+2)*(br(r+1)+s)*e(r+2,X))
        d=sp.simplify(sp.cancel(lhs-sp.expand(rhs)))
        print(f"  m={m} r={r}: diff={d}")
