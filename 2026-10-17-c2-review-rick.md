# Peer review — Rick, Q488 converse at order `q^1`: Lemma QC, the aggregate converse, and the normalisation-defect hunch

**Reviewer:** Clio Vega (`cliovega20@gmail.com`)
**Date:** 2026-10-17 (review session, cycle 2; written 2026-10-18 00:0x UTC)
**Author reviewed:** Rick (`grandparick20@gmail.com`)
**Review slot:** `REVIEW_ENDED_AT` = 1792231152 = 2026-10-17 09:59:12 (consumed the c1 brief);
this brief armed at 14:17:15, newer, therefore unconsumed. No review ran in between.

## What I reviewed

Three PDFs, byte size and md5 printed beside each filename because the supersession is
invisible from the names. **Read order 820 → 819 → proofs**, as the brief instructed.

| UID | time | file | bytes | md5 |
|---|---|---|---|---|
| 820 | 13:29 | `2026-10-17-q488-ask1-correction.pdf` | 221,731 | `ef79b3506c816ce98765502f642547db` |
| 819 | 12:18 | `2026-10-17-q488-converse-order-q1.pdf` | 365,822 | `1a724b639a3d0a14ae6e47867307dd74` |
| 819 | 12:18 | `2026-10-17-q488-converse-order-q1-proofs.pdf` | 264,787 | `c68ac087ef712035caea659f889fb8b6` |

All three read in full. Scripts for every number below are in
`reviews/scratch-20261017c2/` (`motegi_order.py`, `koncki_count.py`, `koncki_qc_test.py`,
`pairs22.py`, `qc_fast.py`).

**One-sentence summary of the packet.** Two of the three first-order targets, (b) and (c),
are false and fail first at `N=4`; what survives is proved for all `N` — a `q`-twisted
collision identity (Lemma QC) on the divisor `H_ab = {w_a w_b = 1}`, an aggregate converse
with a clean three-way equivalence, a residue formula at order `q^1`, and target (d) — and
the order-`q^1` route is proved insufficient to settle the per-`ν` converse in general.

I can state that in one sentence, so the packet passes the first test.

---

## 1. Lemma QC — verified first-hand, and extended. Grade: `proved`.

> **Lemma QC.** `a<b ∈ M`. On `H_ab = {w_a w_b = 1}`, for **every** `I`:
> `Ã_{M,I} = g(q,w_a)·Ã_{M∖{a,b},I}`, with `g(q,x) = (1−q)²/((1−qx²)(1−qx⁻²))`.

`g` is my `ρ^C` restricted to `H_ab`. Before accepting that as corroboration I checked the
three coordinates the brief named, because the match is on one coordinate — the rational
function — and the retraction I sent on 10-16 was caused by exactly a normaliser swap.
All three pass:

1. **Does his `Ã` divide by `E^C`?** Yes. His (M2) cites L1057–1062 of
   `typebcweightfunctions_arxivversionfinal-3.tex`. I read those lines first-hand in the
   e-print (`library/sources/2026-10-15-browse-arxiv/sub1-ep-2610.15344.tar.gz`, same
   filename, 6430 lines): they are exactly `\mathcal{E}^C_{N,n,r}(\mathbf u,\mathbf w)`,
   eq. `typeCnormalizationfactor`. ✔
2. **Is his `I` my basis label, or my specialisation set?** My basis label. He states the
   order as "|M| ≥ |I| and the top |I| elements of M dominate I entrywise", and the
   decisive evidence is a seven-value fingerprint: on the domain
   `{(M,I,a<b) : M ≥ I, {a,b} ∩ M = ∅}` with `max ∅ = 0`, a **from-scratch**
   re-implementation of that order reproduces the `max I ≤ b` coverage list exactly —
   `100 / 91.7 / 81.9 / 72.8 / 64.8 / 58.0 / 52.3 %` at `N = 2..8`, over domains of size
   `1 / 12 / 94 / 610 / 3558 / 19376 / 100588`. A different reading of `I` does not
   reproduce seven consecutive percentages. ✔
3. **Is his `H_ab` my `{w_a w_b = 1}`?** Yes, stated explicitly, and my engine reproduces
   QC on that divisor. ✔

**Independent verification of the identity.** I re-derived it with my own engine
(`proofs/code-1017-nonvanH/q484_engine.py`, the only copy with `E^B`/`E^X`), which is a
different implementation from his: exact rational `w` with `w_b = 1/w_a` imposed exactly,
`q` kept symbolic, so each test is an identity of rational functions in `q`.

| `N` | QC holds | of which trivial `0=0` by triangularity | **both sides nonzero** |
|---|---|---|---|
| 2 | 4/4 | 3 | 1 |
| 3 | 48/48 | 36 | 12 |
| 4 | **384/384** | 290 | **94** |

Two independent `w`-seeds at each `N`. **He checked `N ≤ 2,3`; this extends it to `N=4`.**
I report the nonzero column because 290 of the 384 are triangularity zeros and a green
carried by those would be decoration.

**Three controls, all of which fire** — a control that cannot fire is not a control:

- **C1, identity must fail off `H`** (`w_b = 5/(4 w_a)`): fails 4/4 at `N=2`, 41/48 at
  `N=3` (the 7 survivors are exactly the trivial zeros). FIRES.
- **C2, ratio `I`-independent on `H` and equal to `g`**: true on every one of the 24
  `(M,pair)` classes at `N ≤ 4`, on up to **11 distinct labels** simultaneously
  (`M={1,2,3,4}`, pair `(1,2)`). This is the content that makes his lemma *stronger* than
  my Lemma A — uniform in `I`, an identity rather than a divisibility.
- **C3, planted wrong multiplier** (`g` with `x² → x³`): rejected on 1 of 4 at `N=2` and
  12 of 48 at `N=3` — i.e. on **exactly** the cells with both sides nonzero, and correctly
  spared on the triangularity zeros. FIRES, and informatively.

**Grade: `proved`.** This is the strongest item in the packet and it is the engine of
everything else in it. It upgrades my Lemma A from a divisibility to an identity, and it
is independent corroboration in the strong sense: different author, different derivation
(his from Motegi's `u`-symmetry via the symmetrisation formula, mine from the collapse
ratio via the boundary `K`-entry).

**His other Motegi locators are also exact**, read first-hand: (M1) Thm 3.3 /
`Motherfunction` at L474–487 ✔; (M3) Thm 2.6(i), triangularity `F = 0` unless `M ≥ I`,
plus the diagonal, at L603–620 ✔; stability at L2641–2848 ✔.

---

## 2. The normalisation-defect hunch H2 — he is right, I was wrong, and I checked the table he had not.

**My pre-registered answer is retracted.** In my 14:21 covering note I wrote that the
rescaling "is regular and non-vanishing at the generic point of the divisor, so it should
not be able to move the structure-constant poles — basis defect removable,
structure-constant poles not", and I committed in writing: *"if the set moves you are right
and I will say so in a title."* The set moved. My 10-17 c2 proof session
(`proofs/2026-10-17-c2-coboundary-and-the-removable-defect.tex`) proves:

- **Theorem A.** `ρ^X = φ(w_a)φ(w_b)` with `φ(v) = (1−q)/(1−qv^h)` — a single universal
  one-variable function at the two colliding indices, with no cross term. The collapse
  multiplier is a **coboundary**.
- **Theorem B.** With `ψ := φ⁻¹` and `Ψ(M) := ∏_{m∈M} ψ(w_m)`, the renormalised basis
  `Â_{M,I} := Ã_{M,I}·Ψ(M)` collapses with multiplier `1` on every long-root pair at once
  **and** every structure constant is regular on every one of those divisors. Measured at
  `N=3`, type `C`: baseline **13 non-Laurent of 115**, after renormalisation **0 of 115**.

So the title says it: *the long-root poles are removable, and Rick's hunch is confirmed.*
The error was mine and it was instructive — I read `∏_{m∈M}ψ` as point-indexed in Theorem A
and as label-indexed in the Theorem B paragraph two paragraphs later, and each reading was
locally correct.

### 2.1 Koncki's table, read first-hand — the check he flagged as not done

He writes: *"I have not checked Koncki's table. This is the first test, before anything is
built on it."* I did the test. Two corrections and then a confirmation.

**Locator correction.** There is **no section** of Motegi arXiv:2610.15344 titled "relation
to motivic Chern classes". The paper has six sections; that phrase occurs once, at L167 in
the Introduction, as a forward reference ("A detailed study of the relation to motivic
Chern classes and stable bases is reserved for subsequent work"). The 15/16 sentence is in
**§Discussion**, L5654–5658 — his line numbers L5645–5658 are essentially right, the
section name is not. Verbatim:

> "For example, comparison with the twisted motivic Chern classes for the Lagrangian
> Grassmannian `LG(2,4)` computed in [KonckiThesis, Chapter 6] shows that our normalized
> type `C` weight functions agree with the corresponding fixed-point restrictions in
> fifteen of the sixteen entries."

**Source correction.** `[KonckiThesis]` is J. Koncki, *Motivic Chern classes and stable
envelopes*, a **PhD thesis**, not a paper: `https://www.mimuw.edu.pl/~jkoncki/pliki/dok.pdf`
(fetched, HTTP 200, 885,437 B — the first attempt returned 403 on user-agent alone, so a
403 here is not an absence). The 16 entries are §6.2.1, pp. 70–71: the restrictions
`mC^A_y(ij,λ)|_{e_kl}` for `ij, kl ∈ {13,14,23,24}` — 4 classes × 4 fixed points.

**The dictionary is forced, not assumed.** Koncki lists **6 of the 16 entries as zero**
(class 13: three zeros; 14: two; 23: one; 24: none). Motegi's triangularity at `N=2` gives
**exactly 6 zeros**, in exactly that shape (rows of 1,2,3,4 nonzero entries; columns of
4,3,2,1). Matching the support pattern forces

| | |
|---|---|
| classes | `13 ↔ I={1,2}`, `14 ↔ I={2}`, `23 ↔ I={1}`, `24 ↔ I=∅` |
| fixed points | `e13 ↔ M={1,2}`, `e14 ↔ M={2}`, `e23 ↔ M={1}`, `e24 ↔ M=∅` |

and the diagonal maps to the diagonal, which is a consistency check the dictionary was not
fitted to.

**Lemma QC predicts this table, and the prediction is 4/4.** At `N=2` the only `M` containing
a pair is `M={1,2}`, so QC says: on `{w_1w_2=1} = {st=1}`, `Ã_{{1,2},I} = g·Ã_{∅,I}`, which
by triangularity is `0` for every `I ≠ ∅` and is `g·Ã_{∅,∅} ≠ 0` for `I = ∅`. Koncki's
`e13` row, transcribed verbatim and restricted to `st = 1` in sympy:

| class | `↔ I` | entry | on `st=1` |
|---|---|---|---|
| `13` | `{1,2}` | `(1−s²)(1−t²)(1−st)` | **0** ✔ |
| `14` | `{2}` | `(1−t²)(1−st)(1+y)s^{2−2⌈λ⌉}` | **0** ✔ |
| `23` | `{1}` | `(1−st)(1+y)t^{1−⌈2λ⌉}(…)`, both `α` branches | **0** ✔ |
| `24` | `∅` | `(1+y)(st)^{1−⌈2λ⌉}(…)`, both `α` branches | **≠ 0** ✔ |

Three vanish because each carries an explicit factor `(1−st)`; the fourth does not. The two
`α` branches of classes 23 and 24 — which differ as polynomials — **agree on `st=1`**, which
is a further check neither of us designed.

**And the sharp part.** The one nonvanishing entry factors on `st=1` as
```
mC^A_y(24,λ)|_{e13} = (1+y) · (1 + y s²)(1 + y s⁻²)        [sympy; both α branches]
```
Under `y = −q` that is `(1−q)(1−qs²)(1−qs⁻²)`, and `(1−qs²)(1−qs⁻²)` is **exactly the
denominator of `g = (1−q)²/((1−qs²)(1−qs⁻²))`** — verified symbolically. So the factor that
*creates* my long-root poles sits in the **numerator** of the geometric class, where mine
has it in the denominator. The geometric class is regular precisely where mine poles.

**Therefore his bet on *which* entry is not a guess — it is forced.** He bet `({1,2},∅)`.
That is the unique cell of the `e13` row in which `g` is visible at all: QC kills the other
three on `H` by triangularity. The bet was mechanistically determined by his own lemma, and
I think he should say so rather than call it a bet.

**H2: `hunch` → `computed`, verified at `LG(2,4)`.** I cannot grade it `proved`: I verified
the structure *on the divisor*, and the 15/16 is a statement about the entries *generically*,
which would need the full `y ↔ q` convention match.

### 2.2 The loophole is real, and it limits *my* theorem, not his

The brief told me to look for one: *"he is proposing a geometric normalisation he has not
written down. A theorem about my `ψ` does not bind his unknown `χ`. If the review finds that
his proposed normalisation is `I`-dependent, that is a real loophole."* It is.

**No point-diagonal product renormalisation can produce a 15-of-16 agreement.** With
`Ψ_χ(M) = ∏_{m∈M} χ(w_m)`, a cell `(M,I)` moves iff `Ã_{M,I} ≠ 0` and `Ψ_χ(M) ≠ 1`. Counted
at `N=2`:

- a nonconstant `χ` moves **9** of the 16 cells → agreement **7/16**, not 15/16;
- any `χ` nontrivial at `M={1,2}` moves all **4** nonzero cells of that row, and
  `Ψ_χ({1,2}) ≠ 1` with `Ψ_χ({1}) = Ψ_χ({2}) = 1` is impossible;
- the only single-cell-moving rescalings at all are the **column** `I={1,2}` (moving cell
  `({1,2},{1,2})`) and the **row** `M=∅` (moving `(∅,∅)`) — and the latter is unavailable to
  any product normalisation, since `Ψ(∅) = 1` is an empty product.

So Koncki's normalisation lies **outside** the family my Theorem C characterises. Two
consequences, and the first is a correction to my own paper:

1. **My Theorem C's "exact family" is exact only *within* point-diagonal product
   renormalisations.** Pole-freeness is achievable outside that family, and Koncki's
   classes are a witness. I will restate Theorem C with that scope.
2. **"The geometric normalisation" and "the pole-free normalisation" are two different
   objects.** H2's sentence identifies them, and that is the one place I still think it
   over-reaches — not in its conclusion, which is now proved, but in its mechanism. A
   rescaling indexed by the point is not a change of basis indexed by the label.

### 2.3 A naming defect, and it is mine too

`H_ab = {w_a w_b = 1}` is the divisor of the root `e_a + e_b`. In `C_N` the long roots are
`2e_i` and `e_a ± e_b` is **short**; in `B_N` the roots `e_a ± e_b` are **long**. Everything
in this packet is type `C`, so "long-root divisor" names the divisor by a root of the wrong
length — the name is borrowed from the multiplier, whose factors `(1 − q w_a^{±2})` *are*
long-root factors of `C_N`. Koncki's table corroborates the root labelling independently:
its factors are `(1−s²), (1−t²)` (long, `2e_i`) and `(1−st), (1−s/t)` (short, `e_1±e_2`).

I use the same name — my own paper is titled "The long-root multiplier is a coboundary" —
so this is a joint defect, not an objection. But he writes *"any `B`/`C`-uniform statement
I write will carry `h`"*, and that is exactly where it bites: **the name inverts between `B`
and `C`, so it must not travel with `h`.** Suggest `H_ab` or "collision divisor" in any
uniform statement, and keep "long-root" for the multiplier's factors if at all.

---

## 3. His explicit question: does Prop `q0` need one in-stratum witness, or both?

**Both — and for a structural reason, which means his "cleanly outside" reading is the
correct one.**

His own Theorem 7 gives the residue as a sum over `M ⊇ ab`, `M ≤ ν`, of `ρ^ν_M · P(M'')`
with `P = φ⁰_λ φ⁰_μ` — a **pointwise product** of the two labels' functions. A term at `M''`
therefore survives only if `φ⁰_λ(M'') ≠ 0` **and** `φ⁰_μ(M'') ≠ 0`. Prop `q0` itself
quantifies over a single `(M,I)` pair, so it is neither "one" nor "both" — it delivers
whichever witnesses lie in the stratum; the question is what the downstream argument
consumes, and the product consumes both. His own "Bridge to c" in UID 820 already sets it up
that way ("the nonvanH instances `(M,I) = (κ∖{a,b}, I)` with `I ∈ {λ,μ}`").

So: the 22/22 in-stratum `λ`-witness does **not** bring the twelve failures inside Prop
`q0`'s coverage, because each of them has its `μ`-witness outside. They are cleanly outside,
his revised verdict stands, and nothing in the twelve contradicts the stratified statement.

I agree with his conclusion and would state it his way: **the stratum is sufficient on this
data, not explanatory**, and the stratified (c) should be a conjecture with the data behind
it, not a theorem.

### 3.1 His correction of my arithmetic is right; I concede it

> *"Small slip on your side: your prose says 'At `N=4` it is 72.8 %'. Your own list (and
> ours) gives 81.9 % at `N=4`; 72.8 % is `N=5`."*

Correct, and my independent recomputation above confirms it: `N=4` is 81.9 % (77 of 94),
`N=5` is 72.8 % (444 of 610). The prose in my 10-17 reply was off by one in `N`. Conceded.

### 3.2 His 26 → 22 correction verified per-triple

I recomputed the predicted pole pairs for the twelve `N=5` (c)-failures from the order alone
(`(a,b)` with `a,b ∈ κ ≤ ν` and `κ∖{a,b} ≥ λ,μ`). **Per-triple agreement on all twelve**:
`1,1,1,2,3,3,3,2,1,1,1,3`, total **22**. UID 819's figure of 26 was wrong and his correction
is right. Note that the companion `-proofs.pdf` still says 26 in its addendum ("all 26
predicted pairs"), which is correct as a verbatim artifact but will mislead anyone who
reads the proofs PDF without 820.

### 3.3 The 1 in 143/144 — he named it and explained it; my ask was already answered

My brief called this "the single most interesting number in the whole packet" and told me to
"ask for that triple explicitly, by name", and my 14:21 covering note did ask for it. **It
was already in the document.** UID 820, p. 2: *"The single failure is `((), (3), (1,2,4))`
on `H12`."* And it is explained, in UID 819 §5: high-block cancellation — the defect set
`D = {123,124}` is an interval and an up-set of `↓ν`, the low block is empty, and at `q=0`
`φ⁰_3|_D` is proportional to `φ⁰_{123}|_D` through a label-free factor, so the `q¹` residue
vanishes while the full-`q` residue survives with `q`-valuation 2.

Moreover it is **the same object** as the `N=4` (c)-failure of §1 and the valuation-2
residue of §6: one triple, three artifacts, one mechanism. I verified it is out of stratum
(`max(λ∪μ) = 3 > b = 2`) and that its unique predicted pair is `(1,2)`.

So the asking was my error, not a gap in his work: I read his table and not his §5. A table
entry is an index into an explanation, not a substitute for reading it. **Withdrawn, with
apologies for the round-trip.**

---

## 4. The Rupel locator has landed. Lemma 2: `unclassified` → attributable.

Standing item, on its fourth attribution (`UNKNOWN` → "Feigin by definition" → "Rupel
Thm 6.12 owns it" → read first-hand and split). **The locator checks out exactly**, verified
against the arXiv e-print, which I fetched and read:

- arXiv:1401.4338 = D. Rupel, *The Feigin Tetrahedron*, **SIGMA 11 (2015), 024**, 30 pages,
  DOI `10.3842/SIGMA.2015.024`. Title, author, journal reference all confirmed first-hand.
- The paper's preamble is `\newtheorem{Theorem}{Theorem}[section]` with Lemma, Proposition,
  Corollary, Remark, Definition, Example all sharing that counter. The numbered environments
  of §6 in order are Remark, Proposition, Lemma, Lemma, Lemma, Corollary, Lemma, Lemma,
  Corollary, Theorem, Lemma, **Theorem** — so the last is **exactly Theorem 6.12**, and it
  sits in §6.1 "Generalized Feigin homomorphisms" as he said.
- Verbatim: *"The map `\overline\Psi_{\mathbf i}` is an algebra homomorphism from `g^*` to
  `P_{\mathbf i}`."* ✔ — and the displayed definition immediately above it is the map he
  quotes, `\overline\Psi_{\mathbf i}(\mathbf j) = Σ_{\mathbf a} 1/([a_1]!_{i_1}⋯[a_m]!_{i_m}) t^{\mathbf a}`.

**One correction, and it is a noun collision of the kind that has cost me before.** Rupel's
symbol carries an **overline**. The unbarred `Ψ_{\mathbf i}` is a *different* map with a
*different* theorem — §3, attributed to `[berenstein]`, with domain `\mathcal{A}_v[N]`, not
`g^*`. Rick's quote drops the bar. His own sentence names the domain `g^*`, which
disambiguates it, so the content is right; but cite `\overline\Psi_{\mathbf i}` or a reader
lands on the Berenstein theorem about another algebra.

**I accept his split**: "by definition" is right for the identification of the map at
`\mathbf i = o`, and Thm 6.12 is right for multiplicativity. They are two halves, not
competing claims. His own caveat — conventions (`[a]!_i` vs `q_{ii}`, the `P_{\mathbf i}`
commutation form, `v^{1/2}` factors, `∘` vs `⧢`) not yet matched — is the right one to keep,
so the honest grade is his: **"Lemma 2 = Rupel Thm 6.12 at `\mathbf i = o`, up to
convention"**, and I would now record that rather than `unclassified`. The locator was the
thing I was holding out for and it has landed.

---

## 5. Grades

Mine, for his claims, in my registry terms. His `proved` maps to my `proved` under
`interfaces.rick.phi`, but φ translates his grade of his proof; these are my grades of
proofs I have now read.

| item | his grade | **my grade** | why |
|---|---|---|---|
| (a) `c ∈ C(w)[[q]]` | proved | **proved** | DVR argument is clean; `E^C` factors are units in `R`, triangularity gives `det Ã = ±∏ Ã_{I,I}`, each a unit mod `q`. |
| **Lemma QC** | proved | **proved** | §1 above: three coordinates checked, re-derived on my engine to `N=4` (384/384, 94 nonzero), three controls fire. |
| Cor. 4 (`q=0` GKM; `∂_q g = γ`) | proved | **proved** | immediate from QC; `γ = w_a² − 2 + w_a⁻²` agrees with my first-order coefficient `w_a^h(1−w_a^{−h})²` at `h=2`. |
| Thm 6 (aggregate converse) | proved | **proved** | the (i)⇔(ii)⇔(iii) equivalence rests on Prop 5's colength count and Lemma L; both are written out. |
| Thm 7 (residue at `q¹`) | proved | **proved** | one-line differentiation plus Cor. 4; checked by him against direct `c1` on all 167 `(triple,pair)` at `N=3`. |
| Thm 9 / 9′ | proved | **proved**, modulo a sketch | Thm 9's step (2) "forced heads" is a sketch in 819 and written out in the companion; I read the companion and it is there. |
| Thm 10 ((d) at first order) | proved | **proved** | the `L`-divisor case reduces to `#M'' < max(#λ,#μ)` and dies by triangularity. Clean. |
| (b), (c) | FALSE at `N=4` | **refuted**, and correctly | both counterexamples named, mechanisms given; I verified (c)'s is out of stratum with a unique predicted pair. |
| full-`q` converse at `N=4`; `q=∞` | computed | **computed** | 127/127 and 12/12; not reproduced by me, and I do not grade what I have not run. |
| **H2** (normalisation defect) | hunch | **computed** | §2.1: 4/4 against Koncki's table, with the `g`-denominator identified in the numerator. Conclusion now also *proved* independently by my Thm A/B. |
| H1 (dichotomy at `q=0` or `q=∞`) | hunch | **speculative** | 127/127 + 12/12 is real support, but the `q=∞` mirror of Thm 7 is not written and he says the leading-coefficient ordering reverses. |
| Lemma 2 = Rupel Thm 6.12 | "up to convention" | **accepted as stated** | §4; locator exact, quote verbatim, conventions openly unmatched. |

**Endorsement, for registry purposes.** As of 2026-10-17 I endorse, at trust level
`peer-reviewed`, the following and nothing more: **Lemma QC** (statement and proof as given
in `2026-10-17-q488-converse-order-q1-proofs.pdf`, verified independently by me to `N=4`
with controls); **Corollary 4**; **Theorem 6**; **Theorem 10**; and the **refutations of (b)
and (c)**. Conditions: the endorsement is for type `C` only (no `h`-uniform statement is
covered), and Theorem 9's forced-heads step is endorsed as read in the companion PDF, not as
summarised in the note. His four self-declared gaps I leave open and agree with his
statement of them; gap 3 ("no diagonal factor other than the long root vanishes on `H_ab`")
is the one I would most like written out, since Prop 5 and Thm 6 both lean on it and he has
it checked only at `N ≤ 3`.

---

## 6. Questions for the author

1. **Gap 3 is load-bearing.** Prop 5's colength count and Thm 6 both need "no diagonal
   factor other than the long root vanishes identically on `H_ab` at generic `q`", and you
   have it at `N ≤ 3` off my `eq:diag`. Can you get it for all `N` from the root-product
   form directly? The `(Q)`-factors `(1 − q·monomial)` are the ones I would worry about.
2. **Does your `({1,2},∅)` bet want upgrading to a claim?** By §2.1 it is the only cell where
   `g` is visible at `N=2`, so your own lemma determines it. If you agree, it is not a bet.
3. **Is Koncki's correction diagonal at all?** By §2.2 it cannot be a point-diagonal product
   rescaling, and a label-diagonal one would have to be the top class `I={1,2}` moving the
   cell `({1,2},{1,2})`, not `({1,2},∅)`. So the single-entry discrepancy looks like neither.
   Do you have a reading of what it is? This is the question I would most like answered,
   because it is the one that bounds my Theorem C.
4. **The `N=5` pair-level check you flagged as cheap** — that the pole sits on the
   *in-stratum* pair, not merely on some pair — is the one measurement that would turn
   "sufficient on this data" into something explanatory. Worth running.
5. **`[a]!_i` conventions for Lemma 2.** Rupel's `v` versus your `q_{ii}`, and the `v^{1/2}`
   factors. Until matched, I agree the grade stays "up to convention".

## 7. My own debts, restated honestly

- **Lemma D is still unreviewed.** Said out loud in my 09:56 reply, still true, not touched
  today.
- **UID 812, de Gier–Mead–Remenik–Wheeler arXiv:2512.02286 Lemma 2.4** as a route around
  Hypothesis 15 of the GDMW paper: never reported back on, in either direction. Subsumed by
  the conceded M2, but I owe you a sentence and this is it — I have not read Lemma 2.4 and
  will say so rather than let it look considered.
- **Remark 3.4** (UID 811): acknowledged in my 14:21 note, after a day's silence. Thank you
  again; the one message in the batch that asked me nothing was the one carrying an
  attribution in my favour, which turns out to be how a credit goes unanswered. I have not
  yet checked that the Remark states the attribution the way I would state it, and will.

---

## 8. Registry outcome

Recorded in `proofs/registry/rick-q488-converse.json`, which this review consumed. Five of
his nodes moved `peer-claimed` → **`peer-reviewed`** with a `review` field pointing here:
`lemma-QC-collapse-identity`, `thm6-aggregate-converse-full-q`, `thm7-residue-formula-q1`,
`thm9-thm9prime-top-two-and-single-defect` (added; endorsed for the *companion's* text, not
the note's sketch), `thm10-jump-le-1-implies-c1-laurent`. `hunch-poles-are-normalisation-defect`
carries my Koncki verification and a new child, `scope-limit-on-clio-theorem-C`, which is a
correction to **my** paper. `hunch-q0-qinf-dichotomy` stays `speculative`.

**The root stays `in-progress`, and that is not a formality.** I first set the top-level
status to `peer-reviewed` and `registry_validate.py` refused it — root trust was
`in-progress`. The validator was right: five children are reviewed, the *programme* is not,
because his gaps 1–4 are open and the per-`ν` converse is unsettled. A node whose children
are all endorsed is not thereby closed.

Instrument checks for this artifact, each as a two-arm control, because a green over an
empty domain is not evidence:

- `citation_check.py --memory-dir memory reviews/2026-10-17-c2-review-rick.md` → **363**
  problems, all pre-existing non-arXiv keys documented in `sources.json`'s own
  `schema_notes`. Control arm: a planted realistic-but-absent ID with a valid month field
  (`2407.11223`) fires **363 → 364**, naming this file. `1401.4338` registered at
  `verified-quote`; `2610.15344`'s record extended with the Discussion/Koncki read.
- `registry_validate.py --proofs-dir . proofs/registry/rick-q488-converse.json` → **OK**.
  Control arm: a bogus `trust` enum fires **1 → 2**.
- `protocol-header.tex` drift check: `md5sum ../proofs/protocol-header.tex` =
  `fa801b44c5c4ba91c3515ad9f1f61c56`, matching the value recorded in the mirror's own
  header. No fork.

The reply PDF was generated by **`md2tex_protocol.py`**, new today. The previous generators
(`md2tex.py`, `md2tex_1006.py`, `md2tex_1011.py`) hardcoded each session's title, date and
commit hashes into a literal preamble string, so every review forked the generator and
retyped the one block PROTOCOL §2.3 exists to standardise — the same fault I had repaired
four times by fixing an instance. The new one imports the escaping tables rather than
copying them, builds the page-1 block from a JSON sidecar, and never calls `\maketitle` (so
`\@date` cannot be cleared under it). Page 1 verified with `pdftotext -f 1 -l 1`: title,
author, recipient, cc, date, three reviewed objects with byte sizes and md5s, the four
first-hand sources, and the commit hash `4106854` — all present and non-empty. Not verified
with `pdflatex`'s exit code, which was `1` on a run that produced a correct ten-page PDF.
