"""(a) verify Day 162 Theorem B on my pipeline; (b) hunt the ODE for the TRUE F_1."""
import sympy as sp
from fp_lib import *

N = 10
F = FP_coeffs(N)
E1s, E2s = u1+u2, u1*u2

# ---- F_0 and the TRUE F_1 = d_{u3} F_P |_{u3=0} ----
F0 = [sp.expand(c.subs(u3,0)) for c in F]
F1 = [sp.expand(sp.diff(c,u3).subs(u3,0)) for c in F]
print("[T^k] F_1 (true), k=0..3:", [sp.factor(F1[k]) for k in range(4)])
naiveF1 = [sp.expand(sp.Rational(sum(sp.Rational(1,j) for j in range(1,k+1)) if k else 0)
                     * rising(u1+1,k)*rising(u2+1,k)/sp.factorial(k)) for k in range(N)]
print("Day160's F_1 = sum T^k/k! H_k A_k A_k, k=0..3:", [sp.factor(naiveF1[k]) for k in range(4)])
print("agree? ", [sp.simplify(F1[k]-naiveF1[k])==0 for k in range(4)])

def dT(A):
    return [sp.expand((n+1)*A[n+1]) for n in range(len(A)-1)] + [sp.Integer(0)]
def mulT(A, k):          # multiply by T^k
    return ([sp.Integer(0)]*k + A)[:len(A)]

def LA(Fs):
    """Day 158 operator (A): T^2 F'' + [(E1+3)T - 1] F' + (1+E1+E2) F, 2-variable E's."""
    Fp, Fpp = dT(Fs), dT(dT(Fs))
    out = []
    for n in range(N):
        t  = mulT(Fpp,2)[n]
        t += (E1s+3)*mulT(Fp,1)[n] - Fp[n]
        t += (1+E1s+E2s)*Fs[n]
        out.append(sp.expand(t))
    return out

print("\nCHECK: L_A[F_0] == 0 (Day 158 Prop A) :", all(sp.simplify(c)==0 for c in LA(F0)[:N-2]))
res = LA(F1)
print("residual L_A[F_1], n=0..5:", [sp.factor(res[n]) for n in range(6)])
print("compare T*F_0' , n=0..5:", [sp.factor(mulT(dT(F0),1)[n]) for n in range(6)])
print("compare F_0    , n=0..5:", [sp.factor(F0[n]) for n in range(6)])

# solve for res = alpha(T) F_0 + beta(T) F_0' with alpha,beta polynomial in T over Q[E1,E2]
Fp0 = dT(F0)
print("\nresidual / F_0 ratios n=0..5:", [sp.simplify(res[n]/F0[n]) if F0[n]!=0 else None for n in range(6)])
