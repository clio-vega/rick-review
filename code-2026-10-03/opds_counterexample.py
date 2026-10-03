"""
Focused, self-contained check of ONE claim in Rick's "Operator form (Op-DS)":

    "So the support is {rho |> mu u k}"    <- stated as an EQUALITY

Rick flags this paragraph: "Not checked separately by script."
Counterexample candidate from the main run: mu = (1,1), k = 2, rho = (2,2).

Independent of the main script: Macdonald P is not used at all here. E_k is applied
directly to the ordinary product e_mu, and the result is expanded in the e-basis by
solving a linear system over Q(s,t).
"""
import sympy as sp
from itertools import combinations, permutations

s, t = sp.symbols('s t')
m = 4
xs = sp.symbols('x1:%d' % (m+1))

def parts(n, k=m):
    def go(n, k, mx):
        if n == 0: yield []; return
        if k == 0: return
        for a in range(min(n, mx), 0, -1):
            for r in go(n-a, k-1, a): yield [a]+r
    return list(go(n, k, n))
def pad(l): return tuple(list(l)+[0]*(m-len(l)))
def dom_leq(a, b):
    sa = sb = 0
    for i in range(max(len(a), len(b))):
        sa += a[i] if i < len(a) else 0
        sb += b[i] if i < len(b) else 0
        if sa > sb: return False
    return True

def e_sym(k):
    if k == 0: return {tuple([0]*m): sp.Integer(1)}
    d = {}
    for A in combinations(range(m), k):
        ex = [0]*m
        for i in A: ex[i] = 1
        d[tuple(ex)] = sp.Integer(1)
    return d
def mul(a, b):
    o = {}
    for e1, c1 in a.items():
        for e2, c2 in b.items():
            kk = tuple(i+j for i, j in zip(e1, e2))
            o[kk] = sp.cancel(o.get(kk, 0)+c1*c2)
    return {k: v for k, v in o.items() if v != 0}
def e_lam(l):
    o = {tuple([0]*m): sp.Integer(1)}
    for k in l: o = mul(o, e_sym(k))
    return o

def Ek(d, k):
    """Rick's E_k F = sum_{|A|=k} prod_{i in A, j notin A} (x_i-t x_j)/(x_i-x_j) X_A F(X_A->sX_A)"""
    poly = sum(c*sp.prod([xs[i]**e for i, e in enumerate(ex)]) for ex, c in d.items())
    out = 0
    for A in combinations(range(m), k):
        Ac = [j for j in range(m) if j not in A]
        co = sp.prod([xs[i] for i in A])
        for i in A:
            for j in Ac: co *= (xs[i]-t*xs[j])/(xs[i]-xs[j])
        out += co*poly.subs({xs[i]: s*xs[i] for i in A}, simultaneous=True)
    out = sp.cancel(sp.together(out))
    num, den = sp.fraction(out)
    P = sp.Poly(sp.expand(num), *xs)
    return {tuple(e): sp.cancel(c/den) for e, c in zip(P.monoms(), P.coeffs()) if sp.cancel(c/den) != 0}

def e_expand(d, n):
    B = parts(n)
    M = sp.Matrix([[e_lam(list(nu)).get(pad(mu), 0) for nu in B] for mu in B])
    rhs = sp.Matrix([d.get(pad(mu), 0) for mu in B])
    sol = M.solve(rhs)
    return {tuple(B[i]): sp.cancel(sp.simplify(sol[i])) for i in range(len(B))}

print("E_k e_mu expanded in the e-basis; m = %d" % m)
print("Rick: support = {rho |> mu u k}, lead [e_{mu u k}] = s^{sum_i min(mu_i,k)}\n")
for mu, k in [([1, 1], 2), ([1], 1), ([1], 2), ([1], 3), ([2], 2), ([1, 1], 1),
              ([1, 1, 1], 1), ([2, 1], 1), ([2], 1), ([1,1],2)]:
    n = sum(mu)+k
    if n > m: continue
    cf = e_expand(Ek(e_lam(mu), k), n)
    uk = tuple(sorted(list(mu)+[k], reverse=True))
    upset = [tuple(r) for r in parts(n) if dom_leq(list(uk), list(r))]
    present = [r for r in upset if sp.simplify(cf.get(r, 0)) != 0]
    missing = [r for r in upset if sp.simplify(cf.get(r, 0)) == 0]
    outside = [r for r in cf if sp.simplify(cf[r]) != 0 and not dom_leq(list(uk), list(r))]
    print("mu=%-10s k=%d   mu u k = %-10s" % (mu, k, list(uk)))
    print("   full e-expansion:", {list(a).__repr__(): sp.factor(b) for a, b in cf.items() if sp.simplify(b) != 0})
    print("   up-set of mu u k : %s" % [list(r) for r in upset])
    print("   PRESENT          : %s" % [list(r) for r in present])
    print("   MISSING (zero)   : %s   <== breaks support = up-set" % [list(r) for r in missing] if missing else "   MISSING (zero)   : none")
    print("   outside up-set   : %s" % [list(r) for r in outside])
    print("   lead [e_{mu u k}] = %s   want s^%d : %s" % (
        sp.factor(cf.get(uk, 0)), sum(min(x, k) for x in mu),
        sp.simplify(cf.get(uk, 0)-s**sum(min(x, k) for x in mu)) == 0))
    print()
