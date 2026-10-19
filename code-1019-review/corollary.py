"""(i) verify the two monotonicity facts my all-N proof of the triple-level
corollary uses; (ii) characterise the pair-level gap set (Task 3.2)."""
from itertools import combinations, chain
def geq(M,I):
    s,r=len(M),len(I)
    if s<r: return False
    return all(i<=m for i,m in zip(I,M[s-r:]))
def subsets(N): return list(chain.from_iterable(combinations(range(1,N+1),k) for k in range(N+1)))
def Eset(lam,mu,nu,a,b,N):
    g=[x for x in range(1,N+1) if x not in (a,b)]
    r=[]
    for k in range(len(g)+1):
        for M in combinations(g,k):
            if geq(nu,tuple(sorted(M+(a,b)))) and geq(M,lam) and geq(M,mu): r.append(M)
    return r

print("=== FACT 1: M subset M'  =>  M' >= M  (monotone under adding elements) ===")
bad=[]
for N in (4,5):
    for M in subsets(N):
        for Mp in subsets(N):
            if set(M)<=set(Mp) and not geq(Mp,M): bad.append((M,Mp))
print("  counterexamples:",len(bad),bad[:3])

print("=== FACT 2: nu >= lam, |nu|-2 >= |lam|  =>  (nu minus its 2 smallest) >= lam ===")
bad=[]
for N in (4,5,6):
    for nu in subsets(N):
        if len(nu)<2: continue
        Mpp=nu[2:]
        for lam in subsets(N):
            if geq(nu,lam) and len(Mpp)>=len(lam) and not geq(Mpp,lam): bad.append((nu,lam))
print("  counterexamples:",len(bad),bad[:3])

print("=== FACT 3 (the (=>) half, cardinality only): M'' in E => |nu| >= |M''|+2 ===")
bad=[]
for N in (3,4,5):
    for nu in subsets(N):
        for a,b in combinations(range(1,N+1),2):
            for lam in subsets(N):
                for mu in subsets(N):
                    if not(geq(nu,lam) and geq(nu,mu)): continue
                    for Mpp in Eset(lam,mu,nu,a,b,N):
                        if not (len(nu) >= len(Mpp)+2 and len(Mpp)>=max(len(lam),len(mu))):
                            bad.append((lam,mu,nu,a,b,Mpp))
print("  counterexamples:",len(bad),bad[:3])

print()
print("=== TASK 3.2: the pair-level gap set {jump>=2 but E(.;a,b)=empty} ===")
print("    candidate characterisation C1:  E != empty  <=>  a,b in nu and nu\\{a,b} >= lam,mu")
for N in (3,4,5):
    tot=0; viol=[]
    for nu in subsets(N):
        for a,b in combinations(range(1,N+1),2):
            for lam in subsets(N):
                for mu in subsets(N):
                    if not(geq(nu,lam) and geq(nu,mu)): continue
                    tot+=1
                    lhs = bool(Eset(lam,mu,nu,a,b,N))
                    rest = tuple(z for z in nu if z not in (a,b))
                    rhs = (a in nu and b in nu and geq(rest,lam) and geq(rest,mu))
                    if lhs!=rhs: viol.append((lam,mu,nu,a,b,lhs,rhs))
    print(f"  N={N}: cases={tot}  C1 violations={len(viol)}  {viol[:4]}")

print()
print("    => so the gap set is exactly {jump>=2} minus {a,b in nu and nu\\{a,b} >= lam,mu}")
for N in (3,4,5):
    gap=[]
    for nu in subsets(N):
        for a,b in combinations(range(1,N+1),2):
            for lam in subsets(N):
                for mu in subsets(N):
                    if not(geq(nu,lam) and geq(nu,mu)): continue
                    if len(nu)-max(len(lam),len(mu))>=2 and not Eset(lam,mu,nu,a,b,N):
                        gap.append((lam,mu,nu,a,b))
    nb = sum(1 for g in gap if not (g[3] in g[2] and g[4] in g[2]))
    print(f"  N={N}: |gap|={len(gap)}; of these {nb} have a notin nu or b notin nu "
          f"({len(gap)-nb} have a,b in nu but nu\\{{a,b}} too small)")

print()
print("=== MY REDUCTION LEMMA: E != empty  <=>  E contains an element of ")
print("    cardinality EXACTLY r0 = max(|lam|,|mu|)   (strip smallest elements) ===")
for N in (3,4,5):
    viol=[]
    for nu in subsets(N):
        for a,b in combinations(range(1,N+1),2):
            for lam in subsets(N):
                for mu in subsets(N):
                    if not(geq(nu,lam) and geq(nu,mu)): continue
                    E=Eset(lam,mu,nu,a,b,N); r0=max(len(lam),len(mu))
                    if bool(E) != any(len(x)==r0 for x in E): viol.append((lam,mu,nu,a,b))
    print(f"  N={N}: violations = {len(viol)}  {viol[:3]}")

print()
print("=== E != empty does NOT require a,b in nu  (so the pole locus is not")
print("    confined to pairs inside nu) -- exhibit witnesses ===")
for N in (3,4):
    wit=[]
    for nu in subsets(N):
        for a,b in combinations(range(1,N+1),2):
            for lam in subsets(N):
                for mu in subsets(N):
                    if not(geq(nu,lam) and geq(nu,mu)): continue
                    if Eset(lam,mu,nu,a,b,N) and not (a in nu and b in nu):
                        wit.append((lam,mu,nu,(a,b),Eset(lam,mu,nu,a,b,N)))
    print(f"  N={N}: {len(wit)} such (triple,pair); first 4: {wit[:4]}")
    nonempty=[w for w in wit if w[0] or w[1]]
    print(f"        of which with lam or mu nonempty: {len(nonempty)}; first 3: {nonempty[:3]}")
