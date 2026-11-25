"""REVIEW 2026-11-25 c2: are the one-move images M0.J_x (to B), M0.J_y (to C) of pair states among the 520
bridge-checked tilings (the tilings of >=2-corner states)?  usage: python3 mos_images.py NW NCH"""
import sys
from collections import Counter
from multiprocessing import Pool
sys.path.insert(0, '/home/clio/projects/reviews/code-1125c2-BS')
from indep_bs_census import census, closure, corners, tiles_of, move
def work(args):
    w, NCH = args
    two, imgs = set(), set()
    for i, (key, b0) in enumerate(census()):
        if i % NCH != w: continue
        for b, dirs in closure(b0):
            cs = corners(set(b.nest[0]['pos']))
            if len(cs) < 2: continue
            two.add(tuple(sorted(tiles_of(b))))
            for x in cs:
                for T in 'BC':
                    imgs.add((T, tuple(sorted(tiles_of(move(b, x, dirs[T])[0])))))
    return two, imgs
if __name__ == '__main__':
    NW, NCH = int(sys.argv[1]), int(sys.argv[2]); two, imgs = set(), set()
    with Pool(NW, maxtasksperchild=1) as pool:
        for t, i in pool.imap_unordered(work, [(w, NCH) for w in range(NCH)]): two |= t; imgs |= i
    out = Counter((T, t in two) for T, t in imgs)
    print('bridged (>=2-corner) tilings:', len(two)); print('distinct one-move images:', len({t for _, t in imgs}))
    for k in sorted(out): print(out[k], 'images to', k[0], 'inside bridged set' if k[1] else 'OUTSIDE bridged set')
