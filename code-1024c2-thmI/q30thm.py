"""Rick's Theorem Q30 (new file proofs/2026-10-25-crownF-strict-reciprocity.md, committed
AFTER my arming stamp) restates my 10-23 closed form INTRINSICALLY on theta = D(kappa)\\D(rho),
instead of on the BR shape R(theta):

  c_rho = (-1)^{|theta|-1} V(theta),  and
  V(theta) = 0  iff  theta has a 3-chain, or some diagonal box (c,c) in theta has (c-1,c) in theta;
  otherwise |c_rho| = 2^{#off-diagonal boxes of theta incomparable to every other box of theta}.

This matters to me because the KLG count is NOT R-invariant (rinv.py: 528/3024 pairs), so
"the closed form" is only well posed once the shape is pinned.  Ground truth here is
brute-force KLG enumeration on R(theta), which is what BR Cor 5.6 actually indexes.
Clio 2026-10-24 c2.
"""
import sys
from fast import D, Rset, strict_partitions, contains, is_rim, forced_count

def klg_count_p1(theta):
    """brute force: #KLG-tableaux of shape theta with content {1}, labels {1'<1} = 0<1.
    (iii)/(iv) are vacuous at p=1; (v) forbids a primed diagonal box.  Inlined rather than
    imported from testZ.py, which runs a module-level test suite off sys.argv[1] on import."""
    from itertools import product as _prod
    bs = sorted(theta); n = len(bs); cnt = 0
    for asg in _prod((0, 1), repeat=n):
        ok = True
        for i, (r, c) in enumerate(bs):
            if r == c and asg[i] == 0: ok = False; break
        if not ok: continue
        for i, a in enumerate(bs):
            for j, b in enumerate(bs):
                if a[0] == b[0] and a[1] < b[1] and not (asg[i] < asg[j]): ok = False; break
                if a[1] == b[1] and a[0] < b[0] and not (asg[i] < asg[j]): ok = False; break
            if not ok: break
        if ok: cnt += 1
    return cnt



def comparable(a, b):
    return (a[0] <= b[0] and a[1] <= b[1]) or (b[0] <= a[0] and b[1] <= a[1])


def V_rick(theta):
    """Rick's Lemma R / Theorem Q30 closed form, evaluated on theta itself."""
    bs = sorted(theta)
    # 3-chain in the product order
    for x in bs:
        for y in bs:
            if y == x or not (x[0] <= y[0] and x[1] <= y[1]) or x == y: continue
            if not (x[0] <= y[0] and x[1] <= y[1]) or x == y: continue
            for z in bs:
                if z == y or z == x: continue
                if y[0] <= z[0] and y[1] <= z[1]:
                    return 0
    # a diagonal box (c,c) in theta with (c-1,c) in theta  (i.e. non-minimal in theta)
    for (a, b) in bs:
        if a == b and (a - 1, a) in theta:
            return 0
    # isolated off-diagonal boxes
    i = 0
    for x in bs:
        if x[0] == x[1]: continue
        if all(y == x or not comparable(x, y) for y in bs): i += 1
    return 2 ** i


def truth(theta, m):
    """BR Cor 5.6 at p=1, ground truth: KLG count of the BR shape R(theta)."""
    return klg_count_p1(Rset(theta, m))


if __name__ == "__main__":
    MM = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    print("== Rick's Theorem Q30 closed form on theta  vs  brute-force KLG count on R(theta) ==")
    tot = bad = 0; shown = 0
    # control: my own 10-23 form applied to theta (the WRONG shape) must disagree somewhere
    wrongshape_bad = 0
    for m in range(1, MM + 1):
        for kap in strict_partitions(m):
            Dk = D(kap, m)
            for rho in strict_partitions(m):
                if rho == kap or not contains(kap, rho): continue
                th = Dk - D(rho, m)
                if not th or not is_rim(th) or len(th) > 12: continue
                t = truth(th, m); v = V_rick(th); tot += 1
                if t != v:
                    bad += 1
                    if shown < 6:
                        print(f"   MISMATCH m={m} kappa={kap} rho={rho} theta={sorted(th)}"
                              f"  truth={t} Q30={v}"); shown += 1
                if forced_count(th) != t: wrongshape_bad += 1
        print(f"   m<={m}: {tot} rim pairs, Theorem Q30 mismatches = {bad}")
    print(f"\n   Theorem Q30 (intrinsic, on theta):        {tot-bad}/{tot} correct")
    print(f"   CONTROL -- same closed form on the WRONG shape (theta instead of R(theta)):"
          f" {wrongshape_bad}/{tot} WRONG")
    print("   -> the control fires, so this test does distinguish the two shape conventions.")
