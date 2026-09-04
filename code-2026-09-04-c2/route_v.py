"""Route (v): the second degenerate slice u3=-1, and what it buys."""
import sys; sys.path.insert(0,'/home/clio/projects/reviews/code-2026-09-04')
import sympy as sp
from fp_lib import *

N = 11
F = FP_coeffs(N)
p_, s_ = u1*u2, u1+u2
F0  = [sp.expand(c.subs(u3,0))  for c in F]
Fm1 = [sp.expand(c.subs(u3,-1)) for c in F]

def dT(A):   return [sp.expand((i+1)*A[i+1]) if i+1<N else sp.Integer(0) for i in range(N)]
def intT(A): return [sp.Integer(0)] + [sp.expand(A[i-1]/i) for i in range(1,N)]
def shiftT(A,k): return [sp.Integer(0)]*k + [A[i] for i in range(N-k)]
F0p = dT(F0)
rhs = [sp.expand(p_/((u1+1)*(u2+1))*(
        F0[i] - (s_+1)*shiftT(F0,1)[i] - 2*shiftT(F0p,2)[i] + (s_+1)*intT(F0)[i]))
       for i in range(N)]
print("(A) F_{-1} = p/((u1+1)(u2+1))[F_0-(s+1)T F_0-2T^2 F_0'+(s+1)int_0^T F_0]")
okA=True
for n in range(N):
    ok = sp.simplify(sp.together(Fm1[n]-rhs[n]))==0
    okA &= ok
print("    T^0..T^%d all match: %s"%(N-1,okA))

L   = logs(F,N)
Xi  = layer(L,1); X0 = layer(L,0); Xm1 = layer(L,-1)
Lm1 = logs(Fm1,N)
print("\n  sanity: log(F_P|_{u3=-1}) == (log F_P)|_{u3=-1} ?",
      all(sp.expand(Lm1[n]-L[n].subs(u3,-1))==0 for n in range(N)))

def deg_part(expr,j): return homog(expr,j,vars=(u1,u2))
print("\n(B) Lambda_{n,n-1} = (1/2)d^2_{u3}Xi_n|0 - d_{u3}X0_n|0 + X^{(-1)}_n|_{u3=0}")
okB=True
for n in range(1,N):
    lam  = deg_part(sp.expand(Lm1[n]), n-1)
    t1   = sp.expand(sp.diff(Xi[n],u3,2).subs(u3,0)/2)
    t2   = sp.expand(sp.diff(X0[n],u3).subs(u3,0))
    t3   = sp.expand(Xm1[n].subs(u3,0))
    ok   = sp.expand(lam-(t1-t2+t3))==0
    okB &= ok
    print(f"    n={n}: {ok}")
print("    ==>", "VERIFIED" if okB else "FAILS")

# also: top two degrees are consistency checks on Day158 Thm1/2 + Day161 Thm1
print("\n(B') consistency: Lambda_{n,n+1}=Xi_n|_{u3=0} ; Lambda_{n,n} = -d_{u3}Xi_n|0 + X0_n|_{u3=0}")
for n in range(1,7):
    a = sp.expand(deg_part(Lm1[n],n+1) - Xi[n].subs(u3,0))==0
    b = sp.expand(deg_part(Lm1[n],n) - (-sp.diff(Xi[n],u3).subs(u3,0) + X0[n].subs(u3,0)))==0
    print(f"    n={n}: {a} {b}")
