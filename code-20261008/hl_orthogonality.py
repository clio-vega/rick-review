"""
Independent ground truth for Green polynomials X^lambda_mu(t), defined by
    p_mu = sum_lambda X^lambda_mu(t) P_lambda(x;t)      (Macdonald III (7.1))

MECHANISM: the Gram--Schmidt / orthogonality *definition* of Hall--Littlewood P.
  - t-deformed Hall inner product, diagonal in the power sums (Macdonald III (4.5)):
        <p_lam, p_mu>_t = delta_{lam,mu} * z_lam / prod_i (1 - t^{lam_i})
  - P_lam = m_lam + (strictly lower in dominance), and <P_lam,P_mu>_t = 0 for lam != mu.
  - Readout A: solve p_mu = sum_lam X^lam_mu P_lam in the m-basis.
  - Readout B: X^lam_mu = b_lam(t) * <p_mu, P_lam>_t    (since Q_lam = b_lam P_lam is dual to P).

Uses NEITHER Kostka--Foulkes nor Murnaghan--Nakayama (Rick's green.py), NOR the
h-expansion of the modified Hall--Littlewood Q'_lam (Clio's Theorem B route).
A third, independent instrument.

Exact arithmetic (Fraction) at rational sample values of t.
"""
from fractions import Fraction as F
from itertools import combinations
from functools import lru_cache
from collections import Counter, defaultdict

# ---------- partitions ----------
@lru_cache(maxsize=None)
def partitions(n, maxpart=None):
    if maxpart is None: maxpart = n
    if n == 0: return ((),)
    out = []
    for k in range(min(n, maxpart), 0, -1):
        for rest in partitions(n - k, k):
            out.append((k,) + rest)
    return tuple(out)

def dominates(lam, mu):
    sl = sm = 0
    for i in range(max(len(lam), len(mu))):
        sl += lam[i] if i < len(lam) else 0
        sm += mu[i] if i < len(mu) else 0
        if sl < sm: return False
    return True

def zlam(lam):
    z = 1
    for part, mult in Counter(lam).items():
        for k in range(1, mult + 1): z *= k
        z *= part ** mult
    return z

def b_lambda(lam, t):
    """b_lam(t) = prod_i phi_{m_i(lam)}(t), phi_r(t) = prod_{k=1}^r (1-t^k)."""
    v = F(1)
    for _part, r in Counter(lam).items():
        for k in range(1, r + 1): v *= (1 - t**k)
    return v

# ---------- p_mu in the monomial basis, via set partitions ----------
def set_partitions(lst):
    if not lst:
        yield []
        return
    first, rest = lst[0], lst[1:]
    for sub in set_partitions(rest):
        for i in range(len(sub)):
            yield sub[:i] + [[first] + sub[i]] + sub[i+1:]
        yield [[first]] + sub

@lru_cache(maxsize=None)
def p_in_m(mu):
    """{nu: integer coeff} with p_mu = sum_nu coeff * m_nu.
    prod p_{mu_i} = sum_{set partitions pi} mtilde_{blocksums(pi)},
    mtilde_nu = (prod_i m_i(nu)!) m_nu."""
    acc = defaultdict(int)
    for pi in set_partitions(list(range(len(mu)))):
        nu = tuple(sorted((sum(mu[i] for i in blk) for blk in pi), reverse=True))
        acc[nu] += 1
    out = {}
    for nu, c in acc.items():
        fac = 1
        for _part, r in Counter(nu).items():
            for k in range(1, r + 1): fac *= k
        out[nu] = c * fac
    return out

# ---------- linear algebra over Fraction ----------
def mat_inverse(M):
    n = len(M)
    A = [[F(M[i][j]) for j in range(n)] + [F(1) if i == j else F(0) for j in range(n)]
         for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if A[r][c] != 0)
        A[c], A[piv] = A[piv], A[c]
        pv = A[c][c]
        A[c] = [v / pv for v in A[c]]
        for r in range(n):
            if r != c and A[r][c] != 0:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]

def solve(A, rhs):
    n = len(A)
    M = [[F(A[i][j]) for j in range(n)] + [F(rhs[i])] for i in range(n)]
    for c in range(n):
        piv = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[piv] = M[piv], M[c]
        pv = M[c][c]
        M[c] = [v / pv for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]

# ---------- the instrument ----------
class GreenEngine:
    def __init__(self, n, t0, perturb=None):
        """perturb: optional (lam, idx, delta) planted error in P_lam, for controls."""
        self.n, self.t = n, F(t0)
        self.lams = list(partitions(n))
        self.ix = {lam: i for i, lam in enumerate(self.lams)}
        N = len(self.lams)

        # m-coords <-> p-coords
        P2M = [[0]*N for _ in range(N)]
        for j, mu in enumerate(self.lams):
            for nu, c in p_in_m(mu).items():
                P2M[j][self.ix[nu]] = c
        Mp = [[F(P2M[j][i]) for j in range(N)] for i in range(N)]  # p-coords -> m-coords
        self.P2Mmat = Mp
        self.M2P = mat_inverse(Mp)                                 # m-coords -> p-coords

        self.gp = [F(zlam(lam)) / self._prod_1mt(lam) for lam in self.lams]

        order = sorted(range(N), key=lambda i: self._dom_key(self.lams[i]))
        # sanity: the linear extension must respect dominance
        for a in range(N):
            for b in range(N):
                if a != b and dominates(self.lams[order[a]], self.lams[order[b]]) :
                    assert a >= b, "linear extension violates dominance"

        self.Pm, self.Pp, self.Pnorm = {}, {}, {}
        for pos, i in enumerate(order):
            lam = self.lams[i]
            vm = [F(0)]*N; vm[i] = F(1)
            vp = self._to_p(vm)
            for j in order[:pos]:
                mu = self.lams[j]
                num = self._ipp(vp, self.Pp[mu])
                if num:
                    c = num / self.Pnorm[mu]
                    vm = [a - c*b for a, b in zip(vm, self.Pm[mu])]
                    vp = [a - c*b for a, b in zip(vp, self.Pp[mu])]
            if perturb and perturb[0] == lam:
                vm = list(vm); vm[perturb[1]] += F(perturb[2]); vp = self._to_p(vm)
            self.Pm[lam], self.Pp[lam] = vm, vp
            self.Pnorm[lam] = self._ipp(vp, vp)

        self.A = [[self.Pm[self.lams[j]][i] for j in range(N)] for i in range(N)]
        self._xcache = {}

    def _prod_1mt(self, lam):
        v = F(1)
        for a in lam: v *= (1 - self.t**a)
        return v

    def _dom_key(self, lam):
        ps, s = [], 0
        for a in lam: s += a; ps.append(s)
        ps += [self.n]*(self.n - len(ps))
        return tuple(ps)

    def _to_p(self, vm):
        N = len(vm)
        return [sum(self.M2P[k][i]*vm[i] for i in range(N) if vm[i]) for k in range(N)]

    def _ipp(self, up, vp):
        return sum(up[k]*vp[k]*self.gp[k] for k in range(len(up)) if up[k] and vp[k])

    # --- readout A: solve the linear system in the m-basis ---
    def X(self, lam, mu):
        if mu not in self._xcache:
            rhs = [F(0)]*len(self.lams)
            for nu, c in p_in_m(mu).items(): rhs[self.ix[nu]] = F(c)
            self._xcache[mu] = solve(self.A, rhs)
        return self._xcache[mu][self.ix[lam]]

    # --- readout B: X = b_lam * <p_mu, P_lam> ---
    def X_dual(self, lam, mu):
        pmu = [F(0)]*len(self.lams)
        for nu, c in p_in_m(mu).items(): pmu[self.ix[nu]] = F(c)
        return b_lambda(lam, self.t) * self._ipp(self._to_p(pmu), self.Pp[lam])

    # --- controls on the instrument ---
    def control_norms(self):
        """<P_lam,P_lam>_t must be 1/b_lam(t)."""
        return [(lam, self.Pnorm[lam], F(1)/b_lambda(lam, self.t))
                for lam in self.lams if self.Pnorm[lam] != F(1)/b_lambda(lam, self.t)]

    def control_orthogonal(self):
        return [(a, b_) for a, b_ in combinations(self.lams, 2)
                if self._ipp(self.Pp[a], self.Pp[b_]) != 0]

    def control_triangular(self):
        """P_lam supported on mu <= lam in dominance, coeff 1 on m_lam."""
        bad = []
        for lam in self.lams:
            if self.Pm[lam][self.ix[lam]] != 1: bad.append(('lead', lam))
            for i, c in enumerate(self.Pm[lam]):
                if c and not dominates(lam, self.lams[i]): bad.append(('supp', lam, self.lams[i]))
        return bad
