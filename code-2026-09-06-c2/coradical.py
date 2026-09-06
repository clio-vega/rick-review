"""Day 173 section 3(ii): is wt (Sym-degree) the coradical filtration of Sym with the
standard coproduct?  Smallest case where they could differ is degree 2.
Sym = S(V), V = span{p_1,p_2,...} all primitive => coradical filtration C_n = S^{<=n}(V)
= span{p_lambda : l(lambda) <= n}.  Check by computing reduced coproducts directly."""
import sympy as sp
from itertools import product

# work in degree <= 4, basis p_lambda; Delta(p_n) = p_n (x) 1 + 1 (x) p_n
# represent elements as dicts: partition(tuple, sorted desc) -> coeff
def pmul(a, b):
    out = {}
    for la, ca in a.items():
        for lb, cb in b.items():
            k = tuple(sorted(la+lb, reverse=True))
            out[k] = out.get(k, 0) + ca*cb
    return {k: v for k, v in out.items() if v}

def coprod(x):
    """Delta on p_lambda = prod (p_i (x) 1 + 1 (x) p_i); returns dict (l1,l2)->coeff"""
    out = {}
    for lam, c in x.items():
        terms = {((), ()): c}
        for part in lam:
            nt = {}
            for (l, r), cc in terms.items():
                for k in [(tuple(sorted(l+(part,), reverse=True)), r),
                          (l, tuple(sorted(r+(part,), reverse=True)))]:
                    nt[k] = nt.get(k, 0) + cc
            terms = nt
        for k, v in terms.items():
            out[k] = out.get(k, 0) + v
    return {k: v for k, v in out.items() if v}

def reduced(x):
    d = coprod(x)
    return {k: v for k, v in d.items() if k[0] != () and k[1] != ()}

# e_k in the power sum basis (Newton):  e_k = sum_{lambda |- k} eps(lambda) p_lambda / z_lambda
def e_in_p(k):
    from sympy.combinatorics.partitions import IntegerPartition
    from sympy.utilities.iterables import partitions as parts
    out = {}
    for pt in parts(k):
        lam = tuple(sorted(sum([[a]*b for a, b in pt.items()], []), reverse=True))
        z = 1
        for a, b in pt.items(): z *= (a**b)*sp.factorial(b)
        eps = (-1)**(k - len(lam))
        out[lam] = out.get(lam, 0) + sp.Rational(eps, z)
    return out

for name, x in [("p_2", {(2,): 1}), ("p_1^2", {(1,1): 1}),
                ("e_2", e_in_p(2)), ("e_3", e_in_p(3)), ("p_3", {(3,): 1})]:
    r = reduced(x)
    maxlen = max((max(len(a), len(b)) for a, b in r), default=0)
    lvl = 1 if not r else 1 + max(len(a)+len(b) for a, b in r) - 1
    deg = sum(list(x.keys())[0]) if len(x) == 1 else sum(max(x, key=lambda l: sum(l)))
    print(f"{name:6s}: wt(Sym-degree) = {deg},  reduced coproduct {'= 0 (PRIMITIVE)' if not r else '!= 0'},"
          f"  coradical level = {min(len(a)+len(b) for a,b in r) if r else 1}")
