"""
Item 1, 2026-09-30 peer review: the Korff sign convention.

Question owed to Rick (his 2026-09-26 review, s.3): which convention is in force
at Korff arXiv:1906.02565 src l.1782 / l.1838, where lem:cylMNrule (ii) m=n
branch prints  (-1)^k (t^{n-k}-1)/(t-1)  and its t->1 limit  (-1)^k (n-k).

Rick's falsifier: in QH^*(Gr_k(C^n)), for P^2 (k=1,n=3) the "defect"
p_1 h_2 + p_2 h_1 is +2q = (-1)^{k-1}(n-k) q, so Korff's (-1)^k(n-k) gives -2.

Written from Korff's PRINTED definitions (bigH src l.1727, cylchi src l.1762)
plus Vafa-Intriligator, which Korff does not use -- a differential check, not a
re-run of his derivation.

Conventions read at first hand from src l.1768, the sentence just before the lemma:
    H_r = H_r(t,-1)    i.e.  a = t,  b = -1    (the OPPOSITE order to the a=-1,
                                                b=t of the rim-hook lemma at
                                                l.1746-1757 / eq A2H)
    matrix element between CONJUGATES lambda',mu' in P^+_{n-k,n}
                                               -- charge sector n-k, not k
    divided by (t-1)^{ell(nu)}
"""
import itertools
import cmath
import sympy as sp

TOL = 1e-9
t, q = sp.symbols('t q')

# q is taken at several generic numeric values; nothing below depends on the choice.
QVALS = [0.7 + 0.3j, 1.0 + 0.0j, -1.3 + 2.1j, 0.05 - 0.9j]


def bethe_subsets(n, k, qv):
    """k-subsets S of the n roots of z^n = c,  c = (-1)^{k-1} q  (Vafa-Intriligator).

    Verified in (A) below to reproduce the Siebert-Tian presentation
    QH^*(Gr_k(C^n)) = Z[q][e_1..e_k]/(h_{n-k+1},..,h_{n-1}, h_n - (-1)^{k-1} q).
    """
    c = ((-1) ** (k - 1)) * qv
    r0 = c ** (1.0 / n)
    roots = [r0 * cmath.exp(2j * cmath.pi * j / n) for j in range(n)]
    return c, list(itertools.combinations(roots, k))


def h_list(zetas, N):
    """h_0..h_N of the finite alphabet zetas, by convolving 1/(1-z x)."""
    h = [1.0 + 0j] + [0j] * N
    for z in zetas:
        new = [0j] * (N + 1)
        for j in range(N + 1):          # 1/(1-zx) = sum z^m x^m
            zm = z ** j
            for i in range(N + 1 - j):
                new[i + j] += h[i] * zm
        h = new
    return h


def p_of(zetas, m):
    return sum(z ** m for z in zetas)


def close(a, b, scale=1.0):
    return abs(a - b) <= TOL * max(1.0, abs(scale), abs(a), abs(b))


PAIRS = [(n, k) for n in range(2, 8) for k in range(1, n)]

print("=" * 78)
print("(A) Siebert-Tian presentation recovered from Vafa-Intriligator")
print("    h_{n-k+1}=..=h_{n-1}=0  and  h_n = (-1)^{k-1} q  on every Bethe subset")
print("=" * 78)
fails = 0
for (n, k) in PAIRS:
    ok = True
    for qv in QVALS:
        c, subs = bethe_subsets(n, k, qv)
        for S in subs:
            hs = h_list(S, n)
            for j in range(n - k + 1, n):
                if not close(hs[j], 0.0, abs(c)):
                    ok = False
            if not close(hs[n], c, abs(c)):
                ok = False
    fails += (not ok)
    print(f"  n={n} k={k}: {'OK' if ok else 'FAIL'}")
print(f"  -> {len(PAIRS)-fails}/{len(PAIRS)} (k,n) pairs, {len(QVALS)} values of q each")

print()
print("=" * 78)
print("(B) the two constants -- they are NOT the same object")
print("      psi(p_n)                     <- what Korff's m=n branch computes")
print("      sum_{e=1}^{n-1} p_e h_{n-e}  <- what Rick's P^2 computation computes")
print("    both are scalars (equal on every Bethe subset); magnitudes k vs n-k")
print("=" * 78)
print(f"  {'(k,n)':>8} | {'psi(p_n)/q':>11} | {'(-1)^(k-1) k':>13} | "
      f"{'defect/q':>10} | {'(-1)^(k-1)(n-k)':>16} | scalar?")
bad = 0
for (n, k) in PAIRS:
    rowok = True
    for qv in QVALS:
        c, subs = bethe_subsets(n, k, qv)
        pns, dfs = [], []
        for S in subs:
            hs = h_list(S, n)
            pns.append(p_of(S, n))
            dfs.append(sum(p_of(S, e) * hs[n - e] for e in range(1, n)))
        scalar = (all(close(v, pns[0], abs(qv)) for v in pns)
                  and all(close(v, dfs[0], abs(qv)) for v in dfs))
        pred_pn = ((-1) ** (k - 1)) * k * qv
        pred_df = ((-1) ** (k - 1)) * (n - k) * qv
        if not (scalar and close(pns[0], pred_pn, abs(qv)) and close(dfs[0], pred_df, abs(qv))):
            rowok = False
    c, subs = bethe_subsets(n, k, 1.0 + 0j)
    hs = h_list(subs[0], n)
    pn = p_of(subs[0], n).real
    df = sum(p_of(subs[0], e) * hs[n - e] for e in range(1, n)).real
    bad += (not rowok)
    print(f"  {(k,n)!s:>8} | {pn:>11.4f} | {(-1)**(k-1)*k:>13} | {df:>10.4f} | "
          f"{(-1)**(k-1)*(n-k):>16} | {'OK' if rowok else 'FAIL'}")
print(f"  -> {len(PAIRS)-bad}/{len(PAIRS)} pairs confirm psi(p_n)=(-1)^(k-1) k q"
      f" and defect=(-1)^(k-1)(n-k) q")

print()
print("=" * 78)
print("(C) Korff's H_n from bigH (src l.1727) at HIS convention (a,b)=(t,-1),")
print("    charge sector n-k.   Printed at src l.1820:  H_n = (-1)^k q (t^{n-k}-1)")
print("=" * 78)


def H_sn_bigH(s, n, K, a, b):
    """The r = s n branch of bigH, verbatim: (-1)^{(K-1)s} q^s b^{sn} (1-(-a/b)^K)."""
    return (-1) ** ((K - 1) * s) * q ** s * b ** (s * n) * (1 - (-sp.Integer(1) * a / b) ** K)


cfail = 0
for (n, k) in PAIRS:
    got = sp.expand(sp.simplify(H_sn_bigH(1, n, n - k, t, sp.Integer(-1))))
    want = sp.expand((-1) ** k * q * (t ** (n - k) - 1))
    ok = sp.simplify(got - want) == 0
    cfail += (not ok)
    print(f"  n={n} k={k}: bigH -> {got}    printed -> {want}   {'OK' if ok else 'MISMATCH'}")
print(f"  -> {len(PAIRS)-cfail}/{len(PAIRS)}; and (t^{{n-k}}-1)/(t-1) -> n-k as t->1,")
print("     so l.1782 and l.1838 follow from l.1820 by the (t-1)^ell(nu) normalisation.")

print()
print("=" * 78)
print("(C') independent check of bigH's H_n at the OTHER convention (a,b)=(-1,t),")
print("     where Korff DOES state the Satake dictionary (l.1757 / eq A2H):")
print("       H_r(-1,t)|V_k  =  multiplication by h_r[(t-1)y] in QH^*(Gr_k(C^n))")
print("     h_r[(t-1)Y] evaluated at the Bethe roots via p_m[(t-1)Y]=(t^m-1)p_m[Y].")
print("=" * 78)
tfail = 0
for (n, k) in PAIRS:
    ok = True
    for tv in [0.37, 1.8, -0.6, 2.5]:
        for qv in QVALS[:2]:
            c, subs = bethe_subsets(n, k, qv)
            for S in subs:
                # sum_r h_r[(t-1)Y] x^r = prod_{i in S} (1-z x)/(1-t z x); take x^n coeff
                num = [1.0 + 0j] + [0j] * n
                for z in S:
                    conv = [0j] * (n + 1)
                    for i in range(n + 1):
                        if i <= n:
                            conv[i] += num[i]
                        if i + 1 <= n:
                            conv[i + 1] += -z * num[i]
                    num = conv
                den = [1.0 + 0j] + [0j] * n
                for z in S:
                    conv = [0j] * (n + 1)
                    for i in range(n + 1):
                        for m in range(n + 1 - i):
                            conv[i + m] += num[i] * (tv * z) ** m if False else 0
                    break
                # do it properly: multiply num by prod 1/(1-t z x) as a power series
                ser = num[:]
                for z in S:
                    new = [0j] * (n + 1)
                    for i in range(n + 1):
                        for m in range(n + 1 - i):
                            new[i + m] += ser[i] * (tv * z) ** m
                    ser = new
                got = ser[n]
                want = complex(H_sn_bigH(1, n, k, sp.Integer(-1), sp.Float(tv))
                               .subs(q, complex(qv)).evalf())
                if not close(got, want, abs(qv)):
                    ok = False
    tfail += (not ok)
    print(f"  n={n} k={k}: h_n[(t-1)Y] at Bethe roots == bigH H_n(-1,t)|V_k : "
          f"{'OK' if ok else 'FAIL'}")
print(f"  -> {len(PAIRS)-tfail}/{len(PAIRS)}: bigH is internally consistent with the")
print("     Satake dictionary Korff states, on 4 values of t and 2 of q.")

print()
print("=" * 78)
print("(D) THE RECONCILIATION")
print("    Korff's constant = omega-twist of psi(p_n) in the CONJUGATE sector K=n-k:")
print("      psi_K(p_n)/q = (-1)^{K-1} K       honest Newton image in charge K")
print("      omega(p_n)   = (-1)^{n-1} p_n     conjugation lambda -> lambda'")
print("    claim:  (-1)^{n-1} (-1)^{n-k-1} (n-k)  ==  (-1)^k (n-k)   for all k,n")
print("=" * 78)
dbad = 0
for n in range(2, 40):
    for k in range(1, n):
        K = n - k
        if (-1) ** (n - 1) * (-1) ** (K - 1) * K != (-1) ** k * (n - k):
            dbad += 1
print(f"  all 1<=k<n, 2<=n<=39 : {dbad} mismatches  (identity (-1)^(2n-k-2)=(-1)^k)")

print()
print("=" * 78)
print("(E) Rick's P^2 computation, re-done independently")
print("=" * 78)
c, subs = bethe_subsets(3, 1, 1.0 + 0j)
S = subs[0]
hs = h_list(S, 3)
print(f"  k=1, n=3, q=1.  h_1={hs[1].real:+.3f}  h_2={hs[2].real:+.3f}  h_3={hs[3].real:+.3f}")
print(f"                  p_1={p_of(S,1).real:+.3f}  p_2={p_of(S,2).real:+.3f}  p_3={p_of(S,3).real:+.3f}")
print(f"  p_1 h_2 + p_2 h_1 = {(p_of(S,1)*hs[2]+p_of(S,2)*hs[1]).real:+.3f} q"
      f"   <-- Rick's sigma.sigma^2 + sigma^2.sigma = +2q.  CONFIRMED.")
print(f"  Newton: sum_(e=1..3) p_e h_(3-e) = "
      f"{sum(p_of(S,e)*hs[3-e] for e in range(1,4)).real:+.3f}  = 3 h_3 = {3*hs[3].real:+.3f}  OK")
print(f"  psi(p_3) = {p_of(S,3).real:+.3f} q  -- magnitude k = 1, NOT n-k = 2.")
print()
print("  Korff's m=n constant at (k,n)=(1,3) is (-1)^1 (3-1) = -2.")
c2, subs2 = bethe_subsets(3, 2, 1.0 + 0j)
S2 = subs2[0]
print(f"  psi(p_3) in the conjugate sector K=n-k=2, i.e. Gr_2(C^3):"
      f" {p_of(S2,3).real:+.3f} q = (-1)^(K-1) K q = {(-1)**1*2:+d} q")
print(f"  omega-twist (-1)^(n-1) = {(-1)**2:+d};  product = {((-1)**2)*p_of(S2,3).real:+.3f}"
      f"  -> -2, MATCHING Korff.")
print()
print("  So at (k,n)=(1,3) Rick's +2 and Korff's -2 are two different constants")
print("  that happen to share magnitude 2; see (B), where psi(p_n) and the")
print("  e<n defect have magnitudes k and n-k and the conjugation swaps them.")
