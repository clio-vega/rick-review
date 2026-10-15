"""
Independent check of Rick's Day 207b, Lemma 7 (the one-index q-series identity, star).
Clio, 2026-10-15.  Pure SymPy -- no combinatorics library -- so this reaches the same
ground truth by a different mechanism than his scripts/day207b.

Definitions, verbatim from his (1):
    alpha_j = prod_{i=1}^{j} (s - t^i) / (t;t)_j,         alpha_{-1} = 0
    c(n,j)  = (s;t)_{n-j}/(t;t)_{n-j} * ( alpha_j - s t^{n-j} alpha_{j-1} )
    c(n,j)  = 0 outside 0 <= j <= n
    F_n(w)  = sum_{j=0}^n c(n,j) w^j
"""
import sympy as sp

s, t, w = sp.symbols('s t w')

def qpoch(a, q, n):
    """(a;q)_n = prod_{i=0}^{n-1} (1 - a q^i)."""
    r = sp.Integer(1)
    for i in range(n):
        r *= (1 - a*q**i)
    return r

def alpha(j):
    if j < 0:
        return sp.Integer(0)
    num = sp.Integer(1)
    for i in range(1, j+1):
        num *= (s - t**i)
    return sp.cancel(num / qpoch(t, t, j))

def c(n, j):
    if not (0 <= j <= n):
        return sp.Integer(0)
    pref = qpoch(s, t, n-j) / qpoch(t, t, n-j)
    return sp.cancel(pref * (alpha(j) - s*t**(n-j)*alpha(j-1)))

def F(n, wval):
    return sp.cancel(sum(c(n, j)*wval**j for j in range(0, n+1)))

# ---- sanity: c(0,0) must be 1 (needed for the base case Gamma_0 = T_0) ----
print("c(0,0) =", sp.simplify(c(0,0)), " [base case of Thm 1 needs this = 1]")

# ---- Lemma 7 (star) ----
# (1-t^n) c(n,j)
#   = (1 - s t^{-j}) sum_{p>=0} (s t^{-j})^p c(n-1-p, j)
#     - t^n (1 - s t^{1-j}) sum_{p>=0} (s t^{1-j})^p c(n-1-p, j-1)
def star_lhs(n, j):
    return sp.cancel((1 - t**n)*c(n, j))

def star_rhs(n, j, PMAX=None):
    if PMAX is None:
        PMAX = n + 3           # generous: c(n-1-p,.) = 0 well before this
    A = sum((s*t**(-j))**p * c(n-1-p, j)   for p in range(PMAX+1))
    B = sum((s*t**(1-j))**p * c(n-1-p, j-1) for p in range(PMAX+1))
    return sp.cancel((1 - s*t**(-j))*A - t**n*(1 - s*t**(1-j))*B)

print("\n=== Lemma 7 (star):  n = 1..9,  j = 0..n+1  (j=n+1 is an out-of-range control) ===")
fails = []
checked = 0
for n in range(1, 10):
    row = []
    for j in range(0, n+2):
        d = sp.simplify(sp.cancel(star_lhs(n, j) - star_rhs(n, j)))
        ok = (d == 0)
        checked += 1
        row.append('.' if ok else 'X')
        if not ok:
            fails.append((n, j, d))
    print(f"  n={n}: " + ''.join(row))
print(f"  checked {checked} (n,j) pairs; failures: {len(fails)}")
for f in fails:
    print("   FAIL", f[0], f[1], sp.simplify(f[2]))

# ---- POSITIVE CONTROL: the check must be able to fail. ----
print("\n=== positive control: perturb the identity and confirm the test fires ===")
def star_rhs_broken(n, j):
    """Drop the t^n prefactor on the second sum -- a single-symbol lesion."""
    PMAX = n + 3
    A = sum((s*t**(-j))**p * c(n-1-p, j)   for p in range(PMAX+1))
    B = sum((s*t**(1-j))**p * c(n-1-p, j-1) for p in range(PMAX+1))
    return sp.cancel((1 - s*t**(-j))*A - (1 - s*t**(1-j))*B)
nfire = 0
for n in range(1, 6):
    for j in range(0, n+1):
        if sp.simplify(sp.cancel(star_lhs(n, j) - star_rhs_broken(n, j))) != 0:
            nfire += 1
print(f"  lesioned identity fails in {nfire} of 20 (n,j) pairs  -> test is non-vacuous" if nfire else "  CONTROL DID NOT FIRE -- test is vacuous")

# ---- The identity F_n(t^{-n}) = 0, which the m=0 branch of Thm 1 needs ----
print("\n=== F_n(t^{-n}) = 0 ?   [this is what 'm=0: Step Lemma gives T_k = 0' requires] ===")
for n in range(0, 9):
    v = sp.simplify(F(n, t**(-n)))
    print(f"  n={n}:  F_n(t^-n) = {v}")
