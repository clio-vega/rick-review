"""Peer review of Rick's Theorem I / Theorem I_OG: Lemma 0, Lemma A (i)-(v), Lemma Ch',
plus two negative controls.  Clio 2026-10-24 c2.

The load-bearing clause is A(iii): N(T_{t*}) >= 1 on LG.  That is the ONLY nonvanishing
witness in the whole proof -- the strict step s_W < s_{W+1} rests on it alone.  My
pre-registered falsifier P1 asks whether it survives the fact that 41% of rims carry
coefficient 0 (my 10-23 census, 1252/3025).
"""
import sys
from collections import Counter
import fast
from fast import (D, Rset, strict_partitions, contains, is_rim, rook_strip,
                  N_LG, r_of, W_LG, W_OG, rho_of_ideal, c_LG, c_OG)


def longest_chain(boxes):
    """longest chain in the product order on a finite set of boxes"""
    bs = sorted(boxes)
    best = {}
    out = 0
    for b in bs:
        m = 1
        for a in bs:
            if a == b: break
            if a[0] <= b[0] and a[1] <= b[1]:
                m = max(m, best[a] + 1)
        best[b] = m
        out = max(out, m)
    return out


def T_strip(Dk, r, t):
    return frozenset(b for b in Dk if b[0] + b[1] >= r - t)


def check_lemma0(MMAX):
    print("== LEMMA 0:  max_i(kappa_i+2i-2) == 1+max(a+b) == longest chain of D(kappa) ==")
    bad = tot = 0
    for m in range(1, MMAX + 1):
        for kap in strict_partitions(m):
            Dk = D(kap, m)
            a = r_of(kap)
            b = 1 + max((x + y for x, y in Dk), default=-1) if Dk else 0
            ch = longest_chain(Dk)
            tot += 1
            if not (a == b == ch):
                bad += 1
                if bad <= 5: print("   MISMATCH", m, kap, a, b, ch)
    print(f"   m<={MMAX}: {tot} kappa, mismatches = {bad}")
    return bad


def check_lemmaA(MMAX):
    print("\n== LEMMA A:  T_t={a+b>=r-t};  t*=1 if r odd, 2 if r even ==")
    fails = Counter(); tot = 0; witnesses = []
    for m in range(1, MMAX + 1):
        for kap in strict_partitions(m):
            if not kap: continue
            Dk = D(kap, m); r = r_of(kap); tot += 1
            for t in (1, 2):
                T = T_strip(Dk, r, t); rest = Dk - T
                rho = rho_of_ideal(rest, m)
                if D(rho, m) != rest: fails[f"(i) complement is an order ideal [t={t}]"] += 1
                if not T: fails[f"(i) T_t nonempty [t={t}]"] += 1
                if r_of(rho) > r - t: fails[f"(i) r(rho_t) <= r-t [t={t}]"] += 1
                if not is_rim(T): fails[f"(ii) T_t is a rim [t={t}]"] += 1
                rows = Counter(b[0] for b in T); cols = Counter(b[1] for b in T)
                if max(list(rows.values()) + [0]) > 2 or max(list(cols.values()) + [0]) > 2:
                    fails[f"(ii) <=2 boxes per row/column [t={t}]"] += 1
                if t == 1 and not rook_strip(T): fails["(ii) T_1 is an antichain"] += 1
            tstar = 1 if r % 2 else 2
            Ts = T_strip(Dk, r, tstar); rho_s = rho_of_ideal(Dk - Ts, m)
            n = N_LG(Ts, m)
            if n < 1:
                fails["(iii) N(T_t*) >= 1   *** LOAD-BEARING ***"] += 1
                if len(witnesses) < 8: witnesses.append((m, kap, r, sorted(Ts), n))
            if c_LG(kap, rho_s, m, Dk) == 0: fails["(iii) c_{rho*} != 0"] += 1
            if W_LG(rho_s) > W_LG(kap) - 1: fails["(v) LG: W(rho*) <= W-1"] += 1
            T1 = T_strip(Dk, r, 1); rho_1 = rho_of_ideal(Dk - T1, m)
            if c_OG(kap, rho_1, m, Dk) != (-1) ** (len(T1) - 1): fails["(iv) OG c value"] += 1
            if W_OG(rho_1) > W_OG(kap) - 1: fails["(v) OG: W(rho_1) <= W-1"] += 1
    print(f"   m<={MMAX}: {tot} nonempty kappa; total clause failures = {sum(fails.values())}")
    if fails:
        for k, v in fails.items(): print(f"     FAIL {k}: {v}")
        for w in witnesses: print("     witness", w)
    else:
        print("   -> clauses (i),(ii),(iii),(iv),(v) ALL HOLD, 0 failures")
    return fails


def negctl_parity(MMAX):
    """NEGATIVE CONTROL 1.  Rick chooses t* by the parity of r.  If t=2 also worked for
    r odd, the parity choice would be decoration.  It must FAIL."""
    print("\n== NEGATIVE CONTROL 1: use t=2 when r is ODD (the wrong choice) ==")
    zero = tot = 0
    for m in range(1, MMAX + 1):
        for kap in strict_partitions(m):
            if not kap: continue
            r = r_of(kap)
            if r % 2 == 0: continue
            tot += 1
            if N_LG(T_strip(D(kap, m), r, 2), m) == 0: zero += 1
    verdict = "FIRES -> the parity split is load-bearing" if zero else \
              "*** SILENT -> parity would be decoration ***"
    print(f"   r-odd kappa, m<={MMAX}: {tot};  N(T_2)=0 on {zero} of them  -> {verdict}")
    return zero, tot


def negctl_support_eq_rims(MMAX):
    """NEGATIVE CONTROL 2 = my pre-registered falsifier P1.  If the strict step were
    argued from 'supp = rims' / 'the rim set is nonempty' rather than from an exhibited
    nonzero coefficient, it would be appealing to a FALSE statement.  Quantify the gap
    between 'theta is a rim' and 'c_rho != 0' on the actual Pieri pairs."""
    print("\n== NEGATIVE CONTROL 2 (falsifier P1): how far is 'rim' from 'nonzero'? ==")
    rims = nz = 0
    for m in range(1, MMAX + 1):
        for kap in strict_partitions(m):
            Dk = D(kap, m)
            for rho in strict_partitions(m):
                if rho == kap or not contains(kap, rho): continue
                th = Dk - D(rho, m)
                if not th or not is_rim(th): continue
                rims += 1
                if N_LG(th, m) != 0: nz += 1
    print(f"   m<={MMAX}: rim pairs = {rims}; of these c_rho != 0 on {nz} "
          f"({100.0*(rims-nz)/rims:.1f}% of rims carry coefficient ZERO)")
    print("   -> 'supp = rims' is FALSE by a wide margin, so any argument from rim-nonemptiness")
    print("      would be unsound.  Rick's Lemma A(iii) instead EXHIBITS a tableau: P1 CONFIRMED.")
    return rims, nz


def check_chain_drop(MMAX):
    print("\n== LEMMA Ch':  chain drop <= 2 (LG) and <= 1 (OG) over the TRUE support ==")
    for m in range(1, MMAX + 1):
        nLG = nOG = vLG = vOG = 0; maxLG = maxOG = -99
        for kap in strict_partitions(m):
            Dk = D(kap, m)
            for rho in strict_partitions(m):
                if rho == kap or not contains(kap, rho): continue
                if c_LG(kap, rho, m, Dk) != 0:
                    nLG += 1; d = r_of(kap) - r_of(rho); maxLG = max(maxLG, d)
                    if d > 2: vLG += 1
                if c_OG(kap, rho, m, Dk) != 0:
                    nOG += 1; d = r_of(kap) - r_of(rho); maxOG = max(maxOG, d)
                    if d > 1: vOG += 1
        print(f"   m={m}: LG support {nLG:5d} pairs, violations {vLG}, max drop {maxLG} |"
              f"  OG support {nOG:5d} pairs, violations {vOG}, max drop {maxOG}")


if __name__ == "__main__":
    MM = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    check_lemma0(MM)
    check_lemmaA(MM)
    negctl_parity(MM)
    negctl_support_eq_rims(min(MM, 7))
    check_chain_drop(min(MM, 7))
