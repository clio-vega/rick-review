"""THE POSITIVE CONTROL the brief demands: reproduce Rick's integer zero window on BOTH
LG and OG with my own engine, over a domain that INCLUDES the OG side and reaches past
his m<=4 ceiling (his check.py/mono.py were killed at m=5).

Theorem I:  s_j(kappa) := (-1)^{|kappa|} H_kappa(-j) satisfies
            0 = s_1 = ... = s_W < s_{W+1} <= s_{W+2} <= ...,  W = ceil(r/2) on LG, r on OG.
Engines: my type-C and type-B Demazure, evaluated DIRECTLY at negative weights (licensed
by Rick's Lemma P; control in direct.py: 0/522 mismatches vs interpolation).
"""
import sys, time
import demazure as C, demazureB as B
from fast import strict_partitions

def r_of(kappa):
    return max((k + 2*(i+1) - 2 for i, k in enumerate(kappa)), default=0)
def W_LG(k): return -(-r_of(k)//2)
def W_OG(k): return r_of(k)

def word_of(kappa, m):
    return C.reduced_word(C.min_rep(sorted(C.subset_of_kappa(kappa, m)), m), m)

def run(m, extra=5):
    ks = strict_partitions(m)
    rows = []
    for typ, chi_fn, Wf in (("LG", lambda wd, j: C.chi(wd, (j,)*m, m), W_LG),
                            ("OG", lambda wd, j: B.chiB(wd, (j,)*m, m), W_OG)):
        nz_ok = van_ok = mono_ok = 0
        nz_bad = van_bad = mono_bad = 0
        bad_examples = []
        for kap in ks:
            wd = word_of(kap, m); sgn = (-1)**sum(kap); W = Wf(kap)
            JM = W + extra
            s = [None] + [sgn*chi_fn(wd, -j) for j in range(1, JM+1)]
            # vanishing half: s_j == 0 for 1 <= j <= W
            for j in range(1, W+1):
                if s[j] == 0: van_ok += 1
                else:
                    van_bad += 1
                    if len(bad_examples)<5: bad_examples.append(("VAN",kap,j,s[j]))
            # strict step + positivity beyond the window
            for j in range(W+1, JM+1):
                if s[j] > 0: nz_ok += 1
                else:
                    nz_bad += 1
                    if len(bad_examples)<5: bad_examples.append(("NZ",kap,j,s[j]))
            # monotone nondecreasing on j >= 1
            for j in range(1, JM):
                if s[j+1] >= s[j]: mono_ok += 1
                else:
                    mono_bad += 1
                    if len(bad_examples)<5: bad_examples.append(("MONO",kap,j,s[j],s[j+1]))
        rows.append((typ, len(ks), van_ok, van_bad, nz_ok, nz_bad, mono_ok, mono_bad, bad_examples))
    return rows

if __name__ == "__main__":
    MM = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    print(f"== THEOREM I window, independent engine, m <= {MM}, {5} points past the window ==")
    for m in range(1, MM+1):
        t0 = time.time()
        for (typ, nk, vo, vb, no, nb, mo, mb, ex) in run(m):
            print(f"  m={m} {typ}: {nk} kappa | vanishing 0=s_1..s_W: {vo}/{vo+vb}"
                  f" | strict/positive past W: {no}/{no+nb} | monotone: {mo}/{mo+mb}"
                  f" | {'OK' if vb+nb+mb==0 else 'FAILURES '+repr(ex)}")
        print(f"      ({time.time()-t0:.1f}s)")

def negctl(m):
    """Two-arm negative control: shift the predicted window by +-1 and confirm the SAME
    test fires.  Without this, 'window OK' is just my engine agreeing with itself."""
    ks = strict_partitions(m); out = []
    for typ, chi_fn, Wf in (("LG", lambda wd,j: C.chi(wd,(j,)*m,m), W_LG),
                            ("OG", lambda wd,j: B.chiB(wd,(j,)*m,m), W_OG)):
        for shift in (-1, +1):
            van_bad = nz_bad = 0
            for kap in ks:
                if not kap: continue
                wd = word_of(kap, m); sgn = (-1)**sum(kap)
                W = Wf(kap) + shift
                if W < 0: continue
                JM = W + 3
                s = [None] + [sgn*chi_fn(wd, -j) for j in range(1, JM+1)]
                for j in range(1, W+1):
                    if s[j] != 0: van_bad += 1
                for j in range(W+1, JM+1):
                    if s[j] <= 0: nz_bad += 1
            out.append((typ, shift, van_bad, nz_bad))
    return out
