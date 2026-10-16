from qsym_indep import *
SL3 = [[2,-1],[-1,2]]
PHIS = {
  "phi=0":        [[0,0],[0,0]],
  "Feigin 1->2":  [[0,-1],[0,0]],
  "Feigin 2->1":  [[0,0],[-1,0]],
  "random bilin": [[3,-2],[5,1]],
}
def tdeg(w): return sum(wdeg0(w,2))

def run(S, words, maxtot_tri, maxtot_pair):
    ao=ab=0; bo=bb=0; failex=[]
    tri=[(a,b,c) for a in words for b in words for c in words
         if tdeg(a)+tdeg(b)+tdeg(c) <= maxtot_tri]
    for a,b,c in tri:
        L = lin_product(S, lin_product(S,{a:lone()},{b:lone()}), {c:lone()})
        R = lin_product(S, {a:lone()}, lin_product(S,{b:lone()},{c:lone()}))
        if L==R: ao+=1
        else:
            ab+=1
            if len(failex)<2: failex.append((a,b,c))
    pairs=[(a,b) for a in words for b in words if tdeg(a)+tdeg(b)<=maxtot_pair]
    for a,b in pairs:
        lhs=defaultdict(lzero)
        for w,cf in lin_product(S,{a:lone()},{b:lone()}).items():
            for k in range(len(w)+1):
                lhs[(w[:k],w[k:])]=ladd(lhs[(w[:k],w[k:])],cf)
        lhs={k:v for k,v in lhs.items() if v}
        rhs=defaultdict(lzero)
        for i in range(len(a)+1):
            ap,app=a[:i],a[i:]
            for j in range(len(b)+1):
                bp,bpp=b[:j],b[j:]
                br=lmono(S.truepair(wdeg0(app,S.n),wdeg0(bp,S.n)))
                left=lin_product(S,{ap:lone()},{bp:lone()})
                right=lin_product(S,{app:lone()},{bpp:lone()})
                for wl,cl in left.items():
                    for wr,cr in right.items():
                        rhs[(wl,wr)]=ladd(rhs[(wl,wr)],lmul(br,lmul(cl,cr)))
        rhs={k:v for k,v in rhs.items() if v}
        if lhs==rhs: bo+=1
        else: bb+=1
    return (ao,ab,len(tri)),(bo,bb,len(pairs)),failex

words=[w for w in words_up_to((2,2)) if tdeg(w)<=3]
print("rank 2 (sl3 form), symbolic in q (exact Laurent).")
print("DOMAIN: %d words (total degree <= 3, incl. empty); triples with total deg <= 4; pairs with total deg <= 4"%len(words))
print()
for name,phi in PHIS.items():
    S=Setup(SL3,phi)
    (ao,ab,nt),(bo,bb,np_),_=run(S,words,4,4)
    print(f"{name:14s} assoc {ao}/{nt} pass ({ab} FAIL) | bialg {bo}/{np_} pass ({bb} FAIL)")
print()
print("POSITIVE CONTROL A: inverted braiding q^{-(a,b)} in crossings")
INV=[[-2,1],[1,-2]]
for name in ["phi=0","Feigin 1->2"]:
    S=Setup(SL3,PHIS[name],braid=INV)
    (ao,ab,nt),(bo,bb,np_),_=run(S,words,4,4)
    print(f"  {name:14s} assoc {ao}/{nt} ({ab} FAIL) | bialg {bo}/{np_} ({bb} FAIL)")
print()
print("POSITIVE CONTROL B: non-bilinear phi (breaks the 2-cocycle condition)")
class BadPhi(Setup):
    def ph(self,a,b):
        return sum(a)*sum(b)+(1 if (sum(a)>1 and sum(b)>1) else 0)
S=BadPhi(SL3,PHIS["phi=0"])
(ao,ab,nt),(bo,bb,np_),fx=run(S,words,4,4)
print(f"  non-bilinear phi assoc {ao}/{nt} ({ab} FAIL) | bialg {bo}/{np_} ({bb} FAIL)")
print("  example assoc failure:",fx[:1])
