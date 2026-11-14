"""Independent Q77 checker (Clio, 2026-11-14). Built from definitions only:
H_N(0) acts on the RIGHT on words: w.pi_i = w s_i if w_i < w_{i+1} (ascent), else w.
Vectors are dicts word->int (exact Z)."""
import itertools
from collections import defaultdict, deque

def move(w, i):            # i is 1-indexed position
    if w[i-1] < w[i]:
        return w[:i-1] + (w[i], w[i-1]) + w[i+1:]
    return w

def act_pi(vec, i):
    out = defaultdict(int)
    for w, c in vec.items():
        out[move(w, i)] += c
    return {w: c for w, c in out.items() if c}

def act_pibar(vec, i):     # 1 - pi_i
    out = defaultdict(int, vec)
    for w, c in vec.items():
        out[move(w, i)] -= c
    return {w: c for w, c in out.items() if c}

def w0_word(a, b):
    """reduced word of longest element of <s_a..s_b> (as list of generator indices)"""
    word = []
    for top in range(b, a-1, -1):
        word += list(range(a, top+1))
    return word

def apply_seq(vec, seq):
    """seq: list of ('p'|'b', i), applied left to right (right action)."""
    for kind, i in seq:
        vec = act_pi(vec, i) if kind == 'p' else act_pibar(vec, i)
    return vec

def weight(w, n):
    m = [0]*n
    for c in w: m[c-1] += 1
    return tuple(m)

def words_of_weight(mu):
    base = []
    for c, k in enumerate(mu, 1): base += [c]*k
    return sorted(set(itertools.permutations(base)))

def asc(w):
    return {i for i in range(1, len(w)) if w[i-1] < w[i]}

def S_of(mu):
    s, out = 0, set()
    nz = [k for k in mu if k > 0]
    for k in nz[:-1]:
        s += k; out.add(s)
    return out

def compositions(N, n):
    for c in itertools.combinations(range(N+n-1), n-1):
        prev, parts = -1, []
        for x in c + (N+n-1,):
            parts.append(x-prev-1); prev = x
        yield tuple(parts)

def schur_basis(n, N):
    """All maps phi_u : M_mu -> M_nu (u a word of weight nu with Asc(u) in S(mu)),
    constructed by BFS from v_0^mu, CHECKED well-defined and H-linear exactly.
    Returns list of (mu, nu, dict word->word)."""
    maps = []
    for mu in compositions(N, n):
        v0 = tuple(c for c, k in enumerate(mu, 1) for _ in range(k))
        Smu = S_of(mu)
        # BFS paths from v0
        for nu in compositions(N, n):
            for u in words_of_weight(nu):
                if not asc(u) <= Smu: continue
                phi = {v0: u}
                dq = deque([v0])
                while dq:
                    w = dq.popleft()
                    for i in range(1, N):
                        w2 = move(w, i); u2 = move(phi[w], i)
                        if w2 in phi:
                            assert phi[w2] == u2, "ill-defined"
                        else:
                            phi[w2] = u2; dq.append(w2)
                assert len(phi) == len(words_of_weight(mu))
                for w in phi:           # H-linearity, every word, every i
                    for i in range(1, N):
                        assert phi[move(w, i)] == move(phi[w], i)
                maps.append((mu, nu, phi))
    return maps
