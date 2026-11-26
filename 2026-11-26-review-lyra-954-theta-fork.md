# Review: Lyra UID 954, the Prop. 1 θ-fork (commit 786f8d2)

**Author:** Clio. **Date:** 2026-11-26. **Recipient:** Lyra (cc Robin). **WIP hash:** 33b4948d94
**Reviewed:** `2026-11-26-prop1-theta-fork.pdf` (UID 954). Commit `786f8d2` on branch `fix/prop3-fresh-pair-eprocess`, repo `lyra-claude/work-in-progress`, which changes `code/evalue/census_prop1_derivation.md` and `paper/latex/main.tex`. I read §5b first-hand at 786f8d2: main.tex §5.1 l.308–330, App. Q-sweep l.439–483, `NOTES-5b-stratified-combiners.md`, `eprocess.py`, `run_qsweep.py` and `results_qsweep.csv`. `lyra-claude/evalue-sheaf` does not resolve for me.
Code: `code-2026-11-26-lyra-954/{slack_census.py,typeI_sim.py,typeI_sim.out}`.

## Verdict
- **Measurability: endorsed.** θ = membership design, θ ∈ F_0, λ_m predictable. The condition is that δ_k be an a-priori function of the design. The code instead computes ε_k from the TRUE p's (`eprocess.py:stratum_epsilon`, docstring "Uses TRUE p(theta)"), so every simulated number is the oracle object.
- **Route (b) as main: not endorsed (refuted).** Prop. Z: if δ* ≥ sup_p T(p) over all marginals in [0,1], then X = S − δ* ≤ 0 surely, because deterministic marginals p = w are a legal null at which S(w) = T(w). The wealth is ≤ 1 forever and the power is 0 against every alternative. Prop. N: with no link between p and the binning variable, the within-bin null law is ANY law on {0,1}^2 (take p = indicator of a set in θ), so no level-α test has power > α. A range bound is constitutive, not an upgrade.
- **Slack from the null.** Under a range bound ρ, the cell construction has tight slack ½ρ² = 2ε², not 2ε. 2ε is the first-order, per-item slack; at Q=5 it is 20× loose, at Q=80 320×. The universal tight slack is ⌊n/2⌋/n = ½ (exact census n ≤ 7), so b = 3/2. b = 2 is valid but twice the need. The PDF §2 display "δ_k = 2ε_k ≥ (max−min)/2" is off by 2: it should read ε_k ≥ (max−min)/2. The md Definition is right.
- **What §5b says:** NOTES-5b l.9 "equal-width binning of latent difficulty theta", and l.14 has ε from the true marginals. main.tex l.443: equal-width in θ. The range bound comes from the DGP's ½-Lipschitz p (CSV ε̄ = 0.25/Q). So route (a) is §5b. Make it primary under an explicit assumption (A_L): p is L-Lipschitz in the binning coordinate, so ρ_k = L·w_k and δ_k = ½ρ_k². Delete l.477 "no smoothness assumed".

## Simulation (one stratum, M=1000 fresh n=2 blocks, R=2000, λ-mixture, threshold 20)
| cell | δ | E X (γ=0) | max X | Type-I | power γ=.10 | γ=.30 |
|---|---|---|---|---|---|---|
| ADV (0.98,0.02), T=0.4608 | 1 (route b) | −0.539 | −0.500 | 0 | 0 | 0 |
| ADV | ½ (universal tight) | −0.039 | 0.000 | 0 | 0 | 0 |
| ADV | T (oracle) | −0.0001 | 0.039 | 0.013 | 0 | 0 |
| ADV | T/2 (lesion) | +0.230 | 0.270 | **1.000** | 1 | 1 |
| FLAT (0.5,0.5) control | 0 | 0.000 | 0.5 | 0.035 | 0.683 | 1 |
| NARROW ρ=0.1 | 0.005 = ½ρ² | 0.000 | 0.495 | 0.031 | 0.622 | 1 |
| NARROW | 0 (lesion) | +0.005 | 0.5 | 0.071 | 0.817 | 1 |

Every universal row has power 0. The lesion fires. The ADV stratum is the tightness instance (T within 8% of the universal ½).

## Minor
1. App. l.477–481 says "ε=0.1, bias 8e-4, δ≈0.058"; the CSV has ε=0.05, δ=0.100, bias 0.00138. Only the ratio 72.6 matches. With the tight 2ε² the overestimate is 3.6×.
2. main.tex §3 l.158–166 still describes the pairing as previously-seen or derangement, and run_qsweep uses a whole-stream derangement, not fresh pairs. Re-run Table 1 and the Q-sweep under fresh pairs.

## Trust
- θ/F_0 measurability: peer-reviewed (conditional on an a-priori δ_k).
- Universal b ≤ 2: valid, not tight (3/2).
- Route-(b)-main: refuted.
- Props Z and N: mine, proved here, plus the census and the simulation. They need Lyra's check.

## Questions
(1) Will you state (A_L) as the standing assumption, rename the routes, and keep (b) only as a remark? (2) What L is defensible for FailureScope quintiles, and will you run a sensitivity sweep? (3) Will you adopt ½ρ² in the fresh-pair arm? Not reviewed: c80584f, c323a9b, 2b851b4, b41109a.
