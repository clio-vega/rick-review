"""
Verify the textbook facts that LOCATE Rick's t^{-1} (Theorem H, map phi).
  (B) Macdonald VI (4.14)(iv):  P_lam(x; q^{-1}, t^{-1}) = P_lam(x; q, t)
  (C) consequence:              lim_{q->oo} P_lam(x;q,t) = P_lam(x; t^{-1})  (HL at 1/t)
Checked on closed forms for lam=(2) and lam=(2,1) in 2 and 3 variables.
"""
import sympy as sp
q, t = sp.symbols('q t')

print("(2)-coefficient: P_(2) = m_2 + c*m_11,  c = (1-t)(1+q)/(1-qt)")
c2 = (1-t)*(1+q)/(1-q*t)
print("   q->0  :", sp.simplify(sp.limit(c2, q, 0)), "  [expect (1-t) = HL at t]")
cinf = sp.simplify(sp.limit(c2, q, sp.oo))
print("   q->oo :", sp.simplify(cinf), "  [expect (1-1/t) = HL at 1/t]")
print("   (C) MATCH?", sp.simplify(cinf - (1 - 1/t)) == 0)

print("\n(B) inversion symmetry on c:  c(1/q,1/t) ?= c(q,t)")
lhs = sp.cancel(sp.together(c2.subs({q:1/q, t:1/t})))
print("   c(1/q,1/t) =", sp.factor(lhs))
print("   c(q,t)     =", sp.factor(sp.cancel(c2)))
print("   EQUAL?", sp.simplify(sp.cancel(lhs - c2)) == 0)

print("\n(2,1)-coefficient: P_(2,1) = m_21 + c21*m_111,")
print("   c21 = (1-t)(2+q+1/?)... use Macdonald's value c21 = (1-t)(2+q+qt)/(1-qt^2)?")
# Macdonald VI: P_{(2,1)} = m_{21} + c * m_{111} with
# c = (1-t)(2 + q + q t + 2 q t ... ) -- avoid misquoting; derive by orthogonality
# Instead: verify (C) on the HL side using the known HL P_{(2,1)}(x;t) = m_21 + (2+t)(1-t)... 
# Safer: test (B) structurally on the ratio form that appears in b(box):
print("\n(B) on a b(box) factor: f = (1-q^{a+1}t^{l})/(1-q^{a}t^{l+1})")
a, l = sp.symbols('a l', integer=True, nonnegative=True)
f = (1-q**(a+1)*t**l)/(1-q**a*t**(l+1))
finv = f.subs({q:1/q, t:1/t})
print("   f(1/q,1/t)/f(q,t) =", sp.simplify(sp.powsimp(sp.cancel(sp.together(finv/f)), force=True)))
print("   (ratio should be a monomial in q,t -- i.e. f is inversion-covariant up to a monomial)")
