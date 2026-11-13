"""§4 of Rick Q75: the ideal I = ker(Q[x,y] -> G_(2^k)), x=M_1, y=M_2=p_2,
computed from the shuffle pairing; then graded isomorphism with
H*(Gr(2,k+2)) = Q[e1,e2]/(h_{k+1},h_{k+2}) decided by a Groebner basis over
C (a,b,c unknowns, ab invertible)."""
import sys
from fractions import Fraction
import sympy as sp
from qsym import qsym_mul, F_product, comp_to_mask, str_to_mask
x, y, e1, e2, a, b, c, w = sp.symbols('x y e1 e2 a b c w')

X = {0: 1}            # F_1 (degree 1)
Y = {0: 1, 1: -1}     # M_2 = F_2 - F_11 (degree 2)
def monomial_F(p, q):
    f, deg = {0: 1}, 0     # unit encoded as degree 0
    for _ in range(p):
        f = qsym_mul(f, deg, X, 1) if deg else dict(X); deg += 1
    for _ in range(q):
        f = qsym_mul(f, deg, Y, 2) if deg else dict(Y); deg += 2
    return f, deg

def nullspace_Q(rows):
    M = sp.Matrix(rows)
    return M.T.nullspace()   # vectors c with sum_r c_r row_r = 0

def ideal_degree(s, n):
    """basis of I_n as sympy polys in x,y."""
    d = len(s) + 1; sm = str_to_mask(s); j = d - n
    mons = [(n - 2 * q, q) for q in range(n // 2 + 1)]
    rows = []
    for (p, q) in mons:
        f, deg = monomial_F(p, q)
        if j == 0:
            rows.append([f.get(sm, 0)])
        elif j < 0:
            rows.append([0])
        else:
            rows.append([sum(cf * F_product(mf, n, mb, j).get(sm, 0) for mf, cf in f.items())
                         for mb in range(1 << (j - 1))])
    return [sp.expand(sum(v[t] * x ** mons[t][0] * y ** mons[t][1] for t in range(len(mons))))
            for v in nullspace_Q(rows)], len(mons)

def h_poly(n):
    h = [sp.Integer(1), e1]
    for m in range(2, n + 1):
        h.append(sp.expand(e1 * h[m - 1] - e2 * h[m - 2]))
    return h[n]

def generated_dims(gens, n):
    """dim of degree-n part of the ideal (gens) in Q[x,y], weights 1,2."""
    vecs = []
    mons = [(n - 2 * q, q) for q in range(n // 2 + 1)]
    for g in gens:
        dg = sp.Poly(g, x, y).as_dict(); deg = max(p + 2 * q for p, q in dg)
        for q2 in range((n - deg) // 2 + 1):
            p2 = n - deg - 2 * q2
            if p2 < 0: continue
            pr = sp.Poly(sp.expand(g * x ** p2 * y ** q2), x, y).as_dict()
            vecs.append([pr.get(m, 0) for m in mons])
    return sp.Matrix(vecs).rank() if vecs else 0

def main():
 for k in range(2, int(sys.argv[1]) + 1):
     s = '01' * (k - 1) + '0'          # (2^k), L = 2k-1
     d = 2 * k
     hilb = []; I = {}
     for n in range(0, d + 2):
         basis, nm = ideal_degree(s, n)
         I[n] = basis; hilb.append(nm - len(basis))
     print('k=%d  Hilb(Q[x,y]/I) = %s' % (k, hilb[:d + 1]), 'low ideal:', {n: len(I[n]) for n in range(k + 3)})
     f = I[k + 1][0]
     # g: an element of I_{k+2} not in x*f
     cand = [p for p in I[k + 2]]
     g = None
     for p in cand:
         if sp.Matrix([[sp.Poly(q, x, y).as_dict().get(m, 0) for m in [(k + 2 - 2 * t, t) for t in range((k + 2) // 2 + 1)]] for q in [sp.expand(x * f), p]]).rank() == 2:
             g = p; break
     # normalise like Rick: monic in the pure x power
     f = sp.expand(f / sp.Poly(f, x, y).as_dict()[(k + 1, 0)])
     g = sp.expand(g - sp.Poly(g, x, y).as_dict().get((k + 1, 0), 0) * 0)
     print('   f =', f); print('   g =', g)
     # do (f,g) generate I in every degree up to d+1 ?
     ok = all(generated_dims([f, g], n) == len(I[n]) for n in range(d + 2))
     print('   (f,g) generate I through degree %d: %s' % (d + 1, ok))
     # graded iso phi: x->a e1, y-> b e2 + c e1^2 ; need phi(f) in J_{k+1}=<h_{k+1}>, phi(g) in J_{k+2}=<e1 h_{k+1}, h_{k+2}>
     hk1, hk2 = h_poly(k + 1), h_poly(k + 2)
     lam, mu, nu = sp.symbols('lam mu nu')
     sub = {x: a * e1, y: b * e2 + c * e1 ** 2}
     eqs = []
     eqs += sp.Poly(sp.expand(f.subs(sub, simultaneous=True) - lam * hk1), e1, e2).coeffs()
     eqs += sp.Poly(sp.expand(g.subs(sub, simultaneous=True) - mu * e1 * hk1 - nu * hk2), e1, e2).coeffs()
     eqs.append(w * a * b - 1)
     G = sp.groebner(eqs, w, lam, mu, nu, a, b, c, order='lex')
     print('   graded iso G_(2^%d) ~ H*(Gr(2,%d)) over C:' % (k, k + 2),
           'NONE (Groebner basis = [1])' if list(G.exprs) == [1] else 'EXISTS; GB tail %s' % list(G.exprs)[-3:])
if __name__ == "__main__":
    main()
