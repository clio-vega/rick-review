"""
Test of Rick's hunch H2 (UID 819 section 7) against the 15/16 itself.

Motegi 2610.15344, section Discussion, L5654-5658 (read first-hand, e-print
typebcweightfunctions_arxivversionfinal-3.tex): the normalised type-C weight functions
agree with Koncki's twisted motivic Chern classes for LG(2,4) in 15 of the 16 entries.

LG(2,4) has 4 torus-fixed points, indexed by subsets of {1,2}; 4 classes likewise.
So the table is the 4x4 matrix of fixed-point restrictions Atilde_{M,I} at N=2, and
"one entry off" means ONE of its 16 cells disagrees.

Question: which rescalings of Atilde move exactly one cell?
Entry (M,I) moves iff Atilde_{M,I} != 0 (triangularity, Motegi Thm 2.6(i), L603-620)
AND the rescaling factor at (M,I) is != 1.
"""
from itertools import combinations
from motegi_order import geq, subsets

N = 2
S = subsets(N)
nz = [(M, I) for M in S for I in S if geq(M, I)]
print(f"N=2: {len(nz)} of {len(S)**2} entries are nonzero; "
      f"{len(S)**2 - len(nz)} vanish by triangularity\n")

print("support pattern (rows = point M, cols = label I):")
print("        " + "".join(f"{str(I):>8}" for I in S))
for M in S:
    print(f"{str(M):>8}" + "".join(f"{'X' if geq(M,I) else '.':>8}" for I in S))

rows = {M: sum(1 for (Mp, I) in nz if Mp == M) for M in S}
cols = {I: sum(1 for (M, Ip) in nz if Ip == I) for I in S}
print("\nnonzero entries per row (point M):   ", {str(k): v for k, v in rows.items()})
print("nonzero entries per col (label I):   ", {str(k): v for k, v in cols.items()})

print("\n--- how many cells move under each kind of rescaling? ---")
# point-diagonal of the coboundary (product) form: Psi(M) = prod_{m in M} chi(w_m).
# Psi(empty) = 1 always (empty product), so row M = () can never be the lone moved row.
moved_product = sum(1 for (M, I) in nz if M != ())
print(f"point-diagonal PRODUCT  Psi(M)=prod_{{m in M}}chi(w_m), chi nonconstant: "
      f"{moved_product} cells move  ->  agreement {16-moved_product}/16")
print(f"  (this is Theorem A/B's pole-removing renormalisation)")
print("\nlone-cell candidates:")
for M in S:
    if rows[M] == 1:
        cell = [c for c in nz if c[0] == M][0]
        print(f"  row/point M={M} has exactly 1 nonzero cell -> unique moved cell {cell}"
              f"   [unavailable to a product normalisation: Psi(())=1]")
for I in S:
    if cols[I] == 1:
        cell = [c for c in nz if c[1] == I][0]
        print(f"  col/label I={I} has exactly 1 nonzero cell -> unique moved cell {cell}")
print(f"\nRick's bet: the odd entry is (M,I) = (({1},{2}) , ()) i.e. ({{1,2}}, empty).")
cell = ((1, 2), ())
print(f"  Is (({1,2}), ()) a lone-cell candidate?  "
      f"row {cell[0]} has {rows[cell[0]]} nonzero cells, "
      f"col {cell[1]} has {cols[cell[1]]} nonzero cells  -> NO")
