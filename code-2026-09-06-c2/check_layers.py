"""Audit of Rick's Day 168 L_0, Day 169 K_{-1}/L_{-1}, and Day 170's corrected SOURCE.

Everything on the LEFT of each comparison is built by me from the Day-131 definition of
Psi (build_FP.py, itself hand-checked at b=0,1 for both slices).  Everything on the RIGHT
is Rick's claimed closed form, transcribed from his proof files.
"""
import sys, sympy as sp
from series import *
from build_FP import FP_series

N = int(sys.argv[1]) if len(sys.argv) > 1 else 10

print(f"# building F_P at u3=0 and u3=-1 from the definition, to T^{N} ...")
c0 = FP_series(0, N)
cm = FP_series(-1, N)
F0 = trim(c0, N)
Fm = trim(cm, N)

Y = Y_series(N); q = q_series(N)
Tv = Tser(N)

# --- sanity: Y = T phi(Y), q^2 = (1-sT)^2 - 4pT^2 ------------------------------
assert sub(Y, mul(Tv, add(add(const(1,N), smul(s,Y)), smul(p, mul(Y,Y))))) == [0]*(N+1)
lhs = mul(q,q)
rhs = sub(mul(sub(const(1,N), smul(s,Tv)), sub(const(1,N), smul(s,Tv))), smul(4*p, mul(Tv,Tv)))
assert sub(lhs, rhs) == [0]*(N+1), "q^2 identity"
print("  (Q1),(Q2) ok")

# --- LINK 0: Day 158 Prop A (ODE for F_0) --------------------------------------
A = add(add(mul(mul(Tv,Tv), deriv(deriv(F0))),
            mul(sub(smul(s+3, Tv), const(1,N)), deriv(F0))),
        smul(1+s+p, F0))
print("Day158 Prop A  T^2F''+[(s+3)T-1]F'+(1+s+p)F = 0 :",
      "PASS" if all(sp.expand(x)==0 for x in A[:N-1]) else "FAIL " + str(A[:N-1]))

# --- LINK: Day 168 Result 2 (F_{-1}' = 2pF_0 - p(1-(s+1)T)F_0'/(p+s+1)) --------
r2 = sub(deriv(Fm), sub(smul(2*p, F0),
         smul(sp.cancel(p/(p+s+1)), mul(sub(const(1,N), smul(s+1, Tv)), deriv(F0)))))
print("Day168 Result 2 (F_{-1}' relation)              :",
      "PASS" if all(sp.cancel(sp.expand(x))==0 for x in r2[:N]) else "FAIL " + str([sp.cancel(x) for x in r2[:N]]))

# --- LINK: Day 169 (star): 3rd-order ODE for F_{-1} ----------------------------
q2 = mul(q,q)
def Dk(k): return add(sub(mul(Tv,Tv), q2), smul(k, Tv))
star = add(add(mul(mul(mul(Tv,Tv), Dk(6)), deriv(deriv(deriv(Fm)))),
               mul(mul(sub(smul(s+3,Tv), const(1,N)), Dk(8)), deriv(deriv(Fm)))),
           mul(add(smul(1+s+p, Dk(10)), const(2,N)), deriv(Fm)))
print("Day169 (star) 3rd-order ODE for F_{-1}          :",
      "PASS" if all(sp.expand(x)==0 for x in star[:N-2]) else "FAIL " + str(star[:N-2]))

# --- layer extraction ----------------------------------------------------------
def layers(G, dmax=3):
    """G a series; return list of layer series L[d], d = 0..dmax, where
       [T^m]L[d] is the u-weight (m+2-d) part of [T^m]G."""
    out = [[sp.Integer(0)]*(N+1) for _ in range(dmax+1)]
    for m in range(N+1):
        parts = wdeg_parts(G[m])
        top = m+2
        for d in range(dmax+1):
            out[d][m] = parts.get(top-d, sp.Integer(0))
        # also record anything ABOVE the claimed top
        above = {w: v for w, v in parts.items() if w > top}
        if above and m < N: print(f"  !! [T^{m}]G has weight ABOVE m+2: {above}")
    return out

G0 = div(deriv(F0), F0)
Gm = div(deriv(Fm), Fm)
H0s, K0s, L0s, _ = layers(G0)
Hms, Kms, Lms, _ = layers(Gm)

H_cf = shift_down(smul(p, Y))                       # pY/T
K0_cf = div(add(mul(smul(p,Y), add(smul(2,q), const(1,N))), smul(s,q)), q2)
Km_cf = smul(-1, div(smul(p,Y), q2))

def cmp(name, a, b, upto):
    d = [sp.cancel(sp.expand(x-y)) for x, y in zip(a[:upto+1], b[:upto+1])]
    bad = [(i, v) for i, v in enumerate(d) if v != 0]
    print(f"{name:52s}: {'PASS' if not bad else 'FAIL ' + str(bad[:3])}")
    return not bad

cmp("Day158  H_0  = pY/T", H0s, H_cf, N-1)
cmp("Day158  K_0  = [pY(2q+1)+sq]/q^2", K0s, K0_cf, N-1)
cmp("Day169  H_{-1} = pY/T", Hms, H_cf, N-1)
cmp("Day169  K_{-1} = -pY/q^2", Kms, Km_cf, N-1)

# --- Day 168 L_0 closed form ---------------------------------------------------
theta = lambda a: mul(Tv, deriv(a))
L0_cf = div(add(add(add(const(1,N), smul(3, mul(Tv, K0_cf))),
                    mul(mul(Tv,Tv), mul(K0_cf,K0_cf))),
                mul(Tv, theta(K0_cf))), q)
cmp("Day168  L_0  = (1+3TK+T^2K^2+T.theta K)/q", L0s, L0_cf, N-1)

# --- Day 169/170 SOURCE for L_{-1} ---------------------------------------------
def source(with_missing_term):
    H = H_cf; Hp = deriv(H); Hpp = deriv(Hp)
    K = Km_cf; Kp = deriv(K)
    R3 = smul(-1, mul(mul(Tv,Tv), q2))
    R2 = mul(q2, sub(const(1,N), smul(s,Tv)))
    T2, T3, T4 = mul(Tv,Tv), mul(mul(Tv,Tv),Tv), mul(mul(Tv,Tv),mul(Tv,Tv))
    c_Hp = add(add(smul(-11,Tv), smul(14*s,T2)), smul(12*p-3*s**2, T3))
    c_H  = add(add(const(1,N), smul(12*s,Tv)), smul(5*p-s**2, T2))
    c_H2 = add(smul(23,T2), smul(s,T3))
    c_K  = add(add(const(-s,N), smul(2*s**2+10*p, Tv)), smul(4*p*s-s**3, T2))
    S = mul(R3, Hpp)
    S = add(S, mul(c_Hp, Hp)); S = add(S, mul(c_H, H))
    S = add(S, smul(3, mul(R3, add(mul(H,Kp), mul(K,Hp)))))
    S = add(S, mul(c_H2, mul(H,H)))
    S = add(S, smul(18, mul(T3, mul(H,Hp))))
    S = add(S, mul(T4, mul(H, mul(H,H))))
    S = add(S, smul(3, mul(R3, mul(H, mul(K,K)))))
    S = add(S, mul(R2, Kp))
    S = add(S, smul(2, mul(c_Hp, mul(H,K))))
    S = add(S, mul(c_K, K)); S = add(S, mul(R2, mul(K,K)))
    if with_missing_term:
        S = add(S, smul(18, mul(T3, mul(mul(H,H), K))))
    return S

for flag, tag in [(False, "Day169 writeup SOURCE (12 terms, as shipped)"),
                  (True,  "Day170 corrected SOURCE (13 terms)")]:
    Lm_cf = smul(-1, div(source(flag), mul(mul(q,q2), H_cf)))
    cmp(f"  L_{{-1}} from {tag}", Lms, Lm_cf, N-1)
