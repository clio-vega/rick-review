"""
Theorem B / Corollary C check on KLO tableau modules X_{lambda/mu} (KLO App. A rule):
  pi_i T = T (i strictly left of i+1), 0 (same column), s_i T (i strictly right of i+1).
Prediction (Rick Cor C): number of indecomposable summands t = prod over maximal runs of r
consecutive ribbon components of 2^(r-1).  Thm B = the case t = 1.
Also: Lemma II.6 (simple top D_C for connected C), Cor II.7 (top multiplicity-free, size
2^(m-1)), and a lesion study of Lemma II.8 (support) with the last component Ch replaced by
(a) a non-ribbon, (b) a ribbon with >= 2 rows, (c) a one-row ribbon.
"""
import itertools, sys, time
import numpy as np
sys.path.insert(0, '.')
from hecke0 import P, Module, endomorphisms, summand_count, nullspace, rank


# ------------------------------------------------------------------ shapes
def connected_shapes(s):
    """connected skew shapes of size s as tuple of rows (start,end) inclusive, top to bottom,
    min start 0.  Going down: start, end weakly decrease; consecutive rows overlap."""
    out = set()

    def rec(rows, left):
        if left == 0:
            mn = min(r[0] for r in rows)
            out.add(tuple((a - mn, b - mn) for a, b in rows))
            return
        a0, b0 = rows[-1]
        for L in range(1, left + 1):
            # new row (a,b): b <= b0, a <= a0, overlap: a0 <= b ; b-a+1 = L
            for b in range(a0, b0 + 1):
                a = b - L + 1
                if a <= a0:
                    rec(rows + [(a, b)], left - L)
    for L in range(1, s + 1):
        rec([(0, L - 1)], s - L)
    return sorted(out)


def cells_of(rows, r0=0, c0=0):
    return [(r0 + i, c0 + c) for i, (a, b) in enumerate(rows) for c in range(a, b + 1)]


def width(rows):
    return max(b for a, b in rows) - min(a for a, b in rows) + 1


def star(comps):
    """C1 * C2 * ... : C1 north-east.  Return list of cells (row, col), and the cell lists
    of each component."""
    widths = [width(C) for C in comps]
    cells, parts = [], []
    r0 = 0
    for j, C in enumerate(comps):
        c0 = sum(widths[j + 1:])          # components further south-west sit to the left
        cs = cells_of(C, r0, c0)
        parts.append(cs); cells += cs
        r0 += len(C)
    return cells, parts


def is_ribbon(rows):
    cs = set(cells_of(rows))
    return not any((r, c) in cs and (r + 1, c) in cs and (r, c + 1) in cs and (r + 1, c + 1) in cs
                   for (r, c) in cs)


def syt(cells):
    cs = set(cells)
    pred = {x: [y for y in [(x[0] - 1, x[1]), (x[0], x[1] - 1)] if y in cs] for x in cells}
    res = []
    n = len(cells)

    def rec(T, placed, v):
        if v > n:
            res.append(dict(T)); return
        for x in cells:
            if x not in placed and all(p in placed for p in pred[x]):
                T[x] = v; placed.add(x)
                rec(T, placed, v + 1)
                placed.discard(x); del T[x]
    rec({}, set(), 1)
    return res


def tableau_module(cells):
    Ts = syt(cells); n = len(cells)
    key = lambda T: tuple(sorted(T.items()))
    idx = {key(T): k for k, T in enumerate(Ts)}
    act = []
    for i in range(1, n):
        col = []
        for T in Ts:
            inv = {v: x for x, v in T.items()}
            (ri, ci), (rj, cj) = inv[i], inv[i + 1]
            if ci == cj:
                col.append([])
            elif ci < cj:
                col.append([(1, idx[key(T)])])
            else:
                T2 = dict(T); T2[inv[i]] = i + 1; T2[inv[i + 1]] = i
                col.append([(1, idx[key(T2)])])
        act.append(col)
    return Module(len(Ts), n, act), Ts


def predicted_t(comps):
    rib = [is_ribbon(C) for C in comps]
    t = 1; run = 0
    for r in rib + [False]:
        if r:
            run += 1
        else:
            if run:
                t *= 2 ** (run - 1)
            run = 0
    return t


def hyp_B(comps):
    rib = [is_ribbon(C) for C in comps]
    return len(comps) >= 2 and not any(rib[j] and rib[j + 1] for j in range(len(comps) - 1))


def count_summands(comps, nv_cap):
    cells, parts = star(comps)
    M, Ts = tableau_module(cells)
    sizes = [len(p) for p in parts]
    best = None
    for j in range(1, len(comps)):
        a = sum(sizes[:j])
        first = set(c for p in parts[:j] for c in p)
        gens = [k for k, T in enumerate(Ts) if all((T[x] <= a) == (x in first) for x in T)]
        nv = len(gens) * M.d
        if best is None or nv < best[0]:
            best = (nv, a, gens)
    nv, a, gens = best
    if nv > nv_cap:
        return None, M.d
    from math import comb
    assert M.d == comb(len(cells), a) * len(gens) // 1 or True
    # Ind certificate: d = binom(n,a) * dim V
    assert M.d == comb(len(cells), a) * len(gens), "dim M != index * dim V"
    B_idx = [i - 1 for i in range(1, len(cells)) if i != a]
    E = endomorphisms(M, gens, B_idx)
    return (summand_count(E), len(E)), M.d


if __name__ == '__main__':
    nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    nv_cap = int(sys.argv[2]) if len(sys.argv) > 2 else 1200
    MIXED = (len(sys.argv) > 3 and sys.argv[3] == 'mixed')
    nmin = int(sys.argv[4]) if len(sys.argv) > 4 else 2
    conn = {s: connected_shapes(s) for s in range(1, nmax + 1)}
    print("connected shapes per size:", {s: len(v) for s, v in conn.items()})
    t0 = time.time()
    stats = dict(total=0, skipped=0, mism=0, hypB=0, hypB_ok=0, ctrl=0, ctrl_split=0)
    for n in range(nmin, nmax + 1):
        # compositions of n into m>=2 component sizes
        for m in range(2, n + 1):
            for sizes in itertools.product(range(1, n + 1), repeat=m):
                if sum(sizes) != n:
                    continue
                for comps in itertools.product(*[conn[s] for s in sizes]):
                    if MIXED and n > 5 and all(is_ribbon(C) for C in comps):
                        continue
                    res, d = count_summands(list(comps), nv_cap)
                    if res is None:
                        stats['skipped'] += 1; continue
                    t, dimEnd = res
                    pt = predicted_t(comps)
                    stats['total'] += 1
                    if hyp_B(comps):
                        stats['hypB'] += 1; stats['hypB_ok'] += (t == 1)
                    else:
                        stats['ctrl'] += 1; stats['ctrl_split'] += (t >= 2)
                    if t != pt:
                        stats['mism'] += 1
                        print("MISMATCH", comps, "t", t, "pred", pt, "dimEnd", dimEnd)
        print(f"n<={n}: {stats}  {time.time()-t0:.0f}s", flush=True)
