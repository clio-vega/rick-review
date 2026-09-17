"""Clio 2026-09-17: Rick's Prop 1, c_bot(a,r) = q^{-min(a,r)}, on a grid."""
import sys
from hikita_star_clio import *
allok=True
for a in range(1,5):
    for r in range(1,7):
        if a+r>7: continue
        co,m = star_e(a,r)
        bot = tuple(sorted((a,r),reverse=True))
        got, want = co.get(bot,ZERO), (ONE/q)**min(a,r)
        ok = (got-want)==ZERO; allok = allok and ok
        print("  a=%d r=%d  e_%-8s %s" % (a,r,str(bot),"q^-%d OK"%min(a,r) if ok else "MISMATCH got "+str(got)))
        sys.stdout.flush()
print("Prop 1 on this grid:", "CONFIRMED" if allok else "FAILED")
