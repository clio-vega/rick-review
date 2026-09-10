"""Is Rick's empirical p_k mod 3 pattern FORCED by the proved b_k = 0 mod 3?

Over F_3, B(t) = 1 + sum b_k t^k = 1.  PBW gives prod_k (1-t^k)^{p_k} = 1/B = 1.
Frobenius in char 3: (1-t^k)^{3^j} = 1 - t^{k 3^j}.  Writing p_k = sum_j d_{k,j} 3^j,
   prod_k (1-t^k)^{p_k} = prod_m (1-t^m)^{c_m},   c_m = sum_{k 3^j = m} d_{k,j} mod 3.
The map (c_m) -> prod (1-t^m)^{c_m} is triangular hence injective over F_3, so
c_m = 0 for EVERY m.  Test that, and see what it forces on p_k mod 3.
"""
from fractions import Fraction as Fr
N=40
def mul(f,g,n=N): return [sum(f[i]*g[k-i] for i in range(k+1)) for k in range(n)]
def inv(f,n=N):
    g=[Fr(1,1)/f[0]]+[Fr(0)]*(n-1)
    for k in range(1,n): g[k]=-sum(f[i]*g[k-i] for i in range(1,k+1))/f[0]
    return g
F=[Fr(0)]*N
for _ in range(N+2):
    g=[3-2*F[0]]+[-2*x for x in F[1:]]
    num=mul([Fr(0),Fr(1)]+[Fr(0)]*(N-2),mul(g,g))
    omF=[1-F[0]]+[-x for x in F[1:]]
    den=mul(mul(omF,omF),mul(omF,[3-4*F[0]]+[-4*x for x in F[1:]]))
    F=mul(num,inv(den))
b=[1]+[int(x) for x in F[1:]]
m_=len(b); l=[0]*m_
for n in range(1,m_): l[n]=n*b[n]-sum(l[k]*b[n-k] for k in range(1,n))
p=[0]*m_
for n in range(1,m_):
    s=l[n]-sum(d*p[d] for d in range(1,n) if n%d==0); assert s%n==0; p[n]=s//n

def digits3(x):
    d=[]
    while x: d.append(x%3); x//=3
    return d

M=N-1
print("b_k = 0 mod 3 for all k<=%d : %s" % (M, all(b[k]%3==0 for k in range(1,M+1))))
print()
bad=[]
for m in range(1,M+1):
    c=0; k=m; j=0
    while k>=1:
        if k*(3**j)==m:
            dd=digits3(p[k]); c += dd[j] if j<len(dd) else 0
        if m%(3**(j+1))==0: j+=1; k=m//(3**j)
        else: break
    if c%3!=0: bad.append((m,c%3))
print("c_m != 0 for m<=%d :"%M, bad if bad else "NONE  -- all c_m vanish, as the theory predicts")
print()
print("Consequence for 3 nmid m (only the pair (k,j)=(m,0) occurs, so c_m = p_m mod 3):")
print("  p_m mod 3 for 3 nmid m, m<=%d : %s"%(M,[p[m]%3 for m in range(1,M+1) if m%3]))
print("  all zero:", all(p[m]%3==0 for m in range(1,M+1) if m%3))
print()
print("Consequence for m = 3m' (c_m = d_{3m',0} + d_{m',1} + ... = 0):")
for m in range(3,M+1,3):
    mp=m//3
    print("  m=%2d: p_m mod 3 = %d ;  3^1-digit of p_%d = %d" %
          (m, p[m]%3, mp, (digits3(p[mp])[1] if len(digits3(p[mp]))>1 else 0)))
print()
print("full p_k mod 3, k=1..%d:"%M, [p[k]%3 for k in range(1,M+1)])
print("Rick's stated pattern   :", [0 if k%3 else 2 for k in range(1,M+1)])
print("pattern holds to k=%d   : %s"%(M,[p[k]%3 for k in range(1,M+1)]==[0 if k%3 else 2 for k in range(1,M+1)]))
