"""Convention sensitivity + crystal-axiom anchoring.

Four candidate conventions: (reading order) x (cancelled adjacent pair).
Reference = Clio's & Lyra's shared one: bottom_up + cancel RA.
"""
from clio_sig import *

CONV = [('bottom_up','RA'), ('bottom_up','AR'), ('top_down','RA'), ('top_down','AR')]

def cartan(e):
    A = [[0]*e for _ in range(e)]
    for i in range(e):
        A[i][i] = 2
        if e == 2:
            A[i][1-i] = -2
        else:
            A[i][(i+1) % e] -= 1
            A[i][(i-1) % e] -= 1
    return A

def content_counts(mu, e):
    m = [0]*e
    for r, part in enumerate(mu):
        for c in range(part):
            m[(c-r) % e] += 1
    return m

def pairing(mu, i, e):
    """<h_i, wt(mu)> = delta_{i,0} - sum_j a_ij m_j   for the level-1 Fock space, wt = Lambda_0 - sum m_j alpha_j."""
    A = cartan(e); m = content_counts(mu, e)
    return (1 if i % e == 0 else 0) - sum(A[i % e][j]*m[j] for j in range(e))

def reduce_tracked(ns, rule):
    """Stack-cancel keeping node identities. ns = list of (r,c,kind) in reading order."""
    a, b = rule[0], rule[1]
    st = []
    for nd in ns:
        if nd[2] == b and st and st[-1][2] == a:
            st.pop()
        else:
            st.append(nd)
    return st

def eps_phi_nodes(mu, i, e, order, rule):
    _, ns = signature(mu, i, e, order)
    st = reduce_tracked(ns, rule)
    return sum(1 for n in st if n[2]=='R'), sum(1 for n in st if n[2]=='A'), st

def remove_node(mu, r):
    lst = list(mu); lst[r] -= 1
    return tuple(p for p in lst if p > 0)

# ---------------------------------------------------------------- test 1: weight identity
print("=== TEST 1: crystal weight axiom  phi_i - eps_i == <h_i, wt(mu)>  (ALL partitions) ===")
for order, rule in CONV:
    bad = tot = 0
    for e in (2,3,4):
        for mu in partitions_upto(9):
            for i in range(e):
                eps, phi, _ = eps_phi_nodes(mu, i, e, order, rule)
                tot += 1
                if phi - eps != pairing(mu, i, e): bad += 1
    print(f"  {order:9s} cancel {rule}:  {bad}/{tot} violations")

# ---------------------------------------------------------------- test 2: eps decrement
print("\n=== TEST 2: crystal axiom  eps_i(e~_i mu) == eps_i(mu) - 1  (good node = leftmost surviving R) ===")
for order, rule in CONV:
    bad = tot = 0
    firstbad = None
    for e in (2,3,4):
        for mu in partitions_upto(9):
            for i in range(e):
                eps, phi, st = eps_phi_nodes(mu, i, e, order, rule)
                if eps == 0: continue
                good = next(n for n in st if n[2]=='R')      # leftmost surviving R in reading order
                nu = remove_node(mu, good[0])
                eps2, _, _ = eps_phi_nodes(nu, i, e, order, rule)
                tot += 1
                if eps2 != eps - 1:
                    bad += 1
                    if firstbad is None: firstbad = (e, mu, i, eps, eps2, good)
    print(f"  {order:9s} cancel {rule}:  {bad}/{tot} violations" + (f"   first: e={firstbad[0]} mu={firstbad[1]} i={firstbad[2]} eps={firstbad[3]}->{firstbad[4]} good={firstbad[5]}" if firstbad else ""))

# ---------------------------------------------------------------- test 3: sensitivity on e*lambda
print("\n=== TEST 3: sensitivity on mu = e*lambda (e<=6, |lam|<=11, 3900 triples) ===")
print("   SEEN = # triples where eps differs from the reference (bottom_up, RA)")
ref = {}
for e in range(2,7):
    for lam in partitions_upto(11):
        mu = tuple(e*p for p in lam)
        for i in range(e):
            ref[(e,lam,i)] = eps_phi_nodes(mu, i, e, 'bottom_up','RA')[0]
for order, rule in CONV:
    seen = viol = 0
    for e in range(2,7):
        for lam in partitions_upto(11):
            mu = tuple(e*p for p in lam)
            for i in range(e):
                eps = eps_phi_nodes(mu, i, e, order, rule)[0]
                if eps != ref[(e,lam,i)]: seen += 1
                if eps > 1: viol += 1
    print(f"  {order:9s} cancel {rule}:  SEEN={seen:5d}   eps>1 violations={viol}")

print("\n=== TEST 3b: same sensitivity on GENERAL partitions (|mu|<=10, e<=4) ===")
ref2 = {}
for e in range(2,5):
    for mu in partitions_upto(10):
        for i in range(e):
            ref2[(e,mu,i)] = eps_phi_nodes(mu, i, e, 'bottom_up','RA')[0]
for order, rule in CONV:
    seen = 0
    for e in range(2,5):
        for mu in partitions_upto(10):
            for i in range(e):
                if eps_phi_nodes(mu, i, e, order, rule)[0] != ref2[(e,mu,i)]: seen += 1
    print(f"  {order:9s} cancel {rule}:  SEEN={seen:5d} / {len(ref2)}")
