"""Independent check of Rick's LG FPSAC cut (WIP 6dbecb8 == 9fa6b0c mathematically),
written from the PRINTED statements.  Clio 2026-11-11 REVIEW.

Engine H: type C_m Demazure operators on Laurent monomials (G1), reduced words built by
left multiplication, dims at j=0..|kappa|, Lagrange interpolation (exact Fractions).
Engine N: brute-force counts of (strictly) order-preserving maps on shifted diagrams.
Engine Bridge: D_w(F_a) at y=1 (Prop 3.x Bridge), an independent route to half-integers.
"""
import sys
from fractions import Fraction as Fr
from itertools import combinations
from functools import lru_cache
from collections import defaultdict

M = int(sys.argv[1]) if len(sys.argv) > 1 else 4

def strict_partitions(m):
    return [tuple(s) for k in range(m+1) for s in combinations(range(m, 0, -1), k)]

def D(kappa):
    return frozenset((a, a+t) for a, k in enumerate(kappa) for t in range(k))

def leq(x, y): return x[0] <= y[0] and x[1] <= y[1]

# ---------- Demazure engine (type C_m), weights in eps-coordinates ----------
def Di(f, i, m):
    """D_i e^lam = (e^lam - e^{-a} s_i e^lam)/(1-e^{-a}); string formula."""
    out = defaultdict(int)
    if i < m - 1:
        al = tuple((1 if t == i else -1 if t == i+1 else 0) for t in range(m))
        pair = lambda l: l[i] - l[i+1]
    else:
        al = tuple((2 if t == m-1 else 0) for t in range(m))
        pair = lambda l: l[m-1]
    for lam, c in f.items():
        n = pair(lam)
        if n >= 0:
            for k in range(n+1):
                out[tuple(l - k*a for l, a in zip(lam, al))] += c
        elif n <= -2:
            for k in range(1, -n):
                out[tuple(l + k*a for l, a in zip(lam, al))] -= c
    return {k: v for k, v in out.items() if v}

def words(m):
    """sign vector mu -> reduced word (list, leftmost first) for minimal w_mu, BFS upward."""
    start = (1,)*m
    W = {start: []}
    frontier = [start]
    while frontier:
        nf = []
        for mu in frontier:
            for i in range(m):
                if i < m-1 and mu[i] == 1 and mu[i+1] == -1:
                    nu = list(mu); nu[i], nu[i+1] = nu[i+1], nu[i]; nu = tuple(nu)
                elif i == m-1 and mu[m-1] == 1:
                    nu = mu[:-1] + (-1,)
                else:
                    continue
                if nu not in W:
                    W[nu] = [i] + W[mu]; nf.append(nu)
        frontier = nf
    return W

def kappa_of(mu, m):
    return tuple(sorted((m - i for i in range(m) if mu[i] == -1), reverse=True))

def apply_word(word, f, m):
    for i in reversed(word):
        f = Di(f, i, m)
    return f

def interp(points):
    xs = [Fr(x) for x, _ in points]; ys = [Fr(y) for _, y in points]
    def P(t):
        t = Fr(t); s = Fr(0)
        for k in range(len(xs)):
            term = ys[k]
            for l in range(len(xs)):
                if l != k: term *= (t - xs[l]) / (xs[k] - xs[l])
            s += term
        return s
    return P

# ---------- counting engines ----------
def count_maps(boxes, lo, hi, strict, even_diag):
    bs = sorted(boxes)          # lexicographic order is a linear extension of product order
    preds = [[j for j in range(i) if leq(bs[j], bs[i])] for i in range(len(bs))]
    vals = [0]*len(bs)
    def rec(i):
        if i == len(bs): return 1
        x = bs[i]
        mn = lo
        for j in preds[i]:
            mn = max(mn, vals[j] + (1 if strict else 0))
        tot = 0
        for v in range(mn, hi+1):
            if even_diag and x[0] == x[1] and v % 2: continue
            vals[i] = v; tot += rec(i+1)
        return tot
    return rec(0)

def N(kappa, j, nu=()):    return count_maps(D(kappa) - D(nu), 1, 2*j-1, True, True)
def Fcount(kappa, n):      return count_maps(D(kappa), 0, n, False, True)
def Ombar(kappa, n):       return count_maps(D(kappa), 1, n, True, False)

def V(theta):
    """strict order-preserving theta -> {e<o} = {0<1}, diagonal boxes -> e (brute force)."""
    return count_maps(theta, 0, 1, True, True)

def V_lemmaR(theta):
    bs = list(theta)
    for x in bs:
        for y in bs:
            for z in bs:
                if len({x, y, z}) == 3 and leq(x, y) and leq(y, z): return 0
    for (a, b) in bs:
        if a == b and any(y != (a, b) and leq(y, (a, b)) for y in bs): return 0
    if any(a == b and ((a-1, a) in theta) != any(y != (a, b) and leq(y, (a, b)) for y in bs)
           for (a, b) in bs):
        raise AssertionError("Lemma R last claim fails")
    i = sum(1 for x in bs if x[0] != x[1] and all(y == x or not (leq(x, y) or leq(y, x)) for y in bs))
    return 2**i

def r_of(kappa):
    return 0 if not kappa else 1 + max(a+b for a, b in D(kappa))

def ceil_half(r): return (r + 1)//2

fails = defaultdict(int); counts = defaultdict(int)
def check(name, cond):
    counts[name] += 1
    if not cond:
        fails[name] += 1
        if fails[name] <= 3: print("  FAIL", name)

for m in range(1, M+1):
    Wd = words(m)
    lam = lambda j: {(j,)*m: 1}
    H = {}
    for mu, w in Wd.items():
        k = kappa_of(mu, m); d = sum(k)
        check("reduced word length = |kappa| (Lemma bonds a)", len(w) == d)
        pts = [(j, sum(apply_word(w, lam(j), m).values())) for j in range(d+2)]
        P = interp(pts[:d+1])
        check("interp uses deg |kappa| (extra point agrees)", P(d+1) == pts[d+1][1])
        H[k] = P
        # Bridge: 2^m H(-a-1/2) = [D_w F_a]_{y=1},  F_a = prod y_i^a (1+y_i), y_i=e^{-eps_i}
        for a in range(0, 4):
            Fa = {(): 1}
            Fa = defaultdict(int); Fa[tuple([-a]*m)] = 1
            for i in range(m):
                G = defaultdict(int)
                for lam_, c in Fa.items():
                    G[lam_] += c
                    l2 = list(lam_); l2[i] -= 1; G[tuple(l2)] += c
                Fa = G
            val = sum(apply_word(w, dict(Fa), m).values())
            check("Bridge (Prop bridge)", Fr(2)**m * P(Fr(-2*a-1, 2)) == val)
    PK = strict_partitions(m)
    for k in PK:
        P = H[k]; d = sum(k); sgn = (-1)**d
        s = lambda x, k=k: (-1)**sum(k) * H[k](x if False else -Fr(x))
        for j in range(0, 6):
            check("Thm main (a) H(j)=F(2j)", P(j) == Fcount(k, 2*j))
        for j in range(1, 7):
            check("Thm main (b) s_j = N_j", sgn*P(-j) == N(k, j))
        r = r_of(k)
        if k:
            check("r formula max(k_i+2i-2)", r == max(k[i] + 2*(i+1) - 2 for i in range(len(k))))
            check("Lemma anchor H(-1)=0", P(-1) == 0)
        # window
        Wn = ceil_half(r)
        sj = [sgn*P(-j) for j in range(1, Wn+8)]
        check("Thm window zeros", all(v == 0 for v in sj[:Wn]))
        check("Thm window positive after", all(v > 0 for v in sj[Wn:]))
        check("Thm window monotone", all(sj[t] <= sj[t+1] for t in range(len(sj)-1)))
        # (star) at integer and half-integer x, x in {1/2,...}
        for twox in range(-6, 14):
            x = Fr(twox, 2)
            lhs = s(x+1) - s(x)
            rhs = sum(V(D(k) - D(rho)) * ((-1)**sum(rho) * H[rho](-x))
                      for rho in PK if rho != k and D(rho) <= D(k))
            check("Prop star (all x, incl half-int, negative)", lhs == rhs)
        for rho in PK:
            if rho != k and D(rho) <= D(k):
                th = D(k) - D(rho)
                check("Lemma R closed form", V(th) == V_lemmaR(th))
        # Theorem A and HZ
        k1 = k[0] if k else 0
        check("Thm A H(-1/2)=2^-k1", P(Fr(-1, 2)) == Fr(1, 2**k1))
        if k:
            kp = k[1:]
            for a in range(1, 9):
                h = P(Fr(-2*a-1, 2))
                Nkp = N(kp, a) if kp else 1
                zero_pred = bool(kp) and a <= ceil_half(r_of(kp))
                check("HZ (i) zero iff", (h == 0) == zero_pred)
                if h != 0:
                    if 2*a < k1: check("HZ (ii) sign 2a<k1", (h > 0) == ((-1)**(d-k1) > 0))
                    if 2*a > k1: check("HZ (ii) sign 2a>k1", (h > 0) == ((-1)**d > 0))
                    if 2*a == k1:
                        check("HZ (ii) 2a=k1 both formulas agree", (-1)**(d-k1) == (-1)**d)
                check("HZ (iii) bound", abs(h) >= Fr(Nkp, 2**k1))
                if 2*a <= k1: check("HZ (iii) equality 2a<=k1", abs(h) == Fr(Nkp, 2**k1))
                check("HZ (iii) integrality", (h * 2**k1).denominator == 1)
                # Corollary row
                srow = N(k, a) + sum(Fr((-1)**(L+1), 2**L) * N(k, a, (L,)) for L in range(1, k1+1))
                check("Cor row", sgn * h == srow)
        for a in range(m, m+5):          # M = 2a+1 >= 2m+1
            v = sgn * Fr(2)**m * P(Fr(-2*a-1, 2))
            check("Cor OC positive integer", v.denominator == 1 and v > 0)
    print(f"m={m}: done, {len(PK)} shapes")
    if m == 3:
        tab = {(1,):[0,-1,-2,-3,-4,'1/2','-1/2','-3/2','-5/2','-7/2'],
               (2,):[0,1,4,9,16,'1/4','1/4','9/4','25/4','49/4'],
               (3,):[0,0,-3,-13,-34,'1/8','1/8','-7/8','-55/8','-175/8'],
               (2,1):[0,0,-1,-5,-14,'1/4',0,'-1/4','-5/2','-35/4'],
               (3,1):[0,0,2,15,56,'1/8',0,'3/8','25/4','245/8'],
               (3,2):[0,0,-1,-13,-70,'1/8',0,'-1/8','-17/4','-259/8'],
               (3,2,1):[0,0,0,1,14,'1/8',0,0,'1/8','35/8']}
        pts = [-1,-2,-3,-4,-5] + [Fr(-1,2),Fr(-3,2),Fr(-5,2),Fr(-7,2),Fr(-9,2)]
        for k, row in tab.items():
            for x, v in zip(pts, row):
                check("Table 1 entry", H[k](x) == Fr(v))
        check("Ex 1.2 H_(2,1)(j)=(j+1)(j+2)(2j+3)/6",
              all(H[(2,1)](j) == Fr((j+1)*(j+2)*(2*j+3), 6) for j in range(-6, 7)))
        check("Rem window-ind s_4(3,2)=13", -H[(3,2)](-4) == 13)
        check("Rem window-ind s_3(3,2)=1", -H[(3,2)](-3) == 1)
        check("Cor row example s_{5/2}(3)=7/8", -H[(3,)](Fr(-5,2)) == Fr(7, 8))

print()
for name in counts:
    print(f"  {name:55s} {counts[name]-fails[name]:6d}/{counts[name]:<6d}")
print("TOTAL FAILURES:", sum(fails.values()))
