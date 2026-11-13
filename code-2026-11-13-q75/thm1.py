"""Theorem 1 of Rick Q75 against the direct shuffle-pairing rank."""
import sys, time
from itertools import product
from qsym import r_vector

def formula(L):
    if L % 2 == 1:
        d = L + 1
        return [min(i // 2, (d - i) // 2) + 1 for i in range(d + 1)]
    d = L + 1
    return [1 if i in (0, d) else min(-(-i // 2), -(-(d - i) // 2)) for i in range(d + 1)]

def alternating(L):
    a = ''.join('01'[(p) % 2] for p in range(L))
    b = ''.join('10'[(p) % 2] for p in range(L))
    return [a, b]

if __name__ == "__main__":
    Lmax = int(sys.argv[1]); Lctl = int(sys.argv[2])
    t0 = time.time()
    for L in range(1, Lmax + 1):
        for s in alternating(L):
            r = r_vector(s)
            print(L, s, r, 'OK' if r == formula(L) else 'FAIL vs %s' % formula(L), flush=True)
    print('alt sweep %.1fs' % (time.time() - t0))
    # separating control: every non-alternating s at L<=Lctl
    for L in range(2, Lctl + 1):
        alts = set(alternating(L)); match = []; tot = 0
        for bits in product('01', repeat=L):
            s = ''.join(bits)
            if s in alts: continue
            tot += 1
            if r_vector(s) == formula(L): match.append(s)
        print('control L=%d: %d/%d non-alternating s match the closed form %s' % (L, len(match), tot, match[:6]))
