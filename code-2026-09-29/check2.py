exec(open('rick_Wr_check.py').read().split('# ---------- checks ----------')[0])
import itertools, sympy as sp

def a_(i,j,X): return sp.cancel((X[i-1]-t*X[j-1])/(X[i-1]-X[j-1]))
def Qx(a,b,X):
    m=len(X); P=sp.Integer(1)
    for i in (a,b):
        for j in range(1,m+1):
            if j not in (a,b): P*= a_(i,j,X)
    return sp.cancel(P)

def sigma_m(F,X):
    m=len(X); tot=sp.Integer(0)
    for a in range(1,m+1):
        G=F
        for k in range(1,a):  G=T(G,k,X)      # T_{a-1}...T_1, rightmost T_1 first
        tot+=G
    return sp.cancel(tot)
def sigma_prime(F,X):
    m=len(X); tot=sp.Integer(0)
    for b in range(2,m+1):
        G=F
        for k in range(2,b): G=T(G,k,X)       # T_{b-1}...T_2
        tot+=G
    return sp.cancel(tot)
def sigma2(F,X):
    m=len(X); tot=sp.Integer(0)
    for a in range(1,m+1):
        for b in range(a+1,m+1):
            G=F
            for k in range(2,b): G=T(G,k,X)   # T_{b-1}...T_2 (rightmost)
            for k in range(1,a): G=T(G,k,X)   # T_{a-1}...T_1
            tot+=G
    return sp.cancel(tot)

print("=== CHECK B: Claim 5(a) coset identity  sigma_m sigma' G = (1+t) sigma^(2) G ===")
for m in [2,3,4]:
    X=mkvars(m)
    for r in range(0, m+2):
        G=pi(pi(e(r,X),X),X)
        d=sp.simplify(sp.cancel(sigma_m(sigma_prime(G,X),X) - (1+t)*sigma2(G,X)))
        print(f"  m={m} r={r}: diff={d}"); assert d==0

print("=== CHECK C: Claim 5 kernel  sigma^(2) G = sum_{a<b} G^(a,b) Qx_ab  (EXACT, not random points) ===")
for m in [2,3,4]:
    X=mkvars(m)
    for r in range(0, m+2):
        F=e(r,X); G=pi(pi(F,X),X)
        lhs=sigma2(G,X)
        # G^(a,b) = X_a X_b * e_r(rest, s X_a, s X_b)
        rhs=sp.Integer(0)
        for a in range(1,m+1):
            for b in range(a+1,m+1):
                rest=[X[j-1] for j in range(1,m+1) if j not in (a,b)]
                args=rest+[s*X[a-1], s*X[b-1]]
                er=sp.expand(sp.symmetric_poly(r,*args)) if 0<r<=len(args) else (sp.Integer(1) if r==0 else sp.Integer(0))
                rhs+= X[a-1]*X[b-1]*er*Qx(a,b,X)
        d=sp.simplify(sp.cancel(lhs-rhs))
        print(f"  m={m} r={r}: diff={d}"); assert d==0

print("=== CHECK D: Theorem 1  t^{-1} e_2(Y) . e_r = W_r ===")
for m in [2,3,4]:
    X=mkvars(m)
    for r in range(0, m+3):
        F=e(r,X)
        if r>m: F=sp.Integer(0)
        lhs=sp.Integer(0)
        for i in range(1,m+1):
            for j in range(i+1,m+1):
                lhs+=Y(Y(F,j,X),i,X)
        lhs=sp.cancel(lhs/t)
        d=sp.simplify(sp.cancel(lhs-W(r,X)))
        print(f"  m={m} r={r}: diff={d}"); assert d==0
print("ALL PASS")
