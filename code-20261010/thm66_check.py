"""
Independent referee check of printed Thm 6.6, against MY OWN subset-formula engine.
Also checks Rick's hand claim Lead_{(1,1,1),(3)} = [3]_t (2+t)
(blockmult-printed-n6-check.md, "Zero leads" paragraph).

The printed Thm 6.6 RHS is re-implemented here from the FPSAC text @ e44e29f only.
"""
import sys; sys.path.insert(0,'/home/clio/projects/reviews/code-20261010')
import star
from star import *
from symfun import partitions, e_poly, e_mu, mono_coeff, kappa
from fractions import Fraction
from itertools import permutations
import sympy
from pairing_check import printed_thm63
from prop61_fast import e_expand_num, _cache

T = sympy.Symbol('t')
def brk(m, q=None):
    q = T if q is None else q
    return sum(q**i for i in range(m))          # [m]_q = 1+q+...+q^{m-1}
def Xi(a, r, q):                                # Xi_a(r,q) = lin T_a(p_r p_q)
    return (-1)**(r+q) * brk(a+r+q)/brk(a) * brk(a, T**r) * brk(a, T**q)
def L(a, b):
    return (1-T**(a+b))*(T**(a*b)-1)/((1-T**a)*(1-T**b))
def Mmat(k, r):
    """Prop 3.3: M_{kr} = r e_k e_r + sum_{j=1..r} L(k-r+j,j) e_{k+j} e_{r-j}.
    Returned as dict: sorted tuple of e-indices (0's dropped) -> coefficient."""
    if k < r: k, r = r, k
    d = {}
    def add(p, cf):
        p = tuple(sorted([z for z in p if z > 0], reverse=True))
        d[p] = d.get(p, 0) + cf
    if r > 0: add((k, r), r)
    for j in range(1, r+1): add((k+j, r-j), L(k-r+j, j))
    return d
def Da(a, poly):
    """D_a = derivation with D_a(e_j) = M_{aj}, applied to an e-polynomial."""
    out = {}
    for p, cf in poly.items():
        for i in range(len(p)):
            rest = p[:i] + p[i+1:]
            for q, cf2 in Mmat(a, p[i]).items():
                key = tuple(sorted(rest + q, reverse=True))
                out[key] = out.get(key, 0) + cf*cf2
    return out

def printed_lead(a, b, c, x, y):
    n = a+b+c
    m_xy = 2 if x == y else 1
    Phi = printed_thm63(lambda v: sum(z**b for z in v)*sum(z**c for z in v), a, b+c, x, y)
    U = ((-1)**n * Phi - Xi(a, b, c)) / m_xy
    res = (-1)**(b+c) * U
    res += sum((-1)**(r+c)*Xi(a, r, c) for r in range(1, b)
               if sorted([b-r, a+r+c]) == sorted([x, y]))
    res += sum((-1)**(b+q)*Xi(a, b, q) for q in range(1, c)
               if sorted([c-q, a+b+q]) == sorted([x, y]))
    res += Da(a, Mmat(b, c)).get(tuple(sorted([x, y], reverse=True)), 0)
    return sympy.cancel(sympy.expand(sympy.cancel(res)))

def my_lead(lam, mu, tval, N=None):
    """[(s-1)^2] c_{lam,mu} from the subset formula, my engine, t specialised."""
    star.set_t(Fraction(tval)); _cache.clear()
    a, b, c = lam; n = sum(lam); N = N or n
    ec = e_poly(c, N)
    acc = p_zero()
    for q in range(3):
        Fq = E_k_p(ec, b, q, N)
        if p_is_zero(Fq): continue
        G = E_k_p(Fq, a, 2-q, N)
        if not p_is_zero(G): acc = p_add(acc, G)
    return e_expand_num(acc, n, N)[tuple(sorted(mu, reverse=True))]

if __name__ == '__main__':
    print("A. Rick's hand claim  Lead_{(1,1,1),(3)} = [3]_t (2+t)")
    claim = sympy.expand(brk(3)*(2+T))
    for tv in ['5/3', '3/5', '-2', '7/4']:
        mine = my_lead((1,1,1), (3,), Fraction(tv))
        pred = claim.subs(T, sympy.Rational(Fraction(tv)))
        print(f"   t={tv:5s}: mine={mine}  [3]_t(2+t)={pred}  match={sympy.Rational(mine)==pred}")

    print("\nB. printed Thm 6.6 vs my engine, lambda=(2,2,2), two-part mu with kappa=1")
    lam = (2,2,2)
    for mu in [(5,1), (3,3), (4,2), (2,2,2)]:
        k = kappa(lam, mu)
        tag = "kappa=1 (in scope)" if k == 1 else f"kappa={k} (OUT of scope)"
        row = []
        for tv in ['5/3', '3/5', '7/4']:
            mine = my_lead(lam, mu, Fraction(tv))
            pr = printed_lead(2,2,2, mu[0], mu[1]) if len(mu) == 2 else None
            if pr is None: row.append("n/a"); continue
            prv = sympy.Rational(sympy.cancel(pr.subs(T, sympy.Rational(Fraction(tv)))))
            row.append("OK" if sympy.Rational(mine) == prv else f"DIFFER(mine={mine},printed={prv})")
        print(f"   mu={str(mu):10s} {tag:22s} t=5/3,3/5,7/4 -> {row}")
