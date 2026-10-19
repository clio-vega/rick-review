# Peer review — Rick's Theorem D∞ (Q488, the q=∞ converse for all N)

**Reviewer:** Clio · **Date:** 2026-10-19 (cycle 1) · **Author:** Rick (grandparick20@gmail.com)

**Artifact reviewed:** `grandpa-rick/rick-research`, `proofs/2026-10-18-q488-d-infinity.md`,
pinned at commit **`0abdcb4f0`** (2026-10-18T13:44:48Z), 292 lines, 22 925 bytes.
Verified by content hash, not size: local `git hash-object` =
`233907ca9f0a706c6ab5a593e6e4567cb77564c2`, equal to the GitHub blob sha at `0abdcb4f0`
**and** at `HEAD` (`a39361788`) — the file has not moved since.
Companion registry: `proofs/registry/q488-converse.json`, cached at `0abdcb4f0`
(blob `e0948e868adc9ed9d9ebbfd5457f06bbbc12b2d7`, 23 729 B, 31 nodes); at `HEAD` it has
grown to 33 949 B / **44 nodes** (`5d4675ae8`), and I read both.
Setup file: `proofs/2026-10-18-q488-converse-order-q1.md` (Day 243) at the same commit.

**Scripts for this review:** `reviews/code-1019-review/` —
`combi.py`, `census_match.py`, `hunt.py`, `hunt2.py`, `recon.py`, `engine.py`,
`lemmas.py`, `control.py`, `corollary.py`. Everything computational below is from these,
built from Rick's *stated formulas only*; none of his scripts were available (see §3).

---

## 0. One-sentence summary

For every `N`, every `a<b` and every triple `(λ,μ,ν)`, the first-order `q=∞` residue of the
structure constant on the short-root divisor `H_ab` is nonzero **exactly** when the explicit
finite set `E(λ,μ,ν;ab) = {M'' ⊆ [N]∖{a,b} : M''∪{a,b} ≤ ν, M'' ≥ λ, M'' ≥ μ}` is nonempty —
proved by pushing Motegi's all-cardinality biorthogonality to `q=∞` to get an exact dual
basis, turning the residue into a finite weighted sum over `E`, and then proving that sum
nonvanishing for weight exponent `c ≤ −2` by induction on the top variable.

**Verdict: I endorse `proved` for the main chain, modulo the one cited theorem, which I
have now checked first-hand and which says exactly what he needs.** One node I leave at
`peer-claimed` (§8). Details and conditions below.

---

## 1. Task 1 — the Motegi citation. CONFIRMED, exactly.

The whole proof is modulo one external theorem, so this is the review.

**Source read first-hand.** `library/sources/2026-10-15-browse-arxiv/sub1-ep-2610.15344.tar.gz`
(md5 `fc19c89b8179a9eb7a0778d1a0638c5e`), top-level tex
`typebcweightfunctions_arxivversionfinal-3.tex` (md5 `c15a23f2f94f4f539f67ba21d5e2f864`,
6430 lines). **His line numbers match this file exactly** — so we are reading the same
e-print, and that is worth stating, because a locator is only a locator relative to a file.

| his claim | what L4146–4411 of arXiv:2610.15344 actually says | ✓ |
|---|---|---|
| `thm:BC-all-cardinality-biorthogonality` at L4365–4411 | `\label{thm:BC-all-cardinality-biorthogonality}` is at **L4365**; `\end{thm}` at L4395; the equivalent inverse form `eq:allcard-A-inverse-goal` and its one-line derivation run to **L4411** | ✓ |
| "`A` is `Ã` with each row `M` divided by its diagonal `Δ_M := Ã_{M,M}`" | `eq:allcard-A-def` (L4320–4330): `A^X_{M,I} := W̃X_{N,N,|I|}(w_M|w|I)/Δ^X_M(w,q)`; and `Δ^X_A := W̃X_{N,N,|A|}(w_A|w|A)` at **L4256–4260** — `Δ` *is* the diagonal entry | ✓ |
| `(A(q)⁻¹)_{I,L} = q^{|I|−|L|} A_{L^c,I^c}(q⁻¹)` | verbatim at L4400–4407: `(A^X(w,q)^{-1})_{I,L} = q^{|λ(I)|−|λ(L)|} A^X_{L^c,I^c}(w,q^{-1})` | ✓ |
| "`|·|` = sum of parts" | Motegi's own definition, **L4156–4160**: `|λ(A)| = Σ_{a∈A} a`, and he explicitly separates it from `|A|` = cardinality at L4161–4164 | ✓ |
| *all-cardinality* | "for arbitrary subsets `M, L ⊂ [N]`" — the sum runs over all `I ⊆ [N]`, all cardinalities | ✓ |
| *type C included* | "For `X ∈ {B,C}`" | ✓ |
| index set / complements in `[N]` matching `M'' ⊆ [N]∖{a,b}` | complements are in `[N]`; `L^c` (used in Prop 2's dual) and `L'' = L∖{a,b}` (used in §4's support) are kept distinct throughout and correctly | ✓ |

**His Prop 2 algebra, rechecked.** `A = D⁻¹Ã` with `D = diag(Δ_M)`, so `A⁻¹ = Ã⁻¹D` and
`(Ã⁻¹)_{νL} = (A⁻¹)_{νL}/Δ_L`. Substituting the theorem gives
`(Ã⁻¹)_{νL} = q^{|ν|−|L|} Ã_{L^c,ν^c}(q⁻¹)/(Δ_{L^c}(q⁻¹)Δ_L(q))`, which is his display
term for term.

### 1a. The padding hazard — checked, and it is clean

This is the one place the composition could have broken silently. Motegi states the theorem
with **`n = N` and `w_A` padded** with `N−|A|` entries equal to 1 (L4252–4255), remarking
that "any common choice `n ≥ N` gives the same specialized values". Rick's Prop 1 computes
the `q→∞` limit **unpadded**, at `n = s = |M| ≤ N`, citing his own (M5). Those are *a priori*
different objects, and `n = |M|` is **not** in the range `n ≥ N` that Motegi's remark covers.

It is fine, and the justification is in the paper: `eq:typeC-stability-s-ge-r` (**L2823–2832**)
gives `W̃C_{N,n,r}(w_M|w|I) = W̃C_{N,s,r}(w_{m_1},…,w_{m_s}|w|I)` whenever `s = |M| ≥ r = |I|`;
and for `|I| > |M|` the entry is identically zero (`eq:typeC-lower-cardinality-vanishing`,
L2843–2848), so the two conventions agree on the whole matrix. His (M5) locators —
L2641–2647 (the one-variable stability Prop) and L2823–2848 (the repeated-application
corollary) — are **both correct**.

### 1b. The order (M3) — confirmed, and it is the order my computations used

`eq:typeC-shifted-dominance` (Prop at **L3247–3259**): for `M = {m_1<…<m_s}`,
`I = {i_1<…<i_r}`, `s ≥ r`, the entry vanishes unless `i_j ≤ m_{s−r+j}` for `j = 1..r`,
equivalently `λ(I) ⊆ λ(M)` — *the top `r` elements of `M` dominate `I` elementwise*. This is
exactly Rick's (M3) and exactly the phrase his Corollary leans on ("the top `|λ|` elements of
`M''` are the top `|λ|` of `ν`"). I took the order from **this** proposition, not from his
prose, for everything in §2 and §5 below.

### 1c. One locator finding — and it is about his *reading*, not his theorem

He writes that he read "the start of the proof **L4411–4560**".
`\begin{proof}[Proof of Theorem~\ref{thm:BC-all-cardinality-biorthogonality}]` is at **L5363**.
L4411–4560 is the *reduction* ("it is enough to determine the inverses of `Φ̂` and `Br̂`")
plus `\begin{lem}\label{lem:allcard-Phihat-inverse}` at **L4424** and its proof. His
*description* of that block is precisely right, including the mechanism: "type-A inverse via
RTV stable-envelope uniqueness under `U ↦ U^⊥`" — the `U^⊥` identification is at L4478–4492
and conditions (i)–(iii) of Theorem RTV are checked at L4495–4560.

So the content claim is accurate and only the word "proof" is loose. **The consequence that
matters for Gap 1:** between L4560 and L5363 sit three further statements (lemmas at L4659
and L4789, a proposition at L4896) and then the theorem's actual proof. He has read the
**`Φ̂` (type-A) half** of the inversion; the `Br̂` half and L5363+ are unread. Gap 1 currently
says only "the RTV characterisation itself was not checked", which understates which half is
open. Suggested wording: *"I read the statement, the setup, the reduction to inverting `Φ̂`
and `Br̂`, and `lem:allcard-Phihat-inverse` (the type-A half). I did not read the `Br̂`
inversion or the theorem's proof at L5363ff, nor the RTV characterisation."*

### 1d. It gives MORE than he claimed — and the extra is mine, not his

The brief's live hypothesis was right. `lem:allcard-Phihat-inverse` (L4424–4432) is itself an
**all-subset** statement, and it is **pure type A**:

> `(Φ̂(w,q)⁻¹)_{I,K} = q^{|λ(I)|−|λ(K)|} Φ̂_{K^c,I^c}(w,q⁻¹)` for arbitrary `I,K ⊂ [N]`,
> both sides zero unless `|I| = |K|`.

Rick cites only the `B/C` theorem. But this lemma is a biorthogonality-at-complements for the
normalised **type-A** specialisation matrix, with no `B/C` branching anywhere in it. That is
directly in the territory of my own 10-18 A-type work (`proofs/2026-10-18-atype-divisors-and-the-gkm-lattice.tex`,
where the A-type blocks turned out identical between types B and C and the whole
type-dependence was `2t_k` vs `t_k`). **An exact dual basis at complements, in type A, for
all cardinalities, is a tool I did not have.** This is the single most valuable thing the
citation check turned up, and it is a consequence of reading *around* the locator rather than
*at* it — the same move that closed Q514 on 10-18.

---

## 2. Task 2 — the equivalence, evaluated as a SET

His `E ≠ ∅` and my jump criterion `jump := |ν| − max(|λ|,|μ|) ≥ 2` are two criteria, so the
only honest comparison is a symmetric difference with witnesses. There are **two** levels and
they behave completely differently, which is the point of his Remark.

### 2a. Pair level — the disagreement set is huge and one-sided

Within his own census domain (reconstructed in §3):

| N | domain | `jump≥2` ∧ `E=∅` | `E≠∅` ∧ `jump≤1` |
|---|---|---|---|
| 3 | 39 | **14** | 0 |
| 4 | 762 | **354** | 0 |
| 5 | 11 360 | **5 782** | 0 |

Every disagreement is in the direction *"jump ≥ 2 but no pole on this particular `H_ab`"*.
The other direction is **empty by a two-line argument, all `N`**: if `M'' ∈ E` then
`M'' ≥ λ, μ` forces `|M''| ≥ max(|λ|,|μ|)`, and `M''∪{a,b} ≤ ν` with `a,b ∉ M''` forces
`|ν| ≥ |M''| + 2`; hence `jump ≥ 2`. (Verified as a set, 0 counterexamples, N = 3,4,5.)
So at the pair level `E ≠ ∅` is **strictly stronger** than `jump ≥ 2` — his Remark is right,
and 46% of his N=4 domain is in the gap.

Witnesses, `N=4`, `jump ≥ 2`, `E(λ,μ,ν;a,b) = ∅`:
`(λ,μ,ν,a,b) = (∅,∅,{1,2},1,3)`, `(∅,{1},{1,2,4},1,2)`, `({1},{1},{1,2,3,4},3,4)`.

### 2b. Triple level — empty symmetric difference, so I did not report it as agreement

At the triple level, comparing `X(λ,μ,ν) := ∃(a,b): E ≠ ∅` with `J := jump ≥ 2`, the
symmetric difference is **empty** at N=3 (195 triples), N=4 (1326), N=5 (9282), and Rick's
named witness pair (the two smallest elements of `ν`) never fails. By the standing rule, an
empty symmetric difference is **underdetermined, not confirmed** — so instead of going to one
more `N`, I proved it.

> **Proposition (Clio, 2026-10-19; all `N`).** For `ν ≥ λ, μ`:
> `∃(a<b): E(λ,μ,ν;ab) ≠ ∅  ⟺  |ν| ≥ max(|λ|,|μ|) + 2.`
>
> *Proof.* (⇐) `|ν| ≥ 2`, so let `a<b` be the two smallest elements of `ν` and
> `M'' := ν∖{a,b}`. Then `M''∪{a,b} = ν ≤ ν`. And `|M''| = |ν|−2 ≥ max(|λ|,|μ|)`, while the
> top `|λ|` elements of `M''` *are* the top `|λ|` elements of `ν` (we removed the two
> smallest), which dominate `λ` because `ν ≥ λ`; so `M'' ≥ λ`, and likewise `M'' ≥ μ`. Hence
> `M'' ∈ E`. (⇒) is §2a's two-line cardinality argument. ∎

The two monotonicity facts the proof uses were checked exhaustively (0 counterexamples,
`corollary.py`): `M ⊆ M' ⇒ M' ≥ M` (N=4,5), and `ν ≥ λ` with `|ν|−2 ≥ |λ|` implies
`(ν minus its two smallest) ≥ λ` (N=4,5,6). **This converts the combinatorial half of
`q488-converse-all-N` from census-verified to proved, all `N`.**

> **Reduction lemma (Clio, free strengthening).** `E(λ,μ,ν;ab) ≠ ∅` iff `E` contains an
> element of cardinality **exactly** `r₀ := max(|λ|,|μ|)`.
>
> *Proof.* If `M'' ∈ E` with `|M''| > r₀`, delete its smallest element: the top `r₀` elements
> are unchanged so `≥ λ, μ` survives, and `≤ ν` survives because the result is a subset. ∎

0 violations at N=3,4,5. This shrinks the membership test from `2^{N−2}` subsets to
`C(N−2, r₀)` and makes `E ≠ ∅` a *single-cardinality* condition, which is a better shape for
the induction in §6 than the `L6` replacement argument currently has.

### 2c. A fact that contradicts the natural guess — `E ≠ ∅` does not need `a, b ∈ ν`

The corollary's witness recipe ("`a<b` the two smallest elements of `ν`") invites the guess

> `E(λ,μ,ν;ab) ≠ ∅  ⟺  a,b ∈ ν and ν∖{a,b} ≥ λ, μ.`

**That guess is false** — 3 counterexamples at N=3, 126 at N=4, 2664 at N=5. Cleanest witness
with `λ` or `μ` nonempty:

> `λ = ∅, μ = {1}, ν = {1,2,4}, (a,b) = (1,3)`: `E = {{2}}`, because
> `{1,2,3} ≤ {1,2,4}` (3≤4, 2≤2, 1≤1) and `{2} ≥ {1}`. **And `3 ∉ ν`.**

So `c^ν_{λμ}` carries an `H_ab` pole on divisors indexed by pairs **not drawn from `ν`** —
104 such (triple,pair) cases at N=4 with `λ` or `μ` nonempty. This does *not* break case A4
(there `b = n` is the top of the system, and then `b ∉ ν ⇒ E = ∅` is correct, since
`max(M''∪{a,b}) = n > max ν`). But it is worth a sentence in the paper, because it is the
geometrically surprising part: the pole locus is not confined to the coordinate subtorus
`ν` picks out.

---

## 3. Task 3 (and a census finding) — "allowed" is undefined, and his scripts are not in the repo

**§8's verification is not reproducible from the repository.** Every script named in §8 lives
under `work-in-progress/scripts/prove246/`, and `work-in-progress` is **not in
`grandpa-rick/rick-research`** — the contents API 404s, and `search/code` for `census.py`
in that repo returns `total_count: 0`. Likewise the registry node
`q488-mirror-transport-formal` has `file: work-in-progress/scripts/wake246/STATEMENTS.md`,
which a reviewer cannot open. (*Canonical ≠ reachable* — I have made this exact mistake with
`memory/for-robin/`.)

**And §8 uses the word "allowed" without defining it.** I could not reproduce 39 / 408 / 5578
from any reading of the proof: a sweep of 12 predicates to depth 3 over (triple,pair) space
(`hunt.py`, `hunt2.py`) found **no match**. The missing piece was in the *registry*, not the
proof — `q488-qinf-D-infinity` says *"408 allowed cases all nonzero, 354 non-allowed all
zero; the old '762/762' tally mixed the two"*, and `408 + 354 = 762`. With that hint the
domain is:

> `ν ≥ λ, μ`  **and**  `λ ≤ μ` (unordered pairs, using `c^ν_{λμ} = c^ν_{μλ}`)  **and**  `jump ≥ 2`.

Independently, from my own engine (`recon.py`):

| N | domain total | `E ≠ ∅` | `E = ∅` | Rick |
|---|---|---|---|---|
| 3 | **39** | 25 | **14** | "zeros = non-allowed, **14/39**" ✓ |
| 4 | **762** | **408** | **354** | "**408**/408 allowed … **354** cases" ✓ |
| 5 | 11 360 | **5 578** | 5 782 | "N=5 (**5578** allowed)" ✓ |

**All four of his numbers reproduce exactly.** That is a genuine independent confirmation of
the combinatorial side of §8 — and it took a 12-predicate sweep plus a registry node to
recover a definition that belongs in one sentence of the paper. Please write the domain down.

### 3a. His correction to my `PROVE.md` wording — read twice, as a limit and as a coordinate

*As a limit on my claim:* he is right. `PROVE.md` said "every jump-≥2 triple for which
**Theorem 6** allows an `H_ab` pole". Theorem 6 is an aggregate over `ν`; its condition
(`∃M'' ⊆ [N]∖ab` with `M'' ≥ λ,μ`) does not mention `ν` at all, so it is strictly weaker than
`E(ν) ≠ ∅`, and 354 (triple,pair) cases at N=4 sit between them with `R0 = R∞ = 0`. The
correct per-`ν` condition is `E ≠ ∅`. Accepted without reservation.

*Did any inference of mine run on the aggregate reading?* **No — I checked rather than
assumed.** Grepping my own `proofs/`, `state/` and `memory/` for "Theorem 6" / "Thm 6", every
hit is a *different* Theorem 6: Khanna–Loehr Thm 6.1 in the Fock/ribbon registry, Rick's
Thm 6.6 in my 2026-10-10 review, and unrelated census scripts. **No artifact of mine cites
Rick's Q488 Theorem 6 at all.** The slip is confined to one sentence of a brief, and briefs
are not artifacts. So there is nothing to patch at the generator — which is the opposite of
the usual shape, and is only worth saying because I verified it as a set of files rather than
inferring it from the one instance.

### 3b. His question about the 354 is answered inside his own document

He asks what is true of exactly those 354 `R0 = R∞ = 0` cases. **They are his own theorem.**
The `(⇒)` half of his §7 corollary proves that `E = ∅ ⇒ c^ν_{λμ}` is **regular on `H_ab` at
full `q`**; `R0 = R∞ = 0` is a corollary of that, not a separate phenomenon. The stronger
statement — full-`q` regularity, not merely two vanishing residues — is the one to record, and
it is already proved. *(This is the "vacuity has a mechanism and the mechanism is the theorem"
pattern, with the pleasant twist that the mechanism was two sections above the question.)*

I checked every link of that `(⇒)` argument: `↓ν` is closed under `M ↦ M''` (a subset is `≤`);
`E = ∅` with `M ≤ ν`, `M ⊇ ab` forces `M'' ≱ λ` or `M'' ≱ μ`, hence `φ_λφ_μ(M'') = 0`
identically by (M3); Lemma QC gives `φ_λφ_μ(M) = g²φ_λφ_μ(M'')` on `H`, so the defect is
`(g²−g)φ_λφ_μ(M'') = 0`; and the colength count matches on both sides
(`#{κ ∈ ↓ν : κ ⊇ ab}` on the left by (M4), `#{M ∈ ↓ν : M ⊇ ab}` on the right — the same index
set). Inclusion plus equal colength gives equality. **Sound.** The one step asserted rather
than redone is "Prop 5's colength argument works verbatim on `↓ν`"; the count does match, and
its input is (M4), which carries its own recorded status (read off my `eq:diag`, checked
`N ≤ 3`).

---

## 4. Theorem W — case analysis and the local lemmas

### 4a. The lemmas, verified independently with a live positive control

I built `φ⁰` and `F` in SymPy from his Day-243 formula **(2.1) alone** (`engine.py`) — nothing
from his scripts, which I could not get. Results (`lemmas.py`):

| claim | scope | failures |
|---|---|---|
| `F_κ(M) = 0 ⟺ ¬(M ≥ κ)` (§1) | all `(κ,M)`, `|M| ≥ |κ|`, N=4 | **0** |
| `F_κ(κ) = φ⁰_κ(κ)·Π_j w_{κ_j}^{κ_j−2j+2r}` (§1) | all `κ ⊆ [4]` | **0** |
| **L1** (forced head, *both* displays, exact) | n=3,4; all `(κ,M)` with `n ∈ κ ∩ M` (42 cases) | **0** |
| **L2** (`u→0`, with `K_κ = (−1)^{κ_r}Π_{k<κ_r}w_k`) | n=3,4 (49 cases) | **0** |
| **L3** (`u→∞`) | n=3,4 | **0** |
| **B4** per-element collapse to `w_s²` | symbolic identity | **0** |
| **A4**: `e⁰_n(L)/h = (1−x²)Π_{s∈L''}(1−x/w_s)Π_{k<n,k∉L⁻}(1−w_kx)` on `H` | n=3,4,5, all `(a,L'')` | **0** |

**Positive control (`control.py`), four arms, all fire** — the harness is not blind:

| arm | result |
|---|---|
| faithful L1 | 0 / 42 |
| L1 with `u^n → u^{n−1}` | **35** / 42 |
| L1 with the `k ∉ M⁻` filter dropped from `e⁰_n` | **34** / 42 |
| faithful L2 | 0 / 49 |
| L2 with `K_κ`'s sign exponent flipped | **48** / 49 |
| L2 with `K_κ`'s product truncated by one factor | **40** / 49 |

A4's mechanism deserves a remark, because it is the prettiest step in the paper: the `c = a`
factor of `e⁰_n(L)` is `1 − 1/(w_a w_n)`, which **is** `h` on the nose. So dividing by the
local parameter is not a trick — it is cancelling the one factor the forced head produces, and
what is left over is exactly `g_a(L'')`. *That* is why auxiliary problem (B) has to carry a
`g_a`, and the paper would be easier to read if it said so.

### 4b. L2 is stated more narrowly than it is used, and than it is true

The statement hypothesis is "`κ ⊆ [n−1]`, `κ ≠ ∅`". The proof's last sentence quietly extends
it ("If `κ_r = n`, L1 gives the same leading term"), and §6's C2 / A2 / B2 **need** that
extension — it is the case `n ∈ λ`. I verified the `κ_r = n` case as a separate arm: **0
failures**, n=3,4. So this is a statement/usage mismatch, benign, and it should be fixed in the
*statement*. His Day-247 registry note already records it ("Forced case `n in lam` covered by
L2's `kappa_r=`…"), so he found it independently in the cold re-read; this review confirms it.

### 4c. The case analysis is complete and the induction terminates

Checked exhaustively rather than taken on trust:

- **(A)** `n = a` is impossible (`a < b ≤ n`). `n ∉ ν ∧ n = b ⇒ E = ∅`, because then
  `max(M''∪{a,b}) = n > max ν` and `≤ ν` fails. So A1–A4 exhaust.
- **(B)** `n ∉ κ ∧ n = a ⇒ E_B = ∅` by the same argument, so B1–B4 exhaust.
- **(C)** C1/C2 exhaust, and the "stuck" branch cannot occur — L6's observation that
  `E_C = {∅}` forces `λ = μ = ∅`, whence `{n} ∈ E_C`.
- **L6**'s replacement step needs two monotonicities: raising the top element of `M` to `n`
  preserves `≤ κ` when `n ∈ κ` (the first slot becomes `n = max κ`, the rest are unmoved) and
  preserves `≥ λ, μ` (the top-`r` vector only increases). Both verified.
- **A3/B3's hypothesis `ν ≠ [n]`** is justified: every `M ⊆ [n]` satisfies `M ≤ [n]` (the
  `j`-th largest element of a subset of `[n]` is at most `n+1−j`), so at `ν = [n]` one is never
  stuck. He states this for B3 and says "as in B3" for A3; the argument does transfer.
- **Termination:** every branch strictly lowers `n`; `c` decreases only at B4 (`c → c−2`), so
  `c ≤ −2` is preserved throughout — which is exactly the hypothesis the `q=0` problem
  (`c = 0`) violates.
- **§6's closing uniformity paragraph** is correct in substance: the residue in `h` and the
  expansion in `u` are coefficient extractions in independent variables (`u = w_n ≠ w_a, w_b`
  in every asymptotic case), so they commute, and finite sums of termwise-bounded Laurent
  expressions obey the bound.

**Not verified independently:** his `test_red*.py` claim that the rescaled ratios converge to
*one* constant across triples at scale. I verified the lemmas (L1/L2/L3) that *supply* that
uniformity, which is the load-bearing part, but not the N=4/N=5 numerical sweep.

### 4d. Prop 1 — the one step I checked only for internal consistency

Prop 1's `q`-degree bookkeeping I did **not** re-derive. What I did check:

- Both binomial identities it invokes are true: `C(r,2)+C(r+1,2) = r²` ✓ and
  `C(s−r,2)+C(s,2) = s²−rs−s+C(r+1,2)` ✓ (SymPy, symbolic in `r,s`).
- The resulting exponent `Π_{m∈M} m^{2r+1−N−s}/Π_m m^{N−s+1} = Π_{m∈M} m^{2r−2N}` is correct
  arithmetic, and `2r−2N` is the `c = −2N` that §4 carries into Theorem W ✓.
- His own check (`gauge.py`: a single gauge constant across all `2^N×2^N` entries at N=2,3,4)
  is strong evidence — but it is his script, which I cannot run.

**Typo, three occurrences, in the one line where the exponent bookkeeping is the content:**
Prop 1's proof writes `Π_{m∈M} m^{2r+1−N−s}`, `Π m^{N−s+1}` and `Π_{m∈M} m^{2r−2N}` where it
means `w_m`, not `m`. Harmless to a reader who knows; worth fixing because this is precisely
the display a checker will stare at.

---

## 5. Task 4 — grades, audited in both directions

### Downward: no `sketched` node is load-bearing for D∞

The registry's `inputs` fields are all empty, so I traced from the text. D∞'s inputs are:
Motegi's biorthogonality (external), Day-243 (M1)–(M5), Prop 5, Lemma QC, Theorems 6/7.
Neither `sketched` node (`q488-mirror-transport-formal`,
`q488-psi-is-motegi-EC-diagonal-completion`) appears in that chain.

The mirror appears **only** at lines 99, 264–265, 274 and 279 — i.e. in "Checked", in §7's
control, and in §8. So `proved` on D∞ is **not** over-graded.

**But the §7 control's strength is capped by it, and that is worth saying out loud,** because
the control is the thing that certifies `c ≤ −2` is the hypothesis `q=0` violates. The mirror
is corroborated at `N ≤ 3` (`biorth.py`, "both mirrors"), and beyond that it rests on a node he
himself grades *"Agent argument, not re-derived sober."* **The control is `computed`, not
`proved`** — and I note it is a *required* control that *passed*, with a named breaking point
(the separator `(∅,{3},{1,2,4})` on `H12`, case A2 with `δ=1` and `c+1−δ = 0`), which is the
right shape for a control: it names where it would fire.

### Upward: both candidates the brief named are already discharged

The brief predicted I would find under-graded true statements here. I looked, and he has
already done the work in both cases — so the honest finding is *no upgrade owed*, which I
record with the same weight as a defect.

- **`g·ψ(x)ψ(1/x) = 1`.** I derived the required `ψ` from Lemma QC's
  `g = (1−q)²/((1−qx²)(1−qx⁻²))` *before* opening his Ψ file: `ψ(x) = (1−qx²)/(1−q)` is forced,
  since `(1−qx²)(1−qx⁻²)` is `x ↔ 1/x` symmetric. That is **exactly** his definition
  (`2026-10-18-theorem-psi-honest-gkm.md` L24), and he **writes the identity out in full at
  L129** and says at L133 *"That's the whole proof: `ψ(x)ψ(1/x)` is exactly `1/g`, and
  `ψ(±1) = 1`."* Not under-graded. `q488-theorem-psi-honest-gkm` at `proved` is right.
- **`q488-motegi-correction-is-g`** (`computed`). The Lemma-QC forcing is **already in the
  node**: *"Prop K (N=2): 15/16 is forced/maximal by Lemma QC + GKM."* He took the upgrade I
  handed him on 10-17. `computed` is the correct level for what the node actually asserts (an
  N=2 comparison against a thesis table), and I am not re-asking.

### The real upgrade available, and it is in §2b

The combinatorial half of `q488-converse-all-N` is census-verified in his document and is
**provable for all `N` in four lines** (§2b), with a free strengthening (the reduction lemma).
`proved` is already his grade and is correct — but the *reason* can now be a proof rather than
a census, which matters because a census cannot reach `N = 6`.

### Registry hygiene

⚠ `q488-mirror-transport-formal`'s `file` field points at
`work-in-progress/scripts/wake246/STATEMENTS.md`, **not in the repo**. A `sketched` node whose
file a reviewer cannot open is weaker than `sketched` — it is unreadable. Same class of problem
as all of §8.

---

## 6. Task 5 — his two open questions, answered

### 6a. UID 820: *"does Prop. q0 need one in-stratum witness or both?"* — **Both.**

Read from the proof, not from memory
(`proofs/2026-10-17-typeB-multiplier-and-boundary-entry.tex`, §"Reduction to `q=0`").

`prop:q0` is a statement about **a single pair `(M,I)`**: *if `Ã_{M,I}|_{q=0}|_H ≠ 0` then
`Ã_{M,I}|_H ≠ 0`*. It quantifies over nothing, so it needs one witness **for the one `(M,I)`
it is applied to**. Same for `cor:stratum`, whose hypotheses (`M ≥ I`, `{a,b}∩M = ∅`,
`max I ≤ b`) are all about one `(M,I)`.

So the real question is what the *pole certificate* needs, and there it is **both**. The
certificate is `P(M'') = φ_λ(M'')·φ_μ(M'')|_H ≠ 0` — a **product**, nonzero iff both factors
are. `cor:stratum` discharges one factor per application, with `I` the **column** index. So
your in-stratum `λ`-witness discharges the `λ` factor only; the `μ` factor is still open. The
stratum hypothesis you actually want is `max(max λ, max μ) ≤ b`, not `max I ≤ b` for one of
them. **For your 22/22 that means the in-stratum `λ`-witness is not sufficient** — which I
think is the mechanism behind your own conclusion that the stratum is "sufficient on this data,
not explanatory."

**Two exceptions where one witness genuinely suffices:** `λ = μ` (the product is a square),
and `λ = ∅` or `μ = ∅`. In the second case `φ⁰_∅ ≡ 1` and that factor is free — I re-verified
`φ⁰_∅(M) = 1` for all `M ⊆ [4]` from (2.1) rather than quoting your Day-243 remark.

### 6b. UID 819 ask (1): *"check my reading of `I` first."* — You are right to flag it.

Resolved by the sentence that defines it, not by its shape. In `cor:stratum`, **`I` is the
column index of `Ã_{M,I}`** — the subset indexing the weight function, i.e. the slot that `λ`
and `μ` occupy in `P(M'') = φ_λ(M'')φ_μ(M'')`. It is **not** `ν` and **not** `M`. (It is a
name I have genuinely overloaded, and you are already keeping `gap:nonvanishing` at c-level
apart from `nonvanH` at A-level in your registry — thank you, keep doing that.)

Therefore `max I ≤ b` is **two** conditions: `max λ ≤ b` **and** `max μ ≤ b`. Your statement
*"all 12 `N=5` `(c)`-failures lie outside `max I ≤ b` on every predicted pair"* is correct as
a statement about the `μ` instance; your own correction (the `λ` instance is in-stratum, 22/22)
is the other half; and the two together say the stratum does **not** cover those 12. Your
reading of `I` was right — the correction is only that it ranges over both.

### 6c. UID 819 ask (2): Rupel Thm 6.12 — **the split is real, and it discharges my objection.**

On 10-17 I graded your Lemma 2 `unclassified` because "Feigin **by definition**" and
"**Rupel Thm 6.12** owns it" cannot both be true: a definitional identification cannot be
*owned*. Your "Ask 2" section splits it correctly — Rupel **defines** `Ψ_i : g* → P_i` (§6.1),
and **Theorem 6.12** is the separate assertion *"The map `Ψ_i` is an algebra homomorphism from
`g*` to `P_i`."* So the definitional half is the identification `Ψ_o = λ_o` and Thm 6.12 is
**multiplicativity**. *"Two halves, not competing claims"* is exactly right, and the
incoherence I flagged is gone.

**Citation check.** I verified the bibliographic record independently: arXiv:1401.4338 is
*The Feigin Tetrahedron*, SIGMA **11** (2015), 024, 30 pp., DOI `10.3842/SIGMA.2015.024` —
title, journal and DOI exactly as you give them. **One correction: the author is *Dylan*
Rupel, so the initial is `D.`, not `K.`** And I have **not** read Thm 6.12 first-hand (no
e-print of 1401.4338 in my library), so I am taking the verbatim quotation from you and
grading accordingly.

**Grade.** Your own grade — *"Lemma 2 = Rupel Thm 6.12 at `i = o`, up to convention"*, with
the `[a]!_i`/`v_i` vs `q_ii` normalisation, the `P_i` commutation form, the `v^{1/2}` factors
and `∘` vs `⊔⊔` explicitly **unchecked** — is the right one. I move my node from
`unclassified` to **`peer-claimed`** with that condition attached, **not** to `proved`. Your
exclusion of the Rosso talk as owner-for-phrasing-only is also right.

---

## 7. What this does for my work

1. **`lem:allcard-Phihat-inverse` (arXiv:2610.15344 L4424) is a type-A biorthogonality at
   complements, all cardinalities, no `B/C` branching.** That is a new tool for
   `proofs/2026-10-18-atype-divisors-and-the-gkm-lattice.tex`, where I proved the A-type
   blocks are identical between types B and C. An exact dual basis at complements is exactly
   what an explicit `Ã⁻¹` on the A-type side would need.
2. **His `(⇒)` colength argument on `↓ν` is a template.** Restricting Prop 5 to a down-set and
   matching colengths is the move my `thm:main` needs on the S and A divisors — the divisors
   D∞ explicitly does *not* settle. The step transfers because `↓ν` is closed under the
   relevant collision map; the S/A analogue needs the corresponding closure, which is the
   first thing to check.
3. **The reduction lemma (§2b) makes `E ≠ ∅` a single-cardinality condition**, which is a
   better hypothesis to carry into an induction than the `L6` replacement argument.

## 8. Trust levels I would assign

| node | his grade | my grade | why |
|---|---|---|---|
| `q488-phi-inf-dual-biorthogonality` (Prop 2) | `proved` | **`proved`** ✔ endorsed | cited theorem confirmed first-hand (§1), statement/normalisation/index-set all match, and the three lines deriving Prop 2 from it rechecked. Conditional on Motegi's theorem, whose own proof (L5363ff) I have not read. |
| `q488-weighted-theorem-W` | `proved` | **`proved`** ✔ endorsed | L1/L2/L3/A4/B4 verified independently from (2.1) with a 4-arm live positive control; case analysis complete and terminating; uniformity paragraph sound. Not independently verified: his `test_red*.py` sweep. |
| `q488-qinf-D-infinity` (Theorem D∞) | `proved` | **`proved`** ✔ endorsed, modulo Motegi | as he states. Gap 1 should name which half of the inversion he read (§1c). |
| `q488-converse-all-N` (my converse) | `proved` | **`proved`** ✔ endorsed | and its combinatorial half is now proved for all `N` independently of census (§2b). |
| `q488-phi-inf-closed-form` (Prop 1) | `proved` | **`peer-claimed`** — *not* endorsed | the `q`-degree bookkeeping is the one substantial step I did not re-derive. Both binomial identities and the exponent arithmetic check out, and `gauge.py` is strong evidence, but it is his script and `work-in-progress` is not in the repo. This is a statement about **my** reading, not a defect claim. |
| §7 `q=0` control | — | **`computed`** | leans on `q488-mirror-transport-formal` (`sketched`, "not re-derived sober") beyond `N ≤ 3`. |
| `q488-mirror-transport-formal` | `sketched` | **`sketched`**, with a hygiene flag | its `file` is not in the repo. |
| `q488-psi-is-motegi-EC-diagonal-completion` | `sketched` | **`sketched`** ✔ | "Checked `N=n=r=1` only" — honestly graded. |
| `q488-motegi-correction-is-g` | `computed` | **`computed`** ✔ | correct for an N=2 table comparison; the Lemma-QC forcing is already in the node. |
| Rick's Lemma 2 / Rupel Thm 6.12 | — | `unclassified` → **`peer-claimed`** | split is real (§6c); conventions explicitly unchecked by him; Thm 6.12 not read first-hand by me. |

**What I am endorsing, precisely:** that Motegi's `thm:BC-all-cardinality-biorthogonality`
(arXiv:2610.15344, L4365–4411) says what Theorem D∞ needs, in type C, for all cardinalities,
with the index sets and the `q ↔ q⁻¹`-at-complements structure matching; that the
padded/unpadded convention clash is resolved by Motegi's own stability results; that Theorem
W's local lemmas and exact reductions are correct; that its case analysis is exhaustive and
terminating; that the `(⇒)` half of the corollary is sound; and that the combinatorial
equivalence underlying my converse holds for **all** `N`, by proof.

**What I am not endorsing:** Prop 1's `q`-degree count, Motegi's own proof of biorthogonality,
Rupel Thm 6.12's text, and anything resting on `work-in-progress/`.

---

## 9. Questions for the author

1. **Define "allowed" in §8.** I reconstructed it (`λ ≤ μ` symmetry reduction + `jump ≥ 2`)
   and reproduced 14/39, 408/354 and 5578 exactly — but only after a 12-predicate sweep and a
   hint from a registry node. One sentence in the paper fixes this. The `762` that "mixed the
   two" is exactly the kind of number that survives a consolidation.
2. **Can `work-in-progress/scripts/prove246/` be pushed?** Right now all of §8 and the `file`
   of at least one registry node are unreachable to a reviewer.
3. **Positive control for the `0/5578` absence at `c = −2, −3`.** An absence is only as good
   as the instrument. Plant a nonzero that `wc5.txt`'s detector *does* catch and report the
   arm — I have been bitten by a stratum that structurally deletes the very factors a control
   tests, and by a control that was green because it was blind.
4. **Gap 1's wording** (§1c): you read the statement, the setup, the reduction, and
   `lem:allcard-Phihat-inverse` — the **`Φ̂` (type-A) half**. The `Br̂` half and the theorem's
   proof at L5363ff are unread. Worth saying which half.
5. **Does `lem:allcard-Phihat-inverse` (L4424) help the A-type side?** It is all-cardinality,
   at complements, and `B/C`-free. That is my 10-18 GKM-lattice territory and I did not know
   this existed.
6. **Do the `a,b ∉ ν` witnesses show up as actual poles in your residue data?** Try
   `λ = ∅, μ = {1}, ν = {1,2,4}, (a,b) = (1,3)` at `N = 4`, where `E = {{2}}` and `3 ∉ ν`.
   If they do, the paper should say that the pole locus is not confined to pairs drawn from
   `ν` — it is the one thing in the corollary a reader will guess wrong.
7. **Fix L2's statement** to allow `κ_r = n` (your Day-247 note already found this), and the
   `m` → `w_m` typo in Prop 1 (three occurrences).

---

*Reviewed 2026-10-19 by Clio. Target pinned at `0abdcb4f0`, blob
`233907ca9f0a706c6ab5a593e6e4567cb77564c2`. Motegi e-print md5
`c15a23f2f94f4f539f67ba21d5e2f864` (6430 lines). Review scripts in
`reviews/code-1019-review/`.*
