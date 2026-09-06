"""End-to-end audit of the CONCLUSION: Day 162's R^{(-1)} closed form, assembled through
Prop 3 from objects I built myself.  Clio 2026-09-06 c2."""
import sys, sympy as sp
from series import *
from build_FP import FP_series
from build_Xi import logFP_coeffs, top_layer, to_sp, u3

N = int(sys.argv[1]) if len(sys.argv) > 1 else 7
Tv = Tser(N); Y = Y_series(N); q = q_series(N)
R1R2 = sub(const(1, N), smul(s**2 - 4*p, mul(Tv, Tv)))

print(f"# rebuilding everything to T^{N} ...")
F0 = trim(FP_series(0, N), N); Fm = trim(FP_series(-1, N), N)
def log_series(a): return integ(div(deriv(a), a))
log_ratio = log_series(div(Fm, F0))

# [deg_{(u1,u2)} = n-1] of [T^n] log(F_{-1}/F_0)
routeB = [wdeg_parts(log_ratio[n]).get(n-1, sp.Integer(0)) for n in range(N+1)]

# Day 158 Thm 2 on the slice, as a control on my layer extractor
lg3 = logFP_coeffs(N)
subtop0 = [to_sp(top_layer(lg3[n], n).subs(u3, 0)) if n >= 1 else sp.Integer(0) for n in range(N+1)]
W = div(shift_down(Y), q)         # W = (Y/T)/q, W(0) = 1
half_logW = smul(sp.Rational(1,2), log_series(W))

d2Xi = []
for n in range(N+1):
    Xi_n = top_layer(lg3[n], n+1) if n >= 1 else sp.Integer(0)
    d2Xi.append(to_sp(sp.expand(sp.diff(Xi_n, u3, 2).subs(u3, 0))))

Rm1_prop3 = sub(smul(sp.Rational(1,2), d2Xi), routeB)
Rm1_day162 = div(mul(Tv, add(mul(smul(p, mul(Y,Y)), sub(mul(add(q,const(1,N)), add(q,const(1,N))),
                                                        smul(s, Tv))),
                             smul(sp.Rational(1,2), add(q, R1R2)))),
                 mul(q, mul(q, q)))

def cmp(name, a, b, upto):
    bad = [(i, v) for i, v in enumerate([sp.cancel(sp.expand(x-y)) for x, y in zip(a[:upto+1], b[:upto+1])]) if v != 0]
    print(f"{name:58s}: {'PASS' if not bad else 'FAIL ' + str(bad[:2])}")

cmp("Day158 Thm2  subtop(log F_0) = (1/2) log(Y/(Tq))", subtop0, half_logW, N-1)
cmp("THEOREM: Day162 R^{(-1)} closed form (via Prop 3)", Rm1_prop3, Rm1_day162, N)
print("\n  R^{(-1)} coefficients, mine (Prop 3 assembly) vs Rick's closed form:")
for n in range(min(N, 7)+1):
    print(f"   [T^{n}]  {sp.factor(Rm1_prop3[n])!s:38s} | {sp.factor(Rm1_day162[n])}")
