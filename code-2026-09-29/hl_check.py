"""Rick's Step-H functional QJ(n,p) = sum_k f_k q_{n+k} q_{p-k}  (UID 728 Claim 6 / UID 724 Claim H).
His UID-728 sect.11(3) 'hunch': this equals Jing's two-row Hall-Littlewood Q_{(n,p)}.
Verified here against the DEFINITION of P_lambda as a symmetrised sum (Macdonald III.1),
not against the raising-operator formula he is trying to match -- so this is independent."""
import sympy as sp, itertools
from sympy import symbols, Integer as I
t=symbols('t')

def hl_P(lam, X):
    """P_lambda(x;t) = (1/v_lam) sum_{w in S_m} w( x^lam prod_{i<j} (x_i - t x_j)/(x_i-x_j) )"""
    m=len(X); lam=list(lam)+[0]*(m-len(lam))
    # v_lam(t) = prod_{i>=0} v_{m_i}(t),  v_r = prod_{j=1..r} (1-t^j)/(1-t)
    from collections import Counter
    cnt=Counter(lam)
    v=I(1)
    for val,mult in cnt.items():
        v*= sp.prod([(1-t**j)/(1-t) for j in range(1,mult+1)])
    tot=I(0)
    for w in itertools.permutations(range(m)):
        term=sp.prod([X[w[i]]**lam[i] for i in range(m)])
        pr=I(1)
        for i in range(m):
            for j in range(i+1,m):
                pr*= (X[w[i]]-t*X[w[j]])/(X[w[i]]-X[w[j]])
        tot+= term*pr
    return sp.cancel(sp.together(tot/v))

def b_lam(lam):
    from collections import Counter
    cnt=Counter([p for p in lam if p>0])
    return sp.prod([sp.prod([(1-t**j) for j in range(1,mult+1)]) for mult in cnt.values()]) or I(1)

def hl_Q(lam,X): return sp.cancel(b_lam(lam)*hl_P(lam,X))

def q_one(n,X):
    """one-row q_n = Q_{(n)}; q_0=1, q_{<0}=0"""
    if n<0: return I(0)
    if n==0: return I(1)
    return hl_Q([n],X)

def f(k): return I(1) if k==0 else t**k - t**(k-1)

def QJ(n,p,X): return sp.cancel(sum(f(k)*q_one(n+k,X)*q_one(p-k,X) for k in range(0,p+1)))

print("Rick's QJ(n,p) vs Hall-Littlewood Q_{(n,p)}   [m = number of variables]")
print("case n>=p  (a genuine partition):")
for m in [3,4]:
    X=symbols('X1:%d'%(m+1))
    for n in range(1,5):
        for p in range(1,n+1):
            d=sp.simplify(sp.expand(sp.cancel(QJ(n,p,X)-hl_Q([n,p],X))))
            print(f"  m={m} (n,p)=({n},{p}): QJ - Q_(n,p) = {d}")
print()
print("case n<p  (a composition -- straightening; Macdonald: Q_(n,p) = -Q_(p-1,n+1), and =0 if p=n+1):")
for m in [3]:
    X=symbols('X1:%d'%(m+1))
    for n in range(1,4):
        for p in range(n+1,5):
            lhs=QJ(n,p,X)
            if p==n+1: guess=I(0); lab="0"
            else: guess=-hl_Q([p-1,n+1],X); lab=f"-Q_({p-1},{n+1})"
            d=sp.simplify(sp.expand(sp.cancel(lhs-guess)))
            print(f"  m={m} (n,p)=({n},{p}): QJ - [{lab}] = {d}")
