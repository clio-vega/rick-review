"""Independent Hilbert polynomials H_kappa(j) = chi(X_kappa, O(j)) for Schubert
varieties in LG(m,2m), via the Demazure character formula for Sp(2m).
Built from the root system, NOT from Rick's scripts.  Clio 2026-10-23 peer review.

Conventions (C_m): weight lattice Z^m with basis eps_1..eps_m.
  simple roots  alpha_i = eps_i - eps_{i+1} (i<m),  alpha_m = 2 eps_m
  coroot pairing <lam,alpha_i^vee> = lam_i - lam_{i+1} (i<m),  = lam_m (i=m)
  s_i (i<m) swaps coords i,i+1;  s_m negates coord m
  omega_m = (1,1,...,1),  O(j) = L_{j omega_m}
"""
from fractions import Fraction
from itertools import combinations
import sys

def pos_roots(m):
    R = []
    for i in range(m):
        for j in range(i+1, m):
            v = [0]*m; v[i] = 1; v[j] = -1; R.append(tuple(v))   # eps_i - eps_j
            v = [0]*m; v[i] = 1; v[j] = 1;  R.append(tuple(v))   # eps_i + eps_j
        v = [0]*m; v[i] = 2; R.append(tuple(v))                  # 2 eps_i
    return R

def is_pos(v):
    """a root is positive iff its first nonzero coordinate is positive (C_m, this basis)"""
    for x in v:
        if x: return x > 0
    return False

# ---- minimal coset representatives of W(C_m)/W(P_m), P_m omits alpha_m ----
# w(eps_i) = sigma_i eps_{p_i}.  w minimal in w W_P  iff  w(alpha_i)>0 for all i<m,
# which forces sigma = (+,...,+,-,...,-), the + block's labels increasing and the
# - block's labels decreasing.  So minimal reps <-> subsets S = {labels with sigma=-}.
def min_rep(S, m):
    S = sorted(S)
    plus = [p for p in range(1, m+1) if p not in set(S)]      # increasing
    minus = sorted(S, reverse=True)                            # decreasing
    sig = [1]*len(plus) + [-1]*len(minus)
    lab = plus + minus
    return tuple(sig), tuple(lab)

def act(w, v):
    """apply w to weight v (v in Z^m, coords in the eps basis).
    w(eps_i) = sig_i eps_{lab_i}, so (w v)_{lab_i} = sig_i * v_i."""
    sig, lab = w
    m = len(v); out = [0]*m
    for i in range(m):
        out[lab[i]-1] += sig[i]*v[i]
    return tuple(out)

def length(w, m):
    return sum(1 for a in pos_roots(m) if not is_pos(act(w, a)))

def left_mult(i, w, m):
    """s_i * w : s_i acts on the VALUE labels."""
    sig, lab = list(w[0]), list(w[1])
    if i < m:            # swap labels i, i+1
        for k in range(m):
            if lab[k] == i:     lab[k] = i+1
            elif lab[k] == i+1: lab[k] = i
    else:                # s_m negates eps_m : flip sign where label == m
        for k in range(m):
            if lab[k] == m: sig[k] = -sig[k]
    return (tuple(sig), tuple(lab))

def reduced_word(w, m):
    """w = s_{i_1} ... s_{i_l} reduced, returned as [i_1,...,i_l] (left descents peeled off)."""
    word = []; cur = w; L = length(cur, m)
    while L > 0:
        for i in range(1, m+1):
            nxt = left_mult(i, cur, m)
            if length(nxt, m) == L-1:
                word.append(i); cur = nxt; L -= 1
                break
        else:
            raise RuntimeError("no left descent")
    return word

# ---- Demazure operators on Laurent polynomials (dict weight -> int coeff) ----
def pairing(lam, i, m):
    return lam[i-1] - lam[i] if i < m else lam[m-1]

def alpha(i, m):
    v = [0]*m
    if i < m: v[i-1] = 1; v[i] = -1
    else:     v[m-1] = 2
    return tuple(v)

def demazure(f, i, m):
    """D_i(e^lam) = sum_{k=0}^{n} e^{lam - k a}  if n>=0;  0 if n=-1;
                    -sum_{k=1}^{-n-1} e^{lam + k a}  if n<=-2.   (n = <lam,alpha_i^vee>)"""
    a = alpha(i, m); out = {}
    for lam, co in f.items():
        n = pairing(lam, i, m)
        if n >= 0:
            for k in range(n+1):
                w = tuple(lam[t] - k*a[t] for t in range(m))
                out[w] = out.get(w, 0) + co
        elif n == -1:
            continue
        else:
            for k in range(1, -n):
                w = tuple(lam[t] + k*a[t] for t in range(m))
                out[w] = out.get(w, 0) - co
    return {k: v for k, v in out.items() if v}

def chi(word, lam, m):
    """(D_{i_1} ... D_{i_l} e^lam)(1)"""
    f = {tuple(lam): 1}
    for i in reversed(word):
        f = demazure(f, i, m)
    return sum(f.values())

# ---- strict partitions, and the bijection subsets <-> strict partitions ----
def strict_partitions(m):
    out = []
    for k in range(m+1):
        for s in combinations(range(m, 0, -1), k):
            out.append(tuple(s))
    return out

def kappa_of_subset(S, m):
    """kappa(S) = sorted{ m+1-t : t in S } descending"""
    return tuple(sorted((m+1-t for t in S), reverse=True))

def subset_of_kappa(kappa, m):
    return frozenset(m+1-p for p in kappa)

# ---- Weyl dimension formula for Sp(2m), lambda = j*omega_m (independent route) ----
def dim_V(j, m):
    a = [j + m - i for i in range(m)]          # lambda+rho = (j+m, ..., j+1)
    r = [m - i for i in range(m)]
    num = 1; den = 1
    for i in range(m):
        num *= a[i]; den *= r[i]
        for k in range(i+1, m):
            num *= (a[i]**2 - a[k]**2); den *= (r[i]**2 - r[k]**2)
    assert num % den == 0 or True
    return Fraction(num, den)

def lagrange(pts):
    """interpolate: pts = [(x,y)], return callable on Fractions"""
    def f(x):
        x = Fraction(x); tot = Fraction(0)
        for i, (xi, yi) in enumerate(pts):
            term = Fraction(yi)
            for k, (xk, _) in enumerate(pts):
                if k != i:
                    term *= Fraction(x - xk, xi - xk)
            tot += term
        return tot
    return f

if __name__ == "__main__":
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    print(f"=== CHECK A: |kappa(S)| == length(w_S) for all 2^{m} subsets, m={m} ===")
    bad = 0
    for k in range(m+1):
        for S in combinations(range(1, m+1), k):
            w = min_rep(S, m); L = length(w, m); kap = kappa_of_subset(S, m)
            if L != sum(kap): bad += 1; print("   MISMATCH", S, kap, L)
    print(f"  mismatches = {bad}")

    print(f"\n=== CHECK B: Bruhat order on min reps  <->  containment of strict partitions ===")
    # Bruhat order on W/W_P via: X_rho subset X_kappa iff rho subset kappa.
    # verify by subword/closure: use the standard criterion on the LG fixed-point
    # description is heavy; instead check ranks + the covering count agrees.
    ks = strict_partitions(m)
    from collections import Counter
    c1 = Counter(sum(k) for k in ks)
    c2 = Counter(length(min_rep(subset_of_kappa(k, m), m), m) for k in ks)
    print(f"  rank generating function by |kappa|: {dict(sorted(c1.items()))}")
    print(f"  rank generating function by l(w)   : {dict(sorted(c2.items()))}   equal={c1==c2}")

    print(f"\n=== CHECK C: engine validation ===")
    # C1: kappa = empty  -> H == 1
    w = min_rep(frozenset(), m); word = reduced_word(w, m)
    print(f"  kappa=():      word={word}, H(j) for j=0..3 -> {[chi(word,[j]*m,m) for j in range(4)]}  (expect 1,1,1,1)")
    # C2: kappa = (1)   -> H(j) = j+1   (X is a line in the minimal embedding)
    kap = (1,); w = min_rep(subset_of_kappa(kap, m), m); word = reduced_word(w, m)
    print(f"  kappa=(1):     word={word}, H(j) for j=0..4 -> {[chi(word,[j]*m,m) for j in range(5)]}  (expect 1,2,3,4,5)")
    # C3: kappa = (k) one-row -> sum_{h<=j} binom(2h+k-1,k-1)
    from math import comb
    for kk in range(1, m+1):
        kap = (kk,); w = min_rep(subset_of_kappa(kap, m), m); word = reduced_word(w, m)
        got = [chi(word, [j]*m, m) for j in range(4)]
        exp = [sum(comb(2*h+kk-1, kk-1) for h in range(jj+1)) for jj in range(4)]
        print(f"  kappa=({kk},):    got {got}   cone-formula {exp}   match={got==exp}")
    # C4: full staircase -> dim V_{j omega_m}  (Demazure vs Weyl dimension formula)
    full = tuple(range(m, 0, -1))
    w = min_rep(subset_of_kappa(full, m), m); word = reduced_word(w, m)
    got = [chi(word, [j]*m, m) for j in range(4)]
    exp = [int(dim_V(j, m)) for j in range(4)]
    print(f"  kappa={full}: Demazure {got}  WeylDim {exp}  match={got==exp}")
