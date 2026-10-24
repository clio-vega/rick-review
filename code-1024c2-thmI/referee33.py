"""REFEREE of Rick's Sec. 3.3 (UID 850: "Two steps are hand-written and I have re-read them
only once: Sec. 3.3 ... Please referee those two.").

Sec. 3.3 proves  T(phi) = C(phi,1),  i.e. BR Cor 5.6 at p=1, by induction against BR Thm 5.5
-- the step that lets him drop the reader-left Cor 5.6.  My review's F2 leans on it.

This refereees the CONCLUSION independently: I implement BR's recursion C(theta,p) straight
from Thm 5.5 (thm:pieriCrec, lines 1439-1466 of kpieri.tex), which BR prove in full, and
compare it against brute-force KLG-tableau enumeration.  The two engines share nothing: one is
an alternating recursion on the north-east arm, the other enumerates labellings.

BR definitions used (kpieri.tex lines 1051-1060, verbatim):
  "If theta is a non-empty rim, then we define the NORTH-EAST ARM of theta to be the largest
   row or column that can be obtained by intersecting theta with a square whose upper-right box
   agrees with the upper-right box of theta.  We let theta-hat be the diagram obtained by
   removing the north-east arm from theta.  Notice that theta is a row or a column if and only
   if theta-hat is empty."

Clio 2026-10-24 c2.
"""
import sys
from functools import lru_cache
from itertools import product, combinations


def strict_partitions(m):
    out = []
    for k in range(m + 1):
        for s in combinations(range(m, 0, -1), k):
            out.append(tuple(s))
    return out


def D(kappa):
    return frozenset((i, i + j) for i, k in enumerate(kappa) for j in range(k))


def is_rim(theta):
    return all(not (b[0] > a[0] and b[1] > a[1]) for a in theta for b in theta)


def is_row(theta):
    return len({b[0] for b in theta}) == 1


def is_col(theta):
    return len({b[1] for b in theta}) == 1


def meets_diagonal(theta):
    return any(a == b for (a, b) in theta)


def upper_right_box(theta):
    """top row, and within it the rightmost box.  For a rim this is BR's upper-right box:
    nothing of theta lies above or to the right of it (Rick's (g3))."""
    r = min(b[0] for b in theta)
    c = max(b[1] for b in theta if b[0] == r)
    return (r, c)


def ne_arm(theta):
    """BR's north-east arm, implemented LITERALLY: range over squares whose upper-right box is
    B = (r,c), namely [r, r+k] x [c-k, c]; keep those intersections that are a row or a column;
    return the largest.  (Maximum over all k -- not a greedy run, which is a different thing.)"""
    r, c = upper_right_box(theta)
    best = frozenset({(r, c)})
    n = len(theta)
    for k in range(0, n + 1):
        sq = frozenset((r + i, c - j) for i in range(k + 1) for j in range(k + 1))
        inter = frozenset(theta) & sq
        if not inter:
            continue
        if (is_row(inter) or is_col(inter)) and len(inter) > len(best):
            best = inter
    return best


def adjacent(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1]) == 1


def connected(psi, hat):
    return any(adjacent(x, y) for x in psi for y in hat)


@lru_cache(maxsize=None)
def C(theta, p):
    """BR Thm 5.5, implemented from the statement.  theta a frozenset of boxes."""
    if not theta:
        return 1 if p <= 0 else 0
    if not is_rim(theta):
        return 0
    if p <= 0:
        return 0                      # theta non-empty
    psi = ne_arm(theta)
    hat = frozenset(theta) - psi
    a = len(theta) - len(hat)
    n = len(theta)
    if not hat:                                              # theta is a row or a column
        if meets_diagonal(theta):                            # (i)
            if is_col(theta):
                return (1 if p == n else 0) - (1 if p == n - 1 else 0)
            return 1 if p == n else 0
        return 2 * (1 if p == n else 0) - (1 if p == n - 1 else 0)   # (ii)
    if connected(psi, hat):                                  # (iii)
        return C(hat, p - a) - C(hat, p - a + 1)
    if a == 1:                                               # (iv), a = 1
        return 2 * C(hat, p - a) - 2 * C(hat, p - a + 1)
    return 2 * C(hat, p - a) - 3 * C(hat, p - a + 1) + C(hat, p - a + 2)   # (iv), a > 1


def klg_count_p1(theta):
    """brute force #KLG-tableaux of shape theta, content {1}: labels {1'<1} = 0<1, rows and
    columns strictly increasing, no primed diagonal box.  (iii)/(iv) vacuous at p=1."""
    bs = sorted(theta); n = len(bs); cnt = 0
    for asg in product((0, 1), repeat=n):
        ok = True
        for i, (r, c) in enumerate(bs):
            if r == c and asg[i] == 0:
                ok = False; break
        if not ok: continue
        for i, x in enumerate(bs):
            for j, y in enumerate(bs):
                if x[0] == y[0] and x[1] < y[1] and not (asg[i] < asg[j]): ok = False; break
                if x[1] == y[1] and x[0] < y[0] and not (asg[i] < asg[j]): ok = False; break
            if not ok: break
        if ok: cnt += 1
    return cnt


def T(theta):
    """BR Cor 5.6 at p = 1:  c = (-1)^{|theta|-1} * #KLG-tableaux."""
    return (-1) ** (len(theta) - 1) * klg_count_p1(theta)


def shapes(nmax):
    """all non-empty shifted skew diagrams D(nu)\\D(lam), lam subset nu strict, nu_1 <= n"""
    out = set()
    for n in range(1, nmax + 1):
        ps = strict_partitions(n)
        for nu in ps:
            Dn = D(nu)
            for lam in ps:
                if len(lam) > len(nu): continue
                if any(lam[i] > nu[i] for i in range(len(lam))): continue
                Dl = D(lam)
                if not Dl <= Dn: continue
                th = Dn - Dl
                if th: out.add(frozenset(th))
    return out


if __name__ == "__main__":
    NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    print("== REFEREE of Sec. 3.3:  T(phi) = C(phi,1)  (BR Cor 5.6 at p=1, reader-left in BR) ==")
    print("   engine A: BR Thm 5.5 recursion on the north-east arm (proved in full in BR)")
    print("   engine B: brute-force KLG-tableau enumeration")
    S = sorted(shapes(NMAX), key=lambda s: (len(s), sorted(s)))
    tot = bad = rims = nonrims = 0
    shown = 0
    for th in S:
        if len(th) > 13: continue
        a = C(th, 1); b = T(th); tot += 1
        if is_rim(th): rims += 1
        else: nonrims += 1
        if a != b:
            bad += 1
            if shown < 8:
                print(f"   MISMATCH {sorted(th)}  C(phi,1)={a}  T(phi)={b}"); shown += 1
    print(f"   shifted skew shapes with nu_1 <= {NMAX}: {tot} ({rims} rims, {nonrims} non-rims)")
    print(f"   agreements: {tot-bad}/{tot}   mismatches: {bad}")

    # NEGATIVE CONTROL: perturb the recursion and confirm the comparison fires.
    print("\n== NEGATIVE CONTROL: break Thm 5.5 case (iv) (a=1 coefficient 2 -> 1) ==")
    global_bad = 0
    import referee33 as me
    orig = me.C
    @lru_cache(maxsize=None)
    def Cbad(theta, p):
        if not theta: return 1 if p <= 0 else 0
        if not is_rim(theta): return 0
        if p <= 0: return 0
        psi = ne_arm(theta); hat = frozenset(theta) - psi
        a = len(theta) - len(hat); n = len(theta)
        if not hat:
            if meets_diagonal(theta):
                if is_col(theta): return (1 if p==n else 0) - (1 if p==n-1 else 0)
                return 1 if p==n else 0
            return 2*(1 if p==n else 0) - (1 if p==n-1 else 0)
        if connected(psi, hat): return Cbad(hat,p-a) - Cbad(hat,p-a+1)
        if a == 1: return 1*Cbad(hat,p-a) - 2*Cbad(hat,p-a+1)      # <-- BROKEN
        return 2*Cbad(hat,p-a) - 3*Cbad(hat,p-a+1) + Cbad(hat,p-a+2)
    for th in S:
        if len(th) > 13: continue
        if Cbad(th, 1) != T(th): global_bad += 1
    v = "FIRES" if global_bad else "*** SILENT -- the comparison cannot fail ***"
    print(f"   broken recursion disagrees on {global_bad}/{tot} shapes  -> {v}")
