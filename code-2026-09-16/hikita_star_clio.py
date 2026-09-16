"""
Clio's INDEPENDENT implementation of Hikita's quantum multiplication (star)
on Lambda_{q,t}, built directly from arXiv:2503.23597 LaTeX source.

Primary source: arxiv.org/e-print/2503.23597, file qt-CSF.tex (fetched 2026-09-16).
All environment numbers resolved by counting the shared `thm` counter
(\newtheorem{thm}{Theorem}[section]; dfn/lemma/prop/cor all share it).

  Def 3.4  (Def_qm, line 649):   F * G := q_(m)( q_(m)^{-1}(F) . q_(m)^{-1}(G) )
                                 equivalently  F * G = q_(m)^{-1}(F) . G
  Lem 3.3  (Lem_iota_elem, 619): q_(m)( e_r(Y_1..Y_m) ) = t^{r(r-1)/2} e_r(X_1..X_m)
  eq (Eqn_Y_i, 564):             Y_i = t^{m-i} T_{i-1}..T_1 Pi T_{m-1}^{-1}..T_i^{-1}
  eq (Eqn_commPiX, 521):         Pi . F = X_1 F(X_2,..,X_m,X_{m+1}),  X_{m+1}=q^{-1}X_1
  Lem 2.x  (Lem_AHA_action, 536): explicit T_i^{+-1} on monomials X_i^k X_{i+1}^l

Consequence used here (NOT taken from Rick):
  e_a(X) * e_r(X) = t^{-a(a-1)/2} * ( e_a(Y) . e_r(X_1,...,X_m) ).

This file deliberately shares NO code with grandpa-rick/rick-research
proofs/scripts/day192/hikita_star.py.
"""
from sympy.polys.fields import field
from sympy.polys.domains import QQ
from itertools import combinations

FF, q, t = field("q,t", QQ)
ONE, ZERO = FF.one, FF.zero

# ---------- Laurent polynomials in X_1..X_m: dict exponent-tuple -> FF ----------

def add(A, B):
    C = dict(A)
    for e, c in B.items():
        v = C.get(e, ZERO) + c
        if v: C[e] = v
        elif e in C: del C[e]
    return C

def scal(c, A):
    if not c: return {}
    return {e: c * v for e, v in A.items()}

def T(i, A, m):
    """T_i . A  for i = 1..m-1, via Lem_AHA_action (monomial formula, no division)."""
    out = {}
    for e, c in A.items():
        k, l = e[i-1], e[i]
        base = list(e)
        def mono(x, y, coef):
            b = list(base); b[i-1] = x; b[i] = y; b = tuple(b)
            v = out.get(b, ZERO) + coef
            if v: out[b] = v
            elif b in out: del out[b]
        if l >= k:
            mono(l, k, t * c)
            for j in range(l - k):          # (l-1,k+1) ... (k,l)
                mono(l-1-j, k+1+j, (t - ONE) * c)
        else:
            mono(l, k, c)
            for j in range(k - l - 1):      # (l+1,k-1) ... (k-1,l+1)
                mono(l+1+j, k-1-j, -(t - ONE) * c)
    return out

def Tinv(i, A, m):
    """T_i^{-1} . A  for i = 1..m-1, via Lem_AHA_action."""
    out = {}
    tinv = ONE / t
    for e, c in A.items():
        k, l = e[i-1], e[i]
        base = list(e)
        def mono(x, y, coef):
            b = list(base); b[i-1] = x; b[i] = y; b = tuple(b)
            v = out.get(b, ZERO) + coef
            if v: out[b] = v
            elif b in out: del out[b]
        if l > k:
            mono(l, k, c)
            for j in range(l - k - 1):      # (l-1,k+1) ... (k+1,l-1)
                mono(l-1-j, k+1+j, (ONE - tinv) * c)
        else:
            mono(l, k, tinv * c)
            for j in range(k - l):          # (l+1,k-1) ... (k,l)
                mono(l+1+j, k-1-j, -(ONE - tinv) * c)
    return out

def Pi(A, m):
    """Pi . F = X_1 * F(X_2,...,X_m,X_{m+1}) with X_{m+1} = q^{-1} X_1."""
    out = {}
    for e, c in A.items():
        # X_i -> X_{i+1}: exponent e[j] moves to slot j+1; e[m-1] goes to X_{m+1}=q^{-1}X_1
        b = [0]*m
        b[0] = e[m-1] + 1          # from X_{m+1}^{e_m} = q^{-e_m} X_1^{e_m}, times X_1
        for j in range(m-1):
            b[j+1] = e[j]
        b = tuple(b)
        coef = c * (ONE/q)**e[m-1]
        v = out.get(b, ZERO) + coef
        if v: out[b] = v
        elif b in out: del out[b]
    return out

def Y(i, A, m):
    """Y_i . A,  Y_i = t^{m-i} T_{i-1}...T_1 Pi T_{m-1}^{-1}...T_i^{-1}  (eq Eqn_Y_i)."""
    B = A
    for j in range(i, m):          # rightmost first: T_i^{-1}, T_{i+1}^{-1}, ..., T_{m-1}^{-1}
        B = Tinv(j, B, m)
    B = Pi(B, m)
    for j in range(1, i):          # then T_1, T_2, ..., T_{i-1}
        B = T(j, B, m)
    return scal(t**(m-i), B)

def e_Y(a, A, m):
    """e_a(Y_1,...,Y_m) . A  =  sum over a-subsets S of prod_{i in S} Y_i . A."""
    total = {}
    for S in combinations(range(1, m+1), a):
        B = A
        for i in S:                # Y_i commute (stated after eq Eqn_commTY)
            B = Y(i, B, m)
        total = add(total, B)
    return total

# ---------- elementary symmetric polynomials and e-basis expansion ----------

def e_poly(r, m):
    """e_r(X_1,...,X_m) as a monomial dict."""
    out = {}
    for S in combinations(range(m), r):
        b = [0]*m
        for i in S: b[i] = 1
        out[tuple(b)] = ONE
    return out

def mul(A, B):
    out = {}
    for e1, c1 in A.items():
        for e2, c2 in B.items():
            b = tuple(x+y for x, y in zip(e1, e2))
            v = out.get(b, ZERO) + c1*c2
            if v: out[b] = v
            elif b in out: del out[b]
    return out

def e_lambda(lam, m):
    out = {tuple([0]*m): ONE}
    for p in lam: out = mul(out, e_poly(p, m))
    return out

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n-k, k):
            yield (k,) + rest

def expand_in_e(A, n, m):
    """Expand symmetric A (degree n) in {e_lambda : lambda |- n, lambda_1 <= m}.
    Solves by leading-monomial triangularity: e_lambda has leading term (in the
    dominance-reverse order on the conjugate) ... we just do exact linear algebra
    on the monomial coefficients, which is unambiguous."""
    lams = [lam for lam in partitions(n) if lam[0] <= m]
    basis = [e_lambda(lam, m) for lam in lams]
    # e_lambda's "leading" monomial: x_1^{l'_1} x_2^{l'_2} ... where l' = conjugate
    def conj(lam):
        return tuple(sum(1 for p in lam if p > j) for j in range(lam[0]))
    order = sorted(range(len(lams)), key=lambda i: conj(lams[i]), reverse=True)
    R = dict(A); coeffs = {}
    for idx in order:
        lam = lams[idx]; c = conj(lam)
        key = tuple(list(c) + [0]*(m-len(c)))
        cf = R.get(key, ZERO)
        if cf:
            coeffs[lam] = cf
            R = add(R, scal(-cf, basis[idx]))
    assert not R, "residual nonzero: not in the span of e_lambda  (residual size %d)" % len(R)
    return coeffs

def star_e(a, r, m=None):
    """e_a(X) * e_r(X), expanded in the e_lambda basis. Def 3.4 + Lem 3.3."""
    if m is None: m = a + r
    assert m >= a + r, "need m >= a+r for the e-basis to be independent"
    A = e_Y(a, e_poly(r, m), m)
    A = scal((ONE/t)**(a*(a-1)//2), A)
    return expand_in_e(A, a+r, m), m
