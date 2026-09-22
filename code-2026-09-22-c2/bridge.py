"""Dictionary between Neyman's C_{k,n} coordinates and Clio's bead coordinates Cyl^{n,m},
then (T1) a re-test of Clio Thm 8.1 in Neyman's coordinates and (T2) a NEW corollary obtained
by combining Neyman Cor.\\label{oneschurcor} with Clio Thm 8.1."""
from neyman_check import *
from itertools import product

def to_x(lam, k, n):
    """x_i = lambda_{-i} + i, i = 1..k.  (m := k, total := n.)"""
    return tuple(part_at(lam, -i, k, n) + i for i in range(1, k + 1))

def x_at(x, i, k, n):
    q, r = divmod(i - 1, k)
    return x[r] + q * n

def u(x):
    return sum(x)

def greedy_hat(lam, mu, k, n, ell):
    """Clio Def 5.1 greedy chain g^t_i = min(g^{t-1}_{i+1}-1, lambda_i); returns sorted gamma,
    or None if the chain fails to reach lambda in ell steps (T_ell empty)."""
    L = to_x(lam, k, n); g = to_x(mu, k, n)
    gam = []
    for t in range(ell):
        gn = tuple(min(x_at(g, i + 1, k, n) - 1, x_at(L, i, k, n)) for i in range(1, k + 1))
        gam.append(u(gn) - u(g)); g = gn
    if g != L: return None
    return tuple(sorted(gam, reverse=True))

def dom_leq(a, b):
    """a <| b for compositions of equal size, comparing sorted partial sums."""
    A = sorted(a, reverse=True); B = sorted(b, reverse=True)
    if sum(A) != sum(B): return False
    sa = sb = 0
    for i in range(max(len(A), len(B))):
        sa += A[i] if i < len(A) else 0
        sb += B[i] if i < len(B) else 0
        if sa > sb: return False
    return True

def maximals(hats):
    hs = sorted(set(hats))
    return sorted({h for h in hs if not any(g != h and dom_leq(h, g) for g in hs)})

# ---------------- T1: Clio Thm 8.1, re-tested in Neyman's coordinates ----------------
print("=== T1  supp(s^c_{lambda/mu}(x_1..x_ell)) == {alpha : sort(alpha) <| lambdahat} ===")
tot = bad = 0
for (k, n) in [(1,3),(2,4),(2,5),(3,5),(3,6)]:
    cands = [t for t in product(range(0,3), repeat=k) if is_cylpar(t,k,n)]
    for lam in cands:
        for mu in cands:
            if not contains(lam,mu,k,n): continue
            for ell in (1,2,3,4):
                gf = {w:c for w,c in gf_chain(lam,mu,k,n,ell).items() if c}
                hat = greedy_hat(lam,mu,k,n,ell)
                if not gf:
                    tot += 1
                    if hat is not None: bad += 1; print("  FAIL empty-but-hat",k,n,lam,mu,ell,hat)
                    continue
                if hat is None:
                    tot += 1; bad += 1; print("  FAIL nonempty-but-no-hat",k,n,lam,mu,ell); continue
                pred = {a for a in product(range(0, sum(hat)+1), repeat=ell)
                        if sum(a)==sum(hat) and dom_leq(a,hat)}
                tot += 1
                if set(gf) != pred:
                    bad += 1
                    if bad < 4: print("  FAIL",k,n,lam,mu,ell,"hat",hat,"extra",set(gf)-pred,"missing",pred-set(gf))
print(f"  {tot} (k,n,lambda,mu,ell) instances, {bad} failures")

# ---------------- T2: new corollary, Neyman Cor.oneschurcor  x  Clio Thm 8.1 ----------------
print("=== T2  max_<| { lambdahat(alpha/mu) : |alpha/mu|=d } == max_<| { lambdahat(lam/alpha) : |lam/alpha|=d } ===")
def mus_below(alpha,k,n,d):
    return [tuple(alpha[i]-dl[i] for i in range(k)) for dl in product(range(d+1),repeat=k)
            if sum(dl)==d and is_cylpar(tuple(alpha[i]-dl[i] for i in range(k)),k,n)]
def lams_above(alpha,k,n,d):
    return [tuple(alpha[i]+dl[i] for i in range(k)) for dl in product(range(d+1),repeat=k)
            if sum(dl)==d and is_cylpar(tuple(alpha[i]+dl[i] for i in range(k)),k,n)]
tot=bad=nontriv=0
for (k,n) in [(1,3),(2,4),(2,5),(3,5),(3,6),(2,6),(4,6)]:
    cands=[t for t in product(range(0,3),repeat=k) if is_cylpar(t,k,n)]
    for alpha in cands:
        for d in range(1,5):
            for ell in (1,2,3,4):
                Lh=[h for mu in mus_below(alpha,k,n,d) if (h:=greedy_hat(alpha,mu,k,n,ell))]
                Rh=[h for lam in lams_above(alpha,k,n,d) if (h:=greedy_hat(lam,alpha,k,n,ell))]
                if not Lh and not Rh: continue
                tot+=1
                if len(set(Lh))>1 or len(set(Rh))>1: nontriv+=1
                if maximals(Lh)!=maximals(Rh):
                    bad+=1
                    if bad<5: print("  FAIL",k,n,alpha,d,ell,maximals(Lh),maximals(Rh))
print(f"  {tot} (k,n,alpha,d,ell) instances ({nontriv} with >1 distinct hat on a side), {bad} failures")
