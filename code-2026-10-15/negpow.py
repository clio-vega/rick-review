"""
Gamma_k (the LHS of Rick's Theorem 1, first display) is a POWER SERIES in z:
    Gamma_k = sum_{r>=0} z^r t^{-C(k,2)} e_k(Y).e_r  =  E(z) * sum_{|A|=k} prod^x_A prod phi(X_a)
and phi(u) = u(1+suz)/(1+uz) expands with non-negative powers of z only.

T_k (the RHS) is a LAURENT polynomial in z:
    T_k = sum_{j+b<=k} s^b t^{-kj} c(k-b,j) e_b z^{b-k} E(t^j z),
whose lowest term is z^{-k} (b=0, n=0) since E(t^j z) is a polynomial in z.

So Gamma_k = T_k as displayed REQUIRES every negative power of z in T_k to cancel.
Extracting:   [z^p] T_k = sum_{b=0}^{k} s^b F_{k-b}(t^{p-b}) e_b e_{p+k-b}
(the Theorem-1 right-hand side with r replaced by p).  For p = -N < 0 this reads
    [z^-N] T_k = sum_{b=0}^{k-N} s^b F_{k-b}(t^{-N-b}) e_b e_{k-N-b}.
We test whether that vanishes, treating e_1,e_2,... as INDEPENDENT (valid for m large).
Clio, 2026-10-15.
"""
import sympy as sp

s, t = sp.Rational(5,7), sp.Rational(3,5)
E = sp.symbols('e0:40')     # e_0 = 1 formally
def ee(i):
    if i < 0:  return sp.Integer(0)
    if i == 0: return sp.Integer(1)
    return E[i]

def qp(a,n):
    r = sp.Integer(1)
    for i in range(n): r *= (1 - a*t**i)
    return r
A = {-1: sp.Integer(0)}
def al(j):
    if j in A: return A[j]
    num = sp.Integer(1)
    for i in range(1,j+1): num *= (s - t**i)
    A[j] = num/qp(t,j); return A[j]
def c(n,j):
    if not (0<=j<=n): return sp.Integer(0)
    return qp(s,n-j)/qp(t,n-j)*(al(j) - s*t**(n-j)*al(j-1))
def F(n,wv): return sum(c(n,j)*wv**j for j in range(n+1))

print("[z^-N] T_k  with e_1,e_2,... treated as independent symbols")
print("(if Gamma_k = T_k exactly as displayed, every one of these must be 0)\n")
anybad = False
for k in range(1,7):
    for N in range(1,k+1):
        expr = sp.expand(sum(s**b * F(k-b, t**(-N-b)) * ee(b) * ee(k-N-b)
                             for b in range(0, k-N+1)))
        z = sp.simplify(expr) == 0
        if not z: anybad = True
        print(f"  k={k} N={N}:  [z^-{N}]T_k = {sp.nsimplify(sp.simplify(expr))}"
              + ("" if z else "   <-- NONZERO"))
    print()
print("All negative-power coefficients vanish:", not anybad)

print("\n--- and the non-negative side, as a control: [z^r]T_k for r>=0 should NOT vanish ---")
for k in (1,2,3):
    for r in (0,1,2):
        expr = sp.expand(sum(s**b*F(k-b,t**(r-b))*ee(b)*ee(r+k-b) for b in range(k+1)))
        print(f"  k={k} r={r}: {sp.simplify(expr)}")
