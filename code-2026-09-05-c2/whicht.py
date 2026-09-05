import sys, itertools, sympy as sp
sys.path.insert(0,'/home/clio/projects/probes/2026-09-04-Q81')
sys.path.insert(0,'/home/clio/projects/probes/2026-09-04-Q76')
sys.path.insert(0,'/home/clio/projects/probes/2026-09-03-Q75')
from nested import C, t
from abacus import beta, parts_of
hits=[]
for n in range(0,6):
    for lam in parts_of(n):
        for es in itertools.permutations(range(2,7),3):
            if len(set(es))<3: continue
            if es.index(max(es))!=0: continue
            ents=C(list(es),lam,n+sum(es)+6)
            if not ents: continue
            g=sp.factor(sp.gcd_list(list(ents.values())))
            if sp.degree(sp.Poly(g,t))>1: hits.append((lam,es,str(g)))
print('extra-t cases:',len(hits))
for h in hits[:40]: print('  lam=%-12s es=%s  gcd=%s'%(str(h[0]),h[1],h[2]))
