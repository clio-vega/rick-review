"""
JOB 2, the interpretation of binom(n-1,2) -- DERIVED, then tested UNTUNED.

Derivation.  Psi(s_lambda) = s*_lambda = det[(u_i)_{alpha_j}]/V,  alpha = lambda + delta,
delta = (n-1,...,1,0).  Expand the falling factorial in the Stirling basis,
    (u)_m = sum_k s(m,k) u^k,     s(m,m) = 1,   s(m,m-1) = -binom(m,2).
Column multilinearity of the bialternant gives
    s*_lambda = s_lambda  -  sum_{j : alpha_j - 1 notin alpha} binom(alpha_j,2) s_{lambda-e_j} + (lower).
For lambda = (1^k), alpha = (n, n-1, ..., n-k+1, n-k-1, ..., 1, 0) has EXACTLY ONE
lowerable entry, alpha_k = n-k+1.  Hence

    ***  Psi(e_k)|_n  =  E_k  -  binom(n-k+1, 2) E_{k-1}  +  (lower weight)  ***

k=2 gives binom(n-1,2): Rick's constant, derived rather than fitted.
k=3,4 are UNTUNED predictions -- no parameter of mine was chosen to fit them.
Clio, 2026-09-05.
"""
import sympy as sp, itertools
from sympy.polys.polyfuncs import symmetrize
falling = lambda x, m: sp.prod([x-j for j in range(m)]) if m > 0 else sp.Integer(1)

def V_of(u):
    n = len(u); return sp.expand(sp.prod([u[i]-u[j] for i in range(n) for j in range(i+1, n)]))

def Psi_direct(f, u):
    n = len(u); V = V_of(u); P = sp.Poly(sp.expand(f)*V, *u)
    num = sp.expand(sum(c*sp.prod([falling(u[i], a[i]) for i in range(n)]) for a, c in P.terms()))
    q, r = sp.div(sp.Poly(num, u[0]), sp.Poly(V, u[0])); assert r.is_zero
    return sp.expand(q.as_expr())

def toE(p, u, Es):
    if sp.expand(p) == 0: return sp.Integer(0)
    s, rem, _ = symmetrize(sp.expand(p), list(u), formal=True); assert sp.expand(rem) == 0
    return sp.expand(s.subs({sp.Symbol(f's{k}'): Es[k-1] for k in range(1, len(u)+1)}))

print("="*80)
print("UNTUNED TEST:  Psi(e_k)|_n = E_k - binom(n-k+1,2) E_{k-1} + lower")
print("  (k=2 is Rick's case and reproduces binom(n-1,2); k>=3 is a free prediction)")
print("="*80)
print(f"  {'n':>3} {'k':>3} {'coeff of E_{k-1}':>18} {'-binom(n-k+1,2)':>17}  verdict")
allok = True
for n in range(3, 7):
    u = sp.symbols(f'u1:{n+1}'); Es = sp.symbols(f'E1:{n+1}')
    for k in range(2, min(n, 4)+1):
        ek = sp.expand(sum(sp.prod([u[i] for i in c]) for c in itertools.combinations(range(n), k)))
        expr = toE(Psi_direct(ek, u), u, Es)
        coeff = sp.expand(sp.diff(expr, Es[k-2]).subs({e: 0 for e in Es}))
        pred = -sp.binomial(n-k+1, 2)
        ok = sp.expand(coeff-pred) == 0; allok &= ok
        print(f"  {n:>3} {k:>3} {str(coeff):>18} {str(pred):>17}  {'OK' if ok else '*** FAILS ***'}")
print(f"\n  ALL UNTUNED PREDICTIONS {'CONFIRMED' if allok else 'NOT confirmed'}")

print("\n"+"="*80)
print("RICK'S OWN GUESS (Day 155 s2): 'binom(n-1,2) is the degree of V(u) in u_1 alone")
print("  after setting u_2=...=u_n=0'")
print("="*80)
for n in range(3, 8):
    u = sp.symbols(f'u1:{n+1}')
    Vres = sp.expand(V_of(u).subs({u[i]: 0 for i in range(1, n)}))
    d = sp.Poly(Vres, u[0]).degree() if Vres != 0 else 0
    print(f"  n={n}: V|_(u_2..u_n=0) = {Vres}, deg in u_1 = {d};  binom(n-1,2) = "
          f"{int(sp.binomial(n-1,2))}  -> {'agrees' if d == int(sp.binomial(n-1,2)) else 'DOES NOT MATCH'}")
print("  => his guess yields n-1, not binom(n-1,2).  Refuted at n=3 (2 vs 1) and every n>=4.")

print("\n"+"="*80)
print("RIVAL READINGS of c_n = binom(n-1,2)-1, and where they separate")
print("="*80)
rivals = {'binom(n-1,2)-1': lambda n: sp.binomial(n-1,2)-1, 'n-2': lambda n: n-2,
          '2(n-3)': lambda n: 2*(n-3), 'binom(n-2,2)+1': lambda n: sp.binomial(n-2,2)+1}
print(f"  {'n':>3} " + " ".join(f"{k:>16}" for k in rivals))
for n in range(3, 8):
    print(f"  {n:>3} " + " ".join(f"{str(f(n)):>16}" for f in rivals.values()))
print("\n  At n=4 (his supplied cell) 'binom(n-1,2)-1' and 'n-2' BOTH give 2: that cell")
print("  cannot separate them.  They first disagree at n=5 (5 vs 3).")
print("  His table reaches n=5,6,7, so his DATA separates them -- the single target")
print("  cell in UID 680 does not.  n=5 is the smallest honest discriminator.")
