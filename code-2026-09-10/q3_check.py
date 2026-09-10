"""Rick's mod9_investigation.md Q3: 'b'_k = a'_k mod 3, empirical, unexplained.'
His reduction says it is equivalent to  S_k := sum_{i<k} b'_i a'_{k-i} = 0 mod 3.
But (dagger) reads  b_k - a_k = 9 S_k, i.e.  3(b'_k - a'_k) = 9 S_k,  i.e.
      b'_k - a'_k = 3 S_k
so b'_k = a'_k mod 3 holds for EVERY k with no further input.
Test: does S_k = 0 mod 3?  If S_k is NOT always 0 mod 3 while b'_k = a'_k mod 3
still holds, Rick's stated equivalence is wrong (he needs mod 3, wrote mod 9)."""
from fractions import Fraction as Fr
N=30
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
a=[0]*N
for n in range(1,N): a[n]=b[n]-sum(a[k]*b[n-k] for k in range(1,n))
bp=[0]+[b[k]//3 for k in range(1,N)]; ap=[0]+[a[k]//3 for k in range(1,N)]

print(" k   b'_k-a'_k  == 3*S_k ?   S_k mod 3   b'_k=a'_k mod 3 ?")
allok=True; Smod=[]
for k in range(1,N):
    S=sum(bp[i]*ap[k-i] for i in range(1,k))
    idok = (bp[k]-ap[k] == 3*S)
    Smod.append(S%3); allok &= idok
    if k<=14: print(" %2d      %-8s        %d           %s"%(k,idok,S%3,(bp[k]-ap[k])%3==0))
print()
print("identity b'_k - a'_k = 3*S_k holds for all k<%d : %s"%(N,allok))
print("=> b'_k = a'_k mod 3 for EVERY k, unconditionally.")
print()
print("S_k mod 3, k=1..%d : %s"%(N-1,Smod))
print("is S_k = 0 mod 3 always (what Rick's reduction would require)?", all(s==0 for s in Smod))
print("=> Rick's stated equivalence needs S_k = 0 mod 3; it is FALSE, yet")
print("   b'_k = a'_k mod 3 still holds.  So the equivalence is misstated,")
print("   and Q3 is a corollary of his own (dagger), not an open problem.")
print()
print("b_k = a_k mod 27 (needs S_k = 0 mod 3), k where it holds:",
      [k for k in range(1,N) if (b[k]-a[k])%27==0])
