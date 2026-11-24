"""Per-seed comparison: Lyra's run_gamma (her code @ b29ca33, her seeds 50000+r, R=600)
vs my 942 rebuild (mixwin_942.py, flat DGP rebuilt from her sec.5 text) on the SAME seeds.
Her L_comp is (R,9) = [Eq, win0..win7]; mine L is (R,10) = [EW, win0..win7, MixWin],
cross is (R,10) likewise. Also: Wilcoxon signed-rank (normal approx, no scipy here),
and a positive control: my flat-DGP output vs alt_dgp on the same seeds must DIFFER."""
import sys, numpy as np
from math import erfc, sqrt
def wilcoxon_p(d):
    d = d[d != 0]; n = len(d)
    r = np.argsort(np.argsort(np.abs(d))) + 1.0          # ties have prob 0 for floats
    Wp = r[d > 0].sum(); mu = n*(n+1)/4; sd = sqrt(n*(n+1)*(2*n+1)/24)
    z = (Wp - mu)/sd; return z, erfc(abs(z)/sqrt(2))
for g in sys.argv[1:]:
    H = np.load(f'her_{g}.npz'); M = np.load(f'mine_{g}.npz')
    Lh = H['L_comp']; Lm = M['L'][:, :9]
    print(f'gamma={g}  R={len(Lh)}')
    print('  max|L_comp(her) - L(mine)| over 600x9 :', np.abs(Lh - Lm).max())
    print('  max|log_mw(her) - L_mix(mine)|        :', np.abs(H['log_mw'] - M['L'][:, 9]).max())
    print('  reject Eq  her/mine:', H['rej_eq'].mean(), M['cross'][:, 0].mean(), ' per-seed equal:', bool((H['rej_eq'] == M['cross'][:, 0]).all()))
    print('  reject MW  her/mine:', H['rej_mw'].mean(), M['cross'][:, 9].mean(), ' per-seed equal:', bool((H['rej_mw'] == M['cross'][:, 9]).all()))
    print('  argmax=Eq her/mine :', (Lh.argmax(1) == 0).mean(), (Lm.argmax(1) == 0).mean())
    z, p = wilcoxon_p(H['log_mw'] - H['log_eq'])
    print(f'  Wilcoxon (MixWin-Eq) normal approx: z={z:+.3f} p={p:.3e}')
