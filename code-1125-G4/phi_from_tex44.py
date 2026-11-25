"""Independent route for the G4 fidelity check (REVIEW 2026-11-25).
Phi and Sigma o rr written from the tex (proofs/2026-11-13c2-Q585-G4-evacuation.tex, Def phi l.98-106,
Def rr/std/Sigma l.121-129) in the tex's OWN coordinates: cells (c, r), French (r = 0 is the bottom row),
rot(c, r) = (C-1-c, R-1-r).  No code is imported from g4.py, mosaic.py or the Lean repo.  A^vee is built
as rot(box minus A) (a set), not by the row-length formula Lean's `compl` uses.  rr uses ell = max f + 2
(Lean uses max f), so agreement also tests shift-invariance of Sigma.
Instances (R, C, A, B, f) are parsed from TworowD4Kernel/PhiOutData.lean (phiData33); only the inputs are
read from it, plus the Python-engine column for a third comparison.
usage: python3 -I phi_from_tex.py PhiOutData.lean lean_dump.txt"""
import re, sys
from collections import Counter

def parse_data(path):
    txt = open(path).read()
    block = txt[txt.index('def phiData44_0'):txt.index('def phiData44 :')]
    rows = re.findall(r'^\s*\((\d+), (\d+), \[([\d, ]*)\], \[([\d, ]*)\], \[(.*?)\], \[(.*?)\]\)[,\]]?\s*$', block, re.M)
    cellv = lambda s: {(int(r), int(c)): int(v) for r, c, v in re.findall(r'\(\((\d+), (\d+)\), (\d+)\)', s)}
    ints = lambda s: [int(x) for x in s.split(',') if x.strip()]
    out = []
    for R, C, A, B, f, ex in rows:
        # Lean (r, c) -> tex (c, r)
        tc = lambda d: {(c, r): v for (r, c), v in d.items()}
        out.append((int(R), int(C), ints(A), ints(B), tc(cellv(f)), tc(cellv(ex))))
    return out

def rot(R, C, X): return (C - 1 - X[0], R - 1 - X[1])
def rowlen(P, r): return P[r] if r < len(P) else 0

def phi(R, C, A, B, f, tie='south'):
    cells = [(c, r) for r in range(R) for c in range(C) if rowlen(B, r) <= c < rowlen(A, r)]
    assert set(cells) == set(f)
    # reverse standard order: standard is (f, then west first); reverse = decreasing (f, c)
    rev = sorted(cells, key=lambda X: (f[X], X[0]), reverse=True)
    holes = [rot(R, C, X) for X in rev]                  # ftilde^{-1}(1), ftilde^{-1}(2), ...
    Avee = {rot(R, C, (c, r)) for r in range(R) for c in range(C) if c >= rowlen(A, r)}
    g = {X: X[1] + 1 for X in Avee}                      # u_{A^vee}: row r filled with r+1
    for h in holes:
        assert h not in g
        while True:
            W, S = (h[0] - 1, h[1]), (h[0], h[1] - 1)
            cand = [Y for Y in (W, S) if Y in g]
            if not cand: break
            if len(cand) == 2:
                if g[W] > g[S]: y = W
                elif g[S] > g[W]: y = S
                else: y = S if tie == 'south' else W
            else: y = cand[0]
            g[h] = g.pop(y); h = y
    return g

def sigma_rr(R, C, A, B, f, order='U'):
    ell = max(f.values()) + 2
    X = {rot(R, C, Y): ell + 1 - v for Y, v in f.items()}   # rr f on rot(A/B)
    kappa = {rot(R, C, (c, r)) for r in range(R) for c in range(C) if c >= rowlen(A, r)}
    if order == 'U':   # decreasing U_kappa: top row first, right to left
        proc = sorted(kappa, key=lambda Y: (-Y[1], -Y[0]))
    else:              # lesion: by columns, right column first, top to bottom
        proc = sorted(kappa, key=lambda Y: (-Y[0], -Y[1]))
    out = {}
    for h in proc:
        assert h not in X
        r_k = h[1]
        while True:
            E, N = (h[0] + 1, h[1]), (h[0], h[1] + 1)
            cand = [Y for Y in (E, N) if Y in X]
            if not cand: break
            if len(cand) == 2: y = N if X[N] <= X[E] else E    # smaller; tie -> north
            else: y = cand[0]
            X[h] = X.pop(y); h = y
        out[h] = r_k + 1                                     # vacated z_k labelled r_k + 1
    return out

def parse_dump(path):
    res = {}
    for line in open(path):
        if '|PHI|' not in line: continue
        i, _, p, _, s = line.rstrip('\n').split('|')
        m = lambda t: {(int(c), int(r)): int(v) for r, c, v in re.findall(r'(\d+),(\d+):(\d+)', t)}  # Lean (r,c) -> (c,r)
        res[int(i)] = (m(p), m(s))
    return res

if __name__ == '__main__':
    data = parse_data(sys.argv[1]); dump = parse_dump(sys.argv[2])
    assert len(data) == 3556 == len(dump), (len(data), len(dump))
    st = Counter()
    for i, (R, C, A, B, f, ex) in enumerate(data):
        P, S = phi(R, C, A, B, f), sigma_rr(R, C, A, B, f)
        LP, LS = dump[i]
        st['py Phi == Lean phi'] += P == LP
        st['py Sigma.rr == Lean sigmaRR'] += S == LS
        st['py Phi == py Sigma.rr (thm G4)'] += P == S
        st['py Phi == engine column'] += P == ex
        st['LESION tie->west: Phi changes'] += phi(R, C, A, B, f, tie='west') != P
        st['LESION column order: Sigma changes'] += sigma_rr(R, C, A, B, f, order='col') != S
        st['nonempty Phi'] += bool(P)
    for k, v in st.items(): print(f'{k}: {v}/3556')
