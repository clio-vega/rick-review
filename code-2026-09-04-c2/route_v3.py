"""(A) corrected: the k=0 term of the closed form is exceptional (u^(k)=u(u+1)B_{k-2}(u)
needs k>=2; at k=1 the factor (1-k) kills it, at k=0 it does not).  Corrected relation:
  F_{-1} = [ p F_0 - p(s+1) T F_0 - 2p T^2 F_0' + p(s+1) int_0^T F_0 + (s+1) ] / ((u1+1)(u2+1))
and then the sharpened claim with ell_{-1}(log F_0) cancelling."""
import sys; sys.path.insert(0,'/home/clio/projects/reviews/code-2026-09-04')
import sympy as sp
from fp_lib import *
N = 11
F = FP_coeffs(N)
p_, s_ = u1*u2, u1+u2
den = (u1+1)*(u2+1)
F0  = [sp.expand(c.subs(u3,0))  for c in F]
Fm1 = [sp.expand(c.subs(u3,-1)) for c in F]
def dT(A):   return [sp.expand((i+1)*A[i+1]) if i+1<N else sp.Integer(0) for i in range(N)]
def intT(A): return [sp.Integer(0)] + [sp.expand(A[i-1]/i) for i in range(1,N)]
def sh(A,k): return [sp.Integer(0)]*k + [A[i] for i in range(N-k)]
F0p = dT(F0)
rhs = [sp.cancel(sp.together((p_*F0[i] - p_*(s_+1)*sh(F0,1)[i] - 2*p_*sh(F0p,2)[i]
        + p_*(s_+1)*intT(F0)[i] + ((s_+1) if i==0 else 0))/den)) for i in range(N)]
okA = all(sp.simplify(sp.together(Fm1[i]-rhs[i]))==0 for i in range(N))
print("(A-corrected) F_{-1} as an explicit operator on F_0 :", "VERIFIED to T^%d"%(N-1) if okA else "FAILS")

# ratio built ONLY from F_0
one=[sp.Integer(1)]+[sp.Integer(0)]*(N-1)
G = mul(F0p, inv(F0,N), N); J = mul(intT(F0), inv(F0,N), N); Finv=inv(F0,N)
ratio = [sp.cancel(sp.together((p_*one[i] - p_*(s_+1)*sh(one,1)[i] - 2*p_*sh(G,2)[i]
          + p_*(s_+1)*J[i] + ((s_+1)*Finv[i]))/den)) for i in range(N)]
true_ratio = mul(Fm1, inv(F0,N), N)
print("ratio == F_{-1}/F_0 ?", all(sp.simplify(sp.together(ratio[i]-true_ratio[i]))==0 for i in range(N)))

L = logs(F,N); Xi=layer(L,1); X0=layer(L,0)
lr = logs(true_ratio,N)   # ratio[0]=1 since Fm1[0]=F0[0]=1
print("\nSHARPENED CLAIM:  R^(-1)_n = (1/2) d^2_{u3} Xi_n|0  -  [deg n-1]([T^n] log(F_{-1}/F_0))")
ok=True
for n in range(1,N):
    lhs = sp.expand(sp.diff(X0[n],u3).subs(u3,0))
    t1  = sp.expand(sp.diff(Xi[n],u3,2).subs(u3,0)/2)
    t2  = homog(sp.expand(sp.cancel(sp.together(lr[n]))), n-1, vars=(u1,u2))
    good = sp.expand(sp.cancel(sp.together(lhs-(t1-t2))))==0
    ok &= good; print(f"   n={n}: {good}")
print("  ==>", "VERIFIED to T^%d"%(N-1) if ok else "FAILS")
