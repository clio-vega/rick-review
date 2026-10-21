"""(C3-nonsymmetric): simple joint spectrum of the Y_i on Pol_d.
Rick's Day 235 node N_imports_C1_C3_replaced gives the triangular diagonal as
  Y_i  ~  s^{lam_i} t^{b_i},   b_i = #{j : lam_j > lam_i} + #{j < i : lam_j = lam_i}
(lam a composition in m parts), with separating operator Z = sum c^{i-1} Y_i.
I verified the triangularity itself (Thm A.4) 220/220 on 2026-10-12 (UID 380).
What remains is: do distinct compositions give distinct eigenvalue TUPLES?
"""
from itertools import product
import sympy as sp
s, t = sp.symbols('s t', positive=True)

def bvec(lam):
    m = len(lam)
    return tuple(sum(1 for j in range(m) if lam[j] > lam[i])
                 + sum(1 for j in range(m) if j < i and lam[j] == lam[i])
                 for i in range(m))

def spectrum(lam, ss=s, tt=t):
    return tuple(ss**l * tt**b for l, b in zip(lam, bvec(lam)))

print("--- simple joint spectrum, generic (s,t) ---")
for m in range(1, 5):
    for d in range(0, 6):
        lams = [c for c in product(range(d+1), repeat=m) if sum(c) == d]
        seen = {}
        clash = []
        for lam in lams:
            key = spectrum(lam)
            if key in seen:
                clash.append((seen[key], lam))
            seen[key] = lam
        print("  m=%d d=%d : %4d compositions, %4d distinct spectra  %s"
              % (m, d, len(lams), len(seen), "OK" if not clash else "CLASH %s" % clash[:2]))

print("--- positive control: must FAIL when s,t are multiplicatively dependent (s=t) ---")
for m, d in [(2,2),(3,3),(4,4)]:
    lams = [c for c in product(range(d+1), repeat=m) if sum(c) == d]
    seen = {}
    clash = 0
    for lam in lams:
        key = spectrum(lam, ss=t, tt=t)
        if key in seen: clash += 1
        seen[key] = lam
    print("  m=%d d=%d at s=t : %d compositions, %d distinct, %d collisions %s"
          % (m, d, len(lams), len(seen), clash, "(control fires)" if clash else "(CONTROL DEAD)"))

print("--- b_i is a permutation of 0..m-1 (Rick's C3 claim 'b perm of 0..m-1') ---")
bad = []
for m in range(1, 6):
    for d in range(0, 7):
        for lam in product(range(d+1), repeat=m):
            if sum(lam) != d: continue
            if sorted(bvec(lam)) != list(range(m)):
                bad.append((lam, bvec(lam)))
print("  checked m<=5, d<=6 : %s" % ("OK, always a permutation of 0..m-1" if not bad
                                     else "FAIL %s" % bad[:3]))
