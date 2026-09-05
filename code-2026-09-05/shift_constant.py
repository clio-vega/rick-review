"""
JOB 2 — the n-variable E_2-shift constant.  Clio, 2026-09-05 peer review.

Definitions (Rick, Day 152 section 1, verbatim):
    rising:  x^(m) = x(x+1)...(x+m-1)          [m factors, starts at x]
    T^+   :  u^alpha  ->  prod_i  u_i^(alpha_i)      extended linearly
    Psi^+ :  f -> T^+(f V)/V,   V = prod_{i<j}(u_i - u_j)
    tops^(n)[b] := weight-b homogeneous slice of Psi^+(e_2^b)
                   in the E-basis, under Rick's Day-123 grading w(E_k) = ceil(k/2).

Rick's two recorded statements about the same object:
    (A) root form   : tops^(n)[b] = (-1)^b prod_{r=0}^{b-1}( E_2 - (binom(n-1,2)+r) E_1 ) + (E_3+ terms)
    (B) shift rule  : tops^(n)[b] = tops^(3)[b] with  E_2 -> E_2 - (binom(n-1,2)-1) E_1
We check BOTH against the definition, and test rival readings of the constant.

Two independent implementations of Psi^+ (poly division vs. exact interpolation-free
expansion) must agree before any conclusion is drawn.
"""
import sympy as sp, math
from sympy.polys.polyfuncs import symmetrize

def rising(x, m):
    return sp.prod([x + j for j in range(m)]) if m > 0 else sp.Integer(1)

def _vander(u):
    n = len(u)
    return sp.expand(sp.prod([u[i] - u[j] for i in range(n) for j in range(i + 1, n)]))

def PsiPlus_div(f, u):
    """Implementation 1: T^+(fV)/V by multivariate exact division in u[0]."""
    V = _vander(u)
    P = sp.Poly(sp.expand(sp.expand(f) * V), *u)
    num = sp.expand(sum(c * sp.prod([rising(u[i], a[i]) for i in range(len(u))])
                        for a, c in P.terms()))
    q, r = sp.div(sp.Poly(num, u[0]), sp.Poly(V, u[0]))
    assert r.is_zero, "V does not divide (impl 1)"
    return sp.expand(q.as_expr())

def PsiPlus_cancel(f, u):
    """Implementation 2: same numerator, but divided by V via sp.cancel (different code path)."""
    V = _vander(u)
    P = sp.Poly(sp.expand(sp.expand(f) * V), *u)
    num = sp.expand(sum(c * sp.prod([rising(u[i], a[i]) for i in range(len(u))])
                        for a, c in P.terms()))
    out = sp.cancel(sp.together(num / V))
    assert sp.expand(sp.expand(out) * V - num) == 0, "V does not divide (impl 2)"
    return sp.expand(out)

def toE(poly, u, Es):
    if sp.expand(poly) == 0:
        return sp.Integer(0)
    s, rem, _ = symmetrize(sp.expand(poly), list(u), formal=True)
    assert sp.expand(rem) == 0, f"not symmetric: {rem}"
    return sp.expand(s.subs({sp.Symbol(f's{k}'): Es[k - 1] for k in range(1, len(u) + 1)}))

def tops(n, b, impl=PsiPlus_div):
    u = sp.symbols(f'u1:{n+1}')
    Es = sp.symbols(f'E1:{n+1}')
    e2 = sp.expand(sum(u[i] * u[j] for i in range(n) for j in range(i + 1, n)))
    psi = impl(sp.expand(e2 ** b), u)
    expr = toE(psi, u, Es)
    P = sp.Poly(expr, *Es)
    top = sp.Integer(0)
    for a, c in P.terms():
        w = sum(a[k] * math.ceil((k + 1) / 2) for k in range(n))
        if w == b:
            top += c * sp.prod([Es[k] ** a[k] for k in range(n)])
    return sp.expand(top), Es

# ---------------------------------------------------------------- hand check
print("=" * 78)
print("HAND CHECK (n=2, b=1).  By hand:  e_2 V = u1^2u2 - u1u2^2")
print("  T^+ -> u1(u1+1)u2 - u1u2(u2+1) = u1u2(u1-u2);  /V = u1u2 = E_2.")
t, Es = tops(2, 1)
print(f"  code says tops^(2)[1] = {t}      -> {'AGREES WITH HAND' if sp.expand(t - Es[1]) == 0 else '*** DISAGREES ***'}")
print(f"  binom(n-1,2) at n=2 is {int(sp.binomial(1,2))}; root form predicts E_2 - 0*E_1. consistent.")

# ------------------------------------------------- two implementations agree
print("\n" + "=" * 78)
print("CROSS-CHECK: two independent Psi^+ implementations")
print("=" * 78)
for (n, b) in [(3, 1), (3, 2), (4, 1), (4, 2)]:
    a1, _ = tops(n, b, PsiPlus_div)
    a2, _ = tops(n, b, PsiPlus_cancel)
    print(f"  n={n} b={b}: {'identical' if sp.expand(a1 - a2) == 0 else '*** MISMATCH ***'}")

# ------------------------------------------------------- full weight-b slices
print("\n" + "=" * 78)
print("FULL weight-b slices tops^(n)[b]  (all E_k, nothing suppressed)")
print("=" * 78)
DATA = {}
for n in range(3, 7):
    for b in range(1, 4):
        if n >= 6 and b >= 3:   # cost guard
            continue
        t, Es = tops(n, b)
        DATA[(n, b)] = (t, Es)
        print(f"  n={n} b={b}:  {sp.factor(t)}")

# -------------------------------------------- the E_3-and-up-free root pattern
print("\n" + "=" * 78)
print("ROOT START.  Kill E_3..E_n; factor; read the roots in units of E_1.")
print("  Sign knob: Rick's Psi-side is E_2 -> -E_2 vs my P-side (he conceded this,")
print("  UID 691).  I flip E_2 -> -E_2 and take (-1)^b so roots come out positive.")
print("=" * 78)
print(f"  {'n':>3} {'b':>3}   {'E3-free slice (P-side)':<40} {'roots':<16} {'binom(n-1,2)':>12}")
roots_seen = {}
for (n, b), (t, Es) in sorted(DATA.items()):
    free = sp.expand(t.subs({Es[k]: 0 for k in range(2, n)}))
    flipped = sp.expand(((-1) ** b) * free.subs({Es[1]: -Es[1]}))
    # roots in E_2 as multiples of E_1
    P = sp.Poly(flipped, Es[1])
    rts = sp.roots(sp.Poly(P.as_expr().subs({Es[0]: 1}), Es[1]))
    rl = sorted([sp.nsimplify(r) for r, m in rts.items() for _ in range(m)], key=lambda z: float(z))
    roots_seen[(n, b)] = rl
    print(f"  {n:>3} {b:>3}   {str(sp.factor(flipped)):<40} {str(rl):<16} {int(sp.binomial(n-1,2)):>12}")

print("\n  => root start r_min(n) vs binom(n-1,2):")
for n in range(3, 7):
    ks = [b for (m, b) in roots_seen if m == n]
    if not ks: continue
    b = max(ks)
    rmin = min(roots_seen[(n, b)])
    print(f"     n={n}: r_min = {rmin},  binom(n-1,2) = {int(sp.binomial(n-1,2))}  "
          f"-> {'MATCH' if sp.Integer(rmin) == sp.binomial(n-1,2) else '*** DIFFERS ***'}")

# ------------------------------------------------ Rick's explicit n=4,b=2 cell
print("\n" + "=" * 78)
print("RICK'S EXPLICIT TARGET (UID 680):  n=4, b=2  ->  E_2^2 - 5E_1E_2 + 6E_1^2 - 3E_3")
print("=" * 78)
E1_, E2_, E3_ = sp.symbols('E1 E2 E3')
his = E2_**2 - 5*E1_*E2_ + 6*E1_**2 - 3*E3_
t42, Es4 = DATA[(4, 2)]
mine_P = sp.expand(t42.subs({Es4[1]: -Es4[1], Es4[2]: -Es4[2]}))   # P-side, odd-E sign flip
print(f"  mine (raw, Psi-side)      : {sp.expand(t42)}")
print(f"  mine (E_2,E_3 -> -E_2,-E_3): {sp.expand(mine_P)}")
print(f"  his                        : {sp.expand(his)}")
print(f"  difference (his - mine_P)  : {sp.expand(his - mine_P)}")
print(f"  his E3-free roots          : {sorted(sp.roots(sp.Poly(sp.expand(his.subs({E3_:0,E1_:1})), E2_)).keys(), key=float)}")
print(f"  mine E3-free roots         : {roots_seen[(4,2)]}")

# --------------------------------------------------------- rival readings
print("\n" + "=" * 78)
print("RIVAL READINGS of the shift constant c_n  (his table: n=3..7 -> 0,2,5,9,14)")
print("  c_n is defined by: substituting E_2 -> E_2 - c_n E_1 into tops^(3)[b]")
print("  reproduces tops^(n)[b].  My computed base tops^(3)[b] has roots 1..b,")
print("  so c_n = r_min(n) - 1.")
print("=" * 78)
rivals = {
    'binom(n-1,2)-1': lambda n: sp.binomial(n - 1, 2) - 1,
    'n-2           ': lambda n: n - 2,
    '2(n-3)        ': lambda n: 2 * (n - 3),
    'binom(n-2,2)+1': lambda n: sp.binomial(n - 2, 2) + 1,
}
print(f"  {'n':>3} {'c_n (computed)':>15} " + " ".join(f"{k:>15}" for k in rivals))
computed_c = {}
for n in range(3, 7):
    ks = [b for (m, b) in roots_seen if m == n]
    if not ks: continue
    c = min(roots_seen[(n, max(ks))]) - 1
    computed_c[n] = c
    row = " ".join(f"{str(f(n)):>15}" for f in rivals.values())
    print(f"  {n:>3} {str(c):>15} " + row)
print("\n  agreement with computed c_n:")
for k, f in rivals.items():
    ok = [n for n in computed_c if sp.Integer(f(n)) == sp.Integer(computed_c[n])]
    bad = [n for n in computed_c if sp.Integer(f(n)) != sp.Integer(computed_c[n])]
    print(f"    {k}: agrees at n={ok}, FAILS at n={bad}")
