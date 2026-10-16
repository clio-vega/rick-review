from qsym_indep import *
from math import comb
import sympy as sp
qs = sp.symbols('q')

def deg_(w,n):
    d=[0]*n
    for a in w: d[a]+=1
    return tuple(d)
def adc(S,i,Y):
    out=defaultdict(lzero)
    for w,c in Y.items():
        out[(i,)+w]=ladd(out[(i,)+w],c)
        e=S.truepair(tuple(1 if k==i else 0 for k in range(S.n)), deg_(w,S.n))
        out[w+(i,)]=ladd(out[w+(i,)],lneg(lmul(c,lmono(e))))
    return {w:c for w,c in out.items() if c}

def zeta_word(phi, w, ts, n):
    """phi-character value on the word w: prod t * q^{sum_{a<b} phi(alpha_wa, alpha_wb)}"""
    e=sum(phi[w[a]][w[b]] for a in range(len(w)) for b in range(a+1,len(w)))
    pref=sp.Integer(1)
    for a in w: pref*=ts[a]
    return pref*qs**e

def laur_to_sp(c): return sum(v*qs**e for e,v in c.items())

TYPES={"A1xA1":[[2,0],[0,2]],"A2":[[2,-1],[-1,2]],"B2":[[2,-2],[-2,4]],"G2":[[2,-3],[-3,6]]}
t1,t2=sp.symbols('t1 t2')
print("Thm 4(1)-(3), computed DIRECTLY in the free braided algebra (not from his closed formula).")
print("For each finite rank-2 type: which antisymmetric parts d = phi_ij - phi_ji kill BOTH q-Serre elements?")
print("(t_1,t_2 generic nonzero symbols; phi diagonal set to 0 -- it factors out.)")
print()
for tname,form in TYPES.items():
    S=Setup(form,[[0,0],[0,0]])
    c = form[0][1]                     # (alpha_1, alpha_2)
    a12 = 2*form[0][1]//form[0][0]; a21 = 2*form[1][0]//form[1][1]
    kills={}
    for (i,j) in [(0,1),(1,0)]:
        aii=form[i][i]; aij=form[i][j]
        n=1-2*aij//aii
        Y={(j,):lone()}
        for _ in range(n): Y=adc(S,i,Y)
        good=[]
        for d in range(-10,11):
            phi=[[0,0],[0,0]]
            phi[0][1]=d; phi[1][0]=0     # antisym part = d
            val=sum(laur_to_sp(cf)*zeta_word(phi,w,(t1,t2),2) for w,cf in Y.items())
            if sp.simplify(val)==0: good.append(d)
        kills[(i,j)]=good
    both=sorted(set(kills[(0,1)])&set(kills[(1,0)]))
    pred=sorted({c,-c})
    print(f"  {tname:6s} a12={a12} a21={a21} (a1,a2)={c}")
    print(f"     S_12 (n={1-a12}) killed at d in {kills[(0,1)]}")
    print(f"     S_21 (n={1-a21}) killed at d in {kills[(1,0)]}")
    print(f"     BOTH at d in {both}   | Thm 4(2) predicts +-(a1,a2) = {pred}   MATCH: {both==pred}")
    print(f"     d=0 (ordinary scalar characters) kills both: {0 in both}   | Thm 4(3) predicts False for edges")
    print()
print("AFFINE A1^(1) cross-check of his aside (a_ij=a_ji=-2, d=0 should be ALLOWED):")
form=[[2,-2],[-2,2]]
S=Setup(form,[[0,0],[0,0]])
res={}
for (i,j) in [(0,1),(1,0)]:
    n=1-2*form[i][j]//form[i][i]
    Y={(j,):lone()}
    for _ in range(n): Y=adc(S,i,Y)
    good=[d for d in range(-8,9)
          if sp.simplify(sum(laur_to_sp(cf)*zeta_word([[0,d],[0,0]],w,(t1,t2),2) for w,cf in Y.items()))==0]
    res[(i,j)]=good
both=sorted(set(res[(0,1)])&set(res[(1,0)]))
print(f"   S_12 killed at {res[(0,1)]}, S_21 at {res[(1,0)]}, BOTH at {both}")
print(f"   d=0 allowed: {0 in both}  (his aside says YES -- scalar characters nondegenerate in affine A1^(1))")
