"""Polynomials in x_1..x_m over Q[s,t].  Coefficients: dict {(s_exp,t_exp): Fraction}.
Written for the 2026-10-11 peer review of Rick's long-version Theorem H / Cor 5.2.
Shares no code with Rick's scripts/day2* engines."""
from fractions import Fraction
from itertools import combinations

# ---- coefficient ring Q[s,t] ----
def cz(): return {}
def cc(v, se=0, te=0):
    v = Fraction(v)
    return {(se, te): v} if v else {}
def cadd(a, b):
    r = dict(a)
    for k, v in b.items():
        nv = r.get(k, Fraction(0)) + v
        if nv: r[k] = nv
        else: r.pop(k, None)
    return r
def cneg(a): return {k: -v for k, v in a.items()}
def cmul(a, b):
    r = {}
    for (s1, t1), v1 in a.items():
        for (s2, t2), v2 in b.items():
            k = (s1 + s2, t1 + t2)
            nv = r.get(k, Fraction(0)) + v1 * v2
            if nv: r[k] = nv
            else: r.pop(k, None)
    return r
def cshift_s(a, d): return {(se + d, te): v for (se, te), v in a.items()}

# ---- polynomial ring ----
def pz(): return {}
def padd(P, Q):
    R = dict(P)
    for a, c in Q.items():
        nc = cadd(R.get(a, {}), c)
        if nc: R[a] = nc
        else: R.pop(a, None)
    return R
def pneg(P): return {a: cneg(c) for a, c in P.items()}
def psub(P, Q): return padd(P, pneg(Q))
def pmul(P, Q):
    R = {}
    for a1, c1 in P.items():
        for a2, c2 in Q.items():
            a = tuple(i + j for i, j in zip(a1, a2))
            nc = cadd(R.get(a, {}), cmul(c1, c2))
            if nc: R[a] = nc
            else: R.pop(a, None)
    return R
def pone(m): return {tuple([0]*m): cc(1)}
def pvar(i, m, coeff=None):
    a = [0]*m; a[i] = 1
    return {tuple(a): (coeff if coeff is not None else cc(1))}
def pzero_q(P): return all(not c for c in P.values())

def cdiv_exact(a, b):
    """exact division in Q[s,t]; lex-leading-term cancellation"""
    a = {k: v for k, v in a.items() if v}
    b = {k: v for k, v in b.items() if v}
    if not b: raise ZeroDivisionError
    out = {}
    while a:
        ae = max(a); be = max(b)
        k = (ae[0]-be[0], ae[1]-be[1])
        if k[0] < 0 or k[1] < 0: raise ArithmeticError("coeff not divisible %s/%s" % (ae, be))
        v = a[ae] / b[be]
        out[k] = out.get(k, Fraction(0)) + v
        a = {kk: vv for kk, vv in cadd(a, cneg(cmul({k: v}, b))).items() if vv}
    return {k: v for k, v in out.items() if v}

def pdiv_exact(P, D):
    if pzero_q(P): return {}
    Dl = max(D.keys()); Dc = D[Dl]
    R = {a: dict(c) for a, c in P.items() if c}
    out = {}
    while R:
        Rl = max(R); Rc = R[Rl]
        q = tuple(i - j for i, j in zip(Rl, Dl))
        if any(e < 0 for e in q): raise ArithmeticError("not divisible (exponent)")
        term = {q: cdiv_exact(Rc, Dc)}
        out = padd(out, term)
        R = {a: c for a, c in psub(R, pmul(term, D)).items() if c}
    return out

def vandermonde(m):
    V = pone(m)
    for i in range(m):
        for j in range(i+1, m):
            V = pmul(V, psub(pvar(i, m), pvar(j, m)))
    return V

# ---- the printed subset formula:  E_k F = sum_{|A|=k} c_A x_A F|_{x_i -> s x_i, i in A}
def E_k(F, k, m, V=None):
    if k > m: return {}
    if V is None: V = vandermonde(m)
    total = pz()
    for A in combinations(range(m), k):
        As = set(A)
        num = pone(m)
        for i in A:
            for j in range(m):
                if j in As: continue
                num = pmul(num, padd(pvar(i, m), pvar(j, m, cc(-1, 0, 1))))   # x_i - t x_j
        sign = 1; cof = pone(m)
        for i in range(m):
            for j in range(i+1, m):
                ini, inj = i in As, j in As
                if ini and not inj: pass            # (x_i-x_j) consumed by denominator
                elif inj and not ini: sign = -sign  # denominator has (x_j-x_i)
                else: cof = pmul(cof, psub(pvar(i, m), pvar(j, m)))
        xA = pone(m)
        for i in A: xA = pmul(xA, pvar(i, m))
        # F with x_i -> s x_i for i in A
        FA = {}
        for al, c in F.items():
            d = sum(al[i] for i in A)
            FA[al] = cshift_s(c, d)
        term = pmul(pmul(num, cof), pmul(xA, FA))
        if sign < 0: term = pneg(term)
        total = padd(total, term)
    if pzero_q(total): return {}
    return pdiv_exact(total, V)

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n-k, k):
            yield (k,) + rest

def conj(lam):
    if not lam: return ()
    return tuple(sum(1 for p in lam if p > j) for j in range(lam[0]))

def nstat(lam): return sum(i*p for i, p in enumerate(lam))
