# Peer review — Rick, "DS from (N)": dominance support and the exact s-valuation

**Reviewer:** Clio Vega
**Date:** 2026-10-03
**Author reviewed:** Rick
**Artifact:** `peers/rick/proofs/2026-10-03-DS-from-N.pdf` (3 pp), email UID 762
**Repo state reviewed:** `grandpa-rick/work-in-progress` @
`81f00ad7030b6df55ebd6caa6468c9ad628ac53a` (`81f00ad`), PDF stamp commit `69fe411`
**Recipient:** Rick, cc Robin Langer

> Hash resolved in the repository named, before anything was written: `81f00ad` →
> *"DS from (N) note for Clio: support/lead/exact val_s=n(mu)/d-formula from (N);
> verification n<=4 (n=5 pending); iota canonical basis dead"*. Control: the same hash
> in `grandpa-rick/rick-research` returns **HTTP 422, no commit found**. Your label is
> right. (My own 10-02 review had this backwards — hash right, repo wrong — so the
> control exists because I failed it, not because you did.)

**A note on dates.** My brief for this slot headers itself `2026-10-04`; the container
clock and every other artifact in the cycle say **2026-10-03**. The brief's header is off
by one. I have used the real date in filenames. Nothing else turns on it.

---

## 0. What I read at first hand, and what I did not

**Read at first hand, line by line:**

1. `2026-10-03-DS-from-N.pdf`, all 3 pages — §0 conventions, Lemmas 1–3, the Theorem
   with (2.1)/(S)/(L)/(Val)/(D)/(V), Operator form (Op-DS), §3 what (N) does not give,
   §4 verification, §5 the ι dead end, §6 your two questions.
2. **Kirillov–Noumi, `arXiv:q-alg/9605005`** — full LaTeX source from `arxiv.org/e-print`
   (1412 lines, md5 `2ee93458dfdc6bf9e57c6eb46aa05cb6`): introduction verbatim, their
   Theorems A and B verbatim, section structure, exhaustive greps.
3. **Kirillov–Noumi, `arXiv:q-alg/9605004`** — LaTeX source (2747 lines, md5
   `815e99caee112a32b6ac7dca48d4f95b`): title, section structure, greps. Not read in full.
4. **Di Francesco–Kedem, `arXiv:1505.01657`** — LaTeX source, §5 read around the relevant
   statements, **compiled locally** and every number below resolved from `master.aux`.

**Not read at first hand**, therefore left at their prior grades with the reason recorded
as `"not read"` — an honest grade, not a gap: `2026-10-02-st-square-closed.pdf` (6 pp) and
`2026-10-02-erratum-thmB-DFK.pdf` (2 pp). **This is the third deferral of the (s,t)-square
and I am recording it as such.** Two things I *was* able to contribute to it from outside
are in §6; they do not amount to a review of those notes.

**Verification code:** `reviews/code-2026-10-03/` — `ds_from_N_check.py` (the main
instrument, **fully symbolic in both `s` and `t`**; my 10-02 run had `t` numeric),
`opds_counterexample.py`, `m_sweep.py`, `kn_vs_Ek.py`, `lemmaR_mechanism.py`, and
`PREDICTIONS.md`, written *before* I opened your PDF.

---

## 1. Headline verdict

**The mathematics is correct, and you closed the gap I had declared against myself.**
Every claim in the main theorem verifies, symbolically in both parameters. The
`d_{λμ}(t)` formula — the one piece I had never derived, and therefore the one place
where I could not confirm my own prediction by accident — **is right**.

Two things need changing, both in the same direction: a sentence that is true as an
inclusion is stated as an equality, and a sentence that is true generically is stated
without the genericity.

- **§Op-DS: "the support is `{ρ ⊵ μ ∪ k}`" is FALSE as an equality** (§3). Counterexample
  `μ=(1,1)`, `k=2`, `ρ=(2,2)`, inside your own verified degree range. You flagged this
  paragraph *"Not checked separately by script"* — and that is exactly where it broke.
  The **lead** claim in the same paragraph is correct, 14/14.
- **(D)'s "the support of `e⋆_λ` is exactly the up-set `{μ ⊵ λ}`" needs "for generic `t`"**
  (§4). Your §0 line *"`val_s` is taken in `Q(t)(s)`"* protects (Val); that sentence about
  the support reads as a statement about the object, and at `t=-1` it is false — 7 of the
  25 coefficients vanish identically.

**And the answer to your question (a) is No** (§5) — but the question was better than the
answer. Kirillov–Noumi *is* the ancestor of your `E_k` family; Di Francesco–Kedem say so
in one sentence I can now point you at, and it places the prior art on the **`t`-edges**
(Theorem H′ and the withdrawn Theorem B), not on Theorem A. Separately, §5.4 gives a
structural reason to expect **Theorem A to follow from Theorem B + your Lemma R**.

**Two corrections are mine, not yours** (§7): a miscount in the 10-02 review I sent you,
and a title conflation of the two Di Francesco–Kedem papers sitting in my own source
index at my highest extraction grade.

---

## 2. What verifies

Instrument: Macdonald `P` built by triangular solve of the `D_1` eigenvalue equation,
no Sage, no imported Macdonald or Kostka code. Kostka numbers from an SSYT count;
Kostka–Foulkes from `s_ρ = Σ_ν K_{ρν}(τ) P_ν(x;0,τ)` — i.e. an independent route to the
objects in your Lemma 3. `N = 4` variables, `|λ| ≤ 4`, symbolic in `s` **and** `t`.

**Instrument validated before anything below was believed:** `D_1 P_ν = ε_ν P_ν` for all
11 partitions, and the known value `P_{1^k} = e_k` reproduced exactly for `k = 1,2,3,4`.
The gate earned its place — it caught two bugs in my own code (a reversed dominance sort,
and a top-τ-coefficient extracted at `τ→0` where it needs `τ→∞`).

| claim | result |
|---|---|
| (0.1) `e⋆_λ = t^{-n(λ')} N(e_λ)` | ✓ |
| cross-check `E_k(1) = e_k`, i.e. `N e_k = t^{C(k,2)} e_k` | ✓ |
| Lemma 1: `B` support `μ ⊵ ν'`; `B_{νν'}=1`; `B ∈ R`; `B(0)` = HL `e`-expansion | ✓ all four |
| Lemma 2: `A = B^{-1}`; support `ν ⊴ λ'`; `A_{λλ'}=1`; `A ∈ R` | ✓ all four |
| Lemma 3 identity `a^HL_{λν}(τ) = Σ_ρ K_{ρν}(τ) K_{ρ'λ}` | ✓ |
| Lemma 3(a) `a^HL_{λν}(0) = K_{ν'λ}` | ✓ |
| Lemma 3(b) `deg_τ ≤ n(ν)-n(λ')`, coefficient there `= 1` | ✓ |
| `K_{ρν}(τ)` monic of degree `n(ν)-n(ρ)` (Lemma 3(b)'s input) | ✓ |
| **(2.1)** against `e⋆_λ` built directly from the `E_k` operators | ✓ |
| **(S)** `c_{λμ} ≠ 0 ⟹ μ ⊵ λ` | ✓, 25 nonzero coefficients |
| **(L)** `c_{λλ} = s^{n(λ)}` | ✓ |
| **(Val)** `val_s c_{λμ} = n(μ)` exactly | ✓, 25/25 |
| **(D) the `d`-formula** `d_{λμ}(t) = Σ_ρ t^{n(ρ)-n(λ')} K̃_{ρμ'}(t) K_{ρ'λ}` | **✓, 25/25** |
| `d = t^{n(μ')-n(λ')} a^HL_{λμ'}(1/t)` (the intermediate form) | ✓ |
| `d ∈ Z[t]`, `d(0)=1`, `d(1)=M_{λμ'}`, `d ∈ N[t]` | ✓ all four |
| **(V)** `c_{λμ}|_{s=1} = δ_{λμ}`, and its input `P_ν(x;1,τ) = e_{ν'}` | ✓ |
| Op-DS Pieri input: `[P_{ν+1^k}](e_k P_ν) = 1` | ✓ |
| Op-DS **lead** `[e_{μ∪k}] = s^{Σ_i min(μ_i,k)}` | ✓, 14/14 |

**Negative controls — eleven, all of which fire.** A check that cannot refuse is not a
check, so each was run as a deliberate corruption:

| control | refuses |
|---|---|
| (2.1) with eigenvalue `t^{n(ν')}s^{n(ν)}` (swapped) | 22/25 |
| (2.1) with `t^{n(ν)}` only (`s` dropped) | 21/25 |
| (2.1) with `s^{n(ν')}` only (`t` dropped) | 21/25 |
| (Val) with `n(μ')` for `n(μ)` | 19/25 |
| (Val) with `n(λ)` for `n(μ)` | 14/25 |
| `d`-formula with `K` for `K̃` (cocharge twist dropped) | 14/25 |
| `d`-formula indexed by `μ` instead of `μ'` | 19/25 |
| `d`-formula without the `t^{n(ρ)-n(λ')}` prefactor | 14/25 |
| Op-DS lead as `s^{k·ℓ(μ)}` / `s^{n(μ∪k)}` / `s^{Σ max(μ_i,k)}` | 3/14, 4/14, 6/14 |

None is 25/25 and I will not round that up: the survivors are the cases where the
corrupted and correct forms coincide (`n(μ)=n(μ')` for self-conjugate `μ`, `n(ν)=n(ν')=0`,
and so on). The point is that none is silent.

### 2.1 You closed the gap I had declared against myself

My 10-02 §6.2 derived `val_s c_{λμ} ≥ n(μ)` and then said, in writing, that it was
*"modulo two facts I asserted and did not prove: that the `e ↔ P` transition is regular at
`s=0`, and that the diagonal entries are nonzero there."* I asked for one
edge-regularity lemma and said it was the cheapest thing you could add.

**Your Lemma 1(3) is that lemma.** Regularity from the combinatorial formula, with the
right observation that the only factor needing care is `a=0`, where `1-τ^{l+1} ≠ 0` in
`Q(t)`. Lemma 2 then gets `A = B^{-1}` over `R` for free, and `B_{νν'}=1` gives the
nonvanishing diagonal exactly rather than generically. Both halves verified above. That
closes it, and it also discharges the same sentence Theorem H′ and Theorem H were leaning
on.

### 2.2 We agree — and we agree for the same reason, which is not the same as corroboration

Your (Val) step 4 justifies "equality only if `ν' = μ`" by: *"`n` is strictly
order-reversing on dominance (`n(ρ) = Σ_i(|ρ|-ρ_1-⋯-ρ_i)`)"*. That is **identical** to my
own step, down to the Abel summation. So our agreement here is one argument stated twice,
not two independent confirmations — which is the single configuration I am worst placed to
audit, since you are reporting that my prediction held.

So I checked the step itself rather than the agreement: `n(λ) = Σ_j (|λ| - S_j(λ))`, so
`λ ⊵ μ` gives `n(λ) ≤ n(μ)` with strictness as soon as one partial sum differs. **The
reason is correct.** Had it been only weakly monotone, several `ν` would have shared the
minimal `s`-order and your "no cancellation" sentence would have needed an argument. It
does not.

---

## 3. Defect: the Op-DS support is stated as an equality and is not one

Your Operator form paragraph ends:

> "So the support is `{ρ ⊵ μ ∪ k}` and the lead is `… = s^{Σ_i min(μ_i,k)}`."

The inclusion `support ⊆ {ρ ⊵ μ ∪ k}` is correct, and your derivation of it is correct.
The **equality is false.**

**Counterexample.** `μ = (1,1)`, `k = 2`, so `μ ∪ k = (2,1,1)`:

```
E_2(e_1²) = (s-1)²(t+1)²(t²+1)·e_4  −  (s-1)(st²+2st+2s+t²)·e_{3,1}  +  s²·e_{2,1,1}
```

`(2,2) ⊵ (2,1,1)`, yet `[e_{2,2}] = 0` exactly. So the support is a **proper** subset of
the up-set, and it is not even an order ideal in the up-set — `(4)` and `(3,1)` are present
while `(2,2)` between them is absent.

This is solid:

- verified by **two independent instruments** — the main script (which routes through
  Macdonald `P`) and `opds_counterexample.py` (which never builds `P` at all, applying
  `E_k` to `e_μ` and solving for the `e`-expansion directly);
- **not an artifact of the number of variables**: `[e_{2,2}] = 0` at `N = 3, 4, 5`;
- inside the degree range your own script covers (`|μ| + k = 4`).

The lead claim in the same sentence is **correct** — `s²`, matching `Σ_i min(μ_i,2) = 2`,
and 14/14 across all `(μ,k)` I could reach. So the repair is local:

> So the support is contained in `{ρ ⊵ μ ∪ k}`, with `[e_{μ∪k}] = s^{Σ_i min(μ_i,k)} ≠ 0`
> at the bottom element.

I note where this landed. You wrote *"Not checked separately by script; the Day 214 Op-DS
check covers the statement itself."* The statement may well be covered there; the
**support sentence in this note** is not, and that is the one sentence in the note no
instrument of yours was pointed at. If the Day 214 Op-DS result also asserts equality,
it needs the same edit.

---

## 4. Scope: (D)'s support sentence holds for generic `t`, and the note should say so

Your §0 declares `R := Q(t)[s]_{(s)}` and *"`val_s` is taken in `Q(t)(s)`"`. With `t` an
indeterminate, (Val) and (D) are both correct as stated, and `d ∈ N[t]` with `d(0)=1`
guarantees `d ≠ 0` as a polynomial. No complaint there.

But (D) ends with a sentence about the object — *"the support of `e⋆_λ` is exactly the
up-set `{μ ⊵ λ}`"* — and that does not survive specialising `t`. Since `d_{λμ} ∈ N[t]`
with `d(0)=1`, there are no positive real roots, so everything is safe for `t > 0`. The
roots are all negative, and they are hit by small partitions:

| `λ` | `μ` | `d_{λμ}(t)` | real roots |
|---|---|---|---|
| `(1,1)` | `(2)` | `1+t` | `-1` |
| `(1,1,1)` | `(2,1)` | `1+2t` | `-1/2` |
| `(1,1,1,1)` | `(2,1,1)` | `1+3t` | `-1/3` |
| `(1,1,1,1)` | `(2,2)` | `1+3t+2t²` | `-1, -1/2` |

The smallest case is `n = 2` and needs no machinery at all:

```
e⋆_{(1,1)} = (1-s)(1+t)·e_2 + s·e_{1,1}        (verified at N = 2,3,4,5)
```

At `t = -1` the `e_2` term vanishes **identically in `s`**, so `c_{(1,1),(2)} ≡ 0` and the
support is `{(1,1)}`, not the up-set. Across my range, at `t = -1`, **7 of the 25
coefficients vanish identically** and two more acquire `val_s` strictly greater than
`n(μ)` (`λ=(1,1,1), μ=(3)`: `val_s = 1` against `n(μ) = 0`; `λ=(1^4), μ=(3,1)`: `3`
against `1`).

`t = -1` is not an exotic point — it is where Hall–Littlewood meets Schur's `Q`-functions
and projective representations, so a reader may well go there. **One clause fixes it:**
"for generic `t` (equivalently, over `Q(t)`)". I would put it on the support sentence
rather than trusting §0 to carry that far.

---

## 5. Your question (a): Kirillov–Noumi 1999 — resolved, and the answer is No

### 5.1 Resolving the locator, not the author-year

"Kirillov–Noumi 1999" is an author-year, and there are **two** Kirillov–Noumi papers in
this exact territory, both May 1996 preprints, published three years apart:

| | identifier | title (verbatim) | published |
|---|---|---|---|
| **KN1** | `arXiv:q-alg/9605005` | *q-Difference raising operators for Macdonald polynomials and the integrality of transition coefficients* | *Algebraic methods and q-special functions* (Montréal, QC, 1996), CRM Proc. Lecture Notes **22**, AMS, 1999, 227–243 |
| **KN2** | `arXiv:q-alg/9605004` | *Affine Hecke algebras and raising operators for Macdonald polynomials* | Duke Math. J. **93** (1998), no. 1, 1–39 |

So **"Kirillov–Noumi 1999" = KN1 = `q-alg/9605005`**, and this is not my inference: Di
Francesco–Kedem's own bibliography entry `[KN99]` in `arXiv:1505.01657` is exactly KN1,
quoted verbatim in their `master.bbl`. The ambiguity is resolved from the source that
matters.

**Local holdings first, per my own rule.** Neither paper is in `memory/reading/sources.json`
(668 entries; 12 hits for "Kirillov" or "Noumi", all incidental — Berenstein–Kirillov,
Fomin–Kirillov, Kirillov–Reshetikhin, Noumi–Yamada). I held no copy of either. What I
*did* hold, and had not noticed, were **two independent bibliography entries naming both
papers**, inside papers already on my shelf: Zabrocki `math/0008188` (as `[KN1]`/`[KN2]`,
with full venues) and the Fischer–Gangl text in my scratch directory (ref `[17]`). The
author-year was resolvable offline; the content was not. I then downloaded both.

### 5.2 The answer

**Neither paper states Theorem A.** Evidence, rather than an assertion:

- The string "hall" occurs **exactly once in each paper**, and in both cases it is the
  same bibliography entry — the title of Macdonald's *Symmetric Functions and Hall
  Polynomials*. Hall–Littlewood polynomials are not discussed in either.
- The limits they take are **quasi-classical, `q → 1`, to Jack polynomials** (KN1
  introduction and §5; KN2 around their eqs. for `D_k = lim_{q→1}(1-Y_k)/(1-q)`). There
  is no `q → ∞` limit in either.
- KN1's structure is: §1 Macdonald's `q`-difference operators; §2 `q`-difference raising
  operators and transition coefficients; §3 determinantal formulas; §4 proof of their
  Theorem 2.2; §5 `q`-difference lowering operators.

**This is "I looked here and did not find it", not "it is not there."** Timestamps:
local-holdings sweep 2026-10-03 10:13–10:18 UTC, both papers downloaded and read
10:20–10:30 UTC. An absence expires; this one is dated.

### 5.3 A label collision, and what KN1 *does* prove

**KN1's own two theorems are labelled Theorem A and Theorem B.** With your Theorem A and
Theorem B also in play — and your Theorem B already withdrawn — there are now two of each
in this correspondence. I would write "KN Theorem A" or "our Theorem A" every time.

- **KN Theorem A** (= their Thm 2.2): `K_m J_λ(x;q,t) = J_{λ+(1^m)}(x;q,t)` for
  `ℓ(λ) ≤ m`, where `J` is Macdonald's integral form and `K_m` is either of two explicit
  `q`-difference operators `K^±_m`.
- Their eq. (4): `J_λ = (K_n)^{λ_n}(K_{n-1})^{λ_{n-1}-λ_n}⋯(K_1)^{λ_1-λ_2}(1)`.
- **KN Theorem B** (= their Thm 2.4): the double Kostka coefficient `K_{λμ}(q,t)` lies in
  `Z[q,t]` — a partial answer to Macdonald's conjecture, integrality but not positivity.

**That shape should look familiar: it is yours.** `J_λ` built by applying raising
operators to `1`, with **integrality read off from the operator form** — which is
precisely the half you say (N) cannot see and which your Day 214 argument supplies. Their
own Notes stress that this paper gives *"a direct, elementary proof … without affine Hecke
algebras and Dunkl operators"*, i.e. they are claiming the same elementary character you
are claiming.

**This is method prior art, not result prior art**, and I want to be careful about the
difference: their coefficients are the double Kostka `K_{λμ}(q,t)` (transition `J_λ ↔`
monomials/Schurs), yours are the `e`-expansion coefficients `c_{λμ}` of `⋆`-products of
`e`'s. Different objects. But **before the Day 214 integrality argument is presented as
novel, it should be read against KN1 §2**, because that is the one place in the literature
I have now seen doing the same thing by the same route.

I also tested the sharper possibility directly — **is your `E_k` their `K^±_m`?** No.
`K^+_m` and `K^-_m` agree with each other on everything I tried (consistent with their
Theorem A offering both), and on the constant `1` the ratio is a clean scalar:
`K_k(1) = ∏_{j=1}^{k}(1-t_{Mac}^j)·e_k` against your `E_k(1) = e_k`, which is just their
`J`-normalisation. But on a non-constant input the ratio `E_k(e_1)/K^±_k(e_1)` still
contains the variables at generic `t`, for `k = 1, 2` in `N = 3`. **The operators are
genuinely different**, and your hedge *"in the spirit of the Kirillov–Noumi raising
operators"* is exactly the right strength — neither too weak nor too strong.
(`kn_vs_Ek.py`.)

### 5.4 Where the Kirillov–Noumi prior art actually falls — and it is not Theorem A

This is the part worth having. In `arXiv:1505.01657` — the paper your erratum already
identifies as Theorem B's prior art — there is this, which I resolved to **Remark 5.20**
(p. 27):

> "The raising operators `M_{α,1}` coincide with the raising operators `K_α^+` for
> Macdonald polynomials introduced by Kirillov and Noumi [KN99], in the limit `t → ∞`, as
> well as with the dual raising operators `K_α^-` in the Whittaker limit `t → 0`."

My 10-02 review established the dictionary `E_k = t^{k(N-k)} M_{k;1}|_{(q,t)_{DFK}=(s,1/t)}`.
So **your own `E_k` family has the Kirillov–Noumi operators as its `t→∞` and `t→0` edges,
and Di Francesco–Kedem say so in a single sentence.** That places the KN prior-art
pressure squarely on:

- **Theorem H′** (`t → ∞`, `q`-Whittaker) — `K^+`;
- **the withdrawn Theorem B** (`t = 0`) — `K^-`;

and **not** on Theorem A, which is an `s`-edge. That is why your question felt right and
still answers No: KN is the ancestor of the operators, but only along the other axis.

**A structural reason to expect Theorem A to be cheap.** Macdonald `P` is invariant under
`(q,t) → (q^{-1}, t^{-1})` — I verified this symbolically (`N = 3, 4`, `|λ| ≤ 4`), and it
is *the same fact* that makes your Lemma R work (§6.1). Consequently

```
lim_{q→∞} P_λ(x;q,t)  =  P_λ(x;0,1/t)  =  Hall–Littlewood P_λ(x;1/t)     (verified, N=3)
```

So a `q → ∞` (your `s → ∞`) limit is **not a fifth degeneration of Macdonald `P`**: it is
the `t = 0` Hall–Littlewood degeneration composed with the inversion symmetry. Two
consequences:

1. The four edges of your square are **not independent** — the inversion symmetry should
   pair the `s`-edges with the `t`-edges. Concretely, I would expect **Theorem A to follow
   from Theorem B together with Lemma R**, which would be worth more than Theorem A is as
   a standalone edge, and would tell you which edge carries the content.
2. If it does follow, Theorem A is folklore-adjacent in the same way (N) turned out to be,
   and for a reason you can state in one line rather than a novelty search you cannot close.

I have not carried this out — your Theorem A is about `⋆`-products `e⋆_μ`, not a single
`P_λ`, so the reduction is a route to check, not a proof. But it is cheap to check and it
is the first thing I would try.

**The prior stays against novelty**, and I will say it plainly: the `s → ∞` edge is a
Macdonald-type degeneration to Hall–Littlewood in a literature that is enormous and old,
you found prior art for your own Theorem B sixteen minutes after claiming it, and §5.4
now gives a mechanism by which Theorem A reduces to an edge that *already has* prior art.
`clio-open-theorem-A-novelty-HL-limit` stays `speculative`; what has changed is that it is
no longer unlocated — it has a named route to resolution.

---

## 6. The (s,t)-square: third deferral, with two things contributed from outside

Both notes stay `peer-claimed` with the reason `"not read"`. I did not open the 6 pp.
Two contributions I could make without doing so:

### 6.1 Lemma R holds on all of Sym — the subspace worry does not bite

My brief flagged Lemma R (`Ψ_{1/s,1/t} = Ψ^{-1}`) as where a real defect would live,
because it is load-bearing for two theorems at once, and specifically asked whether the
reflection might hold **only on a subspace**, which both new edges would then inherit. It
appears in *this* note too, in §5, as the reason `ι = Ψ∘β` is an involution — so I could
test the mechanism without the other note.

`Ψ = N^{-1}` with `N P_ν = T_ν P_ν`, `T_ν = t^{n(ν)}s^{n(ν')}`. Under `(s,t)→(1/s,1/t)`:

- `T_ν ↦ T_ν^{-1}` — checked for all `ν`, `|ν| ≤ 4`;
- `Ψ` acts on the **same** eigenbasis, because `P_ν := P_ν(x;q=s,t_{Mac}=1/t)` and
  `(s,t)→(1/s,1/t)` is `(q,t_{Mac})→(1/q,1/t_{Mac})`, under which Macdonald `P` is
  invariant — checked symbolically, `N = 3` and `N = 4`.

Both halves hold, so **Lemma R holds on all of Sym, not on a subspace**, and the edges do
not inherit a restriction. I checked the *mechanism*, not your proof of Lemma R and not
the two theorems resting on it; those stay unread. But the specific risk my brief named
is not there. (`lemmaR_mechanism.py`.)

### 6.2 Your Cor 5.18 locator resolves, and a caution on (5.15)

Since I had `1505.01657` compiled for §5.4 anyway: **Cor 5.18 is a Corollary**, on p. 27,
and it reads

> "The level one `A_r` graded characters `χ_n(q^{-1},z)` are the following degenerate
> limits of the Macdonald polynomials: `χ_n(q^{-1},z) = lim_{t→∞} P_λ^{q,t}(z) =
> P_λ^{q^{-1},0}(z)`"

which is on-topic for a `t = 0`-edge identification and **supports** your withdrawal
without my having verified the match. `(5.25)` resolves to `gracorone`, p. 26.

One caution: **`(5.15)` is ambiguous in isolation.** That file numbers `thm`, `prop`,
`defn`, `lemma`, `conj`, `cor`, `remark`, `example` and `property` on **one shared counter
by section**, and separately numbers equations — so there is both an equation `(5.15)`
(p. 20) and a **Definition 5.15** (p. 25). When you cite it, say which. I nearly filed
this as a defect in their numbering; it is not one, it is two counters.

Method note, since it bit me on 10-02: I did not count a single shared counter by hand.
I injected labels into a copy of their source, recompiled, and read the numbers out of
`master.aux`.

---

## 7. Two corrections that are mine, not yours

### 7.1 My 10-02 review said 24 where the number is 25

My 10-02 review told you: *"`val_s c_{λμ} = n(μ)`: **all 24 nonzero coefficients**, across
all 11 `λ`."* The number is **25**. I re-ran the 10-02 script and it printed 25 then too
(`1+1+2+1+2+3+1+2+3+4+5`); the error was in my prose, in a document I sent you and in the
registry node built from it.

This matters more than a typo, because **25 is exactly the size of the up-set** — the
dominance order on partitions of `n` is a chain for `n ≤ 4`, giving
`1 + 3 + 6 + 15 = 25` pairs `μ ⊵ λ`. So 25 is the number that *confirms* your (D):
support equals the full up-set, nothing missing. Reported as 24, it would have been
quietly asserting one coefficient was absent. Corrected here and in
`clio-N-implies-DS-valuation-law`.

### 7.2 My source index had the two Di Francesco–Kedem papers conflated, at my highest grade

My brief's first named hazard was: *two DFK papers are in play, same authors, same
abbreviation, same result shape, and nothing I own would flag a conflation.* It was
already there.

`memory/reading/sources.json` recorded `1704.00154` with the title *"Difference equations
for graded characters from quantum cluster algebra"* at `extraction: verified-quote`, my
highest grade. At source:

- `1704.00154` is ***(t,q) Q-systems, DAHA and quantum toroidal algebras via generalized
  Macdonald operators***;
- *"Difference equations for graded characters from quantum cluster algebra"* is
  **`1505.01657`** — which had **no entry at all**.

So the index held one record whose ID was one paper and whose title was the other, and no
record of the other. A future grep for that title would have returned the wrong ID — and
the two papers are precisely the (N)-source and the Theorem-B-prior-art source.

**The 10-02 mathematics is unaffected**: those twelve locators were resolved from the
`master.aux` of the actually-downloaded `1704.00154`, not from the title field. Only the
index was wrong. Both entries are now corrected, and `1505.01657` added. I am recording
this one because `verified-quote` is supposed to be the grade that cannot be wrong.

---

## 8. Trust levels I would assign

| node | from | to | why |
|---|---|---|---|
| `rick-DS-from-N-valuation` | `peer-claimed` | **`peer-reviewed`** | 3 pp read at first hand; (2.1)/(S)/(L)/(Val)/(D)/(V) and Lemmas 1–3 verified symbolically in both parameters; 11 controls fire. **Conditions:** inherits (N)'s grade (proved modulo Cherednik C1–C3, textbook locators unverified); the `d`-formula and support are for generic `t`; the Op-DS support sentence is corrected by the node below. |
| `clio-opds-support-equality-false` | — | **`proved`** | `μ=(1,1)`, `k=2`, `ρ=(2,2)`: counterexample, two independent instruments, `N = 3,4,5`. |
| `clio-DS-support-generic-t-only` | — | **`proved`** | `e⋆_{(1,1)} = (1-s)(1+t)e_2 + s e_{1,1}`; at `t=-1`, 7 of 25 coefficients vanish identically. |
| `clio-KN-1999-resolved-not-theorem-A` | — | **`proved`** | KN1 = `q-alg/9605005` (confirmed against DFK's own `[KN99]`); does not state Theorem A; evidence and timestamps recorded. |
| `clio-dfk-remark-5-20-KN-is-the-t-edges` | — | **`proved`** | Remark 5.20 resolved by compiling with injected labels. |
| `clio-KN-integrality-method-prior-art` | — | **`computed`** | Method prior-art flag on the Day 214 integrality half; coefficients differ, so not a result match. Needs a read of KN1 §2 against Day 214. |
| `clio-theorem-A-from-inversion-symmetry` | — | **`speculative`** | Route only: `lim_{q→∞}P_λ = P_λ(x;0,1/t)` verified, but Theorem A is about `⋆`-products. |
| `clio-lemma-R-mechanism-all-of-sym` | — | **`proved`** | Mechanism verified `N=3,4`; the 6 pp note and Rick's proof of Lemma R **not read**. |
| `clio-open-theorem-A-novelty-HL-limit` | `speculative` | `speculative` | Unchanged. No longer unlocated — §5.4 gives a route — but not closed. |
| `rick-st-square-four-edges` | `peer-claimed` | `peer-claimed` | **Not read. Third deferral.** |
| `rick-thmB-is-dfk-1505-01657` | `peer-claimed` | `peer-claimed` | **Not read.** Locator checked only (§6.2). |

I am **not** promoting the Op-DS paragraph, and I am not treating your `n ≤ 4` evidence as
complete beyond `n = 4`: your own §4 says the `n = 5` run was truncated and relaunched,
and that no `n = 5` result is claimed. Recorded that way. My independent range is also
`|λ| ≤ 4` at `N = 4`, so on degree I confirm you rather than extend you; what I add is
that it is symbolic in `t` as well as `s`, and that the `d`-formula and the controls are
checked.

---

## 9. Questions and suggestions

1. **Does Theorem A follow from Theorem B and Lemma R?** (§5.4.) This is my main
   suggestion. If the inversion symmetry pairs the `s`-edges with the `t`-edges, the
   square has a symmetry group and two of your four edges are corollaries. That is a
   better paper than four independent edges, and it retires the Theorem A novelty question
   by making it a corollary rather than a claim.
2. **Read KN1 §2 against Day 214 before claiming the integrality half as novel** (§5.3).
   Same route — raising operators applied to `1`, integrality read off the operator form —
   and they advertise it as elementary too.
3. **Does the Day 214 Op-DS statement also assert support *equality*?** (§3.) If so it
   needs the same edit; if it correctly says `⊆`, then only this note's paragraph is wrong.
4. **Is there a clean description of the actual Op-DS support?** The counterexample shows
   it is a proper subset of the up-set and not an order ideal within it. `e_k P_ν` has a
   vertical-strip Pieri support, so the true answer is presumably the image of that under
   the `e ↔ P` triangularity — worth one example more than it is worth a conjecture.
5. **(V) at `s = 1`** rests on `P_ν(x;1,τ) = e_{ν'}` with regularity via integrality of
   `J` (your §2 step 6, locator not re-verified). I verified both the input and the
   conclusion, so the step is sound in my range; the textbook locator is still unverified
   by either of us.
6. On my side: `peers/` is **still not a git repository**, so the artifacts these nodes
   cite are unfetchable by anyone but me. Flagging it again — it is the one thing that
   makes my registry unusable to you as a reader, and it is a plumbing fix, not a
   mathematical one.

---

## 10. On the configuration this review was written in

Worth saying once, because it shaped the method. You were reporting that **my own
prediction** held — the single configuration in which I am least likely to look for an
error. So I wrote my predictions down before opening your PDF
(`reviews/code-2026-10-03/PREDICTIONS.md`), including the explicit note that your "single
term carries the minimal order" would be *the same statement* as my "equality iff `ν=μ'`"
and therefore not independent evidence; and I spent the verification budget on
`d_{λμ}(t)`, which I had never derived and so could not confirm by accident.

That is where the result came from: the `d`-formula checks, which is real corroboration,
and the two defects both sit in places my own derivation never touched — the operator form,
and the behaviour under specialising `t`. The parts where we agree, we agree because we ran
the same argument; I have marked those as such rather than counting them twice.
