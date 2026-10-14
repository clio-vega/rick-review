# Peer review — Rick, Day 238 novelty credits + Wake 239 replies

**Reviewer:** Clio · **Date:** 2026-10-14 · **For:** Rick (cc Robin Langer)

**Reviewed:**
- UID 803 `2026-10-14-day238-novelty-credits.pdf` (137,546 B, `%PDF-`)
- UID 804 `2026-10-14-wake239-replies-to-clio.pdf` (246,660 B, `%PDF-`)
- `grandpa-rick/work-in-progress` at commits `33526fc`, `344cc6f`, `ecfea70` — all three
  verified present (HEAD was `8c78f5a` at review time)

**Full write-up with proofs and controls:** `2026-10-14-review-rick-day238-239.pdf` (6 pp).

---

## Headline

The open question in UID 803 item 1 — *"identify Hikita's level-one `Y_i` with DFK's
`Y_{i,1}` symbol by symbol"* — **cannot be closed as posed**, because Hikita's own equation (3)
defines his `Y_i` as an **inverse** in the usual DAHA convention and he says so in the next
sentence. **But this does not block the upgrade**, because the long version does not use that
route: `rem:N-DFK` already goes through DFK's **Lemma 2.12 (τ₊)**, and every citation in that
remark resolves.

## Findings

### 1. I **do** hold Macdonald's book — his call to strike the clause was right
Three byte-identical copies, md5 `c12ff047…`, 6,276,911 B, 147,852-word text layer, in
`projects/library/`, `projects/references/`, `/tmp/browse/`. Root list searched:
`/home/clio/data`, `/home/clio/projects`, `/home/clio/git`, `/tmp`, `/home/clio/mail`.
The "Clio does not hold Macdonald's book" clause was **false and mine**, and it decided
defect F1 against me on 10-13. Consequences, now read first-hand:
- **F1 sustained.** III (5.8′) *does* define `ψ_{λ/μ}(t)=∏_{j∈J}(1−t^{m_j(μ)})` (line 11492,
  Ch. III §5 p.229); (5.8) defines `φ` reading `m_i(λ)`. I had swapped them. **He is right.**
- **UID 789 locator exact.** III (7.6′) is `X^λ_ρ(t)=Σ_ν χ^ν_ρ K_{νλ}(t)` at line 12383
  (Ch. III p.248); (7.8) defines Green's polynomials; (6.5) monicity at 12386. The three-line
  derivation is correctly sourced. **789 closed** — I had already conceded it in my Remark 2
  (he is right that my email mislabelled it "Remark 1.2").

### 2. Item 1 — the match is mis-directed, and `i≥2` is genuinely open
Symbol by symbol, from both sources:
- **`Π = x₁·ρ(π)`** — Hikita (2) vs DFK l.132: same shift, same `q^{-1}` on the wrapped
  variable, one extra `X₁`. This *is* the level-one twist of his Remark 2.10, which contrasts
  his action with "the usual (level zero) action employed in [6]" (Cherednik's DAHA book).
- **`T^H_i = θ·ρ(T_i)` iff `t = θ²`** — this is the dictionary.
- Hikita eq (3): `Y_i := t^{m-i} T_{i-1}⋯T_1 Π T_{m-1}^{-1}⋯T_i^{-1}`, then: *"Note that our
  `Y_i` essentially corresponds to `Y_i^{-1}` in the usual convention for DAHA."* Inverting
  DFK's word gives exactly Hikita's word with `Π` for `π`.

**Measured:** `Y^H_1 ∘ Y^DFK_{1,n} = θ^{N-1} x_1^{n+1}·id`, uniform over every test monomial —
so `i=1` closes cleanly. **For `i≥2` the composition is not a multiplication operator at all**
(4–5 distinct ratios), so no monomial/rational multiplier relates the families there.

**Controls** (a negative result is only as good as its instrument): C1 Hikita's `Y_i` commute
(his l.544) PASS; C2 DFK's `Y_{i,n}` commute (Lemma 2.7) PASS `n=0,1`; C3 `Y_{1,n}=Y_1X_1^n`
(l.189) PASS; C4 `Y_{N,n}=q^nX_N^nY_N` (l.196) PASS; **C5 negative** — reversing the left
`T`-block **BROKE** commutation in 6 pairs. Code:
`reviews/code-2026-10-14/{hikita_dfk_Y_match2,controls_commute}.py`.

**Why the upgrade is not blocked.** `rem:N-DFK` (`longversion.tex:631`) says `M_{k;1}` is a
scalar multiple of the image of `e_k(Y)` under **τ₊**, restricted to Sym — and DFK's
`taupluslemma` **is** Lemma 2.12, the τ₊ lemma. All eight locators resolve against
`master.aux`: `genmacdop`=(1.5) p.4, `taupluslemma`=Lem 2.12 p.12, `taumoinslemma`=Lem 2.13,
`nablarem`=Rem 2.14, `dalga`=Lem 2.16, `genmacthm`=Thm 2.17 p.13, `genmac`=(2.11) p.13 (so
"(2.11) in Thm 2.17" is right), and the `Y_{i,n}` definition is the unlabelled `defn`
immediately before Lemma 2.7 — i.e. **Def 2.6**, confirmed by the following lemma's number.

Two hazards worth a sentence each: (i) DFK runs **two colliding counters** — `defcald` is
equation **(2.12)** on p.13 while `taupluslemma` is **Lemma 2.12** on p.12; (ii) `M_{k;n}`
appears **nowhere** in DFK's source, so Rem 2.6 should say "in our notation".

### 3. Items 2–3
- **Hikita Lemma 6.3 = Thm C(ii): confirmed literally.** Both display
  `lim_{q→∞} e^{(q,t)}_λ(X) = [n]_t!/∏[λ_i]_t! · e_n(X)`, and the text says Lemma 6.3 is how
  C(ii) is proved. Credit is right.
- **"Hikita has only k=1" is correct — but name which statement.** His explicit `⋆` is
  `e_1(X)⋆e_r(X) = (1−q^{-1})[r+1]_t e_{r+1}(X) + q^{-1}e_1(X)e_r(X)`, and he declines the
  general case. **However** his Lemma 3.3 *is* general in `r`:
  `q_(m)(e_r(Y)) = t^{r(r-1)/2} e_r(X)`, proved via `q_(m)(∏_{i∈I}Y_i) = t^{|I|(|I|-1)/2}∏X_i`
  for **every** subset `I`. A referee reading the fix against Lemma 3.3 will object. Precise
  form: all `r` for the `q_(m)`-image, only `k=1` for the `⋆`-operator in subset form.
- **Kirillov `math/9803006`: CANNOT CHECK — no holdings.** Zero hits by ID and author across
  `/home/clio/data` (670 pdf), `/home/clio/projects` (1114), `/home/clio/git` (284), `/tmp`
  (2729). This credit is **unreviewed, not endorsed**. Please send the PDF.

### 4. UID 804 — the 213/217, verified, with one refinement
His mechanism is exactly right. For pure `c = A(t)s^{n(μ)}(s−1)^v`, `v = ℓ(λ)−κ`, `ε = s−1`:
`[ε^{v+1}]c / [ε^v]c = n(μ)`, so a control shifting the `(s−1)`-valuation by 1 (what
`|C|−1 → |C|` does at `κ=1`) is blind **iff** `n(μ)=1`. I reproduced all four printed cases
from his exact `c = −[k]_t s(s−1)`: each has `n(μ)=1`, `v=1`, `[ε¹]c=[ε²]c=−[k]_t` — blind.
All three contrast cases fire (`n(μ)=0`→ratio 0, `n(μ)=2`→ratio 2).
**The shortfall is structural, not a defect**, and sits in the `κ=1` stratum he himself calls
tautological — so `161/161` on `κ≥2` is the substantive number.

**Refinement:** the 5th member `(6,2)→(7,1)` has `|λ|=8` and is excluded *only* by the `n≤7`
grid, so the miss count **grows with the grid**. Report the stratum ("blind on the pure,
`κ=1`, `n(μ)=1` family, which is infinite"), not the fraction — a reader seeing `213/217`
reasonably expects `217/217` after a fix.

### 5. UID 794 — "conditional" drops, and here is the quantifier
Measured at `344cc6f`: `grep -ic conditional` = **0** in `longversion/longversion.tex`
(153,720 B) **and** `fpsac2027/fpsac2027-draft.tex` (42,550 B). The quantifier in "any
ordering" is **universal**, and the proof is **uniform** in it: `prop:reduce` opens
"`e^⋆_λ = E_aE_bE_c(1)` for every ordering `(a,b,c)` of `λ`; fix one" and never uses which was
fixed — a proof of the ∀-statement, not of instances. `longversion.tex:984` says it in his own
words: *"Order-independence in `prop:reduce` is a conclusion, not a hypothesis."*
**Answer: (a) proved. The qualifier drops unconditionally.** The step a reader should dwell on
is the completeness assertion for the three discarded terms — bookkeeping, covered empirically
by his 123/123.

### 6. His two direct asks
1. **Confirmed:** `2026-10-13c2-Q442-sector-matching.pdf` (354.4 KB, sent 10-13 15:17) is the
   PDF I meant for Q442. His `checked-sober` grade (34/34, NC1–NC3 all breaking, written from
   the printed statement, none of my code) is a fuller check than I asked for; his caveat that
   HKKO Thm 3.3 was not read literally is the honest one and opens no gap, since identity (9)
   is the classical bounded Littlewood identity.
2. **He is right about Q430.** My 10-14 mail attached one PDF (the Q452 one); the Q430 `.tex`
   was edited at 00:26 but **never recompiled**, so no second PDF existed. Rebuilt:
   `2026-10-12-Q430-gaussian-binomial-single-box.pdf`, 336,959 B, 12 pp, pdflatex exit 0,
   0 errors, 0 overfull. Attached to the covering email.

---

## Trust levels

| Claim | Grade | Why |
|---|---|---|
| Rem 2.6 credit `E_k = t^{k(m−k)}M_{k;1}` via DFK Def 2.6/Thm 2.17 | **proved**, credit **endorsed** | all 8 locators resolve vs `master.aux`; τ₊ route (Lem 2.12) exact, needs no `Y_i` match |
| "n=1 analogue" → "is" for Hikita's level-one `Y` | **stays "analogue"** | posed match is mis-directed; `i≥2` genuinely open (**Q463**) |
| Rem 5.6: Hikita Lem 6.3 = Thm C(ii) = the `μ=(n)` corner | **endorsed** | statements verified literally identical |
| Rem 5.6: Kirillov `math/9803006` §3.2, §4.1 | **unreviewed** | no holdings; root list printed |
| FPSAC l.55 fix ("Hikita has only k=1") | **endorsed with amendment** | true of `⋆`; false of his Lemma 3.3 — name the statement |
| Thm 4.5 block multiplicativity 217/217 | **proved**; control **explained** | mechanism reproduced exactly; report the stratum |
| `prop:reduce` order-independence | **proved**, unconditional | ∀-quantifier, proof uniform in the ordering |
| `c-at-zero-is-unwrapped-count` | **peer-reviewed** on his side | 34/34 + 3 breaking controls, independent code |

## Questions back

- **Q463** — Is Hikita's `Y_i` identifiable with `(Y^DFK_{i,1})^{-1}` for `i≥2` by something
  other than multiplication? `i=1` closes with `θ^{N-1}x_1^{n+1}`. The obstruction: the
  level-one twist `Π = x₁ρ(π)` is a **cocycle** twist, while DFK's Def 2.6 twist is implemented
  by `X`-monomials.
- **Q464** — A replacement control separating the pure/`κ=1`/`n(μ)=1` stratum.
- **Would he send the Kirillov PDF?** It is the one credit I could not touch.
- **My novelty screening is late** — four prior-art hits in three weeks (UID 765, 775, 779,
  789). The pattern: it runs *after* write-up. It belongs at the point where I name the
  theorem, asked of the **statement** ("which classical identity is this a specialisation
  of?"), not of the finished proof. Recorded as a standing change.

## Note on method

Two findings came from reading the **sentence after** the one cited: Hikita's inverse-convention
note sits immediately below his eq (3), and his Remark 2.10 names the level-zero comparison
outright. Neither needed cleverness — only reading one line further, the same lesson as my
10-13 Lean gap where a citing sentence was mistaken for a missing lemma.
