#!/usr/bin/env python3
"""Exact checks for Clio's review of Lyra's notes UID 869 (n_eff / Ringelmann) and
UID 892 (jury-theorem objection, product combiner under drift). 2026-11-13.

All arithmetic is fractions.Fraction unless marked FLOAT.  Every section ends with
asserts; the script prints PASS lines and a final summary.  Run:  python3 -I checks.py
"""
from fractions import Fraction as F
from itertools import product, combinations
from math import comb
import sympy as sp

checks = []
def ok(name, cond):
    checks.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name)

# ---------------------------------------------------------------------------
# Q1-a.  Lyra's large-N table for R(N)=1/(1+c(N-1)N^-beta)  (symbolic limits)
# ---------------------------------------------------------------------------
N, c = sp.symbols('N c', positive=True)
def neff(beta):
    return N / (1 + c*(N-1)*N**(-beta))
ok("Q1a beta=0: n_eff -> 1/c", sp.simplify(sp.limit(neff(0), N, sp.oo) - 1/c) == 0)
ok("Q1a beta=1: n_eff/N -> 1/(1+c)", sp.simplify(sp.limit(neff(1)/N, N, sp.oo) - 1/(1+c)) == 0)
ok("Q1a beta=1/2: n_eff/N^beta -> 1/c", sp.simplify(sp.limit(neff(sp.Rational(1,2))/sp.sqrt(N), N, sp.oo) - 1/c) == 0)
ok("Q1a beta=2: n_eff/N -> 1", sp.limit(neff(2)/N, N, sp.oo) == 1)

# ---------------------------------------------------------------------------
# Q1-b.  Projectivity forces rho_N constant: the (1,2) marginal of an exchangeable
# N-law obtained by projecting an (N+1)-law is the same pair law.  Demonstrate with
# beta-binomial-like two-point mixtures: a single mixing law gives the same pair
# correlation at every N (positive), while an N-indexed family (rho_N=c/N^2) is a
# valid mixture AT EACH N but its pair marginals differ across N (so no single
# infinite sequence has all of them as projections).
# ---------------------------------------------------------------------------
def mixture_law(N_, atoms):
    """atoms: list of (theta, weight). Returns dict y-tuple -> prob for iid Bern(theta)."""
    law = {}
    for y in product((0, 1), repeat=N_):
        k = sum(y)
        law[y] = sum(w * th**k * (1-th)**(N_-k) for th, w in atoms)
    return law

def pair_corr(law):
    N_ = len(next(iter(law)))
    s = sum(p for y, p in law.items() if y[0] == 1)
    e12 = sum(p for y, p in law.items() if y[0] == 1 and y[1] == 1)
    return s, (e12 - s*s) / (s*(1-s))

def kish_from_law(law):
    """n_eff = N * s(1-s)/ (Var(sum)/N) computed from the full law."""
    N_ = len(next(iter(law)))
    s = sum(p for y, p in law.items() if y[0] == 1)
    m1 = sum(p*sum(y) for y, p in law.items())
    m2 = sum(p*sum(y)**2 for y, p in law.items())
    var_mean = (m2 - m1*m1) / N_**2
    return s*(1-s) / var_mean

cc = F(1, 4)
allgood = True
for N_ in range(2, 8):
    rhoN = cc / N_**2                    # beta = 2
    d = F(1, 4*N_)                       # Var(Theta_N) = d^2 = rhoN * s(1-s), s=1/2
    assert d*d == rhoN * F(1, 4)
    law = mixture_law(N_, [(F(1,2)-d, F(1,2)), (F(1,2)+d, F(1,2))])
    s, r = pair_corr(law)
    allgood &= (s == F(1,2) and r == rhoN and kish_from_law(law) == F(N_) / (1 + (N_-1)*rhoN))
ok("Q1b N-indexed mixture family (beta=2): each N is an iid mixture with rho_N=c/N^2 and Kish exact, N=2..7", allgood)
# projectivity check: the 2-marginal of the N=3 member is not the N=2 member
law3 = mixture_law(3, [(F(1,2)-F(1,12), F(1,2)), (F(1,2)+F(1,12), F(1,2))])
law2 = mixture_law(2, [(F(1,2)-F(1,8), F(1,2)), (F(1,2)+F(1,8), F(1,2))])
marg = {}
for y, p in law3.items():
    marg[y[:2]] = marg.get(y[:2], 0) + p
ok("Q1b family is NOT projective (N=3 member's pair marginal != N=2 member)", marg != law2)

# Var(Theta) identified by the pair law even when the mixing law is not: two mixing laws
# with equal first two moments, different third, give the same pair law and different N=3 laws.
A = [(F(0), F(1,2)), (F(1), F(1,2))]                       # mean 1/2, E th^2 = 1/2
B = [(F(1,2)-F(1,2), F(1,2)), (F(1,2)+F(1,2), F(1,2))]      # same as A (sanity) ...
B = [(F(0), F(1,4)), (F(1,2), F(0)), (F(1), F(1,4)), (F(1,2), F(1,2))]  # mean 1/2, E th^2 = 1/4+1/8 = 3/8
# choose instead a law with same first two moments as A? A has Var=1/4 (max). Use a
# non-extreme pair: C1 = {1/4,3/4} each 1/2 (m2=5/16); C2 = {0:1/8, 1/2:3/4, 1:1/8} (m2 = 1/8+3/16=5/16)
C1 = [(F(1,4), F(1,2)), (F(3,4), F(1,2))]
C2 = [(F(0), F(1,8)), (F(1,2), F(3,4)), (F(1), F(1,8))]
m = lambda at, k: sum(w*th**k for th, w in at)
ok("Q1b C1,C2 share mean and second moment", m(C1,1) == m(C2,1) and m(C1,2) == m(C2,2))
ok("Q1b C1,C2 give identical N=2 laws (Var Theta identified)", mixture_law(2, C1) == mixture_law(2, C2))
ok("Q1b C1,C2 give different N=4 laws (mixing law not identified)", mixture_law(4, C1) != mixture_law(4, C2))

# Constant rho >= 0 does NOT imply a mixture: exchangeable N=3 law with P(S=k)=(1/3,0,1/2,1/6).
PS = [F(1,3), F(0), F(1,2), F(1,6)]
law = {y: PS[sum(y)] / comb(3, sum(y)) for y in product((0,1), repeat=3)}
s, r = pair_corr(law)
m1, m2 = s, sum(p for y, p in law.items() if y[0] and y[1])
m3 = sum(p for y, p in law.items() if all(y))
ok("Q1b counterexample is a probability law, exchangeable, s=1/2, rho=1/3",
   sum(law.values()) == 1 and s == F(1,2) and r == F(1,3))
ok("Q1b counterexample violates Cauchy-Schwarz E[Th]E[Th^3] >= E[Th^2]^2 (so NOT an iid mixture)",
   m1*m3 < m2*m2)

# ---------------------------------------------------------------------------
# Q2.  Heterogeneous judges with ONE shared latent Theta in {easy, hard} (prob 1/2 each),
# conditionally independent given Theta, failure probabilities p_j(Theta).
# ---------------------------------------------------------------------------
def panel(pfun):
    """pfun: list of (p_easy, p_hard). Returns marginals s_j, covariance matrix."""
    J = len(pfun)
    s = [F(1,2)*(a+b) for a, b in pfun]
    cov = [[None]*J for _ in range(J)]
    for i in range(J):
        for j in range(J):
            if i == j:
                cov[i][j] = s[i]*(1-s[i])
            else:
                eij = F(1,2)*(pfun[i][0]*pfun[j][0] + pfun[i][1]*pfun[j][1])
                cov[i][j] = eij - s[i]*s[j]
    return s, cov

def summaries(pfun):
    s, cov = panel(pfun)
    J = len(s)
    v = [cov[i][i] for i in range(J)]
    pairs = [(i, j) for i in range(J) for j in range(J) if i != j]
    # correlations are irrational in general; keep squared-and-signed form for exactness
    phi2 = {(i, j): (cov[i][j]**2 / (v[i]*v[j]), (cov[i][j] > 0) - (cov[i][j] < 0)) for i, j in pairs}
    # Kish design effect of the panel MEAN relative to independent judges with the same marginals:
    deff = 1 + sum(cov[i][j] for i, j in pairs) / sum(v)
    rho_tilde = (deff - 1) / (J - 1)          # the rho that makes 1+(J-1)rho exact
    # symmetrised (random relabelling) panel: exchangeable, marginal sbar
    sbar = sum(s) / J
    e_pair = sum(cov[i][j] + s[i]*s[j] for i, j in pairs) / len(pairs)
    rho_sym = (e_pair - sbar**2) / (sbar*(1-sbar))
    return s, cov, phi2, deff, rho_tilde, rho_sym

# (i) homogeneous control: p_j(Theta) = Theta for all j  -> identity holds exactly.
th = (F(1,10), F(7,10))
s, cov, phi2, deff, rt, rs = summaries([th, th, th])
VarTh = F(1,2)*(th[0]**2 + th[1]**2) - (F(1,2)*(th[0]+th[1]))**2
sb = s[0]
ok("Q2(i) homogeneous: phi = rho~ = rho_sym = Var(Theta)/[s(1-s)]",
   all(p == ((VarTh/(sb*(1-sb)))**2, 1) for p in phi2.values())
   and rt == VarTh/(sb*(1-sb)) and rs == rt)

# (ii) same latent, different response curves: A mild, B steep, C flat (insensitive).
pA, pB, pC = (F(1,10), F(1,2)), (F(1,10), F(9,10)), (F(3,10), F(3,10))
s, cov, phi2, deff, rt, rs = summaries([pA, pB, pC])
ok("Q2(ii) C has zero covariance with A and B despite sharing Theta", cov[0][2] == 0 and cov[1][2] == 0)
print("   Q2(ii) marginals", [str(x) for x in s], " cov_AB", cov[0][1],
      " deff", deff, " rho~", rt, " rho_sym", rs)
# mean pairwise correlation phi-bar (FLOAT for display only)
import math
phis = {k: math.copysign(math.sqrt(v[0]), v[1]) for k, v in phi2.items()}
phibar = sum(phis.values()) / len(phis)
print(f"   Q2(ii) FLOAT phi_AB={phis[(0,1)]:.6f} phi_AC=phi_BC=0  phibar={phibar:.6f}  rho~={float(rt):.6f}  rho_sym={float(rs):.6f}")
ok("Q2(ii) phibar != rho~ != rho_sym (three different numbers)", abs(phibar - float(rt)) > 1e-3 and rt != rs and abs(phibar-float(rs)) > 1e-3)
# no single latent 'Var(Theta)/s(1-s)' reproduces all three pair correlations (one is 0, one is >0)
ok("Q2(ii) pair correlations not all equal -> no single exchangeable Var(Theta) object", len(set(phi2.values())) > 1)

# (iii) opposite response: A fails on hard items, D fails on easy items -> negative co-failure.
pD = (F(1,2), F(1,10))
s, cov, phi2, deff, rt, rs = summaries([pA, pD])
ok("Q2(iii) shared latent with Var(Theta)>0 yet cov(A,D) < 0", cov[0][1] < 0)
print("   Q2(iii) cov_AD =", cov[0][1], " deff =", deff)

# (iv) Frechet ceiling: with marginals s_A < s_B the max correlation of two Bernoullis is
# sqrt(s_A(1-s_B)/(s_B(1-s_A))) < 1.  Exact check of the squared bound at s=(1/10,1/2).
sA, sB = F(1,10), F(1,2)
cov_max = min(sA, sB) - sA*sB
ok("Q2(iv) Frechet: max corr^2 = sA(1-sB)/(sB(1-sA)) = 1/9 for (1/10,1/2)",
   cov_max**2/(sA*(1-sA)*sB*(1-sB)) == sA*(1-sB)/(sB*(1-sA)) == F(1,9))

# ---------------------------------------------------------------------------
# 892 §4.  Positive controls and the filtration-level analysis.
# ---------------------------------------------------------------------------
# PC-0: the classical one.  E1 = E2 in {0,2} fair.  Each is an e-value; E[E1 E2] = 2.
ok("PC0 E1=E2 in {0,2}: E[E1]=1, E[E1*E2]=2", F(1,2)*2 == 1 and F(1,2)*4 == 2)

# PC-1: contemporaneous common shock.  At each step a fair Z in {-1,+1} (unpredictable from
# the past); stratum excesses X1=X2=Z.  Null holds per stratum given the GLOBAL past:
# E[X_s | F_{n-1}] = 0.  Per-stratum factor 1+lam*X_s with lam=1/2.
lam = F(1,2)
step_prod = [(1+lam*z)*(1+lam*z) for z in (-1, 1)]
ok("PC1 product combiner one-step mean = 5/4 > 1", sum(step_prod)/2 == F(5,4))
joint = [1 + F(1,4)*z + F(1,4)*z for z in (-1, 1)]       # joint linear bet, lam_s = 1/4
ok("PC1 joint linear bet one-step mean = 1", sum(joint)/2 == 1)

def crossing_prob(factors, T, thresh):
    """factors: list of equally likely one-step multipliers.  Exact P(max_{n<=T} M_n >= thresh)."""
    dist = {F(1): F(1)}
    crossed = F(0)
    q = F(1, len(factors))
    for _ in range(T):
        nd = {}
        for v, p in dist.items():
            for f in factors:
                w = v*f
                if w >= thresh:
                    crossed += p*q
                else:
                    nd[w] = nd.get(w, 0) + p*q
        dist = nd
    return crossed

alpha = F(1,20)
T = 40
p_prod = crossing_prob(step_prod, T, 1/alpha)
p_joint = crossing_prob(joint, T, 1/alpha)
print(f"   PC1 T={T}: P(sup product >= 20) = {float(p_prod):.4f};  P(sup joint >= 20) = {float(p_joint):.4f}")
ok("PC1 product combiner type-I > alpha (Ville fails)", p_prod > alpha)
ok("PC1 joint linear bet type-I <= alpha (Ville holds)", p_joint <= alpha)

# PC-2: interleaved strata, shock persists across ONE step.  Items arrive one at a time,
# strata alternate 1,2,1,2,...; a fair shock Z_k drives the pair of steps (2k-1, 2k): X = Z_k
# on both.  Stratum-own filtration: stratum s sees an iid fair +-1 sequence -> own-filtration
# martingale.  Global filtration: step 2k is predictable from step 2k-1 -> NOT a martingale.
# Product of the two per-stratum processes = the single global betting process.
pair_factors = [(1+lam*z)*(1+lam*z) for z in (-1, 1)]     # same as PC1 over a block of 2 steps
own = [1 + lam*z for z in (-1, 1)]
ok("PC2 each stratum alone: own-filtration martingale (mean factor 1)", sum(own)/2 == 1)
ok("PC2 product over a 2-step block has mean 5/4 (own-filtration validity is not enough)", sum(pair_factors)/2 == F(5,4))

# PC-3: deterministic common drift.  Base rate b_n (same deterministic sequence in both strata,
# 'moving together'), excess X_{s,n} = Bern(b_n) - b_n independent across strata given n.
# Product factor mean is exactly 1 at every step: trends that move together are not
# correlated increments.
drift = [F(1,10), F(1,5), F(3,10), F(1,2), F(7,10)]
good = True
for b in drift:
    vals = [(F(x) - b, b if x else 1-b) for x in (0, 1)]
    m_ = sum(p1*p2*(1+lam*x1)*(1+lam*x2) for (x1, p1) in vals for (x2, p2) in vals)
    good &= (m_ == 1)
ok("PC3 deterministic common drift: product factor mean exactly 1 at every step", good)

# PC-4: the worst-case slack is a BOUND.  For |X_s|<=1 and E[X_s|F]<=0 under ANY joint law,
# E[(1+lam X1)(1+lam X2)] <= 1 + lam^2.  Check the bound is attained (PC1) and never exceeded
# over a grid of joint laws on {-1,0,1}^2 with both conditional means <= 0.
grid = [F(k, 6) for k in range(7)]
vals3 = (-1, 0, 1)
worst = F(0)
import itertools
# enumerate joint laws with rational weights summing to 1 on a coarse lattice (9 atoms, step 1/6)
def compositions(n, k):
    if k == 1:
        yield (n,); return
    for i in range(n+1):
        for rest in compositions(n-i, k-1):
            yield (i,) + rest
atoms = list(product(vals3, vals3))
count = 0
for comp in compositions(6, 9):
    w = [F(x, 6) for x in comp]
    e1 = sum(wi*a[0] for wi, a in zip(w, atoms)); e2 = sum(wi*a[1] for wi, a in zip(w, atoms))
    if e1 > 0 or e2 > 0:
        continue
    count += 1
    m_ = sum(wi*(1+lam*a[0])*(1+lam*a[1]) for wi, a in zip(w, atoms))
    worst = max(worst, m_)
print(f"   PC4 joint laws enumerated (null-satisfying): {count};  worst product mean = {worst}")
ok("PC4 worst-case product mean = 1 + lam^2 (bound attained, never exceeded)", worst == 1 + lam**2)
ok("PC4 deflated product (1+lam X1)(1+lam X2)/(1+lam^2) is valid over the whole grid", worst/(1+lam**2) <= 1)

# ---------------------------------------------------------------------------
# 892 §2.2: the printed formula e_s(n) = 1 + lam (U_s(n) - V_s(n) - delta) with running
# averages is not a supermartingale.  Toy: increments iid fair +-1, delta=0, lam=1/2,
# e(n) = 1 + lam * mean_n.  After X_1=-1: e(1)=1/2, E[e(2)|X_1=-1] = 1 + lam*(-1/2) = 3/4.
# ---------------------------------------------------------------------------
e1 = 1 + lam*(-1)
Ee2 = F(1,2)*((1 + lam*F(-2,2)) + (1 + lam*F(0,2)))
ok("892 printed running-mean form is NOT a supermartingale (E[e(2)|X1=-1]=3/4 > e(1)=1/2)", Ee2 > e1)
ok("892 printed form is bounded by 1+lam <= 2 < 20, so it can never reject at alpha=0.05", 1 + lam*1 < 20)

print()
npass = sum(1 for _, b in checks if b)
print(f"SUMMARY {npass}/{len(checks)} checks passed")
