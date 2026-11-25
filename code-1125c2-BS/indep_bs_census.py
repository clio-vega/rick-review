"""REVIEW 2026-11-25 c2 -- independent re-count of the PROVE c2 census (2026-11-25c2-Q597-BS-assembly.tex, sec:ver).

Shares with PROVE's bsall.py ONLY: the census seeds (code-1114c2-Q590/common.py: census, the definition of the
census) and the engine (code-1112c2-Q585/migrate.py, Board.step / Board.journey). Everything else is written
fresh here and does not import diverge.py / zonetest.py / q597lib.py / align.py:
  * state closure: uncapped DFS over all nest-A corner moves to B and C (PROVE uses a cap-60 sampler; memory
    note: cap 60 and cap 300 gave the same 5194 states, so an uncapped closure should reproduce 5194);
  * step log: my own Board.step wrapper recording (kind, rhombus-before vertices, rhombus-after vertices,
    removed tiles, created tiles);
  * step typing (class, type): class 0 iff the rhombus's Lambda_0 edge is parallel to the journey's first
    rhombus's Lambda_0 edge; type b from the engine's kind, else a1 if the rhombus displacement has zero
    Lambda_0 part, a0 if zero Lambda_1 part;
  * divergence, common prefix p, the role L at (1, a_T), and the case split by L's re-run type at p;
  * MC: composite boards compared as tile multisets.
Additionally checked (independent of BS machinery): in case a, L's middle has length 2 and the re-run's middle is
the two steps in swapped order as translates (the Prop casea square).
usage: python3 indep_bs_census.py NW NCH
"""
import sys, copy
from collections import Counter
from fractions import Fraction as Fr
from multiprocessing import Pool
sys.path.insert(0, '/home/clio/projects/proofs/code-1114c2-Q590')
from common import census, corners, tiles_of   # census seeds + corner list + tile canonical form
import migrate
from flock import unit_dir   # engine helper: direction vector -> unit complex

_engine_step = migrate.Board.step
STEPLOG = []
def _logged_step(self, R, d):
    before = dict(self.tiles)
    R2 = _engine_step(self, R, d)
    if R2 is not None:
        removed = frozenset((before[t][0], frozenset(before[t][1])) for t in set(before) - set(self.tiles))
        created = frozenset((self.tiles[t][0], frozenset(self.tiles[t][1])) for t in set(self.tiles) - set(before))
        STEPLOG.append((self.last, tuple(before[R][1]), tuple(self.tiles[R2][1]), removed, created))
    return R2
migrate.Board.step = _logged_step

def move(board, corner, dvec):
    """pop nest-A cell `corner`, run its journey in direction dvec on a COPY; return (new board, step log)."""
    nb = copy.deepcopy(board); STEPLOG.clear()
    t = nb.nest[0]['pos'].pop(corner)
    nb.journey(t, 0, unit_dir(dvec))
    return nb, list(STEPLOG)

def state_key(b): return (frozenset(b.nest[0]['pos']), tuple(tiles_of(b)))

def closure(b0):
    A = b0.nest[0]; dirs = {'B': A['w'], 'C': A['u']}
    seen = set(); stack = [b0]
    while stack:
        b = stack.pop(); k = state_key(b)
        if k in seen: continue
        seen.add(k); yield b, dirs
        if len(seen) > 5000: raise RuntimeError('closure exploded')
        for x in corners(set(b.nest[0]['pos'])):
            for T in 'BC':
                stack.append(move(b, x, dirs[T])[0])

def lam0_edge(vs):
    """Lambda_0 edge direction (up to sign) of a rhombus with Z^4 vertices (a0,b0,a1,b1)."""
    vs = [tuple(Fr(c) for c in v) for v in vs]
    for P in vs:
        for Q in vs:
            d = tuple(q - p for p, q in zip(P, Q))
            if (d[0] or d[1]) and not (d[2] or d[3]):
                return d[:2] if d[:2] > (0, 0) else (-d[0], -d[1])
    raise ValueError('no Lambda_0 edge')

def displacement(before, after):
    lo = lambda vs: min(tuple(Fr(c) for c in v) for v in vs)
    return tuple(a - b for a, b in zip(lo(after), lo(before)))

def typed(J):
    if not J: return []
    e0 = lam0_edge(J[0][1]); out = []
    for kind, rb, ra, _, _ in J:
        cl = 0 if lam0_edge(rb) == e0 else 1
        if kind == 'b': ty = 'b'
        else:
            dv = displacement(rb, ra)
            ty = 'a1' if not (dv[0] or dv[1]) else ('a0' if not (dv[2] or dv[3]) else 'a?')
        out.append((cl, ty))
    return out

def same_step(s, t): return s[3] == t[3] and s[4] == t[4]   # same removed and created tiles

def prefix_len(A, B):
    p = 0
    while p < len(A) and p < len(B) and same_step(A[p], B[p]): p += 1
    return p

def suffix_len(A, B, p):
    q = 0
    while q < len(A) - p and q < len(B) - p and same_step(A[-1-q], B[-1-q]): q += 1
    return q

def translate_tiles(S, v):
    return frozenset((k, frozenset(tuple(Fr(c) + w for c, w in zip(P, v)) for P in vs)) for k, vs in S)

def norm_set(S): return frozenset((k, frozenset(tuple(Fr(c) for c in P) for P in vs)) for k, vs in S)

A_OF = {'B': 'a1', 'C': 'a0'}

def work(w, NCH):
    st = Counter()
    for i, (key, b0) in enumerate(census()):
        if i % NCH != w: continue
        for b, dirs in closure(b0):
            st['states'] += 1
            cs = corners(set(b.nest[0]['pos']))
            for x in cs:          # control arm: unordered B/B pairs; the instrument must see non-commutation
                for y in cs:
                    if not x < y: continue
                    bxB, _ = move(b, x, dirs['B']); byB, _ = move(b, y, dirs['B'])
                    st[('control BB pairs, boards equal', sorted(tiles_of(move(bxB, y, dirs['B'])[0])) == sorted(tiles_of(move(byB, x, dirs['B'])[0])))] += 1
            for x in cs:
                for y in cs:
                    if x == y: continue
                    bx, Jx = move(b, x, dirs['B']); by, Jy = move(b, y, dirs['C'])
                    bxy, Jy_x = move(bx, y, dirs['C']); byx, Jx_y = move(by, x, dirs['B'])
                    st['BC ordered pairs'] += 1
                    mc = sorted(tiles_of(bxy)) == sorted(tiles_of(byx))
                    st[('MC boards equal', mc)] += 1
                    roles = [('B', Jx, Jx_y), ('C', Jy, Jy_x)]
                    div = [len(A) != len(R) or prefix_len(A, R) < len(A) for _, A, R in roles]
                    if not any(div):
                        st['nondiverging'] += 1; continue
                    st['diverging'] += 1
                    st[('both diverge', all(div))] += 1
                    info = []
                    for T, A, R in roles:
                        p = prefix_len(A, R)
                        tA, tR = typed(A), typed(R)
                        info.append(dict(T=T, A=A, R=R, p=p, step_both=(p < len(A) and p < len(R)),
                                         ta=tA[p] if p < len(A) else None, tr=tR[p] if p < len(R) else None))
                    st[('both step at p', all(d['step_both'] for d in info))] += 1
                    Ls = [r for r in (0, 1) if info[r]['ta'] == (1, A_OF[info[r]['T']])]
                    st[('#L', len(Ls))] += 1
                    if len(Ls) != 1: continue
                    d = info[Ls[0]]; Tp = info[1 - Ls[0]]['T']
                    if d['tr'] == (1, 'b'): case = 'case b'
                    elif d['tr'] == (1, A_OF[Tp]): case = 'case a'
                    else: case = 'LEFTOVER %s' % (d['tr'],)
                    st[(case,)] += 1
                    st[(case, 'MC', mc)] += 1
                    if case == 'case a':
                        A, R, p = d['A'], d['R'], d['p']
                        q = suffix_len(A, R, p)
                        mA, mR = A[p:len(A)-q], R[p:len(R)-q]
                        ok = len(mA) == 2 and len(mR) == 2
                        if ok:
                            # rigid swap: mR[0] = mA[1] - alpha, mR[1] = mA[0] + gamma, alpha = disp of mA[0], gamma = disp of mA[1]
                            alpha = displacement(mA[0][1], mA[0][2]); gamma = displacement(mA[1][1], mA[1][2])
                            neg = tuple(-c for c in alpha)
                            ok = (norm_set(mR[0][3]) == translate_tiles(mA[1][3], neg)
                                  and norm_set(mR[1][3]) == translate_tiles(mA[0][3], gamma))
                        st[('case a: two-step rigid swap', ok)] += 1
    return st

def run(args):
    return work(*args)

if __name__ == '__main__':
    NW, NCH = int(sys.argv[1]), int(sys.argv[2])
    tot = Counter()
    with Pool(NW, maxtasksperchild=1) as pool:
        for st in pool.imap_unordered(run, [(w, NCH) for w in range(NCH)]): tot.update(st)
    for k in sorted(tot, key=str): print(tot[k], k)
