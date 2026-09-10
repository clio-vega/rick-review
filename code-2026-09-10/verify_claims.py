"""Calibration on AGGSZ's own worked examples, then Rick's Day-183 claims.
Pure integer/Fraction power-series arithmetic -- an implementation independent
of verify_oeis.py (sympy), so agreement between the two is real corroboration."""
from fractions import Fraction as Fr
from math import comb

N = 20
def mul(f,g,n=N): return [sum(f[i]*g[k-i] for i in range(k+1)) for k in range(n)]
def inv(f,n=N):
    g=[Fr(1,1)/f[0]]+[Fr(0)]*(n-1)
    for k in range(1,n): g[k]=-sum(f[i]*g[k-i] for i in range(1,k+1))/f[0]
    return g

# ---- b_k from F(1-F)^3(3-4F) = theta(3-2F)^2 --------------------------------
F=[Fr(0)]*N
for _ in range(N+2):
    g=[3-2*F[0]]+[-2*x for x in F[1:]]
    num=mul([Fr(0),Fr(1)]+[Fr(0)]*(N-2), mul(g,g))
    omF=[1-F[0]]+[-x for x in F[1:]]
    den=mul(mul(omF,omF), mul(omF,[3-4*F[0]]+[-4*x for x in F[1:]]))
    F=mul(num, inv(den))
assert all(x.denominator==1 for x in F), "b_k not integral!"
b=[1]+[int(x) for x in F[1:]]

def inverti(h):
    a=[0]*len(h)
    for n in range(1,len(h)): a[n]=h[n]-sum(a[k]*h[n-k] for k in range(1,n))
    return a
def inv_euler(h):
    m=len(h); l=[0]*m
    for n in range(1,m): l[n]=n*h[n]-sum(l[k]*h[n-k] for k in range(1,n))
    p=[0]*m
    for n in range(1,m):
        s=l[n]-sum(d*p[d] for d in range(1,n) if n%d==0)
        assert s%n==0, "p_%d non-integral"%n
        p[n]=s//n
    return p

print("=== CALIBRATION against AGGSZ's own worked examples ===")
print("Catalan   phi_ha =", inverti([1,1,2,5,14,42,132,429])[1:], "| paper: 1,1,2,5,14,42,...")
print("Fibonacci phi_ha =", inverti([1,1,1,2,3,5,8,13,21])[1:],   "| paper: 1,0,1,0,1,0,...")
print("Lucas'    phi_ha =", inverti([1,1,1,3,4,7,11,18,29])[1:],  "| paper: 1,0,2,-1,2,-3,3,...")
print("1/(1-t)^2 a,p    =", inverti([1,2,3,4,5,6,7])[1:], inv_euler([1,2,3,4,5,6,7])[1:],
      "| paper: a=(2,-1,0..), p=(2,0,0..)")

a=inverti(b); p=inv_euler(b)
rick_b=[3,27,417,7851,164124,3661389,85384566,2056373739,50751637140,1276862920140,32626363346505,844375375808301]
rick_a=[3,18,282,5268,109647,2438928,56758176,1364824620,33643660620,845633502606,21590775239850,558411335278644]
rick_p=[3,21,344,6447,134571,2995655,69761697,1678307754,41386815905,1040573158494,26574621911472,687454232433863]
print("\n=== RICK'S THREE SEQUENCES (12 terms each) ===")
for nm,mine,his in [("b",b[1:13],rick_b),("a",a[1:13],rick_a),("p",p[1:13],rick_p)]:
    print("  %s_k matches Rick: %s" % (nm, mine==his))
    if mine!=his: print("     mine:",mine,"\n     rick:",his)

print("\n=== PBW: B(t) = prod_k (1-t^k)^{-p_k}  mod t^13 ===")
prod=[Fr(1)]+[Fr(0)]*12
for k in range(1,13):
    fac=[Fr(0)]*13; j=0
    while k*j<13: fac[k*j]=Fr(comb(p[k]+j-1,j)); j+=1
    prod=mul(prod,fac,13)
print("  residual B - prod :", [int(prod[i])-b[i] for i in range(13)])

print("\n=== DEFECT (i): Sequence 3's %C arithmetic ===")
print("  Rick (Seq 3) writes:  p_2 = 21 = a_2 + C(a_1,2)*2 = 18 + 3")
print("    a_2 + C(3,2)    = %2d + %d = %d   <- correct; equals p_2 = %d" % (a[2],comb(3,2),a[2]+comb(3,2),p[2]))
print("    a_2 + C(3,2)*2  = %2d + %d = %d   <- what the written formula evaluates to" % (a[2],comb(3,2)*2,a[2]+comb(3,2)*2))
print("  Rick (Seq 2) writes:  p_2 = 21 = 18 + C(3,2)          <- correct form")
print("  free Lie dim, degree 2 on 3 degree-1 gens = (3^2-3)/2 =", (3**2-3)//2)
print("  (free SUPER-Lie on 3 ODD gens would give C(3,2)+3 = %d, i.e. p_2 = %d -- ruled out)" % (comb(3,2)+3, a[2]+comb(3,2)+3))

print("\n=== structural cross-check of the same identity one degree up ===")
w3=(3**3-3)//3
print("  a_3 + Witt_3(3 gens) + a_1*a_2 = %d + %d + %d = %d ;  p_3 = %d  -> %s"
      % (a[3],w3,3*a[2],a[3]+w3+3*a[2],p[3], "MATCH" if a[3]+w3+3*a[2]==p[3] else "MISMATCH"))

print("\n=== modular claims (Rick states these for EVERY k) ===")
print("  b_k = 0 mod 3, k<=12 :", all(v%3==0 for v in b[1:13]))
print("  a_k = 0 mod 3, k<=12 :", all(v%3==0 for v in a[1:13]))
print("  a_k = b_k mod 9      :", all((a[k]-b[k])%9==0 for k in range(1,13)))
print("  a_k = b_k mod 27     : holds only for k in", [k for k in range(1,13) if (a[k]-b[k])%27==0])
print("  p_k mod 3            :", [p[k]%3 for k in range(1,13)])
print("  Rick's stated pattern:", [0 if k%3 else 2 for k in range(1,13)])
print("  b'_k = a'_k mod 3 (Rick's open Q3):", all(((b[k]//3)-(a[k]//3))%3==0 for k in range(1,13)))

print("\n=== EXTENDING the empirical claims past Rick's 12 terms, to k <= 19 ===")
print("  b_13..19 =", b[13:20])
print("  a_13..19 =", a[13:20])
print("  p_13..19 =", p[13:20])
print("  a_k > 0 for all k<=19        :", all(a[k]>0 for k in range(1,20)))
print("  p_k > 0 for all k<=19        :", all(p[k]>0 for k in range(1,20)))
print("  p_k mod 3, k=1..19           :", [p[k]%3 for k in range(1,20)])
print("  period-3 (0,0,2) holds k<=19 :", [p[k]%3 for k in range(1,20)]==[0 if k%3 else 2 for k in range(1,20)])
print("  a_k = b_k mod 9, k<=19       :", all((a[k]-b[k])%9==0 for k in range(1,20)))
print("  b_k,a_k = 0 mod 3, k<=19     :", all(b[k]%3==0 and a[k]%3==0 for k in range(1,20)))
