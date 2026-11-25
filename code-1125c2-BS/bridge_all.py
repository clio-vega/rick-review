"""REVIEW 2026-11-25 c2: run PROVE's bridge.py check (code-1124c2-Q597, unchanged logic) on EVERY distinct tiling
of the uncapped size-5 closure (1979), not only the 520 M0 of pair records.  bridge.py's source is exec'd with its
pickle input replaced by the closure's tilings; nothing else in it is edited.  usage: python3 bridge_all.py NW NCH"""
import sys
from multiprocessing import Pool
sys.path.insert(0, '/home/clio/projects/reviews/code-1125c2-BS')
from indep_bs_census import census, closure, tiles_of
from fractions import Fraction as Fr
def norm(v): return tuple(int(c) if Fr(c).denominator == 1 else Fr(c) for c in v)
def work(args):
    w, NCH = args; out = set()
    for i, (key, b0) in enumerate(census()):
        if i % NCH != w: continue
        for b, _ in closure(b0):
            out.add(frozenset((k, frozenset(norm(v) for v in vs)) for k, vs in b.tiles.values()))
    return out
if __name__ == '__main__':
    NW, NCH = int(sys.argv[1]), int(sys.argv[2]); T = set()
    with Pool(NW, maxtasksperchild=1) as pool:
        for o in pool.imap_unordered(work, [(w, NCH) for w in range(NCH)]): T |= o
    src = open('/home/clio/projects/proofs/code-1124c2-Q597/bridge.py').read()
    line = "PAIRS = pickle.load(open('/home/clio/projects/proofs/code-1122c2-Q597/roles%d.pkl' % SIZE, 'rb'))"
    assert src.count(line) == 1
    src = src.replace(line, "PAIRS = [{'M0': set(t)} for t in INJECT]")
    sys.argv = ['bridge.py', '5']
    exec(compile(src, 'bridge.py', 'exec'), {'__name__': 'bridge', 'INJECT': sorted(T, key=lambda t: sorted(map(str, t)))})
