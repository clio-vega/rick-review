"""The r < a boundary: is the right fix the [k]_t=0 convention (Rick 2.1)
or commutativity (swap a <-> r)?"""
from hikita_star_clio import *
def qi(n):
    if n<=0: return ZERO
    s=ZERO
    for i in range(n): s=s+t**i
    return s
def level(l,a,r):
    pre=(q-ONE)/q**a
    if l==0: return ONE/q**a
    if l==1: return pre*qi(r+2-a)
    if l==2: return pre*(qi(r+4-a)/qi(2))*(qi(r+3-a)*q-t*qi(r+1-a))
    if l==3: return pre*(qi(r+6-a)/(qi(2)*qi(3)))*(qi(r+5-a)*qi(r+4-a)*q**2
             - t*qi(2)*qi(r+2-a)*qi(r+4-a)*q + t**3*qi(r+1-a)*qi(r+2-a))
for (a,b) in [(3,1),(3,2),(4,2),(4,3),(2,1)]:
    co,m = star_e(a,b)
    A, R = min(a,b), max(a,b)      # commutativity: use the SMALLER as the 'a' slot
    print("\n--- e_%d * e_%d  (m=%d) : as stated (a=%d) vs swapped (a=%d,r=%d) ---" % (a,b,m,a,A,R))
    for k in sorted(co.keys(), reverse=True):
        kk = k[1] if len(k)>1 else 0
        asis  = level(a-kk, a, b)  if 0 <= a-kk <= 3 else None
        swapd = level(A-kk, A, R)  if 0 <= A-kk <= 3 else None
        mine  = co[k]
        f = lambda x: ("--" if x is None else ("MATCH" if (mine-x)==0 else "MISMATCH"))
        print("   e_%-8s mine=%-22s  as-stated: %-9s  swapped: %s" % (str(k), str(mine), f(asis), f(swapd)))
