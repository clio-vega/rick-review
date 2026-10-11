"""The |lambda|<=8 cross-check table owed for registry node clio-thmC-two-row-two-part.
Columns (as specified in the node's own `note` field):
  A  my Theorem C closed form (printed formula, evaluated)
  C  ground truth  sum_nu K_{nu,lambda}(t) chi^nu_rho
  D  (extra, not requested) [P_lambda] p_rho computed directly from Macdonald III (2.2)
     Hall-Littlewood polynomials -- independent of both A and C.
Column B (Rick's Sec 3(b) substitution verbatim) needs him to print it; left empty.

Characters chi^nu_rho: Murnaghan-Nakayama, validated by orthogonality and dimension.
K_{nu,lambda}(t) for two-row lambda: by dominance K=0 unless nu >= lambda, so nu is
two-row; exactly one SSYT of shape (n-j,j), content (n-k,k) (row 2 all 2s, row 1
forced), and K is monic of degree n(lambda)-n(nu)=k-j [Macdonald III (6.5)],
so K = t^{k-j}.  BOTH of those facts are verified against engine B below."""
from fractions import Fraction
from functools import lru_cache
from ring import partitions, nstat, conj
import hl, green

# ---------------- Murnaghan-Nakayama characters ----------------
@lru_cache(maxsize=None)
def chi(nu, rho):
    """character of S_n, irrep nu, class rho, by Murnaghan-Nakayama"""
    if sum(nu) == 0: return 1
    r = rho[0]; rest = rho[1:]
    tot = 0
    # remove a border strip of size r from nu in all ways
    for mu, ht in border_strips(nu, r):
        tot += (-1)**ht * chi(mu, rest)
    return tot

@lru_cache(maxsize=None)
def border_strips(nu, r):
    """all (mu, height) with nu/mu a border (rim hook) strip of size r"""
    out = []
    # use the beta-number / first-column hook length encoding
    l = len(nu)
    beta = [nu[i] + (l-1-i) for i in range(l)]           # strictly decreasing
    bset = set(beta)
    for b in beta:
        if b - r < 0: continue
        if (b - r) in bset: continue
        nb = sorted([x for x in beta if x != b] + [b-r], reverse=True)
        # height = number of rows the strip spans - 1 = # of beta between b-r and b
        ht = sum(1 for x in beta if b-r < x < b)
        mu = tuple(nb[i] - (l-1-i) for i in range(l))
        if any(x < 0 for x in mu): continue
        mu = tuple(x for x in mu if x > 0)
        if sum(mu) != sum(nu) - r: continue
        out.append((mu, ht))
    return tuple(out)

def validate_chars(NMAX=8):
    import math
    bad = []
    for n in range(1, NMAX+1):
        parts = list(partitions(n))
        # class sizes
        def csize(rho):
            from collections import Counter
            c = Counter(rho)
            z = 1
            for v, m in c.items(): z *= (v**m) * math.factorial(m)
            return math.factorial(n)//z
        for i, nu in enumerate(parts):
            # dimension = # SYT via hook length formula
            cj = conj(nu)
            hooks = 1
            for a in range(len(nu)):
                for b in range(nu[a]):
                    hooks *= (nu[a]-b) + (cj[b]-a) - 1
            dim = math.factorial(n)//hooks
            if chi(nu, tuple([1]*n)) != dim: bad.append(("dim", nu))
            for mu in parts[i:]:
                s = sum(csize(r)*chi(nu, r)*chi(mu, r) for r in parts)
                if s != (math.factorial(n) if nu == mu else 0):
                    bad.append(("orth", nu, mu, s))
    return bad

# ---------------- K_{nu,lambda}(t) for two-row lambda, verified ----------------
def count_ssyt_two_row(nu, lam):
    """# SSYT of shape nu (<=2 rows) and content lam (<=2 parts), brute force"""
    if len(nu) > 2 or len(lam) > 2: return None
    n1, n2 = nu[0], (nu[1] if len(nu) > 1 else 0)
    c1, c2 = lam[0], (lam[1] if len(lam) > 1 else 0)
    cnt = 0
    # row1: a ones then (n1-a) twos ; row2: all twos (column strict with entries in {1,2})
    for a in range(0, n1+1):
        row1 = [1]*a + [2]*(n1-a); row2 = [2]*n2
        if a + 0 != c1: continue
        if (n1-a) + n2 != c2: continue
        if any(row1[i] >= row2[i] for i in range(n2)): continue
        cnt += 1
    return cnt

def K_two_row(nu, lam):
    """t^{k-j} as {exp: Fraction}"""
    j = nu[1] if len(nu) > 1 else 0
    k = lam[1] if len(lam) > 1 else 0
    return {k-j: Fraction(1)}

def verify_K_against_engineB(NMAX=5):
    """K_{nu,lam}(t) from  s_nu = sum_lam K_{nu,lam}(t) P_lam(x;t), engine B, 2 variables
    (P_kappa = 0 in 2 vars for l(kappa)>2, and s_nu = 0 in 2 vars for l(nu)>2)."""
    bad = []
    for n in range(1, NMAX+1):
        # s_nu in 2 variables, nu two-row: bialternant
        for j in range(0, n//2 + 1):
            nu = (n,) if j == 0 else (n-j, j)
            # s_nu(x1,x2) = sum_{i=0}^{n-2j} x1^{n-j-i} x2^{j+i}
            s = {}
            for i in range(0, n-2*j+1):
                s[(n-j-i, j+i)] = hl.ac(1)
            cur = s; got = {}
            for k in range(0, n//2 + 1):
                lam = (n,) if k == 0 else (n-k, k)
                key = tuple(list(lam) + [0]*(2-len(lam)))
                c = cur.get(key, {})
                if c:
                    got[lam] = c
                    P = hl.P_HL(lam, 2)
                    cur = hl.Psub(cur, {a: hl.amul(c, cc) for a, cc in P.items()})
            assert not {a: c for a, c in cur.items() if c}, ("residue", nu)
            for k in range(0, n//2 + 1):
                lam = (n,) if k == 0 else (n-k, k)
                want = K_two_row(nu, lam) if (j <= k) else {}
                have = {e: v for e, v in got.get(lam, {}).items() if v}
                nssyt = count_ssyt_two_row(nu, lam)
                if have != want: bad.append(("K", nu, lam, have, want))
                if j <= k and nssyt != 1: bad.append(("ssyt-count", nu, lam, nssyt))
    return bad

if __name__ == "__main__":
    b = validate_chars(8)
    print(f"character engine (Murnaghan-Nakayama) validation, n<=8: {len(b)} problems "
          f"(dimension via hook length + full orthogonality)")
    b2 = verify_K_against_engineB(5)
    print(f"K_{{nu,lam}}(t) = t^{{k-j}} and 'exactly one SSYT', vs engine B, n<=5: {len(b2)} problems")
    for x in b2[:4]: print("   ", x)

    # ---- the table ----
    NMAX = 8
    print(f"\n=== clio-thmC-two-row-two-part cross-check, |lambda| <= {NMAX} ===")
    print("   A = my Thm C closed form | C = sum_nu K chi (ground truth) | D = [P_lam]p_rho via HL polys")
    agreeAC = agreeAD = tot = 0; mism = []
    rows = []
    for n in range(2, NMAX+1):
        for k in range(1, n//2 + 1):
            lam = (n-k, k)
            for y in range(1, n//2 + 1):
                x = n - y
                rho = (x, y)
                # A: my printed Theorem C
                mmin = min(x, y); a_, b_ = lam
                def acc(pairs):
                    d = {}
                    for e, v in pairs: d[e] = d.get(e, Fraction(0)) + v
                    return {e: v for e, v in d.items() if v}
                if mmin == b_:
                    A = acc([(0, Fraction(1 + (1 if a_ == b_ else 0))), (b_-1, Fraction(-1)), (b_, Fraction(1))])
                elif 1 <= mmin <= b_-1:
                    A = acc([(b_-1, Fraction(-1)), (b_, Fraction(1)),
                             (b_-mmin-1, Fraction(-1)), (b_-mmin, Fraction(1))])
                else:
                    A = acc([(b_-1, Fraction(-1)), (b_, Fraction(1))])
                # C: ground truth sum_nu K_{nu,lam}(t) chi^nu_rho   (nu two-row by dominance)
                C = {}
                for j in range(0, k+1):
                    nu = (n,) if j == 0 else (n-j, j)
                    ch = chi(nu, rho)
                    if ch:
                        for e, v in K_two_row(nu, lam).items():
                            C[e] = C.get(e, Fraction(0)) + v*ch
                C = {e: v for e, v in C.items() if v}
                # D: direct
                D = {e: v for e, v in green.green_two_row(rho).get(lam, {}).items() if v}
                tot += 1
                agreeAC += (A == C); agreeAD += (A == D)
                if not (A == C == D): mism.append((lam, rho, A, C, D))
                rows.append((lam, rho, C))
    print(f"   {tot} (lambda,rho) pairs:  A==C in {agreeAC},  A==D in {agreeAD},  all three agree in {tot-len(mism)}")
    for m in mism[:5]: print("   MISMATCH", m)
    def fmt(d):
        if not d: return "0"
        return " ".join(("+" if v > 0 else "-") + (f"{abs(v)}" if abs(v) != 1 or e == 0 else "") + (f"t^{e}" if e > 1 else ("t" if e == 1 else "")) for e, v in sorted(d.items()))
    print("\n   lambda      rho       Y^lambda_rho(t)  (columns A, C, D all equal)")
    for lam, rho, C in rows:
        print(f"   {str(lam):10s} {str(rho):9s} {fmt(C)}")
