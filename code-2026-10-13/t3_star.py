"""
TEST 3: the star product itself.

TWO INDEPENDENT IMPLEMENTATIONS, no shared code path:

  M1  Clio's engine (written 2026-09-16/18 for a different review) built
      DIRECTLY from Hikita arXiv:2503.23597 source qt-CSF.tex:
        Def 3.4 (Def_qm), Lem 3.3 (Lem_iota_elem), Y_i = t^{m-i}T_{i-1}..T_1 Pi T_{m-1}^{-1}..T_i^{-1},
        T_i^{+-1} by the monomial formula of Lem 2.x (Lem_AHA_action).
      e_a * F = t^{-C(a,2)} e_a(Y) . F.  Pure Laurent-polynomial arithmetic, no x-division.
      Hikita's q;  Rick's s = q^{-1}.

  M2  Rick's subset formula, thm:subset (longversion.tex l.198):
        E_k F = sum_{|A|=k} c_A x_A F|_{x_i -> s x_i (i in A)},
        c_A = prod_{i in A, j notin A} (x_i - t x_j)/(x_i - x_j).
      Evaluated at generic rational x-points and solved back into the e-basis.
      Uses division by (x_i-x_j) -- a different arithmetic route entirely.

EXTERNAL PRINTED GROUND TRUTH (not Rick's, not mine):
  G1  Hikita Thm 3.12 (= Thm_qtPieri_en, verbatim from source, line 883):
        e_1(X) * e_r(X) = (1-q^{-1})[r+1]_t e_{r+1}(X) + q^{-1} e_1(X) e_r(X)
  G2  Hikita Lemma 6.3 (= Lem_qtelem_limit, line 1420):
        lim_{q->oo} e^{(q,t)}_lambda = ([n]_t!/prod_i [lambda_i]_t!) e_n,
      with e^{(q,t)}_lambda := e_{lambda_1} * ... * e_{lambda_l} (line 271).
"""
from itertools import combinations
from sympy.polys.fields import field
from sympy.polys.domains import QQ
from fractions import Fraction

FF, s, t = field("s,t", QQ)
ONE, ZERO = FF.one, FF.zero

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
def qint(n): return sum(t**i for i in range(n))
def qfact(n):
    r = ONE
    for i in range(1, n+1): r *= qint(i)
    return r

# ===================== M1 : Clio's Y-operator engine =====================
# q = 1/s   (Hikita's q;  Rick's s = q^{-1})
Q = ONE/s

def _add(A, B):
    C = dict(A)
    for e, c in B.items():
        v = C.get(e, ZERO) + c
        if v: C[e] = v
        elif e in C: del C[e]
    return C
def _scal(c, A): return {} if not c else {e: c*v for e, v in A.items()}

def T_(i, A, m):
    out = {}
    for e, c in A.items():
        k, l = e[i-1], e[i]; base = list(e)
        def mono(x, y, coef):
            b = list(base); b[i-1] = x; b[i] = y; b = tuple(b)
            v = out.get(b, ZERO) + coef
            if v: out[b] = v
            elif b in out: del out[b]
        if l >= k:
            mono(l, k, t*c)
            for j in range(l-k): mono(l-1-j, k+1+j, (t-ONE)*c)
        else:
            mono(l, k, c)
            for j in range(k-l-1): mono(l+1+j, k-1-j, -(t-ONE)*c)
    return out

def Tinv_(i, A, m):
    out = {}; tinv = ONE/t
    for e, c in A.items():
        k, l = e[i-1], e[i]; base = list(e)
        def mono(x, y, coef):
            b = list(base); b[i-1] = x; b[i] = y; b = tuple(b)
            v = out.get(b, ZERO) + coef
            if v: out[b] = v
            elif b in out: del out[b]
        if l > k:
            mono(l, k, c)
            for j in range(l-k-1): mono(l-1-j, k+1+j, (ONE-tinv)*c)
        else:
            mono(l, k, tinv*c)
            for j in range(k-l): mono(l+1+j, k-1-j, -(ONE-tinv)*c)
    return out

def Pi_(A, m):
    out = {}
    for e, c in A.items():
        b = [0]*m; b[0] = e[m-1]+1
        for j in range(m-1): b[j+1] = e[j]
        b = tuple(b); coef = c*(ONE/Q)**e[m-1]
        v = out.get(b, ZERO) + coef
        if v: out[b] = v
        elif b in out: del out[b]
    return out

def Y_(i, A, m):
    B = A
    for j in range(i, m): B = Tinv_(j, B, m)
    B = Pi_(B, m)
    for j in range(1, i): B = T_(j, B, m)
    return _scal(t**(m-i), B)

def eY(a, A, m):
    total = {}
    for S in combinations(range(1, m+1), a):
        B = A
        for i in S: B = Y_(i, B, m)
        total = _add(total, B)
    return total

def e_poly(r, m):
    out = {}
    for S in combinations(range(m), r):
        b = [0]*m
        for i in S: b[i] = ONE and 1
        out[tuple(b)] = ONE
    return out
def mul_poly(A, B):
    out = {}
    for e1, c1 in A.items():
        for e2, c2 in B.items():
            b = tuple(x+y for x, y in zip(e1, e2))
            v = out.get(b, ZERO) + c1*c2
            if v: out[b] = v
            elif b in out: del out[b]
    return out
def e_lambda_poly(lam, m):
    out = {tuple([0]*m): ONE}
    for p in lam: out = mul_poly(out, e_poly(p, m))
    return out

def expand_in_e(A, n, m):
    lams = [l for l in partitions(n) if l[0] <= m]
    basis = [e_lambda_poly(l, m) for l in lams]
    lead = []
    for l in lams:
        c = conj(l); lead.append(tuple(list(c)+[0]*(m-len(c))))
    order = sorted(range(len(lams)), key=lambda i: lead[i], reverse=True)
    R = dict(A); co = {}
    for i in order:
        cf = R.get(lead[i], ZERO)
        if cf:
            co[lams[i]] = cf
            R = _add(R, _scal(-cf, basis[i]))
    assert not R, "M1 residual nonzero (%d monomials)" % len(R)
    return co

def star_lambda_M1(lam, m=None):
    """e^star_lambda in the e-basis, by iterating e_a * F = t^{-C(a,2)} e_a(Y) F."""
    n = sum(lam)
    if m is None: m = n
    assert m >= n
    A = {tuple([0]*m): ONE}
    for a in reversed(lam):
        A = eY(a, A, m)
        A = _scal((ONE/t)**(a*(a-1)//2), A)
    return expand_in_e(A, n, m)

# ===================== M2 : Rick's subset formula =====================
def _efun(r, xs):
    """e_r of a list of FF elements."""
    out = ZERO
    for S in combinations(range(len(xs)), r):
        p = ONE
        for i in S: p *= xs[i]
        out += p
    return out

def _eval_e_expansion(co, xs):
    tot = ZERO
    for nu, c in co.items():
        p = c
        for r in nu: p *= _efun(r, xs)
        tot += p
    return tot

def _solve(M, rhs):
    """exact Gaussian elimination, M over QQ (as FF scalars), rhs over FF."""
    nn = len(M)
    A = [list(M[i]) + [rhs[i]] for i in range(nn)]
    for c in range(nn):
        piv = None
        for r in range(c, nn):
            if A[r][c] != ZERO: piv = r; break
        if piv is None: return None
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [v/pv for v in A[c]]
        for r in range(nn):
            if r != c and A[r][c] != ZERO:
                f = A[r][c]
                A[r] = [a-f*b for a, b in zip(A[r], A[c])]
    return [A[i][nn] for i in range(nn)]

_PTS = {}
def _points(m, npts):
    key = (m, npts)
    if key in _PTS: return _PTS[key]
    import random
    rng = random.Random(20261013)
    pts = []
    seen = set()
    while len(pts) < npts:
        v = tuple(sorted(rng.sample(range(1, 60), m)))
        if v in seen: continue
        seen.add(v); pts.append([FF.one*a for a in v])
    _PTS[key] = pts
    return pts

def E_k_M2(co, k, deg, m):
    """co: e-expansion of F (degree deg).  Returns e-expansion of E_k F (degree deg+k)."""
    d = deg + k
    lams = [l for l in partitions(d) if l[0] <= m]
    pts = _points(m, len(lams))
    M = [[_efun2(l, p) for l in lams] for p in pts]
    rhs = []
    for p in pts:
        tot = ZERO
        for A in combinations(range(m), k):
            Aset = set(A)
            cA = ONE
            for i in A:
                for j in range(m):
                    if j not in Aset:
                        cA *= (p[i]-t*p[j])/(p[i]-p[j])
            xA = ONE
            for i in A: xA *= p[i]
            ys = [s*p[i] if i in Aset else p[i] for i in range(m)]
            tot += cA*xA*_eval_e_expansion(co, ys)
        rhs.append(tot)
    sol = _solve(M, rhs)
    assert sol is not None, "singular interpolation matrix"
    return {l: v for l, v in zip(lams, sol) if v}

def _efun2(lam, xs):
    p = ONE
    for r in lam: p *= _efun(r, xs)
    return p

def star_lambda_M2(lam, m=None):
    n = sum(lam)
    if m is None: m = n
    co = {(): ONE}; deg = 0
    for a in reversed(lam):
        co = E_k_M2(co, a, deg, m); deg += a
    return co
