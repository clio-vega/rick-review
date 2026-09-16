import sympy as sp
q,t = sp.symbols('q t')
def qi(n): return sp.expand(sum(t**i for i in range(n))) if n>0 else sp.Integer(0)
print("A Macdonald/HL Pieri coefficient is always a PRODUCT of binomials (1 - q^a t^b)")
print("(Macdonald VI.6: phi/psi are products of (1-q^{a}t^{b+1})/(1-q^{a+1}t^{b}) type factors).")
print("So: does P_2(r) = q[r]_t - t[r-2]_t factor at all over Q[q,t]?\n")
for r in range(1,11):
    P = sp.expand(q*qi(r) - t*qi(r-2))
    f = sp.factor(P)
    print("  r=%-2d  P_2 = %-34s  factored: %-34s  irreducible over Q[q,t]: %s"
          % (r, P, f, sp.Poly(P,q,t).is_irreducible if P!=0 else '--'))
print("\n  Also: t[r-2]_t = [r-1]_t - 1, so  P_2 = q[r]_t - [r-1]_t + 1.")
for r in range(1,8):
    lhs = sp.expand(q*qi(r)-t*qi(r-2)); rhs = sp.expand(q*qi(r)-qi(r-1)+1)
    assert sp.expand(lhs-rhs)==0, r
print("  verified r=1..7.")
print("\n  At q=t:  q[r]_t - t[r-2]_t = t^{r-1}[2]_t :")
for r in range(1,8):
    v = sp.factor(sp.expand((q*qi(r)-t*qi(r-2)).subs(q,t)))
    print("     r=%d: %s   vs t^{r-1}[2]_t = %s" % (r, v, sp.factor(t**(r-1)*(1+t))))
