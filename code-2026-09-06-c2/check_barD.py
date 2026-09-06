"""THEOREM B itself, from the Day-162 definitions, on my own instrument.
   X^{(0)} = l^top_0(log F_P);  W = l^top_0(tau F_P / F_P), tau: u_i -> u_i+1;
   D = X^{(0)} - (1/2) log W;  bar D = D/E_3;  R^{(-1)} = d_{u3} X^{(0)}|_{u3=0}.
   Claim (Day 162 Thm B):  bar D|_{E_3=0} = T Y^2 [(q+1)^2 - E_1 T] / q^3.
"""
import sys, sympy as sp
from series import *
from build_Xi import Psi3, top_layer, to_sp, u1, u2, u3

N = int(sys.argv[1]) if len(sys.argv) > 1 else 8
Tv = Tser(N); Y = Y_series(N); q = q_series(N)
R1R2 = sub(const(1, N), smul(s**2 - 4*p, mul(Tv, Tv)))

print(f"# building F_P (3 vars) to T^{N} ...")
FP = []
for b in range(N+1):
    P = sp.expand(Psi3(b).subs({u1:-u1, u2:-u2, u3:-u3}, simultaneous=True))
    FP.append(sp.expand(P/sp.factorial(b)))
tauFP = [sp.expand(c.subs({u1:u1+1, u2:u2+1, u3:u3+1}, simultaneous=True)) for c in FP]

def poly_log(c):
    lg = [sp.Integer(0)]*(N+1)
    for n in range(1, N+1):
        acc = c[n]
        for k in range(1, n): acc -= sp.Rational(k, n)*lg[k]*c[n-k]
        lg[n] = sp.expand(acc)
    return lg

def poly_div(a, b):
    out = [sp.Integer(0)]*(N+1)
    for n in range(N+1):
        acc = a[n]
        for k in range(1, n+1): acc -= b[k]*out[n-k]
        out[n] = sp.expand(sp.cancel(acc/b[0]))
    return out

logFP = poly_log(FP)
H3    = poly_div(tauFP, FP)                      # H = tau F_P / F_P,  H(0) = 1
# W = l^top_0(H): at [T^n] the u-degree-n part.   X0 = l^top_0(log F_P): same rule.
W3  = [top_layer(H3[n], n) for n in range(N+1)]
X03 = [top_layer(logFP[n], n) if n >= 1 else sp.Integer(0) for n in range(N+1)]
assert sp.expand(W3[0] - 1) == 0, W3[0]

logW3 = poly_log(W3)
Rm1     = [to_sp(sp.expand(sp.diff(X03[n], u3).subs(u3, 0))) for n in range(N+1)]
d1_logW = [to_sp(sp.expand(sp.diff(logW3[n], u3).subs(u3, 0))) for n in range(N+1)]

def cmp(name, a, b, upto):
    bad = [(i, v) for i, v in enumerate([sp.cancel(sp.expand(x-y)) for x, y in zip(a[:upto+1], b[:upto+1])]) if v != 0]
    print(f"{name:58s}: {'PASS' if not bad else 'FAIL ' + str(bad[:2])}")

cmp("Day161 Thm2  d_u3 log W|_0 = T(q+R1R2)/q^3  [true W]",
    d1_logW, div(mul(Tv, add(q, R1R2)), mul(q, mul(q, q))), N)

Rm1_cf = div(mul(Tv, add(mul(smul(p, mul(Y,Y)),
                             sub(mul(add(q,const(1,N)), add(q,const(1,N))), smul(s,Tv))),
                        smul(sp.Rational(1,2), add(q, R1R2)))), mul(q, mul(q,q)))
cmp("Day162  R^{(-1)} = d_u3 X^{(0)}|_0 closed form", Rm1, Rm1_cf, N)

# bar D|_{E_3=0} = (R^{(-1)} - (1/2) d_u3 log W|_0) / E_2
barD = [sp.cancel(sp.expand((Rm1[n] - sp.Rational(1,2)*d1_logW[n])/p)) for n in range(N+1)]
barD_cf = div(mul(mul(Tv, mul(Y,Y)), sub(mul(add(q,const(1,N)),add(q,const(1,N))), smul(s,Tv))),
              mul(q, mul(q,q)))
cmp("*** THEOREM B: bar D|_{E3=0} = TY^2[(q+1)^2-E1T]/q^3", barD, barD_cf, N)
print("\n  [T^n] bar D|_{E3=0}, mine (from the definition):")
for n in range(3, min(N,12)+1):
    print(f"   n={n}: {sp.expand(barD[n])}")
