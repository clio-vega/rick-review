"""Route (v), sharpened.  CLAIM:
    R^(-1)_n = (1/2) d^2_{u3} Xi_n|_{u3=0}  -  [deg_{(u1,u2)}=n-1 part of] [T^n] log(F_{-1}/F_0)
with  F_{-1}/F_0 = p/((u1+1)(u2+1)) * [ 1 - (s+1)T - 2T^2 (F_0'/F_0) + (s+1)(int_0^T F_0)/F_0 ].
The unknown layer ell_{-1}(log F_0) CANCELS.  Everything on the RHS is 2-variable and built
from Day 158's own G = F_0'/F_0 plus J = (int F_0)/F_0, and from Xi (Day152 ThmC + Day158 Thm1).
"""
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
def sh(A,k): return [sp.Integer(0)]*k + [A[i] for i in range(N-k)]

# ratio, built ONLY from F_0
G = mul(dT(F0), inv(F0,N), N)          # F_0'/F_0
J = mul(intT(F0), inv(F0,N), N)        # (int_0^T F_0)/F_0
one = [sp.Integer(1)]+[sp.Integer(0)]*(N-1)
ratio = [sp.expand(p_/((u1+1)*(u2+1))*(
          one[i] - (s_+1)*sh(one,1)[i] - 2*sh(G,2)[i] + (s_+1)*J[i])) for i in range(N)]
print("ratio == F_{-1}/F_0 ?",
      all(sp.simplify(sp.together(ratio[i]-mul(Fm1,inv(F0,N),N)[i]))==0 for i in range(N)))

L  = logs(F,N); Xi = layer(L,1); X0 = layer(L,0)
# log of ratio: ratio[0] = p/((u1+1)(u2+1)) != 1, so normalise
c0 = ratio[0]
rn = [sp.expand(sp.cancel(r/c0)) for r in ratio]
logratio = [sp.expand(sp.log(c0) if i==0 else 0) for i in range(N)]
lr = logs(rn,N)
print("\nCLAIM:  R^(-1)_n = (1/2)d^2_{u3}Xi_n|0 - [deg n-1]([T^n] log(F_{-1}/F_0))")
ok=True
for n in range(1,N):
    lhs = sp.expand(sp.diff(X0[n],u3).subs(u3,0))
    t1  = sp.expand(sp.diff(Xi[n],u3,2).subs(u3,0)/2)
    # log(F_{-1}/F_0) at T^n for n>=1 equals lr[n] (constant-in-T term is log c0, n=0 only)
    t2  = homog(sp.expand(sp.cancel(sp.together(lr[n]))), n-1, vars=(u1,u2))
    r   = sp.expand(sp.cancel(sp.together(lhs-(t1-t2))))
    good = r==0
    ok &= good
    print(f"   n={n}: {good}")
print("  ==>", "VERIFIED to T^%d"%(N-1) if ok else "FAILS")
