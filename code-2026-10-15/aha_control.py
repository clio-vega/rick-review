"""POSITIVE CONTROL for aha.py: lesion Rick's closed form and confirm my
end-to-end test detects it.  A green that cannot go red is not evidence."""
import sympy as sp
from itertools import combinations
exec(open('aha.py').read().split('if __name__')[0])

s, t = sp.Rational(5,7), sp.Rational(3,5)

def run_lesion(m, kmax, rmax, lesion):
    X = sp.symbols(f'X1:{m+1}')
    def sw(F,i):
        a,b=X[i-1],X[i]; return F.subs({a:b,b:a},simultaneous=True)
    def T(F,i):
        sF=sw(F,i); return sp.expand(sp.cancel(t*sF+(t-1)*X[i]*sp.cancel((sF-F)/(X[i-1]-X[i]))))
    def Tinv(F,i): return sp.expand(sp.cancel(T(F,i)/t-(1-1/t)*F))
    def Pi(F):
        sub={X[a]:X[a+1] for a in range(m-1)}; sub[X[m-1]]=s*X[0]
        return sp.expand(X[0]*F.subs(sub,simultaneous=True))
    def Y(F,i):
        G=F
        for a in range(i,m): G=Tinv(G,a)
        G=Pi(G)
        for a in range(1,i): G=T(G,a)
        return sp.expand(t**(m-i)*G)
    def eY(F,k):
        tot=sp.Integer(0)
        for comb in combinations(range(1,m+1),k):
            G=F
            for i in reversed(comb): G=Y(G,i)
            tot+=G
        return sp.expand(tot)
    def e(r):
        if r<0 or r>m: return sp.Integer(0)
        return sp.expand(sum(sp.prod([X[i] for i in c]) for c in combinations(range(m),r)))
    def qp(a,n):
        r=sp.Integer(1)
        for i in range(n): r*=(1-a*t**i)
        return r
    A={-1:sp.Integer(0)}
    def al(j):
        if j in A: return A[j]
        num=sp.Integer(1)
        for i in range(1,j+1): num*=(s-t**i)
        A[j]=sp.cancel(num/qp(t,j)); return A[j]
    def c(n,j):
        if not (0<=j<=n): return sp.Integer(0)
        return sp.cancel(qp(s,n-j)/qp(t,n-j)*(al(j)-s*t**(n-j)*al(j-1)))
    def F_(n,wv): return sp.cancel(sum(c(n,j)*wv**j for j in range(n+1)))
    b2=lambda k:k*(k-1)//2
    fails=0; tot=0
    for k in range(1,kmax+1):
        for r in range(0,rmax+1):
            lhs=sp.expand(sp.cancel(t**(-b2(k))*eY(e(r),k)))
            if lesion=='argshift':   # F_{k-b}(t^{r-b}) -> F_{k-b}(t^{r-b+1})
                rhs=sum(sp.cancel(s**b*F_(k-b,t**(r-b+1)))*e(b)*e(r+k-b) for b in range(k+1))
            elif lesion=='nosb':     # drop the s^b weight
                rhs=sum(sp.cancel(F_(k-b,t**(r-b)))*e(b)*e(r+k-b) for b in range(k+1))
            elif lesion=='prefac':   # t^{-C(k,2)} -> t^{+C(k,2)}
                lhs=sp.expand(sp.cancel(t**(b2(k))*eY(e(r),k)))
                rhs=sum(sp.cancel(s**b*F_(k-b,t**(r-b)))*e(b)*e(r+k-b) for b in range(k+1))
            tot+=1
            if sp.simplify(sp.expand(sp.cancel(lhs-sp.expand(rhs))))!=0: fails+=1
    return fails,tot

for les in ('argshift','nosb','prefac'):
    f,T=run_lesion(3,3,2,les)
    print(f"  LESION '{les}':  detected {f}/{T}  -> "
          + ("NON-VACUOUS" if f else "*** CONTROL DID NOT FIRE ***"))
