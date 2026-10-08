"""Jing--Liu, 'The Green polynomials via vertex operators', arXiv:2104.04411,
J. Pure Appl. Algebra 226 (2022) 107032.  Two-row formula, unnumbered display
immediately after the Recurrence Formula theorem, arXiv v2 Sect. 2, p. 7
(locator held at extraction level `verified-quote` in memory/reading/sources.json;
independently verified 102/102 for n=4..7 on 2026-10-06):

    X^{(m,k)}_rho(t) = (t-1) * sum_{i<k} D^{(i)}(rho) t^{k-1-i}  +  D^{(k)}(rho),
    where  D_t(mu) = sum_i D^{(i)}(mu) t^i = prod_{i>=1} (1 + t^i)^{m_i(mu)}.

Note the superscript (m,k) is the HL index: this is two-row LAMBDA, ARBITRARY rho.
"""
from collections import Counter
import sympy as sp
t = sp.Symbol('t')

def D_coeffs(rho, kmax):
    poly = sp.Poly(sp.expand(sp.prod([(1 + t**i)**mlt for i, mlt in Counter(rho).items()])), t)
    return [poly.coeff_monomial(t**i) if i >= 0 else 0 for i in range(kmax + 1)]

def X_jingliu(lam, rho):
    m, k = lam
    D = D_coeffs(rho, max(k, sum(rho)) + 1)
    return sp.expand((t-1)*sum(D[i]*t**(k-1-i) for i in range(k)) + D[k])

if __name__ == '__main__':
    from fractions import Fraction as F
    from hl_orthogonality import GreenEngine
    from compare_rick_day228 import X_rick, X_clio_thmC
    TV = [F(2), F(3), F(5), F(-2), F(1,2), F(7,3)]
    bad_e = bad_r = bad_c = 0; tot = 0; sym_r = 0; rows = 0
    for n in range(2, 11):
        eng = {tv: GreenEngine(n, tv) for tv in TV}
        for l2 in range(1, n//2 + 1):
            lam = (n - l2, l2)
            for y in range(1, n):
                x = n - y; rho = tuple(sorted((x, y), reverse=True)); rows += 1
                XJ = X_jingliu(lam, rho)
                # (i) symbolic: is Jing-Liu's formula IDENTICAL to Rick's closed form?
                if sp.simplify(XJ - sp.expand(X_rick(lam, x, y, t))) != 0: sym_r += 1
                # (ii) numeric vs the independent engine and vs Clio Thm C
                for tv in TV:
                    tot += 1
                    gt = eng[tv].X(lam, rho)
                    if sp.nsimplify(XJ.subs(t, sp.Rational(tv))) != sp.Rational(gt): bad_e += 1
                    if XJ.subs(t, sp.Rational(tv)) != sp.Rational(X_rick(lam, x, y, tv)): bad_r += 1
                    if XJ.subs(t, sp.Rational(tv)) != sp.Rational(X_clio_thmC(lam, x, y, tv)): bad_c += 1
    print('Jing-Liu 2104.04411 two-row formula, restricted to TWO-PART rho, n=2..10')
    print('  rows (Rick\'s index set)                    : %d' % rows)
    print('  symbolic mismatches  JL  vs RICK Day 228    : %d' % sym_r)
    print('  numeric   mismatches JL  vs engine          : %d / %d' % (bad_e, tot))
    print('  numeric   mismatches JL  vs RICK            : %d / %d' % (bad_r, tot))
    print('  numeric   mismatches JL  vs CLIO Thm C      : %d / %d' % (bad_c, tot))
    print()
    print('  worked branch identification (symbolic, generic lam):')
    for lam, rho, lab in [((6,3),(8,1),'y<lam_2'), ((6,3),(6,3),'y=lam_2, x!=y'),
                          ((5,5),(5,5),'y=lam_2, x=y (m_xy=2)'), ((6,3),(5,4),'y>lam_2')]:
        print('   lam=%s rho=%s [%-22s] JL=%-28s Rick=%s' %
              (lam, rho, lab, X_jingliu(lam, rho), sp.expand(X_rick(lam, rho[0], rho[1], t))))
