"""Clio 2026-09-17: the FACTORED closed form for tau_r, checked against my own
p_2(Y).e_r computes at r = 2..6 (independent of Rick's scripts).

   tau_r(q,t) = -(q^2-1) [r+2]_t ( q t^{r+1} - q + t + 1 ) / ( q^3 [2]_t )

equivalently  q^3 tau_r = (q^2-1)/[2]_t * [r+2]_t * ( (q-t-1) - q t^{r+1} ).
"""
import sys
from hikita_star_clio import *
from p2Y_check import p2Y, rick_tau   # p2Y_check re-runs r=2..5 on import; fine
def qint(n):
    s = ZERO
    for i in range(n): s = s + t**i
    return s
def tau_compact(r):
    return -(q**2-ONE)*qint(r+2)*(q*t**(r+1) - q + t + ONE) / (q**3 * qint(2))
print()
print("CHECK: compact factored form vs Rick's three-monomial (12), symbolically in r")
for r in range(1, 13):
    print("   r=%-2d  agree with Rick (12): %s" % (r, (tau_compact(r) - rick_tau(r)) == ZERO))
print()
print("CHECK: compact form vs my own p_2(Y).e_r compute")
for r in range(2, 7):
    m = r + 2
    co = expand_in_e(p2Y(e_poly(r, m), m), r+2, m)
    got = co.get((r+2,), ZERO)
    print("   r=%-2d m=%-2d  top coeff matches factored form: %s" % (r, m, (got - tau_compact(r)) == ZERO))
    sys.stdout.flush()
