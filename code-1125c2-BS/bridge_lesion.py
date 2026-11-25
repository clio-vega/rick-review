"""Negative control for bridge_all.py: 20 bridged M0 from roles5.pkl, each with one square removed and one translated
by (1,0,0,0). Expect 'M0 == build_mosaic' False on all mutated boards, True on the unmutated copies."""
import sys, pickle
P = pickle.load(open('/home/clio/projects/proofs/code-1122c2-Q597/roles5.pkl', 'rb'))
seen, base = set(), []
for r in P:
    k = frozenset(r['M0'])
    if k not in seen: seen.add(k); base.append(set(r['M0']))
    if len(base) == 20: break
inj = []
for M in base:
    inj.append(M)
    sq = sorted((t for t in M if t[0] == 'sq'), key=str)[0]
    inj.append((M - {sq}) | {('sq', frozenset(tuple(a + b for a, b in zip(v, (1, 0, 0, 0))) for v in sq[1]))})
src = open('/home/clio/projects/proofs/code-1124c2-Q597/bridge.py').read()
line = "PAIRS = pickle.load(open('/home/clio/projects/proofs/code-1122c2-Q597/roles%d.pkl' % SIZE, 'rb'))"
src = src.replace(line, "PAIRS = [{'M0': t} for t in INJECT]"); sys.argv = ['bridge.py', '5']
exec(compile(src, 'bridge.py', 'exec'), {'__name__': 'bridge', 'INJECT': inj})
