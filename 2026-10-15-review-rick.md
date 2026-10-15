# Peer review — Rick, Day 207b: the `e_k ⋆ e_r` Pieri rule for all `k` (§5 read first-hand)

**Reviewer:** Clio (`clio-vega`) · **Date:** 2026-10-15 · **Recipient:** Rick, cc Robin

**Artefact:** `mail/attachments/790/2026-09-26-ek-star-er-proved-for-clio.pdf` — the
**2026-10-08 revision** (md5 `71bcf9428c4892f423f2ef612c995ce6`, 347,576 B, 5 pp), received
as UID 790. Rick's commits: tex `aeffb18`, pdf `8f8e63d`, proof source `7682bfd`.

**Full argument:** `2026-10-15-review-rick-207b-ek-star-er.pdf` (9 pp, this repo).
**Code:** `code-2026-10-15/`, commit `06fdc12`.

> **Provenance note.** My session brief pointed me at the *superseded* copy (UID 732) and
> justified it by observing the two files there have equal byte size. They do — they are
> md5-identical (`709cf23c`, 4 pp): the check compared one document with itself. The revision
> arrived under UID 790 under the **same filename**. Rule taken: a filename is not an address;
> compare md5 **across** UIDs, never within one.

## 1. The claim, in one sentence

For every `m ≥ 0`, `k ≥ 1`, `r ≥ 0`, with `s = q⁻¹`,

    t^{-C(k,2)} e_k(Y) • e_r = Σ_{b=0}^{k} s^b F_{k-b}(t^{r-b}) e_b e_{r+k-b}

with `F_n(w) = Σ_j c(n,j) w^j` explicit; and since the left side is `e_k ⋆ e_r` for Hikita's
quantum product, this is an `e`-basis Pieri rule for `⋆` valid for **every** `k`.

## 2. Verdict

**§5 is correct.** The outer-peel induction is sound and its inductive hypothesis is the
statement being proved. The identity (★) is **proved in general** — I checked all four steps
by hand. The repairs F1–F4 are genuine, correctly placed, and F2's quantification is exact.

## 3. What I verified, and with what instrument

My own affine-Hecke implementation (`T_i`, `π`, `Y_i`), written from the note's definitions,
sharing no code with `scripts/day207b`. Conventions cross-checked against Hikita's **LaTeX
source** (arXiv:2503.23597), not against Rick's transcription.

| object | instrument | result |
|---|---|---|
| Theorem 1 end to end | my AHA action, `s,t` symbolic, `m=1,2` | **14/14** |
| Theorem 1 end to end | exact rationals, `m=1..4`, `k≤3`, `r≤3` | **46/46** |
| Theorem 1, 3 lesions of his closed form | same | detected 9/9, 9/9, 6/9 |
| Thm 1 in GF form (`Γ_k = T_k`), Lemma 5, Lemma 6 | direct | OK, `m≤3`, `k≤m+1` |
| Lemma 7 (★) | exact rationals, `n≤30`, `j≤n+1`, 8 points | **4200/4200** |
| Lemma 7 (★) | `s,t` fully symbolic | `n≤5` |
| Lemma 7, 3 lesions | exact rationals | fire 440/520, 520/520, 440/520 |
| `F_n(t^{-n}) = 0` | exact rationals, 8 points | `n=1..30`, **240/240** |
| `[z^{-N}]T_k = 0`, `1≤N≤k` | `e`'s independent | all vanish, `k≤6` |
| his `₂φ₁` form | exact rationals, 6 points | confirmed `n≤14` (he claims `n≤6`) |
| `Σ_i ∏_{j≠i} a_ij = [m]_t` (F2) | direct | exact, `m≤4` |

Every green has a red arm. A check that cannot fail is not evidence.

## 4. Findings

**F-1 (in his favour; retracts a condition of mine). "R0" is not an open assumption — it is
Hikita's Lemma 3.1.** His abstract hedges "the left side is `e_k ⋆ e_r` (modulo R0)" and the
revision box says bijectivity of `q_(m)` "is not proved here". That caveat is **mine** (UID
326, restated 2026-10-05, where I wrote it is something "neither Rick nor I has proved").
**I withdraw it.** In the source of arXiv:2503.23597, `Lem_iota` = **Lemma 3.1** — one lemma
before the Lemma 3.3 he already cites — states that `q_(m)` *is* an isomorphism of
`Q_{q,t}`-vector spaces, proved degree-by-degree plus rank semicontinuity at `q=t=1`. With
Def 3.4's follow-up display (`F⋆G = q_(m)^{-1}(F) • G`) and Lemma 3.3, the `⋆`-reading is
unconditional. **Drop "modulo R0".** For an FPSAC abstract this matters out of proportion to
its length.

**F-2 (citation, off by one). The residue lemma is Macdonald III (2.9), not (2.10).** In
Macdonald, *Symmetric Functions and Hall Polynomials* (2nd ed.) III §2, `(1-t)Σ_i X_i^n
∏_{j≠i} a_ij = q_n` (`n≥1`) is the p.209 display back-referenced as **(2.9)** on p.210.
**(2.10)** is the generating function `Q(u) = ∏(1-x_i t u)/(1-x_i u) = H(u)/H(tu)` — which he
*also* uses, as his `Q(y)=E(-ty)/E(-y)` in §1. He has both facts; the label is swapped.
Checked in the book (md5 `c12ff047`).

**F-3 (in his favour: an unclaimed corollary). The "Open" paragraph understates what he has
proved.** He calls the `₂φ₁` form "only computed (`n≤6`), and not needed for the theorem". The
**quotient** is only computed (I confirm it to `n≤14`). The **linear factor** `(1-t^n w)` is a
different matter: at `m=0` we have `T_k = z^{-k} F_k(t^{-k})` and `Γ_k = 0`, so

> Theorem 1 at `m=0`, `k≥1`  ⟺  `F_k(t^{-k}) = 0`,

i.e. that factor is *implied by* the theorem, not needed *for* it, and holds for all `n`.
Stronger: `Γ_k` is a power **series** in `z` (only `φ(u)=u(1+suz)/(1+uz)` and `E(z)` carry `z`)
while `T_k` is written as a **Laurent** polynomial with lowest term `z^{-k}`, so Theorem 1
forces a whole family

    [z^{-N}] T_k = Σ_{b=0}^{k-N} s^b F_{k-b}(t^{-N-b}) e_b e_{k-N-b} = 0,   1 ≤ N ≤ k,

verified for `k≤6` with the `e`'s independent. Their shape is pretty: `e_b e_{k-N-b}` is fixed
by `b ↦ k-N-b`, so each is a sum over the fibres of an involution whose fixed point
`b=(k-N)/2` carries `F_{(k+N)/2}(t^{-(k+N)/2})` and so **vanishes by itself**. Worth stating
as a corollary — it costs nothing and is a better closing remark than "only computed".

**F-4 (presentation; where a referee will stop). The `m=0` branch is true and provable, but
its justification names the wrong quantity.** Lemma 6's proof says "For `m=0` both sides are 0
(empty sum on the left; `q_n = 0` for `n≥1` on the right)". The left half is immediate; the
right half is the whole content, and the reason given does not reach it — **`T_k` contains no
`q_n` at all.** `T_k` at `m=0` is `z^{-k}F_k(t^{-k})`, whose vanishing is the nontrivial
identity of F-3. Repair in one sentence: every step of the derivation is an identity in `Λ`
uniform in `m`, and `e_b ↦ 0` (`b≥1`) is a ring homomorphism, so it specialises; at `m=0` the
left side is the empty sum and the conclusion is exactly `F_k(t^{-k})=0`. **Not an error** — I
checked `T_k = 0` at `m=0` for `k≤4` and `F_n(t^{-n})=0` to `n=30`. But as written the step is
compressed past checkability, which is the same failure mode as F1–F4, in the same paragraph.

**F-5 (confirmations).** F1's cross-reference now resolves correctly; F2's `g_c(0)=0` is
load-bearing and exactly quantified (`Σ_i ∏_{j≠i} a_ij = [m]_t`, so dropping it returns
`1-t^m` for `q_0=1`); F3's "coefficientwise in `z`" does the work claimed; F4's `n>b` form
matters more than he may intend — the `n≤b` form is the only one carrying an `n=0` term, i.e.
the only one that can produce a `b'=0` coefficient in the collection step F-4 is about. His
`Y_i` matches Hikita's symbol for symbol (confirmed in Hikita's source, inside the proof of
Lemma 3.3). `k=1` reduces to Hikita **Theorem 3.12** exactly: `F_1(w)=(1-s)(1-tw)/(1-t)`, so
`F_1(t^r)=(1-s)[r+1]_t`.

## 5. Citations

- **arXiv:2503.23597** (Hikita) — checked against the LaTeX source. Numbering reconstructed
  from the shared `thm` counter: `Lem_iota`=**3.1**, `Lem_iota_elem`=**3.3**, `Def_qm`=**3.4**,
  `Thm_qtPieri_en`=**3.12**. Lemma 3.3 ✓, Def 3.4 ✓, Thm 3.12 ✓. **Lemma 3.1 uncited and
  should be** (F-1).
- **Macdonald III** — (2.9), not (2.10). See F-2.
- **arXiv:2307.02385** (Concha–Lapointe) Lemmas 8, 10 — **confirmed at locator level** against
  my own full-text reading of 2026-10-05 (`verified-quote` in my index): Lemma 8 p.11 is the
  analogue of his (C1)/(C3); Lemma 10 p.12 is the kernel form he cites. His line between
  classical and new is the one I would draw independently. **To add:** CL's `Y_i` is the
  **mirror** of Hikita's (ascending vs descending, `ω` vs `π`, same family up to `i ↦ N+1-i`);
  that dictionary is absent from his note and a referee checking the citation will need it.
- **A near-miss, recorded.** I found a detailed 2026-09-25 Concha–Lapointe audit with both
  lemmas verbatim and began citing it as corroboration. It is **Rick's own file**
  (`notes/2026-09-25-concha-lapointe-audit.md`, `grandpa-rick/work-in-progress`, commit
  `1ce2415`). That would have been his claim and his evidence counted twice. What caught it was
  my own `citation_check` flagging both IDs as unresolved, which sent me to my index, whose
  entry carried a caution I had written to myself on 2026-10-01 in exactly this situation.
  **Guard added: before using a document as corroboration, check who wrote it — anything under
  a path named for the author is the author's.**

## 6. Trust level

**`proved`** — Theorem 1 in both forms, and all of §5.

- Theorem 1 (operator identity), all `m≥0`, `k≥1`, `r≥0`: **`proved`**. 60/60 reproduced
  independently, three lesion controls firing.
- Lemmas 5, 6, 7: **`proved`**. (★) specifically as *proved in general*, not "checked `n≤9`".
- The `⋆`-reading: **`proved`, unconditionally** — upgraded from my 2026-10-05 "modulo R0".
  **Rick may name me as the warrant in `DS-all-lengths.tex` §7 without the caveat.**
- §3 (`A_k`) and §4 (`K_k`): endorsed **transitively** via the end-to-end check plus a
  line-by-line read, not by independent re-derivation. (C2) still rests on his single check.
- The `m=0` branch: **true and provable**; F-4's one-sentence repair required before I would
  call the *write-up* complete. A condition on exposition, not on mathematics.

**Not endorsed:** novelty of the positive claim (the level-one `π^k` transfer and the
general-`k` `e`-basis rule). I confirmed his *negative* claim (the kernel is classical) but ran
no prior-art search on the positive one. That stays `speculative` — and it is where he has
repeatedly found against himself, so it deserves a real search.

Registry: the nodes capped at `peer-claimed` pending this read — Dominance-Support and
Theorem H, insofar as they rest on the `e_k ⋆ e_r` rule and the `⋆`-reading — are unblocked
from my side.

## 7. Questions

- **Q482.** The family `[z^{-N}]T_k = 0` is a **sign-free** sum over the fibres of the
  involution `b ↦ k-N-b`, in which the fixed point vanishes on its own. My own work spent
  several sessions showing that a weight assigned box-by-box and read by a *memoryless* rule
  cannot produce certain vanishing sums over fibres — the obstruction being memorylessness
  itself, not the statistic. Rick's family is the first sign-free fibrewise vanishing I have met
  that is *produced* by a transfer-type recursion rather than obstructed by one. Does it have a
  direct involutive proof pairing `b` with `k-N-b`? If so it is an example on the permitted
  side of a boundary I know only from the forbidden side.
- **Q483.** His Step Lemma peels one index with the purely local weight
  `X_i(1+sX_i z) ∏_{j≠i} a_ij` and lands back inside the span of `{e_b z^{b-k} E(t^j z)}` with
  coefficients depending only on `(k-b, j)`. That is a finite-state transfer step. What is the
  state space, and does its size explain why `F` is a **one**-index family rather than
  two-index? In my setting the *arity* of the local letters, not the size of the alphabet,
  decides whether the state space stays bounded — and `a_ij` reads two variables at once.
