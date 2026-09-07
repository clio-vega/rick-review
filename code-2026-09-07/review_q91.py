"""Peer-review verification of proofs/2026-09-06-c2-Q91-fermionic-normal-form.tex, Theorem 1.

Written fresh for the review.  The SHAPE engine below is my own; it imports
nothing from probes/2026-09-06-Q84/engine.py.  Only bead.py (the fermionic
side) is reused, because the point is to re-test the theorem, not the code.

Tests
  A  Theorem 1:  shape engine  ==  bead engine.
  B  Jordan-Wigner reading:  the dressing (-t)^{N_(b,b+e)} is the RATIO of a
     half-infinite string D_a = (-t)^{#{j<a : j in M}} at the two endpoints.
  C  Is R_e(t) a DIAGONAL GAUGE TRANSFORM of alpha_{-e}?  Equivalent to
     path-independence of total spin.  (If yes, Theorem 1 is a triviality.)
  D  Is R_e(t) a fermion BILINEAR (an element of gl_infty-hat, i.e. of the
     Bloch-Okounkov "bounded strip" algebra) for any t?
"""
import sys, itertools
sys.path.insert(0, '/home/clio/projects/probes/2026-09-06-c2-Q91')
import sympy as sp
from bead import R_bead, trim, maya, from_maya, t

# ------------------------------------------------------ SHAPE ENGINE (mine)
def partitions_upto(n):
    out = [()]
    def rec(rem, mx, cur):
        if rem == 0:
            out.append(tuple(cur)); return
        for k in range(min(rem, mx), 0, -1):
            rec(rem - k, k, cur + [k])
    for m in range(1, n + 1):
        rec(m, m, [])
    return out

def cells(lam):
    return {(i, j) for i, r in enumerate(lam) for j in range(r)}

def is_partition(mu):
    return all(mu[i] >= mu[i+1] for i in range(len(mu)-1)) and all(x > 0 for x in mu)

def border_strips(lam, e):
    """All mu > lam with mu/lam a connected border strip of size e.
    Returns list of (mu, height) with height = (#rows of the strip) - 1."""
    lam = trim(lam)
    res = []
    maxrow = len(lam) + e
    # enumerate mu by choosing row lengths >= lam, total added = e
    def rec(i, added, cur):
        if added == e:
            # CRITICAL: copy lam's remaining rows, else mu need not contain lam
            mu = trim(tuple(cur) + tuple(lam[i:]))
            if not is_partition(mu):
                return
            S = cells(mu) - cells(lam)
            if len(S) != e:
                return
            # connected (edge-adjacency)?
            start = next(iter(S)); seen = {start}; stack = [start]
            while stack:
                (a, b) = stack.pop()
                for (da, db) in ((1,0),(-1,0),(0,1),(0,-1)):
                    q = (a+da, b+db)
                    if q in S and q not in seen:
                        seen.add(q); stack.append(q)
            if seen != S:
                return
            # no 2x2 square  <=> border strip
            for (a, b) in S:
                if (a+1,b) in S and (a,b+1) in S and (a+1,b+1) in S:
                    return
            rows = len({a for (a, b) in S})
            res.append((mu, rows - 1))
            return
        if i >= maxrow or added > e:
            return
        lo = lam[i] if i < len(lam) else 0
        for new in range(lo, lo + (e - added) + 1):
            rec(i + 1, added + (new - lo), cur + [new])
    rec(0, 0, [])
    return res

def R_shape(lam, e):
    out = {}
    for mu, h in border_strips(lam, e):
        out[mu] = sp.expand(out.get(mu, 0) + t**h)
    return {k: v for k, v in out.items() if sp.expand(v) != 0}

# ---------------------------------------------------------------- TEST A
def testA(emax=6, nmax=8):
    bad = 0; tot = 0
    for e in range(2, emax + 1):
        for lam in partitions_upto(nmax):
            a, b = R_shape(lam, e), R_bead(lam, e)
            tot += 1
            if a != b:
                bad += 1
                if bad <= 3:
                    print("   MISMATCH", e, lam, a, b)
    print(f"A  Theorem 1  shape==bead:  {tot-bad}/{tot}  (e<=%d, |lam|<=%d)" % (emax, nmax))
    return bad == 0

# ---------------------------------------------------------------- TEST B
def testB(emax=6, nmax=8):
    r"""String ratio identity:
         #{j<b+e : j in M\{b}}  -  #{j<b : j in M}   ==   #{b<j<b+e : j in M}
       for every VALID move (b in M, b+e not in M).  Counted from a finite
       cutoff lo; the divergent tails are identical and cancel."""
    bad = 0; tot = 0
    for e in range(2, emax + 1):
        for lam in partitions_upto(nmax):
            lam = trim(lam)
            lo = -(len(lam) + 2*e + 6)
            M = maya(lam, lo)
            hi = (lam[0] if lam else 0) + 2*e + 6
            for b in range(lo, hi + 1):
                if b not in M or b + e in M:
                    continue
                Mp = (M - {b})
                left  = sum(1 for j in range(lo, b + e) if j in Mp)
                right = sum(1 for j in range(lo, b)     if j in M)
                N     = sum(1 for j in range(b + 1, b + e) if j in M)
                tot += 1
                if left - right != N:
                    bad += 1
    print(f"B  Jordan-Wigner string ratio == N_(b,b+e):  {tot-bad}/{tot} moves")
    return bad == 0

# ---------------------------------------------------------------- TEST C
def testC(e=2, nmax=8):
    """Is there a diagonal G with R_e(t) = G alpha_{-e} G^{-1} ?
    That needs g(mu)/g(lam) = (-t)^{ht(mu/lam)} for EVERY e-ribbon move,
    i.e. total spin must be path-independent.  Look for two paths
    emptyset -> lam with different total height."""
    reach = {(): [0]}          # lam -> set of achievable total heights
    order = sorted(partitions_upto(nmax), key=lambda p: sum(p))
    witnesses = []
    for lam in order:
        if sum(lam) % e:
            continue
        if lam not in reach and lam != ():
            continue
        hs = reach.get(lam)
        if hs is None:
            continue
        for mu, h in border_strips(lam, e):
            if sum(mu) > nmax:
                continue
            reach.setdefault(mu, [])
            for x in hs:
                if x + h not in reach[mu]:
                    reach[mu].append(x + h)
    for lam, hs in sorted(reach.items(), key=lambda kv: (sum(kv[0]), kv[0])):
        if len(set(hs)) > 1:
            witnesses.append((lam, sorted(set(hs))))
    if witnesses:
        lam, hs = witnesses[0]
        print(f"C  spin is PATH-DEPENDENT: smallest witness lam={lam}, e={e}, "
              f"total heights {hs}  =>  NO diagonal G with R_e = G alpha_-e G^-1")
    else:
        print("C  spin path-independent up to |lam|<=%d -- gauge transform NOT excluded" % nmax)
    return witnesses

# ---------------------------------------------------------------- TEST D
def testD(e=2, nmax=7):
    """A fermion bilinear X = sum a_{ij} E_{ij} has matrix coefficient
    <mu|X|lam> = a_{b+e,b} * (fermionic sign) = a_{b+e,b} * (-1)^{ht}, with
    a independent of lam.  R_e(t) has coefficient t^{ht}.  So R_e(t) is a
    bilinear iff (-t)^{ht} is independent of ht over the moves sharing a
    given b -- i.e. iff t = -1.  Test: for each b, collect the heights that
    actually occur."""
    from collections import defaultdict
    occ = defaultdict(set)
    for lam in partitions_upto(nmax):
        lam = trim(lam)
        lo = -(len(lam) + 2*e + 6)
        M = maya(lam, lo)
        hi = (lam[0] if lam else 0) + 2*e + 6
        for b in range(lo, hi + 1):
            if b not in M or b + e in M:
                continue
            N = sum(1 for j in range(b + 1, b + e) if j in M)
            occ[b].add(N)
    multi = {b: sorted(v) for b, v in occ.items() if len(v) > 1}
    if multi:
        b0 = sorted(multi)[0]
        print(f"D  site b={b0} carries heights {multi[b0]} => a_{{b+e,b}} would have to "
              f"equal (-t)^h for two different h; forces (-t)^{multi[b0][0]}=(-t)^{multi[b0][1]}, i.e. t=-1.")
        print(f"   ({len(multi)} sites with >1 height, e={e}, |lam|<={nmax})")
    else:
        print("D  no site carries two heights in range -- inconclusive")
    return multi

if __name__ == '__main__':
    ok = testA(emax=6, nmax=8)
    testB(emax=6, nmax=8)
    testC(e=2, nmax=8)
    testC(e=3, nmax=9)
    testD(e=2, nmax=7)
    testD(e=3, nmax=8)
