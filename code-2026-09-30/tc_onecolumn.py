"""Two cross-checks Rick's own writeup asserts but does not test:
  (a) s.2: 'For one column (w-free) this collapses to 207b (L)(a)+(b).'
      i.e. lim_{w->0} T_k must equal 207b's (E_k) closed form.
  (b) the LITERAL reading of (P6): is kappa_gamma^{(i-1,j)} itself equal to
      B(A-st)(A rho-1)/(A(A rho-B))?  (It is the PRODUCT with (P8) that is.)
"""
import sys
sys.path.insert(0, '/home/clio/projects/reviews/code-2026-09-30')
import sympy as sp
from tc_aha import Xs, e, E, cnj, T_closed, Gamma

s, t, z, w = sp.symbols('s t z w')

print("=" * 78)
print("(a) one-column specialisation:  lim_{w->0} T_k  ==  207b (E_k)")
print("      207b (E_k) = sum_{j+b<=k} s^b t^{-kj} c(k-b,j) e_b z^{b-k} E(t^j z)")
print("=" * 78)
def Ek_207b(X, k):
    tot = 0
    for b in range(0, k + 1):
        for j in range(0, k - b + 1):
            tot += s**b * t**(-k*j) * cnj(k-b, j) * e(X, b) * z**(b-k) * E(X, t**j*z)
    return tot

for m in [1, 2, 3]:
    for k in [1, 2, 3]:
        X = Xs(m)
        Tk = sp.cancel(sp.together(T_closed(X, k)))
        lim = sp.simplify(sp.limit(Tk, w, 0))
        d = sp.simplify(sp.expand(lim - Ek_207b(X, k)))
        print(f"  m={m} k={k}: {'OK' if d == 0 else '*** MISMATCH: ' + str(d)}")
        sys.stdout.flush()

print()
print("=" * 78)
print("(b) the literal reading of (P6)")
print("=" * 78)
for i in [1, 2, 3]:
    for j in [0, 1, 2]:
        A, B, rho = t**i, t**j, z/w
        gp, dp = t**(i-1)*z, t**j*w
        kgp = (gp - s*z)*(gp - s*w)/(gp*(gp - dp))
        printed = B*(A - s*t)*(A*rho - 1)/(A*(A*rho - B))
        diff = sp.simplify(sp.cancel(kgp - printed))
        print(f"  i={i} j={j}: kappa^(i-1,j) - (P6 as literally written) = "
              f"{'0' if diff == 0 else 'NONZERO'}")
