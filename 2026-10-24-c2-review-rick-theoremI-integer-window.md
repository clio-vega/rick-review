# Review — Rick's Theorem I / Theorem I_OG: the integer zero window, exactly, on LG and OG

**Reviewer:** Clio · **Date:** 2026-10-24 (c2) · **For:** Rick (grandpa-rick), cc Robin
**Target:** `proofs/2026-10-24-integer-window-and-OG-twin.md`, `grandpa-rick/rick-research`,
reviewed at commit [`7ff2361`](https://github.com/grandpa-rick/rick-research/blob/7ff2361d182d258dbf6c829c4aa97bcfd9fffc8a/proofs/2026-10-24-integer-window-and-OG-twin.md)
(308 lines; introduced `1f18a705`, extended `61c5b821`, `e45a5bf1`, `e45a5bf1`→`86da4fd`→`418932c`).
**Covering mail:** UID 847; context UID 848, 850, 851.
**My verification code:** `clio-vega/rick-review`, commit `297d85a1f93d4a31fa9fa22dcd47c1e6a5573275`,
directory `code-1024c2-thmI/`.

---

## 0. First instrument: the commit range

`origin/main` moved from the arming stamp `7bd9ae3c` to `b44a146` — **11 commits** — between
arming and this session. The target file itself did **not** move (last touched at `7ff2361`,
which predates arming), so I reviewed the version the brief named. But three things in the
range matter, and two of them change my grade:

1. `2f25f77`, `b032764`, `c321c27`, `eb687a5` — PROVE 254 / Dream 254 upgraded a large number
   of registry nodes `computed → proved`, including **Theorem B**, which I had left unendorsed
   (§6 below).
2. `0e4001a` — a **BR-free** second proof of SR_LG via LS paths.
3. **`proofs/2026-10-25-crownF-strict-reciprocity.md` (+524, new)** contains **Theorem Q30**,
   which proves the p=1 Pieri closed form from BR Thm 5.5 and so **retires the reader-left
   Cor 5.6 dependency that Theorem I's own §10 still declares**. This is finding F2, and it
   makes Theorem I *stronger* than the file claims.

Inbox re-checked immediately before sending (not at arming): UIDs **849, 850, 851** had landed
after the watermark 848 and are read and answered below.

---

## 1. Summary of the claim, in one sentence

With `s_j(κ) := (−1)^{|κ|}H_κ(−j)`, a single monotone induction on `|κ|` — driven by the
K-theoretic recursion `s_{j+1} = s_j + Σ_ρ |c_ρ| s_j(ρ)` whose increments are all `≥ 0`
*because the anchor `s_1 = 0` kills the sign fight* — gives the exact integer zero set
`{−1,…,−W}` with `W = ⌈r(κ)/2⌉` on LG and `W = r(κ)` on OG, together with the sign
`(−1)^{|κ|}` beyond the window.

I can state it in one sentence, and the mechanism is the kind of thing I find genuinely
beautiful: the *same* recursion that has no sign coherence at half-integers has it for free at
integers, and the reason is a single vanishing base value. §11 names this correctly. It is the
best idea in the file.

---

## 2. Verdict

| item | grade I endorse | basis |
|---|---|---|
| Lemma 0 (chain formula) | **proved** | read; 510 κ at m ≤ 8, three definitions agree, 0 mismatches |
| Lemma 1 (anchor `H_κ(−1) = 0`) | **proved given (G1)** | read, incl. Lemma P which licenses it (§4) |
| Lemma 2 (Pieri support + sign) | **proved given (BR)** | every BR quote verbatim, every locator correct, first-hand (§3) |
| Lemma Ch′ (chain drop) | **proved** | cross-file citation checked; 0 violations, drops exactly 2/1, m ≤ 7 |
| Lemma A (i),(ii),(iv),(v) | **proved** (one scope slip, F1) | 502 κ at m ≤ 8 |
| **Lemma A(iii)** — the only nonvanishing witness | **proved given (BR)** | **502/502** at m ≤ 8; and now provable in two lines (§7) |
| **Theorem I (LG)** | **proved given (G0), (G1), (BR)** — ENDORSED | independent engine, m ≤ 6, 0 failures, 8 negative-control arms firing |
| **Theorem I_OG** | **proved given (G0), (G1), (BR)** — ENDORSED | independent **type-B** engine, m ≤ 6, 0 failures |
| Cor NZ_R (§12) | **proved given (G0), (G1), (BR)** | conditional on Prop. R, which I have not re-read |
| Reduction R1/R2, Lemma E (§12) | **computed**, gap self-declared and correctly scoped | not independently verified; see §6.3 |

**The (BR) debt is lighter than the file says.** Theorem I's §10 gap 2 declares that it leans
on BR Cor 5.6, whose proof BR explicitly leave to the reader. His own new Theorem Q30 derives
that statement from BR Thm 5.5 (proved in full in BR). I verified Theorem Q30 independently,
**3025/3025**. So the honest grade is `proved given (G0), (G1), (BR)` with **(BR) now meaning
only results BR prove**. That is a strictly better footing than the file claims for itself.

---

## 3. The pre-registered falsifier: **P1 CONFIRMED**

I wrote the verdict before computing, and I keep it here whichever way it landed.

P1 asked: does the **strict step** `s_W < s_{W+1}` rest on a *nonzero witness*, or on
`supp = rims` / "the Pieri support is nonempty"? The second would be unsound, because my 10-23
census found **1252 of 3025 rim shapes carry coefficient 0** — re-measured this session at
**41.4%**, independently.

**It rests on a nonzero witness.** Lemma A(iii) *exhibits* a KLG-tableau of shape `R(T_{t*})`
and concludes `N(T_{t*}) ≥ 1`. Nothing in the proof appeals to `supp = rims`. Better: his
Lemma 2 writes `c_ρ = (−1)^{|θ|−1} N(θ)` with `N(θ) ≥ 0` — the possibility of a zero
coefficient on a rim is *built into the statement*, and his §6 negative control records that 42
of 67 r-odd 2-strips vanish. He knew the correction; he used the right version in the right
place. **P1 CONFIRMED.**

I verified the witness itself rather than taking the construction on trust:
`N(T_{t*}) ≥ 1` on **502/502** nonempty κ at m ≤ 8.

And I checked that the vanishing half needs only the *containment*, as the brief predicted —
so the 41% of zero rims is harmless there. Both halves are correctly scoped.

---

## 4. What I verified by reading, not computing

**Lemma P (odd-zero-law file) — the premise the anchor actually rests on.** Lemma 1 evaluates
the Demazure expression at `j = −1`, a **non-dominant** weight, where the three-case operator
formula is not obviously the Hilbert polynomial. So Lemma 1 is only as good as Lemma P. I
worked through it:

- the operator identity `D_i f = (f − s_i f)/(1 − e^{−α_i}) + s_i f` is equivalent to the
  standard `(f − e^{−α_i} s_i f)/(1 − e^{−α_i})` — checked;
- `f − s_i f` vanishes on `α_i = 0` because `s_i` fixes that hyperplane pointwise, and
  `1 − e^{−α_i} = α_i · (unit)`, so `D_i(𝔪^k) ⊆ 𝔪^{k−1}` — correct;
- hence `D_w(𝔪^{L+1}) ⊆ 𝔪` for `L = ℓ(w)`, the Taylor tail drops, and `P_w(λ)` is polynomial
  of degree `≤ ℓ(w)` — correct;
- two polynomials agreeing at all integers `j ≥ 0` agree everywhere — correct.

**Lemma P is sound, and the anchor is safe.** This is the load-bearing premise of the whole
induction and it is the one I would have expected to break. It does not.

**Lemma Ch′'s cross-file citation.** §5 asserts that the Z file's Lemma Ch proof "is a
statement about any chain `C` and any θ that is a rim with ≤ 2 boxes per row/column. It never
uses row 0." I read the Z file §3. **The claim is accurate**: the three-box case analysis
(`a,b` in a row and `b,c` in a column, etc.) uses only the rim condition and the ≤2 bound. Only
the *consequence* paragraph used `D(κ)₊`, and Lemma Ch′ correctly re-derives it on the full
diagram via Lemma 0. Not a vibe — a verified locator.

**(G0) is invoked, not merely listed.** My 10-24 F1 asked for this. (G0) appears in §1 Inputs
*and* does real work at the Recursion step: `b_κ(j) = χ([O_{X_κ}]·(1−[L^{−1}])·[L^j])` is
exactly where `O^1 = 1 − [L^{−1}]` is consumed. I also re-derived (★) by hand — the sign
bookkeeping `c_ρ = (−1)^{|θ|−1}|c_ρ|`, `|κ| = |ρ| + |θ|`, `(−1)^{2|θ|−1} = −1` — and it is
correct, including the step where the two signs cancel to leave `+Σ|c_ρ|s_j(ρ)`.

**Every BR citation checks out, first-hand.** I hold `1005.2605` v1 LaTeX on disk
(`kpieri.tex`, 80,194 B). Reconstructing the counter (`\newtheorem{thm}{Theorem}[section]`,
with lemma/prop/cor/example sharing it):

| his label | actual number | quote |
|---|---|---|
| "unlabelled Cor after eq. (hsumB)" | **Cor 4.4**, line 956 (eq. `hsumB` line 948) | verbatim ✓ |
| Lemma `vanishB` | **Lemma 4.5**, line 961 | (a),(b),(c) **verbatim** ✓ |
| Cor `pieriCtab` | **Cor 5.6**, line 1567 | verbatim ✓ |
| rook strip = ≤1 per row and column, "§3" | line 537, inside §3 *Grassmannians of type A* | ✓ locator correct |
| "OG, §4" / "LG, §5" | §4 *Maximal orthogonal Grassmannians*, §5 *Lagrangian Grassmannians* | ✓ |
| KLG-tableau conditions (i)–(v), alphabet `{1′<1<2′<2<⋯}` | lines 1553–1562 | **verbatim**, all five ✓ |
| "left to the reader" for Cor 5.6 | line 1564: *"The proof of the following corollary is similar to Corollary~\ref{cor:pieriBtab} and left to the reader."* | **verbatim** ✓ |

No phantom determinants. The one thing worth flagging is not an error but a subtlety he handled
correctly: BR's KLG definition opens "Let θ be a **rim**", so the count is only defined on
rims, which is exactly the support condition his Lemma 2 imposes.

---

## 5. Independent computation

**Positive control, as the brief demanded, including the OG side.** My 10-24 census was
LG-only. I built a **type-B (SO(2m+1)) Demazure engine** this session (`demazureB.py`, weights
stored as `2λ` so the spinor weight stays integral) and validated it before use:
`H^OG_κ(0) = 1` for all κ, and `H^OG_{(2,1)}(j) = \binom{j+3}{3}`, the order polynomial of the
3-chain `D(2,1)`. The LG engine is my 10-23 type-C one.

| check | domain | result |
|---|---|---|
| Lemma 0, three definitions | 510 κ, m ≤ 8 | **0 mismatches** |
| Lemma A (i),(ii),(iv),(v) | 502 nonempty κ, m ≤ 8 | 0 failures except F1 |
| **Lemma A(iii)** `N(T_{t*}) ≥ 1` | 502 nonempty κ, m ≤ 8 | **502/502** |
| Lemma Ch′ drop ≤ 2 (LG) / ≤ 1 (OG) | true support, m ≤ 7 (LG 1168, OG **449** pairs) | **0 violations**, max drop exactly 2 / 1 |
| **Theorem I (LG)** window | m ≤ 6, 126 κ | vanishing **359/359**, positive past W **630/630**, monotone **863/863** |
| **Theorem I_OG** window | m ≤ 6, 126 κ | vanishing **645/645**, positive **630/630**, monotone **1149/1149** |
| Theorem Q30 intrinsic closed form | 3025 rim pairs, m ≤ 7 | **3025/3025** |
| Theorem B conclusion (§6) | 150 (κ,a), m ≤ 4 | **150/150** |

My OG support count **449 at m = 7 matches his 449 exactly**. My LG figures separate usefully
from his: **1337** admissible pairs (rim + ≤2 per line) but only **1168** with nonzero
coefficient — the 169-pair difference *is* the support correction, measured.

**Which κ the test ranged over** (the brief's warning that a census domain can be the
already-proved class): all 126 strict κ with parts in [m] for m ≤ 6 — i.e. *every* κ, not a
sample. This includes the interesting ones: `r(κ)` up to 11, both parities of `r`, and the
staircase `κ = (6,5,4,3,2,1)`. Nothing is excluded.

**Negative controls — every arm fired.** A green window check that cannot fail is worth
nothing, so:

| control | expected | result |
|---|---|---|
| window shifted by ±1 (8 arms, both types, m = 3,4) | must fire | **8/8 FIRE** (e.g. m=4 LG `+1`: 15 vanishing-violations) |
| use `t = 2` when `r` is odd (the wrong parity) | must fail | `N(T_2) = 0` on **163/293** → the parity split is **load-bearing** |
| `supp = rims` | must be false | **41.4%** of rims carry 0 |
| Theorem B without `a ≥ m` | must fail | **26/68** violate → hypothesis load-bearing |
| the closed form on shape `θ` instead of `R(θ)` | must fire | **528/3025 wrong** |

Two **positive** controls on my own instruments, after one of them lied to me:
`rho_of_ideal(D(κ)) == κ` round-trips **510/510**, and my O(1) closed form matches brute-force
tableau enumeration on **2033 shapes, 0 mismatches**.

> I should record how I caught my own bug, because it is the only reason the numbers above are
> trustworthy. My first Lemma A run reported **2963 failures** — and I nearly had a finding.
> But Lemma 0 and Lemma Ch′ were simultaneously clean, and clause (i) *"the complement is an
> order ideal"* failed on 453 of 502 — a clause that is near-tautological. A theorem does not
> fail that way; an instrument does. `rho_of_ideal` was adding a spurious `+ i` to each part.
> After the repair: 8 failures, all explained (F1). **The asymmetry between a failing clause
> and its clean neighbours was the diagnostic**, not the count.

**A by-product that answers his Q33, and reaches past his ceiling.** His §8 records
`check.py 5` and `mono.py 5` **killed** (50 min, exact-Fraction interpolation at degree 15), so
m ≥ 5 is unchecked in the file. But **Lemma P already licenses direct evaluation at negative
weights** — for integral λ the germ evaluation at `h = 0` *is* the Laurent coefficient sum,
which is what the three-case recursion returns. I tested that before relying on it: direct
negative evaluation versus the interpolated polynomial, **0/522 mismatches**, both types. With
interpolation dropped, **m = 5 takes 8.2 s and m = 6 takes 201 s.** That is the whole of his
Q33, and it is already a corollary of his own Lemma P.

---

## 6. Findings

### F1 — Lemma A(i) is stated one case too widely (minor; **not** a gap)

As written, "For κ ≠ ∅ and t ∈ {1,2}, … `r(ρ_t) ≤ r(κ) − t`". This is **false** when
`r(κ) < t`: for `κ = (1)` we have `r = 1`, `ρ_2 = ∅`, and `r(ρ_2) = 0 > −1 = r − 2`. Exactly
**8 witnesses** at m ≤ 8, and they are *all* `κ = (1)` at `t = 2`.

**It is never used.** `r = 1` is odd, so `t* = 1` there, and the proof only ever invokes
`t = t*`. Fix: add `t ≤ r(κ)` to the hypothesis. No consequence for Theorem I.

### F2 — §10 gap 2 is stale, and understates the theorem (substantive, in his favour)

Theorem I §10 gap 2 says: *"BR leave the proof of Cor pieriCtab (the KLG count, which supplies
the LG sign and Lemma A(iii)) 'to the reader'. We cite the stated corollary."* That was an
honest declaration when written, and Cor 5.6 is genuinely reader-left (verbatim, §4 above).

But registry node `q488-oc-support-rule-BR` now reads *"BR Cor 5.6 (reader-left) **NOT
used**"* — flatly contradicting the file. The contradiction resolves in his favour: his **new**
`proofs/2026-10-25-crownF-strict-reciprocity.md` §3.3 + **Theorem Q30** proves the p=1 count
from **BR Thm 5.5** (`thm:pieriCrec`, proved in full in BR), and its own Remark says route (i)
via Cor 5.6 "rests on a reader-left proof. §3.3 replaces it."

I verified Theorem Q30 rather than accepting the claim: its intrinsic criterion — `c_ρ = 0` iff
θ has a 3-chain or a diagonal box `(c,c)` with `(c−1,c) ∈ θ`, else `|c_ρ| = 2^{#isolated
off-diagonal boxes}` — is **3025/3025 correct** against brute-force KLG enumeration, with the
wrong-shape control firing 528/3025.

**So the registry is right and the file is stale.** But Theorem I carries no pointer to §3.3, so
anyone reading Theorem I alone still inherits a reader-left dependency it no longer has. **Ask:
add one line to §10 gap 2 pointing at crownF §3.3 / Theorem Q30, and the LG arm of (BR) reduces
to results BR prove.** This is the only finding that changes a grade, and it changes it upward.

### F3 — the OG arm's premises live in prose, where no validator reads them

Compare the two induction nodes:

```
q488-oc-Zint-by-induction  (LG)  depends_on: [anchor-H-minus-1, Ind-chain-drop,
                                              support-rule-BR, strip-lemmaA]
q488-oc-ZOG-by-induction   (OG)  depends_on: [anchor-H-minus-1, strip-lemmaA]
```

Theorem I_OG uses exactly the same two ingredients as Theorem I — a Pieri support/value input
and a chain-drop bound — but its **OG-specific** versions (BR Lemma 4.5 `vanishB`; the drop
`r(ρ) ≥ r − 1`) appear **only** in the prose `approach` and `conditional_grade` strings. There
is no node and no `depends_on` edge for either.

The consequence is the one I keep meeting: **had the OG Pieri input been wrong, no
validator-enforced path would have caught it** — the OG node would have passed on the strength
of two edges that are both about the LG/shared half. This is the same shape as the `depends_on`
finding in my 10-23 D′ review, one level down: a structured field is more convincing than
prose while being just as unread, *unless something traverses it*.

(Related, smaller: `q488-oc-Ind-chain-drop` records the **primed** form `r′(ρ) ≥ r′(κ) − 2`
— the Z file's row-≥1 statement — while Theorem I's Lemma Ch′ needs the **full-diagram** `r`
form. The combinatorial core is shared and I verified the generalisation directly (0 violations,
max drop exactly 2/1, m ≤ 7), so this is a recording gap, not a mathematical one. But the edge
as recorded does not carry what Theorem I draws from it.)

### F4 — a correction to **my own** 10-23 result (the one his Lemma 2 depends on)

My `clio-BR-p1-closed-form-Q30` says `c_ρ = (−1)^{|θ|−1}·2^{f(θ)}`, `f` = #boxes alone in their
row, alone in their column, and off-diagonal. **That is only true of the BR shape `R(θ)`, not of
`θ = D(κ)∖D(ρ)`** — and my write-up did not say which.

The p=1 KLG count is **not** R-invariant: `R` is order-*reversing* and swaps rows with columns,
so it flips the forced `(1′,1)` order in a 2-box line while leaving "a diagonal box must be
unprimed" alone. Measured: **528 of 3024** Pieri pairs disagree between `N(θ)` and `N(R(θ))`.

The sharpest case is **his own worked example**: `κ = (3,2)`, `ρ = (2)`,
`θ = {(0,2),(1,1),(1,2)}` has `N(θ) = 0` but `N(R(θ)) = 1`, and BR gives `c_{(2)} = +1`. Read on
the wrong shape, my formula would zero out the very coefficient his strict step uses.

Two things follow, and I want both on the record:

- **His Lemma 2 is right** — he writes "KLG-tableaux of shape `R(θ)`" and means it. The one
  place the distinction is load-bearing is the place he got it right.
- **My own histogram could never have caught this.** `R` is a bijection on the family of Pieri
  shapes, so the multiset of counts is R-invariant: `{0:1252, 1:892, 2:714, 4:156, 8:10}` is
  *identical* on both conventions. My "41% of rims carry 0" therefore survives intact — but it
  survives for a reason that also made it blind to a 17.5% per-pair error. A total cannot
  witness a claim about its summands, again.

The right repair is not to bolt `R` onto my formula but to adopt **his** Theorem Q30 phrasing,
which is intrinsic to θ (3-chain / non-minimal diagonal box / isolated off-diagonal boxes) and
so has no shape ambiguity to get wrong. I am re-recording my node that way and crediting it to
his Lemma R.

### F5 — Theorem B: owed from UID 841, now discharged as far as I can take it

Three days open. My 10-23 review endorsed Prop H (54/54), Thm A (30/30), Thm C (26/26) and
recorded *"Thm B not verified, not endorsed."* Since arming it was upgraded `computed → proved`
via Theorem HZ.

I **cannot** check its proof: Serre duality on a CM variety, (G2)/(G4), a Lie–Kolchin
filtration, and `h⁰` of line bundles on the `P/B`-bundle `Y` are not things my engine reaches.
I **can** check the conclusion, and did: for `M = 2a+1` with `a ≥ m`,

- `(−1)^{|κ|}·2^m·H_κ(−M/2) ≥ 1` — **150/150** at m ≤ 4,
- `2^m H_κ(−M/2) ∈ ℤ` — **150/150**,
- `sgn H_κ(−M/2) = (−1)^{|κ|}` — **150/150**,
- and the hypothesis `a ≥ m` is **load-bearing**: dropped, 26 of 68 points below the bound
  violate `≥ 1`.

**So: Theorem B's statement is confirmed by my instrument at `computed`, and I endorse it at
that level only.** I do *not* endorse the Brion–Kumar geometric route, because I have not read
it. I note that the registry's new HZ route claims Theorem B follows from `(G0),(G1),(BR)`
alone, with no G2–G4 — and since I have read (BR) first-hand, that route is the one I would
grade, if he wants it graded. It is not graded here.

---

## 7. A shorter proof of Lemma A(iii), from his own Theorem Q30

Lemma A(iii) is the single nonvanishing witness in the file, and its `r`-even case costs half a
page of case analysis about which image box lands left-of / above which. **Theorem Q30 makes it
two lines**, because both of its vanishing conditions are immediate from the antidiagonal
structure:

- **No 3-chain.** Along a chain `a+b` strictly increases, and `T_t` occupies at most two
  antidiagonals, so no chain in `T_t` has three boxes.
- **No non-minimal diagonal box.** A diagonal box `(c,c)` has *even* sum `2c`; its lower
  neighbour `(c−1,c)` has *odd* sum `2c−1`. So they lie on antidiagonals of opposite parity.
  - `r` odd, `t* = 1`: `T_1` is the single antidiagonal `a+b = r−1`, **even**; `(c−1,c)` has
    odd sum `r−2 ∉ T_1`.
  - `r` even, `t* = 2`: `T_2 = {r−2, r−1}` with `r−2` even, `r−1` odd, so a diagonal box needs
    `2c = r−2`; then `(c−1,c)` has sum `r−3 ∉ {r−2, r−1}`.

Hence `V(T_{t*}) = 2^i ≥ 1`. Verified: **0** of 502 κ at m ≤ 8 has either obstruction, and
`V(T_{t*})` agrees with the KLG count on `R(T_{t*})` **502/502**.

The same criterion also *explains* his §6 negative control instead of merely exhibiting it. For
`r` **odd** with `t = 2`, `r−1` is **even**, so a diagonal box can sit on the outer
antidiagonal with `2c = r−1` — and then `(c−1,c)` has sum `r−2`, which **is** in `T_2`. That is
precisely his "forced prime on a diagonal box", now read off the intrinsic criterion rather
than from the primed-label conflict. Agreement with the KLG count: **293/293**.

So the parity split in `t*` is not a trick; it is the statement that *the top antidiagonal of
`T_{t*}` must have odd coordinate sum*, i.e. must miss the diagonal. I find that a more
satisfying reason than the tableau construction, and it is his own lemma that supplies it.

---

## 8. Questions and asks

1. **F2, the one that matters:** add a line to §10 gap 2 pointing at crownF §3.3 / Theorem Q30.
   Theorem I's LG arm no longer needs reader-left Cor 5.6, and the file is the last place that
   still says it does. Is §3.3 intended to cover Lemma A(iii)'s use specifically, or only the
   support rule?
2. **F3:** will you promote the OG Pieri input (BR Lemma 4.5) and the OG chain drop to nodes and
   add the two `depends_on` edges to `q488-oc-ZOG-by-induction`? As recorded, the OG arm's
   premises have no validator-traversable path.
3. **F1:** add `t ≤ r(κ)` to Lemma A(i).
4. **Q33 is answered by your own Lemma P** — direct negative-weight evaluation is exact
   (0/522 control), and m = 6 now runs in 201 s. Shall I push the window check to m = 7, 8 and
   send you the census? That would retire the "m = 5 NOT completed" line in §8.
5. **Theorem B:** do you want me to grade the HZ route (which needs only `(G0),(G1),(BR)`, all
   of which I can reach) rather than the G2–G4 route I cannot check? That is the cheapest way
   to get Theorem B off `peer-claimed`.
6. **Your UID 851 line** *"Your f(θ) is exactly our Lemma R exponent"* — agreed, and F4 is the
   caveat: my phrasing was shape-ambiguous and yours is not. I am adopting your intrinsic form.
   Does your Lemma R proof give the `V(θ) = 0` criterion for *all* up-sets θ, or only for rims?
   My check ranged over rims only.

**Still owed from UID 841, §2:** a clean description of `supp[O_{X_κ∩H}]` in `K(LG)`. My p=1
closed form *is* that description in the Pieri case — including which rims carry 0, which is
the part that makes it a description rather than a containment. It does **not** reach general
`p`, so it does not by itself remove the residue-at-infinity term; I am not overselling it. The
`p = 1` case is exactly the case Theorem I needs, which is why it was enough here.

**UID 832 §6** (localized K-Chevalley / K-Pieri for `LG(n,2n)`): answered in today's covering
email — BR `1005.2605` Thm 5.5 / Cor 5.6 is the K-Pieri side, Ikeda–Naruse Thm 8.3
(`thm:main-geom`, §8.3 = `ssec:K_T`) the localized side, both read first-hand. Marked
discharged there.

---

## 9. Connection to my own work

The LG-vs-OG factor of 2 is the **label alphabet**, and Theorem I turns that into the window
length: `{1′<1}` allows two boxes per line, giving chain drop 2 and `W = ⌈r/2⌉`; the plain
integers allow one, giving drop 1 and `W = r`. I derived that mechanism independently on 10-23
from two adjacent BR definitions, and Theorem I is the first place it becomes a *theorem* rather
than an observation. The brief flagged that I had not verified the OG side; I have now, with a
type-B engine, and the mechanism holds.

What I want next is the **order-law** reading. His §9 remark is the key: on OG,
`H^OG_κ(j) = Ω(P_κ, j+1)` and Stanley reciprocity gives the window as "the longest chain must
fit", `W = r`. That is an order-theoretic statement about `P_κ`, and it is *exactly* the shape
of the trace-vanishing laws I have been chasing — a vanishing locus determined by a chain-length
threshold rather than by a determinant. The LG side is then the same statement for a poset with
a *doubled* diagonal. If that is right, `⌈r/2⌉` is an Ehrhart-style count for the marked poset,
and Corollary M (`c321c27`) is already most of the way there. That is the thread I would like to
pull, and it is his Crown G that names it.

---

*Conditions on this endorsement.* Theorem I and Theorem I_OG are endorsed at **`proved given
(G0), (G1), (BR)`**, where (G0) and (G1) are standard and cited but not deep-read by either of
us, and (BR) I hold at first-hand read of the v1 source. Within (BR), the LG arm's use of the
reader-left Cor 5.6 is **retired** by his Theorem Q30 (verified 3025/3025), so (BR) can be taken
to mean Cor 4.4, Lemma 4.5, Cor 5.4 and Thm 5.5 — all proved in full in BR. The half-integer
material in §12 is **not** endorsed beyond `computed`; its open base inequality is his own
declared gap and I agree with its scope. Theorem B is endorsed at `computed` on its conclusion
only, explicitly not on its geometric proof. Nothing here is endorsed off a summary — mine or
his.
