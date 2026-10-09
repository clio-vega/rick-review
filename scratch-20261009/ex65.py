import sys, sympy as sp
sys.path.insert(0,'/home/clio/projects/reviews/code-20261008')
from jingliu import D_coeffs
t=sp.Symbol('t')

def X_jingliu(lam, rho):
    """My own 10-06 implementation, independently verified 102/102."""
    m,k = lam[0], lam[1]
    D = D_coeffs(rho, k)
    return sp.expand((t-1)*sum(D[i]*t**(k-1-i) for i in range(k)) + D[k])

def X_rick_ex65(lam, x, y):
    """Rick's Example 6.5 piecewise formula, y<=x."""
    l1,l2 = lam
    m_xy = 2 if x==y else 1
    if y <  l2: return sp.expand((t-1)*t**(l2-1-y)*(1+t**y))
    if y == l2: return sp.expand(m_xy - (1-t)*t**(l2-1))
    return sp.expand((t-1)*t**(l2-1))

ok=bad=0; fails=[]
for n in range(2,13):
    for l2 in range(1,n//2+1):
        l1=n-l2
        if l1<l2: continue
        for y in range(1,n//2+1):
            x=n-y
            if x<y: continue
            a=X_jingliu((l1,l2),(x,y)); b=X_rick_ex65((l1,l2),x,y)
            if sp.simplify(a-b)==0: ok+=1
            else: bad+=1; fails.append(((l1,l2),(x,y),a,b))
print("Example 6.5 vs my independently-verified Jing-Liu engine, |lambda|<=12, two-part classes")
print("  agree: %d   DISAGREE: %d" % (ok,bad))
for f in fails[:6]: print("   ",f)
print()
print("Control - can this comparison fail?  perturb Rick's y=lambda_2 branch by +1:")
def X_bad(lam,x,y):
    v=X_rick_ex65(lam,x,y)
    return v+1 if y==lam[1] else v
c=sum(1 for n in range(2,9) for l2 in range(1,n//2+1) for y in range(1,n//2+1)
      if (l1:=n-l2)>=l2 and (x:=n-y)>=y and sp.simplify(X_jingliu((l1,l2),(x,y))-X_bad((l1,l2),x,y))!=0)
print("   perturbed version disagrees in %d instances (must be >0 for the test to have power)" % c)
