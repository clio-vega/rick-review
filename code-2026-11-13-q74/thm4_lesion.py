"""Independent spot-check of Rick's Q74 Theorem 4 (1)<=>(4) and of the R_1 column of
his table.  Own code: interval modules (JKLO convention), induction product built on
minimal left coset reps, End(Ind V) = Hom_B(V, Res Ind V) by Frobenius, each basis map
extended along T_w and CHECKED to commute with every pi_i.  Indecomposable <=> End local,
tested by: for random Phi in End, N = Phi - (tr Phi / n) I is nilpotent (x3 trials).
Arithmetic mod P."""
import sys, random
from itertools import permutations, combinations
import numpy as np
from hinf import rref, nullspace, P   # same mod-P linear algebra
random.seed(7)

def interval_modules(m):
    perms = list(permutations(range(1, m + 1)))
    def invset(g):
        pos = {v: p for p, v in enumerate(g)}
        return frozenset((p, q) for p in range(m) for q in range(p + 1, m) if g[p] > g[q])   # POSITION pairs: left weak order
    IS = {g: invset(g) for g in perms}
    def s_left(i, g): return tuple(i + 1 if v == i else (i if v == i + 1 else v) for v in g)
    def desL(g):
        pos = {v: p for p, v in enumerate(g)}
        return {i for i in range(1, m) if pos[i + 1] < pos[i]}
    out = []
    for a in perms:
        for b in perms:
            if not IS[a] <= IS[b]: continue
            Y = [g for g in perms if IS[a] <= IS[g] <= IS[b]]
            idx = {g: k for k, g in enumerate(Y)}; n = len(Y); mats = {}
            for i in range(1, m):
                M = np.zeros((n, n), dtype=np.int64)
                for g in Y:
                    if i in desL(g): M[idx[g], idx[g]] = 1
                    else:
                        h = s_left(i, g)
                        if h in idx: M[idx[h], idx[g]] = 1
                mats[i] = M
            out.append(((a, b), n, mats))
    return out

def mmod(A, B): return (A @ B) % P      # entries < P ~ 1e6, n <= ~300: no overflow

def is_local_from(Ebasis, n):
    if len(Ebasis) == 1: return True
    for _ in range(3):
        Phi = np.zeros((n, n), dtype=np.int64)
        for B in Ebasis: Phi = (Phi + random.randrange(P) * B) % P
        lam = int(np.trace(Phi) % P) * pow(n, P - 2, P) % P
        Nm = (Phi - lam * np.eye(n, dtype=np.int64)) % P
        Q = Nm.copy(); e = 1
        while e < n: Q = mmod(Q, Q); e *= 2
        if Q.any(): return False
    return True

def endo_commutant(mats, n):
    I = np.eye(n, dtype=np.int64)
    A = np.vstack([(np.kron(I, M.T) - np.kron(M, I)) % P for M in mats.values()]) if mats else np.zeros((0, n * n), dtype=np.int64)
    return [v.reshape(n, n) for v in nullspace(A, n * n)]

def induce(a, nX, mX, b, nY, mY):
    """X boxtimes Y = Ind_{H_a x H_b}^{H_N}(X (x) Y). Returns (dim, mats, V-mats on B, coset list, act_T)."""
    N = a + b; nV = nX * nY
    reps = []                         # w as tuple of values in positions 1..N, increasing on blocks
    for A in combinations(range(1, N + 1), a):
        Bv = [v for v in range(1, N + 1) if v not in A]
        reps.append(tuple(A) + tuple(Bv))
    ridx = {w: k for k, w in enumerate(reps)}
    dim = len(reps) * nV
    # V action of pi_j, j != a
    Vm = {}
    for j in range(1, N):
        if j < a: Vm[j] = np.kron(mX[j], np.eye(nY, dtype=np.int64)) if j in mX else None
        elif j > a: Vm[j] = np.kron(np.eye(nX, dtype=np.int64), mY[j - a])
    mats = {}
    for i in range(1, N):
        M = np.zeros((dim, dim), dtype=np.int64)
        for w in reps:
            k = ridx[w]; pi_, pj_ = w.index(i), w.index(i + 1)
            sameA = pi_ < a and pj_ < a; sameB = pi_ >= a and pj_ >= a
            blk = slice(k * nV, (k + 1) * nV)
            if sameA or sameB:
                j = pi_ + 1                 # s_i w = w s_j, j = position of i (1-based)
                M[blk, blk] = Vm[j]
            elif pi_ < pj_:
                w2 = tuple(i + 1 if v == i else (i if v == i + 1 else v) for v in w)
                k2 = ridx[w2]
                M[k2 * nV:(k2 + 1) * nV, blk] = np.eye(nV, dtype=np.int64)
            else:
                M[blk, blk] = np.eye(nV, dtype=np.int64)
        mats[i] = M
    for i in range(1, N):               # positive checks: idempotent + braid
        assert (mmod(mats[i], mats[i]) == mats[i]).all()
        if i + 1 < N:
            L = mmod(mmod(mats[i], mats[i + 1]), mats[i]); R = mmod(mmod(mats[i + 1], mats[i]), mats[i + 1])
            assert (L == R).all()
    return dim, mats, Vm, reps, nV

def end_frobenius(a, b, dim, mats, Vm, reps, nV):
    """Hom_B(V, Res M): f (dim x nV) with f Vm[j] = mats[j] f, j != a. Extend F(T_w v) = T_w f(v)."""
    N = a + b; js = [j for j in range(1, N) if j != a]
    I = np.eye(nV, dtype=np.int64); Id = np.eye(dim, dtype=np.int64)
    A = np.vstack([(np.kron(Id, Vm[j].T) - np.kron(mats[j], I)) % P for j in js]) if js else np.zeros((0, dim * nV), dtype=np.int64)
    sols = nullspace(A, dim * nV)
    base = reps.index(tuple(range(1, N + 1)))
    # reduced word for each coset rep w: T_w = pi_{i1} ... ; build by BFS from identity
    word = {tuple(range(1, N + 1)): []}; frontier = [tuple(range(1, N + 1))]
    while frontier:
        nf = []
        for w in frontier:
            for i in range(1, N):
                pi_, pj_ = w.index(i), w.index(i + 1)
                if (pi_ < a) != (pj_ < a) and pi_ < pj_:
                    w2 = tuple(i + 1 if v == i else (i if v == i + 1 else v) for v in w)
                    if w2 not in word: word[w2] = [i] + word[w]; nf.append(w2)
        frontier = nf
    Es = []
    for v in sols:
        f = v.reshape(dim, nV)
        F = np.zeros((dim, dim), dtype=np.int64)
        for k, w in enumerate(reps):
            img = f.copy()
            for i in reversed(word[w]): img = mmod(mats[i], img)
            F[:, k * nV:(k + 1) * nV] = img
        for i in range(1, N): assert (mmod(F, mats[i]) == mmod(mats[i], F)).all(), 'extension not an endomorphism'
        Es.append(F)
    return Es

def decomposable_product(X, a, Y, b):
    dim, mats, Vm, reps, nV = induce(a, X[1], X[2], b, Y[1], Y[2])
    return not is_local_from(end_frobenius(a, b, dim, mats, Vm, reps, nV), dim)

if __name__ == '__main__':
    mmax = int(sys.argv[1]); cap = int(sys.argv[2])
    box = ((('1',), ('1',)), 1, {})
    ind = {}
    for m in range(1, min(mmax, 4) + 1):
        mods = interval_modules(m)
        ind[m] = [X for X in mods if is_local_from(endo_commutant(X[2], X[1]), X[1])]
        proj = sum(1 for X in ind[m] if X[0][0] == tuple(range(1, m + 1)) or True and False)
        R1 = [X for X in ind[m] if decomposable_product(X, m, box, 1)]
        L1 = [X for X in ind[m] if decomposable_product(box, 1, X, m)]
        print('m=%d: intervals %d, indecomposable %d, R1 %d, L1 %d' % (m, len(mods), len(ind[m]), len(R1), len(L1)), flush=True)
    # Theorem 4 (1) <=> (4) on pairs
    tot = dec = bad = 0
    R1s = {}; L1s = {}
    for a in ind:
        for X in ind[a]:
            R1s[(a, X[0])] = decomposable_product(X, a, box, 1)
            L1s[(a, X[0])] = decomposable_product(box, 1, X, a)
    for a in ind:
        for b in ind:
            if a + b > mmax + 1: continue
            for X in ind[a]:
                for Y in ind[b]:
                    from math import comb
                    if comb(a + b, a) * (X[1] * Y[1]) ** 2 > cap: continue
                    d1 = decomposable_product(X, a, Y, b)
                    d4 = R1s[(a, X[0])]
                    tot += 1; dec += d1; bad += (d1 != d4)
                    if d1 != d4 and bad <= 5: print('LESION-MISMATCH', a, X[0], b, Y[0], d1, d4)
    print('Theorem 4 (1)<=>(4): %d pairs (a+b<=%d), %d decomposable, %d mismatches' % (tot, mmax + 1, dec, bad))
