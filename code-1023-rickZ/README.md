# Code for the 2026-10-24 review of Rick's Theorem Z

Written from Rick's **definitions** (`proofs/2026-10-24-Z-by-hyperplane-induction.md` §§1–3), not
from his scripts. Pure Python + stdlib `fractions`; no SageMath (not installed in this container).

| file | what it checks | domain |
|---|---|---|
| `comb.py` | eq. (1.1); **Lemma S**; `R` preserves strictly-SE pairs; **Lemma Ch** drop bound; admissible-pair census | `m ≤ 8` |
| `comb2.py` | Lemma Ch core claim (longest chain in `θ` ≤ 2) + **positive control**: the weaker "no `2×2` square" predicate breaks it | `m ≤ 8` |
| `demazure.py` | `C_m` root system, minimal coset reps, reduced words, Demazure operators, `H_κ(j)`; **4 engine validations** incl. Demazure vs. Weyl dimension formula | `m ≤ 4` |
| `testZ.py` | the **anchor**, **Theorem Z's conclusion**, **sharpness**, and the **Step-1 identity** `b_κ = Σ c_ρ H_ρ` with `c_ρ` from BR Cor 5.6 | `m ≤ 4` |
| `control3.py` | **negative controls A/B/C** on the Step-1 identity; the multiplicity-2 census | `m ≤ 3` (A/B), `m ≤ 4` (census) |
| `supp.py` | closed form `c_ρ = (−1)^{|θ|−1}2^{f}` for the `p=1` K-Pieri coefficients | `m ≤ 7`, 3025 rims |
| `worked.py` | reproduces his §4 worked example sign row `+000+++` | `κ=(4,3,2,1)` |
| `ex.py` | his `κ=(2,1), ρ=(1)` diagonal-domino witness, in both indexings | `m = 2` |
| `q30.py` | **Q30**: `|c_ρ|` vs. strict `{even<odd}` fillings, all four indexing/diagonal conventions | `m ≤ 7`, 6918 pairs |
| `evidence.py` | the `r′` / window / `H_κ(−M/2)` evidence table | `m = 3,4` |

Run from this directory: `python3 testZ.py 4`, `python3 comb2.py`, `python3 supp.py`, etc.

**Not reached:** `m = 5` was started and killed — the near-full-staircase `κ` need `h⁰(X_κ, O(14))`,
beyond this dict-based character representation. The corroboration domain is honestly `m ≤ 4`.
