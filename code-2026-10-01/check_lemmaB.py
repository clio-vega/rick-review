import itertools, sympy as sp
from sympy import symbols, simplify, cancel, binomial
t = symbols('t')

def qbin(N,r,q):
    num=sp.Integer(1)
    for i in range(r): num*= (1-q**(N-i))
    den=sp.Integer(1)
    for i in range(r): den*= (1-q**(i+1))
    return sp.simplify(sp.cancel(num/den))

print("=== (b) level-set kernel sum, t=0 form: sum_B prod_{i in B, j notin B} x_i/(x_i-x_j) ===")
for N in range(1,7):
    X=symbols('x1:%d'%(N+1))
    for r in range(0,N+1):
        tot=0
        for B in itertools.combinations(range(N), r):
            Bs=set(B); term=sp.Integer(1)
            for i in B:
                for j in range(N):
                    if j in Bs: continue
                    term*= X[i]/(X[i]-X[j])
            tot+=term
        val=sp.simplify(sp.cancel(sp.together(tot)))
        ok = (val==1)
        print('  N=%d r=%d  sum=%s %s'%(N,r,val,'' if ok else '  <<< NOT 1'))

print()
print("=== t-version: sum_B prod (x_i - t x_j)/(x_i - x_j)  vs  [N choose r]_t ===")
for N in range(1,6):
    X=symbols('x1:%d'%(N+1))
    for r in range(0,N+1):
        tot=0
        for B in itertools.combinations(range(N), r):
            Bs=set(B); term=sp.Integer(1)
            for i in B:
                for j in range(N):
                    if j in Bs: continue
                    term*= (X[i]-t*X[j])/(X[i]-X[j])
            tot+=term
        val=sp.simplify(sp.cancel(sp.together(tot)))
        want=sp.expand(qbin(N,r,t))
        ok = sp.simplify(val-want)==0
        print('  N=%d r=%d  sum=%-28s [N,r]_t=%-28s %s'%(N,r,sp.factor(val),sp.factor(want),'OK' if ok else '<<< MISMATCH'))
