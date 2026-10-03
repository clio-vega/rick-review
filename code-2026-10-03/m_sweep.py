"""
Are the two findings m-dependent?  m = number of variables (Rick's N).
Finding 1: Op-DS support is NOT the full up-set.  mu=(1,1), k=2, rho=(2,2) absent.
Finding 2: e^star_{(1,1)} = (1-s)(1+t) e_2 + s e_{1,1}, so at t=-1 the e_2 term dies
           and (S)/(D)'s "support is exactly {mu |> lam}" fails at that numeric t.

NB the e-basis in degree n is indexed by partitions of n with PARTS <= m (not with
<= m parts). For n <= m the two index sets coincide, which is why the main m=4,n<=4
run could use the same routine; here they are separated properly.
"""
import sympy as sp
from itertools import combinations

s, t = sp.symbols('s t')

def run(m, n, targets):
    xs = sp.symbols('x1:%d' % (m+1))
    def parts_atmost(n, k):           # <= k parts  (monomial / m-basis index)
        def go(n, k, mx):
            if n == 0: yield []; return
            if k == 0: return
            for a in range(min(n, mx), 0, -1):
                for r in go(n-a, k-1, a): yield [a]+r
        return list(go(n, k, n))
    def parts_maxpart(n, mx):          # parts <= mx  (e-basis index)
        return [list(reversed(p)) for p in
                [sorted(q) for q in parts_atmost(n, n)] ] if False else \
               [p for p in parts_atmost(n, n) if (not p or p[0] <= mx)]
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
        if k > m: return {}
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
        return {tuple(e): sp.cancel(c/den) for e, c in zip(P.monoms(), P.coeffs())
                if sp.cancel(c/den) != 0}
    def e_expand(d, n):
        EB = parts_maxpart(n, m); MB = parts_atmost(n, m)
        assert len(EB) == len(MB), (len(EB), len(MB))
        M = sp.Matrix([[e_lam(list(nu)).get(pad(mu), 0) for nu in EB] for mu in MB])
        rhs = sp.Matrix([d.get(pad(mu), 0) for mu in MB])
        sol = M.solve(rhs)
        return {tuple(EB[i]): sp.cancel(sp.simplify(sol[i])) for i in range(len(EB))}

    print("  m = %d (N = %d variables)" % (m, m))
    for mu, k in targets:
        nn = sum(mu)+k
        if k > m: print("    mu=%s k=%d : e_%d = 0 in %d vars, skipped" % (mu, k, k, m)); continue
        cf = e_expand(Ek(e_lam(mu), k), nn)
        uk = tuple(sorted(list(mu)+[k], reverse=True))
        upset = [tuple(r) for r in parts_maxpart(nn, m) if dom_leq(list(uk), list(r))]
        miss = [list(r) for r in upset if sp.simplify(cf.get(r, 0)) == 0]
        lead = cf.get(uk, 0)
        print("    E_%d e_%-9s : up-set %s" % (k, str(mu), [list(r) for r in upset]))
        print("        nonzero  : %s" % {str(list(a)): sp.factor(b) for a, b in cf.items() if sp.simplify(b) != 0})
        print("        MISSING from up-set : %s" % (miss if miss else "none"))
        print("        lead [e_{mu u k}] = %s  (= s^%d : %s)" % (
            sp.factor(lead), sum(min(x, k) for x in mu),
            sp.simplify(lead - s**sum(min(x, k) for x in mu)) == 0))

print("FINDING 1: Op-DS support equality, mu=(1,1) k=2, is rho=(2,2) absent for every m?")
for m in [3, 4, 5]:
    run(m, 4, [([1, 1], 2)])

print("\nFINDING 2: e^star_{(1,1)} = E_1 E_1 (1), and its t=-1 behaviour")
for m in [2, 3, 4, 5]:
    run(m, 2, [([1], 1)])
