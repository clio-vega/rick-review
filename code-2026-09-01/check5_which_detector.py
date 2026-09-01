"""Which of the three reported detectors is actually live?
   D1: 'eps_i <= 1 on mu=e*lambda, 0 violations'  (the headline sweep)
   D2: 'every word matches ^(AR)*A?$'             (Lyra's structural check)
   D3: 'the eps VALUES  {0:2334, 1:1566}'         (the fine data)
   Negative control: five planted node-rule errors + two cancellation conventions.
"""
import re
from clio_sig import partitions_upto, signature
from check3_conventions import reduce_tracked
from check4_negcontrol import sig_pert
pat = re.compile(r'^(AR)*A?$')

MODES = ['clean','res_shift','add_validity_dropped','rem_col_shift','no_new_row']
REF = None
print(f"{'planted error':24s} {'D1 eps>1':>10s} {'D2 badword':>11s} {'D3 eps-dist':>28s}  verdict")
rows = []
for mode in MODES:
    viol = badw = 0; dist = {}
    for e in range(2,7):
        for lam in partitions_upto(11):
            mu = tuple(e*p for p in lam)
            for i in range(e):
                ns = sig_pert(mu, i, e, mode)
                w = ''.join(k for (_,_,k) in ns)
                if not pat.match(w): badw += 1
                st = reduce_tracked(ns, 'RA')
                k = sum(1 for n in st if n[2]=='R')
                dist[k] = dist.get(k,0)+1
                if k > 1: viol += 1
    if mode=='clean': REF = dist
    d3 = "match" if dist==REF else "DIFFERS"
    seen = [d for d,ok in (('D1',viol>0),('D2',badw>0),('D3',dist!=REF)) if ok]
    print(f"{mode:24s} {viol:10d} {badw:11d} {str(dict(sorted(dist.items()))):>28s}  " +
          ("baseline" if mode=='clean' else ("SEEN by "+",".join(seen) if seen else "*** MISSED BY ALL ***")))

print("\n--- same, for the two cancellation conventions (node rule clean) ---")
for rule in ('RA','AR'):
    viol=0; dist={}
    for e in range(2,7):
        for lam in partitions_upto(11):
            mu = tuple(e*p for p in lam)
            for i in range(e):
                _, ns = signature(mu, i, e, 'bottom_up')
                st = reduce_tracked(ns, rule)
                k = sum(1 for n in st if n[2]=='R')
                dist[k]=dist.get(k,0)+1
                if k>1: viol+=1
    print(f"  cancel {rule}: eps>1 = {viol:4d}   dist = {dict(sorted(dist.items()))}   "
          + ("baseline" if rule=='RA' else ("SEEN by D3 only" if dist!=REF else "MISSED")))
