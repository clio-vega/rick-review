from fractions import Fraction
from testZ import H_poly
m=4; k=(4,3,2,1)
P,_ = H_poly(k,m)
print("Rick's worked example (Z file, Section 4): kappa=(4,3,2,1), m=4, r'=5, W={3,5,7}")
print('he reports the sign row "+000+++" for (-1)^{|kappa|} H_kappa(-M/2), M=1,3,...,13')
row=""
print(f"  {'M':>3s} {'H(-M/2)':>14s} {'sign':>5s}")
for M in range(1,14,2):
    v=P(Fraction(-M,2)); s=(-1)**sum(k)*v
    ch = '0' if s==0 else ('+' if s>0 else '-')
    row+=ch
    print(f"  {M:>3d} {str(v):>14s} {ch:>5s}")
print(f"  my sign row: {row}    Rick's: +000+++    match={row=='+000+++'}")
