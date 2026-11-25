"""REVIEW 2026-11-25 c2: does the census bridge (bridge.py, 520/520 distinct M0 at size 5) cover every board that
Thm bsall's (Mos) needs -- M0, M0.J_x, M0.J_y -- or only the M0 of pair records?
bridge.py iterates the distinct M0 of roles5.pkl, i.e. states with >= 2 nest-A corners. Here: the distinct tilings
of ALL states in the uncapped closure, and of the states with >= 2 corners. If the counts agree, every one-move
image is (as a tiling) among the bridge-checked boards, because the closure is closed under moves.
usage: python3 mos_coverage.py NW NCH"""
import sys
from collections import Counter
from multiprocessing import Pool
sys.path.insert(0, '/home/clio/projects/reviews/code-1125c2-BS')
from indep_bs_census import census, closure, corners, tiles_of

def work(args):
    w, NCH = args
    allT, twoT = set(), set(); n = Counter()
    for i, (key, b0) in enumerate(census()):
        if i % NCH != w: continue
        for b, _ in closure(b0):
            t = tuple(sorted(tiles_of(b))); allT.add(t); n['states'] += 1
            if len(corners(set(b.nest[0]['pos']))) >= 2: twoT.add(t); n['states with >=2 corners'] += 1
    return allT, twoT, n

if __name__ == '__main__':
    NW, NCH = int(sys.argv[1]), int(sys.argv[2])
    A, Two, N = set(), set(), Counter()
    with Pool(NW, maxtasksperchild=1) as pool:
        for a, t, n in pool.imap_unordered(work, [(w, NCH) for w in range(NCH)]): A |= a; Two |= t; N.update(n)
    print(dict(N)); print('distinct tilings, all states:', len(A)); print('distinct tilings, >=2-corner states:', len(Two))
    print('tilings only in 1-corner states:', len(A - Two))
