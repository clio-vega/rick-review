"""
Clio 2026-09-18, peer review of Rick's Day 204 S5.

Structural analysis of tau_r^(3), from the dumps produced by tau3_dump.py.

(1) Conjecture 10 at k=3, clause 2 (non-top coefficients r-independent).
(2) Conjecture 10 at k=3, clause 1: is q^5 tau_r^(3) = A_0 + A_1 u + A_2 u^2 + A_3 u^3
    with u = t^r and A_j in Q(q,t) independent of r?  Fit on four r's, test on the rest.
(3) If yes: divisibility by [r+3]_t is then an r-INDEPENDENT question about A(u),
    and the per-r answer is governed by which cyclotomics divide one fixed polynomial.
    That decides between "generic divisibility with a gcd-3 obstruction" (Rick) and
    "finitely many accidental n" -- and predicts every further row without computing it.
"""
import json, sys, glob
import sympy as sp
from sympy import symbols, Rational

q, t, u = symbols('q t u')

def load(r):
    d = json.load(open("tau3_r%d.json" % r))
    return d, {eval(k): sp.sympify(v) for k, v in d["coeffs"].items()}

RS = sorted(int(f.split("_r")[1].split(".")[0]) for f in glob.glob("tau3_r*.json"))
print("have r =", RS)
DATA = {r: load(r) for r in RS}

# ---------- (1) non-top coefficients r-independent? ----------
print("\n" + "="*72)
print("(1) Conj 10 clause 2: are the NON-TOP coefficients r-independent?")
shape = ["(r+3)", "(r+2,1)", "(r+1,2)", "(r+1,1,1)", "(r,3)", "(r,2,1)", "(r,1,1,1)"]
def lam_of(r, which):
    return {"(r+3)": (r+3,), "(r+2,1)": (r+2,1), "(r+1,2)": (r+1,2), "(r+1,1,1)": (r+1,1,1),
            "(r,3)": tuple(sorted((r,3), reverse=True)), "(r,2,1)": tuple(sorted((r,2,1), reverse=True)),
            "(r,1,1,1)": tuple(sorted((r,1,1,1), reverse=True))}[which]
inrange = [r for r in RS if r >= 3]
for which in shape[1:]:
    vals = {}
    for r in inrange:
        _, co = DATA[r]
        vals[r] = sp.simplify(co.get(lam_of(r, which), sp.Integer(0)))
    base = vals[inrange[0]]
    same = all(sp.simplify(vals[r] - base) == 0 for r in inrange)
    print("  %-12s r-independent over r=%s : %s%s" % (which, inrange, same,
          "" if same else "   values " + str(vals)))
    if same:
        print("               = %s" % sp.factor(base))

# ---------- (2) fit the top coefficient ----------
print("\n" + "="*72)
print("(2) Conj 10 clause 1: q^5 tau_r^(3) = A_0 + A_1 u + A_2 u^2 + A_3 u^3 ?")
def tau(r):
    _, co = DATA[r]
    return sp.cancel(sp.together(co[(r+3,)] * q**5))

def fit(rs):
    """Solve the 4x4 Vandermonde in u = t^r for A_0..A_3."""
    A = symbols('A0 A1 A2 A3')
    eqs = [sp.Eq(sum(A[j]*t**(j*r) for j in range(4)), tau(r)) for r in rs]
    sol = sp.solve(eqs, A, dict=True)
    assert sol, "no solution"
    return [sp.cancel(sp.together(sol[0][a])) for a in A]

for rs in [(1,2,3,4), (3,4,5,6)]:
    if not set(rs) <= set(RS): 
        print("\n  fit on r=%s: SKIPPED (missing data)" % (rs,)); continue
    Aj = fit(rs)
    print("\n  --- fit on r = %s ---" % (rs,))
    for j, a in enumerate(Aj):
        print("     A_%d = %s" % (j, sp.factor(a)))
    tests = [r for r in RS if r not in rs]
    for r in tests:
        pred = sum(Aj[j]*t**(j*r) for j in range(4))
        ok = sp.simplify(sp.cancel(pred - tau(r))) == 0
        print("     UNTUNED TEST r=%d : %s" % (r, "PASS" if ok else "**FAIL**"))
        if not ok:
            print("        predicted-minus-actual =", sp.factor(sp.cancel(pred - tau(r))))

# ---------- (3) the r-independent divisibility question ----------
print("\n" + "="*72)
print("(3) Divisibility by [n]_t, n = r+3, decided ONCE for all r.")
print("    If q^5 tau_r = A(t^r) with A(u) = sum A_j u^j r-independent, then at a")
print("    primitive d-th root of unity zeta with d | n we have u = zeta^r = zeta^{-3},")
print("    so the vanishing condition is H(zeta) = 0 where H(t) := t^9 A_0 + t^6 A_1 + t^3 A_2 + A_3.")
print("    Hence [n]_t | q^5 tau_r  <=>  Phi_d | num(H) for EVERY d | n, d > 1.")
Aj = fit((1,2,3,4))
Au = sum(Aj[j]*u**j for j in range(4))
print("\n  A(u) factored:", sp.factor(Au))
print("\n  Is (1 - t^3 u) a factor of A(u)?  [ = Prediction 1 clause 1, for ALL r at once ]")
quo, rem = sp.div(sp.Poly(sp.numer(sp.cancel(sp.together(Au))), u), sp.Poly(sp.expand(1 - t**3*u), u))
print("     remainder =", sp.factor(sp.simplify(rem.as_expr())), "  -> divides?", sp.simplify(rem.as_expr()) == 0)

H = sp.cancel(sp.together(t**9*Aj[0] + t**6*Aj[1] + t**3*Aj[2] + Aj[3]))
Hn, Hd = sp.fraction(H)
print("\n  H(t) numerator factored:")
print("    ", sp.factor(Hn))
print("  H(t) denominator:", sp.factor(Hd))

print("\n  Which cyclotomics Phi_d divide num(H)?  (d = 2..30)")
D = []
for d in range(2, 31):
    Phi = sp.Poly(sp.cyclotomic_poly(d, t), t)
    _, rr = sp.div(sp.Poly(sp.expand(Hn), t), Phi)
    hit = sp.simplify(rr.as_expr()) == 0
    if hit: D.append(d)
print("    D = {d : Phi_d | num(H)} =", D)
print("    (denominator vanishes at:", sp.factor(Hd), ")")

print("\n  PREDICTION for every n, with no further computation:")
print("    [n]_t | q^5 tau_{n-3}  <=>  every divisor d>1 of n lies in D")
for n in range(4, 25):
    divs = [d for d in range(2, n+1) if n % d == 0]
    bad = [d for d in divs if d not in D]
    print("     n=%2d (r=%2d) divisors>1 %-18s %s%s" % (n, n-3, str(divs),
          "DIVIDES" if not bad else "FAILS", "" if not bad else "  (missing Phi_%s)" % bad))
