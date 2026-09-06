"""
Independent verification of Rick's Day 167 Prop 3 (Route (v) weight-grading reduction).

Built from the DEFINITION F_P := T^+(e^{T e_2} V)/V  (Day 149 §1 / Day 162 §1),
NOT from Rick's scratch/day152/lib.py.  This is a genuinely independent instrument.

Checks, in order:
  (0) instrument check: F_P via T^+ rising factorials  ==  Day 149's varphi(Psi_b) route
  (1) Fact II(c) is SHARP: deg_u [T^n] log F_P == n+1 (not just <=)
  (2) the (*) identity SYMBOLICALLY IN c  -- i.e. off the slice u_3=0
  (3) Prop 3 itself
  (4) negative controls
"""
import sympy as sp
from sympy import Rational, symbols, expand, quo, factorial

u1, u2, u3, c = symbols('u1 u2 u3 c')
U = (u1, u2, u3)
V  = (u1-u2)*(u1-u3)*(u2-u3)
e2 = u1*u2 + u1*u3 + u2*u3

N = int(__import__('sys').argv[1]) if len(__import__('sys').argv) > 1 else 8

def rising(x, k):
    r = sp.Integer(1)
    for i in range(k):
        r *= (x + i)
    return r

def falling(x, k):
    r = sp.Integer(1)
    for i in range(k):
        r *= (x - i)
    return r

def apply_T(poly, fac):
    """Apply u^alpha -> prod_i fac(u_i, alpha_i) monomial-wise."""
    p = sp.Poly(expand(poly), *U)
    out = sp.Integer(0)
    for mono, coeff in zip(p.monoms(), p.coeffs()):
        term = coeff
        for x, k in zip(U, mono):
            term *= fac(x, k)
        out += term
    return expand(out)

def exact_quo(num, den):
    q = quo(sp.Poly(num, *U), sp.Poly(den, *U)).as_expr()
    assert expand(q*den - num) == 0, "V does not divide exactly"
    return expand(q)

print(f"Building F_P to T^{N} ...", flush=True)
# [T^n] F_P = T^+(e_2^n V) / (n! V)
FP = []
e2n = sp.Integer(1)
for n in range(N+1):
    FP.append(exact_quo(apply_T(expand(e2n*V), rising), V) / factorial(n))
    FP[-1] = expand(FP[-1])
    e2n = expand(e2n*e2)
print("  F_P built. [T^0] =", FP[0], flush=True)
assert FP[0] == 1

# ---- (0) INSTRUMENT CHECK: the varphi(Psi_b) route of Day 149 -----------------
# P_b = varphi(Psi(e_2^b)),  Psi(f) = T_falling(f V)/V,  varphi: u_i -> -u_i
# F_P = sum_b P_b T^b/b!
ok = True
for n in range(min(N, 5)+1):
    Psi = exact_quo(apply_T(expand(e2**n * V), falling), V)
    Pb  = expand(Psi.subs({u1: -u1, u2: -u2, u3: -u3}, simultaneous=True))
    if expand(Pb/factorial(n) - FP[n]) != 0:
        ok = False
        print(f"  [T^{n}] INSTRUMENT MISMATCH")
print(f"(0) instrument check (rising-factorial route == varphi/falling route): "
      f"{'PASS' if ok else 'FAIL'}  (n<={min(N,5)})", flush=True)

# ---- log F_P -----------------------------------------------------------------
def series_log(F, N):
    """log of a T-series with F[0]==1, truncated at T^N."""
    G = [F[n] for n in range(N+1)]; G[0] = sp.Integer(0)   # G = F - 1
    L = [sp.Integer(0)]*(N+1)
    P = [sp.Integer(0)]*(N+1); P[0] = sp.Integer(1)        # P = G^r, start r=0
    for r in range(1, N+1):
        Q = [sp.Integer(0)]*(N+1)
        for i in range(N+1):
            if P[i] == 0: continue
            for j in range(1, N+1-i):
                if G[j] != 0:
                    Q[i+j] += P[i]*G[j]
        P = [expand(x) for x in Q]
        s = Rational((-1)**(r-1), r)
        for n in range(N+1):
            if P[n] != 0: L[n] = L[n] + s*P[n]
    return [expand(x) for x in L]

print("Taking log ...", flush=True)
LF = series_log(FP, N)

def homog(poly, d, vars_=U):
    """total-degree-d homogeneous component."""
    p = sp.Poly(expand(poly), *vars_)
    out = sp.Integer(0)
    for mono, coeff in zip(p.monoms(), p.coeffs()):
        if sum(mono) == d:
            term = coeff
            for x, k in zip(vars_, mono): term *= x**k
            out += term
    return expand(out)

# ---- (1) Fact II(c) SHARP ----------------------------------------------------
print("\n(1) Fact II(c): deg_u [T^n] log F_P  (bound is n+1)")
sharp = True
for n in range(1, N+1):
    d = sp.Poly(LF[n], *U).total_degree()
    flag = "= n+1 (SHARP, so Xi != 0)" if d == n+1 else f"!! {d} vs n+1={n+1}"
    if d != n+1: sharp = False
    print(f"    n={n}: deg_u = {d}   {flag}")
print(f"    -> {'PASS: bound attained at every n, the top layer Xi is NONZERO' if sharp else 'FAIL'}")

# ---- the three layers --------------------------------------------------------
Xi   = {n: homog(LF[n], n+1) for n in range(1, N+1)}   # wt = +1
X0   = {n: homog(LF[n], n)   for n in range(1, N+1)}   # wt =  0
Xm1  = {n: homog(LF[n], n-1) for n in range(1, N+1)}   # wt = -1

Z = {u3: 0}
A   = {n: expand(Rational(1,2)*sp.diff(Xi[n], u3, 2).subs(Z))   for n in range(2, N+1)}
Rm1 = {n: expand(sp.diff(X0[n], u3).subs(Z))                    for n in range(2, N+1)}
C   = {n: expand(Xm1[n].subs(Z))                                for n in range(2, N+1)}

# ---- (2) (*) SYMBOLICALLY IN c  --  the off-slice test -----------------------
print("\n(2) (*) as an identity in c  [c is a FREE variable = the value of u_3]")
print("    claim:  [deg_(u1,u2)=n-1] ( ([T^n] log F_P)|_{u3=c} )  ==  A_n c^2 + R_n c + C_n")
star_ok = True
for n in range(2, N+1):
    lhs = homog(expand(LF[n].subs({u3: c})), n-1, (u1, u2))
    rhs = expand(A[n]*c**2 + Rm1[n]*c + C[n])
    d = expand(lhs - rhs)
    star_ok &= (d == 0)
    print(f"    n={n}: difference = {d}   {'OK' if d==0 else '*** MISMATCH ***'}")
print(f"    -> {'PASS  (holds for ALL c, not just c=0,-1)' if star_ok else 'FAIL'}")

# ---- (2b) the three-layer count: do w<=-2 layers really contribute 0? --------
print("\n(2b) do the w <= -2 layers contribute to degree n-1 after u3 -> c?")
for n in range(3, N+1):
    tot = sp.Integer(0)
    for w in range(-2, -n-1, -1):
        L = homog(LF[n], n+w)
        tot += homog(expand(L.subs({u3: c})), n-1, (u1, u2))
    print(f"    n={n}: sum over w<=-2 of [deg=n-1] = {expand(tot)}"
          f"   {'OK (zero)' if expand(tot)==0 else '*** NONZERO ***'}")

# ---- (3) Prop 3 --------------------------------------------------------------
print("\n(3) Prop 3:  R^(-1)_n = (1/2) d^2_{u3} Xi_n|_0  -  [deg=n-1]([T^n] log(F_{-1}/F_0))")
def logFc(cval):
    Fc = [expand(FP[n].subs({u3: cval})) for n in range(N+1)]
    assert Fc[0] == 1
    return series_log(Fc, N)
Lm1, L0 = logFc(-1), logFc(0)
prop3_ok = True
for n in range(2, N+1):
    corr = homog(expand(Lm1[n] - L0[n]), n-1, (u1, u2))
    d = expand(Rm1[n] - (A[n] - corr))
    prop3_ok &= (d == 0)
    print(f"    n={n}: difference = {d}   {'OK' if d==0 else '*** MISMATCH ***'}")
print(f"    -> {'PASS' if prop3_ok else 'FAIL'}")

# ---- (4) NEGATIVE CONTROLS ---------------------------------------------------
print("\n(4) negative controls (each MUST fail; if one passes the test is degenerate)")
bad = 0
for n in range(2, min(N, 6)+1):
    # (a) drop the Xi term
    if expand(Rm1[n] - (0 - homog(expand(Lm1[n]-L0[n]), n-1, (u1,u2)))) == 0: bad += 1; print(f"    n={n} (a) dropping A_n still passes -- DEGENERATE")
    # (b) wrong coefficient 1 instead of 1/2
    if expand(Rm1[n] - (2*A[n] - homog(expand(Lm1[n]-L0[n]), n-1, (u1,u2)))) == 0: bad += 1; print(f"    n={n} (b) coefficient 1 instead of 1/2 still passes -- DEGENERATE")
    # (c) use c=+1 in place of c=-1 (wrong slice)
    Lp1 = logFc(1)
    if expand(Rm1[n] - (A[n] - homog(expand(Lp1[n]-L0[n]), n-1, (u1,u2)))) == 0: bad += 1; print(f"    n={n} (c) c=+1 in place of c=-1 still passes -- DEGENERATE")
print(f"    -> {'PASS: every control FAILED as it should' if bad==0 else f'{bad} control(s) wrongly passed'}")

# ---- (5) are the three quantities actually nonzero? --------------------------
print("\n(5) non-triviality of the three objects (a check on zeros proves nothing)")
for n in range(2, N+1):
    print(f"    n={n}: A_n {'!=0' if A[n]!=0 else '== 0 !!'},  "
          f"R^(-1)_n {'!=0' if Rm1[n]!=0 else '== 0 !!'},  "
          f"X^(-1)_n|_0 {'!=0' if C[n]!=0 else '== 0 !!'}")
