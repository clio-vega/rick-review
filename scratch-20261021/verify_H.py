"""Lemma H (exact peel) and Lemma Lambda, from the text of
proofs/2026-10-20-dual-block-identity.md sections 3 and 4."""
import sympy as sp
from itertools import combinations
from phicalc import *

def res_inf(h, z):
    """Residue at infinity: -Res_{t=0} h(1/t)/t^2."""
    t = sp.Symbol('t')
    return -sp.residue(sp.simplify(h.subs(z, 1/t)/t**2), t, 0)

print("=== Lemma H (exact peel) ===")
# Phi_r^M[f] = Phi_r^{M-}[ f(x) prod_j (u x_j - 1)/(u(x_j - u)) ]
#            + (1-u^-2) g_{M-}(u) u^{-(r-1)} Phi_{r-1}^{M-}[ f(u,x') prod_j (u - x'_j) ]
tests = [((1,2,3), 1), ((1,2,3), 2), ((1,2,3), 3),
         ((2,3,4,5), 2), ((1,2,4), 2), ((1,2,4), 1)]
# a few symmetric test functions f of r variables
fams = {
  "1":        lambda x: sp.Integer(1),
  "e_r":      lambda x: sp.prod(x),
  "p1":       lambda x: sum(x),
  "sum x^-1": lambda x: sum(1/xi for xi in x),
}
for M, r in tests:
    n = max(M); Mm = tuple(sorted(set(M) - {n}))
    w = wvars(M); u = w[n]
    for name, f in fams.items():
        lhs = Phi(M, r, f, w)
        t1 = Phi(Mm, r, lambda x: f(x)*sp.prod([(u*xj - 1)/(u*(xj - u)) for xj in x]), w)
        t2 = (1 - u**-2)*gS(Mm, u, w)*u**(-(r-1)) * \
             Phi(Mm, r-1, lambda x: f((u,)+tuple(x))*sp.prod([(u - xj) for xj in x]), w)
        ok = sp.simplify(sp.together(lhs - t1 - t2)) == 0
        print("  M=%-12s r=%d f=%-9s : %s" % (str(M), r, name, "OK" if ok else "FAIL"))

print("=== Lemma Lambda ===")
# Phi_r^M[f] = - sum_{H'} S0^M(H') (Res_0 + Res_inf)[ z^-1 G_{M\H'}(z) f(x_{H'}, z) ]
z = sp.Symbol('z')
for M, r in [((1,2,3),1), ((1,2,3),2), ((2,3,4),2), ((1,2,4),3), ((2,3,4),1)]:
    w = wvars(M)
    for name, f in fams.items():
        lhs = Phi(M, r, f, w)
        tot = sp.Integer(0)
        for Hp in combinations(sorted(M), r-1):
            xs = tuple(w[j] for j in Hp)
            S = tuple(t for t in sorted(M) if t not in Hp)
            h = sp.simplify(gS(S, z, w) * f(xs + (z,)) / z)
            tot += S0(M, Hp, w) * (sp.residue(h, z, 0) + res_inf(h, z))
        ok = sp.simplify(sp.together(lhs + tot)) == 0
        print("  M=%-12s r=%d f=%-9s : %s" % (str(M), r, name, "OK" if ok else "FAIL"))
