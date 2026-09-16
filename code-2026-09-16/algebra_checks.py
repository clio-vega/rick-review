import sympy as sp
q, t, r = sp.symbols('q t r')
def qi(n): return sp.simplify(sp.together((1 - t**n)/(1-t)))

print("=== (A) Rick 4.4: q-integer identity [2][r-1][r+1] = [r+2][r-1] + t[r+1][r-2] + t^{r-1}[2] ===")
L = qi(2)*qi(r-1)*qi(r+1)
R = qi(r+2)*qi(r-1) + t*qi(r+1)*qi(r-2) + t**(r-1)*qi(2)
print("   symbolic in r:", sp.simplify(sp.expand(L-R)) == 0)
for rv in range(0,9):
    d = sp.simplify(L.subs(r,rv) - R.subs(r,rv))
    if d != 0: print("   *** fails at r=%d: %s" % (rv, d))

print("\n=== (B) Rick 4.4: P_3 = ([r+1]q - t[r-1])([r+2]q - t^2[r-2]) - t^r [2] q ===")
P3 = qi(r+1)*qi(r+2)*q**2 - t*qi(2)*qi(r-1)*qi(r+1)*q + t**3*qi(r-2)*qi(r-1)
F  = (qi(r+1)*q - t*qi(r-1))*(qi(r+2)*q - t**2*qi(r-2)) - t**r*qi(2)*q
print("   symbolic:", sp.simplify(sp.expand(P3 - F)) == 0)
for rv in range(0,9):
    d = sp.simplify(sp.expand(P3.subs(r,rv) - F.subs(r,rv)))
    if d != 0: print("   *** fails at r=%d: %s" % (rv, d))

print("\n=== (C) Day192 claim: discriminant of the q-quadratic has an irreducible deg-6 t-factor at r=3 ===")
for rv in [3,4,5,6]:
    P = sp.Poly(sp.expand(P3.subs(r,rv)), q)
    A,B,C = P.all_coeffs()
    disc = sp.factor(sp.expand(B**2 - 4*A*C))
    print("   r=%d: disc = %s" % (rv, disc))
    fl = sp.factor_list(sp.expand(B**2-4*A*C))
    degs = [(sp.Poly(f,t).degree(), sp.Poly(f,t).is_irreducible) for f,_ in fl[1]]
    print("        factors (deg_t, irreducible?): %s" % degs)

print("\n=== (D) q->infty limit of c_0: is it binom(r+3,3)_t ? ===")
pre = (q-1)/q**3 * qi(r+3)/(qi(2)*qi(3))
c0 = pre * (qi(r+1)*qi(r+2)*q**2 - t*qi(2)*qi(r-1)*qi(r+1)*q + t**3*qi(r-2)*qi(r-1))
lim = sp.simplify(sp.limit(sp.expand(c0), q, sp.oo))
G = qi(r+1)*qi(r+2)*qi(r+3)/(qi(2)*qi(3))
print("   lim_{q->oo} c_0 - binom(r+3,3)_t =", sp.simplify(sp.expand(lim - G)))

print("\n=== (E) brief Q3: is q[r]_t - t[r-2]_t a known HL/Macdonald coefficient? ===")
X = sp.simplify(q*qi(r) - t*qi(r-2))
print("   general:", sp.simplify(sp.together(X)))
print("   at q=t :", sp.factor(sp.simplify(sp.expand((q*qi(r) - t*qi(r-2)).subs(q,t)))))
for rv in range(1,7):
    print("   r=%d: %s   | at q=t: %s" % (rv, sp.expand(X.subs(r,rv)),
          sp.factor(sp.expand(X.subs(r,rv).subs(q,t)))))
