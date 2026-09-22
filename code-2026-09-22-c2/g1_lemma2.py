import sys
sys.path.insert(0,'/home/clio/projects/proofs/code-q220')
from affine import *
from itertools import combinations
def is_additive(S,T,n):
    if len(S)>=n or len(T)>=n: return False
    return length(window(compose(u_S(S,n),u_S(T,n)),n),n)==len(S)+len(T)
def subs(n): return [frozenset(c) for r in range(n) for c in combinations(range(n),r)]
def subsets_of(S): return [frozenset(c) for r in range(len(S)+1) for c in combinations(sorted(S),r)]
print("Stronger candidate: (S,T) additive, S' subset S, T' subset T  ==>  (S',T') additive")
tot=bad=0; wit=[]
for n in range(3,8):
    sl=subs(n); ncase=nbad=0
    for S in sl:
        for T in sl:
            if not is_additive(S,T,n): continue
            for Sp in subsets_of(S):
                for Tp in subsets_of(T):
                    ncase+=1
                    if not is_additive(Sp,Tp,n):
                        nbad+=1
                        if len(wit)<5: wit.append((n,sorted(S),sorted(T),sorted(Sp),sorted(Tp)))
    print(f" n={n}: {ncase} (S,T,S',T') instances, {nbad} non-additive")
    tot+=ncase; bad+=nbad
print(f"total {tot} instances n=3..7, {bad} failures")
for w in wit: print("  witness (n,S,T,S',T'):",w)
