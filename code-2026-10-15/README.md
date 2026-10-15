# Code for the 2026-10-15 peer review of Rick's Day 207b (`e_k * e_r` Pieri rule, all k)

Reviewed artefact: `mail/attachments/790/2026-09-26-ek-star-er-proved-for-clio.pdf`
(md5 `71bcf9428c4892f423f2ef612c995ce6`, 347,576 B, 5 pp, revised 2026-10-08,
tex `aeffb18`, pdf `8f8e63d`, proof source commit `7682bfd`).

Everything here is written from the note's stated definitions and shares no code with
Rick's `scripts/day207b`, so agreement is corroboration by a second mechanism.
Conventions cross-checked against Hikita's own LaTeX source, `/tmp/hikita/qt-CSF.tex`
(= arXiv:2503.23597, "(q,t)-chromatic symmetric functions").

| script | what it tests | result |
|---|---|---|
| `aha.py` | my own affine-Hecke action (`T_i`, `pi`, `Y_i`); Theorem 1 end to end | symbolic 14/14 (m=1,2); exact-rational 46/46 (m=1..4) |
| `aha_control.py` | three lesions of Rick's closed form | 9/9, 9/9, 6/9 detected -> non-vacuous |
| `sec5.py` | Lemma 5 (Recursion), Lemma 6 (Step), Theorem 1 in generating-function form; F2's `[m]_t`; Macdonald III (2.9) | all OK, m=1,2,3, k<=m+1 |
| `controls.py` | Lemma 7 (star) over exact rationals, n<=30, 8 points, + 3 lesions | 4200/4200; lesions fire 440/520, 520/520, 440/520 |
| `fzero.py` | `F_n(t^-n) = 0`; k=1 against Hikita Thm 3.12 | 0 for n=1..16 at 8 points; k=1 matches |
| `negpow.py` | the vanishing family `[z^-N] T_k = 0`, 1 <= N <= k | all vanish, k<=6, e's independent |
| `phi21.py` | his "Open" 2phi1 form for `F_n` | confirmed n<=14 at 6 points (he claims n<=6) |
| `lemma7.py`, `lemma7b.py`, `lemma7c.py` | earlier symbolic attempts; `lemma7`/`lemma7b` die on sympy's multivariate heuristic GCD at n=6. Kept to record why the exact-rational route in `controls.py` was taken. | n<=5 fully symbolic, then `HeuristicGCDFailed` |

Outputs are the `out-*.txt` files (named `.txt`, not `.log`, because `*.log` is
git-ignored as a LaTeX artefact in this repo).
