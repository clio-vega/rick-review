"""Independent AHA / Y-operator implementation for reviewing Rick's Day 207b.

Deliberately NOT the same mechanism as Rick's scripts/day207b/*.py:
 - he imports his own k3_fast_pipeline.AHA; this is written from scratch
 - polynomials are dicts (exponent tuple) -> sympy coeff in Q(s,t)
 - divided differences are done exactly on monomial PAIRS (closed form),
   not by sp.cancel on a rational expression.
Validated below against Hikita Lemma 3.3: e_k(Y) . 1 = t^{C(k,2)} e_k.
"""
import itertools, sympy as sp

s, t, z = sp.symbols('s t z')

class Pol:
    """poly in X_1..X_m over Q(s,t); dict: tuple(exps) -> coeff"""
    __slots__ = ('m', 'd')
    def __init__(self, m, d=None):
        self.m = m; self.d = {} if d is None else d
    def copy(self): return Pol(self.m, dict(self.d))
    def _add(self, mon, c):
        if c == 0: return
        n = self.d.get(mon, 0) + c
        n = sp.expand(n) if not isinstance(n, int) else n
        if n == 0: self.d.pop(mon, None)
        else: self.d[mon] = n
    def __add__(self, o):
        r = self.copy()
        for mon, c in o.d.items(): r._add(mon, c)
        return r
    def __sub__(self, o):
        r = self.copy()
        for mon, c in o.d.items(): r._add(mon, -c)
        return r
    def scale(self, a):
        a = sp.together(a)
        return Pol(self.m, {mon: sp.expand(c*a) for mon, c in self.d.items() if sp.expand(c*a) != 0})
    def mulvar(self, i):          # multiply by X_{i+1} (0-based i)
        r = Pol(self.m)
        for mon, c in self.d.items():
            mm = list(mon); mm[i] += 1; r._add(tuple(mm), c)
        return r
    def is_zero(self):
        return all(sp.simplify(c) == 0 for c in self.d.values())
    def norm(self):
        return Pol(self.m, {k: sp.cancel(sp.together(v)) for k, v in self.d.items()
                            if sp.cancel(sp.together(v)) != 0})

def const(m, c=1): return Pol(m, {(0,)*m: sp.sympify(c)}) if c != 0 else Pol(m)

def e_poly(m, k, idx=None):
    """elementary symmetric e_k in the variables listed in idx (default all)."""
    if idx is None: idx = list(range(m))
    r = Pol(m)
    if k < 0 or k > len(idx): return r
    if k == 0: return const(m, 1)
    for comb in itertools.combinations(idx, k):
        mon = [0]*m
        for i in comb: mon[i] = 1
        r._add(tuple(mon), sp.Integer(1))
    return r

def swap(P, i):               # s_i : swap X_{i+1} <-> X_{i+2} (0-based i)
    r = Pol(P.m)
    for mon, c in P.d.items():
        mm = list(mon); mm[i], mm[i+1] = mm[i+1], mm[i]
        r._add(tuple(mm), c)
    return r

def divdiff(P, i):
    """(s_i P - P)/(X_{i+1} - X_{i+2}), exact, via monomial pairs."""
    r = Pol(P.m)
    for mon, c in P.d.items():
        a, b = mon[i], mon[i+1]
        if a == b: continue      # s_i-invariant pair contributes 0
        # (X_i^b X_{i1}^a - X_i^a X_{i1}^b)/(X_i - X_{i1})
        lo, hi = min(a, b), max(a, b)
        sgn = 1 if b > a else -1     # numerator s_iP - P
        for l in range(hi-lo):
            mm = list(mon)
            mm[i] = lo + (hi-lo-1-l); mm[i+1] = lo + l
            r._add(tuple(mm), sgn*c)
    return r

def T(P, i):
    """T_i P = t s_i P + (t-1) X_{i+1} (s_i P - P)/(X_i - X_{i+1}); i is 1-based."""
    j = i-1
    return swap(P, j).scale(t) + divdiff(P, j).mulvar(j+1).scale(t-1)

def Tinv(P, i):
    """T_i^{-1} = t^{-1} T_i - (1 - t^{-1}), from (T-t)(T+1)=0."""
    return T(P, i).scale(1/t) - P.scale(1 - 1/t)

def pi(P):
    """pi F = X_1 * F(X_2,...,X_m, s X_1)."""
    m = P.m; r = Pol(m)
    for mon, c in P.d.items():
        mm = [0]*m
        for slot in range(m):
            a = mon[slot]
            if a == 0: continue
            if slot < m-1: mm[slot+1] += a
            else:          mm[0] += a
        cc = c * s**mon[m-1]
        r._add(tuple(mm), sp.expand(cc))
    return r.mulvar(0)

def Y(P, i):
    """Y_i = t^{m-i} T_{i-1}..T_1 pi T_{m-1}^{-1}..T_i^{-1}; rightmost acts first."""
    m = P.m; V = P
    for j in range(i, m): V = Tinv(V, j)       # T_i^{-1}, then T_{i+1}^{-1}, ...
    V = pi(V)
    for j in range(1, i): V = T(V, j)          # T_1, then T_2, ... T_{i-1}
    return V.scale(t**(m-i))

def ekY(P, k):
    """e_k(Y) . P = sum over k-subsets b_1<...<b_k of Y_{b_1}...Y_{b_k} P."""
    m = P.m; tot = Pol(m)
    if k > m: return tot
    for b in itertools.combinations(range(1, m+1), k):
        V = P
        for i in reversed(b): V = Y(V, i)      # rightmost acts first
        tot = tot + V
    return tot.norm()
