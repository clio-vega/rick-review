"""Item 1, addendum: Rick's node R-equiv-compositional (trust=proved) states that
iterating (Re) gives the composition sum
   X_n = sum over (k_1..k_r), k_i>=2 for i<r, k_r>=1,
         of q^{r-1} * prod_{i<r}[k_i-1]_q * [k_r]_q * e_{k_1}...e_{k_r}.
Checked here against (Re) itself and against the geometric expansion
   F/(1-D) = F * sum_{j>=0} D^j
of the STATEMENT of AP (arXiv:1705.10353) Theorem 38, which is where (Re) comes from.
Everything is a polynomial identity in free commuting e_i, so expand() decides it."""
import sympy as sp
q, z = sp.symbols('q z')
N = 7
e = sp.symbols('e0:%d' % (N+1))
def br(i): return sum(q**j for j in range(i))

def comps(n):
    out = []
    def rec(rem, cur):
        out.append(tuple(cur + [rem]))            # close with the final part k_r = rem >= 1
        for k in range(2, rem):                   # a non-final part k_i >= 2, leaving rem-k >= 1
            rec(rem - k, cur + [k])
    rec(n, [])
    return sorted(set(out))

X_comp = [sp.Integer(1)]
for n in range(1, N+1):
    tot = sp.Integer(0)
    for c in comps(n):
        w = q**(len(c)-1) * br(c[-1])
        for k in c[:-1]:
            w *= br(k-1)
        tot += w * sp.prod([e[k] for k in c])
    X_comp.append(sp.expand(tot))

X_Re = [sp.Integer(1)]
for n in range(1, N+1):
    X_Re.append(sp.expand(e[n] + q*sum(br(k-1)*e[k]*X_Re[n-k] for k in range(2, n+1))))

# geometric expansion of AP Thm 38's statement, truncated in z at each step
F = sum(e[i]*z**i for i in range(N+1)).subs(e[0], 1)
D = q*sum(br(i-1)*e[i]*z**i for i in range(2, N+1))
def trunc(p):
    p = sp.expand(p)
    return sum(p.coeff(z, k)*z**k for k in range(N+1))
geo, Dj = sp.Integer(0), sp.Integer(1)
for j in range(N+1):
    geo = trunc(geo + F*Dj)
    Dj = trunc(Dj*D)
X_geo = [sp.expand(sp.expand(geo).coeff(z, n)) for n in range(N+1)]

print(" n | #compositions | compositional == (Re) | compositional == [z^n] F*sum_j D^j")
for n in range(N+1):
    a = sp.expand(X_comp[n]-X_Re[n]) == 0
    b = sp.expand(X_comp[n]-X_geo[n]) == 0
    print(" %d |      %3d      |         %-5s         |        %-5s"
          % (n, len(comps(n)) if n else 1, a, b))
