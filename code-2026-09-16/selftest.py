"""Self-tests of the AHA action BEFORE any star computation.
If these fail, every number downstream is garbage."""
from hikita_star_clio import *
import random

random.seed(11)
m = 4
def rand_poly(m, nterms=5, deg=3):
    A = {}
    for _ in range(nterms):
        e = tuple(random.randint(0, deg) for _ in range(m))
        A = add(A, {e: ONE * random.randint(1, 5)})
    return A

ok = True
def chk(name, cond):
    global ok
    print(("  PASS  " if cond else "  FAIL  ") + name)
    ok = ok and cond

print("AHA relation checks (Def 2.x def:AHA), m=%d:" % m)
for trial in range(4):
    A = rand_poly(m)
    # (T_i - t)(T_i + 1) = 0
    for i in range(1, m):
        L = add(T(i, T(i, A, m), m), add(scal(-(t-ONE), T(i, A, m)), scal(-t, A)))
        chk("(T_%d - t)(T_%d + 1) = 0" % (i, i), not L)
    # T_i T_i^{-1} = id
    for i in range(1, m):
        chk("T_%d T_%d^{-1} = id" % (i, i), not add(Tinv(i, T(i, A, m), m), scal(-ONE, A)))
    # braid
    for i in range(1, m-1):
        L = T(i, T(i+1, T(i, A, m), m), m)
        R = T(i+1, T(i, T(i+1, A, m), m), m)
        chk("braid T_%d T_%d T_%d" % (i, i+1, i), not add(L, scal(-ONE, R)))
    break

print("\nY_i commute (stated after eq Eqn_commTY), m=%d:" % m)
A = rand_poly(m, 4, 2)
for i in range(1, m+1):
    for j in range(i+1, m+1):
        chk("Y_%d Y_%d = Y_%d Y_%d" % (i, j, j, i),
            not add(Y(i, Y(j, A, m), m), scal(-ONE, Y(j, Y(i, A, m), m))))

print("\nLemma 3.3 (Lem_iota_elem): q_(m)(e_r(Y)) = t^{r(r-1)/2} e_r(X), m=%d:" % m)
for r in range(0, m+1):
    lhs = e_Y(r, {tuple([0]*m): ONE}, m)          # e_r(Y) . 1
    rhs = scal(t**(r*(r-1)//2), e_poly(r, m))
    chk("r=%d" % r, not add(lhs, scal(-ONE, rhs)))

print("\nProp 3.6 (Prop_qmult_q=1): star -> ordinary product at q=1:")
for (a, r) in [(1,2),(2,2),(2,3)]:
    co, mm = star_e(a, r)
    from sympy import symbols, simplify, Rational
    import sympy
    qs, ts = symbols('q t')
    vals = {}
    for lam, c in co.items():
        expr = sympy.sympify(str(c)).subs(qs, 1)
        expr = sympy.simplify(expr)
        if expr != 0: vals[lam] = expr
    exp = {tuple(sorted((a, r), reverse=True)): 1}
    chk("e_%d * e_%d |_{q=1} = e_{(%d,%d)}" % (a, r, max(a,r), min(a,r)), vals == exp)

print("\nHikita Thm 3.12 (Thm_qtPieri_en): e_1 * e_r = (1-q^{-1})[r+1]_t e_{r+1} + q^{-1} e_1 e_r")
def qint(n):
    if n <= 0: return ZERO
    s = ZERO
    for i in range(n): s = s + t**i
    return s
for r in range(1, 6):
    co, mm = star_e(1, r)
    want = {(r+1,): (ONE - ONE/q)*qint(r+1), (r, 1): ONE/q}
    got = {k: v for k, v in co.items() if v}
    chk("r=%d" % r, got == {k: v for k, v in want.items() if v})

print("\nALL PASS" if ok else "\nSOME FAILED")
