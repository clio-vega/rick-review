"""eq:ncount and the r_v convention, plus honest vacuity count for the psi' check."""
import itertools
import engine as E
from sympy import Integer, binomial, cancel, symbols, expand
u=symbols('u')

def vstrips(rho,k,maxlen):
    rl=list(rho)+[0]*(maxlen-len(rho)); out=[]
    for add in itertools.product([0,1],repeat=maxlen):
        if sum(add)!=k: continue
        kap=[rl[i]+add[i] for i in range(maxlen)]
        if all(kap[i]>=kap[i+1] for i in range(maxlen-1)):
            out.append((tuple(z for z in kap if z>0), tuple(add)))
    return out

def mult(lam,v): return sum(1 for p in lam if p==v)

print("=== r_v: 'rows of kappa of length v ending in a strip box'  ==  kappa'_v - rho'_v ? ===")
ok=bad=0
for n in range(1,8):
    for rho in E.partitions(n):
        for k in range(1,6):
            for kap,add in vstrips(rho,k,len(rho)+k):
                kp=E.conj(kap); rp=E.conj(rho)
                rl=list(rho)+[0]*(len(add)-len(rho))
                for v in range(1,(kap[0] if kap else 0)+2):
                    # definition at longversion.tex:531
                    r_def = sum(1 for i in range(len(add)) if rl[i]+add[i]==v and add[i]==1)
                    # parenthetical at longversion.tex:588
                    r_par = (kp[v-1] if v-1<len(kp) else 0) - (rp[v-1] if v-1<len(rp) else 0)
                    if r_def==r_par: ok+=1
                    else:
                        bad+=1
                        if bad<4: print("   MISMATCH",rho,kap,v,r_def,r_par)
print(f"  the two definitions of r_v agree: {ok} of {ok+bad} column-values, {bad} mismatches")

print()
print("=== eq:ncount : n(kappa)-n(rho) = C(k,2) + inv(kappa/rho) + sum_v r_v(m_v-r_v) ===")
ok=bad=0; fails=[]
for n in range(1,10):
    for rho in E.partitions(n):
        for k in range(1,7):
            for kap,add in vstrips(rho,k,len(rho)+k):
                rl=list(rho)+[0]*(len(add)-len(rho))
                vmax=(kap[0] if kap else 0)+1
                r={v: sum(1 for i in range(len(add)) if rl[i]+add[i]==v and add[i]==1) for v in range(1,vmax+1)}
                m={v: mult(kap,v) for v in range(1,vmax+1)}
                inv = sum(r[v]*(m[w]-r[w]) for v in range(1,vmax+1) for w in range(v+1,vmax+1))
                rhs = binomial(k,2) + inv + sum(r[v]*(m[v]-r[v]) for v in range(1,vmax+1))
                lhs = E.n_stat(kap)-E.n_stat(rho)
                if lhs==rhs: ok+=1
                else:
                    bad+=1
                    if len(fails)<5: fails.append((rho,kap,k,lhs,rhs))
print(f"  eq:ncount: {ok} of {ok+bad} vertical strips pass, {bad} fail   (|rho| up to 9, k up to 6)")
for f in fails: print("     FAIL rho=%s kap=%s k=%s lhs=%s rhs=%s"%f)

print()
print("  controls on eq:ncount (each MUST fail):")
for lab,fn in [
  ("C1 drop the C(k,2) term",       lambda k,inv,cross: inv+cross),
  ("C2 C(k,2) -> k^2",              lambda k,inv,cross: k**2+inv+cross),
  ("C3 drop the cross term",        lambda k,inv,cross: binomial(k,2)+inv),
  ("C4 drop inv",                   lambda k,inv,cross: binomial(k,2)+cross),
]:
    o=b=0
    for n in range(1,8):
        for rho in E.partitions(n):
            for k in range(1,6):
                for kap,add in vstrips(rho,k,len(rho)+k):
                    rl=list(rho)+[0]*(len(add)-len(rho))
                    vmax=(kap[0] if kap else 0)+1
                    r={v: sum(1 for i in range(len(add)) if rl[i]+add[i]==v and add[i]==1) for v in range(1,vmax+1)}
                    m={v: mult(kap,v) for v in range(1,vmax+1)}
                    inv=sum(r[v]*(m[w]-r[w]) for v in range(1,vmax+1) for w in range(v+1,vmax+1))
                    cross=sum(r[v]*(m[v]-r[v]) for v in range(1,vmax+1))
                    if E.n_stat(kap)-E.n_stat(rho)==fn(k,inv,cross): o+=1
                    else: b+=1
    print(f"    {lab:30s} {b} of {o+b} FAIL (ok={o})")

print()
print("=== how many of the psi' Pieri cases actually TEST the binomial? ===")
def qb(m,r):
    if r<0 or r>m: return Integer(0)
    num=Integer(1);den=Integer(1)
    for i in range(r): num*=(1-u**(m-i)); den*=(1-u**(i+1))
    return cancel(num/den)
tot=nontriv=0
for n in [3,4]:
    for d in range(0,4):
        for rho in (list(E.partitions(d,maxlen=n)) if d>0 else [()]):
            for k in range(1,n+1):
                st=vstrips(tuple(rho),k,n)
                if not st: continue
                tot+=1
                anynon=False
                for kap,add in st:
                    kp=E.conj(kap); rp=E.conj(rho)
                    for v in range(1,(kap[0] if kap else 0)+1):
                        mv=(kp[v-1] if v-1<len(kp) else 0)-(kp[v] if v<len(kp) else 0)
                        rv=(kp[v-1] if v-1<len(kp) else 0)-(rp[v-1] if v-1<len(rp) else 0)
                        if qb(mv,rv)!=1: anynon=True
                if anynon: nontriv+=1
print(f"  psi' Pieri: {tot} cases total, {nontriv} have at least one coefficient != 1,")
print(f"              {tot-nontriv} are INSENSITIVE to the psi' formula (all coefficients 1).")
