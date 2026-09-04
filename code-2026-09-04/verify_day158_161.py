"""Independent verification of Rick's Days 158/159/161 claims, from the DEFINITION of F_P."""
import sympy as sp
from fp_lib import *

N = 9   # T-precision
F = FP_coeffs(N)

print("="*70)
print("CHECK 0 (JOB 3): true F_P vs the product/naive forms at [T^1]")
print("  [T^1] F_P (from definition) =", sp.factor(sp.expand(F[1])))
naive = sp.expand((u1+1)*(u2+1)*(u3+1))
print("  prod A_1(u_i)               =", sp.factor(naive))
print("  difference                  =", sp.expand(F[1]-naive), "   (= -E_3)")
print("  => Day 161's catch is CORRECT: true F_P has NO E_3 at [T^1].")

print("="*70)
print("CHECK 1: F_P|_{u3=0} == sum_k T^k/k! * A_k(u1) A_k(u2)   (Day 158's F_0)")
ok = True
for k in range(N):
    lhs = sp.expand(F[k].subs(u3, 0))
    rhs = sp.expand(rising(u1+1, k)*rising(u2+1, k)/sp.factorial(k))
    d = sp.simplify(lhs-rhs)
    if d != 0:
        ok = False; print("   MISMATCH at k=",k, d)
print("   n<=%d : %s" % (N-1, "ALL MATCH" if ok else "FAILED"))

# ---------- series objects ----------
logF = logs(F, N)
Xi   = layer(logF, 1)     # ell^top_1
X0   = layer(logF, 0)     # ell^top_0

# tau: u_i -> u_i+1
Ftau = [sp.expand(c.subs({u1:u1+1, u2:u2+1, u3:u3+1}, simultaneous=True)) for c in F]
H    = mul(Ftau, inv(F, N), N)
M    = logs(H, N)
W    = layer(H, 0)          # calW = ell^top_0(H)
Hm1  = layer(H, -1)
Mm1  = layer(M, -1)

# ---------- 2-variable closed-form side: Y, q, phi ----------
E1s, E2s = u1+u2, u1*u2
Y = [sp.Integer(0)]*N
for _ in range(N+1):
    Y2 = mul(Y, Y, N)
    phi = [sp.Integer(1)+sp.Integer(0)]+[sp.Integer(0)]*(N-1)
    phi = [sp.expand(( 1 if i==0 else 0) + E1s*Y[i] + E2s*Y2[i]) for i in range(N)]
    Ynew = [sp.Integer(0)] + [phi[i] for i in range(N-1)]
    Y = [sp.expand(c) for c in Ynew]
Y2 = mul(Y, Y, N)
phi = [sp.expand((1 if i==0 else 0) + E1s*Y[i] + E2s*Y2[i]) for i in range(N)]
q = [sp.expand((1 if i==0 else 0) - (E1s if i==1 else 0) - 2*E2s*(Y[i-1] if i>=1 else 0)) for i in range(N)]
qq = mul(q, q, N)
tgt = [sp.expand((1 if i==0 else 0) - (2*E1s if i==1 else 0) + (E1s**2-4*E2s if i==2 else 0)) for i in range(N)]
print("="*70)
print("CHECK 2 (Q1): q^2 == (1-E1 T)^2 - 4 E2 T^2 :",
      all(sp.simplify(qq[i]-tgt[i])==0 for i in range(N)))

# W|_{u3=0} should be Y/(T q) = phi/q
Winv_q = mul(phi, inv(q, N), N)
Wslice = [sp.expand(c.subs(u3,0)) for c in W]
print("CHECK 3 (Day 154): calW|_{u3=0} == phi/q :",
      all(sp.simplify(Wslice[i]-Winv_q[i])==0 for i in range(N)))

# ---------- Day 158 Theorem 1: Xi|_{u3=0} = E2 * sum Y_n T^n/n ----------
Xi0 = [sp.expand(c.subs(u3,0)) for c in Xi]
thm1 = [sp.Integer(0)] + [sp.expand(E2s*Y[n]/n) for n in range(1, N)]
thm1 = [sp.expand(E2s*Y[n]/n) if n>=1 else sp.Integer(0) for n in range(N)]
print("="*70)
print("CHECK 4 (Day 158 Thm 1): Xi|_{u3=0} == E2*Y_n/n :",
      all(sp.simplify(Xi0[n]-thm1[n])==0 for n in range(N)))

# ---------- Day 158 Theorem 2: X0|_{u3=0} = (1/2) log(phi/q) ----------
X00 = [sp.expand(c.subs(u3,0)) for c in X0]
logW0 = logs(Winv_q, N)
print("CHECK 5 (Day 158 Thm 2): X0|_{u3=0} == (1/2) log(calW|_{u3=0}) :",
      all(sp.simplify(X00[n]-logW0[n]/2)==0 for n in range(N)))

# ---------- C.5 : ell^top_{-1}(H)|_{u3=0} == 6T/q^4 ----------
q4 = mul(mul(qq,qq,N),[sp.Integer(1)]+[sp.Integer(0)]*(N-1),N)
inv_q4 = inv(mul(qq,qq,N), N)
c5 = [sp.Integer(0)] + [inv_q4[i] for i in range(N-1)]
c5 = [sp.expand(6*c) for c in c5]
Hm1_0 = [sp.expand(c.subs(u3,0)) for c in Hm1]
print("="*70)
print("CHECK 6 (C.5): ell^top_{-1}(H)|_{u3=0} == 6T/q^4 :",
      all(sp.simplify(Hm1_0[n]-c5[n])==0 for n in range(N)))

# ---------- Day 159 Thm 1 (Day156 lemma): M^{(-1)} = dX0 + (1/2) d^2 Xi, 3-variable ----------
def partial(series):
    return [sp.expand(sp.diff(c,u1)+sp.diff(c,u2)+sp.diff(c,u3)) for c in series]
lhs = Mm1
rhs = [sp.expand(a + b/2) for a,b in zip(partial(X0), partial(partial(Xi)))]
print("CHECK 7 (Day159 Thm1 / Day156 lemma, 3-VARIABLE): M^(-1) == dX0+(1/2)d^2 Xi :",
      all(sp.simplify(lhs[n]-rhs[n])==0 for n in range(N)))

# ---------- Day 152 (P1): log calW = partial Xi (3-variable) ----------
logW3 = logs(W, N)
print("CHECK 8 (Day152 P1, 3-VARIABLE): log calW == partial Xi :",
      all(sp.simplify(logW3[n]-partial(Xi)[n])==0 for n in range(N)))

# ---------- Day 159 Thm 2: Xi_2 = (3/2)E3 + (1/2)E1E2 ----------
E1,E2,E3 = sp.symbols('E1 E2 E3')
print("CHECK 9 (Day159 Thm2): Xi_2 =", sp.factor(Xi[2]),
      "  vs (3/2)E3+(1/2)E1E2 ->",
      sp.simplify(Xi[2] - (sp.Rational(3,2)*u1*u2*u3 + sp.Rational(1,2)*(u1+u2+u3)*(u1*u2+u1*u3+u2*u3))) == 0)

# ---------- Day 161 Theorem 1: d_{u3} Xi |_{u3=0} = -log q ----------
dXi = [sp.expand(sp.diff(c,u3).subs(u3,0)) for c in Xi]
mlogq = [sp.expand(-c) for c in logs(q,N)]
print("="*70)
print("CHECK 10 (Day161 Thm 1): d_{u3}Xi|_{u3=0} == -log q :",
      all(sp.simplify(dXi[n]-mlogq[n])==0 for n in range(N)))
for n in range(1,5):
    print("      n=%d: lhs=%s  rhs=%s" % (n, sp.factor(dXi[n]), sp.factor(mlogq[n])))

# ---------- Day 161 Theorem 2: d_{u3} log calW |_{u3=0} = T(q+R1R2)/q^3 ----------
dlogW = [sp.expand(sp.diff(c,u3).subs(u3,0)) for c in logW3]
R1R2 = [sp.expand((1 if i==0 else 0) - ((E1s**2-4*E2s) if i==2 else 0)) for i in range(N)]
num = [sp.expand(q[i]+R1R2[i]) for i in range(N)]
rhs2 = mul(num, inv(mul(qq,q,N), N), N)
rhs2 = [sp.Integer(0)] + [rhs2[i] for i in range(N-1)]     # multiply by T
print("CHECK 11 (Day161 Thm 2): d_{u3}log calW|_{u3=0} == T(q+R1R2)/q^3 :",
      all(sp.simplify(dlogW[n]-rhs2[n])==0 for n in range(N)))
for n in range(1,5):
    print("      n=%d: lhs=%s  rhs=%s" % (n, sp.factor(dlogW[n]), sp.factor(rhs2[n])))
