from ds_engine import *
import itertools

def conj_full(lam):
    if not lam or lam[0]==0: return ()
    return tuple(sum(1 for p in lam if p>c) for c in range(lam[0]))

def peel(kappa,k):
    """subtract 1 from the k largest parts"""
    L=sorted(kappa,reverse=True)
    assert k<=len([p for p in L if p>0]), (kappa,k)
    L=[p-1 if i<k else p for i,p in enumerate(L)]
    return tuple(sorted([p for p in L if p>0],reverse=True))

def dom(a,b):
    """a dominates b, equal size"""
    assert sum(a)==sum(b)
    sa=sb=0
    for i in range(max(len(a),len(b))):
        sa+= a[i] if i<len(a) else 0
        sb+= b[i] if i<len(b) else 0
        if sa<sb: return False
    return True

print("=== Peel conjugate formula: (peel_k kappa)'_c = kappa'_c - min(k,kappa'_c) + min(k,kappa'_{c+1}) ===")
bad=0; tot=0
for n in range(1,13):
    for kappa in partitions(n):
        kc=conj_full(kappa)
        for k in range(1,len(kappa)+1):
            pk=conj_full(peel(kappa,k))
            for c in range(1,len(kc)+2):
                kcc = kc[c-1] if c-1<len(kc) else 0
                kcc1= kc[c]   if c  <len(kc) else 0
                pred= kcc - min(k,kcc) + min(k,kcc1)
                act = pk[c-1] if c-1<len(pk) else 0
                tot+=1
                if pred!=act:
                    bad+=1
                    if bad<=5: print('  MISMATCH kappa=%s k=%d c=%d pred=%d act=%d'%(str(kappa),k,c,pred,act))
print('  checked %d (kappa,k,c) with n<=12: %d mismatches'%(tot,bad))

print()
print("=== Peel Lemma: kappa <| lambda, |kappa|=|lambda|, k <= l(lambda)  =>  peel_k kappa <| peel_k lambda ===")
bad=0; tot=0
for n in range(1,13):
    ps=list(partitions(n))
    for lam in ps:
        for kap in ps:
            if not dom(lam,kap): continue   # kappa dominated by lambda
            for k in range(1,len(lam)+1):
                tot+=1
                pk_k=peel(kap,k); pk_l=peel(lam,k)
                if not dom(pk_l,pk_k):
                    bad+=1
                    if bad<=5: print('  COUNTEREXAMPLE lam=%s kap=%s k=%d -> %s vs %s'%(lam,kap,k,pk_l,pk_k))
print('  checked %d triples with n<=12: %d counterexamples'%(tot,bad))
