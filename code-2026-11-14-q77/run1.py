from witness import *
import time
def thm1(n, N, lesion=None):
    S = schur_basis(n, N)
    seq = [('b', i) for i in w0_word(1, n-1)] + [('b', i) for i in w0_word(N-n+1, N-1)]
    mu = (N-2*n+2,) + (2,)*(n-1); mu2 = (2, N-2*n+2) + (2,)*(n-2)
    C = {mu}
    if lesion == 'single-factor': seq = [('b', i) for i in w0_word(1, n-1)]
    if lesion == 'C-all': C = set(compositions(N, n))
    beta = operator(n, N, seq, C)
    dword = lambda m: tuple(range(1, n+1)) + tuple(c for c in range(n, 0, -1) for _ in range(m[c-1]-2)) + tuple(range(1, n+1))
    s, g = dword(mu), dword(mu2)
    assert weight(s, n) == mu and weight(g, n) == mu2 and asc(s) == asc(g)
    zs, zg = beta.get(s, {}), beta.get(g, {})
    orb, cert = notin_A_certificate(zs, zg, s, g, N)
    print(f"Thm1 (n,N)=({n},{N}) lesion={lesion}: mu={mu} partner={mu2} |supp beta|={len(beta)} "
          f"B-violations={in_B(beta, S)}  orbit={orb} components-with-nonzero-lambda={cert}")
for nN in [(2,5),(2,6),(3,7)]:
    for les in [None, 'single-factor', 'C-all']:
        thm1(*nN, les)
