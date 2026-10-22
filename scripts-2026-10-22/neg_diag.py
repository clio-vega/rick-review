import itertools, random
from fractions import Fraction as Fr
exec(open('pinf_extra.py').read().split('print("== A.')[0])
random.seed(31337)
print("DIAGNOSIS: does a vanishing COLUMN (all heads < kappa_j) zero both sides?")
def diag(kap,th1,th2,C_fn,lab,heads_from):
    z=deg=0
    for _ in range(40):
        w=pt(16); hs=random.sample(heads_from,len(kap)); xs=[w[m] for m in hs]
        # a column j is identically zero iff every head index < kap[j]
        degen=any(all(h<kap[j] for h in hs) for j in range(len(kap)))
        d=Alt(kap,th1,xs,w)-C_fn(w)*Alt(kap,th2,xs,w)
        if d==0:
            z+=1; deg+=degen
    return z,deg
tests=[((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:Fr(1),"C := 1"),
       ((2,3,4),[2,0,-2],[-2,-2,-2],lambda w:w[2]**2*w[3],"slope -2"),
       ((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:w[3]**2*w[4],"wrong C (s shifted)"),
       ((2,4,5),[1,0,-1],[-1,-1,-1],lambda w:w[2]**2*w[3],"non-consecutive (2,4,5)"),
       ((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:w[2]*w[3]**2,"C exponents swapped")]
print("\n  heads sampled from ALL of [1..15] (what I did before):")
for kap,t1,t2,C,lab in tests:
    z,deg=diag(kap,t1,t2,C,lab,list(range(1,16)))
    print(f"    {lab:26s}: {z}/40 trials gave 0 ; of those, {deg} had a vanishing column")
print("\n  heads sampled from [max(kappa) .. 15] (non-degenerate by construction):")
for kap,t1,t2,C,lab in tests:
    z,deg=diag(kap,t1,t2,C,lab,list(range(max(kap),16)))
    print(f"    {lab:26s}: {z}/40 trials gave 0  -> control fires {40-z}/40")
