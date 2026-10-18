"""
Independent re-implementation of Motegi's dominance order on subsets, used to
check three of Rick's purely combinatorial numbers first-hand (2026-10-17 c2 review):

  (1) the nonvanH coverage list  100 / 91.7 / 81.9 / 72.8 / 64.8 / 58.0 / 52.3 %  (N=2..8)
  (2) his corrected count of predicted pole pairs for the twelve N=5 (c)-failures (22, was 26)
  (3) the stratum classification of those failures (all twelve out of stratum on the mu witness)

Order (Rick, UID 819 Setup, quoting Motegi):
   M >= I  iff  |M| >= |I|  and the top |I| elements of M dominate I entrywise.
"""
from itertools import combinations

def geq(M, I):
    """Motegi's order: M >= I."""
    M = sorted(M); I = sorted(I)
    if len(M) < len(I):
        return False
    r = len(I)
    top = M[len(M) - r:] if r else []
    return all(top[j] >= I[j] for j in range(r))

def subsets(N):
    out = []
    for k in range(N + 1):
        out.extend(combinations(range(1, N + 1), k))
    return out

def mx(S):
    return max(S) if S else 0          # Rick: "with max(empty) = 0"

# ---------- (1) coverage of the stratum max I <= b on the nonvanH domain ----------
print("Coverage of stratum  max I <= b  on  {(M,I,a<b) : M >= I, {a,b} cap M = empty}")
print(f"{'N':>2} {'in stratum':>11} {'domain':>9} {'pct':>7}")
cov = {}
for N in range(2, 9):
    Ss = subsets(N)
    tot = ins = 0
    for M in Ss:
        Mset = set(M)
        for I in Ss:
            if not geq(M, I):
                continue
            for a, b in combinations(range(1, N + 1), 2):
                if a in Mset or b in Mset:
                    continue
                tot += 1
                if mx(I) <= b:
                    ins += 1
    cov[N] = 100.0 * ins / tot
    print(f"{N:>2} {ins:>11} {tot:>9} {cov[N]:>6.1f}%")
claim = {2: 100.0, 3: 91.7, 4: 81.9, 5: 72.8, 6: 64.8, 7: 58.0, 8: 52.3}
print("\nclaimed (Rick's coverage_check.py == my reply's list):", claim)
print("match to 0.1pp:", all(abs(cov[N] - claim[N]) < 0.05 for N in claim))
