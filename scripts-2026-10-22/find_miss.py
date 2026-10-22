import itertools, random, sympy as sp
from fractions import Fraction as Fr
random.seed(99)
exec(open('residue_lemma.py').read().split('print("== Lemma')[0].split('# ---- Lemma')[0])
z = sp.Symbol('z')
def residue_form(s,t,S,w):
    ws={k:sp.Rational(w[k].numerator,w[k].denominator) for k in w}
    Qs=sp.prod([(z-ws[k]) for k in range(1,s)]) if s>1 else sp.Integer(1)
    P=sp.prod([(ws[m]*z-1) for m in S]); D=sp.prod([(z-ws[m]) for m in S])
    R=z**(t-s)*Qs*P/D
    r0=sp.residue(sp.simplify(R),z,0)
    u=sp.Symbol('u')
    rinf=-sp.residue(sp.simplify(R.subs(z,1/u)/u**2),u,0)
    return sp.nsimplify(-r0-rinf)
for S in [(2,3,4),(1,2,3,4),(2,4,5),(1,3,4,5),(3,4,5)]:
    for s in [1,2,3]:
        for t in [-2,-1,0,1,2]:
            w=pt(max(S)+1)
            v=eS(S,w)*Psi((s,),(t,),S,w)
            lhs=sp.Rational(v.numerator,v.denominator)
            rhs=residue_form(s,t,S,w)
            if sp.simplify(lhs-rhs)!=0:
                print(f"  MISS: S={S} s={s} t={t}   lhs={lhs}   rhs={rhs}   ratio={sp.nsimplify(lhs/rhs) if rhs!=0 else 'rhs=0'}")
print("done")
