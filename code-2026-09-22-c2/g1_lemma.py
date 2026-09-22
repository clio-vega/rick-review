import sys, io, contextlib
sys.path.insert(0,'/home/clio/projects/proofs/code-q220')
from affine import *
from itertools import combinations
def is_additive(S,T,n):
    if len(S)>=n or len(T)>=n: return False
    return length(window(compose(u_S(S,n),u_S(T,n)),n),n)==len(S)+len(T)
def subs(n):
    return [frozenset(c) for r in range(n) for c in combinations(range(n),r)]
print("Candidate lemma: (S,T) additive, i in S, i+1 in T  ==>  (S-{i}, T-{i+1}) additive")
print(f"{'n':>2} {'add.pairs':>10} {'bracketed (S,T,i)':>18} {'reduced NON-additive':>21}")
tot=bad=0
wit=[]
for n in range(3,9):
    sl=subs(n); npairs=ncase=nbad=0
    for S in sl:
        for T in sl:
            if not is_additive(S,T,n): continue
            npairs+=1
            for i in range(n):
                if i in S and (i+1)%n in T:
                    ncase+=1
                    if not is_additive(frozenset(S)-{i}, frozenset(T)-{(i+1)%n}, n):
                        nbad+=1
                        if len(wit)<5: wit.append((n,sorted(S),sorted(T),i))
    print(f"{n:>2} {npairs:>10} {ncase:>18} {nbad:>21}")
    tot+=ncase; bad+=nbad
print(f"total: {tot} bracketed instances n=3..8, {bad} non-additive reductions")
for w in wit: print("  witness",w)
