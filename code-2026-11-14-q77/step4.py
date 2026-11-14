from witness import *
from run2 import an_seq, wy, uy
def star(w, n): return tuple(n+1-c for c in reversed(w))
n, N = 3, 6
S = schur_basis(n, N)
seq = an_seq(n)
for y in (2, 3):
    mu = weight(wy(n, y), n)
    beta = operator(n, N, seq, {mu})
    bstar = {star(w, n): {star(x, n): c for x, c in z.items()} for w, z in beta.items()}
    mustar = weight(star(wy(n, y), n), n)
    print(f"y={y}: mu={mu} mu*={mustar} beta* B-viol={in_B(bstar, S)}")
    for yp in (2, 3):
        if yp == y: continue
        s, g = star(wy(n, y), n), star(wy(n, yp), n)
        orb, cert = notin_A_certificate(bstar.get(s, {}), bstar.get(g, {}), s, g, N)
        print(f"   mirrored pair (w_{y}*, w_{yp}*): orbit={orb} cert-components={cert}")
        # cross check: beta (unmirrored) vanishes on mirrored source words
        print("   beta on w*-words:", beta.get(s, {}), beta.get(g, {}), " beta* on w-words:", bstar.get(wy(n,y), {}), bstar.get(wy(n,yp), {}))
