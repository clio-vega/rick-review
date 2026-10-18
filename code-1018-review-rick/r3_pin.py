import sys, sympy as sp
sys.path.insert(0,'/home/clio/projects/proofs/code-1018c2-gauge')
from q484_engine import Atilde, EX
q=sp.Rational(3,7)
# --- case A: the n=0 branch (M'=empty), N=2
w=[sp.Rational(5,3), sp.Rational(3,5)]   # w1*w2 = 1 : on H_12
x=w[0]
g=(1-q)**2/((1-q*x**2)*(1-q*x**-2))
L=sp.cancel(Atilde(2,w,[1,2],[],X='C'))
R=sp.cancel(Atilde(2,w,[],[],X='C'))
print("CASE A  N=2 M={1,2} I={}  on H_12")
print("  L            =",sp.factor(L))
print("  R (n=0 branch)=",sp.factor(R))
print("  expected R = prod_{j<=k}(1-q w_j w_k) =",sp.factor((1-q*w[0]**2)*(1-q*w[0]*w[1])*(1-q*w[1]**2)))
print("  EX(2,0,0)    =",sp.factor(EX(2,0,0,[],w,'C')))
print("  g*R          =",sp.factor(sp.cancel(g*R)))
print("  L/R          =",sp.factor(sp.cancel(L/R)), "   g =",sp.factor(g))
# --- case B: ordinary branch, N=3, M={1,2,3}, I={1}, delete {1,2}
w=[sp.Rational(5,3), sp.Rational(3,5), sp.Rational(7,11)]
x=w[0]
g=(1-q)**2/((1-q*x**2)*(1-q*x**-2))
L=sp.cancel(Atilde(3,w,[1,2,3],[1],X='C'))
R=sp.cancel(Atilde(3,w,[3],[1],X='C'))
print("\nCASE B  N=3 M={1,2,3} I={1}  delete {1,2}  on H_12")
print("  L   =",sp.factor(L)); print("  R   =",sp.factor(R))
print("  L/R =",sp.factor(sp.cancel(L/R))); print("  g   =",sp.factor(g))
print("  (L/R)/g =",sp.factor(sp.cancel(L/R/g)))
