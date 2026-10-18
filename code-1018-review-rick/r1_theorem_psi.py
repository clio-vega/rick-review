"""
REVIEW 2026-10-18 -- first-hand test of Rick's Theorem Psi (2026-10-18-theorem-psi.pdf,
md5 24d012c82e5831a37e697c617cae2f72) using MY engine (q484_engine.py, md5 f53c0258...),
which is a different instrument from his scripts/wake245/psi_n2.py.

Tested, separately (his proof's Inputs, not only its conclusion):
  (C-i)   A~_M = A~_{M\a} on {w_a = 1},            a in M
  (C-ii)  A~_M = A~_{(M\b)+a} on {w_a = w_b},      b in M, a not in M
  (C-iii) A~_M(-w) = A~_M(w)                        [the clause whose stated
                                                     parity count "n(n+1)=0" is
                                                     trivially true for every n]
  (C-i')  A~_M = A~_{M\a} on {w_a = -1}             [his *derived* step]
  (QC)    A~_M = g * A~_{M\{a,b}} on H_ab
  (PSI)   Ahat_M = Ahat_{M'} on the divisor, every root type   <- Theorem Psi

Every arm carries a PLANT control: the engine output is multiplied by a factor that
breaks exactly one input, and the arm must FIRE.
"""
import sys, itertools, random
sys.path.insert(0, '/home/clio/projects/proofs/code-1018c2-gauge')
import sympy as sp
from q484_engine import Atilde, subsets

from q484_engine import q   # FIX: the engine carries its own SYMBOLIC q.
# A numeric q here left three of six arms insensitive and broke exactly the
# two that use psi/g -- a harness fault that reads as a selective math failure.

def psi(v):
    return (1 - q*v**2)/(1 - q)

def Psi(w, M):
    return sp.prod([psi(w[m-1]) for m in M]) if M else sp.Integer(1)

def At(N, w, M, I, plant=None):
    v = Atilde(N, list(w), list(M), list(I), X='C')
    if plant is not None:
        v = v * plant(w, M, I)
    return sp.cancel(v)

# ---- plants: each breaks exactly one structural input --------------------------
P_ODD   = lambda w, M, I: sp.prod([w[m-1] for m in M]) if M else sp.Integer(1)  # breaks evenness when |M| odd
P_CARD  = lambda w, M, I: sp.Integer(1) + sum(M)   # label-sensitive. A CARDINALITY
# plant is INADMISSIBLE for C-ii: |(M\\b)+a| = |M|, so it cannot fire there.
P_PAIR  = lambda w, M, I: (1 - q*sp.prod([w[m-1] for m in M])) if M else sp.Integer(1)

def gen_w(N, rng, forbid=()):
    while True:
        w = [sp.Rational(rng.randint(2, 40), rng.randint(2, 40)) for _ in range(N)]
        vals = set(w) | {1/x for x in w} | {sp.Integer(1), sp.Integer(-1)}
        if len(set(w)) < N: continue
        if any(x in forbid for x in w): continue
        if any(w[i]*w[j] == 1 for i in range(N) for j in range(N)): continue
        if any(q*m == 1 for m in [x**2 for x in w] + [w[i]*w[j] for i in range(N) for j in range(N)]): continue
        return w

def score(name, fn, N, plant=None):
    ok = bad = 0
    for M, I in itertools.product(subsets(N), subsets(N)):
        r = fn(N, M, I, plant)
        if r is None: continue
        ok, bad = (ok+1, bad) if r else (ok, bad+1)
    return name, ok, bad

# ------------------------------------------------------------------ the tests
def t_Ci(N, M, I, plant):
    for a in M:
        w = gen_w(N, random.Random(11))
        w[a-1] = sp.Integer(1)
        L = At(N, w, M, I, plant); R = At(N, w, [m for m in M if m != a], I, plant)
        return sp.simplify(L - R) == 0
    return None

def t_Cineg(N, M, I, plant):
    for a in M:
        w = gen_w(N, random.Random(13))
        w[a-1] = sp.Integer(-1)
        L = At(N, w, M, I, plant); R = At(N, w, [m for m in M if m != a], I, plant)
        return sp.simplify(L - R) == 0
    return None

def t_Cii(N, M, I, plant):
    for b in M:
        for a in range(1, N+1):
            if a in M: continue
            w = gen_w(N, random.Random(17))
            w[a-1] = w[b-1]
            Mp = sorted([m for m in M if m != b] + [a])
            L = At(N, w, M, I, plant); R = At(N, w, Mp, I, plant)
            return sp.simplify(L - R) == 0
    return None

def t_Ciii(N, M, I, plant):
    w = gen_w(N, random.Random(19))
    L = At(N, w, M, I, plant); R = At(N, [-x for x in w], M, I, plant)
    return sp.simplify(L - R) == 0

def t_QC(N, M, I, plant):
    for a, b in itertools.combinations(M, 2):
        w = gen_w(N, random.Random(23))
        x = w[a-1]; w[b-1] = 1/x
        if len(set(w)) < N: return None
        g = (1-q)**2 / ((1 - q*x**2)*(1 - q*x**-2))
        L = At(N, w, M, I, plant)
        R = g * At(N, w, [m for m in M if m not in (a, b)], I, plant)
        return sp.simplify(L - R) == 0
    return None

def t_PSI(N, M, I, plant):
    """Theorem Psi: Ahat_M - Ahat_M' vanishes on the divisor, all three root types."""
    res = []
    Ah = lambda w, S: At(N, w, S, I, plant) * Psi(w, S)
    for a in M:                                     # 2e_a, both components
        for eps in (sp.Integer(1), sp.Integer(-1)):
            w = gen_w(N, random.Random(29)); w[a-1] = eps
            res.append(sp.simplify(Ah(w, M) - Ah(w, [m for m in M if m != a])) == 0)
    for a, b in itertools.combinations(M, 2):       # e_a+e_b
        w = gen_w(N, random.Random(31)); x = w[a-1]; w[b-1] = 1/x
        if len(set(w)) < N: continue
        res.append(sp.simplify(Ah(w, M) - Ah(w, [m for m in M if m not in (a, b)])) == 0)
    for b in M:                                     # e_a-e_b
        for a in range(1, N+1):
            if a in M: continue
            w = gen_w(N, random.Random(37)); w[a-1] = w[b-1]
            res.append(sp.simplify(Ah(w, M) - Ah(w, sorted([m for m in M if m != b]+[a]))) == 0)
    if not res: return None
    return all(res)

TESTS = [('C-i   (w_a=1)', t_Ci, P_CARD), ("C-i'  (w_a=-1)", t_Cineg, P_CARD),
         ('C-ii  (w_a=w_b)', t_Cii, P_CARD), ('C-iii (evenness)', t_Ciii, P_ODD),
         ('QC    (H_ab)', t_QC, P_PAIR), ('PSI   (Thm Psi)', t_PSI, P_PAIR)]

for N in (2, 3):
    print(f'===== N = {N} =====')
    for name, fn, plant in TESTS:
        n0, ok0, bad0 = score(name, fn, N)
        n1, ok1, bad1 = score(name, fn, N, plant)
        fired = 'FIRES' if bad1 > 0 else '*** BLIND ***'
        print(f'  {name:18s} clean {ok0:3d}/{ok0+bad0:3d}   plant {ok1:3d}/{ok1+bad1:3d}  {fired}')
