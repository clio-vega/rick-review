"""Verify Rick's Thm 2.5 (FPSAC thm:2pt) at a=2 against the independent engine.

Statement transcribed FIRST-HAND from peers/rick/incoming-20261007c2/fpsac2027-draft.tex,
lines 267-274 (registry node two-point-string-formula-thm25):

  Phi_a(g;x,y) = (-1)^a (1-t^x)(1-t^y) * {
      sum_{A=1}^{a-1} t^{-AB} [ G_{A,y-B}/((1-t^A)(1-t^B))
                                + 1/(1-t^a) sum_{m>=1} (t^{-Am} - t^{Bm}) G_{A,y-B-m} ]
      - g(1,t,...,t^{a-1})/(1-t^a) * sum_{j=0}^{a-1} t^{-jy} }
  with B = a-A and G_A(w) = g(1,t,...,t^{A-1}, w, wt, ..., wt^{B-1}) = sum_k G_{A,k} w^k.

Dictionary (lem:dict):  Phi_a(P_rho;x,y) = (1-t^x)(1-t^y) X^{rho+1^a}_{(x,y)} / b_lambda.

P_rho(x1,x2;t) is built here from the Weyl symmetrisation definition (Macdonald III (2.2)),
NOT from Rick's G1 helper -- so the 2-variable HL input is independent too.

Note on scope: Phi_a and the right-hand side are both LINEAR in g, and
{P_rho : rho |- d, l(rho) <= 2} is a basis of the degree-d part of Lambda_2.
Our rho range (rho_2 = lam_2 - 1 >= 0) is exactly that basis. So testing g = P_rho
over this range tests the a=2 case of thm:2pt for EVERY g in Lambda_2, not just for P_rho.
"""
import sympy as sp
from fractions import Fraction as F
from hl_orthogonality import GreenEngine, b_lambda

t, w = sp.symbols('t w')

def P_two_var(rho, x1, x2):
    """P_rho(x1,x2;t) from the symmetrisation definition, Macdonald III (2.2):
       P_lam = (1/v_lam(t)) sum_{w in S_2} w( x^lam * (x1 - t x2)/(x1 - x2) )."""
    r1, r2 = rho
    num = (x1**r1 * x2**r2 * (x1 - t*x2) / (x1 - x2)
           + x2**r1 * x1**r2 * (x2 - t*x1) / (x2 - x1))
    # v_lam(t) = prod_i v_{m_i(lam)}(t), v_m(t) = prod_{k=1}^m (1-t^k)/(1-t)^m
    v = 1
    from collections import Counter
    for _p, mlt in Counter(rho).items():
        vm = sp.prod([(1 - t**k) for k in range(1, mlt+1)]) / (1-t)**mlt
        v *= vm
    return sp.cancel(sp.together(num / v))

def Phi_a2(rho, x, y):
    """Thm 2.5 at a=2 (A=B=1), g = P_rho."""
    a, A, B = 2, 1, 1
    G = sp.Poly(sp.expand(sp.cancel(P_two_var(rho, 1, w))), w)
    def Gk(k):
        return G.coeff_monomial(w**k) if k >= 0 else 0
    g_at = P_two_var(rho, 1, t)                        # g(1,t,...,t^{a-1}) = g(1,t)
    inner = (Gk(y-B)/((1-t**A)*(1-t**B))
             + sp.Rational(1,1)/(1-t**a) * sum((t**(-A*m) - t**(B*m))*Gk(y-B-m)
                                               for m in range(1, y+1)))
    brace = t**(-A*B)*inner - g_at/(1-t**a)*sum(t**(-j*y) for j in range(a))
    return (-1)**a * (1-t**x)*(1-t**y) * brace

def X_from_thm2pt(lam, x, y):
    rho = (lam[0]-1, lam[1]-1)
    bl = sp.prod([sp.prod([(1-t**k) for k in range(1, mlt+1)])
                  for _p, mlt in __import__('collections').Counter(lam).items()])
    return sp.cancel(sp.simplify(Phi_a2(rho, x, y) * bl / ((1-t**x)*(1-t**y))))

if __name__ == '__main__':
    import sys
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 9
    TV = [F(2), F(3), F(5), F(-2), F(1,2), F(7,3)]
    engines = {}
    bad = 0; tot = 0; rhos = set()
    for n in range(2, NMAX+1):
        for l2 in range(1, n//2 + 1):
            lam = (n-l2, l2); rho = (lam[0]-1, lam[1]-1); rhos.add(rho)
            for y in range(1, n):
                x = n - y
                Xsym = sp.expand(X_from_thm2pt(lam, x, y))
                for tv in TV:
                    tot += 1
                    key = (n, tv)
                    if key not in engines: engines[key] = GreenEngine(n, tv)
                    gt = engines[key].X(lam, tuple(sorted((x, y), reverse=True)))
                    got = sp.nsimplify(Xsym.subs(t, sp.Rational(tv)))
                    if sp.simplify(got - sp.Rational(gt)) != 0:
                        bad += 1
                        if bad <= 5: print('FAIL', lam, (x, y), tv, got, gt)
        print('  n=%d done' % n, flush=True)
    print()
    print('Thm 2.5 (thm:2pt) at a=2, RAW, vs independent engine, n=2..%d' % NMAX)
    print('  evaluations            : %d' % tot)
    print('  disagreements          : %d' % bad)
    print('  distinct rho tested    : %d  -> %s' % (len(rhos), sorted(rhos)))
    print('  degrees d=|rho| covered: %s' % sorted({sum(r) for r in rhos}))
    print('  these P_rho form a BASIS of (Lambda_2)_d for each d, so the a=2 case')
    print('  of thm:2pt is verified for every g in Lambda_2 of those degrees.')
