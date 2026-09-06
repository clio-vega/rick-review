"""Is the Day 170 correction term 18*T^3*H^2*K forced, or fitted?
Replace 18 by a free scalar c, fix c from the FIRST failing order (T^4),
then ask whether T^5..T^10 follow.  Also test whether a DIFFERENT monomial
shape of the same weight could absorb the discrepancy."""
import sys, sympy as sp
from series import *
from build_FP import FP_series
c = sp.symbols('c')
N = 10
Tv = Tser(N); Y = Y_series(N); q = q_series(N); q2 = mul(q,q)
Fm = trim(FP_series(-1, N), N)
Gm = div(deriv(Fm), Fm)
Lms = [wdeg_parts(Gm[m]).get(m+2-2, sp.Integer(0)) for m in range(N+1)]

H = shift_down(smul(p, Y)); Hp = deriv(H); Hpp = deriv(Hp)
K = smul(-1, div(smul(p,Y), q2)); Kp = deriv(K)
R3 = smul(-1, mul(mul(Tv,Tv), q2)); R2 = mul(q2, sub(const(1,N), smul(s,Tv)))
T2, T3, T4 = mul(Tv,Tv), mul(mul(Tv,Tv),Tv), mul(mul(Tv,Tv),mul(Tv,Tv))
c_Hp = add(add(smul(-11,Tv), smul(14*s,T2)), smul(12*p-3*s**2, T3))
c_H  = add(add(const(1,N), smul(12*s,Tv)), smul(5*p-s**2, T2))
c_H2 = add(smul(23,T2), smul(s,T3))
c_K  = add(add(const(-s,N), smul(2*s**2+10*p, Tv)), smul(4*p*s-s**3, T2))
S12 = mul(R3,Hpp)
for t in [mul(c_Hp,Hp), mul(c_H,H), smul(3, mul(R3, add(mul(H,Kp), mul(K,Hp)))),
          mul(c_H2, mul(H,H)), smul(18, mul(T3, mul(H,Hp))), mul(T4, mul(H,mul(H,H))),
          smul(3, mul(R3, mul(H, mul(K,K)))), mul(R2,Kp), smul(2, mul(c_Hp, mul(H,K))),
          mul(c_K,K), mul(R2, mul(K,K))]:
    S12 = add(S12, t)

extra = mul(T3, mul(mul(H,H), K))
S = add(S12, smul(c, extra))
Lm_cf = smul(-1, div(S, mul(q, mul(q2, H))))
res = [sp.expand(sp.cancel(Lms[n] - Lm_cf[n])) for n in range(N)]
print("residual with free coefficient c on T^3 H^2 K:")
sol = None
for n in range(N):
    r = sp.expand(res[n])
    if r == 0:
        print(f"  T^{n}: 0 identically"); continue
    if sol is None:
        sol = sp.solve(sp.Poly(r, c).all_coeffs()[-1] if False else r, c)
        # r must vanish identically in s,p; solve coefficientwise
        pol = sp.Poly(r, c)
        assert pol.degree() == 1, pol
        a1, a0 = pol.all_coeffs()
        sol = sp.cancel(-a0/a1)
        print(f"  T^{n}: FIRST constraint -> c = {sp.simplify(sol)}")
    else:
        rr = sp.expand(r.subs(c, sol))
        print(f"  T^{n}: with c={sol}: {'0  (PREDICTED, not fitted)' if rr == 0 else 'NONZERO ' + str(rr)}")
