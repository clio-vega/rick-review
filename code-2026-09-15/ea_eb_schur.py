"""Rick's Day 193 meta-conjecture: e_a * e_b has exactly min(a,b)+1 terms.
Browse 142 reported "no classical analogue with the min(a,b)+1 shape".
There is one, and it is the Littlewood-Richardson rule. Since e_r = s_{1^r},
    s_{1^a} . s_{1^b} = sum_{k=0}^{min(a,b)} s_{(2^k, 1^{a+b-2k})}
- exactly min(a,b)+1 Schur terms, each with multiplicity one.

Two independent checks:
 (1) dual Jacobi-Trudi:  s_{(2^k,1^{a+b-2k})} = det [[e_{a+b-k}, e_{a+b-k+1}],
                                                     [e_{k-1},   e_k      ]]
     (conjugate of (2^k,1^{a+b-2k}) is (a+b-k, k)), then the sum TELESCOPES to
     e_{max(a,b)} e_{min(a,b)} = e_a e_b.  Done in free commuting e_i.
 (2) brute force in monomials for small (a,b), Schur via the bialternant.
"""
import sympy as sp
from itertools import combinations

M = 14
e = list(sp.symbols('e0:%d' % (M+1)))
def E(i):
    if i < 0 or i > M: return sp.Integer(0)
    return sp.Integer(1) if i == 0 else e[i]

print("(1) dual Jacobi-Trudi + telescoping, in free e_i")
print("    a  b | terms | sum_k s_{(2^k,1^{a+b-2k})}  ==  e_a e_b ?")
for a in range(1, 6):
    for b in range(a, 6):
        tot = sp.Integer(0)
        for k in range(min(a, b)+1):
            # lambda = (2^k, 1^{a+b-2k}) has conjugate (a+b-k, k)
            tot += E(a+b-k)*E(k) - E(a+b-k+1)*E(k-1)
        ok = sp.expand(tot - E(a)*E(b)) == 0
        print("    %d  %d |   %d   |  %s" % (a, b, min(a, b)+1, "PASS" if ok else "*** FAIL ***"))

print()
print("(2) brute force in monomials (Schur via bialternant), small cases")
def e_r(r, xs):
    if r == 0: return sp.Integer(1)
    if r > len(xs): return sp.Integer(0)
    return sp.expand(sum(sp.prod(c) for c in combinations(xs, r)))
def schur(lam, xs):
    n = len(xs); lam = list(lam) + [0]*(n-len(lam))
    num = sp.Matrix(n, n, lambda i, j: xs[i]**(lam[j] + n-1-j)).det()
    den = sp.prod([xs[i]-xs[j] for i in range(n) for j in range(i+1, n)])
    return sp.cancel(sp.expand(num)/sp.expand(den))
for a, b in [(1, 1), (1, 2), (2, 2), (1, 3), (2, 3)]:
    n = a + b
    xs = sp.symbols('x1:%d' % (n+1))
    lhs = sp.expand(e_r(a, xs)*e_r(b, xs))
    lams = [tuple([2]*k + [1]*(a+b-2*k)) for k in range(min(a, b)+1)]
    rhs = sp.expand(sum(schur(l, xs) for l in lams))
    print("    a=%d b=%d : %-30s %s" % (a, b, " + ".join("s_%s" % "".join(map(str, l)) for l in lams),
          "PASS" if sp.expand(lhs-rhs) == 0 else "*** FAIL ***"))
