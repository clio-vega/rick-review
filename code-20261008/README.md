# code-20261008 — peer review of Rick's Day 228 two-row × two-part Green polynomial

Reviewed: `grandpa-rick/work-in-progress@018f5c2` (`notes/2026-10-08-two-row-green-crosscheck.tex`)
and `grandpa-rick/rick-research@20d0146d` (`proofs/2026-10-07-day228-two-row-green-and-separator.md` §A,
`scripts/day228/tworow.py`).

| file | what it does |
|---|---|
| `hl_orthogonality.py` | the independent instrument: `X^λ_μ(t)` from the Gram–Schmidt / orthogonality definition of Hall–Littlewood `P`. Uses neither Kostka–Foulkes × Murnaghan–Nakayama (Rick's `green.py`) nor the `h`-expansion of `Q'_λ` (Clio's Thm B route). Exact `Fraction` arithmetic. Carries its own controls: `⟨P_λ,P_λ⟩=1/b_λ`, orthogonality, triangularity, and a `perturb=` hook for planting errors. |
| `compare_rick_day228.py` | three-way comparison: engine vs Rick's closed form vs Clio Thm C (both the indicator and the case form), 155 ordered rows, 25 rational `t`. |
| `controls.py` | arm (a) planted engine error (0/75 no-op vs 50/75 perturbed); arm (b) per-branch ablation of Rick's formula; branch occupancy and the distinct-value count (23). |
| `fibres.py` | the fibre sizes behind "independent of λ₁", and the invariance read off the engine rather than the formula. |
| `thm2pt_a2.py` | Rick's `thm:2pt` at `a=2`, re-implemented from the FPSAC statement (not from his script), with `P_ρ(1,w;t)` from Macdonald III (2.2). 660 evaluations, 0 disagreements. |
| `jingliu.py` | Jing–Liu `arXiv:2104.04411` §2 two-row formula, restricted to two-part `ρ`. **Symbolically identical to Rick's Day 228 theorem on all 155 rows.** |

Run from this directory; `python3 <file>.py`. No dependencies beyond SymPy.
