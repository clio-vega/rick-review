"""Green polynomials X^lambda_rho(t) for two-row lambda, from p_rho = sum_lam X^lam_rho P_lam(x;t).
Working in m=2 variables: P_lam with l(lam)>2 vanish there, so the coefficient of P_{(l1,l2)}
is read off exactly. HL polynomials from Macdonald III (2.2). Independent of Rick's engine.

Checks: (a) the Section 3(b) worked example lambda=(5,2), (x,y)=(4,3), X = t^2 - t
        (b) Rick's ex:tworow three-branch closed form
        (c) the Jing-Liu form X^lam_rho = pi_k + (t-1) sum_{j<k} t^{k-1-j} pi_j, k = lam_2,
            and whether swapping lam_1 <-> lam_2 gives a wrong formula (his new index clause)."""
import itertools, functools
import engine as E
from sympy import symbols, cancel, expand, Integer, Poly, factor, simplify, Matrix
t=E.t

X2=E.xs(2)
def vm(m):
    out=Integer(1)
    for i in range(1,m+1): out*=(1-t**i)/(1-t)
    return out
def v_lam(lam,n):
    lam=tuple(lam)+(0,)*(n-len(lam)); out=Integer(1)
    for val in set(lam): out*=vm(sum(1 for z in lam if z==val))
    return out
@functools.lru_cache(maxsize=None)
def HL2(lam):
    """Macdonald III (2.2) in 2 variables, parameter t"""
    n=2; lam=tuple(lam)+(0,)*(n-len(lam))
    num=(X2[0]-t*X2[1])/(X2[0]-X2[1])
    mon=X2[0]**lam[0]*X2[1]**lam[1]
    tot=0
    for w in itertools.permutations(range(2)):
        sub={X2[i]:X2[w[i]] for i in range(2)}
        tot+=(mon*num).subs(sub,simultaneous=True)
    return cancel(expand(cancel(tot/v_lam(lam,2))))

def p_rho(rho):
    out=Integer(1)
    for r in rho: out*=(X2[0]**r+X2[1]**r)
    return expand(out)

def green(lam,rho):
    """coefficient of P_lam in p_rho, lam of length <= 2"""
    n=sum(rho)
    parts=[p for p in E.partitions(n,maxlen=2)]
    target=E.to_mono_dict(p_rho(rho),X2,n)
    basis={p:E.to_mono_dict(HL2(p),X2,n) for p in parts}
    lams=[tuple(p) for p in parts]
    A=Matrix([[basis[p].get(l,0) for p in parts] for l in lams])
    b=Matrix([[target.get(l,0)] for l in lams])
    sol=A.solve(b)
    return cancel(sol[parts.index(tuple(lam))])

print("=== (a) Section 3(b) worked example ===")
g=cancel(green((5,2),(4,3)))
print(f"  X^(5,2)_(4,3)(t) computed independently = {factor(g)}")
print(f"  Rick's printed value t^2 - t : residual = {cancel(g-(t**2-t))}")

print()
print("=== (b) Rick's ex:tworow three-branch closed form ===")
def rick(lam,x,y):
    l1,l2=lam; m_xy=2 if x==y else 1
    if y<l2:  return (t-1)*t**(l2-1-y)*(1+t**y)
    if y==l2: return m_xy-(1-t)*t**(l2-1)
    return (t-1)*t**(l2-1)
ok=bad=0; bybranch={'y<l2':[0,0],'y=l2':[0,0],'y>l2':[0,0]}
fails=[]
for n in range(2,11):
    for l2 in range(1,n//2+1):
        l1=n-l2
        if l1<l2: continue
        for y in range(1,n//2+1):
            x=n-y
            if x<y: continue
            got=cancel(green((l1,l2),(x,y)))
            want=cancel(rick((l1,l2),x,y))
            br='y<l2' if y<l2 else ('y=l2' if y==l2 else 'y>l2')
            if cancel(got-want)==0: ok+=1; bybranch[br][0]+=1
            else:
                bad+=1; bybranch[br][1]+=1
                if len(fails)<5: fails.append(((l1,l2),(x,y),factor(got),factor(want)))
print(f"  ex:tworow: {ok} of {ok+bad} pass, {bad} fail   (|lambda| = 2..10, y <= x)")
for br,(o,b) in bybranch.items(): print(f"      branch {br:5s}: {o} pass, {b} fail   ({o+b} cases -- branch non-vacuous: {o+b>0})")
for f in fails: print("      FAIL",f)

print()
print("  controls (each MUST fail):")
def ctrl(name,fn):
    o=b=0
    for n in range(2,9):
        for l2 in range(1,n//2+1):
            l1=n-l2
            if l1<l2: continue
            for y in range(1,n//2+1):
                x=n-y
                if x<y: continue
                if cancel(green((l1,l2),(x,y))-fn((l1,l2),x,y))==0: o+=1
                else: b+=1
    print(f"    {name:44s} {b} of {o+b} FAIL (ok={o})")
ctrl("C1 branches keyed on lam_1 instead of lam_2", lambda lam,x,y: rick((lam[1],lam[0]),x,y) if lam[1]>=1 else 0)
ctrl("C2 (t-1) -> (1-t) throughout",                lambda lam,x,y: -rick(lam,x,y))
ctrl("C3 swap roles of x and y",                    lambda lam,x,y: rick(lam,y,x))
ctrl("C4 the correct formula (must PASS)",          rick)

print()
print("=== (c) Jing-Liu form, and Rick's new index clause ===")
def pi_j(rho,j):
    """number of j-subsets of the parts of rho whose sum ... = # j-subsets fixed by rho.
       For a permutation of cycle type rho, the number of j-element subsets of [n] fixed
       setwise-pointwise (i.e. unions of cycles) is the number of sub-multisets of rho summing to j."""
    cnt=0
    for r in range(len(rho)+1):
        for comb in itertools.combinations(range(len(rho)),r):
            if sum(rho[i] for i in comb)==j: cnt+=1
    return cnt
def jingliu(lam,rho):
    k=lam[1]
    return cancel(pi_j(rho,k)+(t-1)*sum(t**(k-1-j)*pi_j(rho,j) for j in range(k)))
ok=bad=0
for n in range(2,11):
    for l2 in range(0,n//2+1):
        l1=n-l2
        if l1<l2: continue
        for y in range(1,n//2+1):
            x=n-y
            if x<y: continue
            lam=(l1,l2) if l2>0 else (l1,)
            got=cancel(green(lam,(x,y)))
            want=jingliu((l1,l2),(x,y))
            if cancel(got-want)==0: ok+=1
            else: bad+=1
print(f"  Jing-Liu form with k = lambda_2 (Rick's reading): {ok} of {ok+bad} pass, {bad} fail")
ok2=bad2=0
for n in range(2,11):
    for l2 in range(1,n//2+1):
        l1=n-l2
        if l1<l2 or l1==l2: continue
        for y in range(1,n//2+1):
            x=n-y
            if x<y: continue
            got=cancel(green((l1,l2),(x,y)))
            want=jingliu((l2,l1),(x,y))   # k = lambda_1 : the SWAP he warns about
            if cancel(got-want)==0: ok2+=1
            else: bad2+=1
print(f"  with k = lambda_1 instead (the swap he warns about): {bad2} of {ok2+bad2} FAIL (ok={ok2})")
print("  -> his index clause 'swapping the two gives a wrong formula' is",
      "CONFIRMED" if bad2>0 else "NOT confirmed")
