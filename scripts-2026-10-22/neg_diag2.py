import itertools, random
from fractions import Fraction as Fr
exec(open('pinf_extra.py').read().split('print("== A.')[0])
random.seed(31337)
print("Correct predicate?  row k is identically zero iff head h_k < min(kappa) = kappa_1")
print("(entry (k,j) = x^.. * rho_{kappa_j}(x_k); rho_{kappa_j}(w_m)=0 iff m < kappa_j)\n")
tests=[((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:Fr(1),"C := 1"),
       ((2,3,4),[2,0,-2],[-2,-2,-2],lambda w:w[2]**2*w[3],"slope -2"),
       ((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:w[3]**2*w[4],"wrong C (s shifted)"),
       ((2,4,5),[1,0,-1],[-1,-1,-1],lambda w:w[2]**2*w[3],"non-consecutive (2,4,5)"),
       ((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:w[2]*w[3]**2,"C exponents swapped")]
allagree=True
for kap,t1,t2,C,lab in tests:
    z=0; rowpred=0; agree=0
    for _ in range(60):
        w=pt(16); hs=random.sample(range(1,16),len(kap)); xs=[w[m] for m in hs]
        zero_row = any(h < kap[0] for h in hs)          # h < min(kappa)=kappa_1
        d = Alt(kap,t1,xs,w)-C(w)*Alt(kap,t2,xs,w)
        isz = (d==0)
        z+=isz; rowpred+=zero_row; agree += (isz==zero_row)
    allagree &= (agree==60)
    print(f"  {lab:24s}: diff==0 in {z:2d}/60 ; zero-row predicate true in {rowpred:2d}/60 ; AGREE {agree}/60")
print(f"\n  predicate matches the vanishing EXACTLY in every trial: {allagree}")
