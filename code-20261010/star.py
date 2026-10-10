"""
Independent re-implementation of Hikita's star-product operators E_k and their
(s-1)-Taylor pieces E_k^{(p)}, from the PRINTED subset formula of
Rick's FPSAC draft (work-in-progress @ e44e29f), Proposition 2.1 and eq. (2.1).

Nothing here is imported from Rick's scripts.  The only inputs are the two
printed displays:

  Prop 2.1   e_k * F = E_k F = sum_{|A|=k} c_A X_A F(X_{A^c}, s X_A),
             c_A = prod_{i in A, j notin A} (x_i - t x_j)/(x_i - x_j),
             X_A = prod_{i in A} x_i.

  eq (2.1)   E_k = sum_{p>=0} (s-1)^p E_k^{(p)},
             E_k^{(p)} = sum_{|A|=k} c_A X_A binom(Delta_A, p),
             Delta_A = sum_{i in A} x_i d/dx_i.

Representation: a polynomial in x_1..x_N over Q[t] is a dict
    {alpha (tuple of N ints) : {t_exponent : Fraction}}.
"""
from fractions import Fraction
from itertools import combinations
from math import comb

# ---------- coefficient ring Q[t]  (or Q, when t is specialised) ----------
TVAL = None   # None -> t stays symbolic; a Fraction -> t is specialised (fast mode)
def set_t(v):
    """Specialise t to a rational.  Coefficient dicts then only ever use key 0,
    which makes c_mul O(1) and the whole computation ~100x faster."""
    global TVAL
    TVAL = None if v is None else Fraction(v)
def minus_t_coeff():
    """the coefficient '-t' used in the factor (x_i - t x_j) of c_A"""
    if TVAL is None: return {1: Fraction(-1)}
    return ({0: -TVAL} if TVAL != 0 else {})

def c_zero(): return {}
def c_const(v): return {0: Fraction(v)} if v else {}
def c_add(a, b):
    r = dict(a)
    for e, v in b.items():
        nv = r.get(e, Fraction(0)) + v
        if nv: r[e] = nv
        else: r.pop(e, None)
    return r
def c_neg(a): return {e: -v for e, v in a.items()}
def c_mul(a, b):
    r = {}
    for e1, v1 in a.items():
        for e2, v2 in b.items():
            e = e1 + e2
            nv = r.get(e, Fraction(0)) + v1 * v2
            if nv: r[e] = nv
            else: r.pop(e, None)
    return r
def c_scal(a, k):
    k = Fraction(k)
    if k == 0: return {}
    return {e: v * k for e, v in a.items()}

# ---------- polynomial ring Q[t][x_1..x_N] ----------
def p_zero(): return {}
def p_add(P, Q):
    R = dict(P)
    for a, c in Q.items():
        nc = c_add(R.get(a, {}), c)
        if nc: R[a] = nc
        else: R.pop(a, None)
    return R
def p_neg(P): return {a: c_neg(c) for a, c in P.items()}
def p_sub(P, Q): return p_add(P, p_neg(Q))
def p_mul(P, Q):
    R = {}
    for a1, c1 in P.items():
        for a2, c2 in Q.items():
            a = tuple(i + j for i, j in zip(a1, a2))
            nc = c_add(R.get(a, {}), c_mul(c1, c2))
            if nc: R[a] = nc
            else: R.pop(a, None)
    return R
def p_scal(P, k):
    R = {}
    for a, c in P.items():
        nc = c_scal(c, k)
        if nc: R[a] = nc
    return R
def p_one(N): return {tuple([0]*N): c_const(1)}
def p_var(i, N, coeff=None):
    a = [0]*N; a[i] = 1
    return {tuple(a): (coeff if coeff is not None else c_const(1))}
def p_is_zero(P): return all(not c for c in P.values())

def p_divide_exact(P, D):
    """Exact division P/D in Q[t][x]; raises if not exact.  Multivariate
    division by repeatedly cancelling the lex-leading term of D."""
    def lead(Q):
        return max(Q.keys())
    if p_is_zero(P): return {}
    Dl = lead(D); Dc = D[Dl]
    # Dc must be invertible in Q[t] -> require it to be a nonzero constant times t^e
    R = {a: dict(c) for a, c in P.items() if c}
    out = {}
    while R:
        Rl = lead(R); Rc = R[Rl]
        q_exp = tuple(i - j for i, j in zip(Rl, Dl))
        if any(e < 0 for e in q_exp):
            raise ArithmeticError("not divisible (exponent)")
        qc = c_divide_exact(Rc, Dc)
        term = {q_exp: qc}
        out = p_add(out, term)
        R = {a: c for a, c in p_sub(R, p_mul(term, D)).items() if c}
    return out

def c_divide_exact(a, b):
    """divide in Q[t], require exact"""
    a = {e: v for e, v in a.items() if v}
    b = {e: v for e, v in b.items() if v}
    out = {}
    while a:
        ae = max(a); be = max(b)
        e = ae - be
        if e < 0: raise ArithmeticError("not divisible (t-degree)")
        v = a[ae] / b[be]
        out[e] = out.get(e, Fraction(0)) + v
        sub = {be2 + e: v * bv for be2, bv in b.items()}
        a = {k: av for k, av in c_add(a, c_neg(sub)).items() if av}
    return {e: v for e, v in out.items() if v}

# ---------- Vandermonde ----------
def vandermonde(N):
    V = p_one(N)
    for i in range(N):
        for j in range(i+1, N):
            V = p_mul(V, p_sub(p_var(i, N), p_var(j, N)))
    return V

# ---------- the operator E_k^{(p)} ----------
def E_k_p(F, k, p, N, V=None):
    """E_k^{(p)} F, from (2.1).  F is a poly dict in N vars."""
    if V is None: V = vandermonde(N)
    total = p_zero()
    for A in combinations(range(N), k):
        As = set(A)
        # numerator of c_A : prod_{i in A, j notin A} (x_i - t x_j)
        num = p_one(N)
        for i in A:
            for j in range(N):
                if j in As: continue
                num = p_mul(num, p_add(p_var(i, N), p_var(j, N, minus_t_coeff())))  # x_i - t*x_j
        # V / D_A  where D_A = prod_{i in A, j notin A}(x_i - x_j)
        sign = 1
        cof = p_one(N)
        for i in range(N):
            for j in range(i+1, N):
                ini, inj = i in As, j in As
                if ini and not inj:
                    pass                       # factor (x_i-x_j) consumed by D_A
                elif inj and not ini:
                    sign = -sign               # D_A has (x_j-x_i) = -(x_i-x_j)
                else:
                    cof = p_mul(cof, p_sub(p_var(i, N), p_var(j, N)))
        # X_A * binom(Delta_A, p) F
        XA = p_one(N)
        for i in A: XA = p_mul(XA, p_var(i, N))
        FA = {}
        for alpha, c in F.items():
            w = sum(alpha[i] for i in A)
            b = comb(w, p) if w >= p else 0
            if b:
                nc = c_scal(c, b)
                if nc: FA[alpha] = c_add(FA.get(alpha, {}), nc)
        if not FA: continue
        term = p_mul(p_mul(num, cof), p_mul(XA, FA))
        if sign < 0: term = p_neg(term)
        total = p_add(total, term)
    if p_is_zero(total): return {}
    return p_divide_exact(total, V)
