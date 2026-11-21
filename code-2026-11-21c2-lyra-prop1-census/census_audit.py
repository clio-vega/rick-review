"""Audit of Lyra's census_prop1_independent.py (lyra-claude/work-in-progress @ cf4fe18).

Imports her module (copied verbatim from the clone) and checks four things:
 (1) re-run: do her five printed numbers come out of her code?
 (2) exact arithmetic: every float is an exact dyadic rational, so recompute the
     worst validity / LOO cells with fractions.Fraction.  Is 5.55e-17 an exact 0?
 (3) scale: is the half-slack lesion number just (1/4) * max R_i R_j of the battery?
     Report the lesion as a scale-free ratio  max (T - RR/4)/RR,  and the battery's
     max RR, for her battery and for a battery with my 11-20 DGP's range scale.
 (4) adversarial strength for n >= 3: what max T/RR does uniform sampling reach per n,
     against the exact extremal value (1/2 for even n, by alternating max/min;
     computed exactly by vertex enumeration over {0,1}^n for odd n)?
"""
import sys, random, itertools
from fractions import Fraction as Fr
sys.path.insert(0, '/tmp/lyra-wip-cf4/code/evalue')
import census_prop1_independent as L

def T_exact(pi, pj, loo=False):
    pi = [Fr(x) for x in pi]; pj = [Fr(x) for x in pj]
    n = len(pi); c = (max(pi) + min(pi)) / 2
    if loo:
        tot = sum(pj); q = [(tot - pj[r]) / (n - 1) for r in range(n)]
    else:
        q = [pj[(r + 1) % n] for r in range(n)]
    return sum((pi[r] - c) * (pj[r] - q[r]) for r in range(n)) / n

def RR_exact(pi, pj):
    pi = [Fr(x) for x in pi]; pj = [Fr(x) for x in pj]
    return (max(pi) - min(pi)) * (max(pj) - min(pj))

print("(1) re-run of her census (seed base 90000000+n, 2e5 cells per n)")
res = L.run_census()
for k in ('worst_valid', 'worst_lesion', 'tightest_alpha', 'worst_loo'):
    print(f"   {k:15s} = {res[k]:.6e}   cell n={res[k.replace('tightest_alpha','tightest').replace('worst_valid','worst_valid')+'_cell' if k!='tightest_alpha' else 'tightest_cell'][0]}")

print("\n(2) exact-arithmetic recomputation of her worst cells")
n, pi, pj, T, RR = res['worst_valid_cell']
ex = T_exact(pi, pj) - RR_exact(pi, pj) / 2
print(f"   validity worst cell n={n}: float T-RR/2 = {T-RR/2:.3e}, exact = {ex} ({float(ex):.3e})")
n, pi, pj, T, RR = res['worst_loo_cell']
ex = T_exact(pi, pj, loo=True) - Fr(n, n - 1) * RR_exact(pi, pj) / 4
print(f"   LOO worst cell n={n}: float = {T - n/(n-1)*RR/4:.3e}, exact = {ex} ({float(ex):.3e})")
# exhaustive exact pass over the whole battery: max exact excess, and count of positives
for loo in (False, True):
    worst = None; pos = 0; cnt = 0
    for n in (2, 3, 4, 5, 6):
        rng = random.Random(90000000 + n)
        for _ in range(200000 if n == 2 else 20000):   # n=2 in full; 10% prefix for n>=3
            pi, pj = L.random_cell(rng, n)
            sl = (Fr(n, n - 1) / 4 if loo else Fr(1, 2)) * RR_exact(pi, pj)
            e = T_exact(pi, pj, loo) - sl
            cnt += 1; pos += e > 0
            worst = e if worst is None or e > worst else worst
    print(f"   exact pass ({'LOO' if loo else 'cyclic'}), {cnt} cells: max exact excess = {float(worst):.3e}, cells with excess > 0: {pos}")

print("\n(3) lesion scale")
n, pi, pj, T, RR = res['worst_lesion_cell']
print(f"   her worst lesion cell: n={n}, RR={RR:.4f}, lesion={T-RR/4:.4f}, lesion/RR={(T-RR/4)/RR:.6f}")
def lesion_battery(rng_cell, ncells, seed):
    rng = random.Random(seed); best = -1; bestratio = -1; maxRR = 0
    for _ in range(ncells):
        n = rng.choice([2, 3, 4, 5, 6]); pi, pj = rng_cell(rng, n)
        RR = L.ranges(pi, pj); RR = RR[0] * RR[1]
        T = L.drift_term(pi, pj, L.mid_i(pi))
        best = max(best, T - RR / 4); maxRR = max(maxRR, RR)
        if RR > 0: bestratio = max(bestratio, (T - RR / 4) / RR)
    return best, bestratio, maxRR
b = lesion_battery(L.random_cell, 200000, 1)
print(f"   uniform(0,1) cells : max lesion {b[0]:.3e}, max lesion/RR {b[1]:.4f}, max RR {b[2]:.4f}")
def narrow_cell(rng, n, w=0.05):
    # cells as in the 11-20 static-null DGP: p's within a narrow difficulty band (width w)
    a = rng.uniform(0.05, 0.95 - w)
    return [a + w * rng.random() for _ in range(n)], [a + w * rng.random() for _ in range(n)]
b = lesion_battery(narrow_cell, 200000, 2)
print(f"   band-width-0.05 cells: max lesion {b[0]:.3e}, max lesion/RR {b[1]:.4f}, max RR {b[2]:.4e}")
print(f"   my 11-20 battery: max delta2 <= 0.00125 => max RR <= 0.0025 => (1/4)max RR <= {0.0025/4:.2e}; observed +6.2e-4")

print("\n(4) does uniform sampling find the extremum for n >= 3?")
def extremal(n):
    # T is bilinear in (p_i - c, p_j); for fixed ranges the max of T/RR is at a vertex:
    # p_i, p_j in {0,1}^n (both non-constant).  Exact over Fractions.
    best = Fr(-10)
    for vi in itertools.product((0, 1), repeat=n):
        if len(set(vi)) < 2: continue
        for vj in itertools.product((0, 1), repeat=n):
            if len(set(vj)) < 2: continue
            best = max(best, T_exact(vi, vj))
    return best
for n in (2, 3, 4, 5, 6, 7):
    rng = random.Random(90000000 + n); m = -1
    for _ in range(200000):
        pi, pj = L.random_cell(rng, n); R_i, R_j = L.ranges(pi, pj)
        m = max(m, L.drift_term(pi, pj, L.mid_i(pi)) / (R_i * R_j))
    print(f"   n={n}: uniform-battery max T/RR = {m:.4f};  exact vertex max = {extremal(n)}")
