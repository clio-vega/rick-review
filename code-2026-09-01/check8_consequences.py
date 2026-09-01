"""The registry node C5-level-1-signature-word lists three consequences.
   (1) eps_i(e.lam) <= 1, eps_0 = 0 always
   (2) eps^op (suffix maximum) is 0
   (3) eps_i(vertical inflation) = 0
   Check all three, plus whether the WRONG multiplicity m still yields the right
   dichotomy conclusion (does the error propagate to Q55-crystal-dichotomy-level-1?).
"""
from clio_sig import partitions_upto, signature, eps_phi
from check7_registry import m_registry, m_corrected

def prefix_max(w):   # max excess of R over A over prefixes
    best = cur = 0
    for s in w:
        cur += 1 if s=='R' else -1
        best = max(best, cur)
    return best
def suffix_max(w):
    best = cur = 0
    for s in reversed(w):
        cur += 1 if s=='R' else -1
        best = max(best, cur)
    return best

def conjugate(lam):
    if not lam: return ()
    return tuple(sum(1 for p in lam if p > c) for c in range(lam[0]))

c1 = c2 = c3 = c4 = tot = 0
f2 = f3 = None
for e in range(2,7):
    for lam in partitions_upto(10):
        mu = tuple(e*p for p in lam)
        for i in range(e):
            tot += 1
            eps, phi, w_bu, red, _ = eps_phi(mu, i, e)          # bottom-up, cancel RA
            w_td = signature(mu, i, e, 'top_down')[0]
            # (1)
            if eps > 1 or (i % e == 0 and eps != 0): c1 += 1
            # registry reads eps as PREFIX max of the TOP-DOWN word
            if prefix_max(w_td) != eps: c4 += 1
            # (2) eps^op = suffix max of the top-down word
            if suffix_max(w_td) != 0:
                c2 += 1
                if f2 is None: f2 = (e, lam, i, w_td)
            # (3) vertical inflation V(lam) = (e * lam')'
            V = conjugate(tuple(e*p for p in conjugate(lam)))
            if eps_phi(V, i, e)[0] != 0:
                c3 += 1
                if f3 is None: f3 = (e, lam, i, V, eps_phi(V,i,e)[2])
print(f"{tot} triples, e<=6, |lam|<=10")
print(f"  (1) eps<=1 and eps_0=0            : {c1} failures")
print(f"  (2) eps^op (suffix max) = 0       : {c2} failures" + (f"  first {f2}" if f2 else ""))
print(f"  (3) eps_i(vertical inflation) = 0 : {c3} failures" + (f"  first {f3}" if f3 else ""))
print(f"  cross-check: prefix-max(top-down word) == stack-eps(bottom-up word) : {c4} mismatches")

# does the wrong m change the DICHOTOMY conclusion (eps=1 vs eps^op=0)?
dis = 0; fd = None
for e in range(2,7):
    for lam in partitions_upto(10):
        for i in range(e):
            if (m_registry(lam,i,e) >= 1) != (m_corrected(lam,i,e) >= 1):
                dis += 1
                if fd is None: fd = (e, lam, i, m_registry(lam,i,e), m_corrected(lam,i,e))
print(f"\n  [m_registry >= 1] vs [m_corrected >= 1] disagree on {dis} triples" + (f"; first e={fd[0]} lam={fd[1]} i={fd[2]} m_reg={fd[3]} m_corr={fd[4]}" if fd else ""))
