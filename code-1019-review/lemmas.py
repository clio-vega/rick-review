"""Independent symbolic test of Rick's local lemmas L1, L2, L3 (D-inf sec.5)
and the two exact reduction identities (A4, B4), from my own (2.1) engine."""
import sympy as sp
from itertools import combinations
from engine import W, phi0, F, T0, geq, subsets

def e0(n, M):
    """e^0_n(M) := (1-u^-2) prod_{c in M^-}(1-1/(w_c u)) prod_{k<n, k notin M^-}(1-w_k/u)"""
    u = W[n]; Mm = [c for c in M if c != n]
    v = (1 - u**-2)
    for c in Mm: v *= (1 - 1/(W[c]*u))
    for k in range(1, n):
        if k not in Mm: v *= (1 - W[k]/u)
    return v

print("=== L1 (forced head, EXACT): n in kappa, n in M ===")
bad = []
for n in (3, 4):
    for kappa in subsets(n):
        if n not in kappa: continue
        for M in subsets(n):
            if n not in M or len(M) < len(kappa): continue
            Mm = tuple(c for c in M if c != n); km = tuple(c for c in kappa if c != n)
            u = W[n]; r = len(kappa)
            d1 = sp.simplify(sp.together(phi0(kappa, M) - e0(n, M)*phi0(km, Mm)))
            pre = u**n
            for c in Mm: pre *= W[c]**2
            d2 = sp.simplify(sp.together(F(kappa, M) - e0(n, M)*pre*F(km, Mm)))
            if d1 != 0 or d2 != 0: bad.append((n, kappa, M, d1, d2))
print(f"  n=3,4 all (kappa,M) with n in both: failures = {len(bad)}  {bad[:3]}")

print("=== L2 (u->0): F_kappa(M) = u^-1 (K_kappa F_{kappa^-}(M^-) + O(u)) ===")
print("    K_kappa = (-1)^{kappa_r} prod_{k<kappa_r} w_k   [kappa subset [n-1], kappa != empty]")
bad = []
for n in (3, 4):
    u = W[n]
    for kappa in subsets(n-1):
        if not kappa: continue
        kr = kappa[-1]; km = kappa[:-1]
        K = sp.Integer(-1)**kr
        for k in range(1, kr): K *= W[k]
        for M in subsets(n):
            if n not in M or len(M) < len(kappa): continue
            Mm = tuple(c for c in M if c != n)
            lhs = sp.simplify(sp.limit(sp.together(u*F(kappa, M)), u, 0))
            rhs = sp.simplify(K*F(km, Mm))
            if sp.simplify(sp.together(lhs - rhs)) != 0: bad.append((n, kappa, M, lhs, rhs))
print(f"  n=3,4: failures = {len(bad)}  {bad[:3]}")

print("=== L2 EXTENSION claimed only in the PROOF, not the statement: kappa_r = n ===")
bad = []
for n in (3, 4):
    u = W[n]
    for kappa in subsets(n):
        if not kappa or kappa[-1] != n: continue
        kr = kappa[-1]; km = kappa[:-1]
        K = sp.Integer(-1)**kr
        for k in range(1, kr): K *= W[k]
        for M in subsets(n):
            if n not in M or len(M) < len(kappa): continue
            Mm = tuple(c for c in M if c != n)
            lhs = sp.simplify(sp.limit(sp.together(u*F(kappa, M)), u, 0))
            rhs = sp.simplify(K*F(km, Mm))
            if sp.simplify(sp.together(lhs - rhs)) != 0: bad.append((n, kappa, M))
print(f"  n=3,4, kappa_r = n: failures = {len(bad)}  {bad[:5]}")

print("=== L3 (u->infty): phi0_kappa(M) -> phi0_{kappa^-}(M^-) ===")
bad = []
for n in (3, 4):
    u = W[n]
    for kappa in subsets(n-1):
        if not kappa: continue
        km = kappa[:-1]
        for M in subsets(n):
            if n not in M or len(M) < len(kappa): continue
            Mm = tuple(c for c in M if c != n)
            lhs = sp.simplify(sp.limit(sp.together(phi0(kappa, M)), u, sp.oo))
            rhs = sp.simplify(phi0(km, Mm))
            if sp.simplify(sp.together(lhs-rhs)) != 0: bad.append((n, kappa, M, lhs, rhs))
print(f"  n=3,4: failures = {len(bad)}  {bad[:3]}")

print("=== B4 per-element collapse: w_s^2(1-x/w_s)/(1-x w_s) * (1-1/(w_s x))/(1-w_s/x) * w_s^2 = w_s^2 ===")
x, s = sp.symbols('x s')
lhs = s**2*(1-x/s)/(1-x*s) * (1-1/(s*x))/(1-s/x) * s**2
print("  simplify(LHS - s^2) =", sp.simplify(lhs - s**2))

print("=== A4: e0_n(L)/h = (1-x^2) prod_{s in L''}(1-x/w_s) prod_{k<n, k notin L^-}(1-w_k x)  on H ===")
bad = []
for n in (3, 4, 5):
    for a in range(1, n):
        for L2 in subsets(n-1):
            Lpp = tuple(c for c in L2 if c != a and c < n)
            if a in Lpp: continue
            L = tuple(sorted(Lpp + (a, n)))
            xs = sp.Symbol('x')
            sub = {W[a]: xs, W[n]: 1/xs}
            lhs = sp.simplify(sp.together(e0(n, L).subs(sub) / (1 - 1/(W[a]*W[n])).subs(sub)))
            # that is 0/0; use the cancelled form directly: drop the c=a factor
            u = W[n]; Lm = [c for c in L if c != n]
            v = (1 - u**-2)
            for c in Lm:
                if c != a: v *= (1 - 1/(W[c]*u))
            for k in range(1, n):
                if k not in Lm: v *= (1 - W[k]/u)
            lhs = sp.simplify(v.subs(sub))
            rhs = (1 - xs**2)
            for sS in Lpp: rhs *= (1 - xs/W[sS])
            for k in range(1, n):
                if k not in Lm: rhs *= (1 - W[k]*xs)
            if sp.simplify(sp.together(lhs - rhs)) != 0: bad.append((n, a, L, sp.simplify(lhs-rhs)))
print(f"  n=3,4,5 all (a,L'') : failures = {len(bad)}  {bad[:3]}")
