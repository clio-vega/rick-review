"""Rem T (half-step operator): T = unitriangular sqrt of A_oA_e; claim s_{x+1/2} = T s_x,
and T(kappa,nu) = product over components of theta of weights 1 (single off-diag box),
+-(-1/2)^{|D|} (ribbon with one diagonal box), or 0 / 'full version'.  Clio 2026-11-11."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.argv = [sys.argv[0], "0"]
import io, contextlib
with contextlib.redirect_stdout(io.StringIO()):
    import check as C
from fractions import Fraction as Fr
from extra_helpers import Htab
M = 4
PK = C.strict_partitions(M); D = C.D
idx = {k: i for i, k in enumerate(PK)}; n = len(PK)
A = [[Fr(C.V(D(k)-D(nu))) if D(nu) <= D(k) else Fr(0) for nu in PK] for k in PK]
X = [[A[i][j] - (1 if i == j else 0) for j in range(n)] for i in range(n)]
def mul(P, Q): return [[sum(P[i][t]*Q[t][j] for t in range(n)) for j in range(n)] for i in range(n)]
T = [[Fr(1 if i == j else 0) for j in range(n)] for i in range(n)]
Xk = [row[:] for row in T]; c = Fr(1)
for k in range(1, 12):
    c = c * (Fr(1, 2) - (k-1)) / k
    Xk = mul(Xk, X)
    T = [[T[i][j] + c*Xk[i][j] for j in range(n)] for i in range(n)]
assert mul(T, T) == A, "sqrt failed"
H = Htab(M)
s = lambda k, x: (-1)**sum(k) * H[k](-Fr(x))
ok = tot = 0
for k in PK:
    for twox in range(-4, 10):
        x = Fr(twox, 2); tot += 1
        ok += s(k, x + Fr(1, 2)) == sum(T[idx[k]][idx[nu]] * s(nu, x) for nu in PK)
print(f"s_(x+1/2) = T s_x : {ok}/{tot}")
# component structure
def comps(th):
    th = set(th); out = []
    while th:
        st = [th.pop()]; comp = set(st)
        while st:
            a, b = st.pop()
            for y in ((a+1,b),(a-1,b),(a,b+1),(a,b-1)):
                if y in th: th.remove(y); comp.add(y); st.append(y)
        out.append(frozenset(comp))
    return out
def is_ribbon(cc): return not any((a+1,b) in cc and (a,b+1) in cc and (a+1,b+1) in cc for a,b in cc)
agree = dis = other = 0
for k in PK:
    for nu in PK:
        if not D(nu) <= D(k) or k == nu: continue
        th = D(k) - D(nu); cs = comps(th); t = T[idx[k]][idx[nu]]
        kinds = []
        for cc in cs:
            nd = sum(1 for a, b in cc if a == b)
            if len(cc) == 1 and nd == 0: kinds.append(Fr(1))
            elif nd == 1 and is_ribbon(cc): kinds.append(Fr(1, 2**len(cc)))
            else: kinds.append(None)
        if None in kinds: other += 1; continue
        pred = 1
        for w in kinds: pred *= w
        if abs(t) == pred: agree += 1
        else:
            dis += 1
            if dis <= 5: print("  |T| != predicted", k, nu, sorted(th), t, pred)
print(f"components all of the two named kinds: |T| matches {agree}, mismatches {dis}; "
      f"pairs with another component kind (weight left to 'full version'): {other}")
