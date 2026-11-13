"""Test Rick's (H_infinity) on weak-Bruhat interval modules of H_m(0), m<=5.
Interval module B(sigma,tau) (Jung-Kim-Lee-Oh 2105.14169 convention):
 basis = left weak interval [sigma,tau]_L; pi_i g = g if i in Des_L(g);
 0 if s_i g not in interval; s_i g otherwise.
Res_t to H_{m-t} = <pi_1..pi_{m-t-1}> splits over right cosets W_J g (left mult by
s_i, i in J, preserves them).  Each coset piece is decomposed into indecomposables by
Fitting splitting along random endomorphisms (mod P), locality certified by 4 random
endomorphisms each having a single eigenvalue.  Top multiplicities from Hom(-, C_D).
ALL intervals are tested (a superset of the indecomposable ones)."""
import sys, random
from itertools import permutations, combinations
import numpy as np
import sympy
P = 1000003
random.seed(1)
m = int(sys.argv[1]) if __name__ == "__main__" else 3
perms = list(permutations(range(1, m + 1)))
def s_left(i, g): return tuple(i + 1 if v == i else (i if v == i + 1 else v) for v in g)
def desL(g):
    pos = {v: p for p, v in enumerate(g)}
    return {i for i in range(1, m) if pos[i + 1] < pos[i]}
def invset(g):
    pos = {v: p for p, v in enumerate(g)}
    return frozenset((p, q) for p in range(m) for q in range(p + 1, m) if g[p] > g[q])   # POSITION pairs: left weak order
IS = {g: invset(g) for g in perms}
def leq(a, b): return IS[a] <= IS[b]

def rref(A):
    A = np.array(A, dtype=np.int64) % P
    if A.size == 0: return A, []
    nr, nc = A.shape; piv = []; r = 0
    for c in range(nc):
        if r == nr: break
        nz = np.nonzero(A[r:, c])[0]
        if nz.size == 0: continue
        pr = r + nz[0]
        if pr != r: A[[r, pr]] = A[[pr, r]]
        A[r] = (A[r] * pow(int(A[r, c]), P - 2, P)) % P
        col = A[:, c].copy(); col[r] = 0; rows = np.nonzero(col)[0]
        if rows.size: A[rows] = (A[rows] - (col[rows, None] * A[r][None, :]) % P) % P
        piv.append(c); r += 1
    return A[:r], piv
def nullspace(A, n):
    if len(A) == 0: return np.eye(n, dtype=np.int64)
    R, piv = rref(A); free = [c for c in range(n) if c not in set(piv)]
    out = np.zeros((len(free), n), dtype=np.int64)
    for k, f in enumerate(free):
        out[k, f] = 1
        for row, pc in zip(R, piv): out[k, pc] = (-row[f]) % P
    return out   # rows = basis vectors
def mm(A, B): return (A.astype(object).dot(B.astype(object)) % P).astype(np.int64)

def top_mults(mats, J):
    n = mats[J[0]].shape[0] if J else None
    out = {}
    for r in range(len(J) + 1):
        for D in combinations(J, r):
            # f Pi_i = [i in D] f   <=>  (Pi_i^T - [i in D] I) f^T = 0
            A = np.vstack([(mats[i].T - (np.eye(n, dtype=np.int64) if i in D else 0)) % P for i in J])
            k = len(nullspace(A, n))
            if k: out[D] = k
    return out

def endo_basis(mats, J, n):
    # Phi Pi = Pi Phi ; vec row-major: (Pi^T kron I?)  use explicit: (I kron Pi^T - Pi kron I) for Phi row-major
    I = np.eye(n, dtype=np.int64)
    A = np.vstack([(np.kron(I, mats[i].T) - np.kron(mats[i], I)) % P for i in J])
    # check orientation:  vec(Phi Pi)= (I kron Pi^T) vec(Phi);  vec(Pi Phi) = (Pi kron I) vec(Phi)
    return [v.reshape(n, n) for v in nullspace(A, n * n)]

def charpoly_factors(Phi):
    x = sympy.symbols('x')
    cp = sympy.Matrix(Phi.tolist()).charpoly(x).as_expr()
    return sympy.factor_list(cp, x, modulus=P)[1], x

def polyval_mat(coeffs, Phi):
    n = Phi.shape[0]; R = np.zeros((n, n), dtype=np.int64)
    for c in coeffs:     # Horner, coeffs high->low
        R = (mm(R, Phi) + (int(c) % P) * np.eye(n, dtype=np.int64)) % P
    return R

def decompose(mats, J, n, depth=0):
    """list of (mats restricted) for indecomposable summands."""
    E = endo_basis(mats, J, n)
    if len(E) == 1: return [mats]
    single = 0
    for attempt in range(80):
        Phi = sum(random.randrange(P) * B for B in E) % P
        facs, x = charpoly_factors(Phi)
        if len(facs) == 1:
            if sympy.Poly(facs[0][0], x).degree() == 1:
                single += 1
                if single >= 4: return [mats]
            continue
        # split along first factor power vs rest
        parts = []
        for (q, e) in facs:
            Q = polyval_mat([int(c) for c in sympy.Poly(q ** e, x, modulus=P).all_coeffs()], Phi)
            K = nullspace(Q, n)          # rows: basis of generalized eigenspace (column vectors)
            parts.append(K.T)
        out = []
        for Bm in parts:
            r = Bm.shape[1]
            # restricted action: Pi Bm = Bm A  ->  A = left-inverse * Pi Bm
            R, piv = rref(Bm.T)  # not used directly
            # solve via pivot rows of Bm
            Rr, pv = rref(Bm.T.copy())
            sel = pv  # pivot columns of Bm^T = rows of Bm that are independent
            Bsub = Bm[sel, :]
            Binv = np.array(sympy.Matrix(Bsub.tolist()).inv_mod(P).tolist(), dtype=np.int64)
            sub = {i: mm(Binv, mm(mats[i], Bm)[sel, :]) for i in J}
            for i in J: assert (mm(Bm, sub[i]) == mm(mats[i], Bm)).all(), 'not a submodule'
            out += decompose(sub, J, r, depth + 1)
        return out
    raise RuntimeError('could not split or certify local')

intervals = [(a, b) for a in perms for b in perms if leq(a, b)]
print('m=%d: %d left-weak intervals' % (m, len(intervals)), flush=True)
fails = []; pieces = 0; split_pieces = 0; maxdim = 0
for (a, b) in intervals:
    basis = [g for g in perms if leq(a, g) and leq(g, b)]
    for t in range(1, m - 2):            # |J| >= 2 ; smaller J is automatic
        mt = m - t; J = list(range(1, mt))
        cos = {}
        for g in basis: cos.setdefault(tuple(v if v > mt else 0 for v in g), []).append(g)
        for key, Y in cos.items():
            idx = {g: k for k, g in enumerate(Y)}; n = len(Y); pieces += 1; maxdim = max(maxdim, n)
            mats = {}
            for i in J:
                M = np.zeros((n, n), dtype=np.int64)
                for g in Y:
                    if i in desL(g): M[idx[g], idx[g]] = 1
                    else:
                        h = s_left(i, g)
                        if h in idx: M[idx[h], idx[g]] = 1
                mats[i] = M
            tm = top_mults(mats, J)
            if max(tm.values()) <= 1: continue
            split_pieces += 1
            for Z in decompose(mats, J, n):
                tz = top_mults(Z, J)
                if max(tz.values()) > 1:
                    fails.append(((a, b), t, key, {k: v for k, v in tz.items() if v > 1}))
print('coset pieces examined %d (max dim %d); pieces needing decomposition %d' % (pieces, maxdim, split_pieces))
print('indecomposable summands of Res_t X with a REPEATED top label: %d, in %d intervals'
      % (len(fails), len({f[0] for f in fails})))
for f in fails[:6]: print('  ', f)
