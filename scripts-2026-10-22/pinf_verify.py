"""
Independent verification of Rick's 2026-10-21 reply (UID 832), Targets 1a/1b.
Clio, 2026-10-22.  Nothing is imported from Rick's scripts: Psi is re-implemented
from the primitive localization sum; Lemma A is re-derived and CHECKED, not assumed.
Exact arithmetic throughout (Fraction for the big sums, sympy for the alternants).
"""
import itertools, random
from fractions import Fraction as Fr
random.seed(20261022)

# ------------------------------------------------- primitive definition (mine)
def rho(kappa, X, w):
    e = Fr(1)
    for k in range(1, kappa): e *= (1 - w[k]/X)
    return e

def Psi_perm(kap, th, M, w):
    """PRIMITIVE: sum over ordered r-tuples of distinct heads in M."""
    r = len(kap); tot = Fr(0)
    for h in itertools.permutations(M, r):
        X = [w[m] for m in h]; e = Fr(1)
        for j in range(r):
            e *= (1 - 1/X[j]**2) * rho(kap[j], X[j], w) * X[j]**th[j]
        for j in range(r):
            for k in range(j+1, r): e *= (1 - 1/(X[j]*X[k]))/(1 - X[j]/X[k])
        for t in M:
            if t in h: continue
            for j in range(r): e *= (1 - 1/(w[t]*X[j]))/(1 - w[t]/X[j])
        tot += e
    return tot

# ------------------------------------------------- Lemma A form (my derivation)
def S0(H, M, w):
    e = Fr(1)
    for m in H: e *= (1 - 1/w[m]**2)
    for a, b in itertools.combinations(sorted(H), 2): e *= (1 - 1/(w[a]*w[b]))
    for t in M:
        if t in H: continue
        for m in H: e *= (1 - 1/(w[t]*w[m]))/(1 - w[t]/w[m])
    return e

def det_frac(Mx):
    """Exact determinant by fraction-free-ish Gaussian elimination over Q."""
    A = [row[:] for row in Mx]; n = len(A); d = Fr(1)
    for i in range(n):
        p = next((k for k in range(i, n) if A[k][i] != 0), None)
        if p is None: return Fr(0)
        if p != i: A[i], A[p] = A[p], A[i]; d = -d
        d *= A[i][i]; inv = Fr(1)/A[i][i]
        for k in range(i+1, n):
            f = A[k][i]*inv
            if f: 
                for j in range(i, n): A[k][j] -= f*A[i][j]
    return d

def Alt(kap, th, H, w):
    r = len(kap); Hs = sorted(H)
    return det_frac([[w[Hs[k]]**(j + th[j]) * rho(kap[j], w[Hs[k]], w)
                      for j in range(r)] for k in range(r)])

def Vdm(H, w):
    Hs = sorted(H); v = Fr(1)
    for k in range(len(Hs)):
        for l in range(k+1, len(Hs)): v *= (w[Hs[l]] - w[Hs[k]])
    return v

def Psi_lemmaA(kap, th, M, w):
    r = len(kap); tot = Fr(0)
    for H in itertools.combinations(sorted(M), r):
        tot += S0(H, M, w) * Alt(kap, th, H, w) / Vdm(H, w)
    return tot

def pt(N, seed=None):
    return {k: Fr(random.randint(2, 211), random.randint(2, 211)) + 3*k
            for k in range(1, N+1)}

# ===================== STEP 1: Lemma A derived by me, checked against primitive
print("== STEP 1: Lemma A (primitive perm-sum == my alternant form), exact rational ==")
cases = [((2,3),(1,0),(2,3,4)), ((1,3),(0,2),(1,2,3,4)), ((2,3,4),(1,0,-1),(2,3,4,5)),
         ((1,2,4),(-1,0,1),(1,2,3,4,5)), ((3,),(2,),(3,4,5)),
         ((1,2,3,4),(0,1,-2,3),(1,2,3,4,5,6))]
tot = good = 0
for kap, th, M in cases:
    for _ in range(3):
        w = pt(8); tot += 1
        d = Psi_perm(kap,th,M,w) - Psi_lemmaA(kap,th,M,w)
        good += (d == 0)
print(f"  Lemma A verified: {good}/{tot} exact\n")

# ============ STEP 2: the alternant step of P^infty, FULLY SYMBOLIC (all x,w)
import sympy as sp
print("== STEP 2: P^infty alternant step, FULLY SYMBOLIC in all w and all heads ==")
def rho_s(kappa, X, ws):
    e = sp.Integer(1)
    for k in range(1, kappa): e *= (1 - ws[k]/X)
    return e
def Alt_sym(kap, th, xs, ws, shift):
    """Rows pre-multiplied by x_k**shift to make every entry a POLYNOMIAL.
    The same shift is applied to both sides of the identity, so the identity
    is preserved exactly; this only speeds the determinant up."""
    r = len(kap)
    def ent(k, j):
        num = sp.expand(rho_s(kap[j], xs[k], ws) * xs[k]**(kap[j]-1))   # polynomial
        ex = j + th[j] + shift - (kap[j]-1)
        assert ex >= 0, (k, j, ex)
        return sp.expand(xs[k]**ex * num)
    return sp.Matrix(r, r, ent).det(method='berkowitz')

# (kappa, block positions p..q 0-indexed, t0, outside twists dict)
sym_cases = [
 ((2,3),       (0,1), 1, {}),              # Rick's Theorem B case
 ((2,3,4),     (0,2), 1, {}),              # whole kappa, r=3
 ((1,2,3),     (0,2), -1, {}),             # s=1
 ((1,3,4,5),   (1,3), -1, {0:2}),          # interior block, outside twist
 ((1,2,5,6),   (2,3), 3, {0:-1,1:1}),      # block at the end, mixed outside
 ((2,3,6,7),   (0,1), 0, {2:1,3:-2}),      # TWO blocks; collapse the first only
 ((2,3,6,7),   (2,3), 2, {0:5,1:-3}),      # ... and the second only
 ((3,4,5,6),   (0,3), 2, {}),              # b=4, s=3
 ((1,4,5,6,7), (1,4), 0, {0:3}),           # b=4 interior, r=5
]
ws = {k: sp.Symbol(f'w{k}') for k in range(1, 12)}
ok = 0
for kap, (p,q), t0, oth in sym_cases:
    r = len(kap); b = q-p+1; e = t0-(b-1); s = kap[p]
    xs = [sp.Symbol(f'x{k}') for k in range(r)]
    th1 = [oth.get(j,0) for j in range(r)]; th2 = list(th1)
    for j in range(p,q+1): th1[j] = t0-(j-p); th2[j] = e
    C = sp.Integer(1)
    for m in range(b-1): C *= ws[s+m]**(b-1-m)
    blockconsec = all(kap[j+1]==kap[j]+1 for j in range(p,q))
    sh = max(kap) + max(abs(t) for t in list(th1)+list(th2)) + r + 2
    d = sp.expand(Alt_sym(kap,th1,xs,ws,sh) - C*Alt_sym(kap,th2,xs,ws,sh))
    ok += (d == 0)
    print(f"  kap={kap} block={(p,q)} t0={t0} out={oth} consec={blockconsec}: Alt-identity holds={d==0}")
print(f"  SYMBOLIC alternant step: {ok}/{len(sym_cases)}\n")

print("== STEP 2b: symbolic NEGATIVE controls (must FAIL) ==")
neg = [((2,4,5),(0,2),1,{},"non-consecutive labels (2,4,5)"),
       ((2,3,4),(0,2),1,{},"slope -2 instead of -1"),
       ((2,3,4),(0,2),1,{},"C := 1 (constant dropped)"),
       ((2,3,4),(0,2),1,{},"wrong C: C_{s,b} with s+1")]
for idx,(kap,(p,q),t0,oth,lab) in enumerate(neg):
    r=len(kap); b=q-p+1; e=t0-(b-1); s=kap[p]
    xs=[sp.Symbol(f'x{k}') for k in range(r)]
    th1=[oth.get(j,0) for j in range(r)]; th2=list(th1)
    slope = 2 if idx==1 else 1
    for j in range(p,q+1): th1[j]=t0-slope*(j-p); th2[j]=t0-slope*(b-1)
    C=sp.Integer(1)
    for m in range(b-1): C*= ws[s+m]**(b-1-m)
    if idx==2: C=sp.Integer(1)
    if idx==3:
        C=sp.Integer(1)
        for m in range(b-1): C*= ws[s+1+m]**(b-1-m)
    sh = max(kap) + max(abs(t) for t in list(th1)+list(th2)) + r + 2
    d=sp.expand(Alt_sym(kap,th1,xs,ws,sh)-C*Alt_sym(kap,th2,xs,ws,sh))
    print(f"  control '{lab}': nonzero (correctly fails) = {d != 0}")
