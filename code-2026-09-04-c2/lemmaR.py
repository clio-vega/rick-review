"""JOB 1 step 2-3: reproduce Day 162 Thm B / Missing Lemma (R) from the DEFINITION of F_P,
and try to refute it.  Third pipeline (mine), no code of Rick's."""
import sys, time; sys.path.insert(0,'/home/clio/projects/reviews/code-2026-09-04')
import sympy as sp
from fp_lib import *

N = int(sys.argv[1]) if len(sys.argv)>1 else 10
E1,E2 = sp.symbols('E1 E2')
t0=time.time()
F = FP_coeffs(N); print(f"F_P to T^{N-1}: {time.time()-t0:.1f}s")
L = logs(F, N)                    # log F_P, 3 variables
X0 = layer(L, 0)                  # weight-0 layer: at [T^n], u-degree n
Xi = layer(L, 1)

# ---- R^(-1) := d/du3 X^(0) |_{u3=0}, as a series in T with coeffs in Q[u1,u2] ----
Rm1 = [sp.expand(sp.diff(c,u3).subs(u3,0)) for c in X0]

# ---- Rick's closed form, built in the 2-variable slice ----
def series_Y(N):
    """Y = T*phi(Y), phi=1+E1 Y+E2 Y^2 ; return [T^0..T^{N-1}] coeffs."""
    Y=[sp.Integer(0)]*N
    for n in range(1,N):
        # Y = T*(1+E1*Y+E2*Y^2) ; iterate
        pass
    Y=[sp.Integer(0)]*N
    for it in range(N+2):
        Y2 = mul(Y,Y,N)
        newY=[sp.Integer(0)]*N
        for n in range(1,N):
            newY[n]= sp.expand(( (1 if n-1==0 else 0) + (E1*Y[n-1] if n-1>=0 else 0) + E2*Y2[n-1]))
        Y=newY
    return Y
Y = series_Y(N)
# check Y = T phi(Y)
chk = [sp.expand(Y[n] - ((1 if n==1 else 0) + (E1*Y[n-1] if n>=1 else 0) + (mul(Y,Y,N)[n-1] if n>=1 else 0)*E2)) for n in range(N)]
assert all(c==0 for c in chk), "Y series wrong"

def smul(A,B): return mul(A,B,N)
def sconst(c): return [sp.expand(c)]+[sp.Integer(0)]*(N-1)
def sT(k):  # T^k
    a=[sp.Integer(0)]*N
    if k<N: a[k]=sp.Integer(1)
    return a
def sadd(*As): return [sp.expand(sum(A[i] for A in As)) for i in range(N)]
def sneg(A): return [sp.expand(-a) for a in A]

q = sadd(sconst(1), sneg(smul(sT(1),sconst(E1))), sneg(smul(smul(sT(1),sconst(2*E2)),Y)))
assert q[0]==1
# sanity (Day158 Q1): q^2 = (1-E1 T)^2 - 4 E2 T^2
q2 = smul(q,q)
tgt = sadd(sconst(1), sneg(smul(sT(1),sconst(2*E1))), smul(sT(2),sconst(E1**2-4*E2)))
print("  (Q1) q^2 = (1-E1T)^2-4E2T^2 :", all(sp.expand(q2[i]-tgt[i])==0 for i in range(N)))

R1R2 = sadd(sconst(1), sneg(smul(sT(2),sconst(E1**2-4*E2))))
qinv = inv(q,N); q3inv = smul(qinv,smul(qinv,qinv))
Y2 = smul(Y,Y)
qp1 = sadd(q,sconst(1))
bracket = sadd( smul(sconst(E2),smul(Y2, sadd(smul(qp1,qp1), sneg(smul(sT(1),sconst(E1)))))),
                [sp.Rational(1,2)*x for x in sadd(q,R1R2)] )
RHS = smul(sT(1), smul(q3inv, bracket))

# ---- compare, substituting E1->u1+u2, E2->u1*u2 ----
sub = {E1:u1+u2, E2:u1*u2}
print("\n n :  R^(-1)_n (from definition)   vs  Rick's (R)")
bad=[]
for n in range(N):
    lhs = sp.expand(Rm1[n])
    rhs = sp.expand(RHS[n].subs(sub))
    ok = sp.expand(lhs-rhs)==0
    if not ok: bad.append(n)
    if n<=4: print(f"  n={n}: lhs={sp.factor(lhs)}   rhs={sp.factor(rhs)}  match={ok}")
    else: print(f"  n={n}: match={ok}")
print("\nMISSING LEMMA (R):", "HOLDS to n<=%d"%(N-1) if not bad else f"FAILS at n={bad}")

# ---- also: bar D |_{E3=0} table vs Rick's Day 162 table ----
logW_slice = None
