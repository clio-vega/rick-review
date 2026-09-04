"""NEW: closed form for F_P on the SECOND degenerate slice u3 = -1.
Rationale: Tplus sends u3^c -> u3^(c) = u3(u3+1)...(u3+c-1), which vanishes at u3=-1
for every c>=2.  So u3=-1 is degenerate in exactly the way u3=0 is (there only c>=1 dies),
and the slice is a 2-variable Tplus computation of the same type as Day 158's.

CLAIM (mine).  With p=u1u2, s=u1+u2, B_m(u) := (u+2)^(m) = (u+2)(u+3)...(u+m+1),
   [T^k] F_P|_{u3=-1} = (p/k!) [ B_{k-1}(u1)B_{k-1}(u2) + (1-k)(s+2k+1) B_{k-2}(u1)B_{k-2}(u2) ]
for k>=1 (B_0=1, B_{-1} term absent at k=1 since (1-k)=0), and = 1 for k=0.
Equivalently with Day 158's A_k(u) = (u+1)^(k):
   [T^k] F_P|_{u3=-1} = p/((u1+1)(u2+1) k!) [ A_k A_k + (1-k)(s+2k+1) A_{k-1}A_{k-1} ].
"""
import sys; sys.path.insert(0,'/home/clio/projects/reviews/code-2026-09-04')
import sympy as sp
from fp_lib import *

N = 11
F = FP_coeffs(N)
p_, s_ = u1*u2, u1+u2
def B(u,m):
    r=sp.Integer(1)
    for j in range(m): r*= (u+2+j)
    return r
def A(u,k):
    r=sp.Integer(1)
    for j in range(k): r*=(u+1+j)
    return r

print("k :  match(closed form vs F_P|_{u3=-1})    [and the A_k form]")
allok=True
for k in range(N):
    lhs = sp.expand(F[k].subs(u3,-1))
    if k==0:
        rhs = sp.Integer(1)
    else:
        rhs = sp.expand(p_/sp.factorial(k)*( B(u1,k-1)*B(u2,k-1)
              + (1-k)*(s_+2*k+1)*(B(u1,k-2)*B(u2,k-2) if k>=2 else 0) ))
    ok = sp.expand(lhs-rhs)==0
    # A_k version
    if k==0: rhs2=sp.Integer(1)
    else:
        rhs2 = sp.expand(sp.together(p_/((u1+1)*(u2+1)*sp.factorial(k))*(A(u1,k)*A(u2,k)
               + (1-k)*(s_+2*k+1)*(A(u1,k-1)*A(u2,k-1) if k>=1 else 0))))
    ok2 = sp.simplify(sp.together(lhs-rhs2))==0
    allok &= (ok and ok2)
    print(f"  k={k}: B-form {ok}   A-form {ok2}")
print("\nCLOSED FORM ON THE u3=-1 SLICE:", "VERIFIED to T^%d"%(N-1) if allok else "FAILS")

# --- what it buys: D_n is homogeneous of degree n, so the single slice u3=-1
#     determines D_n COMPLETELY (dehomogenisation).  Demonstrate.
L = logs(F,N); X0 = layer(L,0)
print("\n--- dehomogenisation check: X0_n recovered from its own u3=-1 restriction ---")
for n in range(1,7):
    g = sp.expand(X0[n].subs(u3,-1))         # poly in u1,u2 of degree <= n
    # rebuild:  X0_n(u) = (-u3)^n * g(u1/(-u3), u2/(-u3))
    rebuilt = sp.expand(((-u3)**n * g.subs({u1:u1/(-u3), u2:u2/(-u3)})).rewrite(sp.Pow))
    rebuilt = sp.expand(sp.simplify(rebuilt))
    print(f"  n={n}: recovered == X0_n ?  {sp.expand(rebuilt-X0[n])==0}")
