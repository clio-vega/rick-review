"""ENGINE B: Hall-Littlewood P_lambda(x;u) built directly from the symmetrised
Macdonald III (2.2) sum, with the normalisation FIXED EMPIRICALLY by [m_lambda]P=1
(so no reliance on my memory of v_lambda(t)).  Then e_lambda -> P-basis.
Coefficients are dicts {u_exponent: Fraction}; u_exponent may be negative
(we substitute u = t^{-1} at the end)."""
from fractions import Fraction
from itertools import permutations
from ring import partitions, conj, nstat

def az(): return {}
def ac(v, e=0):
    v = Fraction(v); return {e: v} if v else {}
def aadd(a, b):
    r = dict(a)
    for k, v in b.items():
        nv = r.get(k, Fraction(0)) + v
        if nv: r[k] = nv
        else: r.pop(k, None)
    return r
def aneg(a): return {k: -v for k, v in a.items()}
def amul(a, b):
    r = {}
    for e1, v1 in a.items():
        for e2, v2 in b.items():
            e = e1+e2; nv = r.get(e, Fraction(0)) + v1*v2
            if nv: r[e] = nv
            else: r.pop(e, None)
    return r
def adiv(a, b):
    """exact division in Q[u,u^-1]"""
    a = {k: v for k, v in a.items() if v}; b = {k: v for k, v in b.items() if v}
    out = {}
    while a:
        ae = max(a); be = max(b); e = ae-be
        v = a[ae]/b[be]
        out[e] = out.get(e, Fraction(0)) + v
        a = {k: vv for k, vv in aadd(a, aneg(amul({e: v}, b))).items() if vv}
    return {k: v for k, v in out.items() if v}
def ainv_u(a):
    """substitute u -> u^{-1}"""
    return {-k: v for k, v in a.items()}

# polynomials in x over Q[u,u^-1]
def Pz(): return {}
def Padd(P, Q):
    R = dict(P)
    for k, c in Q.items():
        nc = aadd(R.get(k, {}), c)
        if nc: R[k] = nc
        else: R.pop(k, None)
    return R
def Pmul(P, Q):
    R = {}
    for a1, c1 in P.items():
        for a2, c2 in Q.items():
            k = tuple(i+j for i, j in zip(a1, a2))
            nc = aadd(R.get(k, {}), amul(c1, c2))
            if nc: R[k] = nc
            else: R.pop(k, None)
    return R
def Pone(m): return {tuple([0]*m): ac(1)}
def Pvar(i, m, c=None):
    a = [0]*m; a[i] = 1
    return {tuple(a): (c if c is not None else ac(1))}
def Psub(P, Q): return Padd(P, {k: aneg(c) for k, c in Q.items()})
def Pdiv(P, D):
    if not P: return {}
    Dl = max(D); Dc = D[Dl]
    R = {a: dict(c) for a, c in P.items() if c}; out = {}
    while R:
        Rl = max(R); Rc = R[Rl]
        q = tuple(i-j for i, j in zip(Rl, Dl))
        if any(e < 0 for e in q): raise ArithmeticError("not divisible")
        term = {q: adiv(Rc, Dc)}
        out = Padd(out, term)
        R = {a: c for a, c in Psub(R, Pmul(term, D)).items() if c}
    return out

def vander(m):
    V = Pone(m)
    for i in range(m):
        for j in range(i+1, m):
            V = Pmul(V, Psub(Pvar(i, m), Pvar(j, m)))
    return V

def sign(perm):
    p = list(perm); s = 1
    for i in range(len(p)):
        for j in range(i+1, len(p)):
            if p[i] > p[j]: s = -s
    return s

_num_cache = {}
def _numerator(m):
    """prod_{i<j} (x_i - u x_j)"""
    if m in _num_cache: return _num_cache[m]
    N = Pone(m)
    for i in range(m):
        for j in range(i+1, m):
            N = Pmul(N, Padd(Pvar(i, m), Pvar(j, m, ac(-1, 1))))
    _num_cache[m] = N
    return N

def P_HL(lam, m):
    """P_lambda(x_1..x_m; u), normalised so [x^lambda] = 1."""
    lp = tuple(list(lam) + [0]*(m-len(lam)))
    assert len(lp) == m
    Num = _numerator(m); V = vander(m)
    # sum_{w in S_m} eps(w) w( x^lam * prod_{i<j}(x_i - u x_j) )  /  V
    acc = Pz()
    for perm in permutations(range(m)):
        eps = sign(perm)
        # w: x_i -> x_{perm[i]}
        shifted = {}
        for a, c in Num.items():
            b = [0]*m
            for i in range(m): b[perm[i]] = a[i]
            shifted[tuple(b)] = aadd(shifted.get(tuple(b), {}), c)
        lamb = [0]*m
        for i in range(m): lamb[perm[i]] = lp[i]
        term = Pmul({tuple(lamb): ac(eps)}, shifted)
        acc = Padd(acc, term)
    raw = Pdiv(acc, V)
    lead = raw.get(tuple(lp))
    assert lead, "no x^lambda term in raw sum for %s" % (lam,)
    return {a: adiv(c, lead) for a, c in raw.items()}

def dominates(mu, lam):
    if sum(mu) != sum(lam): return False
    a = b = 0
    for i in range(max(len(mu), len(lam))):
        a += mu[i] if i < len(mu) else 0
        b += lam[i] if i < len(lam) else 0
        if a < b: return False
    return True

def e_in_P(n, m):
    """returns dict  (lam, kappa) -> coeff in Q[u,u^-1]  of  e_lam = sum_kappa C[lam,kappa] P_kappa(x;u)"""
    parts = list(partitions(n))
    Ps = {k: P_HL(k, m) for k in parts}
    # e_lam monomial expansion
    def e_poly(lam):
        from itertools import combinations
        R = Pone(m)
        for k in lam:
            E = Pz()
            for A in combinations(range(m), k):
                a = [0]*m
                for i in A: a[i] = 1
                E[tuple(a)] = ac(1)
            R = Pmul(R, E)
        return R
    # order partitions so that larger in dominance comes first
    order = sorted(parts, key=lambda p: nstat(p))   # ascending n(p) = descending dominance (linear extension)
    out = {}
    for lam in parts:
        cur = e_poly(lam)
        for kap in order:
            key = tuple(list(kap) + [0]*(m-len(kap)))
            c = cur.get(key, {})
            if c:
                out[(lam, kap)] = c
                # subtract c * P_kap
                cur = Psub(cur, {a: amul(c, cc) for a, cc in Ps[kap].items()})
        leftover = {a: c for a, c in cur.items() if c}
        assert not leftover, "e_%s did not reduce to 0 in P-basis: %d terms left" % (lam, len(leftover))
    return out, Ps
