"""k3_perm.py -- Rick's Q1 (Day 169 audit): does the gcd claim survive ALL SIX
orderings of each unordered triple, in particular max{e_i}=e_1?
Reports gcd of entries per (lambda, ORDERED triple), split by which slot m carries
the maximum size.  Q83 cor:q83 predicts (1+t)-valuation exactly 1 in every slot."""
import sys, itertools, sympy as sp
sys.path.insert(0, '.'); sys.path.insert(0, '/home/clio/projects/probes/2026-09-04-Q76')
sys.path.insert(0, '/home/clio/projects/probes/2026-09-03-Q75')
from nested import C, t
from abacus import beta, parts_of

def run(NMAX, EM):
    gcds = {}       # (maxslot, gcd-string) -> count
    hookent = {}    # (maxslot, value-string) -> count   [the thm:wit witness entry]
    for n in range(0, NMAX + 1):
        for lam in parts_of(n):
            for es in itertools.permutations(range(2, EM + 1), 3):
                if len(set(es)) < 3: continue
                maxslot = es.index(max(es)) + 1
                L = n + sum(es) + 6
                ents = C(list(es), lam, L)
                if not ents: continue
                vals = list(ents.values())
                g = sp.factor(sp.gcd_list(vals))
                gcds[(maxslot, str(g))] = gcds.get((maxslot, str(g)), 0) + 1
        print(f'|lam|<={n} done', flush=True)
    # separately: the thm:wit hook witness <mu | C_3 | empty>, mu = (E-j, 1^j), j = f_2
    for es in itertools.permutations(range(2, EM + 1), 3):
        if len(set(es)) < 3: continue
        maxslot = es.index(max(es)) + 1
        f = sorted(es); j = f[1]; E = sum(es)
        mu = tuple([E - j] + [1] * j) if E - j >= 1 else None
        L = E + j + 6
        ents = C(list(es), (), L)          # from empty
        val = ents.get(mu, 0)
        hookent[(maxslot, str(sp.factor(val)))] = hookent.get((maxslot, str(sp.factor(val))), 0) + 1
    print('\n=== gcd of entries, by slot carrying the max ===')
    for k in sorted(gcds): print('  maxslot=%d  gcd=%-24s count=%d' % (k[0], k[1], gcds[k]))
    print('\n=== thm:wit hook witness <(E-j,1^j)|C_3|empty>, j=f_2, by max slot ===')
    for k in sorted(hookent): print('  maxslot=%d  entry=%-24s count=%d' % (k[0], k[1], hookent[k]))

if __name__ == '__main__':
    run(int(sys.argv[1]), int(sys.argv[2]))
