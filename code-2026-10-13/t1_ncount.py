"""
TEST 1 (cheap, decisive): Rick's eq:ncount, longversion.tex l.~597 (commit 33526fc)

    n(kappa) - n(rho) = C(k,2) + inv(kappa/rho) + sum_v r_v (m_v - r_v)       (*)

with  inv(kappa/rho) = sum_{v<w} r_v (m_w(kappa) - r_w),  m_v = m_v(kappa),
      r_v = # rows of kappa of length v ending in a box of the vertical k-strip.

This single identity is the load-bearing step of the proof of Theorem H(2):
it is what converts the explicit weight of H(3) into
      t^{n(kappa)-n(rho)-C(k,2)} psi'_{kappa/rho}(t^{-1}).

CONTROL: re-run with inv read in the SMALLER partition, m_w(rho) instead of
m_w(kappa).  Macdonald's psi/psi' conventions differ on exactly this point, so a
check that does not separate the two readings has not checked anything.
We also report how many strips are "symmetric" (both readings agree) -- those
cases are blind to the distinction.
"""
from itertools import product

def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: yield (); return
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n-k, k):
            yield (k,) + rest

def nstat(lam):                      # n(lambda) = sum (i-1) lambda_i
    return sum(i*p for i, p in enumerate(lam))

def mult(lam):
    m = {}
    for p in lam:
        if p: m[p] = m.get(p, 0) + 1
    return m

def vertical_strips(kappa):
    """All (rho, k, r) with kappa/rho a vertical k-strip, via Rick's own
    parametrisation: lower r_v of the parts of kappa equal to v, for each v.
    'Lower' = decrease by exactly 1.  Returns rho sorted, k=sum r_v, dict r."""
    m = mult(kappa)
    vals = sorted(m)
    out = []
    for choice in product(*[range(m[v]+1) for v in vals]):
        r = {v: c for v, c in zip(vals, choice) if c}
        k = sum(r.values())
        if k == 0: continue
        rho = []
        for v in vals:
            c = r.get(v, 0)
            rho += [v]*(m[v]-c) + [v-1]*c
        rho = tuple(sorted([p for p in rho if p > 0], reverse=True))
        out.append((rho, k, r))
    return out

def is_vertical_strip(kappa, rho):
    """Independent predicate: kappa/rho is a vertical strip iff rho subset kappa
    and kappa'_i - rho'_i in {0,1} for all i  <=>  kappa_i - rho_i in {0,1} is
    WRONG; the right statement is on the conjugate.  Use columns."""
    def conj(l):
        return tuple(sum(1 for p in l if p > j) for j in range(l[0] if l else 0))
    ck, cr = conj(kappa), conj(rho)
    cr = cr + (0,)*(len(ck)-len(cr))
    if len(cr) > len(ck): return False
    # vertical strip: each ROW of kappa/rho has at most one box  <=>  kappa_i - rho_i <= 1
    rr = list(rho) + [0]*(len(kappa)-len(rho))
    if len(rho) > len(kappa): return False
    return all(0 <= a-b <= 1 for a, b in zip(kappa, rr))

def check(nmax):
    tot = good = 0
    ctrl_tot = ctrl_fail = 0
    blind = 0
    asym_examples = []
    strip_pred_mismatch = 0
    for n in range(1, nmax+1):
        for kappa in partitions(n):
            mk = mult(kappa)
            for rho, k, r in vertical_strips(kappa):
                if not is_vertical_strip(kappa, rho):
                    strip_pred_mismatch += 1
                mr = mult(rho)
                inv_K = sum(r.get(v,0)*(mk.get(w,0)-r.get(w,0))
                            for v in mk for w in mk if v < w)
                inv_R = sum(r.get(v,0)*(mr.get(w,0)-r.get(w,0))
                            for v in mk for w in mk if v < w)
                rhs_K = k*(k-1)//2 + inv_K + sum(r[v]*(mk[v]-r[v]) for v in r)
                rhs_R = k*(k-1)//2 + inv_R + sum(r[v]*(mk[v]-r[v]) for v in r)
                lhs = nstat(kappa) - nstat(rho)
                tot += 1
                if lhs == rhs_K: good += 1
                else:
                    print("  FAIL (kappa)", kappa, rho, r, lhs, rhs_K)
                if inv_K == inv_R:
                    blind += 1
                else:
                    ctrl_tot += 1
                    if lhs != rhs_R:
                        ctrl_fail += 1
                        if len(asym_examples) < 4:
                            asym_examples.append((kappa, rho, dict(r), lhs, rhs_K, rhs_R))
    return tot, good, blind, ctrl_tot, ctrl_fail, asym_examples, strip_pred_mismatch

if __name__ == "__main__":
    NMAX = 11
    tot, good, blind, ct, cf, ex, mism = check(NMAX)
    print("DOMAIN: all kappa |- n for 1 <= n <= %d; all vertical strips kappa/rho." % NMAX)
    print("eq:ncount with inv read in KAPPA : %d / %d" % (good, tot))
    print("strip-parametrisation cross-check (independent predicate) mismatches: %d" % mism)
    print()
    print("CONTROL, inv read in RHO (the wrong Macdonald convention):")
    print("  strips where the two readings COINCIDE (test is blind here): %d" % blind)
    print("  strips where they DIFFER (asymmetric witnesses)            : %d" % ct)
    print("  of those, eq:ncount FAILS under the rho-reading            : %d / %d" % (cf, ct))
    print()
    print("smallest asymmetric witnesses (kappa, rho, r, lhs, rhs_kappa, rhs_rho):")
    for e in ex: print("   ", e)
