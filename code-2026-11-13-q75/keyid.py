"""Key Identity (odd and even) of Rick Q75 §3, checked termwise.

LHS: M_alpha^perp R_s computed from the pairing only:
     [R_gamma] M_alpha^perp R_s = [F_s](M_alpha F_gamma)   (shuffle engine).
RHS: built in the RIBBON basis of NSym with R_a R_b = R_{a.b} + R_{a|b}
     (concatenation + near-concatenation); W := Psi^{-1} computed as a
     formal series inverse, NOT from Rick's (G-odd).  z is a grading variable.
"""
import sys
from itertools import product
from qsym import comp_to_mask, mask_to_comp, M_in_F, qsym_mul, F_product

def compositions(n):
    if n == 0:
        yield (); return
    for first in range(1, n + 1):
        for rest in compositions(n - first):
            yield (first,) + rest

# NSym in ribbon basis: dict comp -> coeff ; () is the unit.
def nmul(a, b):
    out = {}
    for x, cx in a.items():
        for y, cy in b.items():
            if not x or not y:
                keys = [x + y]
            else:
                keys = [x + y, x[:-1] + (x[-1] + y[0],) + y[1:]]
            for k in keys:
                out[k] = out.get(k, 0) + cx * cy
    return {k: v for k, v in out.items() if v}

def nadd(a, b, c=1):
    out = dict(a)
    for k, v in b.items():
        out[k] = out.get(k, 0) + c * v
    return {k: v for k, v in out.items() if v}

# z-series: list indexed by z-degree n of homogeneous NSym elements of degree n
N = int(sys.argv[1])            # z-degree cutoff
def smul(A, B):
    C = [dict() for _ in range(N + 1)]
    for p in range(N + 1):
        for q in range(N + 1 - p):
            if A[p] and B[q]:
                C[p + q] = nadd(C[p + q], nmul(A[p], B[q]))
    return C
Psi = [({(n,): 1} if n % 2 == 0 and n > 0 else ({(): 1} if n == 0 else {})) for n in range(N + 1)]
Theta = [({(n,): 1} if n % 2 == 1 else {}) for n in range(N + 1)]
U = [dict()] + [{k: -v for k, v in Psi[n].items()} for n in range(1, N + 1)]   # U = 1 - Psi
# W = sum_r U^r
W = [dict() for _ in range(N + 1)]; W[0] = {(): 1}
P = [dict() for _ in range(N + 1)]; P[0] = {(): 1}
for r in range(1, N + 1):
    P = smul(P, U)
    W = [nadd(W[n], P[n]) for n in range(N + 1)]
# sanity: W*Psi = 1
WP = smul(W, Psi)
assert WP[0] == {(): 1} and all(not WP[n] for n in range(1, N + 1)), 'W Psi != 1'
WT = smul(W, Theta)

# (G-odd): W_{2k} = (-1)^k R_(2^k);  (G-even): (W Theta)_{2k+1} = (-1)^k R_(2^k,1)
for k in range(0, N // 2 + 1):
    assert W[2 * k] == ({(2,) * k: (-1) ** k} if k else {(): 1}), ('G-odd', k, W[2*k])
    assert all(not W[2 * k + 1] for _ in [0]) if 2 * k + 1 <= N else True
for k in range(0, (N - 1) // 2 + 1):
    assert WT[2 * k + 1] == {(2,) * k + (1,): (-1) ** k}, ('G-even', k)
print('G-odd and G-even hold up to z-degree', N)

def perp_M(alpha, s_comp):
    """M_alpha^perp R_s in R-basis via the pairing."""
    i = sum(alpha); d = sum(s_comp); j = d - i
    smask = comp_to_mask(s_comp)
    Ma = M_in_F(comp_to_mask(alpha), i)
    out = {}
    if j == 0:
        c = Ma.get(smask, 0)
        return {(): c} if c else {}
    for g in compositions(j):
        prod = qsym_mul(Ma, i, {comp_to_mask(g): 1}, j)
        c = prod.get(smask, 0)
        if c: out[g] = c
    return out

def power(X, o):
    R = [dict() for _ in range(N + 1)]; R[0] = {(): 1}
    for _ in range(o): R = smul(R, X)
    return R

cnt = bad = 0; nonzero = 0
for k in range(1, N // 2 + 1):          # odd case: s = (2^k), d = 2k
    s = (2,) * k; d = 2 * k
    for i in range(1, d + 1):
        for alpha in compositions(i):
            l = len(alpha); o = sum(a % 2 for a in alpha)
            rhs = smul(power(WT, o), W)[d - i]
            rhs = {g: (-1) ** (l + k) * v for g, v in rhs.items()}
            lhs = perp_M(alpha, s)
            cnt += 1; nonzero += bool(lhs)
            if lhs != rhs:
                bad += 1
                if bad < 5: print('ODD FAIL', s, alpha, lhs, rhs)
print('Key Identity (odd): %d alpha checked, %d bad, %d with nonzero LHS' % (cnt, bad, nonzero))

cnt = bad = 0; zero_even_end = 0; nonzero = 0
for k in range(1, (N - 1) // 2 + 1):    # even case: s = (2^k,1), d = 2k+1
    s = (2,) * k + (1,); d = 2 * k + 1
    for i in range(1, d + 1):
        for alpha in compositions(i):
            l = len(alpha); o = sum(a % 2 for a in alpha)
            lhs = perp_M(alpha, s)
            if alpha[-1] % 2 == 0:
                rhs = {}
            else:
                A = smul(power(WT, o + 1), [dict()]*0 + [{(): 1}] + [dict()] * N)[d - i]
                B = power(WT, o - 1)[d - i]
                rhs = {g: (-1) ** (l + k) * v for g, v in nadd(A, B, -1).items()}
            cnt += 1; nonzero += bool(lhs)
            if lhs != rhs:
                bad += 1
                if bad < 5: print('EVEN FAIL', s, alpha, lhs, rhs)
print('Key Identity (even): %d alpha checked, %d bad, %d with nonzero LHS' % (cnt, bad, nonzero))
