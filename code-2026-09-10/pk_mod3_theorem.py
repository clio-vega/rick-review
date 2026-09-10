"""Rick's p_k mod 3 comment: what is actually true, and what is not.

PROVED INPUT (Rick, Day 148): b_k = 0 mod 3 for all k>=1, i.e. B(t) = 1 in F_3[[t]].
PBW:  prod_{k>=1} (1-t^k)^{p_k} = 1/B(t) = 1  in F_3[[t]].
Frobenius in char 3: (1-t^k)^{3^j} = 1 - t^{k 3^j}.  With p_k = sum_j d_{k,j} 3^j,
      prod_k (1-t^k)^{p_k} = prod_m (1-t^m)^{C_m},  C_m := sum_{3^j | m} d_{m/3^j, j}
as INTEGER exponents.  Exponents are NOT reducible mod 3 -- (1-t^m)^3 = 1-t^{3m} is
not 1 -- so writing C_m = 3q+r replaces q by a CARRY into level 3m.  After carrying
(in increasing m) the residual exponents gamma_m lie in {0,1,2}, and the map
(gamma_m) -> prod (1-t^m)^{gamma_m} is triangular hence injective, so gamma_m = 0 for all m.

CONSEQUENCE.  Carries only ever land on multiples of 3.  So for 3 nmid m nothing
carries in, and C_m has only its j=0 term:  gamma_m = p_m mod 3 = 0.
      ==> THEOREM: p_m = 0 mod 3 whenever 3 does not divide m.
For 3 | m the value p_m mod 3 is fixed by carries out of level m/3, i.e. by higher
base-3 digits of p_{m/3}, p_{m/9}, ... -- a base-3 carry recursion, NOT a period-3 law.
"""
from fractions import Fraction as Fr
N=60
def mul(f,g,n=N): return [sum(f[i]*g[k-i] for i in range(k+1)) for k in range(n)]
def inv(f,n=N):
    g=[Fr(1,1)/f[0]]+[Fr(0)]*(n-1)
    for k in range(1,n): g[k]=-sum(f[i]*g[k-i] for i in range(1,k+1))/f[0]
    return g
F=[Fr(0)]*N
for _ in range(N+3):
    g=[3-2*F[0]]+[-2*x for x in F[1:]]
    num=mul([Fr(0),Fr(1)]+[Fr(0)]*(N-2),mul(g,g))
    omF=[1-F[0]]+[-x for x in F[1:]]
    den=mul(mul(omF,omF),mul(omF,[3-4*F[0]]+[-4*x for x in F[1:]]))
    F=mul(num,inv(den))
b=[1]+[int(x) for x in F[1:]]
l=[0]*N
for n in range(1,N): l[n]=n*b[n]-sum(l[k]*b[n-k] for k in range(1,n))
p=[0]*N
for n in range(1,N):
    s=l[n]-sum(d*p[d] for d in range(1,n) if n%d==0); assert s%n==0; p[n]=s//n
def dig3(x,j):
    for _ in range(j): x//=3
    return x%3

M=N-1
C=[0]*(3*N)
for m in range(1,N):
    j=0
    while 3**j<=m:
        if m%(3**j)==0: C[m]+=dig3(p[m//(3**j)],j)
        j+=1
gamma=[0]*(3*N)
for m in range(1,N):                       # carry upward, increasing m
    gamma[m]=C[m]%3
    if 3*m<3*N: C[3*m]+=C[m]//3
print("after carrying, gamma_m for m=1..%d:"%M, gamma[1:M+1])
print("all gamma_m zero (as injectivity forces):", all(gamma[m]==0 for m in range(1,M+1)))
print()
print("THEOREM  p_m = 0 mod 3 for 3 nmid m -- verified to m=%d: %s"
      % (M, all(p[m]%3==0 for m in range(1,M+1) if m%3)))
print()
print("Rick's Sequence-3 %%C also claims p_m = 2 mod 3 whenever 3 | m.")
vals=[(m,p[m]%3) for m in range(3,M+1,3)]
cex=[(m,v) for m,v in vals if v!=2]
print("  (m, p_m mod 3) :", vals)
print("  COUNTEREXAMPLES:", cex)
print("  first failure  : m =", cex[0][0] if cex else None)
