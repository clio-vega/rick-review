"""Settle the F_3 bookkeeping by direct computation instead of by hand."""
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

def mul3(f,g,n=N): return [sum(f[i]*g[k-i] for i in range(k+1))%3 for k in range(n)]

# (1) direct: prod_k (1-t^k)^{p_k} in F_3[[t]], via repeated squaring on the exponent
def powser3(base,e,n=N):
    r=[0]*n; r[0]=1; bse=base[:]
    while e:
        if e&1: r=mul3(r,bse,n)
        bse=mul3(bse,bse,n); e>>=1
    return r
prod=[0]*N; prod[0]=1
for k in range(1,N):
    f=[0]*N; f[0]=1; f[k]=(-1)%3
    prod=mul3(prod,powser3(f,p[k]))
print("B(t) mod 3           :", [b[i]%3 for i in range(12)], "...  (all 0 after const:",
      all(b[i]%3==0 for i in range(1,N)),")")
print("prod_k (1-t^k)^{p_k} mod 3, orders 0..11:", prod[:12])
print("  == 1 ?", prod[0]==1 and all(x==0 for x in prod[1:]))

# (2) the Frobenius regrouping, computed the same way
def dig3(x,j):
    for _ in range(j): x//=3
    return x%3
c=[0]*N
for m in range(1,N):
    j=0; s=0
    while 3**j<=m:
        if m%(3**j)==0: s+=dig3(p[m//(3**j)],j)
        j+=1
    c[m]=s%3
prod2=[0]*N; prod2[0]=1
for m in range(1,N):
    if c[m]:
        f=[0]*N; f[0]=1; f[m]=(-1)%3
        prod2=mul3(prod2,powser3(f,c[m]))
print()
print("c_m (m=1..30) :", c[1:31])
print("prod_m (1-t^m)^{c_m} mod 3, orders 0..11:", prod2[:12])
print("  == 1 ?", prod2[0]==1 and all(x==0 for x in prod2[1:]))
print("  agrees with direct product ?", prod==prod2)
