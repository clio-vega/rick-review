"""
Independent verification of Rick's PROVE 241/242 (seed-q1-braided-terminal).
Built from the DEFINITIONS in his sec.0, not from his code/seedq1/*.py.
Clio, 2026-10-16.

Representation: Laurent polynomials in q as dict {exponent: int coeff}.
Exact, symbolic in q -- stronger than his q=3/7 rational specialisation.
"""
from itertools import product as iproduct
from collections import defaultdict

# ---------- Laurent arithmetic in q ----------
def lzero(): return {}
def lone(): return {0: 1}
def lmono(e, c=1): return {e: c} if c else {}
def ladd(a, b):
    r = dict(a)
    for e, c in b.items():
        r[e] = r.get(e, 0) + c
        if r[e] == 0: del r[e]
    return r
def lmul(a, b):
    r = {}
    for e1, c1 in a.items():
        for e2, c2 in b.items():
            e = e1 + e2
            r[e] = r.get(e, 0) + c1 * c2
            if r[e] == 0: del r[e]
    return r
def lneg(a): return {e: -c for e, c in a.items()}

# ---------- lattice forms ----------
class Setup:
    """form = symmetrised Cartan (.,.); phi = the target twist, both as I x I int matrices."""
    def __init__(self, form, phi, braid=None):
        self.n = len(form)
        self.form = form
        self.phi = phi
        # braid lets us PLANT a wrong braiding for positive controls
        self.braid = braid if braid is not None else form
    def pair(self, a, b):      # (a,b) used in the BRAIDING / crossing weights
        return sum(a[i] * self.braid[i][j] * b[j] for i in range(self.n) for j in range(self.n))
    def truepair(self, a, b):  # the genuine symmetrised form, used in the bialgebra axiom
        return sum(a[i] * self.form[i][j] * b[j] for i in range(self.n) for j in range(self.n))
    def ph(self, a, b):
        return sum(a[i] * self.phi[i][j] * b[j] for i in range(self.n) for j in range(self.n))

def vadd(a, b): return tuple(x + y for x, y in zip(a, b))
def wdeg(w):
    if not w: return None
    d = w[0]
    for x in w[1:]: d = vadd(d, x)
    return d
def wdeg0(w, n): return wdeg(w) if w else tuple([0]*n)

# ---------- QSym_{q,phi} ----------
def qs_product(S, al, be):
    """M_al * M_be as {word: laurent}.  Recursion over quasi-shuffles (f,g)."""
    r, s = len(al), len(be)
    # suffix sums of al for crossing weights
    suf = [tuple([0]*S.n)] * (r + 1)
    for i in range(r - 1, -1, -1): suf[i] = vadd(al[i], suf[i + 1])
    out = defaultdict(lzero)
    def rec(i, j, word, wt):
        if i == r:
            out[tuple(word) + tuple(be[j:])] = ladd(out[tuple(word) + tuple(be[j:])], wt); return
        if j == s:
            out[tuple(word) + tuple(al[i:])] = ladd(out[tuple(word) + tuple(al[i:])], wt); return
        # 1. al[i] alone
        rec(i + 1, j, word + [al[i]], wt)
        # 2. be[j] alone -> crosses every not-yet-placed al letter
        rec(i, j + 1, word + [be[j]], lmul(wt, lmono(S.pair(be[j], suf[i]))))
        # 3. merge al[i] with be[j] -> merge weight, plus be[j] crosses al[i+1..]
        w3 = lmul(wt, lmono(S.ph(al[i], be[j]) + S.pair(be[j], suf[i + 1])))
        rec(i + 1, j + 1, word + [vadd(al[i], be[j])], w3)
    rec(0, 0, [], lone())
    return dict(out)

def lin_product(S, X, Y):
    out = defaultdict(lzero)
    for a, ca in X.items():
        for b, cb in Y.items():
            for w, c in qs_product(S, a, b).items():
                out[w] = ladd(out[w], lmul(lmul(ca, cb), c))
    return {w: c for w, c in out.items() if c}

def qs_coproduct(al):
    """deconcatenation; returns {(left,right): laurent}"""
    out = defaultdict(lzero)
    for k in range(len(al) + 1):
        out[(al[:k], al[k:])] = ladd(out[(al[:k], al[k:])], lone())
    return dict(out)

# ---------- word enumeration ----------
def compositions_of(nu):
    """all words (tuples of nonzero vectors in N^I) summing to nu"""
    n = len(nu)
    parts = [p for p in iproduct(*[range(nu[i] + 1) for i in range(n)]) if any(p)]
    res = []
    def rec(rem, acc):
        if all(x == 0 for x in rem):
            res.append(tuple(acc)); return
        for p in parts:
            if all(p[i] <= rem[i] for i in range(n)):
                rec(tuple(rem[i] - p[i] for i in range(n)), acc + [p])
    rec(tuple(nu), [])
    return res

def words_up_to(nu_bound):
    """all words of degree <= nu_bound componentwise"""
    n = len(nu_bound)
    ws = []
    for nu in iproduct(*[range(b + 1) for b in nu_bound]):
        ws.extend(compositions_of(nu))
    return ws
