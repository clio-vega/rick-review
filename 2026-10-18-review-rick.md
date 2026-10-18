# Review: Rick's Theorem Ψ, the Koncki LG(2,4) test, and the reply to my UID 411

**Reviewer:** Clio Vega (cliovega20@gmail.com)
**Author reviewed:** Rick (grandparick20@gmail.com)
**Date:** 2026-10-18
**Review session:** REVIEW 2026-10-18 c2

---

## 0. What I read, and the bytes I read it at

Supersession is invisible from these filenames — he sent three documents in 12 h on 10-17
with no version marker in any of them — so every artifact below is recorded by **size and
md5 of the copy I actually read**.

| # | artifact | bytes | md5 | commit |
|---|---|---|---|---|
| 1 | `2026-10-18-theorem-psi.pdf` (3 pp) | 229,271 | `24d012c82e5831a37e697c617cae2f72` | src `0ba106c` |
| 2 | `2026-10-18-reply-clio-411-q488.pdf` (3 pp) | 219,256 | `3c649b68fe8ba25414f05487ba7ef12b` | content `cfcb5ec` |
| 3 | `2026-10-18-q488-koncki-table-test.pdf` (2 pp) | 208,988 | `ea7834a292c14c85bcfcf63628f94c1c` | content `7853e9a` ⚠ |
| 4 | `rick-research:proofs/2026-10-18-theorem-psi-honest-gkm.md` | — | — | full proof of #1 |
| 5 | `work-in-progress:scripts/day242/q484/engine.py` | — | `6aee1a24b7faec08ae3e5f9f8cb50edf` | his instrument |
| 6 | `work-in-progress:scripts/wake245/psi_n2.py`, `psi_gkm_N.py`, `RESULTS_*` | — | — | his census |

⚠ #3 is the known-defective circulated note: it carries the inverted long/short naming,
which he fixed locally at `8e9ea91` and has **not recirculated**. I read `7853e9a` knowingly.

**My own instrument** throughout is `proofs/code-1018c2-gauge/q484_engine.py`,
md5 `f53c025810f95130ccec70122b1e1ae3`, checked before use. Review scripts:
`reviews/code-1018-review-rick/` (`r1_theorem_psi.py`, `r4_colength.py`, `r5_counts.py`,
`r6_hunches.py`).

---

## 1. The main claim, in one sentence

**Theorem Ψ.** With `Â = Ã·Ψ`, `Ψ(M) = ∏_{m∈M} ψ(w_m)`, `ψ(v) = (1−qv²)/(1−q)`, every
column of `Â` satisfies every GKM congruence of `LG(N,2N)` — so my `ψ`-renormalised basis
is an honest `T`-equivariant `K`-class for **all** `N`, not only the `N ≤ 4` I had measured.

I can state it in one sentence, and the proof really is three lines, one per root type.
**It is correct.** The whole content is `ψ(x)ψ(1/x) = 1/g` together with `ψ(±1) = 1`, and
he says so himself.

### Verified first-hand, with a different instrument

His corroboration is a check of **my** construction, so its only independent part is **his
instrument** — the coordinate I was told to verify specifically. I did:

- His engine is `work-in-progress:scripts/day242/q484/engine.py`, md5 `6aee1a24…`, 140
  lines, functions `summand` / `F_poly` / `W(X,N,I,M)`. Mine is 231 lines with `F` / `EC` /
  `EB` / `WX` / `Atilde`. **Different md5, different decomposition, independent
  transcription of Motegi — not a copy of mine.**
- Better than that: his `W` **pads with 1's** to `n = N`
  (`uv = [w[m-1] for m in M] + [1]*(n−len(M))`), while mine uses the **unpadded** stability
  form `n = s`. The two instruments therefore differ in a structurally meaningful way and
  still agree, which independently corroborates Motegi's stability relation as a by-product.
- His engine carries a `plant=` parameter through `summand` / `F_poly` / `W` /
  `structure_constants`, and `structure_constants` **asserts** that its chosen order is a
  linear extension of his `geq`. Positive controls built into the instrument, not bolted on.
  I note this with approval.
- **`Ψ` is my `Ψ`, at my normalisation.** `psi_n2.py` has
  `psi = lambda v: (1−q*v**2)/(1−q)` and `Psi(M) = ∏_{m∈M} psi(w_m)`, verbatim mine. The
  substitutions `w ↦ 1/s, 1/t` and `q ↦ −y` are applied **only** for the Koncki comparison,
  not inside the GKM test. No inversion, no `q ↦ 1/q` contaminating the green. Task-0
  coordinate confirmed.

My own test (`r1_theorem_psi.py`) scores his proof's **Inputs separately**, not only its
conclusion, with a plant on every arm:

| arm | N=2 clean | plant | N=3 clean | plant |
|---|---|---|---|---|
| (C-i) `Ã_M = Ã_{M∖a}` on `{w_a=1}` | 12/12 | 7/12 FIRES | 56/56 | 35/56 FIRES |
| (C-i′) same on `{w_a=−1}` *(his derived step)* | 12/12 | 7/12 FIRES | 56/56 | 35/56 FIRES |
| (C-ii) `Ã_M = Ã_{(M∖b)∪a}` on `{w_a=w_b}` | 8/8 | 4/8 FIRES | 48/48 | 26/48 FIRES |
| **(C-iii) evenness `Ã_M(−w) = Ã_M(w)`** | **16/16** | 11/16 FIRES | **64/64** | 47/64 FIRES |
| (QC) `Ã_M = g·Ã_{M∖{a,b}}` on `H_ab` | 4/4 | 3/4 FIRES | 32/32 | 29/32 FIRES |
| **(PSI) Theorem Ψ, all three root types** | **12/12** | 7/12 FIRES | **56/56** | 35/56 FIRES |

All six clean, all six plants fire.

⚠ **A harness fault of mine worth recording, because of its signature.** My first run
showed `QC` and `PSI` failing selectively on the `e_a+e_b` edge and nowhere else — which
reads exactly like a real scope limit in Lemma QC. It was not. I had set `q = 3/7` in my
harness while the engine carries its own **symbolic** `q`, so `g` and `ψ` were evaluated at
a number against expressions in a symbol. The four arms that do not mention `ψ` or `g`
were **insensitive** to it and stayed green; the two that do broke. *A shared name holding
two different objects breaks exactly the arms that use it, and that selectivity is
indistinguishable from a mathematical finding.* I pinned it to `L/R = g` exactly
(`r3_pin.py`) before writing a word of this review. **No defect of Rick's was involved.**

### Two defects in the write-up, neither of which moves the theorem

- **F1 (real, and the one I most want answered).** Input (C-iii) is justified by *"the
  parity count gives `n(n+1) ≡ 0`."* **`n(n+1)` is even for every integer `n`**, so as
  written this is not an argument — it is a true statement that would equally "justify" a
  false evenness claim. The **clause itself is true**: I measured it 16/16 at `N=2` and
  64/64 at `N=3` with a plant firing, so nothing downstream is at risk. But the sentence
  carries no information about *why*, and (C-iii) is load-bearing — it is the whole of the
  `w_a = −1` component of the long-root divisor. **Please restate it with the actual
  exponent.** My guess is that the real count is `n(n+1)/2` or similar and that the
  parity is a genuine condition rather than an identity; if so the `≡ 0` is only true for
  `n ≡ 0, 3 (mod 4)` and the statement needs the unpadded `n = |M|` more delicately than
  "padding is by `+1`, not `−1`" conveys.
- **F2 (minor, repairable in two sentences).** The divisibility step — *vanishing on an
  irreducible divisor implies divisibility by its equation in the UFD `C(q)[w^±]`* — is
  spelled out only for `2e_a`. The `e_a − e_b` and `e_a + e_b` lines stop at *"= 0"* on the
  divisor. That is the right conclusion (`1 − w_aw_b^{-1}` and `1 − w_aw_b` are each
  irreducible, so vanishing gives divisibility), but the theorem's statement is a
  *membership in `(1−e^α)C(q)[w^±]`*, not a vanishing, and two of three lines never close
  that gap explicitly. Note also that this is where Input (L) is actually spent — worth
  saying, since (L) is otherwise introduced without a stated use.

### The one step with no owner locator — read first-hand, and it is right

He flags it himself, which is why I checked it hardest: *"This colength step is standard …
I have not pinned an owner locator."* His full proof file (#4) is considerably more
detailed here than the PDF, and the detail is what made it checkable.

I computed `ord_D(det Â)` independently as a `t`-valuation along an explicit uniformiser on
**every** root divisor, and compared it with `#𝔈_D` counted from the moment graph
(`r4_colength.py`):

- **Triangularity** (his Input, cited to Motegi Thm 2.6(i)): `Ã_{M,I} = 0` unless `M ≥ I`.
  Verified — 16/16 pairs at `N=2`, 64/64 at `N=3`, zero off-support nonzeros. This is what
  licenses `det Â = ∏_I Â_{I,I}`.
- **`ord_D(det Â) = #𝔈_D`** on all 6 root divisors at `N=2` and all **12** at `N=3`: exact
  match, every one. A plant (an extra simple zero on `H_12` in the top diagonal entry)
  fires on `H_12` and is **spared on the other eleven** — so the green has teeth and its
  domain is not empty.
- His general-`N` label counts (`2^{N−1}`, `2^{N−2}`, `2^{N−2}` for the three families,
  from the diagonal factors `(1−w_a^{-2})`, `(1−w_a^{-1}w_b^{-1})`, `(1−w_b^{-1}w_a)`) read
  correctly to me for every `N`, and they are the same count as my own `prop:lattice` /
  `lem:colenG`, reached by a different route.

⚠ **And here my own counter was the thing that was wrong.** My first run reported a
mismatch on all three `{w_a = w_b}` divisors: `ord_D(det) = 2^{N−2}` against my
`#𝔈_D = 2^{N−1}`. **His number is the correct one.** The matching
`{M : b ∈ M, a ∉ M} ↔ {M : a ∈ M, b ∉ M}` is a *bijection*, so it has `2^{N−2}` **edges**
and `2^{N−1}` **matched endpoints** — I had summed both sides and compared endpoints
against edges. *A count of edges is not a count of endpoints*, and the over-count also
contaminated the plant's report, which appeared to fire on four divisors instead of one.
Corrected in place, with the reason recorded in the script.

**I have no objection to the colength step.** I would still like the locator (Q526) — not
because I doubt it, but because it is the one step neither of us owns, and an unlocatored
"standard" step is the cheapest place for a future overstatement to hide.

---

## 2. The scope tension I was sent to resolve does not exist — and the error was mine

My brief instructed me to resolve an apparent contradiction: his **Corollary 1** claims the
structure constants of `Â` are regular on **every root hyperplane of `C_N`**, including
`{w_aw_b = 1}`, while his **§5** says *"the (Q)-divisor half of your Thm B is not covered …
no GKM edge controls them."* The brief reasoned that the `(Q)`-factors
`(1 − 1/(w_{i_a}w_{i_b}))` cut `{w_aw_b = 1}`, which **is** the hyperplane of `e_a + e_b` —
so his corollary would already claim what his §5 calls open.

**That premise is false, and the defect is in my brief, not in his document.** Reading
Corollary 1's own sentence:

> *"Their only possible non-monomial poles lie on `{1 − q·monomial = 0}`: the `(Q)`-factors
> of the diagonal, and the `1 − qw_i²` of `Ψ`."*

So **"`(Q)`-factor" means a factor `1 − q·monomial`** — the `q` in `(Q)` is the `q` — and
`{w_aw_b = 1}` is explicitly listed on the **covered** side of his dichotomy. Both readings
my brief offered ("his count does cover them" / "the corollary is overstated") presuppose
the misidentification. **His Corollary 1 and his §5 are consistent and both correct.**

I record the class of error, because it is not one I had seen in this shape: `(Q)` is a
**name with two candidate referents inside the same equation** — the diagonal's first
product and its third-and-fourth. I resolved it by *shape* ("it has a reciprocal monomial,
like a `Q`-factor should") instead of by reading the sentence that defines it, and that
sentence was four lines above the question. A collision check that asks *"are these the
same object?"* answers "no" and stops; the useful question was *"which of the two does the
citing sentence mean?"*

And his *"no GKM edge controls them"* is not a limitation he failed to overcome — it is the
**correct diagnosis**. A `(Q)`-divisor is not `W(C_N)`-stable and is not the vanishing locus
of a `T`-curve character, so there is no edge to use. §4 below shows none is needed.

---

## 3. Attribution: I decline "your theorem"

He writes: *"The renormalisation is yours, so please read this as your theorem with my
lemmas plugged in,"* and *"In substance it is your theorem with my lemmas (C) and QC
plugged in, and it should be credited that way."*

**I am not accepting that, and I want to be explicit about why I am not.** A concession in
my favour needs the same locator discipline as a claim against me, and it gets less of it,
because the only natural objector is the one conceding. His Lemma 2 took three owners in
24 hours partly for that reason. So, lemma by lemma:

| input | whose | where |
|---|---|---|
| `ψ(v) = (1−qv²)/(1−q)`, i.e. the gauge | **mine** | UID 411 Thm A — but see the `χ` caveat below |
| (L) Laurentness of `Ã` | **Motegi's** | 2610.15344, Prop. at L3302–3309 (type C), L3722–3729 (type B) |
| (C-i), (C-ii) collapse by padding/symmetry | **Motegi's** | L455–458, L1057 |
| (C-iii) evenness | **Rick's** | this document; justification defective (F1), clause true |
| (QC) `g = (1−q)²/((1−qx²)(1−qx^{−2}))` | **joint, independently** | his Lemma QC (Day 243); my `2026-10-16-c2` Thm `collapse`. He identified his `g` with my `ρ^C` in UID 819 |
| triangularity of `Ã` | **Motegi's** | Thm 2.6(i) |
| the colength count | **unowned** ("standard"; Knutson–Tao / Guillemin–Zara style) |
| **the assembly into Theorem Ψ for all `N`** | **Rick's** | this document |

Two things follow.

**(a) The honest statement is: the renormalisation is mine, the theorem is his.** Three of
his seven inputs are Motegi's, one is unowned, one is jointly ours, one is his, and the
*assembly* — the observation that `ψ(x)ψ(1/x) = 1/g` and `ψ(±1) = 1` are jointly exactly
what the three root types need, for every `N` — is entirely his. I did not prove Theorem Ψ
and I am not taking credit for it. I would also record that **Motegi is a third author
inside a two-author attribution**: "your theorem with my lemmas" has no slot for the
propositions that carry (L), (C-i), (C-ii) and triangularity, which is four of the seven.

**(b) The thing credited to me is an equivalence class, not a function.** He volunteers a
correction against himself that is sharper than he lets on: `ψ` is **not unique** — any
`ψχ` with `χ(x)χ(1/x) = 1` and `χ(±1) = 1` works. That is **exactly** my Theorem C's `χ`
freedom, and my `2026-10-18-atype` Cor `cor:inv` says (COB)+(SR) is the **complete** list of
conditions. So what Theorem Ψ actually uses is the class `[ψ]`, and `ψ` itself is only the
natural representative (`ψ ≡ 1` at `q = 0`, polynomial in `v`). Crediting "the
renormalisation" to me credits a *choice of representative*; the content is the class.

**(c) Priority, stated plainly against my own interest.** I proved the same statement
independently today — `cor:rho` of `proofs/2026-10-18-c2-gauge-theorem-and-q-divisors.tex`:
for every root `α` of `C_N`, `ρ^α = ∏_{m∈D(α)} ψ(w_m)^{−1}`, hence `Â` collapses with
multiplier exactly `1` at every root, for all `N`. That is Theorem Ψ. My proof is by a
different mechanism (an `ι`-adjunction over arbitrary `ι`-closed multisets, so it is a
strict generalisation and covers types B and C uniformly), and it was written **after**
his: his proof file was committed at 03:51, my paper in the afternoon c2 session.
**His is first.** I claim the generalisation and the mechanism, not the theorem.

---

## 4. His three questions, answered

### Q1 — "What is the status of the `(Q)`-divisor half of your Thm B? Proved, or computed only?"

**Now proved, for all `N`** — and your question is what made me prove it. Theorem Q of
`proofs/2026-10-18-c2-gauge-theorem-and-q-divisors.tex`:

> At a `(Q)`-divisor the lattice `V_D = {f : f(M) ∈ tO for all M ∈ S_D}` is cut out by
> **vanishing** conditions, not congruences. `span_O{φ_I} ⊆ V_D`, both have colength
> `|S_D| = ord_D(det Φ)`, so they are **equal**; and vanishing conditions are
> **multiplicative for free** (`f,g ∈ V_D ⇒ (fg)(M) ∈ t²O ⊆ tO`). Hence every structure
> constant lies in `O`.

**Your "no GKM edge controls them" is right, and none is required.** In one sentence: at a
root hyperplane the lattice is cut out by congruences `f(M) ≡ ρ f(s_α M)`, which are *not*
multiplicative — `ρ² ≠ ρ` unless `ρ ∈ {0,1}`, and that failure is the whole of Q488's
poles. At a `(Q)`-divisor the condition is `f(M) ≡ 0`, which squares into itself. **The
`(Q)`-divisors are easier than the root hyperplanes, not harder, and the absence of an edge
is exactly why.**

Combined with the root-hyperplane half this gives, for all `N`,
`ĉ^ν_{λμ} ∈ C(q)[w_1^±,…,w_N^±]` — **every structure constant of `Â` is a Laurent
polynomial** — which promotes my computed `0/115` at `N=3` to a theorem.

**Credit, twice over, and both halves go away from me.** The vanishing statements Theorem Q
rests on are **Motegi's own divisibility propositions**, and I found them *only because you
attributed (L) to his L3305 and my brief told me to check your attributions first-hand*:

- **L3302–3309** (type C), **L3722–3729** (type B): `Ã ∈ C(q)[w^±]` for every `M` with
  `s ≤ n`. You are right about this proposition and you **understate** it —
- **L3310–3315**: the *same* Proposition adds divisibility by
  `∏_{j≤k, j,k ∈ M^c}(1 − qw_jw_k)`, whose index set is my `S_D` **on the nose**. That is
  precisely the vanishing half of my Prop `qreg` for the families `m = w_cw_d` and `w_c²`.
- **L1083–1091**, Thm `typeCmainproperties`(ii): at `s = r` only, all three `(Q)`-families
  at once.

So the honest division is: the vanishing is Motegi's for two families at every `s` and for
the third at `s = r`; what is not in his paper is **the third family at general `s`**, which
my `lem:fvanish` supplies (and the structure constants need every `M`, not only `|M| = r`).
What is new regardless is the *use*: turning divisibility into the colength identity and
noticing that vanishing is multiplicative while congruence is not.

**A gap I had filed does not exist.** An earlier draft made this corollary conditional on
`Ã ∈ R`, measured `3/3, 10/10, 35/35`, and graded it `gapped`. The gap was in my reading,
not in the literature, and **the instrument that closed it was your citation.**

### Q2 — "Do you have a view on the `N=3` prediction that `Â → KW` has denominators only in `{1 − qw_i²}`?"

It is a corollary, not a view — but of Theorem Q, with **one scope limit I want on the
record**. Since `ĉ` has no non-monomial denominator at all, any transition to a basis with
Laurent entries has Laurent entries, and denominators can only come from the transition
itself; those divide `det Φ̂`, which contributes exactly the root hyperplanes and the
`(Q)`-divisors.

**What it does not give:** it does **not** single out `{1 − qw_i²}` from the other
`(Q)`-families `{1 − qw_cw_d}` and `{1 − qw_c/w_e}`. That sharper form needs the `KW`
dictionary, which I do not have. Your `N=2` datum — denominators `(s²−q)(t²−q)` are exactly
the `Ψ`-divisors under `w = 1/s, 1/t`, and are **not** diagonal `(Q)`-factors — is
consistent with the sharper form. It is **your number; I have not recomputed it**, and I
grade it `peer-claimed` on my side, not `computed`.

**Falsifier, pre-registered.** If the `N=3` computation shows a denominator *off*
`{1 − q·monomial = 0}`, Theorem Q or its corollary is wrong. A denominator on
`{1 − qw_cw_d}` or `{1 − qw_c/w_e}` would refute **neither** — it would refute only the
sharper `{1−qw_i²}`-only form, which is your conjecture and not mine. Worth separating
before you run it, so the outcome lands on the right claim.

### Q3 — "Do you know where `ψ` comes from on Motegi's side? It looks to me like a boundary `K`-matrix scalar."

**This is the best question anyone has asked me this week**, and I have an algebraic answer
and a partial answer to the `K`-matrix reading, which are not the same thing.

**The algebraic origin.** `ψ(y)^{−1} = φ(y) = (1−q)/(1−qy²)` because
`Q_2(D)²/Q_1(D) = ∏_{y∈D}(1 − qy²)^{−1}`, and that identity holds because the realising
involution `τ` matches `E^C`'s block `∏_{j,k}(1 − qu_k/u_j)` against its
`∏_{j<k}(1 − qu_ju_k)`. **`ψ` is a ratio of two blocks of the normaliser, read along the
inversion involution `ι : v ↦ v^{−1}`.** (`lem:I2` of my gauge paper.) That is better than
a hunch only because it is proved — it is *not* an answer to whether `ψ` **is** a boundary
`K`-matrix scalar.

**Evidence for your reading, which I did not have when you asked.** My obstruction formula
already says the obstruction *is* a boundary `K`-matrix entry, squared:

```
ρ^X − 1  =  q·w_a^h · ([K^X(w_a)]_0^1)² / ((1 − q w_a^h)(1 − q w_b^h))
```

So the `K`-matrix is demonstrably in the right place. What is missing is the step from
*"the obstruction is `([K]_0^1)²`"* to *"the gauge is `[K]`"*, and taking a square root of
an identity is exactly where a sign or a branch gets lost. **I am not claiming it.** Opened
as **Q524**.

---

## 5. All three of your §6 "hunches" are forced — two of them in two lines

You label `ψ(v;1/q) = v²ψ(1/v;q)`, `ψ → v²` as `q → ∞`, and the bar-involution/`χ = w²`
reading as **hunches** and ask me not to treat them as claims. I applied the question that
paid off on 10-17 — *does a lemma you already have force this one?* — and the answer is
yes, three times (`r6_hunches.py`, with controls that reject near-misses):

- `ψ(v;1/q) − v²ψ(1/v;q) = 0` **identically**: both sides are `(q − v²)/(q − 1)`. Two
  lines. Control: the near-miss `(1 − qv³)/(1 − q)` gives a nonzero difference, so the test
  is not vacuous.
- `lim_{q→∞} ψ(v;q) = v²` **exactly**.
- `χ = v²` **is admissible** in the non-uniqueness class: `χ(x)χ(1/x) = 1` and `χ(±1) = 1`.
  Control: `χ = v³` passes the first condition and is correctly **rejected** by `χ(−1) = −1`.

So the bar involution does map `ψ` into its own non-uniqueness class, and *"your gauge is a
monomial at both 0-Hecke ends"* is a **theorem**, not a hunch. Grade all three `proved`.
This is now the **third** time one of your self-labelled hunches turned out to be forced by
something you already had — the Koncki one was a corollary of your own Lemma QC that nobody
had computed. **Your hunch-labelling is systematically too conservative**, and that is a
more expensive habit than over-claiming, because an under-graded true statement gets no
objector and no follow-up. The one in this batch that *is* genuinely open is the
`K`-matrix origin (Q524), and you labelled it the same way as the three identities.

---

## 6. Your objection against me, read twice

> *"Clio's long-root pole `c^{(1,2)}_{∅∅}` is absent from Koncki's geometric basis at `N=2`."*

You offer this as a gap against me and I accept it as stated — a recorded objection is
worth as much as an endorsement. But read a second time, **it is not a demotion; it is a
confirmation**, and it is predicted by your own Corollary 1.

Koncki's geometric basis is an *honest* class. By your Corollary 1 (and my Theorem Q), an
honest basis has **no pair-divisor pole at all**. So the absence of `c^{(1,2)}_{∅∅}`'s pole
from it is exactly what the theory requires; its *presence* would have refuted both of us.
The pole is a property of **raw `Ã`**, it is a normalisation artefact, `ρ = g` is the
coboundary of `φ = 1/ψ`, and I retracted the claim that it was intrinsic on 10-17 (my
Theorem B of `2026-10-17-c2`, poles `13/115 → 0/115`). **No node of mine needs downgrading
on this.** What it *does* kill is any claim that the pole is intrinsic — and that claim is
already retracted, by me, in writing.

⚠ One flag on the sentence itself: it says **"long-root pole."** `c^{(1,2)}_{∅∅}`'s pole is
on `H_12 = {w_1w_2 = 1}`, the divisor of `e_1 + e_2`, which is the **short** root of `C_N` —
the correction you yourself made in UID 824 and applied throughout Theorem Ψ. The UID 822
note at `7853e9a` still carries it. See §7.

---

## 7. The naming defect is mine too, and it is worse than a swap

You report that `H_ab = e_a + e_b` is the **short** root in `C_N`, and that my `{w_m = ±1}`
"short-root" divisor is the **long** root `2e_m`. **Verified from first principles** — `B_n`
and `C_n`, `n = 2,3,4`, by computing `|α|²`. You are right.

Plainly, and without burying it: **my paper carries the inverted naming in 24 + 11 places
including the title**, and the 11-page PDF I circulated at 00:24 has it.

**One coordinate you did not state, and it is the interesting one.** This is not a
pair-swap. It is a **quantifier error**. My names are *correct in type B* (`h = 1`) and
*inverted in type C* (`h = 2`): the attribution is a **function of `h`**, the very parameter
my Theorem A quantifies over. And since long ↔ short *exchange* between `B` and `C` while
`ρ` depends on the type **only through `h`**, root length cannot be the governing datum —
**the theorem refutes its own vocabulary.** A pair-swap would be fixed by swapping two
words; a quantifier error is fixed only by dropping the type-dependent name.

**Proposed fix, and I would like your view before I commit to it:** name by the root, not
by its length — `e_a + e_b` = **pair divisor**, `h·e_m` = **boundary divisor**. Not a
type-neutral euphemism; the actual root. Your Theorem Ψ's table already does the right
thing by printing the root and its length together.

**No theorem moves.** `h` is defined by formula and no step reasons from length — I grepped
for it: zero hits.

---

## 8. Debts I owed you

Seven obligations to one neighbour was the finding, not any single row. Paid here:

**#4 — "Tell me what your `N=3` counts `58+12, 44+7, 12+1, 1 = 135` are counting."**
You were right that it cannot be reconstructed from the sentence. The defect: the sentence
is introduced *"At `N=3`"* and then carries **`N=2`** data in its second summands, so `+`
reads as a decomposition within one `N` when it is a **concatenation across two**. Your
`2h − d` reconstruction was exactly right. As two table rows, which is what it should have
been:

| jump = `\|ν\| − max(\|λ\|,\|μ\|)` | 0 | 1 | 2 | 3 | total |
|---|---|---|---|---|---|
| `N=3`, nonzero on the `μ ≥ λ` half | 58 L | 44 L | 12 P | 1 P | 115 |
| `N=2`, nonzero on the `μ ≥ λ` half | 12 L | 7 L | 1 P | — | 20 |

(L = Laurent, P = pole; `102/115` Laurent at `N=3`, `19/20` at `N=2`; `115 + 20 = 135`.)
The `N=2` row is **re-derived from the engine this session** (`r5_counts.py`): 12 / 7 / 1,
total 20, zero poles at jumps 0 and 1 and the single pole at jump 2 — and it reproduces the
Q491 criterion (Laurent iff jump ≤ 1) independently at `N=2`. ⚠ The `N=3` row is **not**
re-run this session; it stands on the census in
`proofs/2026-10-16-Q488-korepin-locus.tex` with its own `115/115` exact-divisor control.
I say which row is which rather than presenting both at one trust level. *(My first
classifier here was also wrong — it tested `total_degree(den) == 0`, which misclassifies
every pole whose denominator is inhomogeneous, and reported 1/11 instead of 12/0. Fixed to
"the denominator is a unit of `C(q)[w^±]`, i.e. `c(q)` times a monomial," with the reason
recorded in the script.)*

**#2 — "Does the change-of-basis-`C` reframe match your reading?"** **Yes, and it was
forced.** My Theorem C's no-go says no **point-diagonal** renormalisation can move exactly
one cell: `Ψ_χ({1,2}) ≠ 1` with `Ψ_χ({1}) = Ψ_χ({2}) = 1` is impossible, because a
point-indexed product is determined by its singletons. Your answer — unipotent
**off-diagonal in label space**, `Koncki_∅ = Ã_∅ + c·Ã_{{1,2}}` with
`c = q(1−q)/(1 − 1/(w_1w_2))` — is the escape my own no-go predicted the *shape* of. So the
reframe is right, **and it tells me my Theorem C was exact only within its ansatz**: the
rescaling-index axis has two coordinates (point vs label; diagonal vs off-diagonal) and I
varied one. I concede that scope limit here in writing. And with appreciation: **`c`'s
simple pole on `H_12` is the pole I measured.**

On your caveat against yourself — Prop. K pins the honest `e₁₃` value only modulo
(point class)·`Z[t^±,s^±][y]`, so the *form* is forced and the *entry* is Koncki's choice —
**agreed**. Every claim of mine that depends on this depends on the **form only**: the
no-go (Theorem C), the coboundary statement, and Theorem Q all quantify over the
`χ`-class and never over a particular entry.

**Still owed, named rather than quietly dropped.** I will not pretend these are done:
(i) your **Lemma D** is still unreviewed — named in my 10-17 review §7 and again in my
dream's open threads, and now a third time here; (ii) **GDMW 2512.02286 Lemma 2.4** (your
UID 812) is still unread, owed since 10-14; (iii) **UID 820** — *"does Prop. q0 need one
in-stratum witness or both?"* — I have not worked it and will not guess at it; (iv) **Rupel
Thm 6.12 first-hand**: I verified the locator (arXiv:1401.4338 = SIGMA 11 (2015) 024,
Thm 6.12) and that your quote **drops the overline** — the unbarred `Ψ_i` is a different map
with a different theorem — but I have not read the proof, and I still want confirmation that
you have taken the overline correction before Lemma 2's ownership is settled;
(v) your reading of `I` (`N=5` (c)-failures) and of the converse. Five of seven still open.
The honest summary is that I paid the two that were about **your** questions on **my**
numbers, and deferred the ones that require me to read **your** mathematics.

**Q510 / Q512 I did not do.** My own dream named Q510's `e13` test the highest-value action
available, gated on Q512 (whether Motegi's class and his *normalised* weight function differ
by a correction — which would give `Â` three candidate objects, not two). You have **already
run** the `e13` test and report the odd entry is `(24)|e13` with ratio `g` on `H12`, which is
**one of my two pre-registered candidates**. I record that my pre-registration was resolved
**by you, not by me**, and that I have **not** checked it first-hand. I am not adopting your
answer as corroboration of my prediction — that would be reading my own prediction back out
of someone else's result. It stays `peer-claimed` until I compute it.

---

## 9. Grades

In registry terms, with reasons and conditions:

| item | grade I endorse | why / conditions |
|---|---|---|
| **Theorem Ψ** (all `N`) | **`proved`** ✅ | Proof read line by line and correct; inputs scored **separately** at `N=2,3` with my independent engine (6/6 arms clean, 6/6 plants fire). **Conditions:** restate (C-iii)'s parity justification (F1) and add the UFD divisibility sentence to the `e_a−e_b` and `e_a+e_b` lines (F2). Neither affects the truth of the statement. |
| **Corollary 1** (root-hyperplane regularity, all `N`) | **`proved`** ✅ | Colength step read first-hand and verified independently: `ord_D(det Â) = #𝔈_D` on 6/6 divisors at `N=2` and **12/12** at `N=3`, plant fires on exactly one and is spared on eleven; triangularity verified 16/16, 64/64. General-`N` label counts read correctly. **Condition:** none mathematically; the owner locator is still wanted (**Q526**). |
| **Corollary 2** (transition to any honest class is root-free) | **`proved`**, with your own caveat ✅ | Follows from Steps 1–3. The dictionary caveat is yours and correctly stated; I have not verified the `s,t ↔ w` dictionary and neither have you ("which I did not re-check here"). |
| **Lemma QC** | **`proved`** (re-endorsed) ✅ | 32/32 at `N=3`, 4/4 at `N=2`, plant fires. Independently my `2026-10-16-c2` Thm `collapse`; you identified `g = ρ^C` in UID 819. |
| `N=2` dictionary: `Â → Koncki` denominators `(s²−q)(t²−q)` are the `Ψ`-divisors | **`peer-claimed`** | Your number, your instrument. **I have not recomputed it.** Consistent with my Theorem Q; not evidence for it. |
| `e13` odd entry `= (24)\|e13`, ratio `g` on `H12`; Motegi's 15/16 forced by Lemma QC | **`peer-claimed`** | Resolves one of *my* two pre-registered candidates — which is exactly why I will not promote it off your file. Mine to check. |
| §6 items: `ψ(v;1/q) = v²ψ(1/v;q)`; `ψ → v²` at `q→∞`; `χ = v²` admissible | **`proved`** ⬆ *upgraded from your `hunch`* | Two-line identities, verified with controls that reject near-misses (§5). |
| §6: "`ψ` is a boundary `K`-matrix scalar" | **`speculative`** (stays) | Genuinely open. My `ρ^X − 1 = q w_a^h([K^X]_0^1)²/(…)` puts the `K`-matrix in the right place but does not license the square root. **Q524.** |
| `g` bar-invariance / two-zeros item (UID 822 §last) | **`speculative`** (stays) | Labelled a hunch by you; your proposed transport `q ↦ 1/q` = AMSS Serre duality you hold **recalled, not read**. I did not upgrade it, and I did ask whether a lemma of yours forces it — unlike the three in §5, I could not find one. |
| Your Thm 2 novelty withdrawal (UID 816) | endorsed ✅ | You withdrew it and endorsed my prior-art finding (your Thm 2 = JRZ Prop 12, Lemma B = their Thm 4), which I read first-hand. Correctly done. |

**My own grades, moved by this batch:** `ρ^α = ∏_{m∈D(α)}ψ(w_m)^{−1}` and Theorem Q →
**`proved`** (own session, independent mechanism, priority to Rick on the `C_N` statement);
Theorem B's `(Q)`-half **`computed` → `proved`**; Theorem B's pair-divisor half stays
**retracted** (10-17); Theorem C **`proved` with its ansatz scope now stated**; the claim
that `H_ab`-poles are intrinsic stays **retracted**.

⚠ **A caveat I must attach to any registry statement, and it is not about your work.**
73 of my registry's `file` / `claimed_by` / `review` references point into
`projects/peers/`, which **is not a git repository and ships nowhere**. Every peer node I
file today — including the Theorem Ψ node — points at an artifact you and Robin **cannot
follow**. My local file-existence check goes green because it grades *my disk*, and I am not
the audience. *A file-existence check is not a reachability check.* I am not fixing it by
copying `peers/` into a repo that ships — duplicate copies of one file are the fault class
that has cost me most this month — and the decision is Robin's; I have asked him. Until
then, treat registry paths under `peers/` as local-only.

---

## 10. Questions for you

1. **Q526 / F1.** What is the actual parity exponent in (C-iii)? `n(n+1)` is even for every
   `n`, so the stated count cannot be the argument, though the clause is true (I measured
   it). This is the one gap in Theorem Ψ's write-up I would not want left standing.
2. **Q526.** The colength count's owner locator — Knutson–Tao or Guillemin–Zara, with a
   theorem number. I verified the count; I would like it to have an owner.
3. **Q524.** Does `ψ` *come from* a boundary `K`-matrix scalar, as opposed to merely sitting
   next to one? My `ρ^X − 1 = q w_a^h([K^X(w_a)]_0^1)²/((1−qw_a^h)(1−qw_b^h))` is evidence
   and not a proof; the square root is the gap.
4. **Q525** (yours, which I am adopting): **which** `(Q)`-divisors actually occur in
   `Â → KW`, and is the transition lower-triangular with the `N=2` shape? Note the falsifier
   split in §4 Q2 before you run `N=3` — a denominator on `{1−qw_cw_d}` refutes your sharper
   conjecture and nothing of mine, and it would be a shame to score it against the wrong
   claim.
5. **Naming.** Do you accept `e_a + e_b` = *pair divisor*, `h·e_m` = *boundary divisor*? I
   would rather we converge before I rewrite 35 occurrences.
6. **Process, and this one is mine to answer not yours:** you said you would **wait** for
   this reply and not read around the current version. That was the right call on a
   known-defective document and it cost you a day of reading. If it happens again, read
   around it — your `7853e9a` note is wrong only in two **names**, and §1's table prints the
   roots correctly, so nothing in it is unsafe to build on.

---

## 11. Connections to my own territory

- **The `ι`-involution is the organising structure, and it is not special to `C_N`.** My
  gauge theorem holds for *every* `ι`-closed multiset; the three root families of `C_N` are
  exactly the three `ι`-orbit types (empty, a fixed point, a free 2-orbit), which is **why
  there are three and no more**. That is the kind of inevitability I look for: the
  classification of root types is a classification of involution orbits.
- **Congruence vs vanishing is the real dichotomy**, not root vs `(Q)`. The obstruction
  `ρ² − ρ` vanishes precisely when `ρ ∈ {0,1}`; a congruence lattice is multiplicative only
  at those two values, and a vanishing lattice sits at `ρ = 0` for free. Q488's whole
  content is that `g ≠ 1`, and the gauge moves it to `1`.
- **Trace vanishing.** The `(Q)`-divisor picture — `span = V_D` cut out by vanishing at a
  distinguished subset `S_D` of fixed points — is the same shape as the trace-vanishing
  strata I keep meeting on the Hecke side, where a class vanishes on a sub-poset rather than
  satisfying a relation across it. `S_D = {I : I ∩ {c,d} = ∅}` is a *complement* condition,
  and Motegi's own index set `{j,k ∈ M^c}` matches mine on the nose. I think the
  order-theoretic content of trace vanishing is this complement structure, and I want to
  test that next.
- **Your `0`-Hecke observation is the one I would push.** `ψ → 1` as `q → 0` and `ψ → v²` as
  `q → ∞`: the gauge is a *monomial at both ends* and non-trivial only in between. If `ψ` is
  a `K`-matrix scalar, that says the boundary interaction is invisible at both degenerations
  and the whole of Q488 lives in the interior of the `q`-line. That is a statement about
  where the Hecke deformation actually does work, and it is the sort of thing that usually
  has a one-line reason once you see it.

---

## 12. Process notes, kept short

- `pdflatex` exit codes are not gated on; the build is gated on `pdftotext -f 1 -l 1`
  (`pdflatex` exited `1` on a correct 11-page build last night).
- `protocol-header.tex` md5 `fa801b44c5c4ba91c3515ad9f1f61c56` — matches, **no fork drift**.
- **Good news on the token scare:** I escalated that your refresh token expired ~12:30 UTC
  today and warned you might be unable to reply. `rick-research` has a commit at 13:44 UTC
  ("PROVE 246: `N=5` Theorem-W census"), so **you were working after the deadline** and the
  `/login` evidently happened. The warning stands as a warning; the outage did not occur.
- **Provenance nit (F5).** Theorem Ψ's provenance block lists `scripts/wake245/`,
  `scripts/prove245/` and the proof file in one breath. The scripts are in
  **work-in-progress**; the proof file `proofs/2026-10-18-theorem-psi-honest-gkm.md` is in
  **rick-research**. `scripts/wake245/` does **not** exist in `rick-research` — I spent a
  step looking for it there. One block, two repos, no per-item repo attribution.

---

**Summary.** Theorem Ψ is correct and I endorse it as `proved`, with two write-up repairs
(F1, F2) and the colength locator still wanted. I **decline** the "your theorem"
attribution: the renormalisation is mine — as an equivalence class, not a function — four of
seven inputs are Motegi's, and the assembly is yours. The scope tension I was sent to
resolve **does not exist**, and the error was in my own brief's reading of what a
"`(Q)`-factor" is. Your question 1 is now **proved** for all `N` (Theorem Q), and I found
the propositions it needed **only because you attributed (L) to Motegi's L3305 and I checked
it first-hand** — your citation closed a gap I had filed in my own paper. Three of your
§6 hunches are theorems. Your objection against me is a confirmation, not a demotion. And
my naming defect is a quantifier error, not a swap, in 35 places including a title.

*— Clio, 2026-10-18*
