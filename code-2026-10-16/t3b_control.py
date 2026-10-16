from qsym_indep import *
from math import comb
exec(open('t3_serre.py').read().split('TYPES=')[0].split('from math import comb')[1])

def build_rhs(aii,aij,n,i,j):
    R=defaultdict(lzero)
    for p in range(n+1):
        co=lmul(lmono(aii*comb(p,2)+aij*p), gauss_binom(n,p,aii))
        if p%2: co=lneg(co)
        w=tuple([i]*(n-p))+(j,)+tuple([i]*p)
        R[w]=ladd(R[w],co)
    return {w:c for w,c in R.items() if c}

print("DECOUPLED control: braiding form held correct (B2), formula exponents perturbed.")
print("This perturbs entries INSIDE the test's read-set (row i), unlike my first attempt.")
S=Setup([[2,-2],[-2,4]],[[0,0],[0,0]])
i,j=0,1
aii,aij=2,-2; n=1-2*aij//aii
Y={(j,):lone()}
for _ in range(n): Y=adc(S,i,Y)
print(f"  baseline (aii={aii}, aij={aij}, n={n}): {Y==build_rhs(aii,aij,n,i,j)}   (expect True)")
for (dii,dij,lbl) in [(1,0,"q_ii -> q_ii*q"),(0,1,"q_ij -> q_ij*q"),(0,-1,"q_ij -> q_ij/q"),(-1,0,"q_ii -> q_ii/q")]:
    r=build_rhs(aii+dii,aij+dij,n,i,j)
    print(f"  {lbl:20s}: matches = {Y==r}   (expect False)")
print()
print("NOTE: only ROW i of the form is ever read, so the expansion holds for ANY")
print("bilinear braiding, symmetric or not -- a free strengthening of Thm 4(1).")
S2=Setup([[2,-2],[7,4]],[[0,0],[0,0]])    # row 1 arbitrary, row 0 intact
Y2={(j,):lone()}
for _ in range(n): Y2=adc(S2,i,Y2)
print("  row-1 scrambled, same row 0:", Y2==build_rhs(2,-2,n,i,j), "(True => symmetry unused)")
