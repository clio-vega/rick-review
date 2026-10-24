"""Peer review of Rick's Theorem I / Theorem I_OG (integer zero window, exact, LG+OG).
Clio 2026-10-24 c2.  Independent engines: type-C and type-B Demazure (mine), my own
p=1 KLG closed form, and an order-polynomial / strict-map model on the OG side.
"""
import sys, time
from fractions import Fraction
from itertools import product
from collections import Counter
import demazure as C, demazureB as B
from comb import D, strict_partitions, contains, R, longest_chain
from testZ import klg_count_p1, is_rim

# ---------------------------------------------------------------- basics
def r_of(kappa):
    """Lemma 0: r(kappa) = max_i (kappa_i + 2i - 2), r(empty)=0."""
    return max((k + 2*(i+1) - 2 for i, k in enumerate(kappa)), default=0)

def r_via_chain(kappa, m):
    """1 + max{a+b} over D(kappa); and the longest-chain definition."""
    Dk = D(kappa, m)
    if not Dk: return 0, 0
    return 1 + max(a+b for a, b in Dk), longest_chain(Dk)

def Rset(theta, m):
    return frozenset(R(b, m) for b in theta)

def W_LG(kappa): return -(-r_of(kappa)//2)      # ceil(r/2)
def W_OG(kappa): return r_of(kappa)

def rook_strip(theta):
    rows = Counter(b[0] for b in theta); cols = Counter(b[1] for b in theta)
    return all(v <= 1 for v in rows.values()) and all(v <= 1 for v in cols.values())

def N_LG(theta, m):
    """Rick's N(theta) = #KLG-tableaux of shape R(theta), content {1}.  The R matters:
    the count is NOT R-invariant (rinv.py)."""
    return klg_count_p1(Rset(theta, m))

def c_LG(kappa, rho, m):
    if rho == kappa or not contains(kappa, rho): return 0
    th = D(kappa, m) - D(rho, m)
    if not th or not is_rim(th): return 0
    return (-1)**(len(th)-1) * N_LG(th, m)

def c_OG(kappa, rho, m):
    if rho == kappa or not contains(kappa, rho): return 0
    th = D(kappa, m) - D(rho, m)
    if not th or not rook_strip(th): return 0
    return (-1)**(len(th)-1)

# ---------------------------------------------------------------- Lemma 0
def check_lemma0(MMAX):
    print("== LEMMA 0 (chain formula): max_i(k_i+2i-2) = 1+max(a+b) = longest chain ==")
    bad = 0; tot = 0
    for m in range(1, MMAX+1):
        for kap in strict_partitions(m):
            a = r_of(kap); b, ch = r_via_chain(kap, m)
            tot += 1
            if not (a == b == ch): bad += 1; print("   MISMATCH", m, kap, a, b, ch)
        print(f"   m<={m}: {tot} kappa, mismatches = {bad}")
    return bad

# ---------------------------------------------------------------- Lemma A
def check_lemmaA(MMAX):
    print("\n== LEMMA A: T_t = {a+b >= r-t}; t*=1 if r odd else 2 ==")
    print("   (i) complement is an order ideal  (ii) T_t rim, <=2/row+col, T_1 antichain")
    print("   (iii) LG: N(T_t*) >= 1   (iv) OG: c_{rho_1} = (-1)^{|T_1|-1}   (v) W drops by >=1")
    fails = Counter(); tot = 0
    worst = []
    for m in range(1, MMAX+1):
        for kap in strict_partitions(m):
            if not kap: continue
            Dk = D(kap, m); r = r_of(kap); tot += 1
            for t in (1, 2):
                T = frozenset(b for b in Dk if b[0]+b[1] >= r-t)
                rest = Dk - T
                # (i) order ideal of Delta_m, = D(rho) for a strict rho
                rho = tuple(sorted((len([c for c in rest if c[0]==i]) + i
                                    for i in range(m) if any(c[0]==i for c in rest)),
                                   reverse=True))
                if D(rho, m) != rest: fails[f"(i) ideal t={t}"] += 1
                if not T: fails[f"(i) T empty t={t}"] += 1
                if r_of(rho) > r - t: fails[f"(i) r(rho)<=r-t t={t}"] += 1
                # (ii)
                if not is_rim(T): fails[f"(ii) rim t={t}"] += 1
                rows = Counter(b[0] for b in T); cols = Counter(b[1] for b in T)
                if max(list(rows.values())+[0]) > 2 or max(list(cols.values())+[0]) > 2:
                    fails[f"(ii) <=2 per line t={t}"] += 1
                if t == 1 and not rook_strip(T): fails["(ii) T_1 antichain"] += 1
            tstar = 1 if r % 2 else 2
            Ts = frozenset(b for b in Dk if b[0]+b[1] >= r-tstar)
            rest = Dk - Ts
            rho_s = tuple(sorted((len([c for c in rest if c[0]==i]) + i
                                  for i in range(m) if any(c[0]==i for c in rest)), reverse=True))
            # (iii) the LOAD-BEARING nonvanishing
            n = N_LG(Ts, m)
            if n < 1:
                fails["(iii) N(T_t*) >= 1  *** LOAD-BEARING ***"] += 1
                if len(worst) < 8: worst.append((m, kap, r, sorted(Ts), n))
            if c_LG(kap, rho_s, m) == 0: fails["(iii) c_{rho*} != 0"] += 1
            # (v) LG
            if W_LG(rho_s) > W_LG(kap) - 1: fails["(v) LG W drop"] += 1
            # (iv)+(v) OG
            T1 = frozenset(b for b in Dk if b[0]+b[1] >= r-1)
            rest1 = Dk - T1
            rho_1 = tuple(sorted((len([c for c in rest1 if c[0]==i]) + i
                                  for i in range(m) if any(c[0]==i for c in rest1)), reverse=True))
            if c_OG(kap, rho_1, m) != (-1)**(len(T1)-1): fails["(iv) OG c value"] += 1
            if W_OG(rho_1) > W_OG(kap) - 1: fails["(v) OG W drop"] += 1
        print(f"   m<={m}: {tot} nonempty kappa tested, total failures = {sum(fails.values())}")
    if fails:
        print("   FAILURES:", dict(fails))
        for w in worst: print("     witness", w)
    else:
        print("   ALL CLAUSES (i)-(v) HOLD, 0 failures")
    return fails

# ---------------------------------------------------------------- negative control
def negative_control(MMAX):
    print("\n== NEGATIVE CONTROL: for r ODD, does the t=2 strip fail? (parity must be load-bearing) ==")
    zero = nonzero = 0; conflict_agree = 0; tot = 0
    for m in range(1, MMAX+1):
        for kap in strict_partitions(m):
            if not kap: continue
            r = r_of(kap)
            if r % 2 == 0: continue
            Dk = D(kap, m)
            T2 = frozenset(b for b in Dk if b[0]+b[1] >= r-2)
            n = N_LG(T2, m); tot += 1
            if n == 0: zero += 1
            else: nonzero += 1
    print(f"   r-odd kappa with m<={MMAX}: {tot};  N(T_2) = 0 in {zero}, nonzero in {nonzero}")
    print(f"   -> the t=2 choice FAILS on {zero}/{tot} of the r-odd cases, so t* parity SEPARATES"
          if zero else "   -> t=2 never fails: parity choice would NOT be load-bearing")
    return zero, tot

# ---------------------------------------------------------------- Lemma Ch'
def check_chain_drop(MMAX):
    print("\n== LEMMA Ch': chain drop <= 2 (LG) and <= 1 (OG), over the TRUE support ==")
    for m in range(1, MMAX+1):
        nLG = nOG = 0; vLG = vOG = 0; maxLG = maxOG = -99
        for kap in strict_partitions(m):
            for rho in strict_partitions(m):
                if rho == kap or not contains(kap, rho): continue
                if c_LG(kap, rho, m) != 0:
                    nLG += 1; d = r_of(kap) - r_of(rho); maxLG = max(maxLG, d)
                    if d > 2: vLG += 1
                if c_OG(kap, rho, m) != 0:
                    nOG += 1; d = r_of(kap) - r_of(rho); maxOG = max(maxOG, d)
                    if d > 1: vOG += 1
        print(f"   m={m}: LG support {nLG} pairs, violations {vLG}, max drop {maxLG} | "
              f"OG support {nOG} pairs, violations {vOG}, max drop {maxOG}")

if __name__ == "__main__":
    MM = int(sys.argv[1]) if len(sys.argv) > 1 else 7
    check_lemma0(MM)
    check_lemmaA(MM)
    negative_control(MM)
    check_chain_drop(min(MM, 7))
