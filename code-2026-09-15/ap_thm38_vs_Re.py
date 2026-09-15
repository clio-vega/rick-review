"""
Peer review 2026-09-15, item 1: is Rick's (Re) a consequence of the STATEMENT of
Alexandersson-Panova (arXiv:1705.10353) Theorem 38 (label thm:generatingFunctionsPathCycle)?

AP Thm 38 (statement, verbatim from the arXiv LaTeX source):
    sum_n X_{P_n}(x;q) z^n  =  ( sum_{i>=0} e_i(x) z^i ) / ( 1 - q sum_{i>=2} [i-1]_q e_i(x) z^i )

Rick's (Re)  (registry path-graph-qGF.json, node R-equiv-ebasis-positive, trust=proved):
    X_n = e_n + q sum_{k=2}^{n} [k-1]_q e_k X_{n-k}

Three independent checks:
  (A) ground truth: X_{P_n}(x;q) from the Shareshian-Wachs definition (sum over proper
      colourings, weight q^asc) -- NOT from either formula -- expanded in the e-basis.
  (B) AP Thm 38's generating function reproduces (A).
  (C) Rick's (Re) is the coefficient-of-z^n extraction of AP Thm 38's statement,
      done symbolically with e_i as free commuting indeterminates (a ring identity,
      independent of any chromatic interpretation).
"""
import sympy as sp
from itertools import product

q = sp.symbols('q')
NMAX = 7

# ---------- (A) ground truth from the Shareshian-Wachs definition ----------
# X_{P_n}(x_1..x_m;q) = sum over proper colourings kappa of the path 1-2-...-n
#   of q^{asc(kappa)} x_{kappa(1)}...x_{kappa(n)},  asc = #{i : kappa(i) < kappa(i+1)}.
def X_path_monomial(n, m, xs):
    if n == 0:
        return sp.Integer(1)
    total = sp.Integer(0)
    for kappa in product(range(m), repeat=n):
        if any(kappa[i] == kappa[i+1] for i in range(n-1)):
            continue                      # not a proper colouring
        asc = sum(1 for i in range(n-1) if kappa[i] < kappa[i+1])
        mon = sp.Integer(1)
        for c in kappa:
            mon *= xs[c]
        total += q**asc * mon
    return sp.expand(total)

# e-basis: expand a degree-n symmetric poly in m>=n variables into e_lambda.
def e_poly(i, xs):
    m = len(xs)
    if i == 0: return sp.Integer(1)
    if i > m:  return sp.Integer(0)
    from itertools import combinations
    return sp.expand(sum(sp.prod(c) for c in combinations(xs, i)))

def expand_in_e(poly, n, xs):
    """Return dict {partition: coeff in q} with poly = sum coeff * e_lambda."""
    import sympy
    parts = []
    def gen(rem, mx, cur):
        if rem == 0: parts.append(tuple(cur)); return
        for k in range(min(rem, mx), 0, -1):
            gen(rem-k, k, cur+[k])
    gen(n, n, [])
    basis = {lam: sp.expand(sp.prod([e_poly(k, xs) for k in lam])) for lam in parts}
    coeffs = {lam: sp.Symbol('c_%s' % '_'.join(map(str, lam))) for lam in parts}
    expr = sp.expand(poly - sum(coeffs[l]*basis[l] for l in parts))
    sol = sp.solve(sp.Poly(expr, *xs).coeffs(), list(coeffs.values()), dict=True)
    assert sol, "e-expansion failed for n=%d" % n
    return {l: sp.simplify(sol[0][coeffs[l]]) for l in parts}

print("=" * 72)
print("(A) ground truth  X_{P_n} from the colouring definition, in the e-basis")
print("=" * 72)
truth = {0: {(): sp.Integer(1)}}
for n in range(1, 6):                     # n<=5 : colouring sum is n^m, keep it honest
    m = n                                 # n variables suffice in degree n
    xs = sp.symbols('x1:%d' % (m+1))
    truth[n] = expand_in_e(X_path_monomial(n, m, xs), n, xs)
    terms = " + ".join("(%s)e_%s" % (sp.factor(c), "".join(map(str, l)))
                       for l, c in sorted(truth[n].items()) if c != 0)
    print("  X_P%d = %s" % (n, terms))
