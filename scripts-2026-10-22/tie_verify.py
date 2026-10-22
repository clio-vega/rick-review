"""Target 1b: reproduce Rick's lambda=(2,3) tie counterexample and P1^infty.
Clio 2026-10-22.  Psi re-implemented from the primitive sum (own code)."""
import itertools, random
from fractions import Fraction as Fr
random.seed(1022)

def rho(kappa, X, w):
    e = Fr(1)
    for k in range(1, kappa): e *= (1 - w[k]/X)
    return e
def Psi(kap, th, M, w):
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
def pt(N): return {k: Fr(random.randint(2,211), random.randint(2,211)) + 3*k for k in range(1,N+1)}
def eS(S, w):
    v = Fr(1)
    for m in S: v *= w[m]
    return v

print("== 1b-i: the two-term tie at lambda=(2,3):  1 - Psi_{(2),0}(S) =?= e_S^-2 + w_1 Psi_{(1),-1}(S)")
for S in [(2,3,4), (1,2,3,4), (2,3,4,5), (1,2,3,4,5), (3,4,5), (2,4,5)]:
    res = []
    for _ in range(3):
        w = pt(max(S)+1)
        L = 1 - Psi((2,), (0,), S, w)
        R = eS(S,w)**-2 + w[1]*Psi((1,), (-1,), S, w)
        res.append(L-R == 0)
    print(f"   S={S}: holds={all(res)}  ({sum(res)}/3)")

print("\n== 1b-ii: is the two-term sum genuinely two-term?  single-instance fit search")
# Rick: no single-instance fit e_S^k Psi_{kappa',t} over kappa' in {(1),(2)}, |t|<=3, -4<=k<=2
S_list = [(2,3,4),(1,2,3,4)]
pts = {S: [pt(max(S)+1) for _ in range(3)] for S in S_list}
fits = []
for kp in [(1,),(2,)]:
    for t in range(-3,4):
        for k in range(-4,3):
            if all(all(1 - Psi((2,),(0,),S,w) - eS(S,w)**k * Psi(kp,(t,),S,w) == 0
                       for w in pts[S]) for S in S_list):
                fits.append((kp,t,k))
print(f"   single-instance fits found: {fits}   (Rick claims none)")

print("\n== 1b-iii: P1^infty   Psi_{[r-1],-r} + (-1)^r Psi_{[r],1-r} = e_S^-2 Psi_{[r-1],2-r}")
nok=ntot=0
for r in range(1,5):
    for S in [tuple(range(1,m+1)) for m in range(max(r,2), 6)]:
        if len(S) < r: continue
        for _ in range(2):
            w = pt(max(S)+1)
            A = Psi(tuple(range(1,r)), (-r,)*(r-1), S, w)
            B = Psi(tuple(range(1,r+1)), (1-r,)*r, S, w)
            C = eS(S,w)**-2 * Psi(tuple(range(1,r)), (2-r,)*(r-1), S, w)
            ntot += 1; nok += (A + (-1)**r * B - C == 0)
print(f"   P1^infty: {nok}/{ntot} exact")
# control: RHS twist 3-r must FAIL
bad=0; tot=0
for r in range(2,5):
    for S in [(1,2,3,4),(1,2,3,4,5)]:
        w=pt(max(S)+1)
        A=Psi(tuple(range(1,r)),(-r,)*(r-1),S,w); B=Psi(tuple(range(1,r+1)),(1-r,)*r,S,w)
        C=eS(S,w)**-2*Psi(tuple(range(1,r)),(3-r,)*(r-1),S,w)
        tot+=1; bad += (A+(-1)**r*B-C != 0)
print(f"   control (RHS twist 3-r) fails as it should: {bad}/{tot}")

print("\n== 1b-iv: DOMAIN QUESTION. G = 'consecutive gaps >= 2' (W-sharp L17).")
def inG(lam): return all(lam[i+1]-lam[i] >= 2 for i in range(len(lam)-1))
def maxblock(lam):
    b=run=1
    for i in range(len(lam)-1):
        run = run+1 if lam[i+1]==lam[i]+1 else 1
        b=max(b,run)
    return b
for lam in [(2,3),(2,3,4),(3,4,5),(3,4),(1,),(),(1,3),(1,3,5),(2,5),(1,4,6)]:
    print(f"   lambda={str(lam):10s} in G = {str(inG(lam)):5s}   longest consecutive block = {maxblock(lam) if lam else 0}")
