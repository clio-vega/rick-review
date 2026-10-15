"""
INDEPENDENT verification of Rick's Day 207b Theorem 1.

I implement the affine Hecke action (T_i, pi, Y_i) from scratch, in sympy, and
compare e_k(Y) . e_r against his closed form.  This shares no code with his
scripts/day207b, so agreement is corroboration by a second mechanism.

Conventions taken from the note, and CROSS-CHECKED against Hikita's own source
(/tmp/hikita/qt-CSF.tex, proof of Lem_iota_elem = his Lemma 3.3), which prints
    Y_i = t^{m-i} T_{i-1}...T_1 Pi T_{m-1}^{-1}...T_i^{-1}
    T_i F = t s_i F + (t-1) X_{i+1} (s_i F - F)/(X_i - X_{i+1})
    pi F  = X_1 F(X_2,...,X_m, s X_1),            s = q^{-1}
Clio, 2026-10-15.
"""
import sympy as sp
from itertools import combinations
import sys

def run(m, s_, t_, kmax, rmax, label, verbose=False):
    X = sp.symbols(f'X1:{m+1}')                     # X[0]..X[m-1] = X_1..X_m
    s, t = s_, t_

    def sw(F, i):                                   # s_i : swap X_i, X_{i+1}  (1-indexed i)
        a, b = X[i-1], X[i]
        return F.subs({a: b, b: a}, simultaneous=True)

    def T(F, i):
        sF = sw(F, i)
        return sp.expand(sp.cancel(t*sF + (t-1)*X[i]*sp.cancel((sF - F)/(X[i-1] - X[i]))))

    def Tinv(F, i):                                 # T^-1 = t^-1 T - (1 - t^-1)
        return sp.expand(sp.cancel(T(F, i)/t - (1 - 1/t)*F))

    def Pi(F):
        sub = {X[a]: X[a+1] for a in range(m-1)}    # X_1->X_2, ..., X_{m-1}->X_m
        sub[X[m-1]] = s*X[0]                       # X_m -> s X_1
        return sp.expand(X[0]*F.subs(sub, simultaneous=True))

    def Y(F, i):                                    # Y_i acting on F
        G = F
        for a in range(i, m):                       # (T_i ... T_{m-1})^-1 : T_i^-1 first
            G = Tinv(G, a)
        G = Pi(G)
        for a in range(1, i):                       # T_{i-1}...T_1 : T_1 first
            G = T(G, a)
        return sp.expand(t**(m-i)*G)

    def eY(F, k):                                   # e_k(Y) . F, Y_{b_k} acts first
        tot = sp.Integer(0)
        for comb in combinations(range(1, m+1), k):
            G = F
            for i in reversed(comb):
                G = Y(G, i)
            tot += G
        return sp.expand(tot)

    def e(r):                                       # e_r(X_1..X_m)
        if r < 0 or r > m: return sp.Integer(0)
        return sp.expand(sum(sp.prod([X[i] for i in c]) for c in combinations(range(m), r)))

    # ---- his coefficients ----
    def qp(a, n):
        r = sp.Integer(1)
        for i in range(n): r *= (1 - a*t**i)
        return r
    A = {-1: sp.Integer(0)}
    def al(j):
        if j in A: return A[j]
        num = sp.Integer(1)
        for i in range(1, j+1): num *= (s - t**i)
        A[j] = sp.cancel(num/qp(t, j)); return A[j]
    def c(n, j):
        if not (0 <= j <= n): return sp.Integer(0)
        return sp.cancel(qp(s, n-j)/qp(t, n-j)*(al(j) - s*t**(n-j)*al(j-1)))
    def F_(n, wv):
        return sp.cancel(sum(c(n, j)*wv**j for j in range(n+1)))

    binom2 = lambda k: k*(k-1)//2
    res = []
    # --- calibration A: Hikita Lemma 3.3 ---
    for k in range(1, min(kmax, m)+2):
        lhs = eY(sp.Integer(1), k)
        rhs = sp.expand(t**binom2(k)*e(k))
        res.append((f"cal e_{k}(Y).1 = t^C({k},2) e_{k}", sp.simplify(sp.expand(lhs-rhs)) == 0))
    # --- main: Theorem 1 ---
    for k in range(1, kmax+1):
        for r in range(0, rmax+1):
            lhs = sp.expand(sp.cancel(t**(-binom2(k))*eY(e(r), k)))
            rhs = sp.expand(sum(sp.cancel(s**b*F_(k-b, t**(r-b)))*e(b)*e(r+k-b)
                                for b in range(k+1)))
            ok = sp.simplify(sp.expand(sp.cancel(lhs-rhs))) == 0
            res.append((f"Thm1  m={m} k={k} r={r}", ok))
            if verbose and not ok:
                print("   lhs-rhs =", sp.factor(sp.simplify(sp.expand(sp.cancel(lhs-rhs)))))
    npass = sum(1 for _, o in res if o)
    print(f"[{label}]  m={m}  {npass}/{len(res)} PASS")
    for nm, o in res:
        if not o: print(f"      *** FAIL: {nm}")
    return res, npass, len(res)

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "sym"
    if which == "sym":
        s, t = sp.symbols('s t')
        print("### fully symbolic s,t ###")
        tot = p = 0
        for m in (1, 2):
            _, a, b = run(m, s, t, kmax=min(m,2), rmax=2, label="symbolic")
            p += a; tot += b
        print(f"### symbolic total {p}/{tot}")
    else:
        s, t = sp.Rational(5,7), sp.Rational(3,5)
        print(f"### exact rationals s={s} t={t} ###")
        tot = p = 0
        for m, kmax, rmax in [(1,1,3),(2,2,3),(3,3,3),(4,3,2)]:
            _, a, b = run(m, s, t, kmax=kmax, rmax=rmax, label="rational")
            p += a; tot += b
        print(f"### rational total {p}/{tot}")
