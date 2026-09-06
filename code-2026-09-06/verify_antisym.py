"""
Consequence of Rick's (*) that Day 167 does not state.

(*) says  G(c) := [deg_(u1,u2)=n-1]([T^n] log F_P|_{u3=c})  =  A_n c^2 + R_n c + C_n,
a QUADRATIC in c.  Rick uses c=0 and c=-1 to kill C_n, which leaves BOTH A_n and the
log-ratio term -- so his remaining queue has two items, (A) the xi_2 closure and
(B) the log(F_{-1}/F_0) closure.

But c^2 is EVEN and c is ODD.  So the ANTISYMMETRIC combination kills A_n AND C_n at once:
        G(c) - G(-c) = 2 R_n c
  =>    R^(-1)_n = (1/2c) [deg=n-1] ( [T^n] log( F_c / F_{-c} ) )     for any c != 0.

If this holds, term (A) -- the xi_2 / Xi closure -- is NOT needed for Missing Lemma (R).
"""
import sympy as sp
from sympy import Rational, symbols, expand, quo, factorial
u1,u2,u3 = symbols('u1 u2 u3'); U=(u1,u2,u3)
V=(u1-u2)*(u1-u3)*(u2-u3); e2=u1*u2+u1*u3+u2*u3
N=7
def rising(x,k):
    r=sp.Integer(1)
    for i in range(k): r*= (x+i)
    return r
def apply_T(poly):
    p=sp.Poly(expand(poly),*U); out=sp.Integer(0)
    for mono,coeff in zip(p.monoms(),p.coeffs()):
        t=coeff
        for x,k in zip(U,mono): t*=rising(x,k)
        out+=t
    return expand(out)
def exact_quo(num,den):
    q=quo(sp.Poly(num,*U),sp.Poly(den,*U)).as_expr()
    assert expand(q*den-num)==0
    return expand(q)
FP=[];e2n=sp.Integer(1)
for n in range(N+1):
    FP.append(expand(exact_quo(apply_T(expand(e2n*V)),V)/factorial(n))); e2n=expand(e2n*e2)
def series_log(F,N):
    G=[F[n] for n in range(N+1)];G[0]=sp.Integer(0)
    L=[sp.Integer(0)]*(N+1);P=[sp.Integer(0)]*(N+1);P[0]=sp.Integer(1)
    for r in range(1,N+1):
        Q=[sp.Integer(0)]*(N+1)
        for i in range(N+1):
            if P[i]==0: continue
            for j in range(1,N+1-i):
                if G[j]!=0: Q[i+j]+=P[i]*G[j]
        P=[expand(x) for x in Q]; s=Rational((-1)**(r-1),r)
        for n in range(N+1):
            if P[n]!=0: L[n]=L[n]+s*P[n]
    return [expand(x) for x in L]
def homog(poly,d,vars_=U):
    p=sp.Poly(expand(poly),*vars_); out=sp.Integer(0)
    for mono,coeff in zip(p.monoms(),p.coeffs()):
        if sum(mono)==d:
            t=coeff
            for x,k in zip(vars_,mono): t*=x**k
            out+=t
    return expand(out)
LF=series_log(FP,N)
X0={n:homog(LF[n],n) for n in range(1,N+1)}
Rm1={n:expand(sp.diff(X0[n],u3).subs({u3:0})) for n in range(2,N+1)}
Xi={n:homog(LF[n],n+1) for n in range(1,N+1)}
A={n:expand(Rational(1,2)*sp.diff(Xi[n],u3,2).subs({u3:0})) for n in range(2,N+1)}
def logFc(cv):
    Fc=[expand(FP[n].subs({u3:cv})) for n in range(N+1)]; assert Fc[0]==1
    return series_log(Fc,N)
cache={}
def LFc(cv):
    if cv not in cache: cache[cv]=logFc(cv)
    return cache[cv]

print("ANTISYMMETRIC FORM:  R^(-1)_n  ==  (1/2c) [deg=n-1] [T^n] log(F_c / F_{-c})")
print("(no Xi term, no xi_2, no term (A))\n")
allok=True
for cv in [1, 2, sp.Rational(1,2), 3, -1]:
    row=[]
    for n in range(2,N+1):
        diff=homog(expand(LFc(cv)[n]-LFc(-cv)[n]),n-1,(u1,u2))
        d=expand(Rm1[n]-Rational(1,2)/cv*diff)
        row.append(d==0); allok &= (d==0)
    print(f"  c={cv}:  n=2..{N}  ->  {'all OK' if all(row) else row}")
print(f"\n  => {'CONFIRMED for every c tested' if allok else 'FAILED'}")

print("\nNEGATIVE CONTROLS (must fail):")
bad=0
for n in range(2,6):
    diff=homog(expand(LFc(1)[n]-LFc(-1)[n]),n-1,(u1,u2))
    if expand(Rm1[n]-diff)==0: bad+=1; print(f"   n={n}: dropping the 1/(2c) still passes -- DEGENERATE")
    # symmetric combination should NOT give R (it gives 2A c^2 + 2C, not R)
    s=homog(expand(LFc(1)[n]+LFc(-1)[n]),n-1,(u1,u2))
    if expand(Rm1[n]-Rational(1,2)*s)==0: bad+=1; print(f"   n={n}: the SYMMETRIC combination also gives R -- DEGENERATE")
print(f"   -> {'PASS: controls failed as they should' if bad==0 else f'{bad} wrongly passed'}")

print("\nSANITY: the SYMMETRIC combination should recover A_n and C_n, not R_n:")
for n in range(2,6):
    s=homog(expand(LFc(1)[n]+LFc(-1)[n]),n-1,(u1,u2))
    z=homog(expand(LFc(0)[n]),n-1,(u1,u2))
    # G(1)+G(-1) = 2A + 2C ; G(0) = C  =>  A = (G(1)+G(-1))/2 - G(0)
    d=expand(A[n]-(Rational(1,2)*s - z))
    print(f"   n={n}: A_n from symmetric part, difference = {d}  {'OK' if d==0 else '*** MISMATCH ***'}")
