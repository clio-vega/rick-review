"""Negative controls: plant convention errors and confirm each test SEES them."""
from clio_sig import partitions_upto
from check3_conventions import cartan, content_counts, pairing, reduce_tracked, remove_node

def nodes_perturbed(mu, mode):
    """Node generator with a deliberately planted error."""
    L = len(mu); out = []
    for r in range(L):
        if mode == 'add_validity_dropped':           # forget the strict-step test on addables
            out.append((r, mu[r], 'A'))
        elif r == 0 or mu[r-1] > mu[r]:
            out.append((r, mu[r], 'A'))
        below = mu[r+1] if r+1 < L else 0
        if mode == 'rem_col_shift':                  # removable at column mu_r instead of mu_r-1
            if mu[r] > below: out.append((r, mu[r], 'R'))
        elif mu[r] > below:
            out.append((r, mu[r]-1, 'R'))
    if mode != 'no_new_row':
        out.append((L, 0, 'A'))
    return out

def sig_pert(mu, i, e, mode, order='bottom_up'):
    ns = [(r,c,k) for (r,c,k) in nodes_perturbed(mu, mode) if (c-r) % e == (i + (1 if mode=='res_shift' else 0)) % e]
    ns.sort(key=lambda t:(t[0],t[1]))
    if order=='bottom_up': ns = ns[::-1]
    return ns

MODES = ['clean','res_shift','add_validity_dropped','rem_col_shift','no_new_row']
print("=== NEGATIVE CONTROL on TEST 1 (weight axiom) — does it see a broken node rule? ===")
for mode in MODES:
    bad = tot = 0
    for e in (2,3,4):
        for mu in partitions_upto(9):
            for i in range(e):
                st = reduce_tracked(sig_pert(mu,i,e,mode), 'RA')
                eps = sum(1 for n in st if n[2]=='R'); phi = sum(1 for n in st if n[2]=='A')
                tot += 1
                if phi-eps != pairing(mu,i,e): bad += 1
    flag = "  <-- planted error DETECTED" if (bad>0) != (mode=='clean') and mode!='clean' else ("" if mode=='clean' else "  <-- MISSED")
    print(f"  {mode:22s}: {bad:4d}/{tot} weight-axiom violations{flag}")

print("\n=== NEGATIVE CONTROL on TEST 3 (the eps<=1 claim itself) — does the sweep see a broken claim? ===")
for mode in MODES:
    viol = 0
    for e in range(2,6):
        for lam in partitions_upto(9):
            mu = tuple(e*p for p in lam)
            for i in range(e):
                st = reduce_tracked(sig_pert(mu,i,e,mode), 'RA')
                if sum(1 for n in st if n[2]=='R') > 1: viol += 1
    print(f"  {mode:22s}: {viol:4d} triples with eps>1 on mu=e*lambda")

print("\n=== What the MIRROR convention (bottom_up, cancel AR) actually returns on mu=e*lambda ===")
from clio_sig import signature
dist = {}
for e in range(2,7):
    for lam in partitions_upto(11):
        mu = tuple(e*p for p in lam)
        for i in range(e):
            _, ns = signature(mu, i, e, 'bottom_up')
            st = reduce_tracked(ns, 'AR')
            k = sum(1 for n in st if n[2]=='R')
            dist[k] = dist.get(k,0)+1
print(f"  eps distribution under the mirror: {dict(sorted(dist.items()))}")
