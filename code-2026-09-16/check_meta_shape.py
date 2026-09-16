"""Check Rick's level-l meta-shape formulas (registry node
hikita-star-P_l-meta-shape-conjecture, trust=computed) against MY data."""
from hikita_star_clio import *
def qi(n):
    if n <= 0: return ZERO
    s = ZERO
    for i in range(n): s = s + t**i
    return s

def rick_level(l, a, r):
    """c_{a-l}^{(a)}(r), Rick's meta-shape, day193 writeup section 4.1."""
    pre = (q - ONE)/q**a
    if l == 0: return ONE/q**a
    if l == 1: return pre * qi(r+2-a)
    if l == 2: return pre * (qi(r+4-a)/qi(2)) * (qi(r+3-a)*q - t*qi(r+1-a))
    if l == 3: return pre * (qi(r+6-a)/(qi(2)*qi(3))) * (
        qi(r+5-a)*qi(r+4-a)*q**2 - t*qi(2)*qi(r+2-a)*qi(r+4-a)*q + t**3*qi(r+1-a)*qi(r+2-a))
    return None

import sys
cases = [(2,2),(2,3),(2,4),(3,3),(3,4),(4,4)]
for (a,b) in cases:
    co, m = star_e(a,b)
    print("\n--- e_%d * e_%d (m=%d) ---" % (a,b,m))
    for l in range(0, a+1):
        k = a - l
        lam = tuple(sorted((a+b-k,k),reverse=True)) if k>0 else (a+b,)
        if a+b-k < k: continue
        mine = co.get(lam, ZERO)
        his = rick_level(l, a, b)
        if his is None:
            print("   l=%d (e_%s): Rick has NO formula (top level); mine = %s" % (l, lam, mine)); continue
        print("   l=%d (e_%s): %s" % (l, lam, "MATCH" if (mine-his)==0 else "*** MISMATCH ***"))
        if (mine-his)!=0:
            print("       mine:", mine); print("       rick:", his)
