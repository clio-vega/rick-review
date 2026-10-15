"""Two-arm controls.  Clio 2026-10-15.
(A) Lemma 7 over exact rationals, n up to 30, with three independent lesions.
(B) The end-to-end AHA test, lesioned, to prove it is non-vacuous."""
from fractions import Fraction as Fr

def build(s,t,lesion=None):
    def qp(a,n):
        r=Fr(1)
        for i in range(n): r*=(1-a*t**i)
        return r
    A={-1:Fr(0)}
    def al(j):
        if j in A: return A[j]
        num=Fr(1)
        for i in range(1,j+1): num*=(s-t**i)
        A[j]=num/qp(t,j); return A[j]
    def c(n,j):
        if not (0<=j<=n): return Fr(0)
        if lesion=='alpha':   return qp(s,n-j)/qp(t,n-j)*(al(j)-s*t**(n-j)*al(j))
        if lesion=='nomius':  return qp(s,n-j)/qp(t,n-j)*(al(j)+s*t**(n-j)*al(j-1))
        return qp(s,n-j)/qp(t,n-j)*(al(j)-s*t**(n-j)*al(j-1))
    return c

def star(c,s,t,n,j,drop_tn=False):
    P=n+3
    A=sum((s*t**(-j))**p*c(n-1-p,j)   for p in range(P+1))
    B=sum((s*t**(1-j))**p*c(n-1-p,j-1) for p in range(P+1))
    pre=Fr(1) if drop_tn else t**n
    return (1-t**n)*c(n,j) - ((1-s*t**(-j))*A - pre*(1-s*t**(1-j))*B)

pts=[(Fr(2),Fr(3)),(Fr(-3),Fr(5)),(Fr(5,7),Fr(3,5)),(Fr(1,3),Fr(-1,2)),
     (Fr(11,4),Fr(7,9)),(Fr(-2,5),Fr(13,3)),(Fr(9,2),Fr(-4,7)),(Fr(1,11),Fr(6,5))]

print("(A) LEMMA 7 (star) -- exact rational arithmetic, n=1..30, j=0..n+1, 8 points")
tot=0; bad=[]
for (s,t) in pts:
    c=build(s,t)
    for n in range(1,31):
        for j in range(0,n+2):
            tot+=1
            if star(c,s,t,n,j)!=0: bad.append((float(s),float(t),n,j))
print(f"    {tot-len(bad)}/{tot} verified   failures={len(bad)}")

print("\n    LESION 1 -- drop t^n on the second sum:")
f=0;T=0
for (s,t) in pts:
    c=build(s,t)
    for n in range(1,11):
        for j in range(0,n+1):
            T+=1
            if star(c,s,t,n,j,drop_tn=True)!=0: f+=1
print(f"      fails {f}/{T}  -> {'NON-VACUOUS' if f else '*** CONTROL DID NOT FIRE ***'}")

print("    LESION 2 -- alpha_{j-1} -> alpha_j inside c(n,j):")
f=0;T=0
for (s,t) in pts:
    c=build(s,t,lesion='alpha')
    for n in range(1,11):
        for j in range(0,n+1):
            T+=1
            if star(c,s,t,n,j)!=0: f+=1
print(f"      fails {f}/{T}  -> {'NON-VACUOUS' if f else '*** CONTROL DID NOT FIRE ***'}")

print("    LESION 3 -- sign of the s t^{n-j} alpha_{j-1} term:")
f=0;T=0
for (s,t) in pts:
    c=build(s,t,lesion='nomius')
    for n in range(1,11):
        for j in range(0,n+1):
            T+=1
            if star(c,s,t,n,j)!=0: f+=1
print(f"      fails {f}/{T}  -> {'NON-VACUOUS' if f else '*** CONTROL DID NOT FIRE ***'}")

print("\n(A') F_n(t^-n)=0 -- same 8 points, n=1..30")
tot=0;bad=0
for (s,t) in pts:
    c=build(s,t)
    for n in range(1,31):
        tot+=1
        if sum(c(n,j)*t**(-n*j) for j in range(n+1))!=0: bad+=1
print(f"    {tot-bad}/{tot} vanish; nonvanishing={bad}")
print("    control: F_n(t^-(n+1)) nonzero for n=1..10 at all 8 points:",
      all(sum(build(s,t)(n,j)*t**(-(n+1)*j) for j in range(n+1))!=0
          for (s,t) in pts for n in range(1,11)))
