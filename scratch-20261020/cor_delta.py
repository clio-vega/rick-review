"""Corollary Delta (theorem-W-sharp section 3):
   C(empty,empty,[n];c) = K_n det( w_i^{c-k} - w_i^k )_{i=1..n, k=0..n-1}
   claim: det = 0  <=>  c in [0, 2n-2].
Instrument: sympy exact symbolic determinant in Q(w_1..w_n), c an explicit integer.
This is a claim about a DOMAIN of c, so sweep c well outside the window in BOTH
directions, and include odd c (the Day 246 failure mode was an even-only sample).
"""
import sympy as sp

def detmat(n, c):
    w = sp.symbols(f'w1:{n+1}', positive=True)
    M = sp.Matrix(n, n, lambda i, k: w[i]**(c-k) - w[i]**k)
    return sp.simplify(sp.factor(M.det()))

print("n  c    det==0 ?   in [0,2n-2]?   agree")
bad = []
for n in range(1, 6):
    lo, hi = 0, 2*n-2
    for c in range(-6, 2*n+7):          # both directions, every parity
        d = detmat(n, c)
        iszero = (d == 0)
        inwin = (lo <= c <= hi)
        ok = (iszero == inwin)
        if not ok:
            bad.append((n, c, iszero, inwin))
        if n <= 4:
            print(f"{n}  {c:3d}   {str(iszero):5s}      {str(inwin):5s}        {'ok' if ok else 'MISMATCH'}")
print()
print("n=5 swept silently.")
print("MISMATCHES:", bad if bad else "none -- Corollary Delta confirmed for n<=5, c in [-6, 2n+6]")
