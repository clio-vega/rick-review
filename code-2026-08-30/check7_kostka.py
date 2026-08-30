from core import *
cnt={}
def rec(n,ok):
    cnt[n]=cnt.get(n,[0,0]); cnt[n][0]+=1; cnt[n][1]+=(1 if ok else 0)
    if not ok: print("   *** FAIL",n)
def parts3(n):
    return [(a,b,n-a-b) for a in range(n,-1,-1) for b in range(min(a,n-a),-1,-1)
            if n-a-b<=b]
def schur(mu):
    mu=list(mu)+[0]*(3-len(mu))
    return sp.expand(sp.cancel(sp.Matrix(3,3,lambda i,j: U[i]**(mu[j]+2-j)).det()/V))
def fac_schur(mu):
    mu=list(mu)+[0]*(3-len(mu))
    return sp.expand(sp.cancel(sp.Matrix(3,3,lambda i,j: ff(U[i],mu[j]+2-j)).det()/V))
# Kostka K_{mu',(2^b)} = # SSYT of shape mu' content (2^b) -- count directly
def kostka(shape, content):
    shape=[x for x in shape if x>0]
    rows=len(shape)
    def fill(idx, tab):
        if idx==len(content):
            return 1
        tot=0
        # place content[idx] copies of letter idx+1, horizontal strip
        def place(r, prev_end, left, tab):
            if left==0 or r==rows:
                return [tuple(tab)] if left==0 else []
            out=[]
            cur=tab[r]
            maxadd = (shape[r]-cur)
            # SSYT column-strict: new entries in row r must be > entries above in same column
            # horizontal strip condition: cur + k <= prev_end (row above's OLD length) for r>0
            lim = maxadd
            if r>0: lim=min(lim, tab[r-1]-cur)  # tab[r-1] already updated
            for k in range(min(left,max(lim,0)), -1, -1):
                nt=list(tab); nt[r]=cur+k
                out += place(r+1, cur, left-k, nt)
            return out
        # need strip added top-down using OLD upper-row lengths -> do rows top-down with old lengths
        old=list(tab)
        res=[]
        def go(r,left,new):
            if left==0 and r<=rows:
                res.append(tuple(new)+tuple(old[r:])); return
            if r==rows: return
            cur=old[r]; hi=shape[r]-cur
            if r>0: hi=min(hi, old[r-1]-cur)   # horizontal strip: <= old length of row above
            for k in range(0,min(left,max(hi,0))+1):
                go(r+1,left-k,new+[cur+k])
        go(0,content[idx],[])
        for nt in set(res):
            tot += fill(idx+1,list(nt))
        return tot
    return fill(0,[0]*rows)
def conj(mu):
    mu=[x for x in mu if x>0]
    if not mu: return []
    return [sum(1 for x in mu if x>j) for j in range(mu[0])]

for b in range(0,6):
    P=parts3(2*b)
    Smat=[schur(mu) for mu in P]
    tgt=sp.expand(e2**b)
    # linear solve over the monomial basis
    monos=sorted(set(sum([sp.Poly(x,u1,u2,u3).monoms() for x in Smat+[tgt]],[])))
    A=sp.Matrix([[sp.Poly(s,u1,u2,u3).coeff_monomial(u1**m[0]*u2**m[1]*u3**m[2]) for s in Smat] for m in monos])
    bvec=sp.Matrix([sp.Poly(tgt,u1,u2,u3).coeff_monomial(u1**m[0]*u2**m[1]*u3**m[2]) for m in monos])
    sol=A.solve_least_squares(bvec)
    rec('e_2^b = sum c_mu s_mu (exact)', sp.expand(sum(sol[i]*Smat[i] for i in range(len(P)))-tgt)==0)
    cs={P[i]:sol[i] for i in range(len(P)) if sol[i]!=0}
    # Kostka check
    kk={mu:kostka(conj(mu),[2]*b) for mu in cs}
    rec('c_mu == K_{mu\',(2^b)}', all(cs[mu]==kk[mu] for mu in cs))
    rec("Psi(e_2^b) = sum_mu K_{mu',(2^b)} s*_mu",
        sp.expand(to_E(Psi_u(e2**b)) - to_E(sum(c*fac_schur(mu) for mu,c in cs.items())))==0)
    print(f"   b={b}: support {dict(cs)}  kostka {kk}")
print()
for k,(n,g) in sorted(cnt.items()): print(f"  {k:42s} {g}/{n}")
