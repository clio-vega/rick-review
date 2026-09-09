"""Independent check of Rick's Day180 §3: ht_e(b,M) = #{c in M: b<c<b+e}
   is the HEIGHT (=rows-1=leg length) of the e-ribbon added by the bead move b -> b+e.
   Built from scratch: Maya set -> partition -> skew cells -> count rows.
   No import of Rick's code, no import of Clio's abacus.py."""
from itertools import combinations

def maya_to_partition(M, cutoff=40):
    """M subset of Z, charge 0 (finite symmetric difference with Z_{<0}).
    Bead at position c  <->  c = lambda_i - i  for some i (1-indexed)."""
    beads = sorted([c for c in M if c > -cutoff], reverse=True)
    lam = []
    for i, c in enumerate(beads):          # i = 0,1,2,... ; row index i+1
        part = c + (i + 1)
        lam.append(part)
    while lam and lam[-1] == 0:
        lam.pop()
    return tuple(lam)

def cells(lam):
    return {(r, c) for r, L in enumerate(lam) for c in range(L)}

def charge0_maya(lam, cutoff=40):
    M = set(range(-cutoff, 0))            # vacuum: negatives
    lam = list(lam)
    for i in range(len(lam) + cutoff):
        li = lam[i] if i < len(lam) else 0
        pos = li - (i + 1)
        M.discard(-(i + 1)); M.add(pos)
    return M

fails = 0; checks = 0; range_bad = 0
# enumerate all partitions in a box, all e, all legal moves
def parts(n, maxpart):
    if n == 0: yield (); return
    for k in range(min(n, maxpart), 0, -1):
        for rest in parts(n - k, k):
            yield (k,) + rest

for n in range(0, 13):
  for lam in parts(n, 8):
    M = charge0_maya(lam)
    for e in range(1, 7):
      for b in sorted(M):
        if b + e in M or b < -20: continue
        Mp = (M - {b}) | {b + e}
        mu = maya_to_partition(Mp)
        if sum(mu) != sum(lam) + e:   # not a legal add of an e-ribbon
            continue
        skew = cells(mu) - cells(lam)
        if len(skew) != e: continue
        rows = len({r for r, c in skew})
        ht_geom = rows - 1
        ht_bead = len([c for c in M if b < c < b + e])
        checks += 1
        if ht_geom != ht_bead:
            fails += 1
            if fails <= 5:
                print(f"  MISMATCH lam={lam} e={e} b={b}: geom rows-1={ht_geom}, beads={ht_bead}")
        if not (0 <= ht_bead <= e - 1):
            range_bad += 1

print(f"checks={checks}  height-mismatches={fails}  range-violations={range_bad}")
