"""app:cherednik -- thm:tri eigenvalue + the printed m=3, lambda=(2,0,1) example."""
import itertools, engine as E
from sympy import simplify, expand, cancel, Poly, Integer, factor
s,t = E.s, E.t

def rk(lam, i):   # i is 0-indexed here
    return sum(1 for j in range(len(lam)) if lam[j] > lam[i]) + \
           sum(1 for j in range(i) if lam[j] == lam[i])

def sortd(e): return tuple(sorted(e, reverse=True))

print("=== thm:tri : coeff of x^lambda in Y^o_i x^lambda  ==  s^{lam_i} t^{rk_i(lam)} ===")
tot_ok=tot_bad=0; bij_ok=bij_bad=0
for m in [2,3,4]:
    for d in range(0,4):
        for lam in itertools.product(range(d+1), repeat=m):
            if sum(lam)!=d: continue
            X=E.xs(m)
            mon=Integer(1)
            for v,k in zip(X,lam): mon*=v**k
            for i in range(m):
                res = E.Yop(mon,X,i+1,twisted=False)
                P = Poly(expand(cancel(res)), *X)
                got = P.coeff_monomial(tuple(lam))
                want = s**lam[i]*t**rk(lam,i)
                if simplify(got-want)==0: tot_ok+=1
                else:
                    tot_bad+=1
                    if tot_bad<4: print("  FAIL",m,lam,i,got,want)
            # rk_i is a bijection [m] -> {0..m-1}
            if sorted(rk(lam,i) for i in range(m))==list(range(m)): bij_ok+=1
            else: bij_bad+=1
print(f"thm:tri diagonal eigenvalue: {tot_ok} of {tot_ok+tot_bad} pass, {tot_bad} fail")
print(f"rk_i bijection claim (thm:C3): {bij_ok} of {bij_ok+bij_bad} pass, {bij_bad} fail")

print()
print("=== printed example: m=3, lambda=(2,0,1), Y^o_1 = t^2 pi_o T_2^{-1} T_1^{-1} ===")
m=3; X=E.xs(m); lam=(2,0,1)
mon = X[0]**2*X[2]
res = expand(cancel(E.Yop(mon,X,1,twisted=False)))
# cross-check the printed word form directly
alt = cancel(t**2*E.pi_circ(E.Tinv(E.Tinv(mon,X,1),X,2),X))
print("  word form t^2 pi_o T_2^{-1} T_1^{-1} agrees with Y^o_1 definition:",
      simplify(cancel(res-alt))==0)
P=Poly(res,*X)
terms={mon_:P.coeff_monomial(mon_) for mon_ in [(2,0,1),(1,0,2),(0,2,1),(1,1,1)]}
print("  full expansion of Y^o_1 x^(2,0,1):")
for k,v in sorted(Poly(res,*X).terms()):
    print("     x^%s : %s" % (str(k), factor(v)))
printed = {(2,0,1): s**2, (1,0,2): -s*(t-1), (0,2,1): -t*(t-1), (1,1,1): -s*(t-1)}
allok=True
for k,v in printed.items():
    d=simplify(terms[k]-v)
    print(f"     printed x^{k}: {v}   residual {d}")
    if d!=0: allok=False
# is the expansion EXACTLY these four terms (no extras)?
nterms=len(Poly(res,*X).terms())
print(f"  printed terms match: {allok};  number of monomials in result: {nterms} (printed names 4)")
# dominance claim: partial sums (1,1,3) and (0,2,3) both <= (2,2,3)
def psums(e): 
    out=[];a=0
    for v in e: a+=v; out.append(a)
    return tuple(out)
print("  partial sums: x^(2,0,1)->%s  x^(1,0,2)->%s  x^(0,2,1)->%s  (printed 2,2,3 / 1,1,3 / 0,2,3)"
      % (psums((2,0,1)),psums((1,0,2)),psums((0,2,1))))
print("  sort((1,1,1))=%s strictly below sort((2,0,1))=%s : %s"
      % (sortd((1,1,1)), sortd((2,0,1)), E.dominates(sortd((2,0,1)), sortd((1,1,1)))))
