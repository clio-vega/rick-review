"""Rick's P1b Cut Lemma vs D_m R_s computed from the pairing (keyid.perp_M)."""
import sys
from itertools import product
sys.argv = [sys.argv[0], '1']
from keyid import perp_M
from qsym import mask_to_comp, str_to_mask

def ribbon_of_word(wd):        # {r,u}-word -> composition (u = descent)
    parts, cur = [], 1
    for ch in wd:
        if ch == 'u': parts.append(cur); cur = 1
        else: cur += 1
    parts.append(cur); return tuple(parts)

def Ev(word):                  # word over {r,u,e}; e = r+u
    if word == 'e': return {(): 1}
    out = {}
    idx = [t for t, ch in enumerate(word) if ch == 'e']
    for ch in product('ru', repeat=len(idx)):
        wl = list(word)
        for t, cc in zip(idx, ch): wl[t] = cc
        if wl[0] != 'r' or wl[-1] != 'u': continue
        comp = ribbon_of_word(''.join(wl[1:-1]))
        out[comp] = out.get(comp, 0) + 1
    return out

def cut(s, m):
    P = 'r' + ''.join('u' if ch == '1' else 'r' for ch in s) + 'u'
    out = {}
    for i in range(len(P) - m):
        if P[i] == 'r' and P[i + m] == 'u':
            sign = (-1) ** P[i + 1:i + m].count('u')
            for k, v in Ev(P[:i] + 'e' + P[i + m + 1:]).items():
                out[k] = out.get(k, 0) + sign * v
    return {k: v for k, v in out.items() if v}

tot = bad = nz = 0
for L in range(1, int(sys.argv_L) if False else 10):
    for bits in product('01', repeat=L):
        s = ''.join(bits); comp = mask_to_comp(str_to_mask(s), L + 1)
        for m in range(1, min(5, L + 1) + 1):
            lhs = perp_M((m,), comp); rhs = cut(s, m)
            tot += 1; nz += bool(lhs)
            if lhs != rhs:
                bad += 1
                if bad <= 3: print('FAIL', s, m, lhs, rhs)
print('Cut Lemma: %d (s,m) cases, L<=9, m<=5: %d bad, %d nonzero' % (tot, bad, nz))
