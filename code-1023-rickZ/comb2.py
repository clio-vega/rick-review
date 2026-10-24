from comb import *
from collections import Counter

# max over chains C of D(kappa) of |C cap theta|  ==  longest chain contained in theta
# (C cap theta is a chain in theta; any chain in theta is a chain of D(kappa))

print("== CHECK 2b: Lemma Ch core claim -- longest chain in theta <= 2, over BR'-admissible pairs ==")
for m in range(1, 9):
    ks = strict_partitions(m); n = 0; viol = []
    hist = Counter()
    for kappa in ks:
        Dk = D(kappa, m)
        for rho in ks:
            if rho == kappa or not contains(kappa, rho): continue
            theta = Dk - D(rho, m)
            if not theta or not admissible_BRprime(theta): continue
            n += 1
            lc = longest_chain(theta)
            hist[lc] += 1
            if lc > 2: viol.append((kappa, rho, sorted(theta), lc))
    print(f"  m={m}: {n} pairs, |C cap theta| histogram {dict(sorted(hist.items()))}, violations = {len(viol)}")

print("\n== CONTROL (positive): replace BR's strictly-SE rim by the WEAKER 'no 2x2 square' ==")
print("   If the weaker predicate also gave the chain bound, BR's definition would not be load-bearing.")
for m in range(1, 9):
    ks = strict_partitions(m); n = 0; viol = []
    for kappa in ks:
        Dk = D(kappa, m)
        for rho in ks:
            if rho == kappa or not contains(kappa, rho): continue
            theta = Dk - D(rho, m)
            if not theta or not admissible_weak(theta): continue
            n += 1
            if longest_chain(theta) > 2: viol.append((kappa, rho, sorted(theta), longest_chain(theta)))
    extra = n - sum(1 for kappa in ks for rho in ks
                    if rho != kappa and contains(kappa, rho)
                    and (D(kappa,m)-D(rho,m)) and admissible_BRprime(D(kappa,m)-D(rho,m)))
    print(f"  m={m}: weak-admissible pairs = {n} (+{extra} vs BR'), CHAIN-BOUND FAILURES = {len(viol)}")
    if viol: print(f"       first failure: kappa={viol[0][0]} rho={viol[0][1]} theta={viol[0][2]} chain={viol[0][3]}")

print("\n== CONTROL: drop bound r'(rho) >= r'(kappa)-2 under the WEAKER predicate ==")
for m in range(1, 9):
    ks = strict_partitions(m); dv = []; mind = 0
    for kappa in ks:
        Dk = D(kappa, m); rk = rprime(kappa, m)
        for rho in ks:
            if rho == kappa or not contains(kappa, rho): continue
            theta = Dk - D(rho, m)
            if not theta or not admissible_weak(theta): continue
            rr = rprime(rho, m); mind = min(mind, rr-rk)
            if rr < rk - 2: dv.append((kappa, rho, rk, rr))
    print(f"  m={m}: drop violations = {len(dv)}, min drop = {mind}" +
          (f"  e.g. kappa={dv[0][0]} rho={dv[0][1]} r'={dv[0][2]}->{dv[0][3]}" if dv else ""))

print("\n== Rick's sharp witness: the diagonal 3-box shape {(r,r),(r,r+1),(r+1,r+1)} ==")
th = frozenset({(0,0),(0,1),(1,1)})
print(f"  theta = {sorted(th)}")
print(f"  no 2x2 square?            {no_2x2(th)}")
print(f"  <=2 per row and column?   {le2_per_row_col(th)}")
print(f"  no strictly-SE pair (BR)? {no_strict_SE_pair(th)}   <- BR's rim condition EXCLUDES it")
print(f"  longest chain in theta:   {longest_chain(th)}        <- a 3-chain, so Lemma Ch would FAIL")
print(f"  (1,1) strictly SE of (0,0)? {(1>0) and (1>0)}")
