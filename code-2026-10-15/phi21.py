"""His 'Open' remark:  F_n(w) = (1-t^n w) (s;t)_n/(t;t)_n * 2phi1(t^{1-n}, t/s; t^{1-n}/s; t; w),
   flagged in the note as 'only computed (n<=6), and it is not needed for the theorem'.
   Verify it further, and confirm the LINEAR FACTOR is the m=0 case of Theorem 1."""
from fractions import Fraction as Fr

def check(s,t,NMAX):
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
        return qp(s,n-j)/qp(t,n-j)*(al(j)-s*t**(n-j)*al(j-1))
    def Fcoef(n):                    # coefficient list of F_n(w)
        return [c(n,j) for j in range(n+1)]
    def phi21_coef(n):               # coefficient list of (1-t^n w)*pref*2phi1(...)
        a, b_, cc = t**(1-n), t/s, t**(1-n)/s
        pref = qp(s,n)/qp(t,n)
        ser=[]                       # 2phi1 coefficients, terminates at k=n-1
        for k in range(0,n):
            num = qp(a,k)*qp(b_,k); den = qp(cc,k)*qp(t,k)
            ser.append(pref*num/den)
        out=[Fr(0)]*(n+1)            # multiply by (1 - t^n w)
        for k,v in enumerate(ser):
            out[k]+=v
            out[k+1]-=t**n*v
        return out
    bad=[]
    for n in range(1,NMAX+1):
        if Fcoef(n)!=phi21_coef(n): bad.append(n)
    return bad

pts=[(Fr(2),Fr(3)),(Fr(5,7),Fr(3,5)),(Fr(-3),Fr(5)),(Fr(1,3),Fr(-1,2)),
     (Fr(11,4),Fr(7,9)),(Fr(-2,5),Fr(13,3))]
print("2phi1 form of F_n -- coefficient-by-coefficient, n = 1..14, 6 exact points")
allok=True
for (s,t) in pts:
    bad=check(s,t,14)
    allok &= not bad
    print(f"   (s,t)=({s},{t}):  {'all n=1..14 agree' if not bad else 'FAIL at n='+str(bad)}")
print("VERDICT: 2phi1 form confirmed to n=14 at all 6 points:", allok)
