from util import *
import sys, sympy as sp
NMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 7
t0 = int(rng.integers(2, p))
def cost(lam): return math.prod(math.comb(sum(lam), k) for k in sorted(lam)[:-1])
cache = {}
def es(lam, tt, K):
    key = (lam, tt, K)
    if key not in cache: cache[key] = estar(Ctx(1, tt, K, maxe=len(lam) + 1), lam)
    return cache[key]
def Lead(lam, mu, tt):
    l = len(lam); kp = kappa(lam, mu); c = es(lam, tt, l - kp + 1)[mu]; return c[l - kp]
def W_closed(k, J, tt):
    n = k + sum(J); v = (-1) ** len(J) * tq(n, tt) * inv(tq(k, tt)) % p
    for j in J: v = v * tq(k, tt, j) % p
    return v
def histories(lam, tt, Wf=None):
    """process lam_l..lam_1; labeled blocks; returns dict final sorted sizes -> (sum of weights, count, m)"""
    out = {}
    def rec(i, blocks, w, m):
        if i < 0:
            key = srt(blocks); s, c = out.get(key, (0, 0)); out[key] = ((s + w) % p, c + 1); return
        k = lam[i]
        rec(i - 1, blocks + [k], w, m)
        for T in subsets(blocks):
            if not T: continue
            J = tuple(sorted(blocks[x] for x in T))
            nb = [blocks[x] for x in range(len(blocks)) if x not in T] + [k + sum(J)]
            rec(i - 1, nb, w * (Wf or W_closed)(k, J, tt) % p, m + len(J))
    rec(len(lam) - 1, [], 1, 0); return out
STRAT={}; NSUM={}
def W_nosign(k,J,tt): return W_closed(k,J,tt)*(-1)**len(J)%p
R = Res("Thm3.7 NEG: weights without (-1)^p (should FAIL for odd m)")
for n in range(3, 8):
    for lam in partitions(n):
        if cost(lam) > 4e4: continue
        H = histories(lam, t0, W_nosign)
        for mu in partitions(n):
            if mu == lam or kappa(lam, mu) != len(mu): continue
            m = len(lam)-len(mu); mm=len(lam)-len(mu); _L=es(lam,t0,m+1)[mu][m];
            _o=(_L == H.get(mu,(0,0))[0]);
            STRAT.setdefault(mm%2,[0,0])[0 if _o else 1]+=1;
            NSUM.setdefault(mm%2,[0,0])[0 if _L==0 else 1]+=1;
            R.chk(_o, "")
print(R, "(expected FAIL)")

print("\n--- s2b Thm3.7 sign control, stratified by m = l(lam)-l(mu) mod 2 ---")
for k in sorted(STRAT):
    ok,bad=STRAT[k]; z,nz=NSUM[k]
    print(f"  m {'even' if k==0 else 'odd '}: ok={ok:3d} bad={bad:3d}   (Lead==0 in {z} of them)")
