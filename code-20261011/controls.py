"""Negative controls for the Cor 5.2 two-engine test, INCLUDING a deliberately
rank-0 one (operator-order reversal) to measure the test's own symmetry group.
Each control reports the smallest n at which it fires."""
from fractions import Fraction
from itertools import permutations
from ring import *
from ebasis import e_expand, estar, count01
import hl

def engineA(n, m, V, parts, order=None, swap_s=False):
    """order: callable lam -> sequence of k's.  swap_s: s on the complement of A."""
    out = {}
    for lam in parts:
        seq = order(lam) if order else lam
        F = pone(m)
        for k in seq:
            F = E_k_variant(F, k, m, V, swap_s)
        exp = e_expand(F, n, m)
        for mu in parts:
            out[(lam, mu)] = exp.get(mu, {})
    return out

def E_k_variant(F, k, m, V, swap_s):
    if not swap_s: return E_k(F, k, m, V)
    from itertools import combinations
    total = pz()
    for A in combinations(range(m), k):
        As = set(A)
        num = pone(m)
        for i in A:
            for j in range(m):
                if j in As: continue
                num = pmul(num, padd(pvar(i, m), pvar(j, m, cc(-1, 0, 1))))
        sign = 1; cof = pone(m)
        for i in range(m):
            for j in range(i+1, m):
                ini, inj = i in As, j in As
                if ini and not inj: pass
                elif inj and not ini: sign = -sign
                else: cof = pmul(cof, psub(pvar(i, m), pvar(j, m)))
        xA = pone(m)
        for i in A: xA = pmul(xA, pvar(i, m))
        FA = {al: cshift_s(c, sum(al[i] for i in range(m) if i not in As)) for al, c in F.items()}
        term = pmul(pmul(num, cof), pmul(xA, FA))
        if sign < 0: term = pneg(term)
        total = padd(total, term)
    return pdiv_exact(total, V) if not pzero_q(total) else {}

def dA(cdict, parts, use_conj_exp=False):
    out = {}
    for (lam, mu), c in cdict.items():
        e = nstat(conj(mu)) if use_conj_exp else nstat(mu)
        out[(lam, mu)] = {te: v for (se, te), v in c.items() if se == e}
    return out

def dB(C, parts, use_mu=False, no_prefactor=False, no_invert=False, unconj_prefactor=False):
    out = {}
    for lam in parts:
        for mu in parts:
            idx = mu if use_mu else conj(mu)
            c = C.get((lam, idx), {})
            if no_prefactor: sh = 0
            elif unconj_prefactor: sh = nstat(mu) - nstat(lam)
            else: sh = nstat(conj(mu)) - nstat(conj(lam))
            if no_invert: out[(lam, mu)] = {(k + sh): v for k, v in c.items()}
            else:         out[(lam, mu)] = {(-k + sh): v for k, v in c.items()}
    return out

def diff(X, Y, parts):
    return sum(1 for lam in parts for mu in parts if X.get((lam, mu), {}) != Y.get((lam, mu), {}))

RESULTS = {}
for n in range(2, 6):
    m = n; V = vandermonde(m); parts = list(partitions(n))
    base = engineA(n, m, V, parts)
    C, _ = hl.e_in_P(n, m)
    ref_A = dA(base, parts); ref_B = dB(C, parts)
    tests = {
      "BASELINE (A vs B)":                 (ref_A, ref_B),
      "C1 B uses P_mu not P_mu'":          (ref_A, dB(C, parts, use_mu=True)),
      "C2 B drops t-prefactor":            (ref_A, dB(C, parts, no_prefactor=True)),
      "C3 B uses P(x;t) not P(x;1/t)":     (ref_A, dB(C, parts, no_invert=True)),
      "C4 B prefactor n(mu)-n(lam)":       (ref_A, dB(C, parts, unconj_prefactor=True)),
      "C5 A extracts [s^n(mu')]":          (dA(base, parts, use_conj_exp=True), ref_B),
      "C6 A: s on complement of A":        (dA(engineA(n,m,V,parts,swap_s=True), parts), ref_B),
      "C7 A: operators in REVERSED order": (dA(engineA(n,m,V,parts,order=lambda l: tuple(reversed(l))), parts), ref_B),
    }
    for name, (X, Y) in tests.items():
        RESULTS.setdefault(name, {})[n] = diff(X, Y, parts)

print(f"{'control':40s} " + "  ".join(f"n={n}" for n in range(2,6)))
for name, row in RESULTS.items():
    print(f"{name:40s} " + "  ".join(f"{row[n]:3d}" for n in range(2,6)))

# C7 is expected rank-0: verify ALL orderings of the parts agree, not just reversal
print("\n--- rank of operator-order controls: do ALL orderings of lam agree? ---")
for n in (4, 5):
    m = n; V = vandermonde(m); parts = list(partitions(n))
    worst = 0
    for lam in parts:
        vals = set()
        for perm in set(permutations(lam)):
            F = pone(m)
            for k in perm: F = E_k(F, k, m, V)
            exp = e_expand(F, n, m)
            vals.add(tuple(sorted((mu, tuple(sorted(c.items()))) for mu, c in exp.items())))
        worst = max(worst, len(vals))
    print(f"  n={n}: max # distinct results over all orderings of the parts of lam = {worst}  (1 => order is a SYMMETRY)")
