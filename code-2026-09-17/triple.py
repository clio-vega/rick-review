"""SEPARATOR for the support coincidence.

Rule S ("conjugate of the classical Schur support"): support of e_a*e_b*e_c in the
    e-basis = conjugates of the Schur support of e_a e_b e_c  (i.e. {mu : c^{mu'}_{1^a,1^b,1^c} > 0}).
Rule D ("two-row -> l-row dominance interval"): support = ALL mu with <= 3 rows,
    |mu| = n, mu dominates sort(a,b,c).

For two factors these agree (both give min(a,b)+1 two-row shapes). For THREE they
need not.  Compute the truth with my own implementation and see which survives.

  e_a * e_b * e_c = t^{-[a(a-1)+b(b-1)+c(c-1)]/2} * ( e_a(Y) e_b(Y) e_c(Y) . 1 )
(from Hikita line 267:  q(e_lambda(Y)) = t^{sum l_i(l_i-1)/2} e^{(q,t)}_lambda(X) )
"""
from hikita_star_clio import *
import sys, itertools

def star_many(parts, m=None):
    n = sum(parts)
    if m is None: m = n
    A = {tuple([0]*m): ONE}
    for p in sorted(parts):            # Y-operators commute, order irrelevant
        A = e_Y(p, A, m)
    A = scal((ONE/t)**sum(p*(p-1)//2 for p in parts), A)
    return expand_in_e(A, n, m), m

def dominates(mu, nu):
    s1 = s2 = 0
    for i in range(max(len(mu), len(nu))):
        s1 += mu[i] if i < len(mu) else 0
        s2 += nu[i] if i < len(nu) else 0
        if s1 < s2: return False
    return True

# LR: Schur support of e_a e_b e_c = s_{1^a} s_{1^b} s_{1^c} via iterated dual Pieri
def dual_pieri(supp, k):
    """multiply each s_lam by e_k = s_{1^k}: add a vertical strip of size k"""
    out = {}
    for lam in supp:
        L = list(lam) + [0]*(k+1)
        for add_set in itertools.product([0,1], repeat=len(L)):
            if sum(add_set) != k: continue
            new = [L[i]+add_set[i] for i in range(len(L))]
            if any(new[i] < new[i+1] for i in range(len(new)-1)): continue
            # vertical strip: no two added boxes in same row is automatic; need skew vertical strip
            ok = all(new[i] - L[i] <= 1 for i in range(len(L)))
            if not ok: continue
            # horizontal-strip complement condition for vertical strip: L[i] >= new[i+1]
            if any(L[i] < new[i+1] for i in range(len(new)-1)): continue
            nz = tuple(x for x in new if x > 0)
            out[nz] = out.get(nz, 0) + 1
    return out

cases = [(1,1,1),(2,1,1),(2,2,1),(2,2,2),(3,2,1)]
for parts in cases:
    n = sum(parts)
    co, m = star_many(list(parts))
    truth = sorted(co.keys(), reverse=True)
    # Rule S
    supp = {(): 1}
    cur = {(0,): 1}
    cur = {(): 1}
    S = {(): 1}
    for p in parts: S = dual_pieri(S.keys(), p)
    ruleS = sorted({tuple(reversed(sorted(l))) for l in S}, reverse=True)
    ruleS_conj = sorted({tuple(sum(1 for x in lam if x > j) for j in range(lam[0])) for lam in S if lam}, reverse=True)
    # Rule D
    base = tuple(sorted(parts, reverse=True))
    ruleD = sorted([mu for mu in partitions(n) if len(mu) <= len(parts) and dominates(mu, base)], reverse=True)
    print("\n=== e_%s (m=%d): |lambda|=%d ===" % (" * e_".join(map(str,parts)), m, n))
    print("  TRUTH (my compute) :", truth)
    print("  Rule S (conj Schur):", ruleS_conj)
    print("  Rule D (dominance) :", ruleD)
    print("  S correct? %s    D correct? %s" % (ruleS_conj == truth, ruleD == truth))
    sys.stdout.flush()
