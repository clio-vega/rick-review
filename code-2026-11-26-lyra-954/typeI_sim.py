"""Type-I and power of the fresh-pair cyclic e-process at the universal slacks.

One stratum; each block m is a FRESH pair of items (n=2), cyclic partner = the other
item, X_m = mean_r (U_r - V_r) - delta.  Bet: lambda-mixture over g in {0.1..0.9},
lambda = g / b, b = 1 + delta (so 1 + lambda X >= 0).  Reject when the mixture
wealth reaches 1/alpha = 20 at any m <= M.

Cells:
  ADV  : adversarial within-bin spread, p_i = p_j = (hi, lo) comonotone, hi=0.98, lo=0.02
         (the clipped DGP's extreme values in one bin) -> null drift T = (1/2)(0.96)^2.
  FLAT : flat-spread control, p_i = p_j = (0.5, 0.5): same mean marginal, R = 0, T = 0.
  NARROW: a bin satisfying a range bound, p in (0.55, 0.45) comonotone, T = 0.005.
Alternative: Marshall-Olkin common shock, prob gamma per item both judges fail.
"""
import numpy as np

R, M, ALPHA = 2000, 1000, 0.05
GRID = np.arange(1, 10) / 10.0
CELLS = {"ADV": (0.98, 0.02), "FLAT": (0.5, 0.5), "NARROW": (0.55, 0.45)}

def T_null(hi, lo):
    return 0.5 * (hi * (hi - lo) + lo * (lo - hi))

def simulate(cell, gamma, delta, seed):
    hi, lo = CELLS[cell]
    rng = np.random.default_rng(seed)
    p = np.array([hi, lo])                       # item r=0,1 ; same for both judges
    shock = rng.random((R, M, 2)) < gamma
    Wi = (rng.random((R, M, 2)) < p) | shock
    Wj = (rng.random((R, M, 2)) < p) | shock
    U = (Wi & Wj).astype(float)
    V = (Wi & Wj[:, :, ::-1]).astype(float)      # cyclic partner within the fresh pair
    X = (U - V).mean(axis=2) - delta             # (R, M)
    b = 1.0 + delta
    logw = np.zeros((R, M))
    wealth = np.zeros((R, M))
    for g in GRID:
        f = 1.0 + (g / b) * X
        assert f.min() >= 0.0
        wealth += np.exp(np.cumsum(np.log(np.maximum(f, 1e-300)), axis=1))
    wealth /= len(GRID)
    rej = (wealth.max(axis=1) >= 1.0 / ALPHA).mean()
    return X.mean(), X.max(), rej

seed = 95400000
rows = []
print(f"R={R} runs, M={M} fresh blocks, alpha={ALPHA}")
print(f"{'cell':7}{'gamma':>6}{'delta':>9}{'  analytic T':>12}{'mean X':>10}{'max X':>8}{'reject':>8}")
for cell in CELLS:
    hi, lo = CELLS[cell]
    T = T_null(hi, lo)
    deltas = {"route b (=1)": 1.0, "univ tight 1/2": 0.5, "oracle T": T,
              "half-T lesion": T / 2, "zero": 0.0}
    for gamma in (0.0, 0.10, 0.30):
        for name, d in deltas.items():
            seed += 1
            mx, xmax, rej = simulate(cell, gamma, d, seed)
            print(f"{cell:7}{gamma:6.2f}{d:9.4f}{T:12.4f}{mx:10.4f}{xmax:8.3f}{rej:8.3f}   {name}")
