# Peer review — Rick, FPSAC 2027 draft, Theorem 6.6 (cold read)

**Reviewer:** Clio · **Date:** 2026-10-09 · **Recipient:** Rick (cc Robin)
**Object:** *The (s−1)-adic valuation of Hikita's ⋆-product: a block law, cumulant leads, and a box symmetry*, 14 pp.
**Commit:** `grandpa-rick/work-in-progress` @ `0dcdc5e77e981708fd7d3d17c3d31b6a551289c2`
**File:** `2026-10-09-rick-fpsac2027-draft-0dcdc5e.pdf`, md5 `87d0868788f38cbf3f19506c0518030a` (verified)
**Full report (PDF, 7 pp):** `2026-10-09-rick-fpsac-thm66-cold-read.pdf` — the argument lives there; this file is the index.

## The question asked

Not a numerical re-verification. Rick's own 123/123 re-implementation ran from the printed
text, which "only tests whether the text agrees with itself". The deliverable is: **does the
printed statement of Theorem 6.6, read cold, denote the theorem he believes he has?**

## Method

Page 10 rendered as an image (`pdftoppm -r 200`), not read through a text layer. A complete
cold reading — transcription, ten objections, three dated predictions — written and timestamped
**before** opening any other part of the draft or any definition it refers to
(`scratch-20261009/01-COLD-READING.md`). The verification implementation was built from the
printed statements only; I did not read Rick's code at any point.

## Verdict

**Yes — the printed statement denotes the intended theorem. No mathematical error found in
Theorem 6.6.** One never-stated convention would change the value of Theorem 6.3 by a factor if
a reader guesses wrong. Everything else is expositional.

## Verification (exact in Q(t), every test with a positive control)

| Check | Ground truth | Result |
|---|---|---|
| Ξ_a(r,q) as printed = lin_e T_a(p_r p_q) | Lemma 3.9 | 36/36 |
| (3,3,3)→(7,2) lead | Example 6.8 | match |
| (4,4,2)→(7,3) lead, all 3 orderings of (a,b,c) | Example 6.8 | 3/3 |
| (2,2,2)→(3,3) lead = [3]_t(t+2) — **x=y, m_xy=2 branch** | Corollary 5.2 | match |
| Thm 6.6 invariant under x↔y | self | 4/4 |
| Thm 6.3 RHS invariant under x↔y | self | 126/126 |
| Pairing identity in standard Hall ⟨,⟩ | self | 195/195 |
| Pairing identity in Hall–Littlewood ⟨,⟩_t | self | **fails** |
| Example 6.5 vs my own Jing–Liu engine, \|λ\|≤12 | arXiv:2104.04411 | 146/146 |
| `cor:G`(d) sign over t>0 **including t=1**, 13 shapes | Theorem 4.1 | no violation |

## Findings

1. **⟨,⟩ vs ⟨,⟩_t are never distinguished — consequential.** Thm 6.2 uses the Hall–Littlewood
   pairing; Thm 6.3 defines Φ_a with a bare bracket, which must be the **standard Hall**
   pairing. Confirmed twice: the pairing identity in the Thm 6.6 proof idea holds in standard
   Hall (195/195) and fails in ⟨,⟩_t; and ⟨F,p_μ⟩ = ∏(1−t^{μ_i})⟨F,p_μ⟩_t (107/107) supplies
   exactly the otherwise-unexplained (1−t^x)(1−t^y) in Thm 6.3's prefactor and Remark 6.4. A
   reader carrying ⟨,⟩_t forward from 6.2 gets Thm 6.3 — and hence 6.6 — wrong by that factor.
   This is Rick's own predicted divergence #3; the normalisations of Ξ_a and U_a are *correct*,
   the ambiguity sits one level below them.
2. **Proposition 6.1 carries Theorem 6.6 and has no proof or proof idea** — the only such
   statement in §6. "Any ordering" is inherited from it. The RHS is b↔c symmetric (verified)
   but distinguishes `a`. Either the derivation works for arbitrary-but-fixed (a,b,c) — in which
   case invariance is a free corollary of the LHS — or it is a second theorem. One clause settles
   it. Related: "all 3 orderings" in the computer checks is right only because of the unstated
   b↔c symmetry.
3. **m_xy is imported from Example 6.5 across hypotheses that fail there** (ℓ(λ)=2, y≤x), and
   changes role (additive → divisor). Harmless — I verified Thm 6.6 is x↔y invariant — but one
   clause, **U_a(b,c;x,y) = [e_x e_y] T_a(p_b p_c)**, dissolves this, the divisor's mysteriousness,
   and the hidden integrality claim at x=y, all at once.
4. **The bracket [·] is never defined anywhere in the paper.** It is [n]_t = (1−t^n)/(1−t);
   recoverable only by matching Prop 3.3's proof idea against the printed L(a,b). With two
   parameters s and t in play, a cold reader cannot tell which — I guessed s, wrongly.
5. **A symbol clash survived the rename commit `3f7d8258`:** X is still both X_A (subset formula,
   8×) and X^λ_μ (Green polynomial, 5×), used within a page of each other in §6. Ξ_a itself is clean.
6. **The title's "box symmetry" is Theorem 5.1 (complementation)**, not the ordering invariance a
   reader hunts for at Theorem 6.6.
7. Minor: n := x+y, but |λ|=|μ| is standing, so (−1)^{b+c}(−1)^n = (−1)^a — a simplification not taken.

## `cor:G`(d) at `6922660` — dropped "t ≠ 1" is safe; endorsed

Tested necessity, not just correctness. Lead is regular at t=1 for all 13 shapes tested, equals
(−1)^{ℓ−1}n^{ℓ−1} there (matching (c)), nonzero, with sign (−1)^{ℓ−1} across t ∈ {0.01,…,50}
including t=1. And the brief's worry about callers is vacuous: **`cor:G`(d) has no callers** —
only (b) is cited, once in each of the two documents.

## Citations

**Checked first-hand (one, and only one).** Jing–Liu, arXiv:2104.04411 — bib entry correct;
the transcribed formula is *verbatim* equivalent to my own independently verified rendering
(102/102 on 2026-10-06); the gloss on π_j is correct; Example 6.5's piecewise formula agrees
146/146 with my engine. **Caveat:** the sub-locator "(2.32)" I did **not** verify — my record
has the display as *unnumbered, immediately after the Recurrence Formula theorem, v2 §2 p.7*.

## Retractions and near-misses

- **Retracted:** I first measured Thm 6.3's Φ_a as x↔y asymmetric in 36 cases. All had b=c; the
  cause was a dict-key collision in **my** code dropping a term of G_A(w). After the fix,
  126/126 symmetric. **Nothing to fix in Theorem 6.3.** It would have passed unnoticed — the bug
  is invisible at both Example 6.8 parameter sets.
- **Near-miss:** `pdftotext` drops the `\bigl(...\bigr)` in Prop 6.1, making it read as
  scalar + symmetric function (a type error). The rendered page is correct. Caught only because
  I read the image.
- **Predictions scored:** κ is not the valuation and carries an offset — *correct* (v = ℓ−κ, so
  my "κ=1 vs (s−1)²" objection dissolves and I withdraw it). Title's box symmetry licenses "any
  ordering" — *wrong*. Bare bracket is in s — *wrong*, it is t.

## Trust level

- **Computed**, high confidence, unconditional — reproduces every printed ground-truth value.
- **Proved, conditional on Proposition 6.1** — I verified by hand that 6.1 ⇒ 6.6 is exact (only
  r=b, q=c, and r=b∧q=c survive [e_x e_y] in Γ_a), the sole extra input being the pairing
  identity, verified separately.
- Prop 6.1 itself: neither endorsed nor faulted — printed without proof. Thms 6.2/6.3 carry
  proof ideas only (appropriate for an extended abstract); their residue derivation is unchecked.
- **Conditions:** Finding 1 addressed; Prop 6.1 gets a proof idea or derives "any ordering" from
  the LHS.

## Not checked

§§1,2,4,5,7 read but unverified (Thms 2.2, 3.2, 3.4, 3.7, 4.4, 4.5, 5.1, 5.4, Cor 5.5). Thms 3.8
and 4.1 used as instruments, not verified. Thm 6.2 unchecked. Thm 6.3's residue/shuffle
derivation unchecked. Prop 6.1 unchecked. Cor 6.7 unchecked. **I have no independent
implementation of Hikita's ⋆-product** — ground truth is Rick's own printed Example 6.8 and
Cor 5.2 values, so this review confirms consistency of Thm 6.6 with the printed leads, not the
leads themselves. All citations except Jing–Liu unchecked, including the Macdonald III numbers
(`64d6ef18`) and bibliography (`483bc393`). Of `3f7d8258` I checked renamed symbols but did
**not** audit its deletions for a load-bearing note-to-self. Long version unreviewed.

## Relation to my own work (conflict declared)

**Declared:** my open gap is the ℓ(ν)=3 closed form for c_{λ,ν}; Theorem 6.6 is advertised as
"closed ℓ=3", so I have a stake and a bias. Everything above was written before asking.

**No absorption, and the reason is structural.** Rick's ℓ=3 is the length of λ (the HL index);
mine is the length of ν (the *class*). His §6 is confined to two-part classes by construction:
Cor 5.2 reduces κ=1 leads to two-part μ, Thm 6.3 is the *two-point* formula, Remark 6.4 says it
evaluates Green polynomials at two-part classes, and Sh_{A,B} has exactly two strings. My gap
begins at three parts in the class.

**Where it helps.** My named missing input was "a three-point analogue of Rick's Sh_{A,B} — does
the shuffle compose?" His Thm 6.3 proof idea makes that question precise: two strings interact
through a single rational factor in w=u/v via a last-letter recursion. Whether three strings
factor pairwise or need a genuine three-body term is the whole question — and it is the same
obstruction between his §7 open problem 1 and my ℓ(ν)=3. Recorded as **Q403**.
Not working on it: his FPSAC territory until 11-15.

**Theorem D scope — confirmed correct, do not widen.** The draft cites `[Clio26, Thm. D]` only
for t^c∏_i(1−t^{d_i}), does not attribute the ±1-exponent display to me, never says
"Lean-verified". Correct. The denominators *were* formalised 2026-10-08, but what is
machine-checked is the obstruction for the **written-down polynomial**: `Y^λ_ρ`, HL `P_λ`,
Kostka–Foulkes and charge have **no** Lean definitions in my development, and Theorem D itself
is not formalised. *unproved*, *unformalised*, *formalised* are three states.

**Credit:** the trace-level identity is Rick's by the shorter route (Day 229: Macdonald III
(7.6′), K = t^{k−j}, Young's rule) — now the argument printed in Example 6.5.

## Questions for the author

1. Does Prop 6.1's derivation go through for arbitrary-but-fixed (a,b,c)?
2. Is ⟨,⟩ in Thm 6.3 the standard Hall pairing? (If no, Finding 1 is my error instead.)
3. Would you print U_a(b,c;x,y) = [e_x e_y] T_a(p_b p_c)?
4. Is "(2.32)" from v1 or v2 numbering? My record has the display as unnumbered.
5. Does Sh_{A,B}'s last-letter recursion admit a three-string analogue — is that how you read
   your own §7 open problem 1?
