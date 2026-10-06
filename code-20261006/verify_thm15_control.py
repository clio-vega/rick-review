"""
Independent check of Rick's Theorem 1.5 (Day 223 §1), written from the
definitions in his §0, NOT from his scripts/day223/star2.py.

   T_k(f) := sum_{|A|=k} c_A X_A f(X_A),   c_A = prod_{i in A, j notin A} (x_i - t x_j)/(x_i - x_j)
   line G := coefficient of e_n in the e-expansion of G  = (-1)^{n-1} n [p_n] G
   CLAIM:  line T_k(f) = (-1)^d [n]_t/[k]_t * f(1,t,...,t^{k-1}),  f in Lambda_k deg d, n=k+d
"""
import sympy as sp
from itertools import combinations
from kostka_d_matrix import partitions

t = sp.symbols('t')

def bracket(m):
    return sp.simplify(sum(t**i for i in range(m)))

def run(k, d, verbose=True):
    n = k + d
    N = n
    xs = sp.symbols(f'x1:{N+1}')
    # test functions f in Lambda_k of degree d: monomial symmetric m_nu in k vars
    results = []
    for nu in partitions(d):
        if len(nu) > k: continue
        ys = sp.symbols(f'y1:{k+1}')
        from itertools import permutations
        l = list(nu) + [0]*(k-len(nu))
        f_expr = sp.expand(sum(sp.prod([ys[i]**p[i] for i in range(k)])
                               for p in set(permutations(l))))
        # build T_k(f)
        Tk = sp.Integer(0)
        for A in combinations(range(N), k):
            Ac = [j for j in range(N) if j not in A]
            cA = sp.Integer(1)
            for i in A:
                for j in Ac:
                    cA *= (xs[i] - t*xs[j])/(xs[i] - xs[j])
            XA = sp.prod([xs[i] for i in A])
            fA = f_expr.subs({ys[r]: xs[A[r]] for r in range(k)}, simultaneous=True)
            Tk += cA * XA * fA
        Tk = sp.simplify(sp.together(Tk))
        Tk = sp.cancel(Tk)
        Tk = sp.expand(sp.simplify(Tk))
        # line via (-1)^{n-1} n [p_n] G : extract p_n coefficient.
        # Easier: line G = coeff of e_n in e-expansion. Use the pairing
        # line G = (-1)^{n-1} n [p_n] G, and [p_n]G found by expanding G in
        # the monomial basis then using [p_n] m_lam = (-1)^{l-1}(l-1)!/prod m_i!
        # We instead use the e-expansion directly: e_n = x1...xN coefficient route.
        # line G = coefficient of the monomial x1 x2 ... xN in G  (since among all
        # e_lambda, only e_n contains x1...xN with coeff 1 ... ) -- NOT true in general.
        # Use p_n route:
        poly = sp.Poly(sp.expand(Tk), *xs)
        # [p_n] G  via Hall pairing is awkward; instead expand in monomial basis:
        from collections import defaultdict
        mono = defaultdict(lambda: sp.Integer(0))
        for mon, c in poly.terms():
            key = tuple(sorted([e for e in mon if e > 0], reverse=True))
            if sum(mon) != n: continue
            mono[key] += c
        # each m_lam counted once per distinct exponent pattern: divide by #perms present
        # coefficient of m_lam = coefficient of a single representative monomial
        rep = {}
        for mon, c in poly.terms():
            if sum(mon) != n: continue
            key = tuple(sorted([e for e in mon if e > 0], reverse=True))
            if key not in rep: rep[key] = c
        pn_coeff = sp.Integer(0)
        import math
        for lam, c in rep.items():
            l = len(lam)
            from collections import Counter
            mult = Counter(lam)
            denom = sp.Integer(1)
            for v in mult.values(): denom *= sp.factorial(v)
            pn_coeff += c * (-1)**(l-1) * sp.factorial(l-1) / denom
        line = sp.simplify((-1)**(n-1) * n * pn_coeff)
        rhs = sp.simplify((-1)**d * bracket(n)/bracket(k+1) *
                          f_expr.subs({ys[r]: t**r for r in range(k)}, simultaneous=True))
        ok = sp.simplify(sp.expand(sp.cancel(line - rhs))) == 0
        results.append((nu, ok, sp.simplify(line), sp.simplify(rhs)))
        if verbose:
            print(f"   k={k} d={d} f=m_{nu}: {'OK' if ok else 'MISMATCH'}")
            if not ok:
                print(f"      line={sp.factor(line)}")
                print(f"      rhs ={sp.factor(rhs)}")
    return results

print("Theorem 1.5 independent check (Clio, from definitions):")
allr=[]
for (k,d) in [(2,1),(2,2),(3,1),(2,3),(3,2)]:
    allr += run(k,d)
ok=sum(1 for _,o,_,_ in allr if o); print(f"\nTOTAL OK {ok}/{len(allr)}")
