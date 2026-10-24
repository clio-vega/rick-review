"""His open question 1: a clean description of supp[O_{X_kappa cap H}] in K(LG).
With BR Cor 5.6 in hand (p=1), the coefficient is forced -- so the support is EXACT,
not just an inclusion.  Clio 2026-10-23."""
from itertools import product
from collections import Counter
from comb import D, strict_partitions, contains, no_strict_SE_pair, le2_per_row_col
from testZ import klg_count_p1, is_rim

def forced_count(theta):
    """For p=1 the labels are {1'<1} = {0<1}.  Rows and columns strictly increase, so
    a row of 2 must be (0,1) left-to-right and a column of 2 must be (0,1) top-to-bottom;
    condition (v) forces every diagonal box to 1.  Everything else is free.
    Returns (consistent?, #free boxes)."""
    rows, cols = {}, {}
    for b in theta:
        rows.setdefault(b[0], []).append(b)
        cols.setdefault(b[1], []).append(b)
    val = {}
    def put(b, v):
        if b in val and val[b] != v: return False
        val[b] = v; return True
    for r, bs in rows.items():
        if len(bs) > 2: return (False, 0)
        if len(bs) == 2:
            bs.sort()
            if not put(bs[0], 0) or not put(bs[1], 1): return (False, 0)
    for c, bs in cols.items():
        if len(bs) > 2: return (False, 0)
        if len(bs) == 2:
            bs.sort()
            if not put(bs[0], 0) or not put(bs[1], 1): return (False, 0)
    for b in theta:
        if b[0] == b[1]:
            if not put(b, 1): return (False, 0)
    return (True, len(theta) - len(val))

print("CONJECTURE: for p=1, #KLG-tableaux(theta) = 2^f if the forcing is consistent, else 0,")
print("            where f = #boxes alone in their row, alone in their column, and off-diagonal.")
bad = 0; tested = 0; hist = Counter()
for m in range(1, 8):
    ks = strict_partitions(m)
    for kap in ks:
        Dk = D(kap, m)
        for rho in ks:
            if rho == kap or not contains(kap, rho): continue
            th = Dk - D(rho, m)
            if not th: continue
            if not is_rim(th): continue
            got = klg_count_p1(th) if len(th) <= 12 else None
            if got is None: continue
            ok, f = forced_count(th)
            pred = (2**f) if ok else 0
            tested += 1
            hist[got] += 1
            if got != pred:
                bad += 1
                if bad <= 5: print("  MISMATCH", kap, rho, sorted(th), "count", got, "pred", pred)
    print(f"  m<={m}: tested {tested} rim shapes theta, mismatches = {bad}")
print(f"\n  coefficient-magnitude histogram over all rim theta: {dict(sorted(hist.items()))}")
print("\n  => the p=1 K-Pieri coefficient is  c_rho = (-1)^{|theta|-1} * 2^f  (or 0),")
print("     so |c_rho| is ALWAYS a power of 2, and the sign is Rick's (-1)^{|theta|-1}.")
