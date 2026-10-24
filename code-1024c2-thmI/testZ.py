"""Test Rick's Theorem Z against independently computed Hilbert polynomials.
Clio 2026-10-23 peer review."""
from fractions import Fraction
from itertools import combinations, product
import sys, time
from demazure import (min_rep, reduced_word, chi, strict_partitions,
                      subset_of_kappa, dim_V, lagrange)
from comb import D, rprime, contains, admissible_BRprime

def H_poly(kappa, m, verbose=False):
    """H_kappa(j) as a Lagrange interpolator, from |kappa|+1 values at j=0..|kappa|.
    For j>=0, chi = h^0 (Kempf vanishing), and H is a polynomial of degree |kappa| (Snapper)."""
    d = sum(kappa)
    full = tuple(range(m, 0, -1))
    if kappa == full:
        # X_kappa = LG itself; chi(O(j)) = dim V_{j omega_m}: Weyl dimension formula,
        # a route completely independent of the Demazure operators.
        pts = [(j, dim_V(j, m)) for j in range(d+1)]
    else:
        w = min_rep(subset_of_kappa(kappa, m), m); word = reduced_word(w, m)
        pts = [(j, chi(word, [j]*m, m)) for j in range(d+1)]
    return lagrange(pts), pts

# ---------------- BR Corollary 5.6 at p=1, read first-hand from kpieri.tex -----
def klg_count_p1(theta):
    """# KLG-tableaux of shape theta with content {1}: labels in {1'<1}, encoded 0=1', 1=1.
    (i) rows strictly increasing  (ii) columns strictly increasing
    (iii),(iv) the SW conditions: VACUOUS for p=1 (1 is the max, 1' is the min)
    (v) no diagonal box is primed."""
    boxes = sorted(theta)
    n = len(boxes)
    idx = {b: i for i, b in enumerate(boxes)}
    cnt = 0
    for assign in product((0, 1), repeat=n):
        ok = True
        for i, (r, c) in enumerate(boxes):
            if r == c and assign[i] == 0:          # (v)
                ok = False; break
        if not ok: continue
        for i, a in enumerate(boxes):
            for jj, b in enumerate(boxes):
                if a[0] == b[0] and a[1] < b[1] and not (assign[i] < assign[jj]):
                    ok = False; break            # (i)
                if a[1] == b[1] and a[0] < b[0] and not (assign[i] < assign[jj]):
                    ok = False; break            # (ii)
            if not ok: break
        if ok: cnt += 1
    return cnt

def is_rim(theta):
    return all(not (b[0] > a[0] and b[1] > a[1]) for a in theta for b in theta)

def c_BR(lam, nu, m):
    """c^nu_{lam,1} for K(LG(m,2m)) -- BR Cor 5.6 (= (-1)^{|theta|-1} * #KLG-tableaux),
    and 0 unless lam subsetneq nu and theta is a rim (BR Thm 5.5)."""
    if lam == nu or not contains(nu, lam): return 0
    theta = D(nu, m) - D(lam, m)
    if not theta: return 0
    if not is_rim(theta): return 0
    return (-1)**(len(theta)-1) * klg_count_p1(theta)

def dual(kappa, m):
    s = set(kappa)
    return tuple(sorted((x for x in range(1, m+1) if x not in s), reverse=True))

M_MAX = int(sys.argv[1]) if len(sys.argv) > 1 else 4
for m in range(2, M_MAX+1):
    print(f"\n{'='*78}\n  m = {m}   LG({m},{2*m})   dim = {m*(m+1)//2}\n{'='*78}")
    ks = strict_partitions(m)
    t0 = time.time()
    POLY = {}; PTS = {}
    for k in ks:
        POLY[k], PTS[k] = H_poly(k, m)
    print(f"  computed {len(ks)} Hilbert polynomials in {time.time()-t0:.1f}s")

    # ---- sanity: values at j=0..3 are positive integers, H(0)=1 ----
    bad = [k for k in ks if PTS[k][0][1] != 1]
    print(f"  sanity H_kappa(0)=1 : violations = {len(bad)}")

    # ---- TEST 1: the ANCHOR (Thm C vanishing half) H_kappa(-3/2)=0 iff l(kappa)>=2 ----
    print(f"\n  -- TEST 1: anchor.  H_kappa(-3/2) = 0  <=>  l(kappa) >= 2 ?")
    ok = bad2 = 0
    for k in ks:
        v = POLY[k](Fraction(-3, 2))
        want = (len(k) >= 2)
        if (v == 0) == want: ok += 1
        else: bad2 += 1; print(f"     MISMATCH kappa={k} l={len(k)} H(-3/2)={v}")
    print(f"     {ok}/{len(ks)} agree, {bad2} mismatches")

    # ---- TEST 2: Theorem Z's CONCLUSION on the whole window ----
    print(f"\n  -- TEST 2: Theorem Z.  H_kappa(-M/2)=0 for odd M in [3, 2*ceil(r'/2)+1]")
    tot = 0; viol = []
    for k in ks:
        rp = rprime(k, m); top = 2*((rp+1)//2) + 1
        for M in range(3, top+1, 2):
            tot += 1
            v = POLY[k](Fraction(-M, 2))
            if v != 0: viol.append((k, rp, M, v))
    print(f"     window points tested = {tot}, NONZERO (violations) = {len(viol)}")
    for x in viol[:6]: print(f"       kappa={x[0]} r'={x[1]} M={x[2]} H={x[3]}")

    # ---- TEST 2b: SHARPNESS -- the first point BEYOND the window ----
    print(f"\n  -- TEST 2b: sharpness.  is H_kappa(-(M*+2)/2) != 0 at M* = 2*ceil(r'/2)+1 ?")
    nz = z = 0; zz = []
    for k in ks:
        if len(k) < 2: continue
        rp = rprime(k, m); Mn = 2*((rp+1)//2) + 3
        v = POLY[k](Fraction(-Mn, 2))
        if v != 0: nz += 1
        else: z += 1; zz.append((k, rp, Mn))
    print(f"     nonzero just past the window: {nz};  still zero: {z}" +
          (f"  e.g. {zz[:4]}" if zz else "   -> window is EXACTLY right"))

    # ---- TEST 3: STEP 1 identity, b_kappa(j) = sum_rho c_rho H_rho(j) ----
    print(f"\n  -- TEST 3: Step 1.  b_kappa(j) := H_kappa(j)-H_kappa(j-1) = sum_rho c_rho H_rho(j)")
    print(f"     with c_rho = c^{{rho^vee}}_{{kappa^vee,1}} from BR Cor 5.6 (first-hand), transported by Lemma S")
    nfail = 0; nchk = 0; supp_viol = []
    for k in ks:
        lam = dual(k, m)
        terms = []
        for rho in ks:
            nu = dual(rho, m)
            c = c_BR(lam, nu, m)
            if c: terms.append((rho, c))
        # check the polynomial identity at many points, incl. half-integers
        okk = True
        for t in range(-8, 9):
            jj = Fraction(t, 2)
            lhs = POLY[k](jj) - POLY[k](jj-1)
            rhs = sum(Fraction(c) * POLY[rho](jj) for rho, c in terms)
            if lhs != rhs: okk = False; break
        nchk += 1
        if not okk:
            nfail += 1
            print(f"     IDENTITY FAILS kappa={k}: terms={terms}")
        # and the support claim Lemma Ch needs: r'(rho) >= r'(kappa)-2
        for rho, c in terms:
            if rprime(rho, m) < rprime(k, m) - 2:
                supp_viol.append((k, rho, rprime(k, m), rprime(rho, m)))
    print(f"     identity holds for {nchk-nfail}/{nchk} kappa")
    print(f"     support claim r'(rho) >= r'(kappa)-2 over the TRUE support: violations = {len(supp_viol)}")
    # report the alternation Rick claims
    alt = []
    for k in ks:
        lam = dual(k, m)
        for rho in ks:
            nu = dual(rho, m)
            c = c_BR(lam, nu, m)
            if c:
                th = D(nu, m) - D(lam, m)
                alt.append(c == (-1)**(len(th)-1) * abs(c) and True)
    print(f"     nonzero Pieri coefficients: {len(alt)}")
