"""Extra checks + lesion controls for the FPSAC cut review.  Clio 2026-11-11."""
import sys
sys.argv = [sys.argv[0], sys.argv[1] if len(sys.argv) > 1 else "4"]
import io, contextlib, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    import check as C          # runs the main suite; reuse its engines and H tables
from fractions import Fraction as Fr
sys.path.insert(0, "/home/clio/projects/reviews/code-1024c2-thmI")
import referee33 as BR          # BR Thm 5.5 recursion, implemented 10-24 from the statement
print(buf.getvalue().split("\n\n")[-1][-400:])

M = int(sys.argv[1])
D, V, N, leq = C.D, C.V, C.N, C.leq
res = {}
def tally(name, ok):
    a, b = res.get(name, (0, 0)); res[name] = (a + bool(ok), b + 1)

# rebuild H per m (check.py keeps only last m's table), cheaply
def Htab(m):
    Wd = C.words(m); H = {}
    for mu, w in Wd.items():
        k = C.kappa_of(mu, m); d = sum(k)
        pts = [(j, sum(C.apply_word(w, {(j,)*m: 1}, m).values())) for j in range(d+1)]
        H[k] = C.interp(pts)
    return H

def V_rev(theta):   # BR letters 1'<1 read directly on theta, diagonal unprimed (=larger)
    return C.count_maps(theta, 0, 1, True, False) if False else _vrev(theta)
def _vrev(theta):
    bs = sorted(theta); from itertools import product
    c = 0
    for asg in product((0, 1), repeat=len(bs)):
        f = dict(zip(bs, asg))
        if any(x[0] == x[1] and f[x] == 0 for x in bs): continue
        if all(not (x != y and leq(x, y)) or f[x] < f[y] for x in bs for y in bs): c += 1
    return c

lesions = {}
def lesion(name, fired):
    a, b = lesions.get(name, (0, 0)); lesions[name] = (a + bool(fired), b + 1)

for m in range(1, M+1):
    H = Htab(m); PK = C.strict_partitions(m)
    s = lambda k, x: (-1)**sum(k) * H[k](-Fr(x))
    for k in PK:
        subs = [r for r in PK if r != k and D(r) <= D(k)]
        # Rem 4.4: (-1)^{|theta|-1} V(theta) == BR Thm 5.5 C(R(theta),1)
        for rho in subs:
            th = D(k) - D(rho)
            Rth = frozenset((m-1-b, m-1-a) for a, b in th)
            tally("Rem4.4 (-1)^{|th|-1}V(th) == BR-Thm5.5 C(R th,1)",
                  (-1)**(len(th)-1) * V(th) == BR.C(Rth, 1))
            lesion("L1 Rem4.4 on wrong orientation V_rev(th)",
                   (-1)**(len(th)-1) * _vrev(th) != BR.C(Rth, 1))
            # Rem window-ind: V != 0 => r(rho) >= r(kappa)-2
            if V(th): tally("Rem window-ind: V!=0 => r(rho)>=r-2", C.r_of(rho) >= C.r_of(k) - 2)
            if V(th) and len(k) >= 1:
                tally("Rem Z: V!=0 => r(rho')>=r(k')-2", C.r_of(rho[1:]) >= C.r_of(k[1:]) - 2)
        # star lesion: wrong orientation
        x = Fr(5, 2)
        good = s(k, x+1) - s(k, x) == sum(V(D(k)-D(r)) * s(r, x) for r in subs)
        bad = s(k, x+1) - s(k, x) == sum(_vrev(D(k)-D(r)) * s(r, x) for r in subs)
        tally("star at x=5/2 (recheck)", good)
        lesion("L2 star with V_rev", not bad)
        # Rem window-ind surviving term T
        if k:
            r = C.r_of(k); t = 1 if r % 2 else 2
            T = frozenset(b for b in D(k) if b[0]+b[1] >= r - t)
            rhoT = [rr for rr in PK if D(rr) == D(k) - T][0]
            tally("Rem window-ind: V(T)!=0", V(T) != 0)
            tally("Rem window-ind: W(rho_T)<W", C.ceil_half(C.r_of(rhoT)) < C.ceil_half(r))
        # Lemma Npos lesion: floor instead of ceil
        if k:
            r = C.r_of(k)
            lesion("L3 window with floor(r/2)", any((N(k, j) > 0) != (j >= r//2 + 1) for j in range(1, r+3)))
            # HZ (i) lesion: r(kappa) instead of r(kappa')
            kp = k[1:]
            lesion("L4 HZ(i) with r(kappa) for r(kappa')",
                   any((H[k](Fr(-2*a-1, 2)) == 0) != (bool(kp) and a <= C.ceil_half(r)) for a in range(1, 8)))
            # Rem Z: H(-3/2) = 2^{-k1} H_{k'}(-1), k1>=2
            if k[0] >= 2:
                tally("Rem Z: H(-3/2)=2^-k1 H_k'(-1)", H[k](Fr(-3, 2)) == Fr(1, 2**k[0]) * H[kp](-1))
        # Lemma layers (a),(b),(c)
        def Ao(kk, nu):
            if not D(nu) <= D(kk): return 0
            th = D(kk) - D(nu)
            return int(all(not (x != y and leq(x, y)) for x in th for y in th) and all(a != b for a, b in th))
        def Ae(kk, nu):
            if not D(nu) <= D(kk): return 0
            th = D(kk) - D(nu)
            return int(all(not (x != y and leq(x, y)) for x in th for y in th))
        for nu in PK:
            if D(nu) <= D(k):
                tally("Layers (a) AoAe=V", sum(Ao(k, mu)*Ae(mu, nu) for mu in PK) == V(D(k)-D(nu)))
                tally("Layers (b) a=1: Ao = N_{k/nu}(1)", Ao(k, nu) == N(k, 1, nu))
        eps = sum(Ae(k, nu) * s(nu, Fr(1, 2)) for nu in PK)
        want = 1 if not k else (Fr((-1)**(k[0]+1), 2**k[0]) if len(k) == 1 else 0)
        tally("Layers (c) epsilon", eps == want)
    # OC lesion: threshold 2m-1 instead of 2m+1
    for k in PK:
        a = m - 1; v = (-1)**sum(k) * Fr(2)**m * H[k](Fr(-2*a-1, 2))
        lesion("L5 OC at M=2m-1 (should sometimes fail)", not (v.denominator == 1 and v > 0))
    print(f"m={m} extra done")

for n, (a, b) in res.items(): print(f"  {n:58s} {a}/{b}")
print("LESIONS (must fire, i.e. >0):")
for n, (a, b) in lesions.items(): print(f"  {n:58s} fired {a}/{b}")
