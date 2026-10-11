from util import *
import sys, sympy as sp
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
t0 = int(rng.integers(2, p))
STRAT = {}
def cost(lam): return math.prod(math.comb(sum(lam), k) for k in sorted(lam)[:-1])
cache = {}
def es(lam, tt, K):
    key = (lam, tt, K)
    if key not in cache: cache[key] = estar(Ctx(1, tt, K, maxe=len(lam) + 1), lam)
    return cache[key]
Tcache = {}
def Tp(a, kind, rho, tt=t0):
    """T_a g in p-basis, g = p_rho / e_rho / P_rho (in a vars)"""
    key = (a, kind, rho, tt)
    if key not in Tcache:
        n = a + sum(rho)
        g = {"p": lambda Y: pval(Y, rho), "e": lambda Y: eval_e(Y, rho), "P": lambda Y: P_at(rho, Y, tt)}[kind]
        eb = scalar_ebasis(n, n, lambda xb: T_at(a, g, xb, tt))
        Tcache[key] = (eb, ebasis_to_p(eb))
    return Tcache[key]
def mxy(x, y): return 2 if x == y else 1
# ---- Thm 6.2 constant-term adjoint formula ----
z = sp.symbols('z1:5'); ts = sp.Integer(t0)
def laurent_mul(A, B):
    out = {}
    for ea, ca in A.items():
        for eb, cb in B.items():
            k = tuple(i + j for i, j in zip(ea, eb)); out[k] = (out.get(k, 0) + ca * cb) % p
    return out
def poly_to_dict(expr, a):
    P_ = sp.Poly(sp.expand(expr), *z[:a]); out = {}
    for mon, c in P_.terms():
        num, den = sp.fraction(sp.Rational(c)) if c.is_Rational else (None, None)
        out[mon] = int(num) % p * inv(int(den)) % p
    return out
def gpoly(kind, rho, a, tt):
    if kind == "p": return sp.prod([sum(zi ** r for zi in z[:a]) for r in rho])
    if kind == "e": return sp.prod([sp.polys.specialpolys.symmetric_poly(r, *z[:a]) for r in rho])
    lam = tuple(rho) + (0,) * (a - len(rho)); tot = 0
    for w in itertools.permutations(range(a)):
        y = [z[i] for i in w]
        tot += sp.prod([y[i] ** lam[i] for i in range(a)]) * sp.prod([(y[i] - tt * y[j]) / (y[i] - y[j]) for i in range(a) for j in range(i + 1, a)])
    vl = 1
    for k, m in Counter(lam).items():
        for j in range(1, m + 1): vl *= (1 - tt ** j) / (1 - tt)
    return sp.cancel(sp.together(tot / vl))
R = Res("Thm6.2 phi_a <T_a g,F>_t = CT[Z g(z) F(1/z) Omega], Omega expanded in z_i/z_j (i<j)")
Rneg = Res("Thm6.2 NEG: expand Omega in z_j/z_i instead")
tsmall = 3  # exact small t for sympy P-polys; reduce mod p
for a in (1, 2, 3):
    for d_ in range(0, 4):
        n = a + d_
        for rho in (list(partitions(d_)) if d_ else [()]):
            for kind in ("p", "e", "P"):
                if kind == "P" and len(rho) > a: continue
                if kind == "e" and rho and rho[0] > a: continue
                if kind != "p" and not rho: continue
                eb, Gp = Tp(a, kind, rho, tsmall) if rho else (None, None)
                if not rho:  # g = 1
                    eb = scalar_ebasis(n, n, lambda xb: T_at(a, lambda Y: np.ones(Y.shape[0], dtype=np.int64), xb, tsmall)); Gp = ebasis_to_p(eb)
                gz = poly_to_dict(sp.prod(z[:a]) * gpoly(kind, rho, a, sp.Integer(tsmall)), a) if rho else poly_to_dict(sp.prod(z[:a]), a)
                for F in partitions(n):
                    Fp = {F: 1}
                    lhs = hl_pair_pp(Gp, Fp, tsmall)
                    for i in range(1, a + 1): lhs = lhs * (1 - pow(tsmall, i, p)) % p
                    # F(1/z) for p_F
                    Fz = {(0,) * a: 1}
                    for r in F:
                        Fz = laurent_mul(Fz, {tuple(-r if q == i else 0 for q in range(a)): 1 for i in range(a)})
                    prod = laurent_mul(gz, Fz)
                    for rev in (False, True):
                        B = n
                        Om = {(0,) * a: 1}
                        for i in range(a):
                            for j in range(i + 1, a):
                                fac = {}
                                for m_ in range(0, B + 1):
                                    w = 1 if m_ == 0 else (pow(tsmall, m_, p) - pow(tsmall, m_ - 1, p)) % p
                                    if rev: w = inv(tsmall) if m_ == 0 else (inv(pow(tsmall, m_ + 1, p)) - inv(pow(tsmall, m_, p))) % p
                                    e = [0] * a
                                    if not rev: e[i] += m_; e[j] -= m_
                                    else: e[i] -= m_; e[j] += m_
                                    fac[tuple(e)] = w
                                Om = laurent_mul(Om, fac)
                        ct = 0
                        for e, c in prod.items():
                            ct = (ct + c * Om.get(tuple(-x for x in e), 0)) % p
                        (Rneg if rev else R).chk(ct == lhs, f"a={a} {kind}{rho} F=p{F}");
                        STRAT.setdefault((rev,a),[0,0])[0 if ct==lhs else 1]+=1
print(R); print(Rneg, "(expected FAIL for a>=2)")
print("\n--- stratification of the Omega-reversal control by a (a = #variables, Omega has C(a,2) pairs) ---")
for rev in (False, True):
    for a in (1,2,3):
        ok,bad = STRAT.get((rev,a),[0,0])
        print(f"  rev={str(rev):5s} a={a}  C(a,2)={a*(a-1)//2}  ok={ok:3d} bad={bad:3d}")
