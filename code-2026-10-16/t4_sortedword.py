import sympy as sp
from itertools import product as iproduct
from collections import defaultdict
q = sp.symbols('q')

def qint_fact(n, zexp):
    z = q**zexp
    r = sp.Integer(1)
    for m in range(1, n+1):
        r *= sum(z**k for k in range(m))
    return sp.cancel(r)

class Dat:
    def __init__(self, form): self.form=form; self.n=len(form)
    def f(self,i,j): return self.form[i][j]
    def deg(self,w):
        d=[0]*self.n
        for a in w: d[a]+=1
        return tuple(d)
    def pair_lv(self,i,d):  # (alpha_i, d)
        return sum(self.form[i][j]*d[j] for j in range(self.n))

def shuffle(D,u,v):
    """quantum shuffle: crossing weight q^{(v-letter, u-letter)} when v-letter precedes u-letter"""
    out=defaultdict(lambda: sp.Integer(0))
    def rec(a,b,w,wt):
        if a==len(u): out[tuple(w)+tuple(v[b:])]+=wt; return
        if b==len(v): out[tuple(w)+tuple(u[a:])]+=wt; return
        rec(a+1,b,w+[u[a]],wt)
        e=D.pair_lv(v[b], D.deg(u[a:]))
        rec(a,b+1,w+[v[b]],wt*q**e)
    rec(0,0,[],sp.Integer(1))
    return dict(out)

def lam(D,order,w):
    """sorted-word character: nonzero only on o-weakly-increasing words"""
    rank={v:k for k,v in enumerate(order)}
    key=[rank[a] for a in w]
    if any(key[i]>key[i+1] for i in range(len(key)-1)): return sp.Integer(0)
    d=D.deg(w)
    r=sp.Integer(1)
    for i in range(D.n):
        if d[i]: r/= qint_fact(d[i], D.f(i,i))
    return sp.cancel(r)

def phi_o(D,order,a,b):
    """phi_o(alpha_k,alpha_l) = (alpha_k,alpha_l) if k AFTER l in o, else 0; diagonal 0"""
    rank={v:k for k,v in enumerate(order)}
    return sum(a[k]*b[l]*D.f(k,l) for k in range(D.n) for l in range(D.n) if rank[k]>rank[l])

def test(D,order,phi_order,words):
    ok=bad=0
    for u in words:
        for v in words:
            lhs=sum(c*lam(D,order,w) for w,c in shuffle(D,u,v).items())
            e=phi_o(D,phi_order,D.deg(u),D.deg(v))
            rhs=q**e*lam(D,order,u)*lam(D,order,v)
            if sp.simplify(sp.cancel(lhs-rhs))==0: ok+=1
            else: bad+=1
    return ok,bad

A3=[[2,-1,0],[-1,2,-1],[0,-1,2]]
D=Dat(A3)
words=[()]
for L in range(1,4):
    words+= [w for w in iproduct(range(3),repeat=L)]
print("Lemma 2 (sorted-word character) on Sh_q(V), A3, SYMBOLIC in q.")
print("DOMAIN:",len(words),"words of length <= 3 =>",len(words)**2,"pairs")
print()
for order in [(0,1,2),(2,1,0),(1,0,2),(0,2,1)]:
    ok,bad=test(D,order,order,words)
    print(f"  order o={order}:  lam_o(X sh Y) = q^phi_o lam_o(X) lam_o(Y):  {ok}/{ok+bad} pass, {bad} FAIL")
print()
print("POSITIVE CONTROL: lam_o paired with the phi of a DIFFERENT order")
for order,other in [((0,1,2),(2,1,0)),((0,1,2),(1,0,2)),((0,1,2),(0,2,1))]:
    ok,bad=test(D,order,other,words)
    print(f"  lam_{order} with phi_{other}:  {ok}/{ok+bad} pass, {bad} FAIL  (expect many FAIL)")
