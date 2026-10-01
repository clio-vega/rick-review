from ds_engine import *
import itertools

def omega(a): return sum(sp.binomial(v,2) for v in a)
def sort_t(a): return tuple(sorted([v for v in a if v>0],reverse=True))
def conj_full(lam):
    if not lam or lam[0]==0: return ()
    return tuple(sum(1 for p in lam if p>c) for c in range(lam[0]))
def dom(a,b):
    sa=sb=0
    for i in range(max(len(a),len(b))):
        sa+= a[i] if i<len(a) else 0
        sb+= b[i] if i<len(b) else 0
        if sa<sb: return False
    return True

print("Lemma B at t=0: Lambda^0_lam(alpha) := [s^{omega(alpha)}] a^lam_alpha  ==  [ sort(alpha) <| lam' ]")
for n in (2,3,4):
  for m in (n, n+1):
    X=xs(m)
    for lam in partitions(n):
        if len(lam)>m: continue
        P=sp.expand(sp.cancel(eqt(lam,X,sval=s,tval=sp.Integer(0))))
        Pp=sp.Poly(P,*X)
        lamc=conj_full(lam)
        bad=[]; nchk=0
        # every alpha in Z_{>=0}^m of weight n
        for alpha in itertools.product(range(n+1),repeat=m):
            if sum(alpha)!=n: continue
            nchk+=1
            coef=Pp.coeff_monomial(sp.prod([X[i]**alpha[i] for i in range(m)]))
            inset = dom(lamc, sort_t(alpha))   # sort(alpha) <| lam'
            if coef==0:
                got=0; val=None
            else:
                pol=sp.Poly(sp.simplify(coef),s)
                val=min(mm[0] for mm in pol.monoms())
                got=sp.simplify(pol.coeff_monomial(s**omega(alpha)))
            want = 1 if inset else 0
            if sp.simplify(got-want)!=0 or (inset and val!=omega(alpha)):
                bad.append((alpha,inset,got,val,omega(alpha)))
        print('  n=%d m=%d lam=%-12s alphas=%-4d  Lemma B %s'%(n,m,str(lam),nchk,'OK' if not bad else 'FAILS: %s'%bad[:3]))
