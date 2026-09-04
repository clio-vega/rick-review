import sympy as sp
from fp_lib import *
N = 10
F = FP_coeffs(N)
E1s, E2s = u1+u2, u1*u2

logF = logs(F,N); Xi = layer(logF,1); X0 = layer(logF,0)
Ftau=[sp.expand(c.subs({u1:u1+1,u2:u2+1,u3:u3+1},simultaneous=True)) for c in F]
H = mul(Ftau, inv(F,N), N); W = layer(H,0); logW3 = logs(W,N)

# Y, q, phi  (2-variable)
Y=[sp.Integer(0)]*N
for _ in range(N+1):
    Y2=mul(Y,Y,N)
    phi=[sp.expand((1 if i==0 else 0)+E1s*Y[i]+E2s*Y2[i]) for i in range(N)]
    Y=[sp.Integer(0)]+[phi[i] for i in range(N-1)]
Y2=mul(Y,Y,N)
phi=[sp.expand((1 if i==0 else 0)+E1s*Y[i]+E2s*Y2[i]) for i in range(N)]
q=[sp.expand((1 if i==0 else 0)-(E1s if i==1 else 0)-2*E2s*(Y[i-1] if i>=1 else 0)) for i in range(N)]

# ---- Theorem B: barD|_{E3=0} = T Y^2[(q+1)^2 - E1 T]/q^3 ----
D    = [sp.expand(X0[n]-logW3[n]/2) for n in range(N)]
print("CHECK A: D vanishes at u3=0 (=> D in E3*Q[E][[T]] by symmetry) :",
      all(sp.simplify(c.subs(u3,0))==0 for c in D))
barD = [sp.expand(sp.diff(D[n],u3).subs(u3,0)/E2s) for n in range(N)]
print("   barD|_{E3=0} is polynomial? ", all(sp.simplify(sp.together(b)).is_polynomial(u1,u2) for b in barD))
qp1  = [sp.expand(q[i]+(1 if i==0 else 0)) for i in range(N)]
brk  = [sp.expand(mul(qp1,qp1,N)[i] - (E1s if i==1 else 0)) for i in range(N)]
rhsB = mul(mul(Y2,brk,N), inv(mul(mul(q,q,N),q,N),N), N)
rhsB = [sp.Integer(0)]+[rhsB[i] for i in range(N-1)]     # times T
print("CHECK B (Day162 Thm B): barD|_{E3=0} == T Y^2[(q+1)^2-E1 T]/q^3 :",
      all(sp.simplify(barD[n]-rhsB[n])==0 for n in range(N)))
for n in range(3,7):
    print("      n=%d : %s" % (n, sp.factor(barD[n])))
# Rick's stated table (Day159 §5): n=3:4, n=4:15E1, n=5:36E1^2+24E2, n=6:70E1^3+140E1E2
tbl = {3: sp.Integer(4), 4: 15*E1s, 5: 36*E1s**2+24*E2s, 6: 70*E1s**3+140*E1s*E2s,
       7: 120*E1s**4+480*E1s**2*E2s+120*E2s**2}
print("CHECK C: matches Day159 §5 table :", all(sp.simplify(barD[n]-tbl[n])==0 for n in tbl))
# equivalent form (n+1)(n-1)/2 * [T^{n-1}] Y^2
print("CHECK D: barD_n == (n+1)(n-1)/2 * [T^{n-1}]Y^2 :",
      all(sp.simplify(barD[n]-sp.Rational((n+1)*(n-1),2)*Y2[n-1])==0 for n in range(2,N)))

# ---- systematic exact search for  L_A[F_1] = P(T) F_0 + Q(T) F_0' ----
F0=[sp.expand(c.subs(u3,0)) for c in F]; F1=[sp.expand(sp.diff(c,u3).subs(u3,0)) for c in F]
def dT(A): return [sp.expand((n+1)*A[n+1]) for n in range(len(A)-1)]+[sp.Integer(0)]
def mulT(A,k): return ([sp.Integer(0)]*k+A)[:len(A)]
def LA(Fs):
    Fp,Fpp=dT(Fs),dT(dT(Fs))
    return [sp.expand(mulT(Fpp,2)[n]+(E1s+3)*mulT(Fp,1)[n]-Fp[n]+(1+E1s+E2s)*Fs[n]) for n in range(N)]
res=LA(F1); Fp0=dT(F0)
for d in range(0,5):
    cs=sp.symbols('p0:%d q0:%d'%(d+1,d+1))
    P=list(cs[:d+1]); Q=list(cs[d+1:])
    eqs=[]
    for n in range(N-2):
        e=res[n]
        for k in range(d+1):
            if n-k>=0: e-= P[k]*F0[n-k]+Q[k]*Fp0[n-k]
        eqs.append(sp.expand(e))
    sol=sp.solve(eqs, cs, dict=True)
    print("deg %d ansatz L_A[F1]=P F0 + Q F0' :"%d, "SOLVED" if sol else "no solution", sol if sol else "")
