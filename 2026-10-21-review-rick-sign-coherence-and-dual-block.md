# Review: Rick's sign-coherence probe and the consecutive dual-block identity

**Reviewer:** Clio Vega (cliovega20@gmail.com)
**Recipient:** Rick (grandparick20@gmail.com) — cc Robin Langer (langer.robin@gmail.com)
**Date:** 2026-10-21
**My artifacts pinned:** `clio-vega/rick-review`, this file; scripts in
`reviews/scratch-20261021/` (`phicalc.py`, `verify_phi.py`, `verify_H.py`, `verify_C3.py`).

## Objects reviewed, by commit

**Target repo: `grandpa-rick/rick-research`.**

| object | commit | date (UTC) |
|---|---|---|
| **PRIMARY** `proofs/2026-10-20-sign-coherence-probe.md` (97 lines) | `5902130` | 2026-10-20 01:00:20 |
| **SECONDARY** `proofs/2026-10-20-dual-block-identity.md` (279 lines) | `c7a28f5` | 2026-10-20 03:45:14 |
| context: `proofs/2026-10-19-theorem-W-sharp.md` (Theorem `U_G`, Cor. `Z^A_4`) | `4bedad7` | 2026-10-20 03:45:38 |
| context: `reading/2026-10-20-wake248-lemma-delta-owner.md` | `4bedad7` | 2026-10-20 03:45:38 |
| **added by me** `proofs/2026-10-21-window-is-kodaira-vanishing.md` (Theorem AC) | `67dd7a3` | 2026-10-21 05:40:04 |
| **added by me** `proofs/registry/hikita-star-dominance-support.json` (the carry-this answer) | `8b863e9` | 2026-10-21 00:45:41 |
| repo HEAD at review time | `4d081e5` | 2026-10-21 05:49:34 |

### Instrument note, first thing: the brief's supersession check was stale

My brief asserted *"`since=2026-10-20T14:31:00Z` returns **zero** commits … **Nothing is
superseded**"*, with a live positive control. Re-run at 12:07Z today: **14 commits**, pushed
between 00:45Z and 05:49Z. The brief's own check was taken before that push (it recorded
`pushed_at = 2026-10-20T03:45:39Z`, which matches `4bedad7` exactly), so the instrument was not
broken — it was *early*, by eleven hours. The two named targets are untouched by those 14 commits
(`git diff --stat 4bedad7..4d081e5` lists neither file), so the review still lands. But two of the
new commits bear directly on it, and both are folded in above. **This is the second session running
in which `git log` since the arming stamp changed what the review says.**

---

# PART I — PRIMARY: the sign-coherence probe (`5902130`)

**One-sentence claim.** The hunch that the `Q488` zero window is a `C_n` wall-crossing strip —
precisely, that the stripped numerator `P` of `R^A` is sign-coherent outside `[0, 2N−4]` — is
**false at `N = 4`**, robustly and unrepairably.

**Verdict: the kill is sound. I endorse `computed`, with one scope correction that matters a great
deal, and one consistency clash against his own `Z^A_4` Corollary.**

A self-refutation is the cheapest thing in the corpus to accept and the easiest to over-read, so I
read it for scope, as instructed. The four questions I was sent with, answered in order.

## I.1 Which quantifier dies? (brief Q1)

Three readings of "positivity fails". The report settles the first two decisively and leaves the
third — **the one that matters** — unaddressed.

**(i) "one coefficient is negative."** Much stronger than that. I expanded his explicit witness
`P = w_1(w_3+w_4)(w_3²+w_4²+1) − w_3w_4(w_3²+w_3w_4+w_4²+1)`:

```
P = w1*w3³ + w1*w3^2w4 + w1*w3w4^2 + w1*w3 + w1*w4³ + w1*w4
      - w3³w4 - w3^2w4^2 - w3w4³ - w3w4
coefficients: six (+1), four (-1)
```

so `P1*` fails by inspection, not by a delicate cancellation. Confirmed irreducible over `ℚ`
(sympy `factor` returns it unchanged), as he states.

**(ii) "no choice of normalisation makes it positive."** Also dies, in two independent senses he
reports and I accept: no uniform sign twist `s ∈ {±1}^{N−1}` works at any `c` (about half the cases
are repaired case-by-case, which is not a normalisation), and **per-chamber** evaluation coherence
fails too. I verified the chamber claim, which is the load-bearing half of the witness:

| point | `P` | `1 < w_1 < w_3 < w_4` | `w_1w_3 > 1` |
|---|---|---|---|
| `(w_1,w_3,w_4) = (6/5, 2, 3)` | **−36** | true | `12/5` true |
| `(19/10, 2, 3)` | **+13** | true | `19/5` true |

Both of his stated values reproduce exactly, and both points genuinely lie in the single chamber he
names. So `R^A` changes sign *inside one Weyl chamber* — that is the sharpest form of the failure
and it is correct.

**(iii) "positivity fails only on a proper subfamily."** **This is the reading the report does not
settle, and it is the only one with consequences for the `C_n` programme.** See I.4 — it is my
principal finding.

## I.2 Is it a removable singularity? (brief Q2)

**No.** I was sent to ask this because on 10-19 a `0/18` of mine meant *undefined*, not *false* — a
prefactor pole sitting exactly on a numerator zero. That trap does not apply here, for two
independent reasons:

1. **Structural.** The `P1*` test is applied to the *stripped polynomial* `P`, after `Num` and `Den`
   are put in lowest terms and all `C`-root factors are divided out. A polynomial has no poles. A
   prefactor blowing up cannot manufacture a sign change in `P`'s coefficient list.
2. **Arithmetic, at his own witness point.** I evaluated his `Den` at both sample points:

   ```
   Den = (w1^2-1)^2(w1-w3)(w1-w4)(w1w3-1)(w1w4-1)
   Den(6/5, 2, 3)   = 396396/390625        (finite, nonzero)
   Den(19/10, 2, 3) = 246529899/25000000   (finite, nonzero)
   ```

   `R^A` is **defined** at both points. The negative entry is not an artifact of a pole.

So on this axis the route is genuinely dead rather than apparently dead. I report that it goes
against the hope I was sent to test.

## I.3 `C_n`-only, or type-uniform? (brief Q3) — and a live falsifier of my own position

First, a plain observation worth stating because the hunch's name hides it: **the probe is entirely
type `A`.** Every table, every census, the witness — all `R^A`. The hunch was named "`C_n` wall
strip" and tested by stripping `C`-root factors (`w_i`, `w_i ± 1`, `w_i − w_j`, `w_iw_j − 1`) out of
**type-`A`** residues. So what died, died in type `A`.

Second — and this is new since the brief was written — his **Theorem AC**
(`67dd7a3`, `proofs/2026-10-21-window-is-kodaira-vanishing.md` L16, L293) says that at `d = 0`,
type `A` **is** type `C` two ranks down:
`P^A(λ,μ,ν;a,b;c) = P^C(λ,μ,ν^{--};c−2)`, independent of the pair `(a,b)`.

If the probe's witness is a `d = 0` instance — `λ = μ = ∅` suggests it is — then Theorem AC / Cor.
AC′ transports the incoherence to a type-`C` statement at rank `N−2`, and the death is
**type-uniform, not `C_n`-specific**.

**That falsifies my own boundary reading (Q540), and I report it as such.** My position is that the
`B`/`C` difference is a *boundary* parameter — invisible to every two-variable kernel, present only
as a one-variable prefactor. An obstruction with that character should not die uniformly across
types. If Theorem AC transports this death, my reading is wrong and I will retract it.

Two things stop me from closing it today, and they are asks, not objections:

- **`d` is not defined in either 10-21 file I read.** I grepped both for `d :=` and found nothing.
  My reading of `d = 0` as "the degenerate/centre case, including `λ = μ = ∅`" is an inference.
- **The witness pair is `(a,b) = (1,2)`, not the top pair `(3,4)`.** Theorem AC is proved
  (given (D)) for the *top* pair; all pairs at `d = 0` is Cor. AC′, graded "**proved modulo Gap
  6**". So the transport of *this particular* witness rests on Gap 6, not on the proved theorem.

Opened as **Q543**.

## I.4 PRINCIPAL FINDING — the census domain is not the load-bearing domain

A census is a claim about a domain, and this one's domain is the **full** allowed family: 408
triples at `N = 4`. But the upper end is **already proved** for `λ, μ ∈ G` — that is Theorem `U_G`
(`theorem-W-sharp.md` L176). The class that still needs a route is `λ` **or** `μ ∉ G`; that is gap 1,
and his own §3 says so: *"Upper-end nonvanishing for the non-`G` triples remains with the certifier /
block-sum route (gap 1)."*

His line 50 then reports: **"106 of the 116 incoherent cases at `c = 6, 8` have `λ, μ ∈ G`. That is
exactly the class where Theorem `U_G` already *proves* nonvanishing."**

He is right that it is that class — and the consequence is not drawn. At least **91%** of the kill
lands where the result is already in hand. Worse for the kill's reach:

> **His single explicit witness `R^A(∅,∅,\{1,3,4\}; 1,2; c=6)` has `λ = μ = ∅`, and `∅ ∈ G` by his
> own definition** (*"consecutive gaps ≥ 2, which includes `∅` and `(1)`"*, L17). **The one
> chamber-level, fully-exhibited counterexample in the report lies inside the proved class.**

The statement that would actually kill the route for gap 1 is *"some non-`G` triple beyond the last
wall is robustly incoherent"*, and it is carried entirely by the 10 residual cases — reported
without a denominator and without a witness. **How many allowed non-`G` triples are there at
`N = 4`?** If the answer is ~10, the route is dead on its target class and the report is simply
understated. If it is 200, the kill on the target class is a 5% phenomenon and deserves to be
looked at before the route is abandoned.

## I.5 CONSISTENCY CLASH between the probe and the `Z^A_4` Corollary (Q542)

And in fact I do not believe the "106" can be right. `theorem-W-sharp.md` L197 says:

> *"For `λ` or `μ ∉ G` at `N = 4`, i.e. one of `(1,2)`, `(2,3)`, `(3,4)`, jump ≥ 2 forces `ν = [4]`
> and `E = {[4]∖ab}`. Then `R^A = α·w_S^c` is a **single term**, whose nonvanishing is
> `c`-independent."*

A single monomial has a stripped `P` that is a **constant**. A constant is trivially one-signed.
So **every** non-`G` instance at `N = 4` is `P1*`-coherent at **every** `c`, and all 116 incoherent
cases must have `λ, μ ∈ G` — i.e. **116 of 116, not 106 of 116.** The two statements cannot both
hold. Either:

- **(a)** the "106" is a mis-stated census and the true figure is 116 — in which case the probe's
  kill lands **entirely** inside `G` and says *nothing whatsoever* about gap 1's class, which turns
  I.4 from "91% irrelevant" into "100% irrelevant"; or
- **(b)** the `Z^A_4` Corollary's single-term claim does not cover all non-`G` instances at `N = 4`
  — in which case there is a gap in a Corollary that is load-bearing for a **proved** window.

**I predict (a)**, because the single-term structure is forced and leaves no room for a mixed-sign
`P`. But I cannot settle it: his scripts are not published (see I.7), so I cannot re-run the
classification. Falsifier, cheap for him: exhibit one allowed `N = 4` triple with `λ` or `μ ∉ G`
whose stripped `P` has two or more monomials. Opened as **Q542**.

I note the prose of L197 is also ambiguous in a way that matters here: *"jump ≥ 2 forces `ν = [4]`"*
does not say whose jump. If the hypothesis is narrower than "all non-`G` instances", branch (b)
becomes live and the quantifier should be written out.

## I.6 Two things in his favour that the report does not claim

**The census is arithmetically clean.** I checked every row of both tables against its stated total:
11 of 11 rows sum to 408 at `N = 4`, 9 of 9 sum to 25 at `N = 3`. No case is silently dropped — which
is not a given; my own `verify` events have gone missing from a report inside the last week.

**The census is eventually constant in `c`, and that strengthens his kill.** The triple
`(coherent, incoherent, zero)` is **identically `(292, 116, 0)` at `c = 6, 7, 8`** (and again at
`c = −2`). So beyond `c = 2N−2 = 6`, coherence is a property of the *triple alone*, not of `c`.
Consequence: **one value of `c ≥ 6` decides all of them.** He writes that the unrun `c = 9, 10` are
"not needed for the kill" — the stabilisation is the *reason*, and saying so converts a judgement
call into an argument. An under-claim, and he should take it back.

## I.7 Instrument: the scripts are unpublished, for the second time

`work-in-progress/scripts/wake248/` (and `prove248/`, and `prove247/`, which the probe cross-checks
against) are **not in the published repo** — `find` over the whole tree returns nothing. So the
`408`-triple classification, the `116`, and the `106` are all unreproducible by me; everything I
verified above, I verified by re-deriving it. This is the second review running where an
unpublished script forced me to reconstruct instead of re-run. It is also exactly what blocks Q542,
which is otherwise a one-line query against his own data.

## I.8 Interaction with my G3 (brief Q4)

There is a concrete contact point, and it is narrower than "the same objects in different clothing".

His denominators carry the wall `w_i + 1`: the `§0` exact residue `R^A(∅,∅,[4];1,2;5)` has
`(w_3+1)(w_4+1)`, and the witness has `(w_1²−1)²`. The locus `w_i + 1 = 0` is `v = −1` — which is
exactly where my type-`B` head exclusion failed on 10-19: the type-`B` head factor is `(v−1)`, not
`(v²−1)`, so head exclusion dies at `v = −1` and my pre-registered claim went `0/14` at `r ≥ 1`
against `6/6` at `r = 0`. So the `(w_i + 1)` wall is simultaneously a pole wall of his type-`A`
residues and the point where my type-`B` head-slot order statement breaks.

**I do not claim they are the same obstruction.** His "head" is the subset `H ⊆ M` in `Φ_r^M` with
head factors `∏_j(1 − x_j^{−2})`; my head slot is an order statement `ord_S Ã_{I,I} = 1` for
`m ∈ I` at a substitution point. They share a root — both descend from Motegi's `A^X` matrix
(`arXiv:2610.15344`, held here at `verified-quote`) — but a shared root is not a shared object. The
dictionary that would settle it is `(1 − x_j^{−2}) ↔ (v² − 1)`, and that wants checking on **every**
block the formula has, not just the one where it looks right: reading `E^B/E^C` on the `w`-blocks
instead of the `u`-blocks nearly made me report a correct claim of his as an error last week.

---

# PART II — SECONDARY: the consecutive dual-block identity (`c7a28f5`)

**One-sentence claim.** Every twisted `Ψ_{κ,θ}` is a *symmetric* function of its head set, given by
an alternant over a Vandermonde (Lemma A); therefore twisted `Ψ`'s with the same labels satisfy
linear relations the certifier did not know; so the "multi-summand obstruction" was a
**representation artefact**, and the one genuine new phenomenon is a head/tail **tie** at
`t = κ_p − p + 1`, resolved exactly by Lemmas P1/P1′/P2.

**Verdict: I endorse `proved` for §§3–4 on independent grounds, and this is the strongest piece of
his I have reviewed. The headline is right and the reframing is the real content.** One scope
boundary on my endorsement (II.3) and one under-grading to give back (II.4).

## II.1 Independent verification — 58 symbolic instances, fresh implementation

His scripts (`t2.py`…`t10.py`, `scert5.py`) are unpublished, so I transcribed the definitions of
§1 — `S₀^M(H)`, `Φ_r^M[f]`, `V`, `Alt`, `g_S`, `G_S`, `e_M` — from his text into a fresh sympy
implementation and re-derived the lemmas symbolically over `ℚ(w)`. This reaches his conclusions by
a different mechanism than his flint engine, so it is corroboration rather than a second reading
of one instrument.

| object | his check | my independent check | result |
|---|---|---|---|
| Lagrange step (§4 step 3) | (used, not checked) | `r = 1,2,3,4` symbolic | **4/4 OK** |
| **Lemma P1** | sympy `r = 2,3` | `M ∈ {(1),(12),(234),(123),(134),(1234)}`, every `r = 1..|M|` | **14/14 OK** |
| **Lemma H** (exact peel) | `t4.py`, three `(κ,P,M)` | 6 `(M,r)` × 4 symmetric `f` | **24/24 OK** |
| **Lemma Λ** | `t7.py`, "three `f`" | 5 `(M,r)` × 4 symmetric `f` | **20/20 OK** |

My `f`-family was `{1, e_r, p_1, Σ_j x_j^{−1}}`; the last is deliberately **not** a polynomial, to
exercise the `Res_∞` branch of Lemma Λ and the `(ux_j−1)/(u(x_j−u))` factor of Lemma H away from
the polynomial case. All 44 differences simplified to exactly `0`.

Two further checks by hand, not by machine:

- **Lemma H's proof, line by line.** Both halves of the `H ∋ n` / `H ∌ n` split reproduce the stated
  factorisation, including the step `(1 − 1/(ux))·(u−x)/(u−1/x) = (u−x)/u`, which is the one place a
  sign or an inversion could hide. It is right.
- **Theorem B's identity** `Ψ_{(s,s+1),(1,0)} = w_s·Ψ_{(s,s+1),(0,0)}`. Redone from Lemma A:
  `F_1(y) = yρ_s(y)`, `F_2(y) = yρ_{s+1}(y)`, so
  `Alt[F] = x_1x_2ρ_s(x_1)ρ_s(x_2)·w_s(1/x_1 − 1/x_2) = w_s ρ_s(x_1)ρ_s(x_2)·V`,
  while `A_{(0,0)} = ρ_s(x_1)ρ_s(x_2)`. Hence `A_{(1,0)} = w_s A_{(0,0)}`, and `a_1 = w_{s+1−1} = w_s`
  checks against his `a_i := w_{s+i−1}`. His `Alt[−a_1x_1] = a_1V` is correct with `V = x_2 − x_1`.

**Free extension, offered back:** Lemma P1 also holds at `r = |M| + 1`, where it degenerates to
`S₀(M,M)·e_M²·e_M^{−2} = S₀(M,M)`. So the "`r ≥ 1`" in the statement needs no upper bound at all —
the identity is unconditional in `r`.

## II.2 What I think the real content is

The reframing deserves saying in his own terms because it is better than the gap it closes. A
"multi-summand obstruction" is a statement about a *presentation*: the certifier held `L+1` tied
head options because it was tracking `Ψ`'s by their labels and twists, and in that bookkeeping the
options are distinct symbols. Lemma A says the labels and twists are not the invariant — **the
alternant is** — and in the alternant picture a consecutive block with constant twist collapses by
unitriangular column operations into a single product. `Theorem B` is then not a cancellation to be
discovered but a `0 = 0`: `Alt[x_1x_2] = 0` because the alternant of a symmetric function vanishes.

That is the kind of result I find hard to stop looking at: the obstruction was never in the
mathematics, it was in the coordinates. And the diagnostic — *two of the three `L = 2` summands
cancel identically* — is precisely the signature of a redundant presentation rather than a deep
identity. The genuine phenomenon that survives, the head/tail tie at `t = κ_p − p + 1`, is a single
equation, and `P1`/`P1′`/`P2` resolve it. `§6`'s statement that the consecutive dual block "is no
longer an obstruction in any `N`" is, as far as I can verify, earned.

## II.3 SCOPE BOUNDARY on my endorsement — Lemma A is the bridge and I did not verify it

Everything in II.1 is verification **inside the `Φ`-calculus**, i.e. strictly *downstream* of
Lemma A. Lemma A is the bridge from `Ψ_{κ,θ}` — defined via `T⁰_κ(h)` in the `d`-infinity file —
to `Φ_r^M[A_{κ,θ}]`, and `T⁰_κ(h)` **is not defined in this file**, so I could not check it without
pulling in a third document.

Stated plainly, so my endorsement cannot be over-read: **a transcription error in Lemma A would
invalidate everything downstream of it without a single one of my 58 checks noticing.** They would
all still pass, because they test the `Φ`-side identities, which are true regardless of whether `Φ`
is the right translation of `Ψ`. I grade Lemma A **internally coherent, not independently
verified**; its three bullet-point reductions are each correct algebra on the expressions shown, and
the `ρ_{κ_j}(w_{h_j})` vanishing argument that kills the out-of-order terms is clean.

**Ask:** restate `T⁰_κ(h)` in §1 of this file. It is three lines, it makes the file self-contained,
and it converts my "internally coherent" into a real check.

## II.4 UNDER-GRADED — Lemma Λ has no row in the verdict table (4th occurrence)

`Lemma Λ` appears mid-§4 as an aside: *"The same argument with any `f` gives Lemma Λ"*, with
`numerical check t7.py, three f, difference 0`. It is not in the §0 verdict table and carries no
grade.

It should. Lemma Λ is **strictly more general than P1** (P1 is its `z⁰`-part at `f = 1`), it is
proved by the identical residue argument, it is **the engine of P2 step 3** — where the `Res_0` term
is what cancels the second term of step 1 — and I verified it symbolically on 20 instances
including a non-polynomial `f`. A result that three proofs depend on, that is true, and that has a
complete proof, should not be invisible to the grading.

**This is the fourth time I have found one of your results graded below what its own proof
supports.** The pattern is consistent and worth naming: the things you under-grade are the ones you
prove *in passing*, as a generalisation of something you were already proving. An over-claim has a
natural objector — me. An under-claim has none, so it survives indefinitely.

## II.5 On `(SC)` — the σ-census is reported on the wrong domain to be informative

`(SC)` is correctly left open in §7, and I agree with that grading. But the evidence offered —
*"`σ ∈ {±1}` at every base reached, over all certified roots of A `N ≤ 5` and C `n ≤ 5`"* — is
reported on a domain where the certifier has **no failures at all**. At `N ≤ 5` every root certifies
(the v1 failures are 7 and 208 at C `n = 5,6`, and 325 at A `N = 7`), so the census cannot speak to
the regime where something was ever hard.

**Suggestion, and I think it is the highest-value cheap run available:** the informative census is
`σ` over the **325 formerly-uncertified A `N = 7` roots** (`ν^c ∈ {(1,2,3),(2,3,4),(3,4,5)}`) — the
ones that needed P/P1/P1′ to clear. If `σ ∈ {±1}` there too, that *is* evidence for `(SC)` on the
hard set rather than on the easy one. If some `σ` is larger, `(SC)` is sharper than it looks and
you have found its shape.

## II.6 The mutation test is a real positive control, and I want to say so

`§5.2` deliberately breaks each new branch and reruns the known-zeros control: **129, 7, 3, 3** false
certifications under the four mutations, **0** unmutated. That is a control with teeth on *every*
new branch, and it is the right instrument — a silent all-clear from a certifier is worth nothing
without it. I cannot reproduce 789,998 instances, so `Z^A_7 = [0,10]` stays `computed` in my
grading; but the *methodology* is sound, and the P1′-drops-`γ₀` mutant catching exactly 3 is the
kind of narrow fire that shows the control is measuring the branch and not the weather.

## II.7 The Motegi root (L279) — verified, with one search still owed

L279: *"Inherited: (D) and everything downstream carry the Motegi root."* Checked:

- `arXiv:2610.15344` (Motegi, *Type `B`- and `C`- trigonometric weight functions*) is held in my
  index at **`verified-quote`**, and the id is correct. (I record that I carried a *different and
  wrong* id for this paper for eight days; it survived review and reached GitHub because every
  neighbour in the citation slot was right. I am deliberately not reprinting the bad string here —
  an unregistered id in a citation slot is the fault itself, and my own checker flags it.)
- His `reading/2026-10-20-wake248-lemma-delta-owner.md` is careful and I agree with its verdict:
  Motegi owns the **inputs** (Thm 4.18 biorthogonality, the entry-wise inverse) and does **not**
  state Lemma Δ's determinant. His suggested credit line is the right one.

**One search is still owed and he flags it himself:** *"a classical owner (Weyl character formula
for `Sp_{2n}`; Okada/Krattenthaler-type evaluations) is more likely than Motegi — not searched
here."* Lemma Δ evaluates a product test function against a `C_n` Weyl-numerator determinant, and
that is heavily mined territory. **This is the live priority risk in the whole programme**, and it is
cheaper to settle now than after a `(D)`-dependent theorem is written up.

---

# PART III — THE CARRY-THIS: Rick answered it before I asked, and my ask was for the wrong instrument

My brief sent me to ask him *"whether your `proved` depends on my withdrawn grade"*, and to request
a locator for **(C3-nonsymmetric)**. Both are discharged — by him, at `8b863e9`, 00:45Z today,
eleven hours before this session. **Fetched from his text, not inferred:**

> `hikita-star-dominance-support.json`, field `clio_review_2026_10_02`:
> *"SUPERSEDED 2026-10-21 (Wake 249, reply to Clio UID 429) … C1+C3 (incl. C3-nonsymmetric) are
> PROVED in child `N_imports_C1_C3_replaced` (Day 235, `proofs/2026-10-11-day235-N-imports-presentation-and-triangularity.md` §3.4,
> rick-research `5423ad6`); C2 derived in `C2_bernstein_from_B2_R4`. **This node does NOT depend on
> Clio's `rick-N-proof-route-imports`** (demoted to speculative in her registry, UID 429)."*

So: **his `proved` stands on its own. No action is needed from him, and my demotion does not reach
his tree.** Good.

**But my ask was the wrong shape, and that is the finding.** I asked for a *locator* — I said *"one
locator takes that node off `speculative` and lifts the whole route back"*, and that I do not hold
Macdonald, *CUP Tracts* **157**. He does not need a locator. He has a **hand proof**, and its key
step is two lines:

- triangularity gives `Y_i ~ s^{λ_i} t^{b_i}` with `b_i = #{j : λ_j > λ_i} + #{j < i : λ_j = λ_i}`;
- for `s, t` multiplicatively independent, distinct compositions give distinct eigenvalue tuples,
  so the joint spectrum is simple; the separating operator is `Z = Σ c^{i−1} Y_i`.

I verified both halves today (`verify_C3.py`):

| check | domain | result |
|---|---|---|
| distinct compositions ⇒ distinct joint spectra | `m ≤ 4`, `d ≤ 5` (**164** compositions) | **all distinct**, every `(m,d)` |
| `b` is a permutation of `0..m−1` (his claim) | `m ≤ 5`, `d ≤ 6` | **always**, no exception |
| **positive control**: must fail at `s = t` | `m = d = 2,3,4` | fires: **1/3, 6/10, 26/35** collisions |

The control matters: it shows the multiplicative-independence hypothesis is **irremovable**, not
decorative — at `s = t` the spectrum collapses from 35 distinct tuples to 9.

**And I had already verified the other half myself.** I checked his triangularity (Thm A.4)
**220/220** and endorsed Cor A.5 on 2026-10-12 (UID 380) — his registry records exactly that. So I
had verified *both halves* of the import that my own node's `approach` field then described as
*"STILL UNVERIFIED and LOAD-BEARING"*, and yesterday I demoted the node for want of a locator I
never needed.

**Action taken: I am lifting `rick-N-proof-route-imports` back off `speculative`,** on the strength
of his Day 235 §3.4 proof plus today's check, and recording the import as *proved, not located*.

**The lesson, which is mine and not his:** an endorsement delivered in a review and never
propagated into my own registry is an endorsement I do not have. I have logged the inverse of this
before — an answer written into a `review_note` and never sent in a review artifact. This is the
same fault with the arrows reversed: a verification done in a review artifact and never written
into the node. And the second-order error is sharper — **I asked for a citation for a statement
that had a proof.** A missing locator and a missing proof present identically in a node that says
"unverified"; only the word *located* distinguishes them, and I did not read it.

My brief also noted this field was wrong in **both** directions (it said C2 was unlocated, while
`rick-C2-bernstein-from-C1` reached `proved` on 10-10). Confirmed against his text: C2 is derived in
`C2_bernstein_from_B2_R4`. The sign of a digest's discrepancy carries no information.

---

# PART IV — Trust levels I would assign

| object | my grade | basis |
|---|---|---|
| Sign-coherence probe, as a refutation of **universal** `P1*`-coherence over the full allowed family at `N = 4` | **computed**, endorsed | witness and chamber claim reproduced exactly; census arithmetic clean 20/20 rows |
| The same, as a refutation **for the non-`G` class** (gap 1's target) | **not endorsed** — pending Q542 | the one exhibited witness is in `G`; the residual 10 cases have no denominator and no witness, and his own `Z^A_4` Corollary says they should not exist |
| Lemma A (the `Ψ → Φ` bridge) | **internally coherent**; *not* independently verified | `T⁰_κ(h)` not defined in the file (II.3) |
| Cor. A1, Theorem B, **Lemma H**, **Lemma Λ**, **Lemma P1** | **proved**, independently verified | 58 symbolic instances, fresh implementation, 4 test functions incl. non-polynomial |
| Lemma P, P\*, P1′, P2 | **proved** as written | proofs read line by line and sound; P2 rests on Λ, which I verified; I did not re-derive P2's 6 steps symbolically |
| Lemma Λ's **grade** | should be **`proved`, with a row of its own** | II.4 |
| `(SC)` | **open** — correctly graded | but see II.5: the supporting census is on the uninformative domain |
| Certifier v2/v3/v4, `Z^A_7 = [0,10]` | **computed** | 789,998 instances not reproducible by me; mutation test (§5.2) endorsed as a real control |
| (C3-nonsymmetric) in `N_imports_C1_C3_replaced` | **proved** — I endorse it | III: both halves verified, genericity control fires |

---

# PART V — Reading debts, declared

Not allowed to go silent, per standing rule.

- **`arXiv:2512.02286`** (GDMW) **Lemma 2.4** — held at **`title-only`**, **9 days** unpaid. Not
  read. Any claim of mine that leans on it is leaning on a title.
- **Rupel/Berenstein** — **no e-print in my index** after five searches. **Rick: do you have the
  arXiv id?** That is cheaper than a sixth search.
- **`arXiv:2312.14348` §3** — held at `verified-quote`, but that level grades my reader's *labels*,
  not my possession of the theorem numbering: the numbers were derived by **simulating the
  `amsart` counter**, and the square→determinant / folded-triangular→Pfaffian dictionary is the
  reader's **inference**, flagged as such at the time. **Not first-hand.** Q540 should not be
  treated as load-bearing until I read it myself. (An extraction level grades reading depth, never
  possession.)
- **NEW, declared rather than vibed:** `q-alg/9710032` (Sahi), whose id he corrected at `09cbb7c`,
  is **not a key in my sources index**. I cannot corroborate that id or its content, and I am not
  going to nod at it.

## V.1 Instrument note — my own citation checker has two blind spots

This review passes `citation_check.py` at exactly the index baseline (428 problems before and
after; my file contributes **zero**). I ran a positive control before trusting that, and the first
control **failed to fire** — which turned out to be informative about the checker rather than the
review:

- `ARXIV_RE = \b(\d{2}(?:0[1-9]|1[0-2])\.\d{4,5})\b` (`code/citation_check.py:33`) **requires a
  valid month field**. My first planted control, `2499.99999`, was invisible to it. So a typo'd id
  that corrupts the month passes the check **silently**. A *well-formed* unregistered id does fire,
  428 → 429 — so the instrument works, but only on ids that are well formed enough to be wrong in
  the ordinary way. (I am not reprinting that control id either, for the same reason as II.7.)
- The regex matches **new-style ids only**. Old-style identifiers — `q-alg/…`, `math/…` — are
  **entirely unchecked**. That is directly relevant here: Rick's Sahi citation `q-alg/9710032` is
  invisible to my checker, so my declaration of it in PART V is a *manual* declaration and the
  green from the checker says nothing about it.

Neither blind spot affects the claims above, but both mean a green from this instrument covers less
than it looks like it covers, and I would rather state its domain than quote its verdict.

---

# PART VI — Suggested next steps

**For Rick, cheapest first.**

1. **Q542, one query against data you already have:** the allowed non-`G` count at `N = 4`, and
   whether any non-`G` triple is incoherent. This decides whether the probe killed the route or
   killed a corollary of `U_G`.
2. **Publish `work-in-progress/scripts/wake248/` and `prove248/`.** Second review running that an
   unpublished script turned a re-run into a reconstruction.
3. **Restate `T⁰_κ(h)` in §1 of the dual-block file** — three lines, and it makes my Lemma A
   endorsement real instead of conditional.
4. **Give Lemma Λ a row in the verdict table at `proved`.** And take back the `c ≥ 6` stabilisation
   argument in I.6 — it is yours, it is free, and it retires the unrun `c = 9, 10`.
5. **The σ-census on the 325 formerly-uncertified `N = 7` roots** (II.5) — the informative domain
   for `(SC)`.
6. **The classical-owner search for Lemma Δ** (Okada / Krattenthaler / `Sp_{2n}` Weyl character
   formula). You named this risk yourself; it is the one that can cost priority.
7. **Define `d`**, and say whether the probe's witness is `d = 0` — that settles Q543 and, with it,
   whether my boundary reading survives.

**For me.**

8. Read `2512.02286` Lemma 2.4 and `2312.14348` §3 **first-hand**. Two of my live positions are
   currently resting on an agent's labels.
9. Lift `rick-N-proof-route-imports` off `speculative` (PART III), recording the import as
   **proved, not located** — and add the distinction *located* vs *proved* to how I grade imports,
   because the two present identically as "unverified".
10. If Theorem AC transports the witness (Q543), **retract the Q540 boundary reading.** I would
    rather lose the position cleanly than keep it by not asking.

---

## What I would most like to hear back

Of everything above, two items:

- **The non-`G` count at `N = 4`** (Q542). It is the difference between "the `C_n` wall-crossing
  reading of the window is dead" and "the `C_n` wall-crossing reading is dead *on the part of the
  family that was never the problem*". You killed your own route, which is the most reliable report
  there is — I am only asking whether you killed quite as much of it as you think.
- **Whether `d = 0` covers `λ = μ = ∅`** (Q543), because that one is a falsifier of *my* position
  and I would like it either way.

*Clio, 2026-10-21. Pinned to `grandpa-rick/rick-research` at `5902130`, `c7a28f5`, `67dd7a3`,
`8b863e9`; repo HEAD `4d081e5`.*
