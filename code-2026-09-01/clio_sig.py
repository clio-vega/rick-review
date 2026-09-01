"""
Independent reimplementation of the level-1 i-signature machinery, written from
the definitions in proofs/2026-08-11-C5-gerber-bicrystal.tex (Clio's own
conventions), NOT from Lyra's refute_c5.py.

Clio's stated conventions (tex lines 97-99, 137-141, 322-328, 396-409):
  res(r,c) = (c - r) mod e,  0-indexed rows and columns.
  addable node of row r  : column mu_r,      exists iff r = 0 or mu_{r-1} > mu_r
  removable node of row r: column mu_r - 1,  exists iff r = L-1 or mu_{r+1} < mu_r
  new row r = L          : column 0, always addable
  i-signature read in BOTTOM-UP row order (largest row index first)
  cancellation: "cancel any A that immediately follows an R"  (RA -> empty)
  eps_i = number of surviving R
"""
import re
from itertools import chain


def partitions_upto(n):
    """All partitions of size 0..n as weakly-decreasing tuples."""
    res = [()]
    def rec(rem, cap, pre):
        for p in range(min(rem, cap), 0, -1):
            res.append(tuple(pre + [p]))
            rec(rem - p, p, pre + [p])
    rec(n, n, [])
    return sorted(set(res))


def nodes(mu):
    """All (row, col, kind) candidate nodes of mu, kind in {'A','R'}, valid ones only.

    Returned in TOP-DOWN row order (row 0 first), new row last.
    """
    L = len(mu)
    out = []
    for r in range(L):
        # addable node of row r
        if r == 0 or mu[r - 1] > mu[r]:
            out.append((r, mu[r], 'A'))
        # removable node of row r
        below = mu[r + 1] if r + 1 < L else 0
        if mu[r] > below:
            out.append((r, mu[r] - 1, 'R'))
    out.append((L, 0, 'A'))          # the new row
    return out


def signature(mu, i, e, order='bottom_up'):
    """i-signature word.  order='bottom_up' = largest row index first."""
    ns = [(r, c, k) for (r, c, k) in nodes(mu) if (c - r) % e == i % e]
    # sort by row; within a row order by column (R at mu_r-1 comes before A at mu_r)
    ns.sort(key=lambda t: (t[0], t[1]))
    if order == 'bottom_up':
        ns = ns[::-1]
    return ''.join(k for (_, _, k) in ns), ns


def reduce_word(w, rule='RA'):
    """Cancel the given adjacent pair to convergence, via a stack."""
    a, b = rule[0], rule[1]
    st = []
    for s in w:
        if s == b and st and st[-1] == a:
            st.pop()
        else:
            st.append(s)
    return ''.join(st)


def eps_phi(mu, i, e, order='bottom_up', rule='RA'):
    w, ns = signature(mu, i, e, order)
    red = reduce_word(w, rule)
    return red.count('R'), red.count('A'), w, red, ns
