"""Sec 9, Example (two rows): verify the printed piecewise formula for Green
polynomials X^{(l1,l2)}_{(x,y)}(t), and the Jing-Liu general-class formula
X^lam_rho = pi_k + (t-1) sum_{j<k} t^{k-1-j} pi_j,  for ALL classes rho.

Independent route: P_kappa(x1,x2;t) = 0 whenever l(kappa) > 2, so in exactly two
variables  p_rho(x1,x2) = sum_{l(lam)<=2} X^lam_rho P_lam(x1,x2;t).
P_lam built from the Macdonald III (2.2) symmetrised sum (engine B, hl.py)."""
from fractions import Fraction
from ring import partitions
import hl

def Ppoly2(lam):
    """P_(l1,l2)(x1,x2;u) as {(e1,e2): {u_exp: Fraction}}"""
    return hl.P_HL(lam, 2)

def p_rho_2(rho):
    """power sum p_rho in 2 variables"""
    R = {(0, 0): hl.ac(1)}
    for r in rho:
        f = {(r, 0): hl.ac(1), (0, r): hl.ac(1)}
        R = hl.Pmul(R, f)
    return R

def green_two_row(rho):
    """returns {lam (two-row or one-row): X^lam_rho as {u_exp:Fraction}}"""
    n = sum(rho)
    cur = p_rho_2(rho)
    lams = [(n,)] + [(n-j, j) for j in range(1, n//2 + 1)]
    out = {}
    for lam in lams:
        key = tuple(list(lam) + [0]*(2-len(lam)))
        c = cur.get(key, {})
        if c:
            out[lam] = c
            P = Ppoly2(lam)
            cur = hl.Psub(cur, {a: hl.amul(c, cc) for a, cc in P.items()})
    left = {a: c for a, c in cur.items() if c}
    assert not left, ("residue after peeling two-row P's", rho, left)
    return out

def poly(d):
    return {k: v for k, v in d.items() if v}

def printed(l1, l2, x, y):
    """the printed piecewise formula; y <= x"""
    mxy = 2 if x == y else 1
    # NB: ACCUMULATE, never key a dict literal on exponents that can coincide.
    # (l2-y == l2-1 exactly when y==1, which silently dropped a term on first run.)
    def acc(pairs):
        d = {}
        for e, v in pairs: d[e] = d.get(e, Fraction(0)) + v
        return poly(d)
    if y < l2:   # (t-1) t^{l2-1-y} (1+t^y)  =  t^{l2-y} - t^{l2-1-y} + t^{l2} - t^{l2-1}
        return acc([(l2-1-y, Fraction(-1)), (l2-y, Fraction(1)),
                    (l2-1,   Fraction(-1)), (l2,   Fraction(1))])
    if y == l2:  # m_xy - (1-t) t^{l2-1}
        return acc([(0, Fraction(mxy)), (l2-1, Fraction(-1)), (l2, Fraction(1))])
    return acc([(l2-1, Fraction(-1)), (l2, Fraction(1))])   # (t-1) t^{l2-1}

def submultiset_sums(rho):
    """pi_j = # submultisets of the parts of rho with sum j  (= # j-subsets of [n] fixed by rho)"""
    n = sum(rho); pi = [0]*(n+1); pi[0] = 1
    for r in rho:
        for j in range(n, r-1, -1):
            pi[j] += pi[j-r]
    return pi

def jingliu(lam, rho):
    """X^lam_rho = pi_k + (t-1) sum_{j<k} t^{k-1-j} pi_j   for lam=(n-k,k)"""
    k = lam[1] if len(lam) > 1 else 0
    pi = submultiset_sums(rho)
    d = {0: Fraction(pi[k])}
    for j in range(0, k):
        e = k-1-j
        d[e]   = d.get(e, Fraction(0)) - pi[j]
        d[e+1] = d.get(e+1, Fraction(0)) + pi[j]
    return poly(d)

if __name__ == "__main__":
    NMAX = 10
    piece_ok = piece_bad = 0; jl_ok = jl_bad = 0; bad = []
    for n in range(2, NMAX+1):
        for rho in partitions(n):
            G = green_two_row(rho)
            for l2 in range(0, n//2 + 1):
                lam = (n,) if l2 == 0 else (n-l2, l2)
                X = poly(G.get(lam, {}))
                # Jing-Liu formula: every class rho
                J = jingliu(lam, rho)
                if X == J: jl_ok += 1
                else: jl_bad += 1; bad.append(("JL", lam, rho, X, J))
                # printed piecewise formula: only two-part classes rho=(x,y)
                if len(rho) == 2 and l2 >= 1:
                    x, y = rho[0], rho[1]
                    Pr = printed(lam[0], lam[1], x, y)
                    if X == Pr: piece_ok += 1
                    else: piece_bad += 1; bad.append(("PIECE", lam, rho, X, Pr))
    print(f"printed piecewise formula (two-part classes, |lam|<={NMAX}): {piece_ok} ok, {piece_bad} bad")
    print(f"Jing-Liu Thm 2.6 formula (ALL classes,      |lam|<={NMAX}): {jl_ok} ok, {jl_bad} bad")
    for b in bad[:6]: print("   ", b)
    # the claim that makes Thm D bite: diagonal class (x,y)=lam
    print("\n--- diagonal class (x,y)=lam: printed value t^{l2}-t^{l2-1}+m_xy, root in (-1,0)? ---")
    for lam in [(5,3),(7,3),(6,5),(8,5),(7,4),(8,4),(9,2),(6,6)]:
        n = sum(lam); X = poly(green_two_row(lam)[lam])
        def ev(tv): return sum(v*Fraction(tv)**k for k, v in X.items())
        pred = poly({lam[1]: Fraction(1), lam[1]-1: Fraction(-1), 0: Fraction(2 if lam[0]==lam[1] else 1)})
        inhyp = (lam[0] > lam[1]) and lam[1] >= 3 and lam[1] % 2 == 1
        print(f"  lam={lam}: closed form {'matches' if X==pred else 'MISMATCH'}"
              f"   X(-1)={str(ev(-1)):>3}  X(0)={ev(0)}  root in (-1,0): {str(ev(-1)*ev(0)<0):5s}"
              f"  in his hypothesis (l1>l2, l2>=3 odd): {inhyp}")
