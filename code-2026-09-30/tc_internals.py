"""Audit of the internal steps of Rick's Day 209 (TC) proof, from his printed text only.

Targets named in my brief: s.2 (step map / residue extraction) and s.4 Step B
(the normalisations).  Plus the m=0 base case of the s.3 induction, which is
where (TC) silently asserts  sum_{i,j} V^{(k)}_{ij} = 0  for k >= 1.
"""
import sys
sys.path.insert(0, '/home/clio/projects/reviews/code-2026-09-30')
import sympy as sp
from tc_aha import (Xs, e, E, T, Tinv, pi, cnj, alpha, Nnj, K_ij, V, tpoch)

s, t, z, w, x = sp.symbols('s t z w x')
gam, dlt = sp.symbols('gamma delta')
A, B = sp.symbols('A B')

def Z(expr):
    return sp.simplify(sp.cancel(sp.together(sp.expand(expr)))) == 0

print("=" * 78)
print("(1) c(n,j) = 0 for n < j  -- asserted in s.0 to make n_1>=i, n_2>=j automatic")
print("=" * 78)
bad = [(n, j) for n in range(0, 9) for j in range(n + 1, 10) if cnj(n, j) != 0]
print(f"  n<j, n<=8, j<=9: {len(bad)} nonzero  -> {'OK' if not bad else bad[:5]}")
print(f"  alpha_(-1) = {alpha(-1)}  (207b s.0 fixes this; Day 209 does not restate it)")

print()
print("=" * 78)
print("(2) THE m=0 BASE CASE.  At m=0, Gamma_k = 0 and T_k = sum_{i,j} V^{(k)}_{ij}.")
print("    So (TC) at m=0 IS the identity  sum_{i,j} V^{(k)}_{ij} = 0  for k >= 1.")
print("    The writeup discharges this in one clause via (L2)'s empty left side.")
print("=" * 78)
for k in range(0, 7):
    tot = sum(V(k, i, j) for i in range(k + 1) for j in range(k - i + 1))
    val = sp.simplify(sp.cancel(sp.together(tot)))
    print(f"  k={k}: sum_(i,j) V^(k)_ij = {val}"
          f"   {'OK' if (val == 0 or (k == 0 and val == 1)) else '*** NONZERO ***'}")

print()
print("=" * 78)
print("(3) (★2) for all n,i,j INCLUDING the vacuous range i+j>n")
print("=" * 78)
c_sym = s**2 * t**(-sp.Symbol('ipj'))
def star2_residual(n, i, j):
    g, d = t**i * z, t**j * w
    c = s**2 * t**(-i - j)
    kg = (g - s*z)*(g - s*w)/(g*(g - d))
    kd = (d - s*z)*(d - s*w)/(d*(d - g))
    gp, dp = t**(i-1)*z, t**j*w          # kappa_gamma^{(i-1,j)} inputs
    kgp = (gp - s*z)*(gp - s*w)/(gp*(gp - dp))
    g2, d2 = t**i*z, t**(j-1)*w          # kappa_delta^{(i,j-1)} inputs
    kdp = (d2 - s*z)*(d2 - s*w)/(d2*(d2 - g2))
    S = 0
    for p in range(0, n):                 # V^{(n-1-p)} = 0 for p > n-1
        S += c**p * ( V(n-1-p, i, j)*(kg*g**(-p-1) + kd*d**(-p-1))
                     - t**p * V(n-1-p, i-1, j) * kgp * (t**(i-1)*z)**(-p-1)
                     - t**p * V(n-1-p, i, j-1) * kdp * (t**(j-1)*w)**(-p-1) )
    return S - (1 - t**n) * V(n, i, j)

rows, fails = 0, 0
for n in range(0, 6):
    for i in range(0, 5):
        for j in range(0, 5):
            if i == 0 and j == 0 and n == 0:
                continue
            r = star2_residual(n, i, j)
            ok = Z(r); rows += 1; fails += (not ok)
            if not ok:
                print(f"  *** FAIL n={n} i={i} j={j}")
print(f"  {rows-fails}/{rows} (n,i,j) with n<=5, i,j<=4  (includes {sum(1 for n in range(6) for i in range(5) for j in range(5) if i+j>n)} vacuous i+j>n)")

print()
print("=" * 78)
print("(4) s.2, Lemma 2' applied:  (1-t) sum_i H(X_i;x) prod_{j!=i} a_ij")
print("      ==  c/x - sum_{a in {x,gamma,delta}} rho_a E(ta)/E(a)")
print("    brute force in Q(X_1..X_m, s,t,z,w,x,gamma,delta), gamma/delta FREE")
print("=" * 78)
for m in [1, 2, 3, 4]:
    X = Xs(m)
    c = s**2*z*w/(gam*dlt)
    H = lambda yy: yy*(1 + s*yy*z)*(1 + s*yy*w)/((1 + gam*yy)*(1 + dlt*yy)*(1 + x*yy))
    lhs = (1 - t)*sum(H(X[i-1])*sp.prod([(X[i-1] - t*X[j-1])/(X[i-1] - X[j-1])
                                         for j in range(1, m+1) if j != i])
                      for i in range(1, m+1))
    poles = [x, gam, dlt]
    rho = {a: (a - s*z)*(a - s*w)/(a*sp.prod([a - ap for ap in poles if ap is not a]))
           for a in poles}
    rhs = c/x - sum(rho[a]*E(X, t*a)/E(X, a) for a in poles)
    print(f"  m={m}: {'OK' if Z(lhs - rhs) else '*** FAIL ***'}")

print()
print("=" * 78)
print("(5) s.2, the e_n coefficient extraction (the Laurent/residue step).")
print("    Claim: [x^b]{ (c/x)E(x)E(g)E(d) - rho_x E(tx)E(g)E(d)")
print("                  - rho_g E(x)E(tg)E(d) - rho_d E(x)E(g)E(td) }")
print("           == sum_n e_n * coeff_n, with coeff_n as printed in the three cases.")
print("=" * 78)
def printed_coeffs(X, b, m):
    c = s**2*z*w/(gam*dlt)
    kg = (gam - s*z)*(gam - s*w)/(gam*(gam - dlt))
    kd = (dlt - s*z)*(dlt - s*w)/(dlt*(dlt - gam))
    out = {}
    for n in range(0, m + 1):
        if n == b + 1:
            out[n] = c*(1 - t**(b+1))*E(X, gam)*E(X, dlt)
        elif n <= b:
            out[n] = (-kg*gam**(n-b-1)*(E(X, t*gam) - t**n*E(X, gam))*E(X, dlt)
                      - kd*dlt**(n-b-1)*E(X, gam)*(E(X, t*dlt) - t**n*E(X, dlt)))
        else:
            out[n] = sp.Integer(0)
    return out

for m in [1, 2, 3]:
    X = Xs(m)
    c = s**2*z*w/(gam*dlt)
    poles = [x, gam, dlt]
    rho = {a: (a - s*z)*(a - s*w)/(a*sp.prod([a - ap for ap in poles if ap is not a]))
           for a in poles}
    big = ((c/x)*E(X, x)*E(X, gam)*E(X, dlt)
           - rho[x]*E(X, t*x)*E(X, gam)*E(X, dlt)
           - rho[gam]*E(X, x)*E(X, t*gam)*E(X, dlt)
           - rho[dlt]*E(X, x)*E(X, gam)*E(X, t*dlt))
    for b in range(0, 4):
        # [x^b] of the Laurent expansion at x=0
        ser = sp.series(sp.cancel(sp.together(big)), x, 0, b + 2).removeO()
        lhs = sp.expand(ser).coeff(x, b)
        cf = printed_coeffs(X, b, m)
        rhs = sum(cf[n]*e(X, n) for n in cf)
        print(f"  m={m} b={b}: {'OK' if Z(lhs - rhs) else '*** FAIL ***'}")
        sys.stdout.flush()
