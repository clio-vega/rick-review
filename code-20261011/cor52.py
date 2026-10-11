"""Cor 5.2 of the long version, two independent engines.
A: d_{lam mu} = [s^{n(mu)}] c_{lam mu}, c from the printed subset formula.
B: t^{n(mu')-n(lam')} [P_{mu'}(x;t^{-1})] e_lam, from Macdonald III (2.2) HL polys."""
import sys
from fractions import Fraction
from ring import *
from ebasis import e_expand, estar, cstr, count01
import hl

def tpoly_str(d):
    if not d: return "0"
    return " + ".join(f"{v}*t^{k}" if k else f"{v}" for k, v in sorted(d.items()))

def run(n, verbose=False):
    m = n
    V = vandermonde(m)
    parts = list(partitions(n))
    # ---- ENGINE A ----
    A = {}
    for lam in parts:
        F = estar(lam, m, V)
        exp = e_expand(F, n, m)
        for mu in parts:
            c = exp.get(mu, {})
            val = n_mu = nstat(mu)
            d = {te: v for (se, te), v in c.items() if se == n_mu}
            below = [(se, te) for (se, te) in c if se < n_mu]
            A[(lam, mu)] = (d, below, c)
    # ---- ENGINE B ----
    C, _ = hl.e_in_P(n, m)
    B = {}
    for lam in parts:
        for mu in parts:
            mup = conj(mu)
            c = C.get((lam, mup), {})
            sh = nstat(mup) - nstat(conj(lam))
            B[(lam, mu)] = {(-k + sh): v for k, v in c.items()} if c else {}
    # ---- compare ----
    bad = []; nonz = 0; notN = []; valbad = []; onebad = []
    for lam in parts:
        for mu in parts:
            dA, below, craw = A[(lam, mu)]
            dB = B[(lam, mu)]
            if dA != dB: bad.append((lam, mu, dA, dB))
            if dA: nonz += 1
            # Thm DS: valuation exactly n(mu) whenever mu >= lam  -> leading coeff nonzero
            if hl.dominates(mu, lam):
                if below: valbad.append(('val<n(mu)', lam, mu, below))
                if not dA: valbad.append(('lead=0', lam, mu))
            else:
                if craw: valbad.append(('support outside dominance', lam, mu, cstr(craw)))
            # N[t] positivity + integrality
            if any(v < 0 or v.denominator != 1 or k < 0 for k, v in dA.items()): notN.append((lam, mu, dA))
            # d(1) = # 0-1 matrices rows lam cols mu'
            if sum(dA.values()) != count01(lam, conj(mu)): onebad.append((lam, mu, sum(dA.values()), count01(lam, conj(mu))))
    print(f"n={n}: {len(parts)}^2={len(parts)**2} pairs, {nonz} with d!=0")
    print(f"   A vs B mismatches            : {len(bad)}")
    print(f"   Thm DS valuation/support     : {len(valbad)} problems")
    print(f"   d in N[t] violations         : {len(notN)}")
    print(f"   d(1)=M_{{lam,mu'}} violations : {len(onebad)}")
    for b in bad[:4]: print("     MISMATCH", b)
    for b in valbad[:4]: print("     DS", b)
    for b in notN[:4]: print("     notN", b)
    for b in onebad[:4]: print("     one", b)
    return len(bad)+len(valbad)+len(notN)+len(onebad), A, B, parts

if __name__ == "__main__":
    tot = 0
    for n in range(1, int(sys.argv[1]) + 1):
        r = run(n)[0]; tot += r
    print("TOTAL problems:", tot)
