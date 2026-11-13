"""Positive control for ring.py's Groebner decision: feed it a DISGUISED
Grassmannian ideal (Gr ideal pushed through x->2x, y->3y-7x^2/2 ... ) and
check it reports EXISTS; and a perturbed one, check NONE."""
import sympy as sp
from ring import h_poly, x, y, e1, e2, a, b, c, w
lam, mu, nu = sp.symbols('lam mu nu')
def decide(f, g, k):
    hk1, hk2 = h_poly(k + 1), h_poly(k + 2)
    sub = {x: a * e1, y: b * e2 + c * e1 ** 2}
    eqs = sp.Poly(sp.expand(f.subs(sub, simultaneous=True) - lam * hk1), e1, e2).coeffs()
    eqs += sp.Poly(sp.expand(g.subs(sub, simultaneous=True) - mu * e1 * hk1 - nu * hk2), e1, e2).coeffs()
    eqs.append(w * a * b - 1)
    return list(sp.groebner(eqs, w, lam, mu, nu, a, b, c, order='lex').exprs) != [1]
for k in (3, 4, 5):
    T = {e1: 2 * x, e2: 3 * y - sp.Rational(7, 2) * x ** 2}
    f = sp.expand(h_poly(k + 1).subs(T, simultaneous=True)); g = sp.expand(h_poly(k + 2).subs(T, simultaneous=True))
    gp = sp.expand(g + x ** (k + 2) if (k + 2) else g)
    print('k=%d disguised Gr: %s (want True);  perturbed g+x^%d: %s (want False)' % (k, decide(f, g, k), k + 2, decide(f, gp, k)))
