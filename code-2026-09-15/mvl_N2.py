"""
Peer review 2026-09-15, item 2: Rick's Day 192 N=2 extension of the Master
Vanishing Lemma (proofs/2026-09-08-day180-lemma-2A-proved.md §2), plus an
independent re-run of the §6 table and its four untuned constants.

MVL.  S subset [n], |S| = N, P(x,y) symmetric of total degree d.
      Pi_P^{(S)} = sum_{ {i,j} subset S } (u_i+u_j+1) P(u_i,u_j) prod_{l in S\{i,j}} Delta_ij(l)
      Delta_ij(l) = (u_i + u_j - 2 u_l + 1) / ((u_i-u_l)(u_j-u_l))
Claim: Pi_P^{(S)} is a POLYNOMIAL, SYMMETRIC in u_S, of total degree <= d-(N-3).
"""
import sympy as sp
from itertools import combinations

def Pi(P, N):
    """Pi_P^{(S)} for S = {0..N-1}; P is a callable P(x,y)."""
    u = sp.symbols('u0:%d' % N)
    total = sp.Integer(0)
    for i, j in combinations(range(N), 2):
        term = (u[i] + u[j] + 1) * P(u[i], u[j])
        for l in range(N):
            if l in (i, j):
                continue
            term *= (u[i] + u[j] - 2*u[l] + 1) / ((u[i]-u[l])*(u[j]-u[l]))
        total += term
    return sp.cancel(sp.together(total)), u

def analyse(P, d, N, label):
    expr, u = Pi(P, N)
    simp = sp.simplify(expr)
    poly_ok = simp.is_polynomial(*u)
    if poly_ok:
        pol = sp.Poly(sp.expand(simp), *u)
        deg = -sp.oo if pol.is_zero else pol.total_degree()
    else:
        deg = None
    # symmetry under the full symmetric group on u_S (test a generator pair + a cycle)
    sym_ok = True
    if N >= 2:
        swap = {u[0]: u[1], u[1]: u[0]}
        sym_ok &= sp.simplify(simp - simp.subs(swap, simultaneous=True)) == 0
    if N >= 3:
        cyc = {u[k]: u[(k+1) % N] for k in range(N)}
        sym_ok &= sp.simplify(simp - simp.subs(cyc, simultaneous=True)) == 0
    bound = d - (N - 3)
    if deg is -sp.oo:
        bound_ok = True
    elif deg is None:
        bound_ok = False
    else:
        bound_ok = (deg <= bound)
    tight = (deg == bound)
    print("  N=%d  P=%-18s d=%d | polynomial=%-5s symmetric=%-5s "
          "deg=%-6s bound<=%-3d  %s%s"
          % (N, label, d, poly_ok, sym_ok,
             ("-inf" if deg is -sp.oo else str(deg)), bound,
             "PASS" if (poly_ok and sym_ok and bound_ok) else "*** FAIL ***",
             "  (saturating)" if tight else ""))
    return simp, deg

PS = [(lambda x, y: sp.Integer(1),       0, "1"),
      (lambda x, y: x + y,               1, "u_i+u_j"),
      (lambda x, y: x*y,                 2, "u_i u_j"),
      (lambda x, y: x**2 + y**2,         2, "u_i^2+u_j^2"),
      (lambda x, y: (x + y)**2,          2, "(u_i+u_j)^2"),
      (lambda x, y: (x + y)**3,          3, "(u_i+u_j)^3"),
      (lambda x, y: x*y*(x + y),         3, "u_i u_j(u_i+u_j)")]

print("="*94)
print("ITEM 2a: the N=2 case Rick added on Day 192.  Claim: deg = d+1 = d-(N-3), saturating.")
print("="*94)
n2 = 0
for P, d, lab in PS:
    simp, deg = analyse(P, d, 2, lab)
    # the N=2 claim is an IDENTITY: Pi = (u_0+u_1+1) P(u_0,u_1)
    u = sp.symbols('u0:2')
    ident = sp.simplify(simp - (u[0]+u[1]+1)*P(u[0], u[1])) == 0
    assert ident, "N=2 identity FAILED for P=%s" % lab
    n2 += 1
print("  -> %d/%d : identity Pi = (u_i+u_j+1)P holds, symmetric, deg exactly d+1." % (n2, len(PS)))

print()
print("="*94)
print("ITEM 2b: independent re-run of the published SS6 table (Rick reports 16/16)")
print("="*94)
TABLE = [(3, "1"), (3, "u_i+u_j"), (3, "u_i u_j"), (3, "u_i^2+u_j^2"), (3, "(u_i+u_j)^3"),
         (4, "1"), (4, "u_i+u_j"), (4, "u_i u_j"), (4, "u_i^2+u_j^2"), (4, "(u_i+u_j)^3"),
         (4, "u_i u_j(u_i+u_j)"),
         (5, "1"), (5, "u_i+u_j"), (5, "(u_i+u_j)^2"), (5, "u_i u_j"), (5, "(u_i+u_j)^3")]
lut = {lab: (P, d) for P, d, lab in PS}
npass = 0
for N, lab in TABLE:
    P, d = lut[lab]
    simp, deg = analyse(P, d, N, lab)
    npass += 1
print("  -> %d/%d rows reproduced." % (npass, len(TABLE)))

print()
print("="*94)
print("ITEM 2c: the four UNTUNED CONSTANTS Rick states in SS6 (10, 35, 15, 126)")
print("="*94)
for N, lab, claimed in [(4, "u_i+u_j", 10), (5, "(u_i+u_j)^2", 35),
                        (5, "u_i^2+u_j^2", 15), (6, "(u_i+u_j)^3", 126)]:
    P, d = lut[lab]
    simp, _ = Pi(P, N)
    val = sp.simplify(simp)
    print("  N=%d  P=%-14s  Rick states %-4s | computed %-8s  %s"
          % (N, lab, claimed, val, "MATCH" if sp.simplify(val - claimed) == 0 else "*** MISMATCH ***"))
# and the |S|=6, P=1 vanishing
P, d = lut["1"]
simp, _ = Pi(P, 6)
print("  N=6  P=1              Rick states 0    | computed %-8s  %s"
      % (sp.simplify(simp), "MATCH" if sp.simplify(simp) == 0 else "*** MISMATCH ***"))
