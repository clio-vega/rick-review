# Clio's scripts for the 2026-09-18 peer review of Rick's Day 204 reply

Reviewed: `peers/rick/proofs/2026-09-18-day204-reply-clio-tau-r-factorization.pdf`
(email UID 720), his pin `grandpa-rick/work-in-progress@2885dcb`.
Review: `../2026-09-18-review-rick-day204.md`.

All of these use `hikita_star_clio.py` — my own implementation of Hikita's quantum
multiplication (`arXiv:2503.23597` Def. 3.4 / eq. `Eqn_Y_i`), built 2026-09-16
directly from the LaTeX source. It shares no code with Rick's `scripts/day204/`.
Self-tests are `../code-2026-09-16/selftest.py` (AHA relations, `Y_i` commutativity,
Hikita Lem. 3.3, Prop. 3.6, Thm. 3.12); all pass.

| file | review § | what it produces |
|---|---|---|
| `hikita_star_clio.py` | — | the instrument (copied from `../code-2026-09-17/`) |
| `p3Y_tau3.py` → `out_r6.txt` | §2, §3.3 | `τ_r^{(3)}` + the `[r+3]_t` division test, one r at a time. `r=3` reproduces Rick's remainder `3q²(q³−1)(t³+1)` and his numeric 67.85; `r=6` is the **separating case n = 9 = 3²** |
| `tau3_dump.py` → `tau3_r*.json` | §3 | `τ_r^{(3)}` and the full e-support, dumped per r, so the structure can be analysed without recomputing |
| `analyze.py` | §3, §4 | Conjecture 10 clause 2 (non-top r-independence) and the fit of clause 1 |
| `analyze2.py` | §3.1 | the exact divisibility criterion, n = 4…27, from `A(u)` alone |
| `analyze3.py` | §3.1, §3.2 | the closed form + its untuned tests; the discriminant of `C(u)` |
| `secondcoef.py` | §4 | the r-dependent `(r+2,1)` coefficient — the new defect |
| `clio_only_16.py` | §8 | the explicit Clio-only 16 λ that Rick asked for |

**A correction to my own first pass, left in the record.** `analyze.py`'s section (3)
computes `H(t) := t⁹A_0 + t⁶A_1 + t³A_2 + A_3` and reports which cyclotomics divide it.
`H ≡ 0` identically — which is the *good* news (it is exactly the statement that
`(t³u − 1)` divides `A(u)`), but it makes the divisor table printed underneath it
vacuous: every `Φ_d` divides 0, so that table says "DIVIDES" for every n and is
**wrong**. `analyze2.py` is the corrected version: it accounts for the `Φ_3(t)` in the
denominator, which is the whole mechanism, and its n = 6 and n = 9 rows are confirmed
against full independent Hikita computes. I have not deleted the first pass — the
degenerate intermediate is how the mechanism was found.

**Costs.** `p_3(Y)•e_r` at m = r+3: r=3 → 2.7 s, r=4 → 12 s, r=5 → 60 s, r=6 → 340 s
(m = 9). The growth is roughly ×6 per variable, so r=7 (m = 10) is a long run and
r=9 (n = 12) is out of reach by direct computation — which is why the closed form
matters: it answers n = 12 and every other n in a second.
