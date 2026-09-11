"""Independent enumeration of the Shareshian-Wachs chromatic quasisymmetric function
X_{P_n}(t) for the directed path P_n, then Rick's Day 190 (q,t) chain, checked
against Hikita Example 4.6 read from the arXiv source."""
import itertools, sympy as sp
from collections import defaultdict

t, q = sp.symbols('t q')

def X_path(n, N):
    """X_{P_n}(x_1..x_N; t) = sum over proper colorings kappa of the path 1-2-...-n
       t^{asc(kappa)} prod x_{kappa(i)},  asc = #{i : kappa(i) < kappa(i+1)}  (SW convention)"""
    mono = defaultdict(lambda: sp.Integer(0))
    for kappa in itertools.product(range(1, N+1), repeat=n):
        if any(kappa[i] == kappa[i+1] for i in range(n-1)):
            continue                      # proper: adjacent vertices differ
        asc = sum(1 for i in range(n-1) if kappa[i] < kappa[i+1])
        mono[tuple(sorted(kappa))] += t**asc
    return mono

def e_expand(n, N, mono):
    """Express the monomial-expansion in the e-basis by linear algebra on monomials."""
    x = sp.symbols(f'x1:{N+1}')
    def e(r): return sp.expand(sp.polys.specialpolys.symmetric_poly(r, x)) if r > 0 else sp.Integer(1)
    parts = list(sp.utilities.iterables.partitions(n, m=n))
    lams = []
    for p in sp.utilities.iterables.ordered_partitions(n):
        lams.append(tuple(sorted(p, reverse=True)))
    lams = sorted(set(lams), reverse=True)
    target = sp.expand(sum(c * sp.prod([x[i-1] for i in k]) for k, c in mono.items()))
    cs = sp.symbols(f'c0:{len(lams)}')
    expr = sp.expand(target - sum(cs[i]*sp.prod([e(r) for r in lam]) for i, lam in enumerate(lams)))
    sol = sp.solve(sp.Poly(expr, *x).coeffs(), cs, dict=True)
    assert sol, "no e-expansion"
    return {lam: sp.factor(sp.simplify(sol[0].get(cs[i], cs[i]))) for i, lam in enumerate(lams)}

print("== Ordinary CQF X_{P_n}(t), independently enumerated (SW ascent statistic) ==")
ord_cqf = {}
for n, N in ((2, 4), (3, 6)):
    ec = e_expand(n, N, X_path(n, N))
    ord_cqf[n] = ec
    print(f"  X_P{n}(t) = " + "  +  ".join(f"({v}) e_{list(k)}" for k, v in ec.items() if v != 0))

print("\n== Rick's Day 190 claims ==")
print("  claim X_P2(t) = (1+t) e_2                  :",
      "MATCH" if sp.simplify(ord_cqf[2][(2,)] - (1+t)) == 0 else "MISMATCH")
print("  claim X_P3(t) = (1+t+t^2) e_3 + t e_{2,1}  :",
      "MATCH" if sp.simplify(ord_cqf[3][(3,)] - (1+t+t**2)) == 0
                 and sp.simplify(ord_cqf[3][(2,1)] - t) == 0 else "MISMATCH")

# ---- apply q-map:  q(e_lambda(Y)) = t^{sum binom(lam_i,2)} e^{(q,t)}_lambda  (Hikita Thm B(iv)) ----
def shape(lam): return sum(sp.binomial(l, 2) for l in lam)
print("\n== Apply Hikita Thm B(iii)+(iv) ==")
c2 = ord_cqf[2][(2,)] * t**shape((2,))
print(f"  X_P2(q,t) = {sp.factor(c2)} e_2      [Rick: t(1+t) e_2]",
      "  MATCH" if sp.simplify(c2 - t*(1+t)) == 0 else "  MISMATCH")

c3_e3   = ord_cqf[3][(3,)]  * t**shape((3,))     # coefficient of e^{(q,t)}_3 = e_3
c3_e21  = ord_cqf[3][(2,1)] * t**shape((2,1))    # coefficient of e_1 star e_2  (lambda=(2,1))
print(f"  X_P3(q,t) = {sp.factor(c3_e3)} e_3 + {sp.factor(c3_e21)} (e_1 star e_2)")
print(f"    [Rick:    t^3(1+t+t^2) e_3 + t^2 (e_1 star e_2)]",
      " MATCH" if sp.simplify(c3_e3 - t**3*(1+t+t**2)) == 0 and sp.simplify(c3_e21 - t**2) == 0 else " MISMATCH")

# ---- unfold via Hikita Thm 3.12 Pieri:  e_1 * e_r = (1-q^-1)[r+1]_t e_{r+1} + q^-1 e_1 e_r ----
r = 2
qt_int = sum(t**i for i in range(r+1))            # [r+1]_t = [3]_t = 1+t+t^2
star_e3   = (1 - q**-1) * qt_int
star_e1e2 = q**-1
tot_e3   = sp.expand(c3_e3 + c3_e21 * star_e3)
tot_e1e2 = sp.expand(c3_e21 * star_e1e2)
print("\n== Unfold with Hikita Thm 3.12 (Pieri), compare to Hikita Example 4.6 ==")
print(f"  computed : {sp.factor(tot_e1e2)} e_{{2,1}} + {sp.factor(tot_e3)} e_3")
# Hikita Ex 4.6 (verbatim from arXiv source 2503.23597):
hik_e21 = q**-1 * t**2
hik_e3  = q**-1 * t**2 * (1+t+t**2) * (-1 + q + q*t)
print(f"  Hikita   : {sp.factor(hik_e21)} e_{{2,1}} + {sp.factor(hik_e3)} e_3")
d1 = sp.simplify(tot_e1e2 - hik_e21); d2 = sp.simplify(tot_e3 - hik_e3)
print(f"  diff_e21 = {d1}    diff_e3 = {d2}   ->  {'diff = 0 CONFIRMED' if d1==0 and d2==0 else '*** MISMATCH ***'}")
# Rick's own stated unfolded form
rick_e3 = q**-1*t**2*(1+t+t**2)*(-1+q*(1+t)); rick_e21 = q**-1*t**2
print(f"  Rick's stated unfolded form matches Hikita: "
      f"{'YES' if sp.simplify(rick_e3-hik_e3)==0 and sp.simplify(rick_e21-hik_e21)==0 else 'NO'}")

# ---- sanity check 2: Rick's Day 187 (Re) recursion at t=q ----
print("\n== Rick's (Re) recursion  X_Pn(q) = e_n + q sum_{k=2}^n [k-1]_q e_k X_{P_{n-k}}(q) ==")
def qint(k): return sum(q**i for i in range(k))
XP = {0: {(): sp.Integer(1)}, 1: {(1,): sp.Integer(1)}}
for n in (2, 3):
    tgt = {k: v.subs(t, q) for k, v in ord_cqf[n].items()}
    rec = defaultdict(lambda: sp.Integer(0)); rec[(n,)] += 1
    for k in range(2, n+1):
        for lam, c in XP[n-k].items():
            rec[tuple(sorted((k,)+lam, reverse=True))] += q*qint(k-1)*c
    ok = all(sp.simplify(tgt.get(l, 0) - rec.get(l, 0)) == 0 for l in set(tgt) | set(rec))
    print(f"  n={n}: recursion vs enumeration -> {'MATCH (diff 0)' if ok else '*** MISMATCH ***'}")
    XP[n] = tgt
