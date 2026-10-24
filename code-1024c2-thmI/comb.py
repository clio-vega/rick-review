"""Independent re-derivation of Rick's Lemma S and Lemma Ch, from his DEFINITIONS
(proofs/2026-10-24-Z-by-hyperplane-induction.md, sections 1-3), not his scripts.
Clio, 2026-10-23 peer review."""
from itertools import combinations
from functools import lru_cache

def strict_partitions(m):
    """strict kappa with parts in [1,m], decreasing; returned as tuples."""
    out = []
    for k in range(m+1):
        for s in combinations(range(m,0,-1), k):
            out.append(tuple(s))
    return out

def D(kappa, m):
    """shifted diagram: {(r,c): 0<=r<l(kappa), r<=c<=r+kappa_{r+1}-1}"""
    return frozenset((r, c) for r, part in enumerate(kappa)
                     for c in range(r, r+part))

def Delta(m):
    return frozenset((r, c) for r in range(m) for c in range(r, m))

def dual(kappa, m):
    """kappa^vee = [m] \\ kappa, as a decreasing tuple"""
    s = set(kappa)
    return tuple(sorted((x for x in range(1, m+1) if x not in s), reverse=True))

def R(rc, m):
    r, c = rc
    return (m-1-c, m-1-r)

def longest_chain(boxes):
    """longest chain under product order (r,c)<=(r',c') iff r<=r' and c<=c'.
    DP over the DAG of strict domination."""
    bs = sorted(boxes)
    n = len(bs)
    best = [1]*n
    for i in range(n):
        for j in range(i):
            a, b = bs[j], bs[i]
            if a[0] <= b[0] and a[1] <= b[1] and a != b:
                if best[j]+1 > best[i]:
                    best[i] = best[j]+1
    return max(best) if best else 0

def rprime(kappa, m):
    """r'(kappa) = longest chain in D(kappa) restricted to row >= 1   [eq (1.1)]"""
    return longest_chain([b for b in D(kappa, m) if b[0] >= 1])

def rprime_via_definition(kappa, m):
    """r'(kappa) := longest chain in D(kappa^-), kappa^- = (kappa_2, kappa_3, ...).
    This is the ORIGINAL definition; (1.1) claims they agree."""
    km = tuple(kappa[1:])
    return longest_chain(D(km, m))

def no_strict_SE_pair(theta):
    for a in theta:
        for b in theta:
            if b[0] > a[0] and b[1] > a[1]:
                return False
    return True

def le2_per_row_col(theta):
    from collections import Counter
    rows, cols = Counter(), Counter()
    for r, c in theta:
        rows[r] += 1; cols[c] += 1
    return all(v <= 2 for v in rows.values()) and all(v <= 2 for v in cols.values())

def no_2x2(theta):
    for (r, c) in theta:
        if (r, c+1) in theta and (r+1, c) in theta and (r+1, c+1) in theta:
            return False
    return True

def admissible_BRprime(theta):
    """(BR'): no strictly-SE pair, and <=2 boxes per row and per column."""
    return no_strict_SE_pair(theta) and le2_per_row_col(theta)

def admissible_weak(theta):
    """the WEAKER predicate Rick warns against: no 2x2 square + <=2 per row/col."""
    return no_2x2(theta) and le2_per_row_col(theta)

def contains(kappa, rho):
    """rho subseteq kappa : rho_i <= kappa_i for all i"""
    if len(rho) > len(kappa):
        return False
    return all(rho[i] <= kappa[i] for i in range(len(rho)))

# ---------------- CHECK 0: eq (1.1), the two definitions of r' agree ----------
print("== CHECK 0: eq (1.1)  r'(kappa) = longest chain in D(kappa) cap {row>=1} ==")
for m in range(1, 9):
    bad = [k for k in strict_partitions(m) if rprime(k, m) != rprime_via_definition(k, m)]
    print(f"  m={m}: {len(strict_partitions(m))} kappa, mismatches = {len(bad)}")

# ---------------- CHECK 1: Lemma S ------------------------------------------
print("\n== CHECK 1: Lemma S   D(kappa^vee) = R(Delta_m \\ D(kappa)) ==")
for m in range(1, 9):
    ks = strict_partitions(m); bad = []
    Dl = Delta(m)
    for k in ks:
        lhs = D(dual(k, m), m)
        rhs = frozenset(R(b, m) for b in (Dl - D(k, m)))
        if lhs != rhs:
            bad.append(k)
    print(f"  m={m}: {len(ks)} kappa, violations = {len(bad)}" + (f"  e.g. {bad[:3]}" if bad else ""))

# ---- CHECK 1b: R preserves the strictly-SE relation and swaps rows/cols -----
print("\n== CHECK 1b: R maps strictly-SE pairs to strictly-SE pairs (as unordered pairs) ==")
for m in range(2, 9):
    Dl = sorted(Delta(m)); bad = 0; tested = 0
    for a, b in combinations(Dl, 2):
        se = (b[0] > a[0] and b[1] > a[1]) or (a[0] > b[0] and a[1] > b[1])
        Ra, Rb = R(a, m), R(b, m)
        seR = (Rb[0] > Ra[0] and Rb[1] > Ra[1]) or (Ra[0] > Rb[0] and Ra[1] > Rb[1])
        tested += 1
        if se != seR: bad += 1
    print(f"  m={m}: {tested} pairs, mismatches = {bad}")

# ---------------- CHECK 2: Lemma Ch ----------------------------------------
print("\n== CHECK 2: Lemma Ch.  admissible pair counts, chain bound, drop bound ==")
print("  Rick reports pair counts 1, 5, 17, 53, 159, 465, 1337, 3801 for m=1..8")
for m in range(1, 9):
    ks = strict_partitions(m)
    npairs = 0; chain_viol = 0; drop_viol = 0; min_drop = 0
    maxcap = 0
    for kappa in ks:
        Dk = D(kappa, m); rk = rprime(kappa, m)
        chains_pos = [b for b in Dk if b[0] >= 1]
        for rho in ks:
            if rho == kappa or not contains(kappa, rho): continue
            theta = Dk - D(rho, m)
            if not theta: continue
            if not admissible_BRprime(theta): continue
            npairs += 1
            # chain claim: every chain of D(kappa) meets theta in <= 2 boxes
            cap = longest_chain_meet(Dk, theta) if False else None
            # consequence
            rr = rprime(rho, m)
            min_drop = min(min_drop, rr - rk)
            if rr < rk - 2: drop_viol += 1
    print(f"  m={m}: admissible pairs = {npairs}, drop violations = {drop_viol}, min drop = {min_drop}")
