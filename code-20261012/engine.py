"""
Independent engine for reviewing Rick's longversion sec:nabla (Thm N) + app:cherednik.
Everything is built from the PRINTED definitions, in pure SymPy.
Macdonald polynomials come from Macdonald VI (3.4) -- NOT from Rick's Y-circ operators,
so the Thm N check reads the corner by a second mechanism.
"""
import itertools, functools
from sympy import symbols, Rational, cancel, expand, simplify, Poly, together, factor, binomial

s, t = symbols('s t')

def xs(m):
    return symbols('x1:%d' % (m+1))

# ---------- basic operator layer (printed definitions, sec:hikita) ----------

def swap(f, X, i):
    """apply s_i : swap x_i, x_{i+1}  (1-indexed i)"""
    a, b = X[i-1], X[i]
    return f.subs({a: b, b: a}, simultaneous=True)

def T(f, X, i):
    """T_i f = t s_i f + (t-1) x_{i+1}/(x_i - x_{i+1}) (s_i f - f)   -- printed def"""
    sf = swap(f, X, i)
    return cancel(t*sf + (t-1)*X[i]/(X[i-1]-X[i])*(sf - f))

def Tinv(f, X, i):
    """T_i^{-1} = t^{-1} T_i - (1 - t^{-1})   -- (R4)"""
    return cancel(T(f, X, i)/t - (1 - 1/t)*f)

def pi_tw(f, X):
    """pi f(x1..xm) = x1 f(x2,...,xm, s x1)   -- twisted"""
    m = len(X)
    sub = {X[i]: X[i+1] for i in range(m-1)}
    sub[X[m-1]] = s*X[0]
    return expand(X[0]*f.subs(sub, simultaneous=True))

def pi_circ(f, X):
    """pi_circ f(x1..xm) = f(x2,...,xm, s x1)   -- untwisted"""
    m = len(X)
    sub = {X[i]: X[i+1] for i in range(m-1)}
    sub[X[m-1]] = s*X[0]
    return expand(f.subs(sub, simultaneous=True))

def Yop(f, X, i, twisted=True):
    """Y_i = t^{m-i} T_{i-1}...T_1 pi T_{m-1}^{-1}...T_i^{-1}   (rightmost acts first)"""
    m = len(X)
    g = f
    for j in range(m-1, i-1, -1):      # T_{m-1}^{-1} ... T_i^{-1}, rightmost first => T_i^{-1} first
        pass
    # rightmost factor acts first: the word is T_{i-1}..T_1 pi T_{m-1}^{-1}..T_i^{-1}
    # so first apply T_i^{-1}, then T_{i+1}^{-1}, ..., then T_{m-1}^{-1}
    for j in range(i, m):
        g = Tinv(g, X, j)
    g = pi_tw(g, X) if twisted else pi_circ(g, X)
    # then T_1, then T_2, ..., then T_{i-1}
    for j in range(1, i):
        g = T(g, X, j)
    return cancel(t**(m-i) * g)

# ---------- E_k : the subset formula (thm:subset, printed) ----------

def c_A(X, A):
    """c_A = prod_{i in A, j notin A} (x_i - t x_j)/(x_i - x_j)"""
    m = len(X)
    out = 1
    for i in A:
        for j in range(m):
            if j not in A:
                out *= (X[i] - t*X[j])/(X[i]-X[j])
    return out

def E_k(f, X, k):
    """E_k F = sum_{|A|=k} c_A x_A F|_{x_i -> s x_i, i in A}"""
    m = len(X)
    if k > m:
        return 0*f
    tot = 0
    for A in itertools.combinations(range(m), k):
        sub = {X[i]: s*X[i] for i in A}
        xA = functools.reduce(lambda u, v: u*v, [X[i] for i in A], 1)
        tot += c_A(X, A) * xA * f.subs(sub, simultaneous=True)
    return cancel(expand(cancel(tot)))

# ---------- partitions / monomial symmetric functions ----------

def partitions(n, maxlen=None, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0:
        yield ()
        return
    if maxlen is not None and maxlen == 0:
        return
    for first in range(min(n, maxpart), 0, -1):
        for rest in partitions(n-first, None if maxlen is None else maxlen-1, first):
            yield (first,)+rest

def dominates(mu, lam):
    """mu >= lam in dominance (same size)"""
    a = b = 0
    for i in range(max(len(mu), len(lam))):
        a += mu[i] if i < len(mu) else 0
        b += lam[i] if i < len(lam) else 0
        if a < b: return False
    return True

def n_stat(lam):
    return sum(i*p for i, p in enumerate(lam))

def conj(lam):
    if not lam: return ()
    return tuple(sum(1 for p in lam if p > j) for j in range(lam[0]))

def mono_sym(lam, X):
    """monomial symmetric function m_lambda in len(X) variables"""
    m = len(X)
    if len(lam) > m: return 0
    lam = tuple(lam) + (0,)*(m-len(lam))
    seen = set()
    tot = 0
    for p in itertools.permutations(lam):
        if p in seen: continue
        seen.add(p)
        term = 1
        for v, e in zip(X, p):
            term *= v**e
        tot += term
    return expand(tot)

def e_sym(r, X):
    if r == 0: return sympify_one()
    if r > len(X): return 0
    tot = 0
    for A in itertools.combinations(X, r):
        term = 1
        for v in A: term *= v
        tot += term
    return expand(tot)

def sympify_one():
    from sympy import Integer
    return Integer(1)

# ---------- coefficient extraction in the m_lambda basis ----------

def to_mono_dict(f, X, d):
    """express symmetric homogeneous f of degree d in the m_lambda basis -> {lam: coeff}"""
    m = len(X)
    f = expand(cancel(f))
    P = Poly(f, *X)
    out = {}
    for lam in partitions(d, maxlen=m):
        key = tuple(lam) + (0,)*(m-len(lam))
        out[tuple(lam)] = P.coeff_monomial(tuple(key))
    return out

def from_mono_dict(dct, X):
    tot = 0
    for lam, c in dct.items():
        if c != 0:
            tot += c*mono_sym(lam, X)
    return expand(tot)


def psum(lam, m):
    lam = tuple(lam)+(0,)*(m-len(lam))
    out=[]; a=0
    for v in lam[:m]:
        a+=v; out.append(a)
    return tuple(out)
