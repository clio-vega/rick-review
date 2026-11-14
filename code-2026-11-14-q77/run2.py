from witness import *
def an_seq(n, drop_pi=False):
    N = 2*n
    return [('b', i) for i in w0_word(1, n-1)] + ([] if drop_pi else [('p', n)]) + [('b', i) for i in w0_word(n+1, N-1)]
def wy(n, y): return tuple(range(1, n+1)) + (y,) + tuple(range(2, n+1))
def uy(n, y): return tuple(range(2, n+1)) + (y, 1) + tuple(range(2, n+1))
for n in [3, 4]:
    N = 2*n
    S = schur_basis(n, N) if n == 3 else None
    for drop in [False, True]:
        seq = an_seq(n, drop)
        for y in range(1, n+1):
            mu = weight(wy(n, y), n)
            beta = operator(n, N, seq, {mu})
            bv = in_B(beta, S) if S else 'skip'
            for yp in range(1, n+1):
                if yp == y: continue
                s, g = wy(n, y), wy(n, yp)
                zs = beta.get(s, {}); zg = beta.get(g, {})
                orb, cert = notin_A_certificate(zs, zg, s, g, N)
                # Lemma 2 direct: pairs in orbit with first coord u_y / second u_y'
                seen, _ = pair_orbit_components(s, g, N)
                L1 = sorted({b for a, b in seen if a == uy(n, y)}); L2 = sorted({a for a, b in seen if b == uy(n, yp)})
                lem = (L1 == [uy(n, yp)] and L2 == [uy(n, y)])
                print(f"(n,N)=({n},{N}) drop_pi={drop} y={y} y'={yp}: B-viol={bv} <z,u_y>={zs.get(uy(n,y),0)} "
                      f"orbit={orb} cert-components={cert} Lemma2={lem}")
