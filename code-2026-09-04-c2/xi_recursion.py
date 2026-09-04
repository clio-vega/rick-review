"""Last ingredient of Route (v): is d^2_{u3} Xi|_{u3=0} determined by PROVED inputs?
Xi = sum_k E3^k xi_k(E1,E2).  Day158 Thm1 gives xi_0.  Day152 ThmC gives log W in 3 vars,
and (P1) log W = dpartial Xi with dpartial = sum_i d_{u_i}.  Since dpartial E1=3, E2->2E1, E3->E2:
   [E3^k] log W = (k+1) E2 xi_{k+1} + 3 d_{E1} xi_k + 2 E1 d_{E2} xi_k
so xi_0 -> xi_1 -> xi_2 -> ... recursively.  Verify the recursion, then verify that
xi_0,xi_1,xi_2 reproduce d^2_{u3}Xi|_0."""
import sys; sys.path.insert(0,'/home/clio/projects/reviews/code-2026-09-04')
import sympy as sp
from fp_lib import *
from sympy.polys.polyfuncs import symmetrize
N=9
E1,E2,E3=sp.symbols('E1 E2 E3')
F=FP_coeffs(N); L=logs(F,N); Xi=layer(L,1)
H=mul([c.subs({u1:u1+1,u2:u2+1,u3:u3+1}) for c in F], inv(F,N), N)
logW = layer(logs(H,N),0)
def toE(e):
    s,rem,_=symmetrize(sp.expand(e),us,formal=True,symbols=[E1,E2,E3])
    assert sp.simplify(rem)==0; return sp.expand(s)
def xis(expr):           # expr in E1,E2,E3 -> list of xi_k
    p=sp.Poly(expr,E3); d={}
    for m,c in zip(p.monoms(),p.coeffs()): d[m[0]]=sp.expand(c)
    return d
print("(P1) log W = (sum_i d_ui) Xi ?",
      all(sp.expand(logW[n]-sum(sp.diff(Xi[n],v) for v in us))==0 for n in range(N)))
print("\nrecursion  [E3^k] logW = (k+1)E2 xi_{k+1} + 3 d_E1 xi_k + 2 E1 d_E2 xi_k")
okR=True; okD=True
for n in range(1,N):
    xi=xis(toE(Xi[n])); lw=xis(toE(logW[n]))
    for k in range(0,4):
        a=xi.get(k,sp.Integer(0)); b=xi.get(k+1,sp.Integer(0))
        lhs=lw.get(k,sp.Integer(0))
        rhs=sp.expand((k+1)*E2*b + 3*sp.diff(a,E1) + 2*E1*sp.diff(a,E2))
        if sp.expand(lhs-rhs)!=0: okR=False; print("   FAIL n=%d k=%d"%(n,k))
    # d^2_{u3} Xi|_0 from xi_0,xi_1,xi_2 only
    s_,p_=sp.symbols('s_ p_')
    x0,x1,x2=[xi.get(i,sp.Integer(0)) for i in (0,1,2)]
    pred=(sp.diff(x0,E1,2) + s_**2*sp.diff(x0,E2,2) + 2*p_**2*x2
          + 2*s_*sp.diff(sp.diff(x0,E1),E2) + 2*p_*sp.diff(x1,E1) + 2*s_*p_*sp.diff(x1,E2))
    pred=sp.expand(pred.subs({s_:u1+u2,p_:u1*u2,E1:u1+u2,E2:u1*u2}))
    true=sp.expand(sp.diff(Xi[n],u3,2).subs(u3,0))
    if sp.expand(pred-true)!=0: okD=False; print("   d2 FAIL n=%d"%n)
print("   recursion  VERIFIED to T^%d: %s"%(N-1,okR))
print("   d^2_{u3}Xi|_0 from xi_0,xi_1,xi_2  VERIFIED to T^%d: %s"%(N-1,okD))
