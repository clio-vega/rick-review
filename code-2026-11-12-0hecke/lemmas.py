"""
Lemma checks for Rick's Part II.
 (1) Lemma II.6: connected C => top X_C simple, label D_C = {i : i,i+1 same row of T0},
     functional = [T = T0].
 (2) Cor II.7: top multiplicity-free of size 2^(m-1).
 (3) Lemma II.8 (support) LESION: last component Ch is (a) non-ribbon, (b) ribbon with >=2 rows,
     (c) one row.  Rick's hypothesis is (a); his proof only uses ">= 2 rows".
 (4) KLO Thm 5.5's proof infers the shape from row lengths + column lengths (per component).
     Check that map is injective on basic skew shapes, n <= 8.
"""
import itertools, sys
import numpy as np
sys.path.insert(0, '.')
from hecke0 import P, nullspace
from thmB import connected_shapes, star, tableau_module, is_ribbon, cells_of


def top_functionals(M):
    n, d = M.n, M.d
    mats = [np.array(M.mat(i), dtype=np.int64) for i in range(n - 1)]
    out = {}
    for mask in range(1 << (n - 1)):
        eqs = []
        for i in range(n - 1):
            lam = (mask >> i) & 1
            A = mats[i].T.copy()          # f A = lam f  <=>  A^T f^T = lam f^T
            A[np.arange(d), np.arange(d)] -= lam
            eqs.extend((A % P).tolist())
        ns = nullspace(eqs, d)
        if ns:
            out[frozenset(i + 1 for i in range(n - 1) if (mask >> i) & 1)] = ns
    return out


def T0_of(rows):
    T = {}; v = 1
    for (r, c) in cells_of(rows):
        T[(r, c)] = v; v += 1
    return T


conn = {s: connected_shapes(s) for s in range(1, 8)}

# ---- (1) Lemma II.6
bad = 0; tot = 0
for s in range(1, 7):
    for C in conn[s]:
        M, Ts = tableau_module(cells_of(C))
        tf = top_functionals(M)
        T0 = T0_of(C)
        DC = frozenset(T0[x] for x in T0 if (x[0], x[1] + 1) in T0)
        k0 = [k for k, T in enumerate(Ts) if T == T0]
        ok = (list(tf) == [DC] and len(tf[DC]) == 1 and
              [j for j, x in enumerate(tf[DC][0]) if x] == k0)
        tot += 1; bad += (not ok)
print(f"(1) Lemma II.6: connected shapes n<=6: {tot}, failures {bad}")

# ---- (2) Cor II.7
bad = tot = 0
for comps in [c for s1 in range(1, 4) for s2 in range(1, 4) for s3 in range(1, 3)
              for c in itertools.product(conn[s1], conn[s2], conn[s3])][:120]:
    cells, parts = star(list(comps))
    M, Ts = tableau_module(cells)
    tf = top_functionals(M)
    ok = len(tf) == 4 and all(len(v) == 1 for v in tf.values())
    tot += 1; bad += (not ok)
for comps in [c for s1 in range(1, 5) for s2 in range(1, 4) for c in itertools.product(conn[s1], conn[s2])]:
    cells, parts = star(list(comps))
    M, Ts = tableau_module(cells)
    tf = top_functionals(M)
    ok = len(tf) == 2 and all(len(v) == 1 for v in tf.values())
    tot += 1; bad += (not ok)
print(f"(2) Cor II.7: {tot} shapes with m=2,3, failures {bad}")

# ---- (3) Lemma II.8 lesion
def support_check(comps):
    """return (#functional-k pairs tested, #violations of (i), #violations of (ii))"""
    cells, parts = star(list(comps))
    M, Ts = tableau_module(cells)
    a = len(cells)
    Ch = parts[-1]
    bottom = max(r for r, c in Ch)
    lastrow = sorted([x for x in Ch if x[0] == bottom], key=lambda x: x[1])
    llast = len(lastrow)
    tf = top_functionals(M)
    tested = vi = vii = 0
    for D, fs in tf.items():
        eps = fs[0]
        k = 1
        while k + 1 <= a and all(j in D for j in range(a - k, a)):  # [a-(k+1)+1, a-1]
            k += 1
        for kk in range(1, k + 1):
            tested += 1
            if kk > llast:
                vi += 1; continue
            target = set(lastrow[-kk:])
            for j, x in enumerate(eps):
                if x:
                    T = Ts[j]
                    if set(c for c, v in T.items() if v > a - kk) != target:
                        vii += 1; break
    return tested, vi, vii

for label, pred in [("(a) non-ribbon Ch", lambda C: not is_ribbon(C)),
                    ("(b) ribbon Ch, >=2 rows", lambda C: is_ribbon(C) and len(C) >= 2),
                    ("(c) one-row Ch", lambda C: len(C) == 1)]:
    T = VI = VII = shapes = 0; fail_shapes = []
    for s1 in range(1, 4):
        for s2 in range(1, 6):
            if s1 + s2 > 7:
                continue
            for C1 in conn[s1]:
                for Ch in conn[s2]:
                    if not pred(Ch):
                        continue
                    t, vi, vii = support_check([C1, Ch])
                    T += t; VI += vi; VII += vii; shapes += 1
                    if vi or vii:
                        fail_shapes.append((C1, Ch))
    print(f"(3) Lemma II.8 {label}: {shapes} shapes, {T} (eps,k) tests, (i) fails {VI}, (ii) fails {VII};"
          f" e.g. {fail_shapes[:1]}")

# ---- (4) KLO Thm 5.5 row/col injectivity
def normalize(cells):
    r0 = min(r for r, c in cells); c0 = min(c for r, c in cells)
    return frozenset((r - r0, c - c0) for r, c in cells)

def rows_cols(cells):
    rows = {}; cols = {}
    for r, c in cells:
        rows[r] = rows.get(r, 0) + 1; cols[c] = cols.get(c, 0) + 1
    return tuple(rows[r] for r in sorted(rows)), tuple(cols[c] for c in sorted(cols))

for n in range(1, 9):
    seen = {}; coll = 0; nshapes = 0
    conn_n = {s: connected_shapes(s) for s in range(1, n + 1)}
    def comps_lists(left):
        if left == 0:
            yield []
            return
        for s in range(1, left + 1):
            for C in conn_n[s]:
                for rest in comps_lists(left - s):
                    yield [C] + rest
    for comps in comps_lists(n):
        cells, parts = star(comps)
        sh = normalize(cells)
        # per-component row and column length sequences, components in NE->SW order
        inv = tuple(rows_cols(p) for p in parts)
        nshapes += 1
        if inv in seen and seen[inv] != sh:
            coll += 1
        seen[inv] = sh
    print(f"(4) n={n}: {nshapes} basic shapes, row+col invariant collisions {coll}")
