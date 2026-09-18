"""
Clio 2026-09-18. The explicit list of the 16 Clio-only lambda in the DS
evidence scorecard, which Rick asked for in his Day 204 S2:
  "I don't have your explicit Clio-only 16 -- if you want that in the registry,
   send a list."
Regenerated from the SAME two inputs as reviews/code-2026-09-17/ds_audit.py (A):
his PDF S5 enumeration, and my own 2026-09-16 dominance run's log.
"""
rick2 = sorted({tuple(sorted((a, b), reverse=True)) for a in range(1, 5) for b in range(1, 7)}, reverse=True)
rick3 = [(2,1,1), (3,1,1), (2,2,1)]
rick4 = [(1,1,1,1), (2,1,1,1)]
rick = set(rick2 + rick3 + rick4)
mine = set()
for line in open("../code-2026-09-16/out_dominance.txt"):
    if line.strip().startswith("lam=("):
        mine.add(tuple(eval(line.split("lam=")[1].split(")")[0] + ")")))
only = sorted(mine - rick, key=lambda l: (sum(l), len(l), l))
print("Rick explicit: %d   Clio: %d   overlap: %d   union: %d" % (len(rick), len(mine), len(rick & mine), len(rick | mine)))
print("Rick-only : %s" % (sorted(rick - mine, reverse=True),))
print("Clio-only : %d" % len(only))
for lam in only:
    print("   |lam|=%d  len=%d   %s" % (sum(lam), len(lam), str(lam)))
print()
print("by size:")
for n in sorted({sum(l) for l in only}):
    print("  n=%d: %s" % (n, ", ".join(str(l) for l in only if sum(l) == n)))
