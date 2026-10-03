"""
Clio, 2026-10-03 peer review of Rick, "DS from (N)" (WIP 81f00ad).

Independent instrument, FULLY SYMBOLIC IN BOTH s AND t (10-02 ran t numeric).
Macdonald P built by triangular solve of the D_1 eigenvalue equation.
No Sage, no imported Macdonald/Kostka code: Kostka numbers from an SSYT count,
Kostka-Foulkes from s_rho = sum_nu K_{rho nu}(tau) P_nu(x;0,tau).

Conventions are Rick's:  P_nu := P_nu(x; q=s, t_Mac=tau), tau = 1/t,
  T_nu = t^{n(nu)} s^{n(nu')},  N P_nu = T_nu P_nu,  n(lam) = sum (i-1) lam_i.

Order of business (an instrument must reproduce a KNOWN value before any
claim below is believed):
  [A] validation: D_1 P_nu = eps_nu P_nu, and P_{1^k} == e_k exactly.
  [B] Lemma 1: B support / B_{nu nu'}=1 / B regular at s=0 / B(0) = HL e-expansion
  [C] Lemma 2: A = B^{-1}, support, A_{lam lam'}=1, A regular at s=0
  [D] Lemma 3: a^HL_{lam nu}(tau) = sum_rho K_{rho nu}(tau) K_{rho' lam}; (a) and (b)
  [E] (2.1) against e^star built from the E_k operators directly
  [F] (S),(L),(Val)
  [G] *** THE TARGET *** d_{lam mu}(t) = sum_rho t^{n(rho)-n(lam')} Ktilde_{rho mu'}(t) K_{rho' lam}
      plus d in Z[t], d(0)=1, d(1)=M_{lam mu'}
  [H] (V) c|_{s=1} = delta
  [I] Op-DS: support {rho >= mu u k} and lead s^{sum min(mu_i,k)}  <-- Rick: "Not
      checked separately by script".  Also the Pieri top coefficient = 1.
  [J] negative controls -- must FIRE.
"""
import sympy as sp
from itertools import combinations, permutations
import sys

s, t = sp.symbols('s t')
tau = 1/t
m = int(sys.argv[1]) if len(sys.argv) > 1 else 4
NMAX = int(sys.argv[2]) if len(sys.argv) > 2 else m
xs = sp.symbols('x1:%d' % (m+1))

def parts(n, k=None):
    k = k or m
    def go(n, k, mx):
        if n == 0: yield []; return
        if k == 0: return
        for a in range(min(n, mx), 0, -1):
            for rest in go(n-a, k-1, a): yield [a]+rest
    return list(go(n, k, n))

def nstat(lam): return sum(i*p for i, p in enumerate(lam))
def conj(lam):
    lam = [p for p in lam if p > 0]
    return [sum(1 for p in lam if p > j) for j in range(lam[0])] if lam else []
def pad(lam, L=None): return tuple(list(lam) + [0]*((L or m)-len(lam)))
def dom_leq(a, b):
    """a <| b  (a dominated by b): partial sums of a <= those of b, |a|=|b|"""
    a, b = list(a), list(b)
    assert sum(a) == sum(b)
    sa = sb = 0
    for i in range(max(len(a), len(b))):
        sa += a[i] if i < len(a) else 0
        sb += b[i] if i < len(b) else 0
        if sa > sb: return False
    return True

# ---------------- symmetric polynomials as dict exponent-tuple -> coeff -------
def mono_sym(lam):
    return {e: sp.Integer(1) for e in set(permutations(pad(lam)))}
def e_sym(k):
    if k == 0: return {tuple([0]*m): sp.Integer(1)}
    if k > m: return {}
    d = {}
    for A in combinations(range(m), k):
        ex = [0]*m
        for i in A: ex[i] = 1
        d[tuple(ex)] = sp.Integer(1)
    return d
def add(a, b, c=1):
    out = dict(a)
    for k, v in b.items():
        nv = sp.together(out.get(k, 0) + c*v)
        out[k] = nv
    return {k: v for k, v in out.items() if sp.simplify(v) != 0}
def mul(a, b):
    out = {}
    for e1, c1 in a.items():
        for e2, c2 in b.items():
            k = tuple(i+j for i, j in zip(e1, e2))
            out[k] = sp.cancel(out.get(k, 0) + c1*c2)
    return {k: v for k, v in out.items() if v != 0}
def e_lam_poly(lam):
    out = {tuple([0]*m): sp.Integer(1)}
    for k in lam: out = mul(out, e_sym(k))
    return out
def to_mcoeffs(d, n):
    return {tuple(nu): sp.cancel(d.get(pad(nu), sp.Integer(0))) for nu in parts(n)}
def from_mcoeffs(cf, n):
    out = {}
    for nu, c in cf.items():
        if c != 0: out = add(out, mono_sym(list(nu)), c)
    return out

# ---------------- operators ---------------------------------------------------
def apply_op(d, pairs):
    poly = sum(c*sp.prod([xs[i]**e for i, e in enumerate(ex)]) for ex, c in d.items())
    out = 0
    for coef, I, sh in pairs:
        sub = {xs[i]: sh*xs[i] for i in I}
        out += coef*poly.subs(sub, simultaneous=True)
    out = sp.cancel(sp.together(out))
    num, den = sp.fraction(out)
    num = sp.expand(num)
    P = sp.Poly(num, *xs)
    res = {}
    for ex, c in zip(P.monoms(), P.coeffs()):
        v = sp.cancel(c/den)
        if v != 0: res[tuple(ex)] = v
    return res

D1p = [(sp.prod([(tau*xs[i]-xs[j])/(xs[i]-xs[j]) for j in range(m) if j != i]),
        (i,), s) for i in range(m)]

def Ek_pairs(k):
    """Rick's E_k:  sum_{|A|=k} prod_{i in A, j notin A} (x_i - t x_j)/(x_i - x_j)
                    * X_A * F(X_A -> s X_A)"""
    pr = []
    for A in combinations(range(m), k):
        Ac = [j for j in range(m) if j not in A]
        c = sp.prod([xs[i] for i in A])
        for i in A:
            for j in Ac: c *= (xs[i]-t*xs[j])/(xs[i]-xs[j])
        pr.append((c, A, s))
    return pr
EK = {k: Ek_pairs(k) for k in range(1, m+1)}

def eps(nu):
    return sp.expand(sum(s**ni*tau**(m-1-i) for i, ni in enumerate(pad(nu))))

# ---------------- build Macdonald P by triangular solve -----------------------
print("building Macdonald P, m=%d, n<=%d, symbolic in s and t ..." % (m, NMAX))
Pm = {}   # nu -> {mu: u_{nu mu}}  (m-basis coefficients)
Ppoly = {}
for n in range(0, NMAX+1):
    B = parts(n)
    if n == 0: B = [[]]
    # matrix of D_1 in m-basis: D1 m_sigma = sum_kappa Mat[kappa][sigma] m_kappa
    Mat = {}
    for sig in B:
        col = to_mcoeffs(apply_op(mono_sym(sig), D1p), n) if n > 0 else {(): None}
        Mat[tuple(sig)] = col
    # order by dominance, descending (largest first)
    order = sorted([tuple(b) for b in B], key=lambda a: (-nstat(list(a)),))
    # key(a) = #{b : a <| b}; ascending => LARGEST in dominance first, which is
    # what the back-substitution needs (u_sigma for sigma |> kappa must be known).
    _ord = list(order)
    order = sorted(_ord, key=lambda a: sum(1 for b in _ord if dom_leq(list(a), list(b))))
    for nu in order:
        if n == 0:
            Pm[nu] = {nu: sp.Integer(1)}; Ppoly[nu] = {tuple([0]*m): sp.Integer(1)}; continue
        u = {nu: sp.Integer(1)}
        for kap in order:
            if kap == nu or not dom_leq(list(kap), list(nu)): continue
            # (eps_kap - eps_nu) u_{nu kap} = - sum_{sigma != kap} Mat[sigma][kap] u_{nu sigma}
            acc = 0
            for sig, usig in u.items():
                if sig == kap: continue
                acc += Mat[sig].get(kap, 0)*usig
            den = sp.expand(eps(list(kap)) - eps(list(nu)))
            assert sp.simplify(den) != 0, ("eigenvalue collision", nu, kap)
            u[kap] = sp.cancel(-acc/den)
        u = {a: sp.cancel(b) for a, b in u.items() if sp.cancel(b) != 0}
        Pm[nu] = u
        Ppoly[nu] = from_mcoeffs(u, n)
print("  done.")

Nev = {nu: t**nstat(list(nu))*s**nstat(conj(list(nu))) for nu in Pm}

# ================= [A] instrument validation ==================================
print("\n[A] instrument validation (must pass before anything below is believed)")
okA = True
for nu, u in Pm.items():
    if sum(nu) == 0: continue
    got = to_mcoeffs(apply_op(Ppoly[nu], D1p), sum(nu))
    ev = eps(list(nu))
    for mu, c in u.items():
        if sp.simplify(sp.cancel(got.get(mu, 0) - ev*c)) != 0:
            okA = False; print("    FAIL eigen", nu, mu)
print("    D_1 P_nu = eps_nu P_nu for all %d partitions : %s" % (len(Pm)-1, okA))
okK = True
for k in range(1, min(m, NMAX)+1):
    nu = tuple([1]*k)
    same = add(Ppoly[nu], e_sym(k), -1) == {}
    print("    KNOWN VALUE  P_{1^%d} == e_%d : %s" % (k, k, same))
    okK = okK and same
assert okA and okK, "instrument failed validation -- stop"

# ---------------- change of basis: e-expansion --------------------------------
def e_expand(d, n):
    B = parts(n)
    if n == 0: return {(): d.get(tuple([0]*m), 0)}
    Mat = sp.Matrix([[to_mcoeffs(e_lam_poly(list(nu)), n)[tuple(mu)] for nu in B] for mu in B])
    cf = to_mcoeffs(d, n)
    sol = Mat.solve(sp.Matrix([cf[tuple(mu)] for mu in B]))
    return {tuple(B[i]): sp.cancel(sol[i]) for i in range(len(B))}

def P_expand(d, n):
    B = parts(n)
    if n == 0: return {(): d.get(tuple([0]*m), 0)}
    Mat = sp.Matrix([[Pm[tuple(nu)].get(tuple(mu), 0) for nu in B] for mu in B])
    cf = to_mcoeffs(d, n)
    sol = Mat.solve(sp.Matrix([cf[tuple(mu)] for mu in B]))
    return {tuple(B[i]): sp.cancel(sol[i]) for i in range(len(B))}

# ---------------- s-valuation helpers ----------------------------------------
def val_s(expr):
    expr = sp.cancel(sp.together(expr))
    if expr == 0: return None
    num, den = sp.fraction(expr)
    def low(p):
        pp = sp.Poly(sp.expand(p), s)
        return min(mo[0] for mo in pp.monoms())
    return low(num) - low(den)

def coeff_s(expr, v):
    """coefficient of s^v in the Laurent expansion at s=0 (expr regular there after /s^v)"""
    q = sp.cancel(sp.together(sp.cancel(expr)/s**v))
    return sp.cancel(sp.simplify(q.subs(s, 0)))

def regular_at(expr, var, pt):
    e = sp.cancel(sp.together(expr))
    num, den = sp.fraction(e)
    return sp.simplify(den.subs(var, pt)) != 0

# ---------------- Kostka numbers (SSYT count, independent) --------------------
def hstrips(alpha, k):
    """all gamma with gamma subset alpha, |alpha|-|gamma|=k, alpha/gamma a horizontal strip"""
    alpha = [a for a in alpha if a > 0]
    L = len(alpha)
    res = []
    def go(i, cur, left):
        if i == L:
            if left == 0: res.append(tuple(c for c in cur if c > 0))
            return
        lo = alpha[i+1] if i+1 < L else 0      # gamma_i >= alpha_{i+1}
        hi = alpha[i]
        for g in range(lo, hi+1):
            d = alpha[i]-g
            if d <= left: go(i+1, cur+[g], left-d)
    go(0, [], k)
    return res

from functools import lru_cache
@lru_cache(maxsize=None)
def kostka(alpha, beta):
    alpha = tuple(a for a in alpha if a > 0); beta = tuple(b for b in beta if b > 0)
    if sum(alpha) != sum(beta): return 0
    if not beta: return 1 if not alpha else 0
    tot = 0
    for g in hstrips(alpha, beta[-1]):
        tot += kostka(g, beta[:-1])
    return tot

@lru_cache(maxsize=None)
def zero_one_count(rows, cols):
    """# 0-1 matrices with given row sums and column sums"""
    rows = tuple(r for r in rows if r > 0)
    if not rows: return 1 if all(c == 0 for c in cols) else 0
    r, rest = rows[0], rows[1:]
    tot = 0
    for A in combinations(range(len(cols)), r):
        nc = list(cols)
        ok = True
        for i in A:
            nc[i] -= 1
            if nc[i] < 0: ok = False; break
        if ok: tot += zero_one_count(rest, tuple(nc))
    return tot

def schur_poly(rho, n):
    """s_rho = sum_kappa K_{rho kappa} m_kappa"""
    out = {}
    for kap in parts(n):
        K = kostka(tuple(rho), tuple(kap))
        if K: out = add(out, mono_sym(kap), sp.Integer(K))
    return out

# ================= [B] Lemma 1: P in e =======================================
print("\n[B] Lemma 1 (P_nu = sum_mu B_{nu mu} e_mu)")
Bmat, HLm = {}, {}
okB = {'supp': True, 'uni': True, 'reg': True, 'hl': True}
for n in range(1, NMAX+1):
    for nu in parts(n):
        cf = e_expand(Ppoly[tuple(nu)], n)
        Bmat[tuple(nu)] = cf
        for mu, v in cf.items():
            if sp.simplify(v) == 0: continue
            if not dom_leq(list(conj(nu)), list(mu)):      # need mu |> nu'
                okB['supp'] = False; print("    SUPPORT VIOLATION", nu, mu)
            if not regular_at(v, s, 0): okB['reg'] = False; print("    POLE at s=0", nu, mu)
        if sp.simplify(cf.get(tuple(conj(nu)), 0) - 1) != 0:
            okB['uni'] = False; print("    B_{nu nu'} != 1", nu)
# HL P_nu(x;tau) = P_nu|_{s=0}  (legitimate only because okB['reg'])
assert okB['reg'], "P has a pole at s=0 -- Lemma 1(3) would be FALSE"
for nu, u in Pm.items():
    if sum(nu) == 0: continue
    HLm[nu] = {mu: sp.cancel(sp.cancel(v).subs(s, 0)) for mu, v in u.items()}
for n in range(1, NMAX+1):
    for nu in parts(n):
        hl = from_mcoeffs(HLm[tuple(nu)], n)
        lhs = e_expand(hl, n)
        for mu in parts(n):
            a = sp.cancel(sp.cancel(Bmat[tuple(nu)].get(tuple(mu), 0)).subs(s, 0))
            b = sp.cancel(lhs.get(tuple(mu), 0))
            if sp.simplify(a-b) != 0: okB['hl'] = False
print("    support mu |> nu' : %s | B_{nu nu'}=1 : %s | regular at s=0 : %s | B(0)=HL e-exp : %s"
      % (okB['supp'], okB['uni'], okB['reg'], okB['hl']))

# ================= [C] Lemma 2: e in P =======================================
print("\n[C] Lemma 2 (e_lam = sum_nu A_{lam nu} P_nu)")
Amat = {}
okC = {'supp': True, 'uni': True, 'reg': True, 'inv': True}
for n in range(1, NMAX+1):
    B = parts(n)
    for lam in B:
        cf = P_expand(e_lam_poly(lam), n)
        Amat[tuple(lam)] = cf
        for nu, v in cf.items():
            if sp.simplify(v) == 0: continue
            if not dom_leq(list(nu), list(conj(lam))): okC['supp'] = False; print("    SUPP", lam, nu)
            if not regular_at(v, s, 0): okC['reg'] = False; print("    POLE", lam, nu)
        if sp.simplify(cf.get(tuple(conj(lam)), 0) - 1) != 0: okC['uni'] = False; print("    A_{lam lam'}!=1", lam)
    # A = B^{-1} as matrices (rows lam -> nu) vs (rows nu -> mu)
    MA = sp.Matrix([[Amat[tuple(l)].get(tuple(nu), 0) for nu in B] for l in B])
    MB = sp.Matrix([[Bmat[tuple(nu)].get(tuple(mu), 0) for mu in B] for nu in B])
    if sp.simplify(MA*MB - sp.eye(len(B))) != sp.zeros(len(B), len(B)): okC['inv'] = False
print("    support nu <| lam' : %s | A_{lam lam'}=1 : %s | regular at s=0 : %s | A=B^{-1} : %s"
      % (okC['supp'], okC['uni'], okC['reg'], okC['inv']))

# ================= [D] Lemma 3 ===============================================
print("\n[D] Lemma 3  a^HL_{lam nu}(tau) = sum_rho K_{rho nu}(tau) K_{rho' lam}")
# Kostka-Foulkes from s_rho = sum_nu KF[rho][nu] * HL P_nu   (independent route)
KF = {}
for n in range(1, NMAX+1):
    for rho in parts(n):
        cf = {}
        Bp = parts(n)
        Mat = sp.Matrix([[HLm[tuple(nu)].get(tuple(mu), 0) for nu in Bp] for mu in Bp])
        rhs = to_mcoeffs(schur_poly(rho, n), n)
        sol = Mat.solve(sp.Matrix([rhs[tuple(mu)] for mu in Bp]))
        for i, nu in enumerate(Bp):
            v = sp.cancel(sp.simplify(sol[i]))
            if v != 0: cf[tuple(nu)] = v
        KF[tuple(rho)] = cf
okD = {'l3': True, 'a0': True, 'degb': True, 'monic': True}
for n in range(1, NMAX+1):
    for lam in parts(n):
        for nu in parts(n):
            aHL = sp.cancel(sp.cancel(Amat[tuple(lam)].get(tuple(nu), 0)).subs(s, 0))
            rhs = 0
            for rho in parts(n):
                K1 = KF[tuple(rho)].get(tuple(nu), 0)
                K2 = kostka(tuple(conj(rho)), tuple(lam))
                if K1 != 0 and K2 != 0: rhs += K1*sp.Integer(K2)
            if sp.simplify(sp.cancel(aHL - rhs)) != 0:
                okD['l3'] = False; print("    L3 FAIL", lam, nu, sp.simplify(aHL-rhs))
            # (a) a^HL(tau=0) = K_{nu' lam}   [tau = 1/t, so tau->0 is t->oo]
            a_at0 = sp.limit(sp.cancel(aHL), t, sp.oo)
            if sp.simplify(a_at0 - sp.Integer(kostka(tuple(conj(nu)), tuple(lam)))) != 0:
                okD['a0'] = False; print("    L3(a) FAIL", lam, nu)
            # (b) deg_tau a^HL <= n(nu)-n(lam'), coefficient there = 1 when nu <| lam'
            if sp.simplify(aHL) != 0:
                D = nstat(list(nu)) - nstat(conj(lam))
                top = sp.limit(sp.cancel(aHL)*t**D, t, 0)   # tau^D coeff: tau->oo <=> t->0
                if not top.is_finite: okD['degb'] = False; print("    L3(b) deg FAIL", lam, nu)
                elif dom_leq(list(nu), conj(lam)) and sp.simplify(top-1) != 0:
                    okD['monic'] = False; print("    L3(b) lead!=1", lam, nu, top)
print("    Lemma 3 identity : %s | (a) a^HL(0)=K_{nu' lam} : %s | (b) deg bound : %s | lead=1 : %s"
      % (okD['l3'], okD['a0'], okD['degb'], okD['monic']))
# Kostka-Foulkes monicity of degree n(nu)-n(rho), used by Lemma 3(b)
okKF = True
for n in range(1, NMAX+1):
    for rho in parts(n):
        for nu in parts(n):
            v = KF[tuple(rho)].get(tuple(nu), 0)
            if v == 0: continue
            D = nstat(list(nu)) - nstat(list(rho))
            top = sp.limit(sp.cancel(v)*t**D, t, 0)
            if sp.simplify(top - 1) != 0: okKF = False; print("    KF not monic deg n(nu)-n(rho)", rho, nu, top)
print("    K_{rho nu}(tau) monic of degree n(nu)-n(rho) : %s" % okKF)

# ================= e^star_lam built DIRECTLY from the E_k operators ===========
print("\n[E] e^star_lam = E_{lam_1}...E_{lam_l}(1) from the operators; then (2.1)")
ONE = {tuple([0]*m): sp.Integer(1)}
# cross-check first: E_k(1) == e_k  (equivalent to N e_k = t^{C(k,2)} e_k, my 10-02 6.1)
okE1 = True
for k in range(1, min(m, NMAX)+1):
    d = add(apply_op(ONE, EK[k]), e_sym(k), -1)
    if d != {}: okE1 = False
print("    cross-check  E_k(1) == e_k  (i.e. N e_k = t^{C(k,2)} e_k) : %s" % okE1)

estar, cmat = {}, {}
for n in range(1, NMAX+1):
    for lam in parts(n):
        cur = ONE
        for k in reversed(lam): cur = apply_op(cur, EK[k])
        estar[tuple(lam)] = cur
        cmat[tuple(lam)] = e_expand(cur, n)

ok21 = True
for n in range(1, NMAX+1):
    for lam in parts(n):
        for mu in parts(n):
            lhs = cmat[tuple(lam)].get(tuple(mu), 0)
            rhs = 0
            for nu in parts(n):
                A = Amat[tuple(lam)].get(tuple(nu), 0)
                Bb = Bmat[tuple(nu)].get(tuple(mu), 0)
                if A == 0 or Bb == 0: continue
                rhs += A*s**nstat(conj(list(nu)))*t**nstat(list(nu))*Bb
            rhs = sp.cancel(t**(-nstat(conj(list(lam))))*rhs)
            if sp.simplify(sp.cancel(lhs-rhs)) != 0:
                ok21 = False; print("    (2.1) FAIL", lam, mu)
print("    (2.1) c_{lam mu} = t^{-n(lam')} sum_nu A s^{n(nu')} t^{n(nu)} B : %s" % ok21)

# ================= [F] (S), (L), (Val) =======================================
print("\n[F] (S) support, (L) lead, (Val) exact valuation")
okS = okL = okV = True
nz = 0
for n in range(1, NMAX+1):
    for lam in parts(n):
        for mu in parts(n):
            c = sp.cancel(cmat[tuple(lam)].get(tuple(mu), 0))
            if sp.simplify(c) == 0:
                if dom_leq(list(lam), list(mu)) and tuple(lam) != tuple(mu): pass
                continue
            nz += 1
            if not dom_leq(list(lam), list(mu)): okS = False; print("    (S) FAIL", lam, mu)
            if val_s(c) != nstat(list(mu)): okV = False; print("    (Val) FAIL", lam, mu, val_s(c), nstat(list(mu)))
        cll = sp.cancel(cmat[tuple(lam)].get(tuple(lam), 0))
        if sp.simplify(cll - s**nstat(list(lam))) != 0: okL = False; print("    (L) FAIL", lam)
print("    (S) c!=0 => mu |> lam : %s   [%d nonzero coefficients]" % (okS, nz))
print("    (L) c_{lam lam} = s^{n(lam)} : %s" % okL)
print("    (Val) val_s c_{lam mu} = n(mu) EXACTLY : %s" % okV)

# ================= [G] THE TARGET: the d-formula ==============================
print("\n[G] d_{lam mu}(t) = sum_rho t^{n(rho)-n(lam')} Ktilde_{rho mu'}(t) K_{rho' lam}")
def Ktilde(rho, nu):
    """cocharge KF: t^{n(nu)-n(rho)} K_{rho nu}(1/t);  KF[rho][nu] already = K(1/t)"""
    v = KF[tuple(rho)].get(tuple(nu), 0)
    if v == 0: return sp.Integer(0)
    return sp.cancel(t**(nstat(list(nu))-nstat(list(rho)))*v)
okG = {'formula': True, 'poly': True, 'd0': True, 'd1': True, 'aHLform': True, 'N': True}
rows = []
for n in range(1, NMAX+1):
    for lam in parts(n):
        for mu in parts(n):
            c = sp.cancel(cmat[tuple(lam)].get(tuple(mu), 0))
            if sp.simplify(c) == 0: continue
            d = sp.cancel(sp.expand(coeff_s(c, nstat(list(mu)))))
            mup = conj(list(mu)); lamp = conj(list(lam))
            rhs = 0
            for rho in parts(n):
                K2 = kostka(tuple(conj(list(rho))), tuple(lam))
                if K2 == 0: continue
                kt = Ktilde(rho, mup)
                if kt == 0: continue
                rhs += t**(nstat(list(rho))-nstat(lamp))*kt*sp.Integer(K2)
            rhs = sp.cancel(sp.expand(rhs))
            if sp.simplify(sp.cancel(d-rhs)) != 0:
                okG['formula'] = False; print("    d-FORMULA FAIL", lam, mu, sp.simplify(d-rhs))
            # also the intermediate form d = t^{n(mu')-n(lam')} a^HL_{lam mu'}(1/t)
            aHL = sp.cancel(sp.cancel(Amat[tuple(lam)].get(tuple(mup), 0)).subs(s, 0))
            alt = sp.cancel(t**(nstat(mup)-nstat(lamp))*aHL)
            if sp.simplify(sp.cancel(d-alt)) != 0:
                okG['aHLform'] = False; print("    d = t^{n(mu')-n(lam')} a^HL FAIL", lam, mu)
            # d in Z[t], d(0)=1, d(1)=M_{lam mu'}
            pd = sp.Poly(sp.expand(d), t) if sp.simplify(sp.denom(sp.cancel(d))) == 1 else None
            if pd is None or not all(cc.is_integer for cc in pd.all_coeffs()):
                okG['poly'] = False; print("    d NOT in Z[t]", lam, mu, d)
            else:
                if not all(cc >= 0 for cc in pd.all_coeffs()): okG['N'] = False
            if sp.simplify(sp.cancel(d).subs(t, 0) - 1) != 0:
                okG['d0'] = False; print("    d(0)!=1", lam, mu, sp.cancel(d).subs(t,0))
            M = zero_one_count(tuple(lam), tuple(pad(mup, max(len(mup), 1))))
            if sp.simplify(sp.cancel(d).subs(t, 1) - M) != 0:
                okG['d1'] = False; print("    d(1)!=M_{lam mu'}", lam, mu, sp.cancel(d).subs(t,1), M)
            rows.append((tuple(lam), tuple(mu), sp.expand(d)))
print("    Kostka-Foulkes d-formula : %s" % okG['formula'])
print("    d = t^{n(mu')-n(lam')} a^HL_{lam mu'}(1/t) : %s" % okG['aHLform'])
print("    d in Z[t] : %s | d(0)=1 : %s | d(1)=M_{lam mu'} : %s | d in N[t] : %s"
      % (okG['poly'], okG['d0'], okG['d1'], okG['N']))
print("    (%d nonzero d checked)" % len(rows))

# ================= [H] (V) c|_{s=1} = delta ==================================
print("\n[H] (V) c_{lam mu}|_{s=1} = delta_{lam mu}")
okH, okHreg = True, True
for n in range(1, NMAX+1):
    for lam in parts(n):
        for mu in parts(n):
            c = sp.cancel(cmat[tuple(lam)].get(tuple(mu), 0))
            if sp.simplify(c) == 0: continue
            if not regular_at(c, s, 1): okHreg = False; print("    POLE at s=1", lam, mu); continue
            v = sp.simplify(sp.cancel(c).subs(s, 1))
            want = 1 if tuple(lam) == tuple(mu) else 0
            if sp.simplify(v-want) != 0: okH = False; print("    (V) FAIL", lam, mu, v)
print("    regular at s=1 : %s | c|_{s=1} = delta : %s" % (okHreg, okH))
# the input P_nu(x;1,tau) = e_{nu'} that (V) rests on
okPV = True
for nu, u in Pm.items():
    if sum(nu) == 0: continue
    pol = {a: sp.cancel(sp.cancel(b).subs(s, 1)) for a, b in Ppoly[nu].items()}
    if add(pol, e_lam_poly(conj(list(nu))), -1) != {}: okPV = False; print("    P_nu(x;1,tau) != e_{nu'}", nu)
print("    input used by (V):  P_nu(x; q=1, tau) = e_{nu'} : %s" % okPV)

# ================= [G2] the 25 d-polynomials, and vanishing at special t ======
print("\n[G2] the d_{lam mu}(t) table, and whether any vanishes at a numeric t")
print("     (support is the FULL up-set: %d pairs mu |> lam expected)" % len(rows))
bad_t = []
for lam, mu, d in rows:
    rts = sp.solve(sp.Eq(sp.expand(d), 0), t)
    rr = [r for r in rts if r.is_real]
    print("     lam=%-12s mu=%-12s d = %-28s roots %s" % (list(lam), list(mu), sp.expand(d), rr))
    for r in rr: bad_t.append((lam, mu, r))
for tv in [sp.Rational(-5, 2), sp.Rational(7, 3)]:
    hits = [(l, mm) for l, mm, d in rows if sp.simplify(sp.expand(d).subs(t, tv)) == 0]
    print("     d_{lam mu}(%s) = 0 for : %s" % (tv, hits if hits else "none"))

# ================= [G3] does (Val) survive specialising t to a number? ========
print("\n[G3] (Val) at SPECIAL numeric t (Rick's sec 0 says val_s is taken in Q(t)(s),")
print("     so t is an indeterminate -- this probes how load-bearing that line is)")
for tv in [sp.Integer(-1), sp.Rational(-1, 2), sp.Rational(-1, 3)]:
    jumps = []
    for lam, mu, d in rows:
        if sp.simplify(sp.expand(d).subs(t, tv)) != 0: continue
        c = sp.cancel(cmat[lam].get(mu, 0))
        try:
            cs = sp.cancel(sp.together(c.subs(t, tv)))
        except Exception:
            jumps.append((list(lam), list(mu), "undefined")); continue
        if sp.simplify(cs) == 0: jumps.append((list(lam), list(mu), "c vanishes identically"))
        else:
            v = val_s(cs)
            jumps.append((list(lam), list(mu), "val_s = %s, n(mu) = %s" % (v, nstat(list(mu)))))
    print("     t = %-5s : %s" % (tv, jumps if jumps else "no d vanishes"))

# ================= [I] Op-DS (Rick: "Not checked separately by script") =======
print("\n[I] Op-DS: E_k e_mu -- support {rho |> mu u k} and lead s^{sum min(mu_i,k)}")
okI = {'supp': True, 'lead': True, 'full': True, 'pieri': True}
nI = 0
for n in range(0, NMAX):
    mus = parts(n) if n > 0 else [[]]
    for mu in mus:
        for k in range(1, m+1):
            if n+k > NMAX: continue
            src = e_lam_poly(mu) if mu else ONE
            out = apply_op(src, EK[k])
            cf = e_expand(out, n+k)
            uk = tuple(sorted(list(mu)+[k], reverse=True))
            nI += 1
            for rho, v in cf.items():
                if sp.simplify(v) == 0: continue
                if not dom_leq(list(uk), list(rho)):
                    okI['supp'] = False; print("    SUPPORT VIOLATION mu=%s k=%d rho=%s" % (mu, k, list(rho)))
            # full up-set: every rho |> mu u k must actually occur
            for rho in parts(n+k):
                if dom_leq(list(uk), list(rho)) and sp.simplify(cf.get(tuple(rho), 0)) == 0:
                    okI['full'] = False; print("    MISSING rho=%s (mu=%s k=%d)" % (list(rho), mu, k))
            want = s**sum(min(x, k) for x in mu)
            got = sp.cancel(cf.get(uk, 0))
            if sp.simplify(got-want) != 0:
                okI['lead'] = False
                print("    LEAD FAIL mu=%s k=%d: got %s want %s" % (mu, k, got, want))
print("    support {rho |> mu u k} : %s | support is the FULL up-set : %s" % (okI['supp'], okI['full']))
print("    lead coeff of e_{mu u k} = s^{sum_i min(mu_i,k)} : %s   [%d (mu,k) pairs]" % (okI['lead'], nI))
# the Pieri input: e_k P_nu has P_{nu+1^k} coefficient 1
for n in range(0, NMAX):
    for nu in (parts(n) if n > 0 else [[]]):
        for k in range(1, m+1):
            if n+k > NMAX: continue
            tgt = tuple([nu[i]+1 if i < len(nu) else 1 for i in range(k)] + list(nu[k:]))
            if list(tgt) != sorted(tgt, reverse=True): continue
            src = Ppoly[tuple(nu)] if nu else ONE
            cf = P_expand(mul(e_sym(k), src), n+k)
            if sp.simplify(cf.get(tgt, 0) - 1) != 0:
                okI['pieri'] = False
                print("    PIERI top coeff != 1: nu=%s k=%d got %s" % (nu, k, cf.get(tgt, 0)))
print("    Pieri input: [P_{nu+1^k}] (e_k P_nu) = 1 : %s" % okI['pieri'])

# ================= [J] NEGATIVE CONTROLS -- these must FIRE ==================
print("\n[J] negative controls (a check that cannot refuse is not a check)")
def ctrl(name, fn):
    f = 0; tot = 0
    for n in range(1, NMAX+1):
        for lam in parts(n):
            for mu in parts(n):
                c = sp.cancel(cmat[tuple(lam)].get(tuple(mu), 0))
                if sp.simplify(c) == 0: continue
                tot += 1
                if not fn(lam, mu, c): f += 1
    print("    %-52s refuses %d/%d  %s" % (name, f, tot, "FIRES" if f else "*** SILENT ***"))
    return f

def c21_with(evfn):
    def go(lam, mu, c):
        rhs = 0
        for nu in parts(sum(lam)):
            A = Amat[tuple(lam)].get(tuple(nu), 0); Bb = Bmat[tuple(nu)].get(tuple(mu), 0)
            if A == 0 or Bb == 0: continue
            rhs += A*evfn(nu)*Bb
        rhs = sp.cancel(t**(-nstat(conj(list(lam))))*rhs)
        return sp.simplify(sp.cancel(c-rhs)) == 0
    return go

ctrl("(2.1) with eigenvalue t^{n(nu')} s^{n(nu)} (swapped)",
     c21_with(lambda nu: t**nstat(conj(list(nu)))*s**nstat(list(nu))))
ctrl("(2.1) with eigenvalue t^{n(nu)} only (s dropped)",
     c21_with(lambda nu: t**nstat(list(nu))))
ctrl("(2.1) with eigenvalue s^{n(nu')} only (t dropped)",
     c21_with(lambda nu: s**nstat(conj(list(nu)))))
ctrl("(Val) with n(mu') in place of n(mu)",
     lambda lam, mu, c: val_s(c) == nstat(conj(list(mu))))
ctrl("(Val) with n(lam) in place of n(mu)",
     lambda lam, mu, c: val_s(c) == nstat(list(lam)))

def dform(use_tilde=True, conj_mu=True, twist=True):
    def go(lam, mu, c):
        d = sp.cancel(sp.expand(coeff_s(c, nstat(list(mu)))))
        idx = conj(list(mu)) if conj_mu else list(mu)
        lamp = conj(list(lam)); rhs = 0
        for rho in parts(sum(lam)):
            K2 = kostka(tuple(conj(list(rho))), tuple(lam))
            if K2 == 0: continue
            kk = Ktilde(rho, idx) if use_tilde else KF[tuple(rho)].get(tuple(idx), 0)
            if kk == 0: continue
            pw = t**(nstat(list(rho))-nstat(lamp)) if twist else 1
            rhs += pw*kk*sp.Integer(K2)
        return sp.simplify(sp.cancel(d-sp.cancel(rhs))) == 0
    return go
ctrl("d-formula with K (no cocharge twist) in place of Ktilde", dform(use_tilde=False))
ctrl("d-formula indexed by mu instead of mu'", dform(conj_mu=False))
ctrl("d-formula without the t^{n(rho)-n(lam')} prefactor", dform(twist=False))

# Op-DS lead controls
for nm, fn in [("s^{k*len(mu)}", lambda mu, k: s**(k*len(mu))),
               ("s^{n(mu u k)}", lambda mu, k: s**nstat(sorted(list(mu)+[k], reverse=True))),
               ("s^{sum max(mu_i,k)}", lambda mu, k: s**sum(max(x, k) for x in mu))]:
    f = tot = 0
    for n in range(0, NMAX):
        for mu in (parts(n) if n > 0 else [[]]):
            for k in range(1, m+1):
                if n+k > NMAX: continue
                src = e_lam_poly(mu) if mu else ONE
                cf = e_expand(apply_op(src, EK[k]), n+k)
                uk = tuple(sorted(list(mu)+[k], reverse=True))
                tot += 1
                if sp.simplify(sp.cancel(cf.get(uk, 0) - fn(mu, k))) != 0: f += 1
    print("    %-52s refuses %d/%d  %s" % ("Op-DS lead as "+nm, f, tot, "FIRES" if f else "*** SILENT ***"))
print("\ndone.")
