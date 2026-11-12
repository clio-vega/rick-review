"""
Theorem A check.  M_{I,J} = H_N(0)/H_N(0){pi_i - chi(i) : i != a}, built from the regular
representation (basis pi_w).  End M = {u : pi_i u = chi(i) u, i != a} (Frobenius), each u
turned into an explicit matrix phi_u(pi_w g) = pi_w u and checked to commute.
Prediction (Rick Thm A): t := dim End/J = 1 unless D_I, D_J both in {empty, full}; then 2.
Also Norton check: C_D projective iff D in {empty, full}, via dim P_D = #{w: Des(w)=D}.
"""
import itertools, sys, time
import numpy as np
sys.path.insert(0, '.')
from hecke0 import P, rref, nullspace, rank, summand_count


def perms(N):
    return list(itertools.permutations(range(1, N + 1)))


def regular(N):
    """left mult by pi_i on basis pi_w: pi_i pi_w = pi_{s_i w} if l(s_i w)>l(w) else pi_w.
    w as tuple of values w(1..N); s_i w swaps VALUES i,i+1; ascent iff i before i+1 in w."""
    W = perms(N); idx = {w: k for k, w in enumerate(W)}
    act = []
    for i in range(1, N):
        col = []
        for w in W:
            p, q = w.index(i), w.index(i + 1)
            if p < q:  # l(s_i w) > l(w)
                w2 = tuple(i + 1 if x == i else i if x == i + 1 else x for x in w)
                col.append(idx[w2])
            else:
                col.append(idx[w])
        act.append(col)
    return W, idx, act


def reduced_word(w):
    """word i_1..i_l with pi_w = pi_{i_1}...pi_{i_l} (apply right-most first to 1)."""
    w = list(w); word = []
    # left-multiply build: w = s_{i1} ... s_{il}; peel left descents: s_i w < w iff i+1 before i
    while True:
        for i in range(1, len(w)):
            if w.index(i + 1) < w.index(i):
                word.append(i)
                w = [i + 1 if x == i else i if x == i + 1 else x for x in w]
                break
        else:
            break
    return word  # pi_w = pi_{word[0]} pi_{word[1]} ...


def build_M(a, b, DI, DJ):
    N = a + b
    W, idx, act = regular(N)
    n = len(W)
    chi = {i: (1 if i in DI else 0) for i in range(1, a)}
    chi.update({a + q: (1 if q in DJ else 0) for q in range(1, b)})
    # left ideal L = span{ pi_w (pi_i - chi_i) } ; right mult by pi_i: pi_w pi_i = pi_{w s_i} if l up
    gens = []
    for w in W:
        for i, c in chi.items():
            v = [0] * n
            # pi_w pi_i : right descent at position i iff w(i) > w(i+1)
            if w[i - 1] < w[i]:
                w2 = list(w); w2[i - 1], w2[i] = w2[i], w2[i - 1]
                v[idx[tuple(w2)]] += 1
            else:
                v[idx[w]] += 1
            v[idx[w]] -= c
            gens.append(v)
    R, piv = rref(gens)
    pivset = set(piv)
    qb = [k for k in range(n) if k not in pivset]  # quotient basis: images of pi_W[k]
    d = len(qb)
    from math import comb
    assert d == comb(N, a), (d, comb(N, a))
    qpos = {k: t for t, k in enumerate(qb)}
    Rn = np.array(R, dtype=np.int64)

    def reduce(vec):
        """reduce full vector modulo L, return coords in quotient basis."""
        v = np.array(vec, dtype=np.int64) % P
        for row, pc in zip(Rn, piv):
            if v[pc]:
                v = (v - (v[pc] * row) % P) % P
        return [int(v[k]) for k in qb]

    # matrices of pi_i on M
    mats = []
    for i in range(N - 1):
        A = np.zeros((d, d), dtype=np.int64)
        for t, k in enumerate(qb):
            e = [0] * n; e[act[i][k]] = 1
            A[:, t] = reduce(e)
        mats.append(A)
    gvec = reduce([1 if w == tuple(range(1, N + 1)) else 0 for w in W])
    return mats, d, qb, W, gvec, chi


def check_relations(mats):
    for i, A in enumerate(mats):
        assert ((A @ A - A) % P == 0).all()
        if i + 1 < len(mats):
            B = mats[i + 1]
            assert ((A @ B % P @ A - B @ A % P @ B) % P == 0).all()
        for j in range(i + 2, len(mats)):
            assert ((A @ mats[j] - mats[j] @ A) % P == 0).all()


def apply_word(mats, word, v):
    v = np.array(v, dtype=np.int64)
    for i in reversed(word):
        v = (mats[i - 1] @ v) % P
    return v


def End_M(a, b, DI, DJ):
    mats, d, qb, W, gvec, chi = build_M(a, b, DI, DJ)
    check_relations(mats)
    # E = joint eigenspace
    eqs = []
    for i, c in chi.items():
        A = mats[i - 1].copy()
        A[np.arange(d), np.arange(d)] -= c
        eqs.extend((A % P).tolist())
    E = nullspace(eqs, d) if eqs else [[1 if j == k else 0 for j in range(d)] for k in range(d)]
    Ends = []
    for u in E:
        F = np.zeros((d, d), dtype=np.int64)
        for t, k in enumerate(qb):
            F[:, t] = apply_word(mats, reduced_word(W[k]), u)
        for A in mats:
            assert ((F @ A - A @ F) % P == 0).all(), "phi_u not H-linear"
        Ends.append(np.array(F, dtype=object))
    return Ends


def compositions_sets(m):
    return [frozenset(s) for r in range(m) for s in itertools.combinations(range(1, m), r)]


def proj(D, m):
    return D == frozenset() or D == frozenset(range(1, m))


if __name__ == '__main__':
    Nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    # Norton: dim P_D = #{w : Des(w) = D} equals 1 iff D extreme
    for m in range(1, 6):
        cnt = {}
        for w in perms(m):
            D = frozenset(i for i in range(1, m) if w[i - 1] > w[i])
            cnt[D] = cnt.get(D, 0) + 1
        ones = sorted([tuple(sorted(D)) for D, c in cnt.items() if c == 1])
        print(f"Norton m={m}: D with #Des^-1(D)=1: {ones}")
    tot = mism = 0; ctrl_split = 0; dimEnd_hist = {}
    t0 = time.time()
    for N in range(2, Nmax + 1):
        for a in range(1, N):
            b = N - a
            for DI in compositions_sets(a):
                for DJ in compositions_sets(b):
                    Ends = End_M(a, b, DI, DJ)
                    t = summand_count(Ends)
                    pred = 2 if (proj(DI, a) and proj(DJ, b)) else 1
                    tot += 1
                    if pred == 2:
                        ctrl_split += (t == 2)
                    if t != pred:
                        mism += 1
                        print("MISMATCH", a, b, sorted(DI), sorted(DJ), "t=", t, "pred", pred)
                    if a == 2 and b == 2 and DI == frozenset({1}) and DJ == frozenset({1}):
                        print("  example I=J=(1,1)? no: D={1} means I=(1,1)")
                    if sorted(DI) == [2] and sorted(DJ) == [2] and a == 4 and b == 4:
                        print("  I=J=(2,2): dim End =", len(Ends), "t =", t)
        print(f"N={N}: cumulative cases {tot}, mismatches {mism}, both-proj split {ctrl_split}, {time.time()-t0:.1f}s", flush=True)
