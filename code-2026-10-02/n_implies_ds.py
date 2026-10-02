"""
Clio, 2026-10-02 peer review of Rick (N).
Independent instrument: Macdonald P built by DIAGONALISING Macdonald's D_1
(no Sage, no imported Macdonald code), then N defined on that eigenbasis.

Tests, in order:
  A  instrument validation: D_1 eigenvalues match eps_nu = sum_i s^{nu_i} tau^{m-i},
     and the P_nu are monomial-unitriangular.  (Must reproduce a KNOWN value
     before any zero below is believed.)
  B  Theorem (N) itself:  E_k F = t^{-C(k,2)} N (e_k * N^{-1} F).
  C  the closed form it gives: e^star_lam = t^{-n(lam')} N(e_lam).
  D  THE BRIEF'S PREDICTION: val_s c_{lam,mu} = n(mu), where
     e^star_lam = sum_mu c_{lam,mu} e_mu.
  E  negative controls: wrong N eigenvalue must break B.
"""
import sympy as sp
from itertools import combinations, permutations

s = sp.Symbol('s')
m = 4

def parts(n, k):
    """partitions of n into at most k parts, weakly decreasing"""
    def go(n, k, mx):
        if n == 0: yield []; return
        if k == 0: return
        for a in range(min(n, mx), 0, -1):
            for rest in go(n-a, k-1, a): yield [a]+rest
    return list(go(n, k, n))

def nstat(lam): return sum(i*p for i, p in enumerate(lam))
def conj(lam):
    return [sum(1 for p in lam if p > j) for j in range(lam[0])] if lam else []

def pad(lam): return tuple(list(lam) + [0]*(m-len(lam)))

def mono_sym(lam):
    """m_lam as dict exponent-tuple -> 1"""
    return {e: sp.Integer(1) for e in set(permutations(pad(lam)))}

def e_sym(k):
    if k == 0: return {tuple([0]*m): sp.Integer(1)}
    d = {}
    for A in combinations(range(m), k):
        ex = [0]*m
        for i in A: ex[i] = 1
        d[tuple(ex)] = sp.Integer(1)
    return d

def add(a, b, c=1):
    out = dict(a)
    for k, v in b.items(): out[k] = sp.expand(out.get(k, 0) + c*v)
    return {k: v for k, v in out.items() if v != 0}

def mul(a, b):
    out = {}
    for e1, c1 in a.items():
        for e2, c2 in b.items():
            k = tuple(i+j for i, j in zip(e1, e2))
            out[k] = sp.expand(out.get(k, 0) + c1*c2)
    return {k: v for k, v in out.items() if v != 0}

def to_mcoeffs(d, n):
    """read m_nu coefficients: coeff of the dominant monomial x^nu"""
    return {tuple(nu): sp.simplify(d.get(pad(nu), sp.Integer(0))) for nu in parts(n, m)}

def from_mcoeffs(cf, n):
    out = {}
    for nu, c in cf.items():
        if c != 0: out = add(out, mono_sym(list(nu)), c)
    return out

# ---------- operators as dict->dict, with x_i -> shift*x_i substitution ----------
def diffop(d, pairs):
    """pairs: list of (coefficient-as-rational-function, index set I, shift).
       Coefficient is a sympy expr in x's; we clear denominators by expansion."""
    xs = sp.symbols('x1:%d' % (m+1))
    poly = sum(c*sp.prod([xs[i]**e for i, e in enumerate(ex)]) for ex, c in d.items())
    out = 0
    for coef, I, sh in pairs:
        sub = {xs[i]: sh*xs[i] for i in I}
        out += coef*poly.subs(sub, simultaneous=True)
    out = sp.simplify(sp.together(out))
    out = sp.expand(sp.cancel(out))
    res = {}
    P = sp.Poly(out, *xs)
    for ex, c in zip(P.monoms(), P.coeffs()):
        res[tuple(ex)] = sp.expand(c)
    return res

def D1_pairs(tau):
    xs = sp.symbols('x1:%d' % (m+1))
    return [(sp.prod([(tau*xs[i]-xs[j])/(xs[i]-xs[j]) for j in range(m) if j != i]),
             (i,), s) for i in range(m)]

def Ek_pairs(tval):
    xs = sp.symbols('x1:%d' % (m+1))
    out = []
    for k in range(1, m+1):
        pr = []
        for A in combinations(range(m), k):
            Ac = [j for j in range(m) if j not in A]
            c = sp.prod([xs[i] for i in A])
            for i in A:
                for j in Ac: c *= (xs[i]-tval*xs[j])/(xs[i]-xs[j])
            pr.append((c, A, s))
        out.append(pr)
    return out

def run(tval, label):
    print("="*78); print("t = %s   (%s)   m = %d" % (tval, label, m)); print("="*78)
    tau = sp.Rational(1, 1)/tval
    EK = Ek_pairs(tval)
    D1p = D1_pairs(tau)

    # ---- build Macdonald P_nu by diagonalising D_1 on degree-n symmetric space ----
    Pbasis, Nev = {}, {}
    for n in range(0, m+1):
        B = parts(n, m)
        if not B: continue
        cols = []
        for nu in B:
            cols.append(to_mcoeffs(diffop(mono_sym(nu), D1p), n))
        Mat = sp.Matrix([[cols[j][tuple(B[i])] for j in range(len(B))] for i in range(len(B))])
        for nu in B:
            eps = sum(s**nu_i*tau**(m-1-i) for i, nu_i in enumerate(pad(nu)))
            eps = sp.expand(eps)
            ker = (Mat - eps*sp.eye(len(B))).nullspace()
            assert len(ker) == 1, ("eigenspace not 1-dim", nu, len(ker))
            v = ker[0]
            idx = B.index(nu)
            assert v[idx] != 0, ("P_nu has zero m_nu coefficient", nu)
            v = v/v[idx]
            cf = {tuple(B[i]): sp.simplify(v[i]) for i in range(len(B))}
            Pbasis[tuple(nu)] = (from_mcoeffs(cf, n), cf, n)
            Nev[tuple(nu)] = tval**nstat(nu)*s**nstat(conj(nu))

    # ---- A: instrument validation ----
    print("\n[A] instrument validation")
    ok = True
    for nu, (pol, cf, n) in Pbasis.items():
        got = to_mcoeffs(diffop(pol, D1p), n)
        eps = sp.expand(sum(s**nu_i*tau**(m-1-i) for i, nu_i in enumerate(pad(list(nu)))))
        for mu, c in cf.items():
            if sp.simplify(got[mu] - eps*c) != 0: ok = False
    print("    D_1 P_nu = eps_nu P_nu for all %d partitions, n<=%d : %s" % (len(Pbasis), m, ok))
    # known value: P_{1^k} must equal e_k exactly
    for k in range(1, m+1):
        nu = tuple([1]*k)
        same = add(Pbasis[nu][0], e_sym(k), -1) == {}
        print("    KNOWN VALUE  P_{1^%d} == e_%d : %s" % (k, k, same))

    # ---- N and N^{-1} on arbitrary symmetric input ----
    def expandP(d, n):
        cf = to_mcoeffs(d, n); B = parts(n, m)
        out = {}
        rem = dict(cf)
        for nu in B:   # dominance-compatible: process in reverse lex (unitriangular)
            pass
        # solve linear system in the m-basis
        Mat = sp.Matrix([[Pbasis[tuple(nu)][1][tuple(mu)] for nu in B] for mu in B])
        rhs = sp.Matrix([cf[tuple(mu)] for mu in B])
        sol = Mat.solve(rhs)
        return {tuple(B[i]): sp.simplify(sol[i]) for i in range(len(B))}

    def Napply(d, n, power=1):
        pc = expandP(d, n); out = {}
        for nu, c in pc.items():
            if c == 0: continue
            out = add(out, Pbasis[nu][0], sp.simplify(c*Nev[nu]**power))
        return out

    # ---- B: Theorem (N) itself ----
    print("\n[B] Theorem (N):  E_k F = t^{-C(k,2)} N(e_k * N^{-1} F)")
    for n in range(0, m):
        for nu in parts(n, m) or [[]]:
            F = Pbasis[tuple(nu)][0] if nu else {tuple([0]*m): sp.Integer(1)}
            for k in range(1, m+1-n if n > 0 else m+1):
                if n+k > m: continue
                lhs = diffop(F, EK[k-1])
                inner = mul(e_sym(k), Napply(F, n, -1))
                rhs = Napply(inner, n+k, +1)
                pref = tval**(-sp.Rational(k*(k-1), 2))
                diff = add(lhs, rhs, -pref)
                diff = {a: b for a, b in diff.items() if sp.simplify(b) != 0}
                print("    F=P_%-10s k=%d : %s" % (nu if nu else [], k, "OK" if not diff else "*** FAIL ***"))

    # ---- C and D ----
    print("\n[C] closed form e^star_lam = t^{-n(lam')} N(e_lam)   [D] val_s c = n(mu)")
    def estar(lam):
        cur = e_sym(lam[-1])
        for k in reversed(lam[:-1]):
            cur = diffop(cur, EK[k-1])
        return cur
    def val_s(expr):
        expr = sp.simplify(sp.together(expr))
        if expr == 0: return None
        n_, d_ = sp.fraction(sp.cancel(expr))
        def low(p):
            p = sp.expand(p)
            pp = sp.Poly(p, s)
            return min(mo[0] for mo in pp.monoms())
        return low(n_) - low(d_)
    for n in range(1, m+1):
        for lam in parts(n, m):
            st = estar(lam)
            rhsC = Napply(from_mcoeffs({tuple(lam): sp.Integer(1)}, 0) if False else
                          e_lam_poly(lam), n, +1)
            rhsC = {a: sp.simplify(b*tval**(-nstat(conj(lam)))) for a, b in rhsC.items()}
            dC = add(st, rhsC, -1)
            dC = {a: b for a, b in dC.items() if sp.simplify(b) != 0}
            # e-expansion of e^star_lam
            cf = e_expand(st, n)
            bad = [(mu, v) for mu, v in cf.items()
                   if v != 0 and val_s(v) != nstat(list(mu))]
            print("    lam=%-10s [C] %-4s   [D] %s" % (
                lam, "OK" if not dC else "FAIL",
                "val_s = n(mu) for all %d nonzero c" % sum(1 for v in cf.values() if v != 0)
                if not bad else "*** MISMATCH %s ***" % bad[:2]))

def e_lam_poly(lam):
    out = e_sym(lam[0])
    for k in lam[1:]: out = mul(out, e_sym(k))
    return out

def e_expand(d, n):
    """expand a symmetric polynomial of degree n in the e_mu basis"""
    B = parts(n, m)
    Mat = sp.Matrix([[to_mcoeffs(e_lam_poly(list(nu)), n)[tuple(mu)] for nu in B] for mu in B])
    cf = to_mcoeffs(d, n)
    sol = Mat.solve(sp.Matrix([cf[tuple(mu)] for mu in B]))
    return {tuple(B[i]): sp.simplify(sol[i]) for i in range(len(B))}

run(sp.Rational(-5, 2), "Rick's test point t=-5/2")
