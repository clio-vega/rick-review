"""Independent audit of Route A: Day 161 Thm 1 & 2, and Day 170 section 4's nine-term
closed form for d^2_{u_3} Xi|_{u_3=0}.  LHS built by me from the Day-131 definitions."""
import sys, sympy as sp
from series import *
from build_Xi import logFP_coeffs, top_layer, to_sp, u1, u2, u3

N = int(sys.argv[1]) if len(sys.argv) > 1 else 7
print(f"# building log F_P in three variables to T^{N} ...")
lg = logFP_coeffs(N)

d1_Xi, d2_Xi, d1_logW = [], [], []
for n in range(N+1):
    Xi_n  = top_layer(lg[n], n+1) if n >= 1 else sp.Integer(0)   # top weight  n+1
    W_n   = top_layer(lg[n], n)   if n >= 1 else sp.Integer(0)   # sub-top weight n
    d1_Xi.append(to_sp(sp.expand(sp.diff(Xi_n, u3).subs(u3, 0))))
    d2_Xi.append(to_sp(sp.expand(sp.diff(Xi_n, u3, 2).subs(u3, 0))))
    d1_logW.append(to_sp(sp.expand(sp.diff(W_n, u3).subs(u3, 0))))

Y = Y_series(N); q = q_series(N); Tv = Tser(N)

def log_series(a):
    """log of a series with a[0] = 1"""
    assert sp.expand(a[0]) == 1
    return integ(div(deriv(a), a))

logq = log_series(q)
xi0  = integ(shift_down(smul(p, Y)))          # xi_0 = int (E2 Y / T) dT
R1R2 = sub(const(1, N), smul(p*0, Tv))
R1R2 = sub(const(1, N), smul(s**2 - 4*p, mul(Tv, Tv)))

dE1 = lambda a: [sp.expand(sp.diff(x, s)) for x in a]
dE2 = lambda a: [sp.expand(sp.diff(x, p)) for x in a]

def cmp(name, a, b, upto):
    d = [sp.cancel(sp.expand(x-y)) for x, y in zip(a[:upto+1], b[:upto+1])]
    bad = [(i, v) for i, v in enumerate(d) if v != 0]
    print(f"{name:58s}: {'PASS' if not bad else 'FAIL ' + str(bad[:2])}")
    return not bad

# sanity: xi_0 is the top layer of log F_P at u_3 = 0
cmp("Day158 Thm1  Xi|_{u3=0} = int E2 Y/T",
    [to_sp(top_layer(lg[n], n+1).subs(u3, 0)) if n >= 1 else sp.Integer(0) for n in range(N+1)],
    xi0, N)
cmp("Day161 Thm1  d_{u3} Xi|_0 = -log q", d1_Xi, smul(-1, logq), N)
cmp("Day161 Thm2  d_u3 logW|_0 = T(q+R1R2)/q^3  [logW = 2 x subtop]",
    smul(2, d1_logW), div(mul(Tv, add(q, R1R2)), mul(q, mul(q, q))), N)

# --- Day 170 section 4, the nine-term expression -------------------------------
qp_over_q = div(deriv(q), q)
nine = add(add(add(add(add(add(add(add(
    smul(2, dE1(dE1(xi0))),
    smul(3*s, dE1(dE2(xi0)))),
    smul(s**2, dE2(dE2(xi0)))),
    smul(2, dE1(logq))),
    smul(s, dE2(logq))),
    dE2(xi0)),
    smul(-1, div(Tv, q))),
    div(mul(Tv, add(q, R1R2)), mul(q, mul(q, q)))),
    smul(-s, div(mul(Tv, Y), q)))
cmp("Day170 sec4  9-term form of d^2_{u3} Xi|_0", d2_Xi, nine, N)
