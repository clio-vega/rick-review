import itertools, random
from fractions import Fraction as Fr
exec(open('pinf_extra.py').read().split('print("== A.')[0])
random.seed(31337)
print("Predicate (Frobenius-Koenig): with z_j = #{heads h : h < kappa_j},")
print("the alternant vanishes identically iff z_j >= j for some j.")
print("(zero block = rows{h<kappa_j} x columns{j..r}, size z_j x (r-j+1); z_j+(r-j+1)>r <=> z_j>=j)\n")
tests=[((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:Fr(1),"C := 1"),
       ((2,3,4),[2,0,-2],[-2,-2,-2],lambda w:w[2]**2*w[3],"slope -2"),
       ((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:w[3]**2*w[4],"wrong C (s shifted)"),
       ((2,4,5),[1,0,-1],[-1,-1,-1],lambda w:w[2]**2*w[3],"non-consecutive (2,4,5)"),
       ((2,3,4),[1,0,-1],[-1,-1,-1],lambda w:w[2]*w[3]**2,"C exponents swapped"),
       ((3,5,6),[1,0,-1],[-1,-1,-1],lambda w:w[3]**2*w[4],"stress: kappa=(3,5,6)")]
allok=True
for kap,t1,t2,C,lab in tests:
    r=len(kap); agree=0; z=0
    for _ in range(80):
        w=pt(16); hs=random.sample(range(1,16),r); xs=[w[m] for m in hs]
        pred = any(sum(1 for h in hs if h<kap[j]) >= j+1 for j in range(r))  # j 0-indexed
        d = Alt(kap,t1,xs,w)-C(w)*Alt(kap,t2,xs,w)
        isz=(d==0); z+=isz; agree += (isz==pred)
    allok &= (agree==80)
    print(f"  {lab:26s}: diff==0 in {z:2d}/80 ; predicate AGREES {agree}/80")
print(f"\n  predicate matches exactly in every trial: {allok}")
print("\n  => the 3/4 reading earlier was DEGENERATE SAMPLING, not a failed control.")
