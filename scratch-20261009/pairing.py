"""Check the pairing identity used in the proof idea of Thm 6.6:
       <G, p_x p_y> = (-1)^n ( m_xy [e_x e_y] G + lin_e G )
   and determine WHICH inner product makes it true: standard Hall <,> or HL <,>_t.
   Fully independent: e in the p-basis via Newton's identity."""
import sympy as sp
from sympy.utilities.iterables import partitions as sym_parts
t = sp.symbols('t')

def parts_of(n):
    out=[]
    for d in sym_parts(n):
        lam=[]
        for k,v in sorted(d.items(), reverse=True): lam += [k]*v
        out.append(tuple(lam))
    return out

def zlam(lam):
    z=sp.Integer(1); from collections import Counter
    for k,m in Counter(lam).items(): z*= sp.Integer(k)**m * sp.factorial(m)
    return z

def pmul(F,G):
    out={}
    for a,ca in F.items():
        for b,cb in G.items():
            k=tuple(sorted(a+b, reverse=True)); out[k]=out.get(k,0)+ca*cb
    return {k:sp.expand(v) for k,v in out.items() if sp.expand(v)!=0}

E={0:{():sp.Integer(1)}}                      # e_n in the p-basis, Newton's identity
def e(n):
    if n in E: return E[n]
    acc={}
    for r in range(1,n+1):
        term=pmul({(r,):sp.Rational((-1)**(r-1),n)}, e(n-r))
        for k,v in term.items(): acc[k]=acc.get(k,0)+v
    E[n]={k:sp.expand(v) for k,v in acc.items() if sp.expand(v)!=0}
    return E[n]

def e_part(nu):
    F={():sp.Integer(1)}
    for p in nu: F=pmul(F,e(p))
    return F

def hall(F,G):                                 # <p_l,p_m> = delta * z_l
    return sp.expand(sum(F[k]*G.get(k,0)*zlam(k) for k in F))

def hall_t(F,G):                               # <p_l,p_m>_t = delta * z_l / prod(1-t^li)
    s=0
    for k in F:
        if k in G:
            s+= F[k]*G[k]*zlam(k)/sp.prod([(1-t**i) for i in k])
    return sp.cancel(sp.together(s))

print("n | identity in standard Hall <,> | identity in HL <,>_t")
allok_h=True; allok_t=True; nh=0; nt=0
for n in range(2,9):
    for (x,y) in [(a,n-a) for a in range(1,n//2+1)]:
        pxy={tuple(sorted((x,y),reverse=True)):sp.Integer(1)}
        m_xy = 2 if x==y else 1
        for nu in parts_of(n):
            G=e_part(nu)
            rhs_scalar = (-1)**n * ( m_xy*(1 if tuple(sorted(nu,reverse=True))==tuple(sorted((x,y),reverse=True)) else 0)
                                     + (1 if nu==(n,) else 0) )
            if sp.simplify(hall(G,pxy)-rhs_scalar)!=0: allok_h=False
            else: nh+=1
            if sp.simplify(hall_t(G,pxy)-rhs_scalar)!=0: allok_t=False
            else: nt+=1
print("  standard Hall  : identity holds in %d instances, ALL-PASS=%s" % (nh,allok_h))
print("  HL <,>_t       : identity holds in %d instances, ALL-PASS=%s" % (nt,allok_t))
print()
print("Conversion factor check:  <F,p_mu> ?= prod_i (1-t^{mu_i}) * <F,p_mu>_t")
bad=0; good=0
for n in range(2,8):
    for (x,y) in [(a,n-a) for a in range(1,n//2+1)]:
        pxy={tuple(sorted((x,y),reverse=True)):sp.Integer(1)}
        for nu in parts_of(n):
            G=e_part(nu)
            if sp.simplify(hall(G,pxy) - (1-t**x)*(1-t**y)*hall_t(G,pxy))==0: good+=1
            else: bad+=1
print("  holds in %d instances, fails in %d" % (good,bad))
