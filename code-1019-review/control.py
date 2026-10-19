"""POSITIVE CONTROL for lemmas.py: plant realistic-but-wrong variants and
confirm the SAME comparison code reports failures. A green test on a blind
harness is worth nothing (10-17: an inadmissible plant and a blind instrument
both produce silence)."""
import sympy as sp
from engine import W, phi0, F, geq, subsets

def e0(n, M, lesion=None):
    u = W[n]; Mm = [c for c in M if c != n]
    v = (1 - u**-2)
    for c in Mm: v *= (1 - 1/(W[c]*u))
    for k in range(1, n):
        if k not in Mm: v *= (1 - W[k]/u)
    if lesion == 'e0_drop_k_filter':   # drop the "k notin M^-" filter
        v = (1 - u**-2)
        for c in Mm: v *= (1 - 1/(W[c]*u))
        for k in range(1, n): v *= (1 - W[k]/u)
    return v

def run_L1(exp_shift=0, lesion=None):
    bad = 0; tot = 0
    n = 4
    for kappa in subsets(n):
        if n not in kappa: continue
        for M in subsets(n):
            if n not in M or len(M) < len(kappa): continue
            Mm = tuple(c for c in M if c != n); km = tuple(c for c in kappa if c != n)
            u = W[n]; tot += 1
            pre = u**(n + exp_shift)
            for c in Mm: pre *= W[c]**2
            d = sp.simplify(sp.together(F(kappa, M) - e0(n, M, lesion)*pre*F(km, Mm)))
            if d != 0: bad += 1
    return bad, tot

def run_L2(sign_flip=False, drop_last=False):
    bad = 0; tot = 0
    n = 4; u = W[n]
    for kappa in subsets(n-1):
        if not kappa: continue
        kr = kappa[-1]; km = kappa[:-1]
        K = sp.Integer(-1)**(kr + (1 if sign_flip else 0))
        rng = range(1, kr) if not drop_last else range(1, max(1, kr-1))
        for k in rng: K *= W[k]
        for M in subsets(n):
            if n not in M or len(M) < len(kappa): continue
            Mm = tuple(c for c in M if c != n); tot += 1
            lhs = sp.simplify(sp.limit(sp.together(u*F(kappa, M)), u, 0))
            if sp.simplify(sp.together(lhs - K*F(km, Mm))) != 0: bad += 1
    return bad, tot

print("ARM 0 (faithful)        L1 :", run_L1(), " <- must be (0, >0)")
print("ARM 1 (u^n -> u^{n-1})  L1 :", run_L1(exp_shift=-1), " <- must fire")
print("ARM 2 (drop k-filter)   L1 :", run_L1(lesion='e0_drop_k_filter'), " <- must fire")
print("ARM 0 (faithful)        L2 :", run_L2(), " <- must be (0, >0)")
print("ARM 3 (K sign flipped)  L2 :", run_L2(sign_flip=True), " <- must fire")
print("ARM 4 (K prod truncated)L2 :", run_L2(drop_last=True), " <- must fire")
