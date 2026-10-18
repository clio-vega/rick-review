import sys, itertools, random
sys.path.insert(0, '/home/clio/projects/proofs/code-1018c2-gauge')
import sympy as sp
from q484_engine import Atilde, subsets
q = sp.Rational(3,7)
def psi(v): return (1-q*v**2)/(1-q)
def Psi(w,M): return sp.prod([psi(w[m-1]) for m in M]) if M else sp.Integer(1)
def gen_w(N,seed):
    rng=random.Random(seed)
    while True:
        w=[sp.Rational(rng.randint(2,40),rng.randint(2,40)) for _ in range(N)]
        if len(set(w))<N: continue
        if any(w[i]*w[j]==1 for i in range(N) for j in range(N)): continue
        if any(q*m==1 for m in [x**2 for x in w]+[w[i]*w[j] for i in range(N) for j in range(N)]): continue
        return w
print("=== QC failures: A~_M vs g*A~_{M-{a,b}} on H_ab ===")
for N in (2,3):
  for M in subsets(N):
    for a,b in itertools.combinations(M,2):
      for I in subsets(N):
        w=gen_w(N,23); x=w[a-1]; w[b-1]=1/x
        if len(set(w))<N: continue
        g=(1-q)**2/((1-q*x**2)*(1-q*x**-2))
        L=sp.cancel(Atilde(N,w,list(M),list(I),X='C'))
        Rr=sp.cancel(Atilde(N,w,[m for m in M if m not in (a,b)],list(I),X='C'))
        if sp.simplify(L-g*Rr)!=0:
            print(f"  N={N} M={M} (a,b)=({a},{b}) I={I}  s={len(M)} r={len(I)}  L={L}  g*R={sp.cancel(g*Rr)}")
print("=== PSI failures by root type ===")
for N in (2,3):
  for M in subsets(N):
    for I in subsets(N):
      Ah=lambda w,S: sp.cancel(Atilde(N,w,list(S),list(I),X='C')*Psi(w,S))
      for a in M:
        for eps in (sp.Integer(1),sp.Integer(-1)):
          w=gen_w(N,29); w[a-1]=eps
          if sp.simplify(Ah(w,M)-Ah(w,[m for m in M if m!=a]))!=0:
            print(f"  N={N} 2e_{a} eps={eps} M={M} I={I} s={len(M)} r={len(I)}")
      for a,b in itertools.combinations(M,2):
          w=gen_w(N,31); x=w[a-1]; w[b-1]=1/x
          if len(set(w))<N: continue
          if sp.simplify(Ah(w,M)-Ah(w,[m for m in M if m not in (a,b)]))!=0:
            print(f"  N={N} e_{a}+e_{b} M={M} I={I} s={len(M)} r={len(I)}")
      for b in M:
        for a in range(1,N+1):
          if a in M: continue
          w=gen_w(N,37); w[a-1]=w[b-1]
          if sp.simplify(Ah(w,M)-Ah(w,sorted([m for m in M if m!=b]+[a])))!=0:
            print(f"  N={N} e_{a}-e_{b} M={M} I={I} s={len(M)} r={len(I)}")
