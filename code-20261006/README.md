# Evidence for the 2026-10-06 peer review of Rick's Theorem H

Pure Python + sympy. **No Sage in this container**, despite `CLAUDE.md` listing it —
a tool named in my own instructions is a prediction about the container, not an
inventory. Pure Python was the better instrument anyway: it reaches the ground truth
by a different mechanism than any symmetric-function library would.

| Script | Establishes |
|---|---|
| `kostka_d_matrix.py` | library: partitions, Kostka, cocharge Kostka–Foulkes (charge via Lascoux–Schützenberger), 0-1 matrix counts |
| `check_controls.py` | **instrument validation, run before any result**: K-F against known values; `K(1) = K` 209/209 for n ≤ 6; perturbed-statistic negative control fires 5/5 |
| `check_corollary.py` | Corollary structural claims, **209/209** n ≤ 6: `N[t]`, no negative exponents, `d(1)=M_{λμ'}`, `d(0)=1` on dominance |
| `rank_neg2.py` | **non-vacuity measured** (n=6: 64 nonzero / 53 nonconstant / 48 distinct / maxdeg 15) + 3 negative controls on the conjugates, all fired |
| `verify_theoremH_identification.py` | **the decisive test: 39/39** against the *actual* Hikita ⋆-product, via `../code-2026-09-16/hikita_star_clio.py` |
| `kirillov_normalization.py` | the four candidate dictionaries; exhibits the n=2 degenerate-boundary trap |
| `kirillov_exact.py` | **the owed normalization check: 87/87**, `d_{λμ}(t) = t^{n(μ')−n(λ')} M(e,P)_{λμ'}(t⁻¹)`; prefactor control fires |
| `verify_thm15.py` / `verify_thm15_control.py` | Rick's Theorem 1.5 **8/8**; control (`[k]→[k+1]`) **0/8** |
| `macdonald_inv.py` | `q→∞` ⇒ HL at `t⁻¹`; inversion symmetry exact; `b(□)` inversion-covariant up to the monomial `t/q` |

## Superseded / abandoned, kept for honesty

- **`check_factorization.py` — abandoned, do not cite.** It was going to verify leg 1
  of the transition factorization (`e_λ = Σ_ν K_{ν'λ} s_ν`) by building Schur
  bialternants in 6 variables. Killed mid-run: the determinants were slow and the
  check turned out to be **redundant**, because leg 1 is exactly the `t=1`
  specialisation of `check_corollary.py`'s `d(1) = M_{λμ'}` test
  (`Σ_ν K_{ν'λ}K_{νμ'} = M_{λμ'}`), which already passes 209/209. Kept in the tree so
  that nobody reconstructs it thinking it was never tried.
- `rank_neg.py` is the first draft of `rank_neg2.py`; it crashes on the Laurent
  polynomials the negative controls produce (`sp.Poly` rejects `t**(-10)`). That crash
  *was* the first sign the controls were firing. `rank_neg2.py` is the one to run.
